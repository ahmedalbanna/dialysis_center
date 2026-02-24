frappe.ui.form.on('Dialysis Session', {
	refresh: function(frm) {
		// Add custom buttons based on status
		if (!frm.is_new()) {
			if (frm.doc.status === 'Scheduled') {
				frm.add_custom_button(__('Start Session'), function() {
					frm.trigger('start_session');
				}).addClass('btn-primary');
			}
			
			if (frm.doc.status === 'In Progress') {
				frm.add_custom_button(__('Record Vitals'), function() {
					frm.trigger('add_vital_signs');
				}, __('Actions'));
				
				frm.add_custom_button(__('Log Event'), function() {
					frm.trigger('add_session_event');
				}, __('Actions'));
				
				frm.add_custom_button(__('Complete Session'), function() {
					frm.trigger('complete_session');
				}).addClass('btn-success');
			}
			
			if (frm.doc.status === 'Completed' && frm.doc.docstatus === 0) {
				frm.add_custom_button(__('Generate Invoice'), function() {
					frm.trigger('generate_invoice');
				}).addClass('btn-primary');
			}
			
			// Add vital signs monitoring
			frm.trigger('setup_vital_monitoring');
			
			// Show session progress
			frm.trigger('show_session_progress');
		}
		
		// Set status indicator
		frm.trigger('set_status_indicator');
	},
	
	start_session: function(frm) {
		frappe.confirm(
			__('Are you sure you want to start this dialysis session?'),
			function() {
				frappe.call({
					method: 'frappe.client.set_value',
					args: {
						doctype: 'Dialysis Session',
						name: frm.doc.name,
						fieldname: {
							status: 'In Progress',
							started_at: frappe.datetime.now_datetime()
						}
					},
					callback: function(r) {
						frm.reload_doc();
						frappe.show_alert({
							message: __('Session started successfully'),
							indicator: 'green'
						});
					}
				});
			}
		);
	},
	
	complete_session: function(frm) {
		// Validate required fields
		if (!frm.doc.post_dialysis_weight) {
			frappe.msgprint(__('Please enter Post-Dialysis Weight'));
			return;
		}
		
		frappe.confirm(
			__('Complete this dialysis session?'),
			function() {
				frappe.call({
					method: 'frappe.client.set_value',
					args: {
						doctype: 'Dialysis Session',
						name: frm.doc.name,
						fieldname: {
							status: 'Completed',
							completed_at: frappe.datetime.now_datetime()
						}
					},
					callback: function(r) {
						frm.reload_doc();
						frappe.show_alert({
							message: __('Session completed successfully'),
							indicator: 'green'
						});
					}
				});
			}
		);
	},
	
	add_vital_signs: function(frm) {
		// Add a new row to vital signs table
		let row = frm.add_child('vital_signs');
		frappe.model.set_value(row.doctype, row.name, 'reading_time', frappe.datetime.now_datetime());
		frm.refresh_field('vital_signs');
		
		// Scroll to the vital signs section
		frappe.utils.scroll_to(frm.fields_dict['vital_signs'].$wrapper, true);
	},
	
	add_session_event: function(frm) {
		// Dialog to add session event
		let d = new frappe.ui.Dialog({
			title: __('Log Session Event'),
			fields: [
				{
					fieldname: 'event_type',
					fieldtype: 'Select',
					label: __('Event Type'),
					options: 'Vital Sign Alert\nMachine Alarm\nHypotension\nHypertension\nCramping\nNausea/Vomiting\nChest Pain\nAccess Issue\nEquipment Malfunction\nMedication Given\nFluid Adjustment\nOther',
					reqd: 1
				},
				{
					fieldname: 'severity',
					fieldtype: 'Select',
					label: __('Severity'),
					options: 'Low\nMedium\nHigh\nCritical',
					default: 'Low',
					reqd: 1
				},
				{
					fieldname: 'description',
					fieldtype: 'Small Text',
					label: __('Description'),
					reqd: 1
				},
				{
					fieldname: 'action_taken',
					fieldtype: 'Small Text',
					label: __('Action Taken')
				}
			],
			primary_action_label: __('Log Event'),
			primary_action: function(values) {
				let row = frm.add_child('session_events');
				frappe.model.set_value(row.doctype, row.name, 'event_time', frappe.datetime.now_datetime());
				frappe.model.set_value(row.doctype, row.name, 'event_type', values.event_type);
				frappe.model.set_value(row.doctype, row.name, 'severity', values.severity);
				frappe.model.set_value(row.doctype, row.name, 'description', values.description);
				frappe.model.set_value(row.doctype, row.name, 'action_taken', values.action_taken);
				
				frm.refresh_field('session_events');
				d.hide();
				
				frappe.show_alert({
					message: __('Event logged successfully'),
					indicator: 'blue'
				});
			}
		});
		
		d.show();
	},
	
	generate_invoice: function(frm) {
		frappe.new_doc('Invoice', {
			patient: frm.doc.patient,
			patient_name: frm.doc.patient_name,
			dialysis_session: frm.doc.name
		});
	},
	
	setup_vital_monitoring: function(frm) {
		if (frm.doc.status !== 'In Progress') return;
		
		// Create vital signs chart
		if (frm.doc.vital_signs && frm.doc.vital_signs.length > 0) {
			frm.trigger('render_vitals_chart');
		}
	},
	
	render_vitals_chart: function(frm) {
		// Prepare data for chart
		let times = [];
		let bp_systolic = [];
		let bp_diastolic = [];
		let heart_rate = [];
		
		frm.doc.vital_signs.forEach(reading => {
			times.push(frappe.datetime.str_to_user(reading.reading_time));
			bp_systolic.push(reading.bp_systolic || 0);
			bp_diastolic.push(reading.bp_diastolic || 0);
			heart_rate.push(reading.heart_rate || 0);
		});
		
		// Render chart (requires Chart.js or Frappe Charts)
		console.log('Vital signs data:', {times, bp_systolic, bp_diastolic, heart_rate});
	},
	
	show_session_progress: function(frm) {
		if (!frm.doc.started_at) return;
		
		let now = frappe.datetime.now_datetime();
		let started = frappe.datetime.str_to_obj(frm.doc.started_at);
		let elapsed = frappe.datetime.get_diff(now, started) / 60; // minutes
		
		let duration = frm.doc.treatment_duration || 240;
		let progress = Math.min((elapsed / duration) * 100, 100);
		
		// Show progress bar
		let progress_html = `
			<div class="session-progress" style="margin: 15px 0;">
				<div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
					<span><strong>Session Progress</strong></span>
					<span>${Math.floor(elapsed)} / ${duration} minutes</span>
				</div>
				<div class="progress">
					<div class="progress-bar ${progress >= 100 ? 'progress-bar-success' : 'progress-bar-info'}" 
						 role="progressbar" 
						 style="width: ${progress}%"
						 aria-valuenow="${progress}" 
						 aria-valuemin="0" 
						 aria-valuemax="100">
						${Math.floor(progress)}%
					</div>
				</div>
			</div>
		`;
		
		// Add to dashboard
		frm.dashboard.add_comment(progress_html, true);
	},
	
	set_status_indicator: function(frm) {
		const status_colors = {
			'Scheduled': 'blue',
			'In Progress': 'orange',
			'Completed': 'green',
			'Cancelled': 'red'
		};
		
		if (frm.doc.status) {
			frm.page.set_indicator(frm.doc.status, status_colors[frm.doc.status] || 'gray');
		}
	},
	
	pre_dialysis_weight: function(frm) {
		frm.trigger('calculate_weight_loss');
	},
	
	post_dialysis_weight: function(frm) {
		frm.trigger('calculate_weight_loss');
	},
	
	calculate_weight_loss: function(frm) {
		if (frm.doc.pre_dialysis_weight && frm.doc.post_dialysis_weight) {
			let weight_loss = frm.doc.pre_dialysis_weight - frm.doc.post_dialysis_weight;
			frm.set_value('weight_loss', weight_loss);
		}
	},
	
	started_at: function(frm) {
		frm.trigger('calculate_actual_duration');
	},
	
	completed_at: function(frm) {
		frm.trigger('calculate_actual_duration');
	},
	
	calculate_actual_duration: function(frm) {
		if (frm.doc.started_at && frm.doc.completed_at) {
			let duration = frappe.datetime.get_diff(frm.doc.completed_at, frm.doc.started_at) / 60; // minutes
			frm.set_value('actual_duration', Math.round(duration));
		}
	}
});

