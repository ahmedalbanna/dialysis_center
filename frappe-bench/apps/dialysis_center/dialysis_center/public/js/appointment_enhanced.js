/**
 * Enhanced Appointment Form with Real-time Updates
 */

frappe.ui.form.on('Appointment', {
	refresh: function(frm) {
		// Set status indicator
		set_status_indicator(frm);
		
		// Add custom buttons based on status
		if (frm.doc.status === 'Scheduled' && !frm.is_new()) {
			frm.add_custom_button(__('Check In'), function() {
				check_in_appointment(frm);
			}, __('Actions'));
			
			frm.add_custom_button(__('Reschedule'), function() {
				show_reschedule_dialog(frm);
			}, __('Actions'));
		}
		
		if (frm.doc.status === 'Checked In') {
			frm.add_custom_button(__('Start Session'), function() {
				start_dialysis_session(frm);
			}, __('Actions'));
		}
		
		// Show available slots when date/machine changes
		if (frm.doc.appointment_date && frm.doc.machine) {
			show_slot_availability(frm);
		}
	},
	
	appointment_date: function(frm) {
		if (frm.doc.appointment_date) {
			load_available_slots(frm);
		}
	},
	
	machine: function(frm) {
		if (frm.doc.appointment_date && frm.doc.machine) {
			check_machine_availability(frm);
		}
	},
	
	patient: function(frm) {
		if (frm.doc.patient) {
			load_patient_history(frm);
		}
	}
});

function set_status_indicator(frm) {
	if (!window.DialysisCenter) return;
	
	const statusColors = window.DialysisCenter.constants.STATUS_COLORS;
	const color = statusColors[frm.doc.status] || 'gray';
	frm.page.set_indicator(__(frm.doc.status), color);
}

async function load_available_slots(frm) {
	if (!window.DialysisCenter || !frm.doc.appointment_date) return;
	
	try {
		const slots = await window.DialysisCenter.api.AppointmentAPI.getAvailableSlots(
			frm.doc.appointment_date,
			frm.doc.machine
		);
		
		if (slots && slots.length > 0) {
			// Show available slots in a custom field
			const slotsHTML = `
				<div class="available-slots" style="margin: 10px 0; padding: 10px; background: #f0f9ff; border-radius: 5px;">
					<strong>Available Time Slots:</strong>
					<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px;">
						${slots.map(slot => `
							<button class="btn btn-xs btn-default" onclick="selectSlot('${slot.time}', '${frm.doc.name}')">
								${slot.time}
							</button>
						`).join('')}
					</div>
				</div>
			`;
			
			// Insert after appointment_time field
			const timeField = frm.fields_dict.appointment_time;
			if (timeField && timeField.wrapper) {
				$(timeField.wrapper).after(slotsHTML);
			}
		}
	} catch (error) {
		console.error('Failed to load slots:', error);
	}
}

window.selectSlot = function(time, appointmentName) {
	const frm = cur_frm;
	if (frm && frm.doc.name === appointmentName) {
		frm.set_value('appointment_time', time);
	}
};

async function check_machine_availability(frm) {
	if (!window.DialysisCenter) return;
	
	frappe.call({
		method: 'dialysis_center.api.appointment.check_machine_availability',
		args: {
			machine: frm.doc.machine,
			date: frm.doc.appointment_date,
			time: frm.doc.appointment_time
		},
		callback: function(r) {
			if (r.message && !r.message.available) {
				frappe.msgprint({
					title: __('Machine Unavailable'),
					message: __('This machine is not available at the selected time'),
					indicator: 'orange'
				});
			}
		}
	});
}

function check_in_appointment(frm) {
	frappe.confirm(
		__('Check in this appointment?'),
		function() {
			frappe.call({
				method: 'dialysis_center.api.appointment.check_in_appointment',
				args: { appointment: frm.doc.name },
				callback: function(r) {
					if (r.message) {
						frappe.show_alert({ message: __('Patient checked in'), indicator: 'green' }, 3);
						frm.reload_doc();
					}
				}
			});
		}
	);
}

function start_dialysis_session(frm) {
	frappe.new_doc('Dialysis Session', {
		patient: frm.doc.patient,
		patient_name: frm.doc.patient_name,
		appointment: frm.doc.name,
		machine: frm.doc.machine,
		session_date: frm.doc.appointment_date
	});
}

function show_reschedule_dialog(frm) {
	const d = new frappe.ui.Dialog({
		title: __('Reschedule Appointment'),
		fields: [
			{
				fieldtype: 'Date',
				fieldname: 'new_date',
				label: __('New Date'),
				reqd: 1,
				default: frm.doc.appointment_date
			},
			{
				fieldtype: 'Time',
				fieldname: 'new_time',
				label: __('New Time'),
				reqd: 1
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'reason',
				label: __('Reason for Rescheduling')
			}
		],
		primary_action_label: __('Reschedule'),
		primary_action: function(values) {
			frappe.call({
				method: 'dialysis_center.api.appointment.reschedule_appointment',
				args: {
					appointment: frm.doc.name,
					new_date: values.new_date,
					new_time: values.new_time,
					reason: values.reason
				},
				callback: function(r) {
					if (r.message) {
						frappe.show_alert({ message: __('Appointment rescheduled'), indicator: 'green' }, 3);
						frm.reload_doc();
						d.hide();
					}
				}
			});
		}
	});
	d.show();
}

async function load_patient_history(frm) {
	if (!window.DialysisCenter || !frm.doc.patient) return;
	
	try {
		const sessions = await window.DialysisCenter.api.PatientAPI.getDetails(frm.doc.patient);
		
		if (sessions && sessions.recent_sessions) {
			const historyHTML = `
				<div class="patient-history" style="margin: 10px 0; padding: 10px; background: #f9fafb; border-radius: 5px;">
					<strong>Recent Sessions:</strong>
					<ul style="margin: 8px 0; padding-left: 20px;">
						${sessions.recent_sessions.slice(0, 3).map(s => `
							<li>${window.DialysisCenter.formatters.formatDate(s.session_date)} - ${s.status}</li>
						`).join('')}
					</ul>
				</div>
			`;
			
			frm.set_df_property('patient', 'description', historyHTML);
		}
	} catch (error) {
		console.error('Failed to load patient history:', error);
	}
}
