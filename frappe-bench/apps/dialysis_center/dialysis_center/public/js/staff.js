// Staff Form Enhancement
// Features: Staff profile, qualifications, schedule, performance metrics

frappe.ui.form.on('Staff', {
	onload: function(frm) {
		frm.set_intro(__('Manage staff profiles and qualifications'));
		update_staff_indicator(frm);
	},
	
	refresh: function(frm) {
		update_staff_indicator(frm);
		
		if (!frm.is_new()) {
			// Show staff summary
			show_staff_summary(frm);
			
			// Add action buttons
			frm.add_custom_button(__('View Schedule'), function() {
				show_staff_schedule(frm);
			}, __('View'));
			
			frm.add_custom_button(__('Performance Metrics'), function() {
				show_performance_metrics(frm);
			}, __('Analytics'));
			
			// Add status toggle
			if (frm.doc.status === 'Active') {
				frm.add_custom_button(__('Deactivate'), function() {
					update_staff_status(frm, 'Inactive');
				}, __('Actions'));
			} else {
				frm.add_custom_button(__('Activate'), function() {
					update_staff_status(frm, 'Active');
				}, __('Actions'));
			}
		}
	},
	
	validate: function(frm) {
		if (!frm.doc.staff_name) {
			frappe.throw(__('Staff name is required'));
		}
		
		if (!frm.doc.designation) {
			frappe.throw(__('Designation is required'));
		}
		
		// Validate contact information
		if (frm.doc.email && !validate_email(frm.doc.email)) {
			frappe.throw(__('Invalid email address'));
		}
		
		if (frm.doc.phone && !validate_phone(frm.doc.phone)) {
			frappe.throw(__('Invalid phone number'));
		}
	},
	
	before_save: function(frm) {
		// Set initials for avatar
		if (!frm.doc.initials && frm.doc.staff_name) {
			const names = frm.doc.staff_name.trim().split(' ');
			const initials = names.map(n => n[0]).join('').substring(0, 2).toUpperCase();
			frm.set_value('initials', initials);
		}
	},
	
	after_save: function(frm) {
		frappe.msgprint(__('Staff information saved successfully'));
	},
	
	// Field-level events
	designation: function(frm) {
		// Auto-load role permissions based on designation
		if (frm.doc.designation) {
			frappe.call({
				method: 'dialysis_center.api.staff.get_designation_permissions',
				args: {
					designation: frm.doc.designation
				},
				callback: function(r) {
					if (r.message && r.message.permissions) {
						const perms = r.message.permissions;
						frm.set_value('can_approve_sessions', perms.can_approve_sessions);
						frm.set_value('can_prescribe', perms.can_prescribe);
						frm.set_value('can_access_records', perms.can_access_records);
					}
				}
			});
		}
	},
	
	start_date: function(frm) {
		// Calculate tenure
		if (frm.doc.start_date) {
			const today = new Date();
			const start = new Date(frm.doc.start_date);
			const tenure_days = Math.floor((today - start) / (1000 * 60 * 60 * 24));
			
			if (tenure_days >= 0) {
				const years = Math.floor(tenure_days / 365);
				const months = Math.floor((tenure_days % 365) / 30);
				frm.set_value('tenure_years', years);
			}
		}
	},
	
	status: function(frm) {
		update_staff_indicator(frm);
	}
});

// Staff List View
frappe.listview_settings['Staff'] = {
	add_fields: ['staff_name', 'designation', 'status', 'phone', 'email'],
	
	formatters: {
		status: function(value) {
			const colors = {
				'Active': 'green',
				'Inactive': 'red',
				'On Leave': 'orange'
			};
			
			return `<span style="background-color: ${colors[value] || 'white'}; color: white; padding: 4px 8px; border-radius: 3px; font-weight: bold;">${value}</span>`;
		},
		
		designation: function(value) {
			return `<span style="color: #666;">${value}</span>`;
		}
	},
	
	filters: [
		['status', '!=', 'Terminated']
	],
	
	onload: function(listview) {
		// Add filters
		listview.page.add_action_item(__('Active Staff'), function() {
			listview.filter_area.add([
				['Staff', 'status', '=', 'Active']
			]);
			listview.refresh();
		});
		
		listview.page.add_action_item(__('On Leave'), function() {
			listview.filter_area.add([
				['Staff', 'status', '=', 'On Leave']
			]);
			listview.refresh();
		});
		
		// Bulk actions
		listview.page.add_menu_item(__('Generate Payroll'), function() {
			const selected = listview.get_checked_items();
			if (selected.length === 0) {
				frappe.msgprint(__('Please select staff members'));
				return;
			}
			
			frappe.msgprint(__('Payroll generation functionality'));
		});
	}
};

// Helper functions

function update_staff_indicator(frm) {
	const status_colors = {
		'Active': 'green',
		'Inactive': 'red',
		'On Leave': 'orange',
		'Terminated': 'darkred'
	};
	
	const color = status_colors[frm.doc.status] || 'gray';
	frm.page.set_indicator(__(frm.doc.status || 'Inactive'), color);
}

function validate_email(email) {
	const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	return pattern.test(email);
}

function validate_phone(phone) {
	const pattern = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/;
	return pattern.test(phone.replace(/\s/g, ''));
}

