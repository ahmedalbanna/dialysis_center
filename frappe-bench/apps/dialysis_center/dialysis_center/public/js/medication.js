// Medication Form Enhancement
// Features: Inventory tracking, expiration alerts, stock management

frappe.ui.form.on('Medication', {
	onload: function(frm) {
		frm.set_intro(__('Manage medication inventory and stock'));
		update_medication_indicator(frm);
	},
	
	refresh: function(frm) {
		update_medication_indicator(frm);
		
		if (!frm.is_new()) {
			// Show stock status
			show_stock_status(frm);
			
			// Add stock actions
			if (frm.doc.current_stock <= frm.doc.minimum_stock_level) {
				frm.add_custom_button(__('Add Stock'), function() {
					show_stock_dialog(frm);
				}, __('Stock'));
			}
			
			frm.add_custom_button(__('View Stock History'), function() {
				show_stock_history(frm);
			}, __('View'));
			
			// Check expiration
			if (frm.doc.expiration_date) {
				check_expiration(frm);
			}
		}
	},
	
	validate: function(frm) {
		if (!frm.doc.medication_name) {
			frappe.throw(__('Medication name is required'));
		}
		
		if (!frm.doc.medication_code) {
			frappe.throw(__('Medication code is required'));
		}
		
		if (!frm.doc.unit_of_measurement) {
			frappe.throw(__('Unit of measurement is required'));
		}
		
		if (!frm.doc.manufacturer) {
			frappe.throw(__('Manufacturer is required'));
		}
		
		// Validate stock levels
		if (frm.doc.current_stock < 0) {
			frappe.throw(__('Current stock cannot be negative'));
		}
		
		if (frm.doc.minimum_stock_level < 0) {
			frappe.throw(__('Minimum stock level cannot be negative'));
		}
		
		// Validate expiration date
		if (frm.doc.expiration_date) {
			const expiry = new Date(frm.doc.expiration_date);
			const today = new Date();
			
			if (expiry < today) {
				frappe.throw(__('Medication has expired'));
			}
		}
	},
	
	before_save: function(frm) {
		// Calculate days until expiration
		if (frm.doc.expiration_date) {
			const today = new Date();
			const expiry = new Date(frm.doc.expiration_date);
			const days_until_expiry = Math.floor((expiry - today) / (1000 * 60 * 60 * 24));
			frm.set_value('days_until_expiration', Math.max(0, days_until_expiry));
		}
		
		// Calculate stock status
		if (frm.doc.current_stock <= frm.doc.minimum_stock_level) {
			frm.set_value('stock_status', 'Low Stock');
		} else if (frm.doc.current_stock <= frm.doc.maximum_stock_level) {
			frm.set_value('stock_status', 'Good');
		} else {
			frm.set_value('stock_status', 'Overstocked');
		}
	},
	
	after_save: function(frm) {
		frappe.msgprint(__('Medication saved successfully'));
	},
	
	// Field-level events
	expiration_date: function(frm) {
		check_expiration(frm);
	},
	
	current_stock: function(frm) {
		// Warn if low stock
		if (frm.doc.current_stock && frm.doc.minimum_stock_level) {
			if (frm.doc.current_stock <= frm.doc.minimum_stock_level) {
				frappe.msgprint({
					title: __('Low Stock Alert'),
					message: __('Stock level is below minimum ({0} units)', [frm.doc.minimum_stock_level]),
					indicator: 'orange'
				});
			}
		}
	}
});

