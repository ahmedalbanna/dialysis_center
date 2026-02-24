import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, flt
from frappe import _

class LabTest(Document):
	def validate(self):
		self.validate_patient()
		self.validate_test_date()
		self.validate_test_type()
		self.check_abnormal_results()
		self.set_status()
	
	def validate_test_type(self):
		"""Validate test type is properly set"""
		if not self.test_name:
			frappe.throw(_("Test Name/Type is required"))
	
	def validate_patient(self):
		"""Validate patient exists"""
		if self.patient:
			patient_status = frappe.db.get_value("Patient", self.patient, "status")
			if patient_status != "Active":
				frappe.msgprint(_("Warning: Lab test for inactive patient"), 
					indicator="orange", alert=True)
	
	def validate_test_date(self):
		"""Set test date if not set"""
		if not self.test_date:
			self.test_date = nowdate()
	
	def check_abnormal_results(self):
		"""Mark results outside normal range and alert"""
		abnormal_count = 0
		critical_count = 0
		
		if self.results:
			for result in self.results:
				# Check if result is within normal range
				if result.normal_range_min and result.normal_range_max and result.result_value:
					value = flt(result.result_value)
					min_val = flt(result.normal_range_min)
					max_val = flt(result.normal_range_max)
					
					if value < min_val or value > max_val:
						result.is_abnormal = 1
						abnormal_count += 1
						
						# Check for critical values (way outside normal range)
						if value < (min_val * 0.5) or value > (max_val * 1.5):
							result.is_critical = 1
							critical_count += 1
		
		if critical_count > 0:
			frappe.msgprint(_("CRITICAL: {0} test result(s) are critically abnormal").format(critical_count),
				indicator="red", alert=True)
		elif abnormal_count > 0:
			frappe.msgprint(_("Warning: {0} test result(s) are abnormal").format(abnormal_count),
				indicator="orange", alert=True)
	
	def set_status(self):
		"""Set test status"""
		if not self.status:
			if self.results and len(self.results) > 0:
				self.status = "Pending"
			else:
				self.status = "Ordered"
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from notes
		if self.notes:
			self.notes = self.notes.strip()
		
		# Set test date if not set
		if not self.test_date:
			self.test_date = nowdate()
		
		# Normalize test name
		if self.test_name:
			self.test_name = self.test_name.strip()
	
	def before_submit(self):
		"""Validate before submission"""
		if not self.results or len(self.results) == 0:
			frappe.throw(_("Cannot submit lab test without results"))
		
		# Ensure all results have values
		for result in self.results:
			if not result.result_value:
				frappe.throw(_("Row {0}: Result value is required").format(result.idx))
		
		self.status = "Completed"
		if not self.completed_date:
			self.completed_date = nowdate()
	
	def on_submit(self):
		"""Create lab result records and update patient lab history"""
		self.create_lab_results()
		self.update_patient_lab_history()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"lab_test_{self.name}")
		frappe.cache.delete_value(f"patient_{self.patient}_lab_tests")
		frappe.cache.delete_value(f"patient_{self.patient}_latest_lab_results")
	
	def update_patient_lab_history(self):
		"""Update patient's lab history on test submission"""
		if self.patient:
			try:
				# Update patient's last lab test date
				frappe.db.set_value("Patient", self.patient, "last_lab_test_date", self.test_date)
				
				# Count abnormal results
				abnormal_count = len([r for r in self.results if r.is_abnormal])
				if abnormal_count > 0:
					frappe.db.set_value("Patient", self.patient, "has_abnormal_results", 1)
			except Exception as e:
				frappe.log_error(message=str(e), title="Patient Lab History Update Failed")
	
	def create_lab_results(self):
		"""Create individual lab result records for trending"""
		for result in self.results:
			lab_result = frappe.get_doc({
				"doctype": "Lab Result",
				"patient": self.patient,
				"test_name": self.test_name,
				"test_parameter": result.test_parameter,
				"result_value": result.result_value,
				"unit": result.unit,
				"normal_range_min": result.normal_range_min,
				"normal_range_max": result.normal_range_max,
				"is_abnormal": result.is_abnormal,
				"test_date": self.test_date,
				"lab_test": self.name
			})
			lab_result.insert(ignore_permissions=True)
