import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate, getdate
from frappe import _

class Invoice(Document):
	def validate(self):
		self.validate_patient()
		self.validate_items_exist()
		self.validate_items()
		self.calculate_line_totals()
		self.calculate_totals()
		self.validate_amounts()
		self.set_due_date()
	
	def validate_items_exist(self):
		"""Validate that invoice items reference valid items/services"""
		if not self.items or len(self.items) == 0:
			frappe.throw(_("Invoice must have at least one item"))
		
		for item in self.items:
			if not item.description:
				frappe.throw(_("Row {0}: Description is required").format(item.idx))
	
	def validate_patient(self):
		"""Validate patient exists and is active"""
		if self.patient:
			patient_status = frappe.db.get_value("Patient", self.patient, "status")
			if patient_status != "Active":
				frappe.msgprint(_("Warning: Invoice is being created for inactive patient"), 
					indicator="orange", alert=True)
	
	def validate_items(self):
		"""Validate invoice has items"""
		if not self.items or len(self.items) == 0:
			frappe.throw(_("Invoice must have at least one item"))
		
		# Validate each item
		for item in self.items:
			if not item.description:
				frappe.throw(_("Row {0}: Description is required").format(item.idx))
			
			if flt(item.quantity) <= 0:
				frappe.throw(_("Row {0}: Quantity must be greater than 0").format(item.idx))
			
			if flt(item.rate) < 0:
				frappe.throw(_("Row {0}: Rate cannot be negative").format(item.idx))
	
	def calculate_totals(self):
		"""Calculate invoice totals from line items"""
		self.total_qty = 0
		self.subtotal = 0
		
		# Calculate from items table
		if self.items:
			for item in self.items:
				item.amount = flt(item.quantity) * flt(item.rate)
				self.subtotal += item.amount
				self.total_qty += flt(item.quantity)
		
		# Calculate discount
		if self.discount_percent:
			self.discount_amount = flt(self.subtotal * (self.discount_percent / 100), 2)
		elif not self.discount_amount:
			self.discount_amount = 0
		
		# Calculate tax
		if self.tax_percent:
			taxable_amount = self.subtotal - self.discount_amount
			self.tax_amount = flt(taxable_amount * (self.tax_percent / 100), 2)
		elif not self.tax_amount:
			self.tax_amount = 0
		
		# Calculate grand total
		self.total_amount = flt(self.subtotal - self.discount_amount + self.tax_amount, 2)
		
		# Calculate outstanding
		self.outstanding_amount = flt(self.total_amount - (self.paid_amount or 0), 2)
		
		# Update payment status
		self.update_payment_status()
	
	def validate_amounts(self):
		"""Validate calculated amounts"""
		if self.total_amount < 0:
			frappe.throw(_("Total amount cannot be negative"))
		
		if self.discount_amount > self.subtotal:
			frappe.throw(_("Discount amount cannot be greater than subtotal"))
		
		if self.paid_amount > self.total_amount:
			frappe.throw(_("Paid amount cannot be greater than total amount"))
	
	def update_payment_status(self):
		"""Update payment status based on amounts"""
		if self.outstanding_amount <= 0:
			self.payment_status = "Paid"
		elif self.paid_amount > 0:
			self.payment_status = "Partially Paid"
		else:
			self.payment_status = "Unpaid"
	
	def calculate_line_totals(self):
		"""Calculate line totals for each item"""
		if self.items:
			for item in self.items:
				item.amount = flt(item.quantity) * flt(item.rate)
	
	def set_due_date(self):
		"""Set due date if not set"""
		if not self.due_date and self.invoice_date:
			# Default 30 days from invoice date
			from frappe.utils import add_days
			self.due_date = add_days(self.invoice_date, 30)
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from text fields
		if self.notes:
			self.notes = self.notes.strip()
		
		# Set invoice date if not set
		if not self.invoice_date:
			self.invoice_date = nowdate()
		
		# Normalize patient name
		if self.patient_name:
			self.patient_name = self.patient_name.strip()
		
		# Ensure totals are calculated
		self.calculate_line_totals()
		self.calculate_totals()
	
	def before_submit(self):
		"""Validate before submitting"""
		if self.payment_status != "Paid" and not self.outstanding_amount:
			self.calculate_totals()
		
		# Link to dialysis session if applicable
		if self.session and not self.session_linked:
			self.link_to_session()
	
	def on_submit(self):
		"""Actions after invoice submission"""
		self.update_session_billing_status()
		self.update_patient_billing_summary()
		self.db_set("status", "Submitted")
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"invoice_{self.name}")
		frappe.cache.delete_value(f"patient_{self.patient}_invoices")
		frappe.cache.delete_value(f"patient_{self.patient}_outstanding")
	
	def update_patient_billing_summary(self):
		"""Update patient's billing summary"""
		if self.patient:
			try:
				# Recalculate patient's total outstanding
				outstanding_total = frappe.db.sql("""
					SELECT COALESCE(SUM(outstanding_amount), 0)
					FROM `tabInvoice`
					WHERE patient = %s AND docstatus = 1 AND payment_status != 'Paid'
				""", (self.patient,))[0][0]
				
				frappe.db.set_value("Patient", self.patient, "total_outstanding", outstanding_total)
			except Exception as e:
				frappe.log_error(message=str(e), title="Patient Billing Summary Update Failed")
	
	def link_to_session(self):
		"""Link invoice to dialysis session"""
		if self.session:
			session = frappe.get_doc("Dialysis Session", self.session)
			if session.docstatus == 1:  # Submitted
				self.session_linked = 1
	
	def update_session_billing_status(self):
		"""Update related session with billing status"""
		if self.session:
			try:
				session = frappe.get_doc("Dialysis Session", self.session)
				session.add_comment("Comment", _("Invoice {0} created for amount {1}").format(
					self.name, self.total_amount))
			except Exception as e:
				frappe.log_error(message=str(e), title="Session Update Failed")
	
	def on_cancel(self):
		"""Actions on invoice cancellation"""
		# Reset payment status
		self.db_set("payment_status", "Cancelled")
		self.db_set("outstanding_amount", 0)
		
		# Cancel linked payments
		payments = frappe.get_all("Payment", 
			filters={"invoice": self.name, "docstatus": 1},
			fields=["name"])
		
		for payment in payments:
			try:
				payment_doc = frappe.get_doc("Payment", payment.name)
				payment_doc.cancel()
			except Exception as e:
				frappe.log_error(message=str(e), title="Payment Cancellation Failed")
		
		# Update patient billing summary
		self.update_patient_billing_summary()
		
		# Clear caches
		frappe.cache.delete_value(f"invoice_{self.name}")
		frappe.cache.delete_value(f"patient_{self.patient}_invoices")
		frappe.cache.delete_value(f"patient_{self.patient}_outstanding")

