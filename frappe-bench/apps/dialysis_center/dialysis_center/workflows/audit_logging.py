"""
Workflow and Audit Logging Module
Maintains comprehensive audit trails for compliance and tracking
"""
import frappe
from frappe import _
from frappe.utils import now_datetime, getdate
import json


class WorkflowAuditLogger:
	"""Handles workflow event logging and audit trails"""
	
	@staticmethod
	def log_workflow_transition(doc, old_state, new_state, action, user=None):
		"""Log state transition"""
		if user is None:
			user = frappe.session.user
		
		frappe.get_doc({
			"doctype": "Workflow Event Log",
			"document_type": doc.doctype,
			"document_name": doc.name,
			"old_state": old_state,
			"new_state": new_state,
			"transition_action": action,
			"transition_timestamp": now_datetime(),
			"transition_user": user,
			"notes": f"Transitioned from {old_state} to {new_state} via action: {action}"
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_field_change(doc, field_name, old_value, new_value, user=None):
		"""Log field value changes"""
		if user is None:
			user = frappe.session.user
		
		# Convert complex types to JSON for storage
		if isinstance(old_value, (dict, list)):
			old_value = json.dumps(old_value)
		if isinstance(new_value, (dict, list)):
			new_value = json.dumps(new_value)
		
		frappe.get_doc({
			"doctype": "Field Change Log",
			"document_type": doc.doctype,
			"document_name": doc.name,
			"field_name": field_name,
			"old_value": str(old_value)[:500],
			"new_value": str(new_value)[:500],
			"change_timestamp": now_datetime(),
			"change_user": user
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_approval_action(doc, approver, action, comments=None):
		"""Log approval/rejection actions"""
		frappe.get_doc({
			"doctype": "Approval Log",
			"document_type": doc.doctype,
			"document_name": doc.name,
			"approver": approver,
			"action": action,  # Approved, Rejected, Requested Changes
			"approval_timestamp": now_datetime(),
			"approval_comments": comments
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_document_access(doc_type, doc_name, action, user=None):
		"""Log document access (view, edit, delete)"""
		if user is None:
			user = frappe.session.user
		
		frappe.get_doc({
			"doctype": "Document Access Log",
			"document_type": doc_type,
			"document_name": doc_name,
			"access_action": action,
			"access_timestamp": now_datetime(),
			"access_user": user,
			"user_ip": frappe.request.remote_addr if frappe.request else None
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_document_export(doc_type, doc_name, export_format):
		"""Log document exports (PDF, Excel, etc.)"""
		frappe.get_doc({
			"doctype": "Document Export Log",
			"document_type": doc_type,
			"document_name": doc_name,
			"export_format": export_format,
			"export_timestamp": now_datetime(),
			"export_user": frappe.session.user
		}).insert(ignore_permissions=True)


class SessionEventLogger:
	"""Handles session-specific event logging"""
	
	@staticmethod
	def log_session_event(session_name, event_type, patient, description, event_data=None):
		"""Log session events (vital reading, medication admin, etc.)"""
		frappe.get_doc({
			"doctype": "Session Event Log",
			"session": session_name,
			"patient": patient,
			"event_type": event_type,
			"event_time": now_datetime(),
			"description": description,
			"event_data": json.dumps(event_data) if event_data else None
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_vital_reading(session_name, patient, systolic, diastolic, pulse, temperature, notes=None):
		"""Log vital signs with status"""
		reading = frappe.get_doc({
			"doctype": "Session Vital Reading",
			"session": session_name,
			"patient": patient,
			"blood_pressure_systolic": systolic,
			"blood_pressure_diastolic": diastolic,
			"pulse_rate": pulse,
			"temperature": temperature,
			"recorded_at": now_datetime(),
			"notes": notes
		})
		reading.insert(ignore_permissions=True)
		
		# Check for abnormal values and log alert
		abnormal_flags = []
		if systolic > 180 or systolic < 90:
			abnormal_flags.append(f"Systolic BP {systolic} (abnormal)")
		if diastolic > 110 or diastolic < 60:
			abnormal_flags.append(f"Diastolic BP {diastolic} (abnormal)")
		if pulse > 120 or pulse < 50:
			abnormal_flags.append(f"Pulse {pulse} (abnormal)")
		if temperature > 38.5 or temperature < 36:
			abnormal_flags.append(f"Temperature {temperature}°C (abnormal)")
		
		if abnormal_flags:
			SessionEventLogger.log_session_event(
				session_name, "Abnormal Vital", patient,
				f"Abnormal vitals detected: {', '.join(abnormal_flags)}",
				{"systolic": systolic, "diastolic": diastolic, "pulse": pulse, "temperature": temperature}
			)
		
		return reading
	
	@staticmethod
	def log_medication_administration(session_name, patient, medication, dose, route, administered_by, notes=None):
		"""Log medication administration"""
		frappe.get_doc({
			"doctype": "Medication Administration Log",
			"session": session_name,
			"patient": patient,
			"medication": medication,
			"dose": dose,
			"route": route,
			"administered_by": administered_by,
			"administration_time": now_datetime(),
			"notes": notes
		}).insert(ignore_permissions=True)
		
		SessionEventLogger.log_session_event(
			session_name, "Medication Administered", patient,
			f"Administered {dose} of {medication} via {route}",
			{"medication": medication, "dose": dose, "route": route, "administered_by": administered_by}
		)
	
	@staticmethod
	def log_machine_issue(session_name, patient, machine, issue_type, description, resolved=False):
		"""Log equipment issues during session"""
		frappe.get_doc({
			"doctype": "Machine Issue Log",
			"session": session_name,
			"patient": patient,
			"machine": machine,
			"issue_type": issue_type,
			"description": description,
			"issue_timestamp": now_datetime(),
			"resolved": resolved
		}).insert(ignore_permissions=True)
		
		SessionEventLogger.log_session_event(
			session_name, "Machine Issue", patient,
			f"{issue_type}: {description}",
			{"machine": machine, "issue_type": issue_type, "resolved": resolved}
		)


class BillingAuditLogger:
	"""Handles billing-related audit logging"""
	
	@staticmethod
	def log_invoice_creation(invoice_doc, source_doc_type=None, source_doc_name=None):
		"""Log invoice creation"""
		frappe.get_doc({
			"doctype": "Billing Audit Log",
			"document_type": "Invoice",
			"document_name": invoice_doc.name,
			"action_type": "Created",
			"action_timestamp": now_datetime(),
			"action_user": frappe.session.user,
			"amount_involved": invoice_doc.total,
			"source_document": f"{source_doc_type}:{source_doc_name}" if source_doc_type else None,
			"description": f"Invoice created for {invoice_doc.patient}: {invoice_doc.total}"
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_payment_received(invoice_name, amount, payment_method, reference, notes=None):
		"""Log payment reception"""
		frappe.get_doc({
			"doctype": "Billing Audit Log",
			"document_type": "Invoice",
			"document_name": invoice_name,
			"action_type": "Payment Received",
			"action_timestamp": now_datetime(),
			"action_user": frappe.session.user,
			"amount_involved": amount,
			"payment_reference": reference,
			"description": f"Payment of {amount} received via {payment_method}. Ref: {reference}"
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_refund_issued(invoice_name, amount, reason):
		"""Log refund issued"""
		frappe.get_doc({
			"doctype": "Billing Audit Log",
			"document_type": "Invoice",
			"document_name": invoice_name,
			"action_type": "Refund Issued",
			"action_timestamp": now_datetime(),
			"action_user": frappe.session.user,
			"amount_involved": -amount,
			"description": f"Refund of {amount} issued. Reason: {reason}"
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_invoice_cancellation(invoice_name, reason, refund_amount=0):
		"""Log invoice cancellation"""
		frappe.get_doc({
			"doctype": "Billing Audit Log",
			"document_type": "Invoice",
			"document_name": invoice_name,
			"action_type": "Cancelled",
			"action_timestamp": now_datetime(),
			"action_user": frappe.session.user,
			"amount_involved": -refund_amount,
			"description": f"Invoice cancelled. Reason: {reason}. Refund: {refund_amount}"
		}).insert(ignore_permissions=True)


class ComplianceAuditLogger:
	"""Handles compliance and policy adherence logging"""
	
	@staticmethod
	def log_policy_violation(violation_type, document_type, document_name, description, severity="Medium"):
		"""Log policy violation"""
		frappe.get_doc({
			"doctype": "Policy Violation Log",
			"violation_type": violation_type,
			"document_type": document_type,
			"document_name": document_name,
			"violation_description": description,
			"violation_timestamp": now_datetime(),
			"violation_user": frappe.session.user,
			"severity": severity
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_data_access_violation(user, resource, access_type, granted_access):
		"""Log unauthorized access attempts"""
		if not granted_access:
			frappe.get_doc({
				"doctype": "Access Violation Log",
				"user": user,
				"resource_type": resource,
				"access_type": access_type,
				"access_timestamp": now_datetime(),
				"granted": False,
				"user_ip": frappe.request.remote_addr if frappe.request else None
			}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_sensitive_data_access(document_type, document_name, sensitive_fields, user=None):
		"""Log access to sensitive patient data"""
		if user is None:
			user = frappe.session.user
		
		frappe.get_doc({
			"doctype": "Sensitive Data Access Log",
			"document_type": document_type,
			"document_name": document_name,
			"sensitive_fields": ", ".join(sensitive_fields),
			"access_timestamp": now_datetime(),
			"access_user": user,
			"purpose": "Clinical Review"
		}).insert(ignore_permissions=True)


class ReportingAuditLogger:
	"""Handles reporting-related audit logging"""
	
	@staticmethod
	def log_report_generation(report_name, filters, user=None):
		"""Log report generation"""
		if user is None:
			user = frappe.session.user
		
		frappe.get_doc({
			"doctype": "Report Generation Log",
			"report_name": report_name,
			"filters_applied": json.dumps(filters) if filters else None,
			"generation_timestamp": now_datetime(),
			"generated_by": user
		}).insert(ignore_permissions=True)
	
	@staticmethod
	def log_report_export(report_name, export_format, user=None):
		"""Log report export"""
		if user is None:
			user = frappe.session.user
		
		frappe.get_doc({
			"doctype": "Report Export Log",
			"report_name": report_name,
			"export_format": export_format,
			"export_timestamp": now_datetime(),
			"exported_by": user
		}).insert(ignore_permissions=True)


# ============================================================================
# AUDIT TRAIL RETRIEVAL FUNCTIONS
# ============================================================================

def get_document_audit_trail(doc_type, doc_name):
	"""Get complete audit trail for a document"""
	
	audit_trail = {
		"document": f"{doc_type}:{doc_name}",
		"workflow_events": [],
		"field_changes": [],
		"access_logs": [],
		"approval_logs": []
	}
	
	# Get workflow events
	workflow_events = frappe.get_all(
		"Workflow Event Log",
		filters={
			"document_type": doc_type,
			"document_name": doc_name
		},
		order_by="transition_timestamp asc",
		fields=["*"]
	)
	audit_trail["workflow_events"] = workflow_events
	
	# Get field changes
	field_changes = frappe.get_all(
		"Field Change Log",
		filters={
			"document_type": doc_type,
			"document_name": doc_name
		},
		order_by="change_timestamp asc",
		fields=["*"]
	)
	audit_trail["field_changes"] = field_changes
	
	# Get access logs
	access_logs = frappe.get_all(
		"Document Access Log",
		filters={
			"document_type": doc_type,
			"document_name": doc_name
		},
		order_by="access_timestamp desc",
		limit_page_length=50,
		fields=["*"]
	)
	audit_trail["access_logs"] = access_logs
	
	# Get approval logs
	approval_logs = frappe.get_all(
		"Approval Log",
		filters={
			"document_type": doc_type,
			"document_name": doc_name
		},
		order_by="approval_timestamp asc",
		fields=["*"]
	)
	audit_trail["approval_logs"] = approval_logs
	
	return audit_trail


def get_session_audit_trail(session_name):
	"""Get complete audit trail for a dialysis session"""
	
	audit_trail = {
		"session": session_name,
		"events": [],
		"vital_readings": [],
		"medications": [],
		"machine_issues": []
	}
	
	# Get session events
	events = frappe.get_all(
		"Session Event Log",
		filters={"session": session_name},
		order_by="event_time asc",
		fields=["*"]
	)
	audit_trail["events"] = events
	
	# Get vital readings
	vital_readings = frappe.get_all(
		"Session Vital Reading",
		filters={"session": session_name},
		order_by="recorded_at asc",
		fields=["*"]
	)
	audit_trail["vital_readings"] = vital_readings
	
	# Get medications
	medications = frappe.get_all(
		"Medication Administration Log",
		filters={"session": session_name},
		order_by="administration_time asc",
		fields=["*"]
	)
	audit_trail["medications"] = medications
	
	# Get machine issues
	machine_issues = frappe.get_all(
		"Machine Issue Log",
		filters={"session": session_name},
		order_by="issue_timestamp asc",
		fields=["*"]
	)
	audit_trail["machine_issues"] = machine_issues
	
	return audit_trail


def get_billing_audit_trail(invoice_name):
	"""Get complete billing audit trail for an invoice"""
	
	billing_logs = frappe.get_all(
		"Billing Audit Log",
		filters={"document_name": invoice_name},
		order_by="action_timestamp asc",
		fields=["*"]
	)
	
	return {
		"invoice": invoice_name,
		"billing_history": billing_logs
	}
