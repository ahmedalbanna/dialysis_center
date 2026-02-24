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
			
			frm.add_custom_button(__('Upload Document'), function() {
				frappe.new_doc('Patient Document', {
					patient: frm.doc.name,
					patient_name: frm.doc.patient_name
				});
			}, __('Actions'));
			
			frm.add_custom_button(__('View Sessions'), function() {
				frappe.set_route('List', 'Dialysis Session', {patient: frm.doc.name});
			}, __('View'));
			
			frm.add_custom_button(__('View Invoices'), function() {
				frappe.set_route('List', 'Invoice', {patient: frm.doc.name});
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
		
		// Add quick stats
		if (!frm.is_new()) {
			show_patient_stats(frm);
		}
	},
	
	date_of_birth: function(frm) {
		// Auto-calculate age when DOB changes
		if (frm.doc.date_of_birth) {
			calculate_age(frm);
		}
	},
	
	national_id: function(frm) {
		// Check for duplicate national ID
		if (frm.doc.national_id) {
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
	},
	
	email: function(frm) {
		// Validate email format
		if (frm.doc.email) {
			const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
			if (!email_pattern.test(frm.doc.email)) {
				frappe.msgprint({
					title: __('Invalid Email'),
					message: __('Please enter a valid email address'),
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
		
		// Show warning for unusual ages
		if (age < 18) {
			frappe.msgprint({
				title: __('Minor Patient'),
				message: __('Patient is under 18 years old'),
				indicator: 'orange'
			});
		} else if (age > 100) {
			frappe.msgprint({
				title: __('Please Verify'),
				message: __('Patient age appears to be {0} years. Please verify date of birth.', [age]),
				indicator: 'orange'
			});
		}
	}
}

function show_patient_stats(frm) {
	// Fetch and display patient statistics
	frappe.call({
		method: 'dialysis_center.api.patient.get_patient_dashboard',
		args: {
			patient: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.statistics) {
				const stats = r.message.statistics;
				
				// Create HTML for stats
				const stats_html = `
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
								<div style="font-size: 24px; font-weight: bold; color: #f5222d;">${format_currency(stats.total_outstanding || 0)}</div>
								<div style="color: #666; font-size: 12px;">Outstanding Amount</div>
							</div>
						</div>
					</div>
				`;
				
				// Add stats to form
				if (!frm.fields_dict.patient_stats) {
					const stats_field = frm.add_custom_button('', () => {}, '', 'stats_wrapper');
				}
				
				$(frm.fields_dict.patient_name.wrapper).after(stats_html);
			}
		}
	});
}
