frappe.ui.form.on('Dialysis Session', {
	refresh: function(frm) {
		// Add custom buttons
		if (frm.doc.docstatus === 0 && frm.doc.status !== 'Completed') {
			frm.add_custom_button(__('Complete Session'), function() {
				complete_session(frm);
			}).addClass('btn-primary');
		}
		
		if (frm.doc.docstatus === 1 && !frm.doc.invoice) {
			frm.add_custom_button(__('Create Invoice'), function() {
				create_invoice_from_session(frm);
			});
		}
		
		// Status indicator
		if (frm.doc.status === 'Completed') {
			frm.page.set_indicator(__('Completed'), 'green');
		} else if (frm.doc.status === 'In Progress') {
			frm.page.set_indicator(__('In Progress'), 'blue');
		} else if (frm.doc.status === 'Cancelled') {
			frm.page.set_indicator(__('Cancelled'), 'red');
		}
	},
	
	patient: function(frm) {
		// Auto-fill patient details and last session data
		if (frm.doc.patient) {
			frappe.call({
				method: 'dialysis_center.api.patient.get_patient_dashboard',
				args: {patient: frm.doc.patient},
				callback: function(r) {
					if (r.message && r.message.patient) {
						const patient = r.message.patient;
						
						// Set default values from patient
						if (patient.dry_weight && !frm.doc.pre_dialysis_weight) {
							frm.set_value('target_dry_weight', patient.dry_weight);
						}
						
						if (patient.duration && !frm.doc.treatment_duration) {
							frm.set_value('treatment_duration', patient.duration);
						}
						
						if (patient.dialysis_type) {
							frm.set_value('dialysis_type', patient.dialysis_type);
						}
						
						if (patient.access_type) {
							frm.set_value('access_type', patient.access_type);
						}
					}
				}
			});
		}
	},
	
	treatment_template: function(frm) {
		// Load treatment template parameters
		if (frm.doc.treatment_template) {
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Treatment Template',
					name: frm.doc.treatment_template
				},
				callback: function(r) {
					if (r.message) {
						const template = r.message;
						
						// Auto-fill treatment parameters
						frm.set_value('treatment_duration', template.duration);
						frm.set_value('blood_flow_rate', template.blood_flow_rate);
						frm.set_value('dialysate_flow_rate', template.dialysate_flow_rate);
						frm.set_value('uf_goal', template.uf_goal);
						frm.set_value('dialyzer_type', template.dialyzer_type);
						frm.set_value('anticoagulation', template.anticoagulation_protocol);
						frm.set_value('heparin_dose', template.heparin_loading_dose);
						
						frappe.show_alert({
							message: __('Treatment parameters loaded from template'),
							indicator: 'green'
						}, 3);
					}
				}
			});
		}
	},
	
	pre_dialysis_weight: function(frm) {
		calculate_weight_gain(frm);
	},
	
	post_dialysis_weight: function(frm) {
		calculate_weight_loss(frm);
	},
	
	dialysis_machine: function(frm) {
		// Check machine availability
		if (frm.doc.dialysis_machine && frm.doc.session_date) {
			check_machine_availability(frm);
		}
	},
	
	session_date: function(frm) {
		// Check machine availability when date changes
		if (frm.doc.dialysis_machine && frm.doc.session_date) {
			check_machine_availability(frm);
		}
	},
	
	before_submit: function(frm) {
		// Validate required post-dialysis data
		if (!frm.doc.post_dialysis_weight) {
			frappe.msgprint(__('Please enter post-dialysis weight'));
			frappe.validated = false;
		}
		
		if (!frm.doc.session_end_time) {
			frappe.msgprint(__('Please enter session end time'));
			frappe.validated = false;
		}
	}
});

function calculate_weight_gain(frm) {
	if (frm.doc.pre_dialysis_weight && frm.doc.target_dry_weight) {
		const weight_gain = frm.doc.pre_dialysis_weight - frm.doc.target_dry_weight;
		frm.set_value('weight_gain', weight_gain);
		
		// Calculate UF goal
		if (weight_gain > 0) {
			frm.set_value('uf_goal', weight_gain);
		}
	}
}

