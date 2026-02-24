"""
Workflow Definitions for Dialysis Center
Defines state machines for all clinical and operational documents
"""
import frappe
from frappe import _

# ============================================================================
# APPOINTMENT WORKFLOW: Draft → Scheduled → Check-In → In-Progress → Completed/Cancelled
# ============================================================================
APPOINTMENT_WORKFLOW = {
	"name": "Appointment Workflow",
	"document_type": "Appointment",
	"is_active": 1,
	"states": [
		{
			"state": "Draft",
			"is_initial": 1,
			"allow_self_approval": 1,
			"color": "lightgray",
			"description": "Appointment created but not yet scheduled"
		},
		{
			"state": "Scheduled",
			"allow_self_approval": 0,
			"color": "lightblue",
			"description": "Appointment confirmed and scheduled"
		},
		{
			"state": "Check-In",
			"allow_self_approval": 0,
			"color": "lightyellow",
			"description": "Patient has checked in"
		},
		{
			"state": "In-Progress",
			"allow_self_approval": 0,
			"color": "lightyellow",
			"description": "Dialysis session is in progress"
		},
		{
			"state": "Completed",
			"is_end": 1,
			"color": "lightgreen",
			"description": "Appointment completed successfully"
		},
		{
			"state": "Cancelled",
			"is_end": 1,
			"color": "lightcoral",
			"description": "Appointment was cancelled"
		}
	],
	"transitions": [
		# Draft -> Scheduled
		{
			"state": "Draft",
			"next_state": "Scheduled",
			"action": "Schedule",
			"allowed_roles": ["Dialysis Administrator", "Dialysis Receptionist"],
			"trigger_message": "Appointment scheduled",
			"update_field": "status",
			"update_value": "Scheduled"
		},
		# Scheduled -> Check-In
		{
			"state": "Scheduled",
			"next_state": "Check-In",
			"action": "Check In",
			"allowed_roles": ["Dialysis Receptionist", "Dialysis Nurse"],
			"trigger_message": "Patient checked in at {checked_in_time}",
			"update_field": "status",
			"update_value": "Checked In"
		},
		# Check-In -> In-Progress
		{
			"state": "Check-In",
			"next_state": "In-Progress",
			"action": "Start Session",
			"allowed_roles": ["Dialysis Nurse", "Dialysis Doctor"],
			"trigger_message": "Dialysis session started",
			"update_field": "status",
			"update_value": "In Progress"
		},
		# In-Progress -> Completed
		{
			"state": "In-Progress",
			"next_state": "Completed",
			"action": "Complete",
			"allowed_roles": ["Dialysis Nurse", "Dialysis Doctor"],
			"trigger_message": "Appointment completed successfully",
			"update_field": "status",
			"update_value": "Completed"
		},
		# Draft/Scheduled/Check-In -> Cancelled
		{
			"state": "Draft",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator", "Dialysis Receptionist"],
			"trigger_message": "Appointment cancelled",
			"update_field": "status",
			"update_value": "Cancelled"
		},
		{
			"state": "Scheduled",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator", "Dialysis Receptionist"],
			"trigger_message": "Appointment cancelled",
			"update_field": "status",
			"update_value": "Cancelled"
		},
		{
			"state": "Check-In",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator", "Dialysis Doctor"],
			"trigger_message": "Appointment cancelled after check-in",
			"update_field": "status",
			"update_value": "Cancelled"
		}
	]
}

