import frappe
from frappe.model.document import Document

class VitalSignsReading(Document):
	def validate(self):
		"""Validate vital signs and set alerts"""
		self.check_vital_ranges()
		if not self.reading_time:
			self.reading_time = frappe.utils.now_datetime()
	
	def check_vital_ranges(self):
		"""Check if vitals are within normal ranges and set status"""
		alerts = []
		
		# Check BP
		if self.bp_systolic:
			if self.bp_systolic > 180 or self.bp_systolic < 90:
				alerts.append(f"BP Systolic: {self.bp_systolic} mmHg")
				self.status_indicator = "Critical"
			elif self.bp_systolic > 140 or self.bp_systolic < 100:
				alerts.append(f"BP Systolic: {self.bp_systolic} mmHg")
				if self.status_indicator != "Critical":
					self.status_indicator = "Warning"
		
		# Check Heart Rate
		if self.heart_rate:
			if self.heart_rate > 120 or self.heart_rate < 50:
				alerts.append(f"Heart Rate: {self.heart_rate} bpm")
				self.status_indicator = "Critical"
			elif self.heart_rate > 100 or self.heart_rate < 60:
				alerts.append(f"Heart Rate: {self.heart_rate} bpm")
				if self.status_indicator != "Critical":
					self.status_indicator = "Warning"
		
		# Check O2 Saturation
		if self.oxygen_saturation:
			if self.oxygen_saturation < 90:
				alerts.append(f"O2 Sat: {self.oxygen_saturation}%")
				self.status_indicator = "Critical"
			elif self.oxygen_saturation < 95:
				alerts.append(f"O2 Sat: {self.oxygen_saturation}%")
				if self.status_indicator != "Critical":
					self.status_indicator = "Warning"
		
		if alerts and not self.alert_notes:
			self.alert_notes = "Alerts: " + ", ".join(alerts)
