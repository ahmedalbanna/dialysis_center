/**
 * Enhanced Dialysis Session Form with Real-time Vitals
 */

frappe.ui.form.on('Dialysis Session', {
	refresh: function(frm) {
		set_status_indicator(frm);
		
		// Add action buttons
		if (frm.doc.status === 'In Progress' && !frm.is_new()) {
			frm.add_custom_button(__('Record Vitals'), function() {
				show_vitals_dialog(frm);
			}, __('Actions'));
			
			frm.add_custom_button(__('Log Event'), function() {
				show_event_dialog(frm);
			}, __('Actions'));
			
			frm.add_custom_button(__('Complete Session'), function() {
				complete_session(frm);
			}, __('Actions'));
		}
		
		// Show vitals chart if session has vitals
		if (!frm.is_new() && frm.doc.vitals && frm.doc.vitals.length > 0) {
			render_vitals_chart(frm);
		}
		
		// Setup real-time updates
		if (frm.doc.status === 'In Progress') {
			setup_realtime_updates(frm);
		}
	}
});

function set_status_indicator(frm) {
	if (!window.DialysisCenter) return;
	
	const statusColors = window.DialysisCenter.constants.STATUS_COLORS;
	const color = statusColors[frm.doc.status] || 'gray';
	frm.page.set_indicator(__(frm.doc.status), color);
}

function show_vitals_dialog(frm) {
	const d = new frappe.ui.Dialog({
		title: __('Record Vital Signs'),
		fields: [
			{
				fieldtype: 'Column Break'
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
				fieldtype: 'Column Break'
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
				precision: 1
			},
			{
				fieldtype: 'Column Break'
			},
			{
				fieldtype: 'Float',
				fieldname: 'weight',
				label: __('Weight (kg)'),
				precision: 1
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'notes',
				label: __('Notes')
			}
		],
		primary_action_label: __('Record'),
		primary_action: async function(values) {
			// Validate vitals using utility
			if (window.DialysisCenter) {
				const bpValidation = window.DialysisCenter.validators.validators.bloodPressure(
					values.systolic_bp,
					values.diastolic_bp
				);
				
				if (!bpValidation.valid) {
					frappe.msgprint({
						title: __('Validation Error'),
						message: __(bpValidation.message),
						indicator: 'red'
					});
					return;
				}
			}
			
			try {
				if (window.DialysisCenter) {
					await window.DialysisCenter.api.SessionAPI.addVitalReading(frm.doc.name, values);
					frappe.show_alert({ message: __('Vitals recorded'), indicator: 'green' }, 3);
					frm.reload_doc();
					d.hide();
				}
			} catch (error) {
				frappe.msgprint({
					title: __('Error'),
					message: __('Failed to record vitals'),
					indicator: 'red'
				});
			}
		}
	});
	d.show();
}

function show_event_dialog(frm) {
	const d = new frappe.ui.Dialog({
		title: __('Log Session Event'),
		fields: [
			{
				fieldtype: 'Select',
				fieldname: 'event_type',
				label: __('Event Type'),
				options: '\nComplication\nMachine Issue\nPatient Request\nNurse Note',
				reqd: 1
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'description',
				label: __('Description'),
				reqd: 1
			}
		],
		primary_action_label: __('Log Event'),
		primary_action: function(values) {
			frappe.call({
				method: 'dialysis_center.api.session.log_session_event',
				args: {
					session: frm.doc.name,
					event_type: values.event_type,
					description: values.description
				},
				callback: function(r) {
					if (r.message) {
						frappe.show_alert({ message: __('Event logged'), indicator: 'blue' }, 3);
						frm.reload_doc();
						d.hide();
					}
				}
			});
		}
	});
	d.show();
}

function complete_session(frm) {
	frappe.confirm(
		__('Complete this dialysis session?'),
		async function() {
			try {
				if (window.DialysisCenter) {
					await window.DialysisCenter.api.SessionAPI.completeSession(frm.doc.name);
					frappe.show_alert({ message: __('Session completed'), indicator: 'green' }, 3);
					frm.reload_doc();
				}
			} catch (error) {
				frappe.msgprint({
					title: __('Error'),
					message: __('Failed to complete session'),
					indicator: 'red'
				});
			}
		}
	);
}

function render_vitals_chart(frm) {
	// Create container for chart
	const chartContainer = document.createElement('div');
	chartContainer.id = 'vitals-chart-container';
	chartContainer.style.margin = '20px 0';
	
	// Find a good place to insert (after vitals table)
	const vitalsField = frm.fields_dict.vitals;
	if (vitalsField && vitalsField.wrapper) {
		vitalsField.wrapper.parentNode.insertBefore(chartContainer, vitalsField.wrapper.nextSibling);
		
		// Mount Vue VitalsChart component here (placeholder for now)
		chartContainer.innerHTML = '<div style="padding: 20px; background: #f9fafb; border-radius: 8px;"><h4>Vitals Trend Chart</h4><canvas id="session-vitals-chart"></canvas></div>';
		
		// Render simple chart
		if (window.Chart) {
			render_simple_vitals_chart(frm.doc.vitals);
		}
	}
}

function render_simple_vitals_chart(vitals) {
	const canvas = document.getElementById('session-vitals-chart');
	if (!canvas) return;
	
	const ctx = canvas.getContext('2d');
	
	new Chart(ctx, {
		type: 'line',
		data: {
			labels: vitals.map((v, i) => `Reading ${i + 1}`),
			datasets: [
				{
					label: 'Systolic BP',
					data: vitals.map(v => v.systolic_bp),
					borderColor: '#ef4444',
					backgroundColor: 'rgba(239, 68, 68, 0.1)'
				},
				{
					label: 'Diastolic BP',
					data: vitals.map(v => v.diastolic_bp),
					borderColor: '#3b82f6',
					backgroundColor: 'rgba(59, 130, 246, 0.1)'
				},
				{
					label: 'Heart Rate',
					data: vitals.map(v => v.heart_rate),
					borderColor: '#f59e0b',
					backgroundColor: 'rgba(245, 158, 11, 0.1)'
				}
			]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			scales: {
				y: { beginAtZero: false }
			}
		}
	});
}

function setup_realtime_updates(frm) {
	// Listen for vital signs updates via Socket.IO
	frappe.realtime.on('vital_signs_added', function(data) {
		if (data.session === frm.doc.name) {
			console.log('New vital signs:', data.vitals);
			frm.reload_doc();
		}
	});
	
	frappe.realtime.on('session_event_logged', function(data) {
		if (data.session === frm.doc.name) {
			console.log('Session event:', data.event);
			frappe.show_alert({
				message: __('New event: {0}', [data.event.event_type]),
				indicator: 'blue'
			}, 5);
		}
	});
}
