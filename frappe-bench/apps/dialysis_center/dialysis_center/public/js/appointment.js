// Appointment Form Enhancement
// Features: Calendar view integration, availability checker, check-in functionality

frappe.ui.form.on('Appointment', {
	onload: function(frm) {
		// Initialize form state
		frm.set_intro(__('Schedule and manage dialysis appointments'));
		
		// Set appointment status indicator
		update_appointment_indicator(frm);
		
		// Load appointment constraints
		load_appointment_constraints(frm);
	},
	
	refresh: function(frm) {
		// Update status indicator
		update_appointment_indicator(frm);
		
		// Control field visibility based on appointment status
		if (frm.doc.docstatus === 0) {
			frm.set_df_property('appointment_time', 'read_only', 0);
			frm.set_df_property('notes', 'read_only', 0);
			
			// Add check-in button for upcoming appointments
			if (frm.doc.status === 'Confirmed' && !frm.is_new()) {
				frm.add_custom_button(__('Check In'), function() {
					check_in_appointment(frm);
				}, __('Actions'));
			}
			
			// Add reschedule button for scheduled appointments
			if (['Confirmed', 'Rescheduled'].includes(frm.doc.status) && !frm.is_new()) {
				frm.add_custom_button(__('Reschedule'), function() {
					show_reschedule_dialog(frm);
				}, __('Actions'));
			}
			
			// Add cancel button
			if (!['Completed', 'Cancelled'].includes(frm.doc.status) && !frm.is_new()) {
				frm.add_custom_button(__('Cancel Appointment'), function() {
					cancel_appointment(frm);
				}, __('Actions'));
			}
		}
		
		// Show appointment details summary
		if (!frm.is_new()) {
			show_appointment_details(frm);
		}
		
		// Disable past appointment dates
		frm.set_df_property('appointment_date', 'description', 
			__('Select a date on or after today'));
	},
	
	validate: function(frm) {
		// Validate appointment date
		if (frm.doc.appointment_date) {
			const appointment_date = new Date(frm.doc.appointment_date);
			const today = new Date();
			today.setHours(0, 0, 0, 0);
			
			if (appointment_date < today) {
				frappe.throw(__('Appointment date cannot be in the past'));
			}
		}
		
		// Validate required fields
		if (!frm.doc.patient) {
			frappe.throw(__('Patient is required'));
		}
		
		if (!frm.doc.appointment_date) {
			frappe.throw(__('Appointment date is required'));
		}
		
		if (!frm.doc.appointment_time) {
			frappe.throw(__('Appointment time is required'));
		}
		
		// Check for appointment conflicts
		check_appointment_conflicts(frm);
	},
	
	before_save: function(frm) {
		// Set appointment status if new
		if (frm.is_new()) {
			frm.set_value('status', 'Scheduled');
		}
		
		// Calculate appointment datetime
		if (frm.doc.appointment_date && frm.doc.appointment_time) {
			const datetime_str = `${frm.doc.appointment_date} ${frm.doc.appointment_time}`;
			frm.set_value('appointment_datetime', datetime_str);
		}
	},
	
	after_save: function(frm) {
		frappe.msgprint(__('Appointment saved successfully'));
		
		// Clear any cached data
		frappe.cache.delete_value(`appointment_${frm.doc.name}`);
		frappe.cache.delete_value(`patient_appointments_${frm.doc.patient}`);
	},
	
	// Field-level events
	patient: function(frm) {
		// Fetch patient details when patient changes
		if (frm.doc.patient) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Patient',
					filters: { name: frm.doc.patient },
					fieldname: ['patient_name', 'phone', 'email', 'status']
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('patient_name', r.message.patient_name);
						frm.set_value('patient_phone', r.message.phone);
						frm.set_value('patient_email', r.message.email);
						
						// Show warning if patient inactive
						if (r.message.status !== 'Active') {
							frappe.msgprint({
								title: __('Patient Status'),
								message: __('Patient status is {0}', [r.message.status]),
								indicator: 'orange'
							});
						}
					}
				}
			});
			
			// Check availability
			check_appointment_availability(frm);
		}
	},
	
	appointment_date: function(frm) {
		// Check availability when date changes
		check_appointment_availability(frm);
	},
	
	appointment_time: function(frm) {
		// Check availability when time changes
		check_appointment_availability(frm);
	},
	
	status: function(frm) {
		// Update indicator when status changes
		update_appointment_indicator(frm);
		frm.refresh();
	}
});

// Helper functions

function update_appointment_indicator(frm) {
	const status_color = {
		'Scheduled': 'blue',
		'Confirmed': 'green',
		'Rescheduled': 'orange',
		'Checked In': 'purple',
		'Completed': 'green',
		'Cancelled': 'red',
		'No Show': 'red'
	};
	
	const color = status_color[frm.doc.status] || 'gray';
	frm.page.set_indicator(__(frm.doc.status), color);
}

