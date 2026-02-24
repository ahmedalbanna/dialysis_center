// Invoice Form Enhancement
// Features: Payment status tracker, printable invoice preview, payment recording

frappe.ui.form.on('Invoice', {
	onload: function(frm) {
		frm.set_intro(__('Manage billing for dialysis services'));
		
		// Load invoice status
		update_invoice_indicator(frm);
	},
	
	refresh: function(frm) {
		// Update payment status indicator
		update_invoice_indicator(frm);
		update_payment_status_ui(frm);
		
		// Show payment progress
		if (!frm.is_new()) {
			show_payment_progress(frm);
		}
		
		// Add invoice actions
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Print Invoice'), function() {
				print_invoice(frm);
			}, __('Actions'));
			
			// Add payment recording button
			if (frm.doc.payment_status !== 'Paid') {
				frm.add_custom_button(__('Record Payment'), function() {
					show_payment_dialog(frm);
				}, __('Actions'));
			}
			
			// Add email button
			frm.add_custom_button(__('Send Invoice'), function() {
				send_invoice_email(frm);
			}, __('Actions'));
			
			// Add refund button if paid
			if (frm.doc.payment_status === 'Paid') {
				frm.add_custom_button(__('Refund'), function() {
					show_refund_dialog(frm);
				}, __('Actions'));
			}
		}
		
		// Add draft invoice actions
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Preview'), function() {
				preview_invoice(frm);
			}, __('Actions'));
		}
	},
	
	validate: function(frm) {
		// Validate required fields
		if (!frm.doc.patient) {
			frappe.throw(__('Patient is required'));
		}
		
		if (!frm.doc.invoice_date) {
			frappe.throw(__('Invoice date is required'));
		}
		
		if (!frm.doc.items || frm.doc.items.length === 0) {
			frappe.throw(__('At least one item is required'));
		}
		
		// Validate invoice items
		let total = 0;
		for (let i = 0; i < frm.doc.items.length; i++) {
			const item = frm.doc.items[i];
			
			if (!item.description) {
				frappe.throw(__('Row {0}: Description is required', [i + 1]));
			}
			
			if (!item.quantity || item.quantity <= 0) {
				frappe.throw(__('Row {0}: Quantity must be positive', [i + 1]));
			}
			
			if (!item.rate || item.rate < 0) {
				frappe.throw(__('Row {0}: Rate must be non-negative', [i + 1]));
			}
			
			total += item.quantity * item.rate;
		}
		
		// Validate total
		if (total <= 0) {
			frappe.throw(__('Invoice total must be greater than zero'));
		}
	},
	
	before_save: function(frm) {
		// Calculate totals
		calculate_invoice_totals(frm);
	},
	
	after_save: function(frm) {
		frappe.msgprint(__('Invoice saved successfully'));
	},
	
	// Field-level events
	patient: function(frm) {
		if (frm.doc.patient) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Patient',
					filters: { name: frm.doc.patient },
					fieldname: ['patient_name', 'email', 'phone']
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('patient_name', r.message.patient_name);
						frm.set_value('patient_email', r.message.email);
						frm.set_value('patient_phone', r.message.phone);
					}
				}
			});
		}
	},
	
	appointment: function(frm) {
		// Load appointment details
		if (frm.doc.appointment) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Appointment',
					filters: { name: frm.doc.appointment },
					fieldname: ['appointment_date', 'patient']
				},
				callback: function(r) {
					if (r.message && !frm.doc.invoice_date) {
						frm.set_value('invoice_date', r.message.appointment_date);
					}
				}
			});
		}
	},
	
	invoice_date: function(frm) {
		// Set due date automatically
		if (frm.doc.invoice_date && !frm.doc.due_date) {
			const due_date = frappe.datetime.add_days(frm.doc.invoice_date, 30);
			frm.set_value('due_date', due_date);
		}
	}
});

