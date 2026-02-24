// Enhanced Dialysis Session Form
// Features: Real-time vital signs monitoring, session timeline, event logging

frappe.ui.form.on('Dialysis Session', {
	onload: function(frm) {
		// Initialize session monitoring
		frm.set_intro(__('Monitor and record dialysis session progress'));
		
		// Load session events
		if (!frm.is_new()) {
			load_session_events(frm);
		}
	},
	
	refresh: function(frm) {
		// Update session status indicator
		update_session_indicator(frm);
		
		// Control field visibility based on session status
		update_session_form_fields(frm);
		
		// Show vital signs chart for ongoing sessions
		if (!frm.is_new() && frm.doc.status === 'In Progress') {
			render_vital_signs_chart(frm);
			
			// Add real-time monitoring button
			frm.add_custom_button(__('Add Vital Signs'), function() {
				show_vital_signs_dialog(frm);
			}, __('Monitoring'));
			
			// Add event logging button
			frm.add_custom_button(__('Log Event'), function() {
				show_session_event_dialog(frm);
			}, __('Monitoring'));
		}
		
		// Show completed session summary
		if (frm.doc.status === 'Completed') {
			show_session_summary(frm);
		}
		
		// Add session actions
		if (frm.doc.status === 'Scheduled') {
			frm.add_custom_button(__('Start Session'), function() {
				start_session(frm);
			}, __('Actions'));
		}
		
		if (frm.doc.status === 'In Progress') {
			frm.add_custom_button(__('End Session'), function() {
				end_session(frm);
			}, __('Actions'));
			
			frm.add_custom_button(__('Emergency Stop'), function() {
				emergency_stop_session(frm);
			}, __('Actions'));
		}
	},
	
	validate: function(frm) {
		// Validate required fields
		if (!frm.doc.patient) {
			frappe.throw(__('Patient is required'));
		}
		
		if (!frm.doc.appointment) {
			frappe.throw(__('Appointment is required'));
		}
		
		if (!frm.doc.session_date) {
			frappe.throw(__('Session date is required'));
		}
		
		// Validate session times
		if (frm.doc.status === 'In Progress') {
			if (!frm.doc.actual_start_time) {
				frappe.throw(__('Actual start time is required for in-progress sessions'));
			}
		}
		
		if (frm.doc.status === 'Completed') {
			if (!frm.doc.actual_start_time || !frm.doc.actual_end_time) {
				frappe.throw(__('Both start and end times are required for completed sessions'));
			}
			
			const start = new Date(frm.doc.actual_start_time);
			const end = new Date(frm.doc.actual_end_time);
			
			if (end <= start) {
				frappe.throw(__('End time must be after start time'));
			}
		}
	},
	
	before_save: function(frm) {
		// Calculate session duration if completed
		if (frm.doc.status === 'Completed' && frm.doc.actual_start_time && frm.doc.actual_end_time) {
			const start = new Date(frm.doc.actual_start_time);
			const end = new Date(frm.doc.actual_end_time);
			const duration_minutes = Math.round((end - start) / (1000 * 60));
			frm.set_value('actual_duration_minutes', duration_minutes);
		}
	},
	
	after_save: function(frm) {
		frappe.msgprint(__('Session saved successfully'));
		
		// Refresh vital signs display
		render_vital_signs_chart(frm);
	},
	
	// Field-level events
	patient: function(frm) {
		// Fetch patient dialysis schedule when patient changes
		if (frm.doc.patient) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Patient',
					filters: { name: frm.doc.patient },
					fieldname: ['patient_name', 'blood_type', 'weight']
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('patient_name', r.message.patient_name);
						frm.set_value('patient_blood_type', r.message.blood_type);
						frm.set_value('patient_weight', r.message.weight);
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
					fieldname: ['appointment_date', 'appointment_time', 'scheduled_duration']
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('session_date', r.message.appointment_date);
						frm.set_value('scheduled_start_time', r.message.appointment_time);
						frm.set_value('scheduled_duration_minutes', r.message.scheduled_duration);
					}
				}
			});
		}
	},
	
	dialysis_machine: function(frm) {
		// Load machine details
		if (frm.doc.dialysis_machine) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Dialysis Machine',
					filters: { name: frm.doc.dialysis_machine },
					fieldname: ['machine_name', 'serial_number', 'status']
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('machine_name', r.message.machine_name);
						
						if (r.message.status !== 'Operational') {
							frappe.msgprint({
								title: __('Machine Status'),
								message: __('Machine status is {0}. Please verify before use.', [r.message.status]),
								indicator: 'orange'
							});
						}
					}
				}
			});
		}
	},
	
	status: function(frm) {
		// Update indicator when status changes
		update_session_indicator(frm);
		frm.refresh();
	}
});