// Medication List View
frappe.listview_settings['Medication'] = {
	add_fields: ['medication_name', 'medication_code', 'current_stock', 'stock_status', 'expiration_date', 'days_until_expiration'],
	
	formatters: {
		stock_status: function(value) {
			const colors = {
				'Good': 'green',
				'Low Stock': 'orange',
				'Out of Stock': 'red',
				'Overstocked': 'blue'
			};
			
			return `<span style="background-color: ${colors[value] || 'white'}; color: white; padding: 4px 8px; border-radius: 3px; font-weight: bold;">${value}</span>`;
		},
		
		current_stock: function(value) {
			return `<strong>${value || 0}</strong>`;
		},
		
		days_until_expiration: function(value) {
			if (!value) return '-';
			
			let color = '#52c41a';  // Green
			if (value <= 30) {
				color = '#f5222d';  // Red
			} else if (value <= 90) {
				color = '#faad14';  // Orange
			}
			
			return `<span style="color: ${color}; font-weight: bold;">${value} days</span>`;
		},
		
		expiration_date: function(value) {
			if (!value) return '-';
			return frappe.datetime.str_to_user(value);
		}
	},
	
	filters: [
		['status', '!=', 'Discontinued']
	],
	
	onload: function(listview) {
		// Add stock filters
		listview.page.add_action_item(__('Low Stock'), function() {
			listview.filter_area.add([
				['Medication', 'stock_status', '=', 'Low Stock']
			]);
			listview.refresh();
		});
		
		listview.page.add_action_item(__('Expiring Soon'), function() {
			const thirty_days_from_now = frappe.datetime.add_days(frappe.datetime.now_date(), 30);
			listview.filter_area.add([
				['Medication', 'expiration_date', '<=', thirty_days_from_now],
				['Medication', 'expiration_date', '>=', frappe.datetime.now_date()]
			]);
			listview.refresh();
		});
		
		// Bulk stock adjustment
		listview.page.add_menu_item(__('Adjust Stock'), function() {
			const selected = listview.get_checked_items();
			if (selected.length === 0) {
				frappe.msgprint(__('Please select medications'));
				return;
			}
			
			show_bulk_adjustment_dialog(selected.map(d => d.name));
		});
	}
};

// Helper functions

function update_medication_indicator(frm) {
	let indicator = 'gray';
	let indicator_text = 'Unknown';
	
	if (frm.doc.stock_status === 'Good') {
		indicator = 'green';
		indicator_text = 'In Stock';
	} else if (frm.doc.stock_status === 'Low Stock') {
		indicator = 'orange';
		indicator_text = 'Low Stock';
	} else if (frm.doc.stock_status === 'Out of Stock') {
		indicator = 'red';
		indicator_text = 'Out of Stock';
	}
	
	frm.page.set_indicator(__(indicator_text), indicator);
	
	// Add expiration alert
	if (frm.doc.days_until_expiration !== null && frm.doc.days_until_expiration < 30) {
		frm.page.set_indicator(__('Expiring Soon'), 'red');
	}
}

function check_expiration(frm) {
	if (!frm.doc.expiration_date) return;
	
	const today = new Date();
	const expiry = new Date(frm.doc.expiration_date);
	const days_until = Math.floor((expiry - today) / (1000 * 60 * 60 * 24));
	
	if (days_until < 0) {
		frappe.msgprint({
			title: __('Expired Medication'),
			message: __('This medication has expired and should not be used'),
			indicator: 'red'
		});
	} else if (days_until <= 30) {
		frappe.msgprint({
			title: __('Expiration Alert'),
			message: __('This medication will expire in {0} days', [days_until]),
			indicator: 'orange'
		});
	}
}

function show_stock_status(frm) {
	const status_html = `
		<div class="stock-status" style="margin: 15px 0; padding: 15px; background: #f5f5f5; border-radius: 5px;">
			<div class="row">
				<div class="col-sm-3">
					<small>Current Stock</small><br/>
					<strong style="font-size: 18px;">${frm.doc.current_stock || 0}</strong>
					<small>${frm.doc.unit_of_measurement}</small>
				</div>
				<div class="col-sm-3">
					<small>Minimum Level</small><br/>
					<strong>${frm.doc.minimum_stock_level || 0}</strong>
					<small>${frm.doc.unit_of_measurement}</small>
				</div>
				<div class="col-sm-3">
					<small>Status</small><br/>
					<strong style="color: ${
						frm.doc.stock_status === 'Good' ? '#52c41a' :
						frm.doc.stock_status === 'Low Stock' ? '#faad14' : '#f5222d'
					}">${frm.doc.stock_status}</strong>
				</div>
				<div class="col-sm-3">
					<small>Expires In</small><br/>
					<strong style="color: ${frm.doc.days_until_expiration <= 30 ? '#f5222d' : '#52c41a'}">${frm.doc.days_until_expiration || 0} days</strong>
				</div>
			</div>
		</div>
	`;
	
	$(frm.wrapper).find('.stock-status').remove();
	$(frm.fields_dict.medication_name.wrapper).after(status_html);
}

