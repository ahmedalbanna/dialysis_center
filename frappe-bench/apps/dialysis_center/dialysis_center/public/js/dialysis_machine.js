// Dialysis Machine Form Enhancement
// Features: Machine maintenance tracking, availability status, performance monitoring

frappe.ui.form.on('Dialysis Machine', {
	onload: function(frm) {
		frm.set_intro(__('Monitor and maintain dialysis equipment'));
		update_machine_indicator(frm);
	},
	
	refresh: function(frm) {
		update_machine_indicator(frm);
		
		if (!frm.is_new()) {
			// Show machine status dashboard
			show_machine_status(frm);
			
			// Add maintenance actions
			frm.add_custom_button(__('Schedule Maintenance'), function() {
				show_maintenance_dialog(frm);
			}, __('Maintenance'));
			
			frm.add_custom_button(__('Record Service'), function() {
				show_service_dialog(frm);
			}, __('Maintenance'));
			
			// Add status actions
			if (frm.doc.status === 'Operational') {
				frm.add_custom_button(__('Mark Out of Service'), function() {
					update_machine_status(frm, 'Out of Service');
				}, __('Actions'));
			} else {
				frm.add_custom_button(__('Mark Operational'), function() {
					update_machine_status(frm, 'Operational');
				}, __('Actions'));
			}
			
			// Show maintenance history
			show_maintenance_history(frm);
		}
	},
	
	validate: function(frm) {
		if (!frm.doc.machine_name) {
			frappe.throw(__('Machine name is required'));
		}
		
		if (!frm.doc.machine_type) {
			frappe.throw(__('Machine type is required'));
		}
		
		if (!frm.doc.status) {
			frappe.throw(__('Machine status is required'));
		}
	},
	
	before_save: function(frm) {
		// Calculate age of machine
		if (frm.doc.purchase_date) {
			const today = new Date();
			const purchase = new Date(frm.doc.purchase_date);
			const age_days = Math.floor((today - purchase) / (1000 * 60 * 60 * 24));
			const age_years = Math.floor(age_days / 365);
			frm.set_value('age_in_years', age_years);
		}
		
		// Calculate days since last maintenance
		if (frm.doc.last_maintenance_date) {
			const today = new Date();
			const last_maint = new Date(frm.doc.last_maintenance_date);
			const days_since = Math.floor((today - last_maint) / (1000 * 60 * 60 * 24));
			
			if (days_since > 90) {
				frappe.msgprint({
					title: __('Maintenance Alert'),
					message: __('Machine is overdue for maintenance ({0} days since last service)', [days_since]),
					indicator: 'orange'
				});
			}
		}
	},
	
	after_save: function(frm) {
		frappe.msgprint(__('Machine information saved successfully'));
	},
	
	status: function(frm) {
		update_machine_indicator(frm);
		frm.refresh();
	}
});

// Dialysis Machine List View
frappe.listview_settings['Dialysis Machine'] = {
	add_fields: ['machine_name', 'machine_type', 'status', 'last_maintenance_date', 'age_in_years'],
	
	formatters: {
		status: function(value) {
			const colors = {
				'Operational': 'green',
				'Out of Service': 'red',
				'Maintenance': 'orange',
				'Retired': 'gray'
			};
			
			return `<span style="background-color: ${colors[value] || 'white'}; color: white; padding: 4px 8px; border-radius: 3px; font-weight: bold;">${value}</span>`;
		},
		
		machine_type: function(value) {
			return `<span style="color: #666;">${value}</span>`;
		},
		
		last_maintenance_date: function(value) {
			if (!value) return '-';
			return frappe.datetime.str_to_user(value);
		},
		
		age_in_years: function(value) {
			return `${value || 0} years`;
		}
	},
	
	filters: [
		['status', '!=', 'Retired']
	],
	
	onload: function(listview) {
		// Add status filters
		listview.page.add_action_item(__('Operational'), function() {
			listview.filter_area.add([
				['Dialysis Machine', 'status', '=', 'Operational']
			]);
			listview.refresh();
		});
		
		listview.page.add_action_item(__('Needs Maintenance'), function() {
			listview.filter_area.add([
				['Dialysis Machine', 'last_maintenance_date', '<', frappe.datetime.add_days(frappe.datetime.now_date(), -90)]
			]);
			listview.refresh();
		});
	}
};

// Helper functions

function update_machine_indicator(frm) {
	const status_colors = {
		'Operational': 'green',
		'Out of Service': 'red',
		'Maintenance': 'orange',
		'Retired': 'gray'
	};
	
	const color = status_colors[frm.doc.status] || 'gray';
	frm.page.set_indicator(__(frm.doc.status || 'Unknown'), color);
	
	// Add maintenance alert if overdue
	if (frm.doc.last_maintenance_date) {
		const today = new Date();
		const last_maint = new Date(frm.doc.last_maintenance_date);
		const days_since = Math.floor((today - last_maint) / (1000 * 60 * 60 * 24));
		
		if (days_since > 90) {
			frm.page.set_indicator(__('Maintenance Overdue'), 'orange');
		}
	}
}

