// Lab Test Form Enhancement
// Features: Test result tracking, trending analysis, abnormal value flagging

frappe.ui.form.on('Lab Test', {
	onload: function(frm) {
		frm.set_intro(__('Record and track laboratory test results'));
		update_lab_test_indicator(frm);
	},
	
	refresh: function(frm) {
		update_lab_test_indicator(frm);
		
		// Show previous results for comparison
		if (!frm.is_new()) {
			show_test_history(frm);
			
			// Add action buttons
			frm.add_custom_button(__('View Trending'), function() {
				show_trend_analysis(frm);
			}, __('Actions'));
			
			// Add approval button for pending results
			if (frm.doc.status === 'Pending') {
				frm.add_custom_button(__('Mark Complete'), function() {
					mark_test_complete(frm);
				}, __('Actions'));
			}
		}
		
		// Show abnormal values warning
		check_abnormal_values(frm);
	},
	
	validate: function(frm) {
		if (!frm.doc.patient) {
			frappe.throw(__('Patient is required'));
		}
		
		if (!frm.doc.test_date) {
			frappe.throw(__('Test date is required'));
		}
		
		// Validate test parameters
		if (frm.doc.test_parameters && frm.doc.test_parameters.length > 0) {
			for (let i = 0; i < frm.doc.test_parameters.length; i++) {
				const param = frm.doc.test_parameters[i];
				
				if (!param.parameter_name) {
					frappe.throw(__('Row {0}: Parameter name is required', [i + 1]));
				}
				
				if (param.value === null || param.value === '') {
					frappe.throw(__('Row {0}: Test value is required', [i + 1]));
				}
			}
		}
	},
	
	before_save: function(frm) {
		// Flag abnormal values
		if (frm.doc.test_parameters) {
			let has_abnormal = false;
			
			frm.doc.test_parameters.forEach(param => {
				// Check if value is within reference range
				if (param.reference_range) {
					const is_abnormal = check_reference_range(param.value, param.reference_range);
					if (is_abnormal) {
						param.is_abnormal = 1;
						has_abnormal = true;
					} else {
						param.is_abnormal = 0;
					}
				}
			});
			
			frm.set_value('has_abnormal_values', has_abnormal ? 1 : 0);
		}
	},
	
	after_save: function(frm) {
		frappe.msgprint(__('Lab test saved successfully'));
	},
	
	patient: function(frm) {
		if (frm.doc.patient) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Patient',
					filters: { name: frm.doc.patient },
					fieldname: ['patient_name', 'date_of_birth']
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('patient_name', r.message.patient_name);
					}
				}
			});
		}
	},
	
	test_date: function(frm) {
		// Validate test date is not in future
		const test_date = new Date(frm.doc.test_date);
		const today = new Date();
		
		if (test_date > today) {
			frappe.msgprint({
				title: __('Future Date'),
				message: __('Test date cannot be in the future'),
				indicator: 'orange'
			});
		}
	}
});

// Lab Test List View
frappe.listview_settings['Lab Test'] = {
	add_fields: ['patient_name', 'test_date', 'status', 'has_abnormal_values'],
	
	formatters: {
		status: function(value) {
			const colors = {
				'Pending': 'orange',
				'Completed': 'green',
				'Reviewed': 'blue',
				'Cancelled': 'red'
			};
			
			return `<span style="background-color: ${colors[value] || 'white'}; color: white; padding: 4px 8px; border-radius: 3px; font-weight: bold;">${value}</span>`;
		},
		
		test_date: function(value) {
			return frappe.datetime.str_to_user(value);
		},
		
		has_abnormal_values: function(value) {
			if (value === 1) {
				return '<span style="color: #f5222d; font-weight: bold;">⚠ Abnormal</span>';
			}
			return '<span style="color: #52c41a;">Normal</span>';
		}
	},
	
	onload: function(listview) {
		listview.page.add_action_item(__('Abnormal Results'), function() {
			listview.filter_area.add([
				['Lab Test', 'has_abnormal_values', '=', 1]
			]);
			listview.refresh();
		});
		
		listview.page.add_action_item(__('Pending'), function() {
			listview.filter_area.add([
				['Lab Test', 'status', '=', 'Pending']
			]);
			listview.refresh();
		});
	}
};

// Helper functions

function update_lab_test_indicator(frm) {
	const colors = {
		'Pending': 'orange',
		'Completed': 'blue',
		'Reviewed': 'green',
		'Cancelled': 'red'
	};
	
	const color = colors[frm.doc.status] || 'gray';
	frm.page.set_indicator(__(frm.doc.status || 'Draft'), color);
	
	// Add abnormal indicator
	if (frm.doc.has_abnormal_values) {
		frm.page.set_indicator(__('Abnormal Values'), 'red');
	}
}

