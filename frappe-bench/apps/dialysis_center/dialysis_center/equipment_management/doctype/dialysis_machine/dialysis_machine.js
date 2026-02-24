frappe.ui.form.on('Dialysis Machine', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add custom buttons
			frm.add_custom_button(__('Schedule Maintenance'), function() {
				frappe.prompt([
					{
						fieldname: 'maintenance_date',
						fieldtype: 'Date',
						label: 'Maintenance Date',
						default: frappe.datetime.get_today(),
						reqd: 1
					}
				], function(values) {
					frappe.call({
						method: 'mark_maintenance',
						doc: frm.doc,
						args: {
							maintenance_date: values.maintenance_date
						},
						callback: function() {
							frm.reload_doc();
							frappe.show_alert({
								message: __('Machine marked for maintenance'),
								indicator: 'orange'
							});
						}
					});
				}, __('Schedule Maintenance'));
			});
			
			if (frm.doc.status === 'Maintenance') {
				frm.add_custom_button(__('Mark Available'), function() {
					frappe.call({
						method: 'mark_available',
						doc: frm.doc,
						callback: function() {
							frm.reload_doc();
							frappe.show_alert({
								message: __('Machine marked as available'),
								indicator: 'green'
							});
						}
					});
				});
			}
			
			// Add indicator for maintenance due
			if (frm.doc.next_maintenance_date) {
				let days_until = frappe.datetime.get_day_diff(frm.doc.next_maintenance_date, frappe.datetime.get_today());
				if (days_until < 0) {
					frm.dashboard.add_indicator(__('Maintenance Overdue'), 'red');
				} else if (days_until <= 7) {
					frm.dashboard.add_indicator(__('Maintenance Due Soon'), 'orange');
				}
			}
		}
	},
	
	last_maintenance_date: function(frm) {
		if (frm.doc.last_maintenance_date && frm.doc.maintenance_frequency_days) {
			let next_date = frappe.datetime.add_days(
				frm.doc.last_maintenance_date, 
				frm.doc.maintenance_frequency_days
			);
			frm.set_value('next_maintenance_date', next_date);
		}
	},
	
	maintenance_frequency_days: function(frm) {
		if (frm.doc.last_maintenance_date && frm.doc.maintenance_frequency_days) {
			let next_date = frappe.datetime.add_days(
				frm.doc.last_maintenance_date, 
				frm.doc.maintenance_frequency_days
			);
			frm.set_value('next_maintenance_date', next_date);
		}
	}
});
