import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _

class TreatmentTemplate(Document):
	def validate(self):
		"""Validate treatment template"""
		self.validate_template_completeness()
		self.validate_values()
		self.set_default_values()
	
	def validate_template_completeness(self):
		"""Validate template has all required details"""
		if not self.template_name:
			frappe.throw(_("Template Name is required"))
		
		if not self.treatment_duration:
			frappe.throw(_("Treatment Duration is required"))
		
		if not self.dialysis_modality:
			frappe.throw(_("Dialysis Modality is required"))
	
	def validate_values(self):
		"""Validate numeric values"""
		if self.treatment_duration and flt(self.treatment_duration) <= 0:
			frappe.throw(_("Treatment Duration must be greater than 0"))
		
		if self.blood_flow_rate and flt(self.blood_flow_rate) < 0:
			frappe.throw(_("Blood Flow Rate cannot be negative"))
		
		if self.dialysate_flow_rate and flt(self.dialysate_flow_rate) <= 0:
			frappe.throw(_("Dialysate Flow Rate must be greater than 0"))
	
	def set_default_values(self):
		"""Set default values if not provided"""
		if not self.dialysis_modality:
			self.dialysis_modality = "Hemodialysis"
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace
		if self.template_name:
			self.template_name = self.template_name.strip()
		
		if self.description:
			self.description = self.description.strip()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"treatment_template_{self.name}")
		frappe.cache.delete_value("treatment_templates_list")