function calculate_weight_loss(frm) {
	if (frm.doc.pre_dialysis_weight && frm.doc.post_dialysis_weight) {
		const weight_loss = frm.doc.pre_dialysis_weight - frm.doc.post_dialysis_weight;
		frm.set_value('weight_loss', weight_loss);
		
		// Show alert if weight loss is unusual
		if (weight_loss < 0) {
			frappe.msgprint({
				title: __('Weight Gain During Session'),
				message: __('Patient gained weight during session. Please verify measurements.'),
				indicator: 'orange'
			});
		} else if (weight_loss > 5) {
			frappe.msgprint({
				title: __('Excessive Weight Loss'),
				message: __('Weight loss of {0} kg is unusually high. Please verify.', [weight_loss.toFixed(2)]),
				indicator: 'orange'
			});
		}
	}
}

function check_machine_availability(frm) {
	frappe.call({
		method: 'dialysis_center.api.appointment.check_machine_availability',
		args: {
			machine: frm.doc.dialysis_machine,
			date: frm.doc.session_date,
			exclude_session: frm.doc.name
		},
		callback: function(r) {
			if (r.message && !r.message.available) {
				frappe.msgprint({
					title: __('Machine Not Available'),
					message: __('This machine is already scheduled for another session on this date.'),
					indicator: 'orange'
				});
			}
		}
	});
}

function complete_session(frm) {
	frappe.confirm(
		__('Complete this dialysis session? This will mark it as completed and ready for submission.'),
		function() {
			// Set completion fields
			frm.set_value('status', 'Completed');
			frm.set_value('session_end_time', frappe.datetime.now_datetime());
			
			frappe.show_alert({
				message: __('Session marked as completed. Please review and submit.'),
				indicator: 'green'
			}, 5);
		}
	);
}

function create_invoice_from_session(frm) {
	frappe.call({
		method: 'dialysis_center.api.billing.create_invoice_from_session',
		args: {
			session: frm.doc.name
		},
		callback: function(r) {
			if (r.message) {
				frappe.set_route('Form', 'Invoice', r.message);
				frappe.show_alert({
					message: __('Invoice created successfully'),
					indicator: 'green'
				}, 3);
			}
		}
	});
}

// Vital Signs child table
frappe.ui.form.on('Vital Signs Reading', {
	bp_systolic: function(frm, cdt, cdn) {
		validate_vital_signs(frm, cdt, cdn);
	},
	
	bp_diastolic: function(frm, cdt, cdn) {
		validate_vital_signs(frm, cdt, cdn);
	},
	
	heart_rate: function(frm, cdt, cdn) {
		validate_vital_signs(frm, cdt, cdn);
	}
});

function validate_vital_signs(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	
	// Validate blood pressure ranges
	if (row.bp_systolic) {
		if (row.bp_systolic < 70 || row.bp_systolic > 200) {
			frappe.msgprint({
				title: __('Abnormal BP - Systolic'),
				message: __('Systolic BP of {0} is outside normal range. Please verify.', [row.bp_systolic]),
				indicator: 'red'
			});
		}
	}
	
	if (row.bp_diastolic) {
		if (row.bp_diastolic < 40 || row.bp_diastolic > 130) {
			frappe.msgprint({
				title: __('Abnormal BP - Diastolic'),
				message: __('Diastolic BP of {0} is outside normal range. Please verify.', [row.bp_diastolic]),
				indicator: 'red'
			});
		}
	}
	
	// Validate heart rate
	if (row.heart_rate) {
		if (row.heart_rate < 40 || row.heart_rate > 160) {
			frappe.msgprint({
				title: __('Abnormal Heart Rate'),
				message: __('Heart rate of {0} bpm is outside normal range. Please verify.', [row.heart_rate]),
				indicator: 'red'
			});
		}
	}
}