function show_machine_status(frm) {
	const status_html = `
		<div class="machine-status" style="margin: 15px 0; padding: 15px; background: #f5f5f5; border-radius: 5px;">
			<div class="row">
				<div class="col-sm-3">
					<small>Status</small><br/>
					<strong style="color: ${frm.doc.status === 'Operational' ? '#52c41a' : '#f5222d'}">${frm.doc.status}</strong>
				</div>
				<div class="col-sm-3">
					<small>Age</small><br/>
					<strong>${frm.doc.age_in_years || 0} years</strong>
				</div>
				<div class="col-sm-3">
					<small>Last Maintenance</small><br/>
					<strong>${frm.doc.last_maintenance_date ? frappe.datetime.str_to_user(frm.doc.last_maintenance_date) : 'Never'}</strong>
				</div>
				<div class="col-sm-3">
					<small>Sessions Completed</small><br/>
					<strong>${frm.doc.total_sessions_completed || 0}</strong>
				</div>
			</div>
		</div>
	`;
	
	$(frm.wrapper).find('.machine-status').remove();
	$(frm.fields_dict.machine_name.wrapper).after(status_html);
}

function show_maintenance_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Schedule Maintenance'),
		fields: [
			{
				fieldtype: 'Date',
				fieldname: 'maintenance_date',
				label: __('Maintenance Date'),
				default: frappe.datetime.add_days(frappe.datetime.now_date(), 1),
				reqd: 1
			},
			{
				fieldtype: 'Select',
				fieldname: 'maintenance_type',
				label: __('Maintenance Type'),
				options: '\nRoutine\nPrevention\nRepair\nCalibration',
				reqd: 1
			},
			{
				fieldtype: 'Text',
				fieldname: 'reason',
				label: __('Reason for Maintenance'),
				reqd: 1
			}
		],
		primary_action_label: __('Schedule'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.dialysis_machine.schedule_maintenance',
				args: {
					machine: frm.doc.name,
					maintenance: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Maintenance scheduled successfully'));
						frm.reload_doc();
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function show_service_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Record Service'),
		fields: [
			{
				fieldtype: 'Datetime',
				fieldname: 'service_date',
				label: __('Service Date'),
				default: frappe.datetime.now_datetime(),
				reqd: 1
			},
			{
				fieldtype: 'Select',
				fieldname: 'service_type',
				label: __('Service Type'),
				options: '\nMaintenance\nRepair\nParts Replacement\nCalibration',
				reqd: 1
			},
			{
				fieldtype: 'Text',
				fieldname: 'description',
				label: __('Service Description'),
				reqd: 1
			},
			{
				fieldtype: 'Data',
				fieldname: 'performed_by',
				label: __('Performed By'),
				reqd: 1
			}
		],
		primary_action_label: __('Record Service'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.dialysis_machine.record_service',
				args: {
					machine: frm.doc.name,
					service: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Service recorded successfully'));
						frm.set_value('last_maintenance_date', values.service_date);
						frm.save();
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function show_maintenance_history(frm) {
	frappe.call({
		method: 'dialysis_center.api.dialysis_machine.get_maintenance_history',
		args: {
			machine: frm.doc.name,
			limit: 10
		},
		callback: function(r) {
			if (r.message && r.message.history && r.message.history.length > 0) {
				const history = r.message.history;
				
				const history_html = `
					<div class="maintenance-history" style="margin: 15px 0; padding: 15px; background: #f9f9f9; border-radius: 5px;">
						<h6>Maintenance History</h6>
						<table class="table table-sm" style="margin: 0;">
							<thead>
								<tr>
									<th>Date</th>
									<th>Type</th>
									<th>Description</th>
								</tr>
							</thead>
							<tbody>
								${history.map(h => `
									<tr>
										<td>${frappe.datetime.str_to_user(h.service_date)}</td>
										<td>${h.service_type}</td>
										<td>${h.description}</td>
									</tr>
								`).join('')}
							</tbody>
						</table>
					</div>
				`;
				
				$(frm.wrapper).find('.maintenance-history').remove();
				$(frm.wrapper).find('.machine-status').after(history_html);
			}
		}
	});
}

function update_machine_status(frm, new_status) {
	frappe.call({
		method: 'dialysis_center.api.dialysis_machine.update_status',
		args: {
			machine: frm.doc.name,
			new_status: new_status
		},
		callback: function(r) {
			if (r.message && r.message.success) {
				frm.set_value('status', new_status);
				frm.save();
				frappe.msgprint(__('Machine status updated'));
			}
		}
	});
}