// Appointment-specific list view customization
frappe.listview_settings['Dialysis Session'] = {
	add_fields: ['patient_name', 'status', 'session_date', 'actual_duration_minutes', 'complication_notes'],
	
	formatters: {
		status: function(value) {
			const colors = {
				'Scheduled': 'lightblue',
				'In Progress': 'lightyellow',
				'Completed': 'lightgreen',
				'Cancelled': 'lightcoral',
				'Emergency Stop': 'red'
			};
			
			return `<span style="background-color: ${colors[value] || 'white'}; padding: 4px 8px; border-radius: 3px;">${value}</span>`;
		},
		
		session_date: function(value) {
			return frappe.datetime.str_to_user(value);
		},
		
		actual_duration_minutes: function(value) {
			if (!value) return '-';
			const hours = Math.floor(value / 60);
			const mins = value % 60;
			return `${hours}h ${mins}m`;
		}
	},
	
	filters: [
		['status', '!=', 'Cancelled']
	],
	
	onload: function(listview) {
		// Add custom filters
		listview.page.add_action_item(__('Today\'s Sessions'), function() {
			listview.filter_area.add([
				['Dialysis Session', 'session_date', '=', frappe.datetime.now_date()]
			]);
			listview.refresh();
		});
		
		// Add bulk actions
		listview.page.add_menu_item(__('Generate Report'), function() {
			const selected = listview.get_checked_items();
			if (selected.length === 0) {
				frappe.msgprint(__('Please select sessions'));
				return;
			}
			
			frappe.call({
				method: 'dialysis_center.api.dialysis_session.generate_session_report',
				args: {
					sessions: selected.map(d => d.name)
				},
				callback: function(r) {
					if (r.message) {
						frappe.msgprint(__('Report generated successfully'));
					}
				}
			});
		});
	}
};

// Helper functions

function update_session_indicator(frm) {
	const status_color = {
		'Scheduled': 'blue',
		'In Progress': 'orange',
		'Completed': 'green',
		'Cancelled': 'red',
		'Emergency Stop': 'darkred'
	};
	
	const color = status_color[frm.doc.status] || 'gray';
	frm.page.set_indicator(__(frm.doc.status), color);
}

function update_session_form_fields(frm) {
	// Read-only patient info during session
	if (frm.doc.status !== 'Scheduled') {
		frm.set_df_property('patient', 'read_only', 1);
		frm.set_df_property('appointment', 'read_only', 1);
		frm.set_df_property('dialysis_machine', 'read_only', 1);
	}
	
	// Read-only start time after session started
	if (frm.doc.status === 'In Progress' || frm.doc.status === 'Completed') {
		frm.set_df_property('actual_start_time', 'read_only', 1);
	}
}

function start_session(frm) {
	frappe.call({
		method: 'dialysis_center.api.dialysis_session.start_session',
		args: {
			session: frm.doc.name,
			start_time: frappe.datetime.now_datetime()
		},
		callback: function(r) {
			if (r.message && r.message.success) {
				frm.set_value('status', 'In Progress');
				frm.set_value('actual_start_time', r.message.start_time);
				frm.save();
				frappe.msgprint(__('Session started successfully'));
			}
		}
	});
}