function check_appointment_availability(frm) {
	if (!frm.doc.patient || !frm.doc.appointment_date) return;
	
	frappe.call({
		method: 'dialysis_center.api.appointment.check_availability',
		args: {
			patient: frm.doc.patient,
			appointment_date: frm.doc.appointment_date,
			appointment_time: frm.doc.appointment_time,
			exclude_appointment: frm.doc.name
		},
		callback: function(r) {
			if (r.message) {
				if (r.message.available_slots) {
					frm.set_df_property('appointment_time', 'description',
						__('Available slots: {0}', [r.message.available_slots.join(', ')]));
				}
				
				if (r.message.conflicts && r.message.conflicts.length > 0) {
					frappe.msgprint({
						title: __('Scheduling Conflict'),
						message: __('Patient has existing appointment(s) at this time'),
						indicator: 'orange'
					});
				}
			}
		}
	});
}

function check_appointment_conflicts(frm) {
	if (!frm.doc.patient || !frm.doc.appointment_date || !frm.doc.appointment_time) {
		return;
	}
	
	frappe.call({
		method: 'dialysis_center.api.appointment.check_conflicts',
		args: {
			patient: frm.doc.patient,
			appointment_date: frm.doc.appointment_date,
			appointment_time: frm.doc.appointment_time,
			exclude_appointment: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.conflicts && r.message.conflicts.length > 0) {
				frappe.throw(__('Cannot schedule: Existing appointment at this time. Conflicting appointments: {0}',
					[r.message.conflicts.join(', ')]));
			}
		}
	});
}

function check_in_appointment(frm) {
	frappe.call({
		method: 'dialysis_center.api.appointment.check_in',
		args: {
			appointment: frm.doc.name,
			check_in_time: frappe.datetime.now_datetime()
		},
		callback: function(r) {
			if (r.message && r.message.success) {
				frappe.msgprint(__('Check-in recorded successfully'));
				frm.set_value('status', 'Checked In');
				frm.set_value('check_in_time', r.message.check_in_time);
				frm.save();
			}
		}
	});
}

function show_reschedule_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Reschedule Appointment'),
		fields: [
			{
				fieldtype: 'Date',
				fieldname: 'new_date',
				label: __('New Date'),
				reqd: 1
			},
			{
				fieldtype: 'Time',
				fieldname: 'new_time',
				label: __('New Time'),
				reqd: 1
			},
			{
				fieldtype: 'Text',
				fieldname: 'reason',
				label: __('Reason for Rescheduling')
			}
		],
		primary_action_label: __('Reschedule'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.appointment.reschedule',
				args: {
					appointment: frm.doc.name,
					new_date: values.new_date,
					new_time: values.new_time,
					reason: values.reason
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Appointment rescheduled successfully'));
						frm.set_value('appointment_date', values.new_date);
						frm.set_value('appointment_time', values.new_time);
						frm.set_value('status', 'Rescheduled');
						frm.save();
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function cancel_appointment(frm) {
	frappe.confirm(
		__('Are you sure you want to cancel this appointment?'),
		function() {
			frappe.call({
				method: 'dialysis_center.api.appointment.cancel',
				args: {
					appointment: frm.doc.name
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Appointment cancelled successfully'));
						frm.set_value('status', 'Cancelled');
						frm.save();
					}
				}
			});
		}
	);
}

function load_appointment_constraints(frm) {
	// Load appointment constraints from settings
	frappe.call({
		method: 'dialysis_center.api.appointment.get_appointment_constraints',
		callback: function(r) {
			if (r.message) {
				const constraints = r.message;
				frm.set_df_property('appointment_date', 'description',
					__('Available: {0}', [constraints.working_days]));
			}
		}
	});
}

function show_appointment_details(frm) {
	// Fetch and display appointment summary
	frappe.call({
		method: 'dialysis_center.api.appointment.get_appointment_details',
		args: {
			appointment: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.details) {
				const details = r.message.details;
				const details_html = `
					<div class="appointment-details" style="margin: 15px 0; padding: 15px; background: #f5f5f5; border-radius: 5px;">
						<div style="margin-bottom: 10px;">
							<strong>Patient:</strong> ${details.patient_name}
						</div>
						<div style="margin-bottom: 10px;">
							<strong>Date & Time:</strong> ${details.appointment_datetime}
						</div>
						<div style="margin-bottom: 10px;">
							<strong>Status:</strong> <span class="badge badge-${details.status_lower}">${details.status}</span>
						</div>
						${details.check_in_time ? `
							<div style="margin-bottom: 10px;">
								<strong>Check-in:</strong> ${details.check_in_time}
							</div>
						` : ''}
					</div>
				`;
				
				$(frm.wrapper).find('.appointment-details').remove();
				$(frm.fields_dict.patient_name.wrapper).after(details_html);
			}
		}
	});
}