// Invoice List View Customization
frappe.listview_settings['Invoice'] = {
	add_fields: ['patient_name', 'invoice_date', 'total_amount', 'payment_status', 'outstanding_amount'],
	
	formatters: {
		payment_status: function(value) {
			const colors = {
				'Unpaid': 'red',
				'Partial': 'orange',
				'Paid': 'green'
			};
			
			return `<span style="background-color: ${colors[value] || 'white'}; color: white; padding: 4px 8px; border-radius: 3px; font-weight: bold;">${value}</span>`;
		},
		
		total_amount: function(value) {
			return frappe.format(value, { fieldtype: 'Currency' });
		},
		
		outstanding_amount: function(value) {
			const color = value > 0 ? '#f5222d' : '#52c41a';
			return `<span style="color: ${color}; font-weight: bold;">${frappe.format(value, { fieldtype: 'Currency' })}</span>`;
		},
		
		invoice_date: function(value) {
			return frappe.datetime.str_to_user(value);
		}
	},
	
	filters: [
		['docstatus', '!=', 0]  // Only show submitted invoices
	],
	
	onload: function(listview) {
		// Add payment status filter
		listview.page.add_action_item(__('Unpaid'), function() {
			listview.filter_area.add([
				['Invoice', 'payment_status', '=', 'Unpaid']
			]);
			listview.refresh();
		});
		
		// Add due date filter
		listview.page.add_action_item(__('Overdue'), function() {
			listview.filter_area.add([
				['Invoice', 'due_date', '<', frappe.datetime.now_date()],
				['Invoice', 'payment_status', '!=', 'Paid']
			]);
			listview.refresh();
		});
		
		// Bulk payment recording
		listview.page.add_menu_item(__('Record Payments'), function() {
			const selected = listview.get_checked_items();
			if (selected.length === 0) {
				frappe.msgprint(__('Please select invoices'));
				return;
			}
			
			show_bulk_payment_dialog(selected.map(d => d.name));
		});
	}
};

// Helper functions

function update_invoice_indicator(frm) {
	const status_colors = {
		'Unpaid': 'red',
		'Partial': 'orange',
		'Paid': 'green'
	};
	
	const color = status_colors[frm.doc.payment_status] || 'gray';
	frm.page.set_indicator(__(frm.doc.payment_status || 'Draft'), color);
}

function calculate_invoice_totals(frm) {
	let subtotal = 0;
	
	// Calculate subtotal from items
	if (frm.doc.items) {
		subtotal = frm.doc.items.reduce((sum, item) => {
			return sum + (item.quantity * item.rate);
		}, 0);
	}
	
	frm.set_value('subtotal', subtotal);
	
	// Calculate tax
	const tax_amount = subtotal * (frm.doc.tax_rate || 0) / 100;
	frm.set_value('tax_amount', tax_amount);
	
	// Calculate discount
	let discount_amount = 0;
	if (frm.doc.discount_type === 'Fixed') {
		discount_amount = frm.doc.discount_value || 0;
	} else if (frm.doc.discount_type === 'Percentage') {
		discount_amount = subtotal * (frm.doc.discount_value || 0) / 100;
	}
	frm.set_value('discount_amount', discount_amount);
	
	// Calculate total
	const total = subtotal + tax_amount - discount_amount;
	frm.set_value('total_amount', total);
	
	// Calculate outstanding (if not paid)
	const paid = frm.doc.paid_amount || 0;
	frm.set_value('outstanding_amount', Math.max(0, total - paid));
}

function show_payment_status_ui(frm) {
	if (frm.is_new()) return;
	
	// Show payment progress
	const paid = frm.doc.paid_amount || 0;
	const total = frm.doc.total_amount || 0;
	const percentage = total > 0 ? (paid / total) * 100 : 0;
	
	const status_html = `
		<div class="payment-status" style="margin: 15px 0; padding: 15px; background: #f5f5f5; border-radius: 5px;">
			<div style="margin-bottom: 10px;">
				<small style="color: #666;">Payment Status</small>
				<div style="font-size: 18px; font-weight: bold;">${frm.doc.payment_status}</div>
			</div>
			<div class="progress" style="margin: 10px 0; height: 20px;">
				<div class="progress-bar" style="width: ${percentage}%; background-color: ${percentage === 100 ? '#52c41a' : percentage > 50 ? '#faad14' : '#f5222d'}; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;">
					${Math.round(percentage)}%
				</div>
			</div>
			<div class="row" style="font-size: 12px;">
				<div class="col-sm-3">
					<small>Total</small><br/>
					<strong>${frappe.format(total, { fieldtype: 'Currency' })}</strong>
				</div>
				<div class="col-sm-3">
					<small>Paid</small><br/>
					<strong style="color: #52c41a;">${frappe.format(paid, { fieldtype: 'Currency' })}</strong>
				</div>
				<div class="col-sm-3">
					<small>Outstanding</small><br/>
					<strong style="color: #f5222d;">${frappe.format(Math.max(0, total - paid), { fieldtype: 'Currency' })}</strong>
				</div>
				<div class="col-sm-3">
					<small>Due Date</small><br/>
					<strong>${frm.doc.due_date ? frappe.datetime.str_to_user(frm.doc.due_date) : '-'}</strong>
				</div>
			</div>
		</div>
	`;
	
	$(frm.wrapper).find('.payment-status').remove();
	$(frm.fields_dict.patient_name.wrapper).after(status_html);
}

