import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{"label": _("Session ID"), "fieldname": "name", "fieldtype": "Link", "options": "Dialysis Session", "width": 140},
		{"label": _("Patient"), "fieldname": "patient_name", "fieldtype": "Data", "width": 150},
		{"label": _("Date"), "fieldname": "session_date", "fieldtype": "Date", "width": 100},
		{"label": _("Machine"), "fieldname": "dialysis_machine", "fieldtype": "Link", "options": "Dialysis Machine", "width": 120},
		{"label": _("Duration (min)"), "fieldname": "treatment_duration", "fieldtype": "Int", "width": 100},
		{"label": _("Pre-Weight (kg)"), "fieldname": "pre_dialysis_weight", "fieldtype": "Float", "width": 110},
		{"label": _("Post-Weight (kg)"), "fieldname": "post_dialysis_weight", "fieldtype": "Float", "width": 110},
		{"label": _("Weight Loss (kg)"), "fieldname": "weight_loss", "fieldtype": "Float", "width": 110},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100}
	]

def get_data(filters):
	conditions = ""
	if filters.get("patient"):
		conditions += f" AND patient = '{filters.get('patient')}'"
	if filters.get("from_date"):
		conditions += f" AND session_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" AND session_date <= '{filters.get('to_date')}'"
	
	return frappe.db.sql(f"""
		SELECT 
			name, patient_name, session_date, dialysis_machine,
			treatment_duration, pre_dialysis_weight, post_dialysis_weight,
			weight_loss, status
		FROM `tabDialysis Session`
		WHERE docstatus < 2 {conditions}
		ORDER BY session_date DESC
	""", as_dict=1)
