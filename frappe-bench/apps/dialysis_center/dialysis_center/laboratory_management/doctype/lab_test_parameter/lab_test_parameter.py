import frappe
from frappe.model.document import Document

class LabTestParameter(Document):
	def validate(self):
		"""Validate parameter results against reference ranges"""
		self.set_normal_range()
		self.check_result_status()
	
	def set_normal_range(self):
		"""Set normal range display text"""
		if self.reference_range_min and self.reference_range_max:
			self.normal_range = f"{self.reference_range_min} - {self.reference_range_max}"
		elif self.reference_range_min:
			self.normal_range = f"> {self.reference_range_min}"
		elif self.reference_range_max:
			self.normal_range = f"< {self.reference_range_max}"
	
	def check_result_status(self):
		"""Check if result is within normal range"""
		if self.result_type == "Numeric" and self.result_value:
			try:
				result = float(self.result_value)
				
				if self.reference_range_min and result < self.reference_range_min:
					self.status = "Low"
					# Critical if significantly below range
					if result < (self.reference_range_min * 0.7):
						self.status = "Critical"
				elif self.reference_range_max and result > self.reference_range_max:
					self.status = "High"
					# Critical if significantly above range
					if result > (self.reference_range_max * 1.3):
						self.status = "Critical"
				else:
					self.status = "Normal"
			except (ValueError, TypeError):
				pass