function end_session(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('End Dialysis Session'),
		fields: [
			{
				fieldtype: 'Datetime',
				fieldname: 'end_time',
				label: __('End Time'),
				default: frappe.datetime.now_datetime(),
				reqd: 1
			},
			{
				fieldtype: 'Link',
				fieldname: 'nephrologist',
				label: __('Nephrologist Review'),
				options: 'Staff',
				reqd: 1
			},
			{
				fieldtype: 'Text',
				fieldname: 'completion_notes',
				label: __('Completion Notes')
			},
			{
				fieldtype: 'Check',
				fieldname: 'patient_tolerated_well',
				label: __('Patient Tolerated Well')
			}
		],
		primary_action_label: __('End Session'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.dialysis_session.end_session',
				args: {
					session: frm.doc.name,
					end_time: values.end_time,
					nephrologist: values.nephrologist,
					completion_notes: values.completion_notes,
					patient_tolerated_well: values.patient_tolerated_well
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frm.set_value('status', 'Completed');
						frm.set_value('actual_end_time', values.end_time);
						frm.set_value('nephrologist_review', values.nephrologist);
						frm.set_value('completion_notes', values.completion_notes);
						frm.save();
						frappe.msgprint(__('Session completed successfully'));
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function emergency_stop_session(frm) {
	frappe.confirm(
		__('Are you sure you want to perform an emergency stop? This action is critical.'),
		function() {
			const dialog = new frappe.ui.Dialog({
				title: __('Emergency Stop Session'),
				fields: [
					{
						fieldtype: 'Text',
						fieldname: 'reason',
						label: __('Reason for Emergency Stop'),
						reqd: 1
					},
					{
						fieldtype: 'Text',
						fieldname: 'actions_taken',
						label: __('Actions Taken'),
						reqd: 1
					}
				],
				primary_action_label: __('Confirm Emergency Stop'),
				primary_action(values) {
					frappe.call({
						method: 'dialysis_center.api.dialysis_session.emergency_stop',
						args: {
							session: frm.doc.name,
							reason: values.reason,
							actions_taken: values.actions_taken,
							stop_time: frappe.datetime.now_datetime()
						},
						callback: function(r) {
							if (r.message && r.message.success) {
								frm.set_value('status', 'Emergency Stop');
								frm.set_value('complication_notes', values.reason);
								frm.save();
								frappe.msgprint({
									title: __('Emergency Stop Recorded'),
									message: __('Emergency stop has been recorded. Patient may require immediate medical attention.'),
									indicator: 'red'
								});
								dialog.hide();
							}
						}
					});
				}
			});
			
			dialog.show();
		}
	);
}

function show_vital_signs_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Record Vital Signs'),
		fields: [
			{
				fieldtype: 'Datetime',
				fieldname: 'reading_time',
				label: __('Reading Time'),
				default: frappe.datetime.now_datetime(),
				reqd: 1
			},
			{
				fieldtype: 'Int',
				fieldname: 'systolic_bp',
				label: __('Systolic BP (mmHg)'),
				reqd: 1
			},
			{
				fieldtype: 'Int',
				fieldname: 'diastolic_bp',
				label: __('Diastolic BP (mmHg)'),
				reqd: 1
			},
			{
				fieldtype: 'Int',
				fieldname: 'heart_rate',
				label: __('Heart Rate (bpm)'),
				reqd: 1
			},
			{
				fieldtype: 'Float',
				fieldname: 'temperature',
				label: __('Temperature (°C)'),
				reqd: 1
			},
			{
				fieldtype: 'Int',
				fieldname: 'respiratory_rate',
				label: __('Respiratory Rate (breaths/min)'),
				reqd: 1
			},
			{
				fieldtype: 'Float',
				fieldname: 'oxygen_saturation',
				label: __('O2 Saturation (%)'),
				reqd: 1
			},
			{
				fieldtype: 'Text',
				fieldname: 'notes',
				label: __('Notes')
			}
		],
		primary_action_label: __('Save'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.dialysis_session.add_vital_signs',
				args: {
					session: frm.doc.name,
					vital_signs: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Vital signs recorded'));
						render_vital_signs_chart(frm);
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function show_session_event_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Log Session Event'),
		fields: [
			{
				fieldtype: 'Datetime',
				fieldname: 'event_time',
				label: __('Event Time'),
				default: frappe.datetime.now_datetime(),
				reqd: 1
			},
			{
				fieldtype: 'Select',
				fieldname: 'event_type',
				label: __('Event Type'),
				options: '\nVital Signs\nMedication Administered\nComplication\nDevice Alarm\nStaff Intervention\nOther',
				reqd: 1
			},
			{
				fieldtype: 'Text',
				fieldname: 'event_description',
				label: __('Event Description'),
				reqd: 1
			},
			{
				fieldtype: 'Select',
				fieldname: 'severity',
				label: __('Severity'),
				options: '\nMinor\nModerate\nSevere\nCritical'
			},
			{
				fieldtype: 'Text',
				fieldname: 'intervention',
				label: __('Intervention Taken')
			}
		],
		primary_action_label: __('Log Event'),
		primary_action(values) {
			frappe.call({
				method: 'dialysis_center.api.dialysis_session.log_session_event',
				args: {
					session: frm.doc.name,
					event: values
				},
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__('Event logged successfully'));
						load_session_events(frm);
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function render_vital_signs_chart(frm) {
	frappe.call({
		method: 'dialysis_center.api.dialysis_session.get_vital_signs',
		args: {
			session: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.vital_signs) {
				const vitals = r.message.vital_signs;
				
				// Create vital signs chart
				const chart_html = `
					<div class="vital-signs-chart" style="margin: 15px 0; padding: 15px; background: #f9f9f9; border-radius: 5px; border-left: 4px solid #1890ff;">
						<h6>Latest Vital Signs</h6>
						<div class="row" style="margin-bottom: 10px;">
							<div class="col-sm-2">
								<small>BP</small><br/>
								<strong>${vitals[0]?.systolic_bp || '-'}/${vitals[0]?.diastolic_bp || '-'}</strong>
							</div>
							<div class="col-sm-2">
								<small>HR</small><br/>
								<strong>${vitals[0]?.heart_rate || '-'}</strong>
							</div>
							<div class="col-sm-2">
								<small>Temp</small><br/>
								<strong>${vitals[0]?.temperature || '-'}°C</strong>
							</div>
							<div class="col-sm-2">
								<small>RR</small><br/>
								<strong>${vitals[0]?.respiratory_rate || '-'}</strong>
							</div>
							<div class="col-sm-2">
								<small>O2 Sat</small><br/>
								<strong>${vitals[0]?.oxygen_saturation || '-'}%</strong>
							</div>
							<div class="col-sm-2">
								<small>Time</small><br/>
								<small>${vitals[0] ? frappe.datetime.str_to_user(vitals[0].reading_time) : '-'}</small>
							</div>
						</div>
					</div>
				`;
				
				$(frm.wrapper).find('.vital-signs-chart').remove();
				$(frm.fields_dict.patient_name.wrapper).after(chart_html);
			}
		}
	});
}

function load_session_events(frm) {
	frappe.call({
		method: 'dialysis_center.api.dialysis_session.get_session_events',
		args: {
			session: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.events) {
				const events = r.message.events;
				
				if (events.length === 0) {
					return;
				}
				
				// Create event timeline
				const timeline_html = `
					<div class="session-events-timeline" style="margin: 15px 0; padding: 15px; background: #f5f5f5; border-radius: 5px;">
						<h6>Session Events</h6>
						<div class="timeline">
							${events.map((event, idx) => `
								<div class="timeline-item" style="padding: 10px; border-left: 2px solid #1890ff; margin-left: 10px; padding-left: 15px;">
									<div style="color: #666; font-size: 12px;">
										${frappe.datetime.str_to_user(event.event_time)}
									</div>
									<div style="font-weight: bold; margin: 5px 0;">
										${event.event_type}
									</div>
									<div>${event.event_description}</div>
									${event.severity ? `<div style="color: #f5222d; margin-top: 5px;"><small>Severity: ${event.severity}</small></div>` : ''}
								</div>
							`).join('')}
						</div>
					</div>
				`;
				
				$(frm.wrapper).find('.session-events-timeline').remove();
				$(frm.fields_dict.patient_name.wrapper).after(timeline_html);
			}
		}
	});
}

function show_session_summary(frm) {
	frappe.call({
		method: 'dialysis_center.api.dialysis_session.get_session_summary',
		args: {
			session: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.summary) {
				const summary = r.message.summary;
				const summary_html = `
					<div class="session-summary" style="margin: 15px 0; padding: 15px; background: #f6ffed; border-radius: 5px; border-left: 4px solid #52c41a;">
						<h6>Session Summary</h6>
						<div class="row">
							<div class="col-sm-3">
								<small>Duration</small><br/>
								<strong>${summary.duration_hours}h ${summary.duration_minutes}m</strong>
							</div>
							<div class="col-sm-3">
								<small>Events</small><br/>
								<strong>${summary.event_count}</strong>
							</div>
							<div class="col-sm-3">
								<small>Complications</small><br/>
								<strong>${summary.complication_count}</strong>
							</div>
							<div class="col-sm-3">
								<small>Outcome</small><br/>
								<strong>${summary.patient_tolerated_well ? 'Good' : 'Requires Review'}</strong>
							</div>
						</div>
					</div>
				`;
				
				$(frm.wrapper).find('.session-summary').remove();
				$(frm.fields_dict.patient_name.wrapper).after(summary_html);
			}
		}
	});
}
