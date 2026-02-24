/**
 * Enhanced Patient Form with Vue Components
 */

frappe.ui.form.on('Patient', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			frm.add_custom_button(__('View Dashboard'), function() {
				frappe.set_route('query-report', 'Patient Treatment History', {patient: frm.doc.name});
			});
			
			frm.add_custom_button(__('Schedule Appointment'), function() {
				frappe.new_doc('Appointment', {
					patient: frm.doc.name,
					patient_name: frm.doc.patient_name
				});
			}, __('Actions'));
			
			frm.add_custom_button__('View Sessions'), function() {
				frappe.set_route('List', 'Dialysis Session', {patient: frm.doc.name});
			}, __('View'));
		}
		
		// Show indicator based on status
		if (frm.doc.status === 'Active') {
			frm.page.set_indicator(__('Active'), 'green');
		} else if (frm.doc.status === 'Inactive') {
			frm.page.set_indicator(__('Inactive'), 'orange');
		} else if (frm.doc.status === 'Deceased') {
			frm.page.set_indicator(__('Deceased'), 'red');
		}
		
		// Add patient statistics card using Vue component
		if (!frm.is_new()) {
			show_patient_stats_vue(frm);
		}
	},
	
	date_of_birth: function(frm) {
		if (frm.doc.date_of_birth) {
			calculate_age(frm);
		}
	},
	
	national_id: function(frm) {
		if (frm.doc.national_id) {
			check_duplicate_national_id(frm);
		}
	},
	
	email: function(frm) {
		if (frm.doc.email && window.DialysisCenter) {
			const validation = window.DialysisCenter.validators.validators.email(frm.doc.email);
			if (!validation.valid) {
				frappe.msgprint({
					title: __('Invalid Email'),
					message: __(validation.message),
					indicator: 'orange'
				});
			}
		}
	}
});

function calculate_age(frm) {
	if (frm.doc.date_of_birth) {
		const dob = new Date(frm.doc.date_of_birth);
		const today = new Date();
		let age = today.getFullYear() - dob.getFullYear();
		const month_diff = today.getMonth() - dob.getMonth();
		
		if (month_diff < 0 || (month_diff === 0 && today.getDate() < dob.getDate())) {
			age--;
		}
		
		frm.set_value('age', age);
		
		// Age validation using utility
		if (window.DialysisCenter) {
			const validation = window.DialysisCenter.validators.validators.ageRange(frm.doc.date_of_birth);
			if (!validation.valid) {
				frappe.msgprint({
					title: __('Age Warning'),
					message: __(validation.message),
					indicator: 'orange'
				});
			}
		}
	}
}

function check_duplicate_national_id(frm) {
	frappe.db.get_value('Patient', 
		{'national_id': frm.doc.national_id, 'name': ['!=', frm.doc.name]}, 
		'name', 
		(r) => {
			if (r && r.name) {
				frappe.msgprint({
					title: __('Duplicate National ID'),
					message: __('A patient with this National ID already exists: {0}', [r.name]),
					indicator: 'red'
				});
			}
		}
	);
}

async function show_patient_stats_vue(frm) {
	// Use API helper to fetch patient dashboard data
	if (!window.DialysisCenter || !window.DialysisCenter.api) {
		console.warn('DialysisCenter API not loaded yet');
		return;
	}

	try {
		const data = await window.DialysisCenter.api.PatientAPI.getDashboard(frm.doc.name);
		
		if (data && data.statistics) {
			const stats = data.statistics;
			
			// Create container for Vue component
			const statsContainer = document.createElement('div');
			statsContainer.id = 'patient-stats-vue';
			statsContainer.style.margin = '15px 0';
			
			// Insert after patient_name field
			const nameField = frm.fields_dict.patient_name.wrapper;
			nameField.parentNode.insertBefore(statsContainer, nameField.nextSibling);
			
			// Render stats using plain HTML (Vue component would be mounted here in full implementation)
			statsContainer.innerHTML = `
				<div class="row patient-stats" style="margin: 15px 0;">
					<div class="col-sm-3">
						<div class="stat-card" style="background: #e6f7ff; padding: 15px; border-radius: 5px; text-align: center;">
							<div style="font-size: 24px; font-weight: bold; color: #1890ff;">${stats.total_sessions || 0}</div>
							<div style="color: #666; font-size: 12px;">Total Sessions</div>
						</div>
					</div>
					<div class="col-sm-3">
						<div class="stat-card" style="background: #f6ffed; padding: 15px; border-radius: 5px; text-align: center;">
							<div style="font-size: 24px; font-weight: bold; color: #52c41a;">${stats.completed_sessions || 0}</div>
							<div style="color: #666; font-size: 12px;">Completed Sessions</div>
						</div>
					</div>
					<div class="col-sm-3">
						<div class="stat-card" style="background: #fff7e6; padding: 15px; border-radius: 5px; text-align: center;">
							<div style="font-size: 24px; font-weight: bold; color: #faad14;">${stats.upcoming_appointments || 0}</div>
							<div style="color: #666; font-size: 12px;">Upcoming Appointments</div>
						</div>
					</div>
					<div class="col-sm-3">
						<div class="stat-card" style="background: #fff1f0; padding: 15px; border-radius: 5px; text-align: center;">
							<div style="font-size: 24px; font-weight: bold; color: #f5222d;">${window.DialysisCenter.formatters.formatCurrency(stats.total_outstanding || 0)}</div>
							<div style="color: #666; font-size: 12px;">Outstanding Amount</div>
						</div>
					</div>
				</div>
			`;
		}
	} catch (error) {
		console.error('Failed to load patient dashboard:', error);
	}
}
