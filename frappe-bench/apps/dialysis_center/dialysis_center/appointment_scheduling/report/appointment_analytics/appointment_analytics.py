import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	summary = get_summary(data)
	chart = get_chart_data(data)
	return columns, data, None, chart, summary

def get_columns():
	return [
		{"label": _("Appointment"), "fieldname": "name", "fieldtype": "Link", "options": "Appointment", "width": 140},
		{"label": _("Patient"), "fieldname": "patient_name", "fieldtype": "Data", "width": 150},
		{"label": _("Date"), "fieldname": "appointment_date", "fieldtype": "Date", "width": 100},
		{"label": _("Time"), "fieldname": "appointment_time", "fieldtype": "Time", "width": 80},
		{"label": _("Machine"), "fieldname": "machine", "fieldtype": "Link", "options": "Dialysis Machine", "width": 120},
		{"label": _("Duration (min)"), "fieldname": "duration", "fieldtype": "Int", "width": 100},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Checked In"), "fieldname": "checked_in_time", "fieldtype": "Datetime", "width": 140}
	]

def get_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += f" AND appointment_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" AND appointment_date <= '{filters.get('to_date')}'"
	if filters.get("status"):
		conditions += f" AND status = '{filters.get('status')}'"
	if filters.get("machine"):
		conditions += f" AND machine = '{filters.get('machine')}'"
	
	return frappe.db.sql(f"""
		SELECT 
			name, patient_name, appointment_date, appointment_time,
			machine, duration, status, checked_in_time
		FROM `tabAppointment`
		WHERE docstatus < 2 {conditions}
		ORDER BY appointment_date DESC, appointment_time DESC
	""", as_dict=1)

def get_summary(data):
	"""Calculate summary statistics"""
	if not data:
		return []
	
	total = len(data)
	completed = len([d for d in data if d.status == "Completed"])
	cancelled = len([d for d in data if d.status == "Cancelled"])
	scheduled = len([d for d in data if d.status == "Scheduled"])
	
	# Calculate show rate (completed / total scheduled)
	show_rate = (completed / total * 100) if total > 0 else 0
	
	return [
		{
			"value": total,
			"label": "Total Appointments",
			"indicator": "Blue",
			"datatype": "Int"
		},
		{
			"value": completed,
			"label": "Completed",
			"indicator": "Green",
			"datatype": "Int"
		},
		{
			"value": cancelled,
			"label": "Cancelled",
			"indicator": "Red",
			"datatype": "Int"
		},
		{
			"value": f"{show_rate:.1f}%",
			"label": "Show Rate",
			"indicator": "Green" if show_rate > 80 else "Orange",
			"datatype": "Data"
		}
	]

def get_chart_data(data):
	"""Generate status distribution chart"""
	if not data:
		return None
	
	status_counts = {}
	for d in data:
		status = d.status or "Unknown"
		status_counts[status] = status_counts.get(status, 0) + 1
	
	return {
		"data": {
			"labels": list(status_counts.keys()),
			"datasets": [{"values": list(status_counts.values())}]
		},
		"type": "pie"
	}