# ============================================================================
# DIALYSIS SESSION WORKFLOW: Draft → In-Progress → Completed/Cancelled
# ============================================================================
DIALYSIS_SESSION_WORKFLOW = {
	"name": "Dialysis Session Workflow",
	"document_type": "Dialysis Session",
	"is_active": 1,
	"states": [
		{
			"state": "Draft",
			"is_initial": 1,
			"allow_self_approval": 0,
			"color": "lightgray",
			"description": "Session created but not started"
		},
		{
			"state": "In-Progress",
			"allow_self_approval": 0,
			"color": "lightyellow",
			"description": "Dialysis session is active"
		},
		{
			"state": "Completed",
			"is_end": 1,
			"color": "lightgreen",
			"description": "Session completed successfully"
		},
		{
			"state": "Cancelled",
			"is_end": 1,
			"color": "lightcoral",
			"description": "Session was cancelled"
		}
	],
	"transitions": [
		# Draft -> In-Progress
		{
			"state": "Draft",
			"next_state": "In-Progress",
			"action": "Start",
			"allowed_roles": ["Dialysis Nurse", "Dialysis Doctor"],
			"trigger_message": "Session started",
			"update_field": "status",
			"update_value": "In Progress"
		},
		# In-Progress -> Completed
		{
			"state": "In-Progress",
			"next_state": "Completed",
			"action": "Complete",
			"allowed_roles": ["Dialysis Nurse", "Dialysis Doctor"],
			"trigger_message": "Session completed",
			"update_field": "status",
			"update_value": "Completed"
		},
		# Draft/In-Progress -> Cancelled
		{
			"state": "Draft",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator", "Dialysis Doctor"],
			"trigger_message": "Session cancelled",
			"update_field": "status",
			"update_value": "Cancelled"
		},
		{
			"state": "In-Progress",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Doctor"],
			"trigger_message": "Session cancelled after start",
			"update_field": "status",
			"update_value": "Cancelled"
		}
	]
}

# ============================================================================
# INVOICE WORKFLOW: Draft → Submitted → Partially Paid → Paid/Cancelled
# ============================================================================
INVOICE_WORKFLOW = {
	"name": "Invoice Workflow",
	"document_type": "Invoice",
	"is_active": 1,
	"states": [
		{
			"state": "Draft",
			"is_initial": 1,
			"allow_self_approval": 0,
			"color": "lightgray",
			"description": "Invoice is being prepared"
		},
		{
			"state": "Submitted",
			"allow_self_approval": 0,
			"color": "lightblue",
			"description": "Invoice submitted and awaiting payment"
		},
		{
			"state": "Partially Paid",
			"allow_self_approval": 0,
			"color": "lightyellow",
			"description": "Partial payment received"
		},
		{
			"state": "Paid",
			"is_end": 1,
			"color": "lightgreen",
			"description": "Invoice fully paid"
		},
		{
			"state": "Cancelled",
			"is_end": 1,
			"color": "lightcoral",
			"description": "Invoice was cancelled"
		}
	],
	"transitions": [
		# Draft -> Submitted (with conditional approval)
		{
			"state": "Draft",
			"next_state": "Submitted",
			"action": "Submit",
			"allowed_roles": ["Dialysis Administrator", "Dialysis Accountant"],
			"conditions": "doc.total > 0",
			"trigger_message": "Invoice submitted for payment",
			"update_field": "status",
			"update_value": "Submitted"
		},
		# Submitted -> Partially Paid
		{
			"state": "Submitted",
			"next_state": "Partially Paid",
			"action": "Receive Partial Payment",
			"allowed_roles": ["Dialysis Accountant", "Dialysis Administrator"],
			"conditions": "doc.paid_amount > 0 AND doc.paid_amount < doc.total",
			"trigger_message": "Payment received: {paid_amount}",
			"update_field": "payment_status",
			"update_value": "Partially Paid"
		},
		# Submitted/Partially Paid -> Paid
		{
			"state": "Submitted",
			"next_state": "Paid",
			"action": "Mark as Paid",
			"allowed_roles": ["Dialysis Accountant", "Dialysis Administrator"],
			"conditions": "doc.paid_amount >= doc.total",
			"trigger_message": "Invoice fully paid",
			"update_field": "payment_status",
			"update_value": "Paid"
		},
		{
			"state": "Partially Paid",
			"next_state": "Paid",
			"action": "Mark as Paid",
			"allowed_roles": ["Dialysis Accountant", "Dialysis Administrator"],
			"conditions": "doc.paid_amount >= doc.total",
			"trigger_message": "Invoice fully paid",
			"update_field": "payment_status",
			"update_value": "Paid"
		},
		# Draft -> Cancelled
		{
			"state": "Draft",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator"],
			"trigger_message": "Invoice cancelled",
			"update_field": "status",
			"update_value": "Cancelled"
		},
		# Submitted/Partially Paid -> Cancelled (require manager approval for amounts > 5000)
		{
			"state": "Submitted",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator"],
			"conditions": "doc.total <= 5000",
			"trigger_message": "Invoice cancelled",
			"update_field": "status",
			"update_value": "Cancelled"
		},
		{
			"state": "Submitted",
			"next_state": "Cancelled",
			"action": "Cancel (Manager Approval)",
			"allowed_roles": ["Dialysis Manager"],
			"conditions": "doc.total > 5000",
			"trigger_message": "Invoice cancelled with manager approval",
			"update_field": "status",
			"update_value": "Cancelled"
		},
		{
			"state": "Partially Paid",
			"next_state": "Cancelled",
			"action": "Cancel (Manager Approval)",
			"allowed_roles": ["Dialysis Manager"],
			"conditions": "doc.total > 5000",
			"trigger_message": "Invoice cancelled with refund",
			"update_field": "status",
			"update_value": "Cancelled"
		}
	]
}

