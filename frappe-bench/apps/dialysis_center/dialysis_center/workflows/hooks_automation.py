"""
Document Lifecycle Hooks and Automation
Handles before_insert, before_save, on_submit, on_cancel for all documents
"""
import frappe
from frappe import _
from frappe.utils import now_datetime, getdate, add_to_date, flt
from datetime import datetime, timedelta
import json


# ============================================================================
# APPOINTMENT HOOKS
# ============================================================================

def appointment_before_insert(doc, method):
	"""Set defaults when appointment is created"""
	# Set default status if not set
	if not doc.status:
		doc.status = "Draft"
	
	# Set default priority
	if not doc.priority:
		doc.priority = "Normal"
	
	# Set default appointment type
	if not doc.appointment_type:
		doc.appointment_type = "Regular"
	
	# Set default duration from patient treatment plan if available
	if doc.patient and not doc.duration:
		patient = frappe.get_cached_doc("Patient", doc.patient)
		doc.duration = patient.duration or 240  # 4 hours default


def appointment_before_save(doc, method):
	"""Normalize data before saving"""
	# Trim and normalize notes
	if doc.notes:
		doc.notes = doc.notes.strip()
	
	# Calculate appointment end time
	if doc.appointment_time and doc.duration:
		from datetime import datetime, timedelta
		time_obj = datetime.strptime(str(doc.appointment_time), "%H:%M:%S")
		end_time = time_obj + timedelta(minutes=doc.duration)
		doc.appointment_end_time = end_time.strftime("%H:%M:%S")
	
	# Auto-fetch patient name
	if doc.patient and not doc.patient_name:
		doc.patient_name = frappe.db.get_value("Patient", doc.patient, "patient_name")


def appointment_on_submit(doc, method):
	"""Create related records and send notifications on submission"""
	# Update status to Scheduled if not already done
	if doc.status == "Draft":
		frappe.db.set_value("Appointment", doc.name, "status", "Scheduled")
	
	# Log appointment submission
	log_workflow_event(doc, "on_submit", "Appointment submitted")
	
	# Send notification to patient
	send_appointment_notification(doc, "scheduled")


def appointment_on_cancel(doc, method):
	"""Reverse operations when appointment is cancelled"""
	# Cancel related session if exists
	related_session = frappe.db.exists("Dialysis Session", {
		"appointment": doc.name,
		"status": ["!=", "Completed"]
	})
	
	if related_session:
		session = frappe.get_doc("Dialysis Session", related_session)
		if session.docstatus == 0:
			session.cancel()
		else:
			# If already submitted, just update status
			frappe.db.set_value("Dialysis Session", session.name, "status", "Cancelled")
	
	# Log cancellation
	log_workflow_event(doc, "on_cancel", f"Appointment cancelled. Reason: {doc.cancellation_reason or 'Not specified'}")
	
	# Send notification
	send_appointment_notification(doc, "cancelled")


# ============================================================================
# DIALYSIS SESSION HOOKS
# ============================================================================

def dialysis_session_before_insert(doc, method):
	"""Set defaults when session is created"""
	if not doc.status:
		doc.status = "Draft"
	
	# Auto-fetch patient name
	if doc.patient and not doc.patient_name:
		doc.patient_name = frappe.db.get_value("Patient", doc.patient, "patient_name")
	
	# Set session start time to now if not provided
	if not doc.session_start_time:
		doc.session_start_time = now_datetime()


def dialysis_session_before_save(doc, method):
	"""Normalize data before saving"""
	# Trim notes
	if doc.notes:
		doc.notes = doc.notes.strip()
	
	# Calculate session duration if start and end times exist
	if doc.session_start_time and doc.session_end_time:
		start = frappe.utils.get_datetime(doc.session_start_time)
		end = frappe.utils.get_datetime(doc.session_end_time)
		duration_minutes = int((end - start).total_seconds() / 60)
		doc.actual_duration = duration_minutes


def dialysis_session_on_submit(doc, method):
	"""Create related records on session submission"""
	# Log session start
	log_workflow_event(doc, "on_submit", "Dialysis session started")
	
	# Create session event log entries if not already created
	if not frappe.db.exists("Session Event Log", {
		"session": doc.name,
		"event_type": "Session Started"
	}):
		frappe.get_doc({
			"doctype": "Session Event Log",
			"session": doc.name,
			"patient": doc.patient,
			"event_type": "Session Started",
			"event_time": now_datetime(),
			"description": "Dialysis session started"
		}).insert(ignore_permissions=True)
	
	# Update related appointment
	if doc.appointment:
		frappe.db.set_value("Appointment", doc.appointment, "status", "In Progress")


