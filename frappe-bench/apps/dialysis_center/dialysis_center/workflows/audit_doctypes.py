"""
Audit and Logging DocTypes Schema Definitions
Auto-creates required DocTypes for audit trails
"""
import frappe
from frappe import _


AUDIT_DOCTYPES = {
	# ============================================================================
	# WORKFLOW EVENT LOG - Tracks all workflow state transitions
	# ============================================================================
	"Workflow Event Log": {
		"autoname": "format:WEL-{YYYY}-{#####}",
		"fields": [
			{"fieldname": "document_type", "fieldtype": "Link", "label": "Document Type", "options": "DocType"},
			{"fieldname": "document_name", "fieldtype": "Data", "label": "Document Name"},
			{"fieldname": "old_state", "fieldtype": "Data", "label": "Old State"},
			{"fieldname": "new_state", "fieldtype": "Data", "label": "New State"},
			{"fieldname": "transition_action", "fieldtype": "Data", "label": "Action"},
			{"fieldname": "transition_timestamp", "fieldtype": "Datetime", "label": "Timestamp", "read_only": 1},
			{"fieldname": "transition_user", "fieldtype": "Link", "label": "User", "options": "User"},
			{"fieldname": "notes", "fieldtype": "Text", "label": "Notes"},
		]
	},
	
	# ============================================================================
	# FIELD CHANGE LOG - Tracks all field value changes
	# ============================================================================
	"Field Change Log": {
		"autoname": "format:FCL-{YYYY}-{#####}",
		"fields": [
			{"fieldname": "document_type", "fieldtype": "Link", "label": "Document Type", "options": "DocType"},
			{"fieldname": "document_name", "fieldtype": "Data", "label": "Document Name"},
			{"fieldname": "field_name", "fieldtype": "Data", "label": "Field Name"},
			{"fieldname": "old_value", "fieldtype": "Text", "label": "Old Value"},
			{"fieldname": "new_value", "fieldtype": "Text", "label": "New Value"},
			{"fieldname": "change_timestamp", "fieldtype": "Datetime", "label": "Timestamp", "read_only": 1},
			{"fieldname": "change_user", "fieldtype": "Link", "label": "User", "options": "User"},
		]
	},
	
	# ============================================================================
	# SESSION EVENT LOG - Tracks all session activities
	# ============================================================================
	"Session Event Log": {
		"autoname": "format:SEL-{YYYY}-{#####}",
		"fields": [
			{"fieldname": "session", "fieldtype": "Link", "label": "Session", "options": "Dialysis Session"},
			{"fieldname": "patient", "fieldtype": "Link", "label": "Patient", "options": "Patient"},
			{"fieldname": "event_type", "fieldtype": "Select", "label": "Event Type",
			 "options": "Session Started\nSession Completed\nSession Cancelled\nAbnormal Vital\nMachine Issue"},
			{"fieldname": "event_time", "fieldtype": "Datetime", "label": "Event Time"},
			{"fieldname": "description", "fieldtype": "Text", "label": "Description"},
			{"fieldname": "event_data", "fieldtype": "JSON", "label": "Event Data"},
		]
	},
	
	# ============================================================================
	# SESSION VITAL READING - Tracks vital signs during session
	# ============================================================================
	"Session Vital Reading": {
		"autoname": "format:SVR-{YYYY}-{#####}",
		"fields": [
			{"fieldname": "session", "fieldtype": "Link", "label": "Session", "options": "Dialysis Session"},
			{"fieldname": "patient", "fieldtype": "Link", "label": "Patient", "options": "Patient"},
			{"fieldname": "blood_pressure_systolic", "fieldtype": "Int", "label": "Systolic (mmHg)"},
			{"fieldname": "blood_pressure_diastolic", "fieldtype": "Int", "label": "Diastolic (mmHg)"},
			{"fieldname": "pulse_rate", "fieldtype": "Int", "label": "Pulse (bpm)"},
			{"fieldname": "temperature", "fieldtype": "Float", "label": "Temperature (°C)"},
			{"fieldname": "recorded_at", "fieldtype": "Datetime", "label": "Recorded At"},
			{"fieldname": "notes", "fieldtype": "Text", "label": "Notes"},
		]
	},
	
	# ============================================================================
	# BILLING AUDIT LOG - Tracks all billing transactions
	# ============================================================================
	"Billing Audit Log": {
		"autoname": "format:BAL-{YYYY}-{#####}",
		"fields": [
			{"fieldname": "document_type", "fieldtype": "Link", "label": "Document Type", "options": "DocType"},
			{"fieldname": "document_name", "fieldtype": "Data", "label": "Document Name"},
			{"fieldname": "action_type", "fieldtype": "Select", "label": "Action",
			 "options": "Created\nSubmitted\nPayment Received\nPartial Payment\nRefund Issued\nCancelled"},
			{"fieldname": "action_timestamp", "fieldtype": "Datetime", "label": "Timestamp"},
			{"fieldname": "action_user", "fieldtype": "Link", "label": "User", "options": "User"},
			{"fieldname": "amount_involved", "fieldtype": "Currency", "label": "Amount"},
			{"fieldname": "description", "fieldtype": "Text", "label": "Description"},
		]
	},
	
	# ============================================================================
	# INVOICE REMINDER LOG - Tracks payment reminders sent
	# ============================================================================
	"Invoice Reminder Log": {
		"autoname": "format:IRL-{YYYY}-{#####}",
		"fields": [
			{"fieldname": "invoice", "fieldtype": "Link", "label": "Invoice", "options": "Invoice"},
			{"fieldname": "reminder_type", "fieldtype": "Select", "label": "Reminder Type",
			 "options": "Overdue\nUpcoming Due\nPayment Confirmation"},
			{"fieldname": "sent_to", "fieldtype": "Data", "label": "Sent To"},
			{"fieldname": "sent_date", "fieldtype": "Datetime", "label": "Sent Date"},
		]
	},
	
	# ============================================================================
	# PAYMENT RECORD - Tracks all payments and refunds
	# ============================================================================
	"Payment Record": {
		"autoname": "format:PAY-{YYYY}-{#####}",
		"fields": [
			{"fieldname": "invoice", "fieldtype": "Link", "label": "Invoice", "options": "Invoice"},
			{"fieldname": "payment_date", "fieldtype": "Date", "label": "Payment Date"},
			{"fieldname": "amount", "fieldtype": "Currency", "label": "Amount"},
			{"fieldname": "payment_method", "fieldtype": "Select", "label": "Payment Method",
			 "options": "Cash\nCheck\nCredit Card\nBank Transfer\nMobile Payment\nRefund"},
			{"fieldname": "reference_number", "fieldtype": "Data", "label": "Reference Number"},
			{"fieldname": "notes", "fieldtype": "Text", "label": "Notes"},
		]
	},
}


def create_audit_doctypes():
	"""Create all audit-related DocTypes"""
	for doctype_name, fields_config in AUDIT_DOCTYPES.items():
		# Check if already exists
		if frappe.db.exists("DocType", doctype_name):
			frappe.msgprint(f"DocType already exists: {doctype_name}")
			continue
		
		# Create DocType
		doc = frappe.get_doc({
			"doctype": "DocType",
			"name": doctype_name,
			"module": "Dialysis Center",
			"custom": 0,
			"engine": "InnoDB",
			"fields": fields_config.get("fields", []),
		})
		
		# Add configuration options
		if "autoname" in fields_config:
			doc.autoname = fields_config["autoname"]
		
		doc.insert(ignore_permissions=True)
		frappe.msgprint(f"Created DocType: {doctype_name}")
	
	frappe.db.commit()