# ============================================================================
# LAB TEST WORKFLOW: Draft → Submitted → Results Received → Reviewed
# ============================================================================
LAB_TEST_WORKFLOW = {
	"name": "Lab Test Workflow",
	"document_type": "Lab Test",
	"is_active": 1,
	"states": [
		{
			"state": "Draft",
			"is_initial": 1,
			"allow_self_approval": 0,
			"color": "lightgray",
			"description": "Test order being prepared"
		},
		{
			"state": "Submitted",
			"allow_self_approval": 0,
			"color": "lightblue",
			"description": "Test order submitted to lab"
		},
		{
			"state": "Results Received",
			"allow_self_approval": 0,
			"color": "lightyellow",
			"description": "Results received from lab"
		},
		{
			"state": "Reviewed",
			"is_end": 1,
			"color": "lightgreen",
			"description": "Results reviewed by doctor"
		}
	],
	"transitions": [
		# Draft -> Submitted
		{
			"state": "Draft",
			"next_state": "Submitted",
			"action": "Submit",
			"allowed_roles": ["Dialysis Doctor", "Dialysis Administrator"],
			"trigger_message": "Lab test order submitted",
			"update_field": "status",
			"update_value": "Submitted"
		},
		# Submitted -> Results Received
		{
			"state": "Submitted",
			"next_state": "Results Received",
			"action": "Receive Results",
			"allowed_roles": ["Dialysis Administrator", "Lab Technician"],
			"trigger_message": "Lab results received",
			"update_field": "status",
			"update_value": "Results Received"
		},
		# Results Received -> Reviewed
		{
			"state": "Results Received",
			"next_state": "Reviewed",
			"action": "Review",
			"allowed_roles": ["Dialysis Doctor"],
			"trigger_message": "Lab results reviewed by doctor",
			"update_field": "status",
			"update_value": "Reviewed"
		}
	]
}