// Vital Signs Reading child table events
frappe.ui.form.on('Vital Signs Reading', {
	bp_systolic: function(frm, cdt, cdn) {
		check_vital_alerts(frm, cdt, cdn);
	},
	
	bp_diastolic: function(frm, cdt, cdn) {
		check_vital_alerts(frm, cdt, cdn);
	},
	
	heart_rate: function(frm, cdt, cdn) {
		check_vital_alerts(frm, cdt, cdn);
	},
	
	oxygen_saturation: function(frm, cdt, cdn) {
		check_vital_alerts(frm, cdt, cdn);
	}
});

function check_vital_alerts(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	let alerts = [];
	
	// Check BP
	if (row.bp_systolic > 180 || row.bp_systolic < 90) {
		alerts.push(`Critical BP: ${row.bp_systolic}/${row.bp_diastolic}`);
	} else if (row.bp_systolic > 140 || row.bp_systolic < 100) {
		alerts.push(`Warning BP: ${row.bp_systolic}/${row.bp_diastolic}`);
	}
	
	// Check Heart Rate
	if (row.heart_rate > 120 || row.heart_rate < 50) {
		alerts.push(`Critical HR: ${row.heart_rate} bpm`);
	} else if (row.heart_rate > 100 || row.heart_rate < 60) {
		alerts.push(`Warning HR: ${row.heart_rate} bpm`);
	}
	
	// Check O2 Saturation
	if (row.oxygen_saturation && row.oxygen_saturation < 90) {
		alerts.push(`Critical O2: ${row.oxygen_saturation}%`);
	} else if (row.oxygen_saturation && row.oxygen_saturation < 95) {
		alerts.push(`Warning O2: ${row.oxygen_saturation}%`);
	}
	
	if (alerts.length > 0) {
		frappe.show_alert({
			message: alerts.join(', '),
			indicator: 'red'
		});
		
		frappe.model.set_value(cdt, cdn, 'alert_notes', alerts.join('; '));
	}
}
