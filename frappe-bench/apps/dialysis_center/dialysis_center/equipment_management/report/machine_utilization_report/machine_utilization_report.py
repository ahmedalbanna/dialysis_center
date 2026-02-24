import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{"label": _("Machine ID"), "fieldname": "machine_id", "fieldtype": "Link", "options": "Dialysis Machine", "width": 120},
		{"label": _("Manufacturer"), "fieldname": "manufacturer", "fieldtype": "Data", "width": 150},
		{"label": _("Model"), "fieldname": "model", "fieldtype": "Data", "width": 120},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Total Sessions"), "fieldname": "total_sessions", "fieldtype": "Int", "width": 120},
		{"label": _("Total Hours"), "fieldname": "total_hours_used", "fieldtype": "Float", "width": 110},
		{"label": _("Utilization %"), "fieldname": "utilization_rate", "fieldtype": "Float", "width": 110},
		{"label": _("Last Maintenance"), "fieldname": "last_maintenance_date", "fieldtype": "Date", "width": 130},
		{"label": _("Next Maintenance"), "fieldname": "next_maintenance_date", "fieldtype": "Date", "width": 130}
	]

def get_data(filters):
	conditions = ""
	if filters.get("status"):
		conditions += f" AND status = '{filters.get('status')}'"
	
	return frappe.db.sql(f"""
		SELECT 
			machine_id, manufacturer, model, status,
			total_sessions, total_hours_used, utilization_rate,
			last_maintenance_date, next_maintenance_date
		FROM `tabDialysis Machine`
		WHERE 1=1 {conditions}
		ORDER BY total_sessions DESC
	""", as_dict=1)
