frappe.ui.form.on('Appointment', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add action buttons based on status
			if (frm.doc.status === 'Scheduled') {
				frm.add_custom_button(__('Check In'), function() {
					frm.trigger('check_in_patient');
				}).addClass('btn-primary');
				
				frm.add_custom_button(__('Cancel Appointment'), function() {
					frm.trigger('cancel_appointment');
				});
			}
			
			if (frm.doc.status === 'Checked In') {
				frm.add_custom_button(__('Create Session'), function() {
					frm.trigger('create_dialysis_session');
				}).addClass('btn-success');
			}
			
			// Show appointment timeline
			frm.trigger('show_appointment_info');
		}
		
		// Set indicator
		frm.trigger('set_status_indicator');
		
		// Check slot availability when form loads
		if (frm.is_new()) {
			frm.trigger('check_slot_availability');
		}
	},
	
	check_in_patient: function(frm) {
		frappe.confirm(
			__('Check in patient {0} for this appointment?', [frm.doc.patient_name]),
			function() {
				frappe.call({
					method: 'dialysis_center.appointment_scheduling.doctype.appointment.appointment.check_in_appointment',
					args: {
						appointment: frm.doc.name
					},
					callback: function(r) {
						frm.reload_doc();
						frappe.show_alert({
							message: __('Patient checked in successfully'),
							indicator: 'green'
						});
					}
				});
			}
		);
	},
	
	cancel_appointment: function(frm) {
		frappe.prompt({
			label: __('Cancellation Reason'),
			fieldname: 'reason',
			fieldtype: 'Small Text',
			reqd: 1
		}, function(values) {
			frappe.call({
				method: 'frappe.client.set_value',
				args: {
					doctype: 'Appointment',
					name: frm.doc.name,
					fieldname: {
						status: 'Cancelled',
						notes: (frm.doc.notes || '') + '\nCancellation Reason: ' + values.reason
					}
				},
				callback: function(r) {
					frm.reload_doc();
					frappe.show_alert({
						message: __('Appointment cancelled'),
						indicator: 'red'
					});
				}
			});
		}, __('Cancel Appointment'));
	},
	
	create_dialysis_session: function(frm) {
		frappe.new_doc('Dialysis Session', {
			patient: frm.doc.patient,
			patient_name: frm.doc.patient_name,
			appointment: frm.doc.name,
			session_date: frm.doc.appointment_date,
			session_time: frm.doc.appointment_time,
			dialysis_machine: frm.doc.machine,
			treatment_duration: frm.doc.duration
		});
	},
	
	show_appointment_info: function(frm) {
		if (!frm.doc.appointment_date) return;
		
		let info_html = `
			<div class="appointment-info" style="padding: 10px; background: #f8f9fa; border-radius: 5px; margin: 10px 0;">
				<div class="row">
					<div class="col-sm-6">
						<strong>${__('Date')}:</strong> ${frappe.datetime.str_to_user(frm.doc.appointment_date)}<br>
						<strong>${__('Time')}:</strong> ${frm.doc.appointment_time || 'Not set'}
					</div>
					<div class="col-sm-6">
						<strong>${__('Duration')}:</strong> ${frm.doc.duration || 0} minutes<br>
						<strong>${__('Machine')}:</strong> ${frm.doc.machine || 'Not assigned'}
					</div>
				</div>
			</div>
		`;
		
		frm.dashboard.add_comment(info_html, true);
	},
	
	set_status_indicator: function(frm) {
		const status_colors = {
			'Scheduled': 'blue',
			'Checked In': 'orange',
			'In Progress': 'purple',
			'Completed': 'green',
			'Cancelled': 'red'
		};
		
		if (frm.doc.status) {
			frm.page.set_indicator(frm.doc.status, status_colors[frm.doc.status] || 'gray');
		}
	},
	
	check_slot_availability: function(frm) {
		if (frm.doc.appointment_date && frm.doc.machine && frm.doc.appointment_time) {
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Appointment',
					filters: {
						appointment_date: frm.doc.appointment_date,
						machine: frm.doc.machine,
						appointment_time: frm.doc.appointment_time,
						status: ['not in', ['Cancelled', 'Completed']]
					}
				},
				callback: function(r) {
					if (r.message > 0) {
						frappe.msgprint({
							title: __('Slot Conflict'),
							message: __('This time slot may already be booked for this machine'),
							indicator: 'orange'
						});
					}
				}
			});
		}
	},
	
	patient: function(frm) {
		if (frm.doc.patient) {
			// Fetch patient's default duration
			frappe.db.get_value('Patient', frm.doc.patient, ['duration', 'patient_name'], function(r) {
				if (r && r.duration) {
					frm.set_value('duration', r.duration);
				}
				if (r && r.patient_name) {
					frm.set_value('patient_name', r.patient_name);
				}
			});
		}
	},
	
	appointment_date: function(frm) {
		frm.trigger('check_slot_availability');
	},
	
	machine: function(frm) {
		frm.trigger('check_slot_availability');
		
		// Check machine status
		if (frm.doc.machine) {
			frappe.db.get_value('Dialysis Machine', frm.doc.machine, 'status', function(r) {
				if (r && r.status !== 'Available') {
					frappe.msgprint({
						title: __('Machine Status'),
						message: __('Warning: Machine status is {0}', [r.status]),
						indicator: 'orange'
					});
				}
			});
		}
	},
	
	appointment_time: function(frm) {
		frm.trigger('check_slot_availability');
		
		// Calculate end time
		if (frm.doc.appointment_time && frm.doc.duration) {
			let time_parts = frm.doc.appointment_time.split(':');
			let minutes = parseInt(time_parts[0]) * 60 + parseInt(time_parts[1]) + frm.doc.duration;
			let end_hours = Math.floor(minutes / 60);
			let end_minutes = minutes % 60;
			frm.set_value('appointment_end_time', 
				`${String(end_hours).padStart(2, '0')}:${String(end_minutes).padStart(2, '0')}:00`);
		}
	},
	
	duration: function(frm) {
		frm.trigger('appointment_time');
	}
});