function check_reference_range(value, range_str) {
	// Parse reference range like "4.5-11.0" or ">2.5"
	if (!range_str) return false;
	
	try {
		if (range_str.includes('-')) {
			const [min, max] = range_str.split('-').map(Number);
			return value < min || value > max;
		} else if (range_str.startsWith('>')) {
			const threshold = parseFloat(range_str.substring(1));
			return value <= threshold;
		} else if (range_str.startsWith('<')) {
			const threshold = parseFloat(range_str.substring(1));
			return value >= threshold;
		}
	} catch (e) {
		console.error('Error parsing reference range:', e);
	}
	
	return false;
}

function check_abnormal_values(frm) {
	if (!frm.is_new() && frm.doc.has_abnormal_values) {
		const abnormal_html = `
			<div style="padding: 15px; background: #fff1f0; border-left: 4px solid #f5222d; border-radius: 5px; margin: 15px 0;">
				<strong style="color: #f5222d;">⚠ Abnormal Values Detected</strong>
				<p style="margin: 10px 0; color: #666;">This test contains abnormal values that may require clinical attention.</p>
			</div>
		`;
		
		$(frm.wrapper).find('.abnormal-warning').remove();
		$(frm.fields_dict.patient_name.wrapper).after(abnormal_html);
	}
}

function show_test_history(frm) {
	frappe.call({
		method: 'dialysis_center.api.lab_test.get_test_history',
		args: {
			patient: frm.doc.patient,
			limit: 5
		},
		callback: function(r) {
			if (r.message && r.message.tests && r.message.tests.length > 0) {
				const tests = r.message.tests;
				const history_html = `
					<div style="margin: 15px 0; padding: 15px; background: #f9f9f9; border-radius: 5px;">
						<h6>Recent Test History</h6>
						<div style="max-height: 200px; overflow-y: auto;">
							<table class="table table-sm" style="margin: 0;">
								<thead>
									<tr>
										<th>Date</th>
										<th>Test Type</th>
										<th>Status</th>
									</tr>
								</thead>
								<tbody>
									${tests.map(t => `
										<tr onclick="frappe.set_route('Form', 'Lab Test', '${t.name}')" style="cursor: pointer;">
											<td>${frappe.datetime.str_to_user(t.test_date)}</td>
											<td>${t.test_type}</td>
											<td><span style="color: ${t.status === 'Completed' ? '#52c41a' : '#faad14'}">${t.status}</span></td>
										</tr>
									`).join('')}
								</tbody>
							</table>
						</div>
					</div>
				`;
				
				$(frm.wrapper).find('.test-history').remove();
				$(frm.wrapper).find('.patient-name').after(history_html);
			}
		}
	});
}

function show_trend_analysis(frm) {
	frappe.call({
		method: 'dialysis_center.api.lab_test.get_parameter_trend',
		args: {
			patient: frm.doc.patient,
			parameter: frm.doc.test_parameters?.[0]?.parameter_name,
			months: 6
		},
		callback: function(r) {
			if (r.message) {
				const trend = r.message;
				
				const dialog = new frappe.ui.Dialog({
					title: __('Test Value Trend'),
					size: 'large',
					fields: [
						{
							fieldtype: 'HTML',
							fieldname: 'trend_chart',
							html: `<div id="trend-chart" style="height: 400px;"></div>`
						}
					]
				});
				
				dialog.show();
				
				// Render simple trend visualization
				const html = `
					<div style="padding: 20px;">
						<h6>${frm.doc.test_parameters?.[0]?.parameter_name} Trend</h6>
						<p>Values over last 6 months</p>
						${trend.values.map((v, i) => `
							<div style="margin: 10px 0; display: flex; align-items: center;">
								<span style="width: 80px;">${v.date}</span>
								<div style="flex-grow: 1; background: #f0f0f0; height: 30px; position: relative;">
									<div style="background: #1890ff; height: 100%; width: ${v.percentage}%;"></div>
									<span style="position: absolute; right: 10px; top: 5px; font-weight: bold;">${v.value}</span>
								</div>
							</div>
						`).join('')}
					</div>
				`;
				
				$(dialog.$wrapper).find('#trend-chart').html(html);
			}
		}
	});
}

function mark_test_complete(frm) {
	frappe.call({
		method: 'dialysis_center.api.lab_test.mark_complete',
		args: {
			lab_test: frm.doc.name
		},
		callback: function(r) {
			if (r.message && r.message.success) {
				frm.set_value('status', 'Completed');
				frm.set_value('completed_date', r.message.completed_date);
				frm.save();
				frappe.msgprint(__('Lab test marked as complete'));
			}
		}
	});
}
