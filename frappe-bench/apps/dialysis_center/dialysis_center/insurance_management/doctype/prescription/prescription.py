import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _

class Prescription(Document):
	def validate(self):
		"""Validate prescription"""
		self.validate_medication_items()
		self.validate_dosage()
	
	def validate_medication_items(self):
		"""Validate prescription has medication items"""
		if not self.items or len(self.items) == 0:
			frappe.throw(_("Prescription must have at least one medication"))
		
		# Validate each medication item
		for item in self.items:
			if not item.medication:
				frappe.throw(_("Row {0}: Medication is required").format(item.idx))
			
			# Verify medication exists
			if not frappe.db.exists("Medication", item.medication):
				frappe.throw(_("Row {0}: Medication {1} does not exist").format(item.idx, item.medication))
	
	def validate_dosage(self):
		"""Validate dosage information"""
		for item in self.items:
			if not item.dosage:
				frappe.throw(_("Row {0}: Dosage is required").format(item.idx))
			
			if not item.frequency:
				frappe.throw(_("Row {0}: Frequency is required").format(item.idx))
			
			if item.duration and flt(item.duration) <= 0:
				frappe.throw(_("Row {0}: Duration must be greater than 0").format(item.idx))
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from notes
		if self.notes:
			self.notes = self.notes.strip()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"prescription_{self.name}")
		if hasattr(self, 'patient'):
			frappe.cache.delete_value(f"patient_{self.patient}_prescriptions")