function show_stock_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Add Stock'),
		fields: [
			{
				fieldtype: 'Int',
				fieldname: 'quantity',
				label: __('Quantity to Add'),
				default: frm.doc.minimum_stock_level - (frm.doc.current_stock || 0),
				reqd: 1
			},
			{
				fieldtype: 'Date',
				fieldname: 'received_date',
				label: __('Date Received'),
				default: frappe.datetime.now_date(),
				reqd: 1
			},
			{
				fieldtype: 'Date',
				fieldname: 'expiration_date',
				label: __('Expiration Date'),
				reqd: 1
			},
			{
				fieldtype: 'Data',
				fieldname: 'batch_number',
				label: __('Batch Number')
			},
			{
				fieldtype: 'Data',
				fieldname: 'supplier',
				label: __('Supplier')
			},
			{
				fieldtype: 'Currency',
				fieldname: 'unit_cost',
				label: __('Unit Cost')
			}
		],
		primary_action_label: __('Add Stock'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.medication.add_stock',
				args: {
					medication: frm.doc.name,
					stock_movement: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Stock added successfully'));
						const new_stock = (frm.doc.current_stock || 0) + values.quantity;
						frm.set_value('current_stock', new_stock);
						frm.set_value('expiration_date', values.expiration_date);
						frm.save();
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function show_stock_history(frm) {
	frappe.call({
		method: 'dialysis_center.api.medication.get_stock_history',
		args: {
			medication: frm.doc.name,
			limit: 20
		},
		callback: function(r) {
			if (r.message && r.message.history) {
				const history = r.message.history;
				
				const dialog = new frappe.ui.Dialog({
					title: __('Stock History'),
					size: 'large',
					fields: [
						{
							fieldtype: 'HTML',
							fieldname: 'history_html',
							html: `
								<table class="table table-sm">
									<thead>
										<tr>
											<th>Date</th>
											<th>Type</th>
											<th>Quantity</th>
											<th>Reference</th>
											<th>Remarks</th>
										</tr>
									</thead>
									<tbody>
										${history.map(h => `
											<tr>
												<td>${frappe.datetime.str_to_user(h.movement_date)}</td>
												<td>
													<span style="color: ${h.movement_type === 'Stock In' ? '#52c41a' : '#f5222d'};">
														${h.movement_type}
													</span>
												</td>
												<td><strong>${h.quantity}</strong></td>
												<td>${h.reference_doc || '-'}</td>
												<td>${h.remarks || '-'}</td>
											</tr>
										`).join('')}
									</tbody>
								</table>
							`
						}
					]
				});
				
				dialog.show();
			}
		}
	});
}

function show_bulk_adjustment_dialog(medications) {
	const dialog = new frappe.ui.Dialog({
		title: __('Bulk Stock Adjustment'),
		fields: [
			{
				fieldtype: 'Select',
				fieldname: 'adjustment_type',
				label: __('Adjustment Type'),
				options: '\nAdd\nRemove\nAdjust',
				reqd: 1
			},
			{
				fieldtype: 'Int',
				fieldname: 'quantity',
				label: __('Quantity'),
				reqd: 1
			},
			{
				fieldtype: 'Text',
				fieldname: 'reason',
				label: __('Reason'),
				reqd: 1
			}
		],
		primary_action_label: __('Apply Adjustment'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.medication.bulk_stock_adjustment',
				args: {
					medications: medications,
					adjustment: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Stock adjusted for {0} items', [medications.length]));
						dialog.hide();
						cur_list.refresh();
					}
				}
			});
		}
	});
	
	dialog.show();
}
