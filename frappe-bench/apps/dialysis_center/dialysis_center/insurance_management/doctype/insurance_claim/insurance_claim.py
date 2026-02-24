import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate, getdate
from frappe import _

class InsuranceClaim(Document):
	def validate(self):
		"""Validate insurance claim"""
		self.validate_patient()
		self.validate_provider()
		self.validate_claim_amount()
		self.calculate_coverage()
	
	def validate_patient(self):
		"""Validate patient exists and is active"""
		if self.patient:
			patient_status = frappe.db.get_value("Patient", self.patient, "status")
			if patient_status != "Active":
				frappe.msgprint(_("Warning: Claim for inactive patient"), 
					indicator="orange", alert=True)
	
	def validate_provider(self):
		"""Validate insurance provider exists"""
		if self.insurance_provider:
			if not frappe.db.exists("Insurance Provider", self.insurance_provider):
				frappe.throw(_("Insurance Provider {0} does not exist").format(self.insurance_provider))
	
	def validate_claim_amount(self):
		"""Validate claim amount is positive"""
		if flt(self.claim_amount) <= 0:
			frappe.throw(_("Claim amount must be greater than 0"))
		
		if self.approved_amount and flt(self.approved_amount) > flt(self.claim_amount):
			frappe.throw(_("Approved amount cannot be greater than claimed amount"))
	
	def calculate_coverage(self):
		"""Calculate coverage based on percentage and amount"""
		if self.coverage_percentage and self.claim_amount:
			suggested = flt(self.claim_amount) * (flt(self.coverage_percentage) / 100)
			if not self.approved_amount:
				self.approved_amount = suggested
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from notes
		if self.claim_notes:
			self.claim_notes = self.claim_notes.strip()
		
		# Set claim date if not set
		if not self.claim_date:
			self.claim_date = nowdate()
	
	def on_submit(self):
		"""Actions when claim is submitted"""
		self.update_claim_status()
		self.update_claim_history()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"insurance_claim_{self.name}")
		frappe.cache.delete_value(f"patient_{self.patient}_claims")
	
	def update_claim_status(self):
		"""Update claim status on submission"""
		self.db_set("status", "Submitted")
		self.db_set("submission_date", nowdate())
	
	def update_claim_history(self):
		"""Update patient's claim history"""
		if self.patient:
			try:
				frappe.db.set_value("Patient", self.patient, "last_claim_date", self.claim_date)
			except Exception as e:
				frappe.log_error(message=str(e), title="Patient Claim History Update Failed")
