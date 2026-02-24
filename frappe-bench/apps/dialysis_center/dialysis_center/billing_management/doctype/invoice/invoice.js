frappe.ui.form.on('Invoice', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add payment button
			if (frm.doc.payment_status !== 'Paid' && frm.doc.docstatus === 1) {
				frm.add_custom_button(__('Record Payment'), function() {
					frm.trigger('record_payment');
				}).addClass('btn-primary');
			}
			
			// Add print button
			frm.add_custom_button(__('Print Invoice'), function() {
				frm.print_doc();
			});
			
			// Show payment status
			frm.trigger('show_payment_info');
		}
		
		// Set indicator
		frm.trigger('set_status_indicator');
	},
	
	record_payment: function(frm) {
		frappe.new_doc('Payment', {
			invoice: frm.doc.name,
			patient: frm.doc.patient,
			patient_name: frm.doc.patient_name,
			amount: frm.doc.outstanding_amount
		});
	},
	
	show_payment_info: function(frm) {
		let payment_html = `
			<div class="payment-summary" style="padding: 15px; background: #f8f9fa; border-radius: 5px; margin: 10px 0;">
				<div class="row">
					<div class="col-sm-4">
						<h6>${__('Total Amount')}</h6>
						<h4>${format_currency(frm.doc.total_amount || 0)}</h4>
					</div>
					<div class="col-sm-4">
						<h6>${__('Amount Paid')}</h6>
						<h4 style="color: green;">${format_currency(frm.doc.amount_paid || 0)}</h4>
					</div>
					<div class="col-sm-4">
						<h6>${__('Outstanding')}</h6>
						<h4 style="color: ${(frm.doc.outstanding_amount || 0) > 0 ? 'red' : 'green'};">
							${format_currency(frm.doc.outstanding_amount || 0)}
						</h4>
					</div>
				</div>
			</div>
		`;
		
		frm.dashboard.add_comment(payment_html, true);
	},
	
	set_status_indicator: function(frm) {
		const status_colors = {
			'Draft': 'gray',
			'Unpaid': 'red',
			'Partially Paid': 'orange',
			'Paid': 'green',
			'Cancelled': 'red'
		};
		
		if (frm.doc.payment_status) {
			frm.page.set_indicator(frm.doc.payment_status, status_colors[frm.doc.payment_status] || 'blue');
		}
	},
	
	before_save: function(frm) {
		frm.trigger('calculate_totals');
	},
	
	calculate_totals: function(frm) {
		let subtotal = 0;
		
		// Calculate subtotal from items
		if (frm.doc.invoice_items) {
			frm.doc.invoice_items.forEach(item => {
				if (item.quantity && item.rate) {
					item.amount = item.quantity * item.rate;
					subtotal += item.amount;
				}
			});
		}
		
		frm.set_value('subtotal', subtotal);
		
		// Calculate discount
		let discount = 0;
		if (frm.doc.discount_percentage) {
			discount = (subtotal * frm.doc.discount_percentage) / 100;
		} else if (frm.doc.discount_amount) {
			discount = frm.doc.discount_amount;
		}
		frm.set_value('discount_amount', discount);
		
		// Calculate tax
		let taxable_amount = subtotal - discount;
		let tax = 0;
		if (frm.doc.tax_percentage) {
			tax = (taxable_amount * frm.doc.tax_percentage) / 100;
		} else if (frm.doc.tax_amount) {
			tax = frm.doc.tax_amount;
		}
		frm.set_value('tax_amount', tax);
		
		// Calculate total
		let total = taxable_amount + tax;
		frm.set_value('total_amount', total);
		
		// Calculate outstanding
		let outstanding = total - (frm.doc.amount_paid || 0);
		frm.set_value('outstanding_amount', outstanding);
		
		// Update payment status
		frm.trigger('update_payment_status');
	},
	
	update_payment_status: function(frm) {
		if (!frm.doc.total_amount) {
			frm.set_value('payment_status', 'Draft');
		} else if (frm.doc.outstanding_amount <= 0) {
			frm.set_value('payment_status', 'Paid');
		} else if (frm.doc.amount_paid > 0) {
			frm.set_value('payment_status', 'Partially Paid');
		} else {
			frm.set_value('payment_status', 'Unpaid');
		}
	},
	
	discount_percentage: function(frm) {
		if (frm.doc.discount_percentage) {
			frm.set_value('discount_amount', 0);
		}
		frm.trigger('calculate_totals');
	},
	
	discount_amount: function(frm) {
		if (frm.doc.discount_amount) {
			frm.set_value('discount_percentage', 0);
		}
		frm.trigger('calculate_totals');
	},
	
	tax_percentage: function(frm) {
		frm.trigger('calculate_totals');
	},
	
	patient: function(frm) {
		if (frm.doc.patient) {
			frappe.db.get_value('Patient', frm.doc.patient, 'patient_name', function(r) {
				if (r && r.patient_name) {
					frm.set_value('patient_name', r.patient_name);
				}
			});
		}
	},
	
	dialysis_session: function(frm) {
		if (frm.doc.dialysis_session) {
			// Auto-add session as invoice item
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Dialysis Session',
					name: frm.doc.dialysis_session
				},
				callback: function(r) {
					if (r.message) {
						let row = frm.add_child('invoice_items');
						frappe.model.set_value(row.doctype, row.name, 'item_type', 'Dialysis Session');
						frappe.model.set_value(row.doctype, row.name, 'item_description', 
							`Dialysis Session - ${frappe.datetime.str_to_user(r.message.session_date)}`);
						frappe.model.set_value(row.doctype, row.name, 'quantity', 1);
						frappe.model.set_value(row.doctype, row.name, 'rate', 500); // Default rate
						frappe.model.set_value(row.doctype, row.name, 'reference_doctype', 'Dialysis Session');
						frappe.model.set_value(row.doctype, row.name, 'reference_name', frm.doc.dialysis_session);
						frm.refresh_field('invoice_items');
					}
				}
			});
		}
	}
});

// Invoice Item child table events
frappe.ui.form.on('Invoice Item', {
	quantity: function(frm, cdt, cdn) {
		calculate_item_amount(frm, cdt, cdn);
	},
	
	rate: function(frm, cdt, cdn) {
		calculate_item_amount(frm, cdt, cdn);
	},
	
	invoice_items_remove: function(frm) {
		frm.trigger('calculate_totals');
	}
});

function calculate_item_amount(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.quantity && row.rate) {
		frappe.model.set_value(cdt, cdn, 'amount', row.quantity * row.rate);
	}
	frm.trigger('calculate_totals');
}
