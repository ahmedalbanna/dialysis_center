import frappe
from frappe import _
from frappe.utils import nowdate, flt
import json

# Helper function for standardized API responses
def api_response(status="success", data=None, message=""):
	"""Standardized API response format"""
	return {
		"status": status,
		"data": data,
		"message": message
	}

# ==================== INSURANCE PROVIDERS & CLAIMS ====================

@frappe.whitelist()
def get_insurance_provider_list(start=0, page_length=20):
	"""
	Get list of insurance providers
	
	Args:
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: providers, message}
	"""
	try:
		start = int(start)
		page_length = min(int(page_length), 100)
		
		providers = frappe.get_all("Insurance Provider",
			fields=["name", "provider_name", "phone_number", "email", "website", "address"],
			order_by="provider_name asc",
			start=start,
			page_length=page_length
		)
		
		frappe.get_logger().info(f"API: get_insurance_provider_list - {len(providers)} providers retrieved")
		
		return api_response(data={
			"providers": providers,
			"count": len(providers),
			"total": frappe.db.count("Insurance Provider")
		})
	except Exception as e:
		frappe.log_error(f"get_insurance_provider_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def create_insurance_claim(patient_id, invoice_id, claim_date=None, claim_amount=None):
	"""
	Create insurance claim for invoice
	
	Args:
		patient_id (str): Patient ID
		invoice_id (str): Invoice ID
		claim_date (str): Claim date (YYYY-MM-DD)
		claim_amount (float): Claim amount (if different from invoice total)
	
	Returns:
		dict: {status, data: claim, message}
	"""
	try:
		if not all([patient_id, invoice_id]):
			return api_response(status="error", message="patient_id and invoice_id are required")
		
		# Validate patient
		if not frappe.db.exists("Patient", patient_id):
			return api_response(status="error", message="Patient not found")
		
		# Validate invoice
		if not frappe.db.exists("Invoice", invoice_id):
			return api_response(status="error", message="Invoice not found")
		
		invoice = frappe.get_doc("Invoice", invoice_id)
		patient = frappe.get_value("Patient", patient_id, ["patient_name"])
		
		# Check if claim already exists for this invoice
		existing = frappe.db.exists("Insurance Claim", {"invoice": invoice_id})
		if existing:
			return api_response(status="error", message=f"Claim already exists for this invoice: {existing}")
		
		claim = frappe.get_doc({
			"doctype": "Insurance Claim",
			"patient": patient_id,
			"patient_name": patient[0],
			"invoice": invoice_id,
			"claim_date": claim_date or nowdate(),
			"claim_amount": claim_amount or invoice.total_amount,
			"status": "Submitted"
		})
		
		claim.insert(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: create_insurance_claim - {claim.name} created")
		
		return api_response(data=claim.as_dict(), message="Insurance claim created successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"create_insurance_claim error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_claim_status(claim_id):
	"""
	Get insurance claim status and details
	
	Args:
		claim_id (str): Claim ID
	
	Returns:
		dict: {status, data: claim_details, message}
	"""
	try:
		if not claim_id:
			return api_response(status="error", message="Claim ID is required")
		
		if not frappe.db.exists("Insurance Claim", claim_id):
			return api_response(status="error", message="Claim not found")
		
		claim = frappe.get_doc("Insurance Claim", claim_id)
		
		# Get related invoice
		invoice = frappe.get_doc("Invoice", claim.invoice) if claim.invoice else None
		
		return api_response(data={
			"claim": claim.as_dict(),
			"invoice_details": {
				"invoice_id": invoice.name,
				"patient_name": invoice.patient_name,
				"invoice_date": invoice.invoice_date,
				"total_amount": invoice.total_amount,
				"payment_status": invoice.payment_status
			} if invoice else None,
			"claim_status": claim.status,
			"reimbursement_status": "Pending" if claim.status == "Submitted" else claim.status
		})
	except Exception as e:
		frappe.log_error(f"get_claim_status error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_patient_claims(patient_id, status=None):
	"""
	Get all insurance claims for a patient
	
	Args:
		patient_id (str): Patient ID
		status (str): Filter by status (Submitted, Approved, Rejected, Reimbursed)
	
	Returns:
		dict: {status, data: claims, message}
	"""
	try:
		if not patient_id:
			return api_response(status="error", message="Patient ID is required")
		
		if not frappe.db.exists("Patient", patient_id):
			return api_response(status="error", message="Patient not found")
		
		filters = {"patient": patient_id}
		if status:
			filters["status"] = status
		
		claims = frappe.get_all("Insurance Claim",
			filters=filters,
			fields=["name", "patient", "invoice", "claim_date", "claim_amount", "status"],
			order_by="claim_date desc"
		)
		
		# Calculate summary
		total_claims = len(claims)
		total_amount = sum([flt(c.claim_amount) for c in claims])
		
		status_breakdown = {}
		for claim in claims:
			claim_status = claim.status
			status_breakdown[claim_status] = status_breakdown.get(claim_status, 0) + 1
		
		return api_response(data={
			"patient": patient_id,
			"claims": claims,
			"total_claims": total_claims,
			"total_claim_amount": total_amount,
			"status_breakdown": status_breakdown
		})
	except Exception as e:
		frappe.log_error(f"get_patient_claims error: {str(e)}")
		return api_response(status="error", message=str(e))