# ============================================================================
# INSURANCE CLAIM WORKFLOW: Draft → Submitted → Approved/Rejected/Pending
# ============================================================================
INSURANCE_CLAIM_WORKFLOW = {
	"name": "Insurance Claim Workflow",
	"document_type": "Insurance Claim",
	"is_active": 1,
	"states": [
		{
			"state": "Draft",
			"is_initial": 1,
			"allow_self_approval": 0,
			"color": "lightgray",
			"description": "Claim being prepared"
		},
		{
			"state": "Submitted",
			"allow_self_approval": 0,
			"color": "lightblue",
			"description": "Claim submitted to insurance provider"
		},
		{
			"state": "Pending",
			"allow_self_approval": 0,
			"color": "lightyellow",
			"description": "Claim awaiting insurance decision"
		},
		{
			"state": "Approved",
			"is_end": 1,
			"color": "lightgreen",
			"description": "Claim approved by insurance"
		},
		{
			"state": "Rejected",
			"is_end": 1,
			"color": "lightcoral",
			"description": "Claim rejected by insurance"
		},
		{
			"state": "Cancelled",
			"is_end": 1,
			"color": "lightcoral",
			"description": "Claim was cancelled"
		}
	],
	"transitions": [
		# Draft -> Submitted
		{
			"state": "Draft",
			"next_state": "Submitted",
			"action": "Submit",
			"allowed_roles": ["Dialysis Administrator", "Insurance Coordinator"],
			"conditions": "doc.patient AND doc.insurance_provider AND doc.claim_amount > 0",
			"trigger_message": "Claim submitted to insurance provider",
			"update_field": "status",
			"update_value": "Submitted"
		},
		# Submitted -> Pending
		{
			"state": "Submitted",
			"next_state": "Pending",
			"action": "Mark as Pending",
			"allowed_roles": ["Insurance Coordinator"],
			"trigger_message": "Claim pending insurance review",
			"update_field": "status",
			"update_value": "Pending"
		},
		# Pending -> Approved
		{
			"state": "Pending",
			"next_state": "Approved",
			"action": "Approve",
			"allowed_roles": ["Insurance Coordinator", "Dialysis Manager"],
			"trigger_message": "Claim approved by insurance provider",
			"update_field": "status",
			"update_value": "Approved"
		},
		# Pending -> Rejected
		{
			"state": "Pending",
			"next_state": "Rejected",
			"action": "Reject",
			"allowed_roles": ["Insurance Coordinator"],
			"trigger_message": "Claim rejected by insurance provider",
			"update_field": "status",
			"update_value": "Rejected"
		},
		# Draft -> Cancelled
		{
			"state": "Draft",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator"],
			"trigger_message": "Claim cancelled",
			"update_field": "status",
			"update_value": "Cancelled"
		},
		# Submitted/Pending -> Cancelled
		{
			"state": "Submitted",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator"],
			"trigger_message": "Claim cancelled",
			"update_field": "status",
			"update_value": "Cancelled"
		},
		{
			"state": "Pending",
			"next_state": "Cancelled",
			"action": "Cancel",
			"allowed_roles": ["Dialysis Administrator"],
			"trigger_message": "Claim cancelled",
			"update_field": "status",
			"update_value": "Cancelled"
		}
	]
}


def get_workflow_definition(doctype):
	"""Get workflow definition for a doctype"""
	workflows = {
		"Appointment": APPOINTMENT_WORKFLOW,
		"Dialysis Session": DIALYSIS_SESSION_WORKFLOW,
		"Invoice": INVOICE_WORKFLOW,
		"Lab Test": LAB_TEST_WORKFLOW,
		"Insurance Claim": INSURANCE_CLAIM_WORKFLOW
	}
	return workflows.get(doctype)


def create_all_workflows():
	"""Create all workflow definitions in Frappe"""
	workflows = [
		APPOINTMENT_WORKFLOW,
		DIALYSIS_SESSION_WORKFLOW,
		INVOICE_WORKFLOW,
		LAB_TEST_WORKFLOW,
		INSURANCE_CLAIM_WORKFLOW
	]
	
	for workflow_def in workflows:
		# Check if workflow already exists
		if not frappe.db.exists("Workflow", workflow_def["name"]):
			workflow = frappe.get_doc({
				"doctype": "Workflow",
				**workflow_def
			})
			workflow.insert(ignore_permissions=True)
			frappe.msgprint(f"Created workflow: {workflow_def['name']}")
		else:
			frappe.msgprint(f"Workflow already exists: {workflow_def['name']}")