def dialysis_session_on_cancel(doc, method):
	"""Reverse operations when session is cancelled"""
	# Log cancellation with reason
	reason = doc.cancellation_reason or "Not specified"
	log_workflow_event(doc, "on_cancel", f"Session cancelled. Reason: {reason}")
	
	# Create cancellation event log
	frappe.get_doc({
		"doctype": "Session Event Log",
		"session": doc.name,
		"patient": doc.patient,
		"event_type": "Session Cancelled",
		"event_time": now_datetime(),
		"description": f"Session cancelled: {reason}"
	}).insert(ignore_permissions=True)
	
	# Reverse any session-related charges
	reverse_session_charges(doc)


# ============================================================================
# INVOICE HOOKS
# ============================================================================

def invoice_before_insert(doc, method):
	"""Set defaults when invoice is created"""
	if not doc.status:
		doc.status = "Draft"
	
	if not doc.payment_status:
		doc.payment_status = "Unpaid"
	
	# Set invoice date to today
	if not doc.invoice_date:
		doc.invoice_date = getdate()
	
	# Set due date (30 days from invoice date)
	if not doc.due_date:
		doc.due_date = add_to_date(doc.invoice_date, days=30)


def invoice_before_save(doc, method):
	"""Normalize data and calculate totals"""
	# Trim notes
	if doc.notes:
		doc.notes = doc.notes.strip()
	
	# Calculate total if items exist
	if doc.items:
		doc.total = sum(item.amount for item in doc.items) if hasattr(doc, 'items') else 0
		doc.paid_amount = flt(doc.paid_amount or 0)
		doc.pending_amount = doc.total - doc.paid_amount
		
		# Update payment status
		if doc.paid_amount == 0:
			doc.payment_status = "Unpaid"
		elif doc.paid_amount >= doc.total:
			doc.payment_status = "Paid"
		else:
			doc.payment_status = "Partially Paid"


def invoice_on_submit(doc, method):
	"""Create related records and send notifications on submission"""
	# Log submission
	log_workflow_event(doc, "on_submit", f"Invoice submitted. Amount: {doc.total}")
	
	# Send invoice notification
	send_invoice_notification(doc, "submitted")
	
	# Update session billing status if linked
	if doc.session:
		frappe.db.set_value("Dialysis Session", doc.session, "billing_status", "Invoiced")


def invoice_on_cancel(doc, method):
	"""Reverse operations when invoice is cancelled"""
	# Refund payments
	if doc.paid_amount and doc.paid_amount > 0:
		refund_amount = doc.paid_amount
		log_workflow_event(doc, "on_cancel", f"Invoice cancelled. Refund amount: {refund_amount}")
		
		# Create refund record
		frappe.get_doc({
			"doctype": "Payment Record",
			"invoice": doc.name,
			"payment_date": getdate(),
			"amount": -refund_amount,  # Negative for refund
			"payment_method": "Refund",
			"notes": f"Refund for cancelled invoice {doc.name}"
		}).insert(ignore_permissions=True)
	
	# Reverse any related accounting entries
	reverse_invoice_charges(doc)
	
	# Update session billing status
	if doc.session:
		frappe.db.set_value("Dialysis Session", doc.session, "billing_status", "Not Invoiced")


# ============================================================================
# LAB TEST HOOKS
# ============================================================================

def lab_test_before_insert(doc, method):
	"""Set defaults when lab test is created"""
	if not doc.status:
		doc.status = "Draft"
	
	# Set test date to today
	if not doc.test_date:
		doc.test_date = getdate()
	
	# Auto-fetch patient name
	if doc.patient and not doc.patient_name:
		doc.patient_name = frappe.db.get_value("Patient", doc.patient, "patient_name")


def lab_test_before_save(doc, method):
	"""Normalize data before saving"""
	if doc.notes:
		doc.notes = doc.notes.strip()


def lab_test_on_submit(doc, method):
	"""Create related records on submission"""
	log_workflow_event(doc, "on_submit", "Lab test submitted")
	
	# Create lab result record
	frappe.get_doc({
		"doctype": "Lab Result",
		"lab_test": doc.name,
		"patient": doc.patient,
		"test_date": doc.test_date,
		"status": "Pending"
	}).insert(ignore_permissions=True)
	
	# Send notification
	send_lab_notification(doc, "submitted")


# ============================================================================
# INSURANCE CLAIM HOOKS
# ============================================================================

def insurance_claim_before_insert(doc, method):
	"""Set defaults when claim is created"""
	if not doc.status:
		doc.status = "Draft"
	
	# Set submission date
	if not doc.submission_date:
		doc.submission_date = getdate()


def insurance_claim_before_save(doc, method):
	"""Normalize data before saving"""
	if doc.notes:
		doc.notes = doc.notes.strip()


