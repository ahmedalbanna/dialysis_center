import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data, filters)
	return columns, data, None, chart

def get_columns():
	return [
		{"label": _("Patient"), "fieldname": "patient", "fieldtype": "Link", "options": "Patient", "width": 120},
		{"label": _("Patient Name"), "fieldname": "patient_name", "fieldtype": "Data", "width": 150},
		{"label": _("Test Date"), "fieldname": "test_date", "fieldtype": "Date", "width": 100},
		{"label": _("Test Parameter"), "fieldname": "test_parameter", "fieldtype": "Data", "width": 150},
		{"label": _("Result Value"), "fieldname": "result_value", "fieldtype": "Float", "width": 100},
		{"label": _("Unit"), "fieldname": "unit", "fieldtype": "Data", "width": 80},
		{"label": _("Normal Range"), "fieldname": "normal_range", "fieldtype": "Data", "width": 120},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100}
	]

def get_data(filters):
	conditions = ""
	if filters.get("patient"):
		conditions += f" AND lr.patient = '{filters.get('patient')}'"
	if filters.get("test_parameter"):
		conditions += f" AND lr.test_parameter = '{filters.get('test_parameter')}'"
	if filters.get("from_date"):
		conditions += f" AND lr.test_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" AND lr.test_date <= '{filters.get('to_date')}'"
	
	data = frappe.db.sql(f"""
		SELECT 
			lr.patient,
			p.patient_name,
			lr.test_date,
			lr.test_parameter,
			lr.result_value,
			lr.unit,
			CONCAT(lr.normal_range_min, ' - ', lr.normal_range_max) as normal_range,
			CASE 
				WHEN lr.is_abnormal = 1 THEN 'Abnormal'
				ELSE 'Normal'
			END as status
		FROM `tabLab Result` lr
		LEFT JOIN `tabPatient` p ON lr.patient = p.name
		WHERE 1=1 {conditions}
		ORDER BY lr.patient, lr.test_parameter, lr.test_date
	""", as_dict=1)
	
	return data

def get_chart_data(data, filters):
	"""Generate trending chart for selected parameter"""
	if not data or not filters.get("test_parameter"):
		return None
	
	# Filter data for chart
	chart_data = [d for d in data if d.test_parameter == filters.get("test_parameter")]
	
	if not chart_data:
		return None
	
	# Sort by date
	chart_data = sorted(chart_data, key=lambda x: x.test_date)
	
	labels = [str(d.test_date) for d in chart_data]
	values = [d.result_value for d in chart_data]
	
	# Get normal range for reference lines
	normal_min = chart_data[0].get("normal_range", "").split(" - ")[0] if chart_data else None
	normal_max = chart_data[0].get("normal_range", "").split(" - ")[-1] if chart_data else None
	
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Result Value", "values": values}
			]
		},
		"type": "line",
		"lineOptions": {
			"regionFill": 1
		}
	}
