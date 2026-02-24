import frappe
from frappe import _
from frappe.utils import nowdate, flt, add_days
import json

# Helper function for standardized API responses
def api_response(status="success", data=None, message=""):
	"""Standardized API response format"""
	return {
		"status": status,
		"data": data,
		"message": message
	}

# ==================== INVOICE LIST & DETAILS ====================

@frappe.whitelist()
def get_invoice_list(filters=None, start=0, page_length=20):
	"""
	Get list of invoices with filtering
	
	Args:
		filters (str/dict): Additional filters
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: invoices, message}
	"""
	try:
		start = int(start)
		page_length = min(int(page_length), 100)
		
		filter_dict = {}
		if filters:
			if isinstance(filters, str):
				filters = frappe.parse_json(filters)
			filter_dict.update(filters)
		
		invoices = frappe.get_all("Invoice",
			filters=filter_dict,
			fields=["name", "patient", "patient_name", "invoice_date", "total_amount", 
					"amount_paid", "outstanding_amount", "payment_status"],
			order_by="invoice_date desc",
			start=start,
			page_length=page_length
		)
		
		frappe.get_logger().info(f"API: get_invoice_list - {len(invoices)} invoices retrieved")
		
		return api_response(data={
			"invoices": invoices,
			"count": len(invoices),
			"total": frappe.db.count("Invoice", filter_dict)
		})
	except Exception as e:
		frappe.log_error(f"get_invoice_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_invoice_details(invoice_id):
	"""
	Get full invoice details with line items
	
	Args:
		invoice_id (str): Invoice ID
	
	Returns:
		dict: {status, data: invoice_details, message}
	"""
	try:
		if not invoice_id:
			return api_response(status="error", message="Invoice ID is required")
		
		if not frappe.db.exists("Invoice", invoice_id):
			return api_response(status="error", message="Invoice not found")
		
		invoice = frappe.get_doc("Invoice", invoice_id)
		
		return api_response(data={
			"invoice": invoice.as_dict(),
			"items": invoice.invoice_items if hasattr(invoice, 'invoice_items') else [],
			"payment_history": frappe.get_all("Payment",
				filters={"invoice": invoice_id},
				fields=["name", "payment_date", "amount", "payment_mode", "reference_number"])
		})
	except Exception as e:
		frappe.log_error(f"get_invoice_details error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def create_invoice(patient_id, session_ids=None, treatment_items=None):
	"""
	Create invoice from sessions or manual items
	
	Args:
		patient_id (str): Patient ID
		session_ids (str/list): Dialysis session IDs (optional)
		treatment_items (str/list): Manual treatment items (optional)
	
	Returns:
		dict: {status, data: invoice, message}
	"""
	try:
		if not patient_id:
			return api_response(status="error", message="patient_id is required")
		
		if not frappe.db.exists("Patient", patient_id):
			return api_response(status="error", message="Patient not found")
		
		patient = frappe.get_value("Patient", patient_id, ["patient_name"])
		
		invoice = frappe.get_doc({
			"doctype": "Invoice",
			"patient": patient_id,
			"patient_name": patient[0],
			"invoice_date": nowdate(),
			"payment_status": "Unpaid"
		})
		
		# Add sessions if provided
		if session_ids:
			if isinstance(session_ids, str):
				session_ids = frappe.parse_json(session_ids)
			
			for session_id in session_ids:
				if frappe.db.exists("Dialysis Session", session_id):
					invoice.append("invoice_items", {
						"item_type": "Dialysis Session",
						"item_description": f"Dialysis Session - {session_id}",
						"quantity": 1,
						"unit": "Session",
						"rate": 500,  # Should be from price list
						"reference_doctype": "Dialysis Session",
						"reference_name": session_id
					})
		
		# Add manual treatment items if provided
		if treatment_items:
			if isinstance(treatment_items, str):
				treatment_items = frappe.parse_json(treatment_items)
			
			for item in treatment_items:
				invoice.append("invoice_items", item)
		
		invoice.insert(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: create_invoice - {invoice.name} created")
		
		return api_response(data=invoice.as_dict(), message="Invoice created successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"create_invoice error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def submit_invoice(invoice_id):
	"""
	Submit invoice for payment
	
	Args:
		invoice_id (str): Invoice ID
	
	Returns:
		dict: {status, data: invoice, message}
	"""
	try:
		if not invoice_id:
			return api_response(status="error", message="Invoice ID is required")
		
		if not frappe.db.exists("Invoice", invoice_id):
			return api_response(status="error", message="Invoice not found")
		
		invoice = frappe.get_doc("Invoice", invoice_id)
		
		if invoice.docstatus != 0:
			return api_response(status="error", message="Invoice already submitted or cancelled")
		
		invoice.submit()
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: submit_invoice - {invoice_id} submitted")
		
		return api_response(data=invoice.as_dict(), message="Invoice submitted successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"submit_invoice error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def record_payment(invoice_id, amount, payment_date=None, payment_method="Cash"):
	"""
	Record payment for invoice
	
	Args:
		invoice_id (str): Invoice ID
		amount (float): Payment amount
		payment_date (str): Payment date (YYYY-MM-DD)
		payment_method (str): Payment method (Cash, Card, Check, Bank Transfer)
	
	Returns:
		dict: {status, data: payment, message}
	"""
	try:
		if not invoice_id or not amount:
			return api_response(status="error", message="invoice_id and amount are required")
		
		if not frappe.db.exists("Invoice", invoice_id):
			return api_response(status="error", message="Invoice not found")
		
		invoice = frappe.get_doc("Invoice", invoice_id)
		amount = flt(amount)
		
		if amount <= 0:
			return api_response(status="error", message="Amount must be positive")
		
		payment = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice_id,
			"patient": invoice.patient,
			"patient_name": invoice.patient_name,
			"payment_date": payment_date or nowdate(),
			"amount": amount,
			"payment_mode": payment_method,
			"status": "Completed"
		})
		
		payment.insert(ignore_permissions=True)
		payment.submit()
		
		# Update invoice
		invoice.amount_paid = flt(invoice.amount_paid or 0) + amount
		invoice.outstanding_amount = flt(invoice.total_amount) - flt(invoice.amount_paid)
		
		if invoice.outstanding_amount <= 0:
			invoice.payment_status = "Paid"
		elif invoice.amount_paid > 0:
			invoice.payment_status = "Partially Paid"
		
		invoice.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: record_payment - Payment {payment.name} recorded for {invoice_id}")
		
		return api_response(data=payment.as_dict(), message="Payment recorded successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"record_payment error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_outstanding_invoices(patient_id=None):
	"""
	Get outstanding (unpaid/partially paid) invoices
	
	Args:
		patient_id (str): Patient ID (optional, for single patient)
	
	Returns:
		dict: {status, data: invoices, message}
	"""
	try:
		filters = {
			"payment_status": ["!=", "Paid"],
			"docstatus": 1
		}
		
		if patient_id:
			filters["patient"] = patient_id
		
		invoices = frappe.get_all("Invoice",
			filters=filters,
			fields=["name", "patient", "patient_name", "invoice_date", "total_amount",
					"amount_paid", "outstanding_amount", "payment_status"],
			order_by="invoice_date asc"
		)
		
		total_outstanding = sum([inv.outstanding_amount for inv in invoices])
		
		return api_response(data={
			"invoices": invoices,
			"count": len(invoices),
			"total_outstanding": total_outstanding
		})
	except Exception as e:
		frappe.log_error(f"get_outstanding_invoices error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_financial_summary(from_date=None, to_date=None):
	"""
	Get financial summary (revenue, collections, outstanding)
	
	Args:
		from_date (str): Start date (YYYY-MM-DD)
		to_date (str): End date (YYYY-MM-DD)
	
	Returns:
		dict: {status, data: summary, message}
	"""
	try:
		filters = {"docstatus": 1}
		
		if from_date:
			filters["invoice_date"] = [">=", from_date]
		if to_date:
			if "invoice_date" in filters:
				filters["invoice_date"] = ["between", [from_date, to_date]]
			else:
				filters["invoice_date"] = ["<=", to_date]
		
		invoices = frappe.get_all("Invoice",
			filters=filters,
			fields=["total_amount", "amount_paid", "outstanding_amount", "payment_status"]
		)
		
		total_revenue = sum([inv.total_amount for inv in invoices])
		collected = sum([inv.amount_paid or 0 for inv in invoices])
		outstanding = sum([inv.outstanding_amount or 0 for inv in invoices])
		
		paid_count = len([inv for inv in invoices if inv.payment_status == "Paid"])
		partially_paid = len([inv for inv in invoices if inv.payment_status == "Partially Paid"])
		unpaid = len([inv for inv in invoices if inv.payment_status == "Unpaid"])
		
		return api_response(data={
			"from_date": from_date or "N/A",
			"to_date": to_date or "N/A",
			"total_revenue": total_revenue,
			"collected": collected,
			"outstanding": outstanding,
			"total_invoices": len(invoices),
			"paid_invoices": paid_count,
			"partially_paid_invoices": partially_paid,
			"unpaid_invoices": unpaid,
			"collection_rate": (collected / total_revenue * 100) if total_revenue > 0 else 0
		})
	except Exception as e:
		frappe.log_error(f"get_financial_summary error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def create_invoice_from_session(session):
	"""Create an invoice from a dialysis session"""
	if not session:
		frappe.throw(_("Session is required"))
	
	session_doc = frappe.get_doc("Dialysis Session", session)
	
	if session_doc.status != "Completed":
		frappe.throw(_("Session must be completed to generate invoice"))
	
	# Check if invoice already exists
	existing = frappe.db.exists("Invoice", {"dialysis_session": session})
	if existing:
		frappe.throw(_("Invoice already exists for this session: {0}").format(existing))
	
	# Create invoice
	invoice = frappe.get_doc({
		"doctype": "Invoice",
		"patient": session_doc.patient,
		"patient_name": session_doc.patient_name,
		"invoice_date": nowdate(),
		"dialysis_session": session,
		"payment_status": "Unpaid"
	})
	
	# Add session as invoice item
	invoice.append("invoice_items", {
		"item_type": "Dialysis Session",
		"item_description": f"Dialysis Session - {session_doc.session_date}",
		"quantity": 1,
		"unit": "Session",
		"rate": 500,  # Default rate - should be configurable
		"reference_doctype": "Dialysis Session",
		"reference_name": session
	})
	
	invoice.insert(ignore_permissions=True)
	
	return invoice.name

@frappe.whitelist()
def record_payment(invoice, amount, payment_mode="Cash", reference_number=None):
	"""Record a payment for an invoice"""
	if not invoice or not amount:
		frappe.throw(_("Invoice and amount are required"))
	
	invoice_doc = frappe.get_doc("Invoice", invoice)
	amount = flt(amount)
	
	# Create payment document
	payment = frappe.get_doc({
		"doctype": "Payment",
		"invoice": invoice,
		"patient": invoice_doc.patient,
		"patient_name": invoice_doc.patient_name,
		"payment_date": nowdate(),
		"amount": amount,
		"payment_mode": payment_mode,
		"reference_number": reference_number,
		"status": "Completed"
	})
	
	payment.insert(ignore_permissions=True)
	payment.submit()
	
	# Update invoice
	invoice_doc.amount_paid = flt(invoice_doc.amount_paid) + amount
	invoice_doc.outstanding_amount = flt(invoice_doc.total_amount) - flt(invoice_doc.amount_paid)
	
	if invoice_doc.outstanding_amount <= 0:
		invoice_doc.payment_status = "Paid"
	elif invoice_doc.amount_paid > 0:
		invoice_doc.payment_status = "Partially Paid"
	
	invoice_doc.save(ignore_permissions=True)
	
	return payment.name

@frappe.whitelist()
def get_outstanding_invoices(patient=None):
	"""Get outstanding invoices"""
	filters = {
		"payment_status": ["!=", "Paid"],
		"docstatus": 1
	}
	
	if patient:
		filters["patient"] = patient
	
	invoices = frappe.get_all("Invoice",
		filters=filters,
		fields=["name", "patient", "patient_name", "invoice_date", "total_amount", 
				"outstanding_amount", "payment_status"],
		order_by="invoice_date desc"
	)
	
	total_outstanding = sum([inv.outstanding_amount for inv in invoices])
	
	return {
		"invoices": invoices,
		"total_outstanding": total_outstanding,
		"count": len(invoices)
	}

@frappe.whitelist()
def get_payment_history(patient=None, from_date=None, to_date=None):
	"""Get payment history"""
	filters = {"docstatus": 1}
	
	if patient:
		filters["patient"] = patient
	if from_date:
		filters["payment_date"] = [">=", from_date]
	if to_date:
		if "payment_date" in filters:
			filters["payment_date"] = ["between", [from_date, to_date]]
		else:
			filters["payment_date"] = ["<=", to_date]
	
	payments = frappe.get_all("Payment",
		filters=filters,
		fields=["name", "patient", "patient_name", "payment_date", "amount", 
				"payment_mode", "invoice", "reference_number"],
		order_by="payment_date desc"
	)
	
	total_amount = sum([p.amount for p in payments])
	
	return {
		"payments": payments,
		"total_amount": total_amount,
		"count": len(payments)
	}

@frappe.whitelist()
def get_revenue_summary(from_date=None, to_date=None):
	"""Get revenue summary"""
	filters = {"docstatus": 1}
	
	if from_date:
		filters["invoice_date"] = [">=", from_date]
	if to_date:
		if "invoice_date" in filters:
			filters["invoice_date"] = ["between", [from_date, to_date]]
		else:
			filters["invoice_date"] = ["<=", to_date]
	
	# Get invoice totals
	invoices = frappe.get_all("Invoice",
		filters=filters,
		fields=["total_amount", "amount_paid", "outstanding_amount", "payment_status"]
	)
	
	total_revenue = sum([inv.total_amount for inv in invoices])
	collected = sum([inv.amount_paid for inv in invoices])
	outstanding = sum([inv.outstanding_amount for inv in invoices])
	
	paid_count = len([inv for inv in invoices if inv.payment_status == "Paid"])
	partially_paid = len([inv for inv in invoices if inv.payment_status == "Partially Paid"])
	unpaid = len([inv for inv in invoices if inv.payment_status == "Unpaid"])
	
	return {
		"total_revenue": total_revenue,
		"collected": collected,
		"outstanding": outstanding,
		"total_invoices": len(invoices),
		"paid_invoices": paid_count,
		"partially_paid_invoices": partially_paid,
		"unpaid_invoices": unpaid,
		"collection_rate": (collected / total_revenue * 100) if total_revenue > 0 else 0
	}

@frappe.whitelist()
def apply_discount(invoice, discount_type="percentage", discount_value=0):
	"""Apply discount to an invoice"""
	if not invoice:
		frappe.throw(_("Invoice is required"))
	
	doc = frappe.get_doc("Invoice", invoice)
	discount_value = flt(discount_value)
	
	if discount_type == "percentage":
		doc.discount_percentage = discount_value
		doc.discount_amount = 0
	else:
		doc.discount_amount = discount_value
		doc.discount_percentage = 0
	
	doc.save(ignore_permissions=True)
	
	return doc