def insurance_claim_on_submit(doc, method):
	"""Create related records on submission"""
	log_workflow_event(doc, "on_submit", f"Insurance claim submitted. Amount: {doc.claim_amount}")
	
	# Send notification to insurance provider
	send_insurance_notification(doc, "submitted")


def insurance_claim_on_cancel(doc, method):
	"""Reverse operations when claim is cancelled"""
	log_workflow_event(doc, "on_cancel", f"Insurance claim cancelled")
	
	# Update related invoice if exists
	if doc.invoice:
		frappe.db.set_value("Invoice", doc.invoice, "insurance_claim", None)


# ============================================================================
# HELPER FUNCTIONS FOR HOOKS
# ============================================================================

def log_workflow_event(doc, event_type, description):
	"""Log workflow event for audit trail"""
	frappe.get_doc({
		"doctype": "Workflow Event Log",
		"document_type": doc.doctype,
		"document_name": doc.name,
		"event_type": event_type,
		"event_time": now_datetime(),
		"user": frappe.session.user,
		"description": description
	}).insert(ignore_permissions=True)


def send_appointment_notification(doc, action):
	"""Send appointment notification to patient and staff"""
	patient_email = frappe.db.get_value("Patient", doc.patient, "email")
	
	if not patient_email:
		return
	
	messages = {
		"scheduled": {
			"subject": f"Appointment Confirmed - {doc.appointment_date}",
			"template": "appointment_scheduled"
		},
		"cancelled": {
			"subject": "Appointment Cancelled",
			"template": "appointment_cancelled"
		}
	}
	
	if action in messages:
		msg_config = messages[action]
		send_notification_email(
			recipients=[patient_email],
			subject=msg_config["subject"],
			template=msg_config["template"],
			doc=doc
		)


def send_session_notification(doc, action):
	"""Send session notification"""
	patient_email = frappe.db.get_value("Patient", doc.patient, "email")
	
	if not patient_email:
		return
	
	messages = {
		"started": {
			"subject": "Dialysis Session Started",
			"template": "session_started"
		},
		"completed": {
			"subject": "Dialysis Session Completed",
			"template": "session_completed"
		}
	}
	
	if action in messages:
		msg_config = messages[action]
		send_notification_email(
			recipients=[patient_email],
			subject=msg_config["subject"],
			template=msg_config["template"],
			doc=doc
		)


def send_invoice_notification(doc, action):
	"""Send invoice notification"""
	patient_email = frappe.db.get_value("Patient", doc.patient, "email")
	
	if not patient_email:
		return
	
	messages = {
		"submitted": {
			"subject": f"Invoice {doc.name} - Amount Due: {doc.total}",
			"template": "invoice_submitted"
		},
		"paid": {
			"subject": f"Invoice {doc.name} - Payment Received",
			"template": "invoice_paid"
		}
	}
	
	if action in messages:
		msg_config = messages[action]
		send_notification_email(
			recipients=[patient_email],
			subject=msg_config["subject"],
			template=msg_config["template"],
			doc=doc
		)


def send_lab_notification(doc, action):
	"""Send lab test notification"""
	doctor_email = frappe.db.get_value("User", doc.ordered_by, "email") if doc.ordered_by else None
	
	if doctor_email:
		send_notification_email(
			recipients=[doctor_email],
			subject=f"Lab Test Submitted - {doc.patient}",
			template="lab_test_submitted",
			doc=doc
		)


def send_insurance_notification(doc, action):
	"""Send insurance claim notification"""
	coordinator_emails = frappe.db.sql_list(
		"SELECT email FROM `tabUser` WHERE name IN (SELECT user FROM `tabUserRole` WHERE role='Insurance Coordinator')"
	)
	
	if coordinator_emails:
		send_notification_email(
			recipients=coordinator_emails,
			subject=f"Insurance Claim {doc.name} Submitted",
			template="insurance_claim_submitted",
			doc=doc
		)


def send_notification_email(recipients, subject, template, doc):
	"""Generic email notification sender"""
	try:
		# This is a placeholder - implement actual email sending based on your email templates
		frappe.sendmail(
			recipients=recipients,
			subject=subject,
			message=f"Document: {doc.doctype} - {doc.name}"
		)
	except Exception as e:
		frappe.log_error(f"Failed to send notification email: {str(e)}")


def reverse_session_charges(doc):
	"""Reverse any charges created for a cancelled session"""
	# Find and reverse any billing entries
	charges = frappe.get_all("Session Charge", {
		"session": doc.name,
		"reversed": 0
	})
	
	for charge in charges:
		frappe.db.set_value("Session Charge", charge.name, "reversed", 1)


def reverse_invoice_charges(doc):
	"""Reverse any charges for a cancelled invoice"""
	frappe.db.set_value("Invoice", doc.name, "status", "Cancelled")
