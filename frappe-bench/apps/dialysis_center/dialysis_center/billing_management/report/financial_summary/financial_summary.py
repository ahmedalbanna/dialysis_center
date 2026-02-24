import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	return columns, data, None, chart

def get_columns():
	return [
		{"label": _("Invoice"), "fieldname": "name", "fieldtype": "Link", "options": "Invoice", "width": 140},
		{"label": _("Patient"), "fieldname": "patient_name", "fieldtype": "Data", "width": 150},
		{"label": _("Date"), "fieldname": "invoice_date", "fieldtype": "Date", "width": 100},
		{"label": _("Total Amount"), "fieldname": "total_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Paid Amount"), "fieldname": "paid_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Outstanding"), "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Payment Status"), "fieldname": "payment_status", "fieldtype": "Data", "width": 120}
	]

def get_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += f" AND invoice_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" AND invoice_date <= '{filters.get('to_date')}'"
	if filters.get("payment_status"):
		conditions += f" AND payment_status = '{filters.get('payment_status')}'"
	
	return frappe.db.sql(f"""
		SELECT 
			name, patient_name, invoice_date, total_amount,
			paid_amount, outstanding_amount, payment_status
		FROM `tabInvoice`
		WHERE docstatus < 2 {conditions}
		ORDER BY invoice_date DESC
	""", as_dict=1)

def get_chart_data(data):
	if not data:
		return None
	
	paid = sum([d.paid_amount or 0 for d in data])
	outstanding = sum([d.outstanding_amount or 0 for d in data])
	
	return {
		"data": {
			"labels": ["Paid", "Outstanding"],
			"datasets": [{"values": [paid, outstanding]}]
		},
		"type": "donut"
	}