@frappe.whitelist()
def get_session_details(session):
	"""Get details from dialysis session for invoicing"""
	if not session:
		return {}
	
	session_doc = frappe.get_doc("Dialysis Session", session)
	patient = frappe.get_doc("Patient", session_doc.patient)
	
	# Get default rate from treatment template or patient
	default_rate = 0
	if patient.treatment_template:
		template = frappe.get_doc("Treatment Template", patient.treatment_template)
		default_rate = template.session_rate or 0
	
	return {
		"patient": session_doc.patient,
		"patient_name": session_doc.patient_name,
		"session_date": session_doc.session_date,
		"default_rate": default_rate,
		"duration": session_doc.actual_duration or session_doc.treatment_duration
	}

@frappe.whitelist()
def create_invoice_from_session(session):
	"""Create invoice from dialysis session"""
	session_doc = frappe.get_doc("Dialysis Session", session)
	
	# Check if invoice already exists
	existing = frappe.db.exists("Invoice", {"session": session})
	if existing:
		frappe.throw(_("Invoice already exists for this session: {0}").format(existing))
	
	# Get patient details
	patient = frappe.get_doc("Patient", session_doc.patient)
	
	# Get rate from treatment template
	rate = 0
	if patient.treatment_template:
		template = frappe.get_doc("Treatment Template", patient.treatment_template)
		rate = template.session_rate or 0
	
	# Create invoice
	invoice = frappe.get_doc({
		"doctype": "Invoice",
		"patient": session_doc.patient,
		"patient_name": session_doc.patient_name,
		"invoice_date": nowdate(),
		"session": session,
		"items": [{
			"description": f"Dialysis Session - {session_doc.session_date}",
			"quantity": 1,
			"rate": rate,
			"amount": rate
		}]
	})
	invoice.insert()
	
	return invoice.name