function show_payment_progress(frm) {
	// Fetch payment records
	frappe.call({
		method: 'dialysis_center.api.invoice.get_payment_history',
		args: {
			invoice: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.payments) {
				const payments = r.message.payments;
				
				if (payments.length === 0) {
					return;
				}
				
				const payments_html = `
					<div class="payment-history" style="margin: 15px 0; padding: 15px; background: #f9f9f9; border-radius: 5px;">
						<h6>Payment History</h6>
						<table class="table table-sm" style="margin: 0;">
							<thead>
								<tr>
									<th>Date</th>
									<th>Amount</th>
									<th>Method</th>
									<th>Reference</th>
								</tr>
							</thead>
							<tbody>
								${payments.map(p => `
									<tr>
										<td>${frappe.datetime.str_to_user(p.payment_date)}</td>
										<td>${frappe.format(p.amount, { fieldtype: 'Currency' })}</td>
										<td>${p.payment_method}</td>
										<td>${p.reference_number || '-'}</td>
									</tr>
								`).join('')}
							</tbody>
						</table>
					</div>
				`;
				
				$(frm.wrapper).find('.payment-history').remove();
				$(frm.wrapper).find('.payment-status').after(payments_html);
			}
		}
	});
}

function show_payment_dialog(frm) {
	const outstanding = frm.doc.outstanding_amount || 0;
	
	const dialog = new frappe.ui.Dialog({
		title: __('Record Payment'),
		fields: [
			{
				fieldtype: 'Currency',
				fieldname: 'amount',
				label: __('Amount Paid'),
				default: outstanding,
				reqd: 1
			},
			{
				fieldtype: 'Date',
				fieldname: 'payment_date',
				label: __('Payment Date'),
				default: frappe.datetime.now_date(),
				reqd: 1
			},
			{
				fieldtype: 'Select',
				fieldname: 'payment_method',
				label: __('Payment Method'),
				options: '\nCash\nBank Transfer\nCard\nCheck\nOther',
				reqd: 1
			},
			{
				fieldtype: 'Data',
				fieldname: 'reference_number',
				label: __('Reference Number')
			},
			{
				fieldtype: 'Text',
				fieldname: 'notes',
				label: __('Notes')
			}
		],
		primary_action_label: __('Record Payment'),
		primary_action(values) {
			// Validate amount
			if (values.amount > outstanding) {
				frappe.msgprint({
					title: __('Amount Exceeds Outstanding'),
					message: __('Payment amount exceeds outstanding amount of {0}', 
						[frappe.format(outstanding, { fieldtype: 'Currency' })])
				});
				return;
			}
			
			frappe.call({
				method: 'dialysis_center.api.invoice.record_payment',
				args: {
					invoice: frm.doc.name,
					payment: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Payment recorded successfully'));
						
						// Update invoice
						const new_paid = (frm.doc.paid_amount || 0) + values.amount;
						frm.set_value('paid_amount', new_paid);
						
						// Update payment status
						if (new_paid >= frm.doc.total_amount) {
							frm.set_value('payment_status', 'Paid');
						} else if (new_paid > 0) {
							frm.set_value('payment_status', 'Partial');
						}
						
						frm.save();
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function show_bulk_payment_dialog(invoices) {
	const dialog = new frappe.ui.Dialog({
		title: __('Record Bulk Payments'),
		fields: [
			{
				fieldtype: 'Date',
				fieldname: 'payment_date',
				label: __('Payment Date'),
				default: frappe.datetime.now_date(),
				reqd: 1
			},
			{
				fieldtype: 'Select',
				fieldname: 'payment_method',
				label: __('Payment Method'),
				options: '\nCash\nBank Transfer\nCard\nCheck\nOther',
				reqd: 1
			},
			{
				fieldtype: 'Data',
				fieldname: 'reference_number',
				label: __('Reference Number')
			},
			{
				fieldtype: 'Currency',
				fieldname: 'total_amount',
				label: __('Total Payment Amount'),
				reqd: 1
			}
		],
		primary_action_label: __('Record Payments'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.invoice.record_bulk_payments',
				args: {
					invoices: invoices,
					payment: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Payments recorded for {0} invoices', 
							[r.message.count]));
						dialog.hide();
						cur_list.refresh();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function print_invoice(frm) {
	const print_url = `/app/invoice/${frm.doc.name}`;
	frappe.print(print_url, print_settings = {
		with_border: 1
	});
}

function preview_invoice(frm) {
	// Create preview dialog
	const dialog = new frappe.ui.Dialog({
		title: __('Invoice Preview'),
		size: 'large',
		static: true,
		fields: [
			{
				fieldtype: 'HTML',
				fieldname: 'preview_html',
				html: render_invoice_preview(frm)
			}
		]
	});
	
	dialog.show();
}

function render_invoice_preview(frm) {
	const items_html = (frm.doc.items || []).map(item => `
		<tr>
			<td>${item.description}</td>
			<td style="text-align: right;">${item.quantity}</td>
			<td style="text-align: right;">${frappe.format(item.rate, { fieldtype: 'Currency' })}</td>
			<td style="text-align: right;">${frappe.format(item.quantity * item.rate, { fieldtype: 'Currency' })}</td>
		</tr>
	`).join('');
	
	return `
		<div style="background: white; padding: 30px; font-family: Arial, sans-serif;">
			<!-- Header -->
			<div style="display: flex; justify-content: space-between; margin-bottom: 30px;">
				<div>
					<h2 style="margin: 0;">INVOICE</h2>
					<p style="margin: 5px 0; color: #666;">${frm.doc.name}</p>
				</div>
				<div style="text-align: right;">
					<strong>Invoice Date:</strong> ${frappe.datetime.str_to_user(frm.doc.invoice_date)}<br/>
					<strong>Due Date:</strong> ${frm.doc.due_date ? frappe.datetime.str_to_user(frm.doc.due_date) : '-'}
				</div>
			</div>
			
			<!-- Bill To -->
			<div style="margin-bottom: 30px;">
				<h6>Bill To:</h6>
				<div>${frm.doc.patient_name}</div>
				${frm.doc.patient_email ? `<div>${frm.doc.patient_email}</div>` : ''}
				${frm.doc.patient_phone ? `<div>${frm.doc.patient_phone}</div>` : ''}
			</div>
			
			<!-- Items -->
			<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
				<thead>
					<tr style="border-bottom: 2px solid #333;">
						<th style="text-align: left; padding: 10px; font-weight: bold;">Description</th>
						<th style="text-align: right; padding: 10px; font-weight: bold;">Quantity</th>
						<th style="text-align: right; padding: 10px; font-weight: bold;">Rate</th>
						<th style="text-align: right; padding: 10px; font-weight: bold;">Amount</th>
					</tr>
				</thead>
				<tbody>
					${items_html}
				</tbody>
			</table>
			
			<!-- Totals -->
			<div style="float: right; width: 300px; margin-top: 20px;">
				<table style="width: 100%; border-collapse: collapse;">
					<tr>
						<td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Subtotal:</strong></td>
						<td style="text-align: right; padding: 8px; border-bottom: 1px solid #ddd;">${frappe.format(frm.doc.subtotal, { fieldtype: 'Currency' })}</td>
					</tr>
					${frm.doc.tax_amount > 0 ? `
						<tr>
							<td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Tax (${frm.doc.tax_rate}%):</strong></td>
							<td style="text-align: right; padding: 8px; border-bottom: 1px solid #ddd;">${frappe.format(frm.doc.tax_amount, { fieldtype: 'Currency' })}</td>
						</tr>
					` : ''}
					${frm.doc.discount_amount > 0 ? `
						<tr>
							<td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Discount:</strong></td>
							<td style="text-align: right; padding: 8px; border-bottom: 1px solid #ddd;">-${frappe.format(frm.doc.discount_amount, { fieldtype: 'Currency' })}</td>
						</tr>
					` : ''}
					<tr>
						<td style="padding: 12px; background: #f5f5f5; font-weight: bold; font-size: 16px;">Total:</td>
						<td style="text-align: right; padding: 12px; background: #f5f5f5; font-weight: bold; font-size: 16px;">${frappe.format(frm.doc.total_amount, { fieldtype: 'Currency' })}</td>
					</tr>
				</table>
			</div>
			
			<div style="clear: both;"></div>
		</div>
	`;
}

function send_invoice_email(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Send Invoice'),
		fields: [
			{
				fieldtype: 'Data',
				fieldname: 'recipient_email',
				label: __('Recipient Email'),
				default: frm.doc.patient_email,
				reqd: 1
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'message',
				label: __('Message')
			}
		],
		primary_action_label: __('Send'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.invoice.send_invoice_email',
				args: {
					invoice: frm.doc.name,
					recipient_email: values.recipient_email,
					message: values.message
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Invoice sent successfully'));
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function show_refund_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Record Refund'),
		fields: [
			{
				fieldtype: 'Currency',
				fieldname: 'refund_amount',
				label: __('Refund Amount'),
				reqd: 1
			},
			{
				fieldtype: 'Date',
				fieldname: 'refund_date',
				label: __('Refund Date'),
				default: frappe.datetime.now_date(),
				reqd: 1
			},
			{
				fieldtype: 'Text',
				fieldname: 'reason',
				label: __('Reason'),
				reqd: 1
			}
		],
		primary_action_label: __('Process Refund'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.invoice.process_refund',
				args: {
					invoice: frm.doc.name,
					refund: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Refund processed successfully'));
						frm.reload_doc();
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}
