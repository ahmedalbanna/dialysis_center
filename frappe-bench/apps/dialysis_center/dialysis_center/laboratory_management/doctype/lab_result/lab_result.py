import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _

class LabResult(Document):
	def validate(self):
		self.check_abnormal_flag()
	
	def check_abnormal_flag(self):
		"""Auto-set abnormal flag based on normal range"""
		if self.result_value and self.normal_range_min and self.normal_range_max:
			value = flt(self.result_value)
			min_val = flt(self.normal_range_min)
			max_val = flt(self.normal_range_max)
			
			if value < min_val or value > max_val:
				self.is_abnormal = 1
			else:
				self.is_abnormal = 0
