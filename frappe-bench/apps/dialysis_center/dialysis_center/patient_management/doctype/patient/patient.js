frappe.ui.form.on('Patient', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add custom buttons
			frm.add_custom_button(__('Schedule Appointment'), function() {
				frappe.new_doc('Appointment', {
					patient: frm.doc.name,
					patient_name: frm.doc.patient_name
				});
			}, __('Actions'));
			
			frm.add_custom_button(__('New Session'), function() {
				frappe.new_doc('Dialysis Session', {
					patient: frm.doc.name,
					patient_name: frm.doc.patient_name
				});
			}, __('Actions'));
			
			frm.add_custom_button(__('Generate Invoice'), function() {
				frappe.new_doc('Invoice', {
					patient: frm.doc.name,
					patient_name: frm.doc.patient_name
				});
			}, __('Actions'));
			
			frm.add_custom_button(__('View Treatment History'), function() {
				frappe.set_route('query-report', 'Patient Treatment History', {patient: frm.doc.name});
			}, __('Reports'));
			
			// Add dashboard
			frm.trigger('show_patient_dashboard');
			
			// Add indicators
			frm.trigger('set_status_indicators');
		}
	},
	
	show_patient_dashboard: function(frm) {
		if (frm.doc.__islocal) return;
		
		// Clear existing dashboard
		frm.dashboard.clear_headline();
		
		// Get patient summary
		frappe.call({
			method: 'dialysis_center.patient_management.doctype.patient.patient.get_patient_summary',
			args: {patient: frm.doc.name},
			callback: function(r) {
				if (r.message) {
					frm.trigger('render_dashboard', r.message);
				}
			}
		});
	},
	
	render_dashboard: function(frm, data) {
		if (!data) return;
		
		// Create dashboard HTML
		let html = `
			<div class="patient-dashboard" style="margin-bottom: 15px;">
				<div class="row">
					<div class="col-sm-3">
						<div class="dashboard-card">
							<div class="card-header">Recent Sessions</div>
							<div class="card-value">${data.recent_sessions ? data.recent_sessions.length : 0}</div>
						</div>
					</div>
					<div class="col-sm-3">
						<div class="dashboard-card">
							<div class="card-header">Upcoming Appointments</div>
							<div class="card-value">${data.upcoming_appointments ? data.upcoming_appointments.length : 0}</div>
						</div>
					</div>
					<div class="col-sm-3">
						<div class="dashboard-card">
							<div class="card-header">Outstanding Amount</div>
							<div class="card-value">${format_currency(data.total_outstanding || 0)}</div>
						</div>
					</div>
					<div class="col-sm-3">
						<div class="dashboard-card">
							<div class="card-header">Patient Status</div>
							<div class="card-value status-${(frm.doc.status || '').toLowerCase()}">${frm.doc.status || 'Unknown'}</div>
						</div>
					</div>
				</div>
			</div>
		`;
		
		// Add to form
		frm.fields_dict['patient_dashboard_html'].$wrapper.html(html);
		
		// Render recent sessions timeline
		if (data.recent_sessions && data.recent_sessions.length > 0) {
			frm.trigger('render_sessions_timeline', data.recent_sessions);
		}
		
		// Render upcoming appointments
		if (data.upcoming_appointments && data.upcoming_appointments.length > 0) {
			frm.trigger('render_appointments_list', data.upcoming_appointments);
		}
	},
	
	render_sessions_timeline: function(frm, sessions) {
		let timeline_html = '<div class="sessions-timeline" style="margin-top: 20px;"><h5>Recent Sessions</h5>';
		
		sessions.forEach(session => {
			timeline_html += `
				<div class="timeline-item">
					<div class="timeline-badge badge-${session.status === 'Completed' ? 'success' : 'warning'}">
						<i class="fa fa-circle"></i>
					</div>
					<div class="timeline-content">
						<a href="/app/dialysis-session/${session.name}">${session.name}</a>
						<span class="text-muted"> - ${frappe.datetime.str_to_user(session.session_date)}</span>
						<span class="badge badge-sm badge-${session.status === 'Completed' ? 'success' : 'warning'}">${session.status}</span>
					</div>
				</div>
			`;
		});
		
		timeline_html += '</div>';
		
		// You'd need to add an HTML field in the DocType for this
		// For now, we'll add it to the dashboard section
	},
	
	render_appointments_list: function(frm, appointments) {
		let appt_html = '<div class="appointments-list" style="margin-top: 20px;"><h5>Upcoming Appointments</h5><ul>';
		
		appointments.forEach(appt => {
			appt_html += `
				<li>
					<a href="/app/appointment/${appt.name}">${appt.name}</a> - 
					${frappe.datetime.str_to_user(appt.appointment_date)} 
					${appt.appointment_time || ''}
				</li>
			`;
		});
		
		appt_html += '</ul></div>';
	},
	
	set_status_indicators: function(frm) {
		// Set color indicator based on patient status
		const status_colors = {
			'Active': 'green',
			'Inactive': 'gray',
			'Deceased': 'red',
			'Transferred': 'orange'
		};
		
		if (frm.doc.status) {
			frm.set_indicator_color(status_colors[frm.doc.status] || 'blue', frm.doc.status);
		}
	},
	
	date_of_birth: function(frm) {
		if (frm.doc.date_of_birth) {
			let age = frappe.datetime.get_age(frm.doc.date_of_birth);
			frm.set_value('age', age);
		}
	},
	
	national_id: function(frm) {
		// Check for duplicate national ID
		if (frm.doc.national_id && !frm.doc.__islocal) {
			frappe.call({
				method: 'frappe.client.get_list',
				args: {
					doctype: 'Patient',
					filters: {
						national_id: frm.doc.national_id,
						name: ['!=', frm.doc.name]
					},
					fields: ['name', 'patient_name']
				},
				callback: function(r) {
					if (r.message && r.message.length > 0) {
						frappe.msgprint({
							title: __('Duplicate National ID'),
							message: __('National ID already exists for patient: {0}', [r.message[0].patient_name]),
							indicator: 'red'
						});
					}
				}
			});
		}
	},
	
	status: function(frm) {
		// Warn when changing status to Inactive or Deceased
		if (frm.doc.status === 'Inactive' || frm.doc.status === 'Deceased') {
			frappe.msgprint({
				title: __('Status Change'),
				message: __('Please provide a reason for changing status to {0}', [frm.doc.status]),
				indicator: 'orange'
			});
		}
	}
});

// Medical History child table events
frappe.ui.form.on('Patient Medical History Item', {
	condition_type: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		
		// Auto-set severity based on condition type
		if (row.condition_type === 'Allergy') {
			if (!row.severity) {
				frappe.model.set_value(cdt, cdn, 'severity', 'Moderate');
			}
		}
	}
});
