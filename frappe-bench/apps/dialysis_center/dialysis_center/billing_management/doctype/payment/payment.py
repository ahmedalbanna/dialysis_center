import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate, now_datetime
from frappe import _

class Payment(Document):
	def validate(self):
		self.validate_invoice()
		self.validate_payment_date()
		self.validate_amount()
		self.calculate_change()
		self.set_payment_date()
	
	def validate_payment_date(self):
		"""Validate payment date is not in future"""
		if self.payment_date:
			if getdate(self.payment_date) > getdate():
				frappe.throw(_("Payment date cannot be in the future"))
	
	def validate_invoice(self):
		"""Validate invoice exists and is submitted"""
		if self.invoice:
			invoice = frappe.get_doc("Invoice", self.invoice)
			
			if invoice.docstatus != 1:
				frappe.throw(_("Cannot create payment for unsubmitted invoice"))
			
			if invoice.payment_status == "Paid":
				frappe.msgprint(_("Warning: Invoice is already fully paid"), 
					indicator="orange", alert=True)
			
			# Auto-fill patient if not set
			if not self.patient:
				self.patient = invoice.patient
				self.patient_name = invoice.patient_name
	
	def validate_amount(self):
		"""Validate payment amount"""
		if flt(self.amount) <= 0:
			frappe.throw(_("Payment amount must be greater than 0"))
		
		if self.invoice:
			invoice = frappe.get_doc("Invoice", self.invoice)
			
			# Check if payment exceeds outstanding amount
			total_paid = flt(invoice.paid_amount) + flt(self.amount)
			if total_paid > flt(invoice.total_amount):
				frappe.throw(_("Payment amount ({0}) exceeds outstanding amount ({1})").format(
					self.amount, invoice.outstanding_amount))
		
		# Validate cash tender
		if self.payment_method == "Cash":
			if self.amount_tendered and flt(self.amount_tendered) < flt(self.amount):
				frappe.throw(_("Amount tendered cannot be less than payment amount"))
	
	def calculate_change(self):
		"""Calculate change for cash payments"""
		if self.payment_method == "Cash" and self.amount_tendered:
			self.change_amount = flt(self.amount_tendered - self.amount, 2)
		else:
			self.change_amount = 0
	
	def set_payment_date(self):
		"""Set payment date if not set"""
		if not self.payment_date:
			self.payment_date = nowdate()
		
		if not self.payment_time:
			self.payment_time = now_datetime()
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from notes
		if self.notes:
			self.notes = self.notes.strip()
		
		# Normalize reference number
		if self.reference_number:
			self.reference_number = self.reference_number.strip().upper()
		
		# Ensure amounts are calculated
		self.calculate_change()
	
	def before_submit(self):
		"""Validate before submitting"""
		if not self.invoice:
			frappe.throw(_("Invoice is required before submitting payment"))
		
		if not self.payment_method:
			frappe.throw(_("Payment method is required"))
		
		# Validate reference number for non-cash payments
		if self.payment_method != "Cash" and not self.reference_number:
			frappe.msgprint(_("Warning: Reference number recommended for {0} payments").format(
				self.payment_method), indicator="orange", alert=True)
	
	def on_submit(self):
		"""Update invoice after payment submission"""
		if self.invoice:
			self.update_invoice_payment()
		
		# Update patient outstanding amount
		if self.patient:
			self.update_patient_outstanding()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"payment_{self.name}")
		frappe.cache.delete_value(f"invoice_{self.invoice}_payments")
		frappe.cache.delete_value(f"patient_{self.patient}_payments")
	
	def update_patient_outstanding(self):
		"""Update patient's total outstanding amount"""
		if self.patient:
			try:
				outstanding_total = frappe.db.sql("""
					SELECT COALESCE(SUM(outstanding_amount), 0)
					FROM `tabInvoice`
					WHERE patient = %s AND docstatus = 1 AND payment_status != 'Paid'
				""", (self.patient,))[0][0]
				
				frappe.db.set_value("Patient", self.patient, "total_outstanding", outstanding_total)
			except Exception as e:
				frappe.log_error(message=str(e), title="Patient Outstanding Update Failed")
	
	def update_invoice_payment(self):
		"""Update invoice paid amount and status"""
		invoice = frappe.get_doc("Invoice", self.invoice)
		
		# Update paid amount
		invoice.paid_amount = flt(invoice.paid_amount or 0) + flt(self.amount)
		
		# Recalculate outstanding and status
		invoice.calculate_totals()
		invoice.save(ignore_permissions=True)
		
		# Add comment to invoice
		invoice.add_comment("Comment", _("Payment received: {0} via {1}").format(
			self.amount, self.payment_method))
	
	def on_cancel(self):
		"""Reverse payment on cancellation"""
		if self.invoice:
			self.reverse_invoice_payment()
		
		# Update patient outstanding amount
		if self.patient:
			self.update_patient_outstanding()
		
		# Clear caches
		frappe.cache.delete_value(f"payment_{self.name}")
		frappe.cache.delete_value(f"invoice_{self.invoice}_payments")
		frappe.cache.delete_value(f"patient_{self.patient}_payments")
	
	def reverse_invoice_payment(self):
		"""Reverse payment from invoice"""
		invoice = frappe.get_doc("Invoice", self.invoice)
		
		# Reverse paid amount
		invoice.paid_amount = max(flt(invoice.paid_amount or 0) - flt(self.amount), 0)
		
		# Recalculate outstanding and status
		invoice.calculate_totals()
		invoice.save(ignore_permissions=True)
		
		# Add comment to invoice
		invoice.add_comment("Comment", _("Payment {0} cancelled").format(self.name))

@frappe.whitelist()
def get_invoice_outstanding(invoice):
	"""Get outstanding amount for an invoice"""
	if not invoice:
		return 0
	
	invoice_doc = frappe.get_doc("Invoice", invoice)
	return {
		"outstanding_amount": invoice_doc.outstanding_amount,
		"total_amount": invoice_doc.total_amount,
		"paid_amount": invoice_doc.paid_amount,
		"payment_status": invoice_doc.payment_status
	}

@frappe.whitelist()
def create_payment_from_invoice(invoice, amount, payment_method="Cash"):
	"""Create payment record from invoice"""
	invoice_doc = frappe.get_doc("Invoice", invoice)
	
	if invoice_doc.docstatus != 1:
		frappe.throw(_("Invoice must be submitted before creating payment"))
	
	if invoice_doc.payment_status == "Paid":
		frappe.throw(_("Invoice is already fully paid"))
	
	# Create payment
	payment = frappe.get_doc({
		"doctype": "Payment",
		"invoice": invoice,
		"patient": invoice_doc.patient,
		"patient_name": invoice_doc.patient_name,
		"amount": amount or invoice_doc.outstanding_amount,
		"payment_method": payment_method,
		"payment_date": nowdate()
	})
	payment.insert()
	
	return payment.name