function show_staff_summary(frm) {
	const summary_html = `
		<div class="staff-summary" style="margin: 15px 0; padding: 15px; background: #f5f5f5; border-radius: 5px;">
			<div class="row">
				<div class="col-sm-3">
					<small>Designation</small><br/>
					<strong>${frm.doc.designation}</strong>
				</div>
				<div class="col-sm-3">
					<small>Status</small><br/>
					<strong style="color: ${frm.doc.status === 'Active' ? '#52c41a' : '#f5222d'}">${frm.doc.status}</strong>
				</div>
				<div class="col-sm-3">
					<small>Tenure</small><br/>
					<strong>${frm.doc.tenure_years || 0} years</strong>
				</div>
				<div class="col-sm-3">
					<small>Qualifications</small><br/>
					<strong>${frm.doc.qualifications ? frm.doc.qualifications.split(',').length : 0}</strong>
				</div>
			</div>
		</div>
	`;
	
	$(frm.wrapper).find('.staff-summary').remove();
	$(frm.fields_dict.staff_name.wrapper).after(summary_html);
}

function show_staff_schedule(frm) {
	frappe.call({
		method: 'dialysis_center.api.staff.get_staff_schedule',
		args: {
			staff: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.schedule) {
				const schedule = r.message.schedule;
				
				const dialog = new frappe.ui.Dialog({
					title: __('Staff Schedule'),
					size: 'large',
					fields: [
						{
							fieldtype: 'HTML',
							fieldname: 'schedule_html',
							html: render_schedule_table(schedule)
						}
					]
				});
				
				dialog.show();
			}
		}
	});
}

function render_schedule_table(schedule) {
	const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
	
	const rows = days.map(day => {
		const day_schedule = schedule[day] || {};
		const is_off = !day_schedule.start_time;
		
		return `
			<tr>
				<td><strong>${day}</strong></td>
				<td>${is_off ? 'Off' : day_schedule.start_time}</td>
				<td>${is_off ? '' : day_schedule.end_time}</td>
			</tr>
		`;
	}).join('');
	
	return `
		<table class="table table-sm">
			<thead>
				<tr>
					<th>Day</th>
					<th>Start Time</th>
					<th>End Time</th>
				</tr>
			</thead>
			<tbody>
				${rows}
			</tbody>
		</table>
	`;
}

function show_performance_metrics(frm) {
	frappe.call({
		method: 'dialysis_center.api.staff.get_performance_metrics',
		args: {
			staff: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.metrics) {
				const metrics = r.message.metrics;
				
				const dialog = new frappe.ui.Dialog({
					title: __('Performance Metrics'),
					size: 'large',
					fields: [
						{
							fieldtype: 'HTML',
							fieldname: 'metrics_html',
							html: `
								<div style="padding: 20px;">
									<div class="row" style="margin-bottom: 20px;">
										<div class="col-sm-3">
											<div style="background: #e6f7ff; padding: 20px; border-radius: 5px; text-align: center;">
												<div style="font-size: 24px; font-weight: bold; color: #1890ff;">${metrics.total_sessions || 0}</div>
												<small>Sessions Facilitated</small>
											</div>
										</div>
										<div class="col-sm-3">
											<div style="background: #f6ffed; padding: 20px; border-radius: 5px; text-align: center;">
												<div style="font-size: 24px; font-weight: bold; color: #52c41a;">${metrics.completion_rate || 0}%</div>
												<small>Completion Rate</small>
											</div>
										</div>
										<div class="col-sm-3">
											<div style="background: #fff7e6; padding: 20px; border-radius: 5px; text-align: center;">
												<div style="font-size: 24px; font-weight: bold; color: #faad14;">${metrics.average_rating || 0}</div>
												<small>Average Rating</small>
											</div>
										</div>
										<div class="col-sm-3">
											<div style="background: #f9f9f9; padding: 20px; border-radius: 5px; text-align: center;">
												<div style="font-size: 24px; font-weight: bold; color: #666;">${metrics.attendance_rate || 0}%</div>
												<small>Attendance Rate</small>
											</div>
										</div>
									</div>
									${metrics.recent_evaluations ? `
										<h6>Recent Evaluations</h6>
										${metrics.recent_evaluations.map(e => `
											<div style="padding: 10px; border-bottom: 1px solid #ddd; margin-bottom: 10px;">
												<div><strong>${e.evaluator}</strong> - ${frappe.datetime.str_to_user(e.evaluation_date)}</div>
												<div style="color: #666; margin: 5px 0;">${e.comments}</div>
												<div style="color: #faad14;">Rating: ${e.rating}/5</div>
											</div>
										`).join('')}
									` : ''}
								</div>
							`
						}
					]
				});
				
				dialog.show();
			}
		}
	});
}

function update_staff_status(frm, new_status) {
	frappe.call({
		method: 'dialysis_center.api.staff.update_staff_status',
		args: {
			staff: frm.doc.name,
			new_status: new_status
		},
		callback: function(r) {
			if (r.message && r.message.success) {
				frm.set_value('status', new_status);
				frm.save();
				frappe.msgprint(__('Staff status updated'));
			}
		}
	});
}
