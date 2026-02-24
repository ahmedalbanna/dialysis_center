import frappe
from frappe.model.document import Document

class SessionEvent(Document):
	def validate(self):
		"""Validate session event"""
		if not self.event_time:
			self.event_time = frappe.utils.now_datetime()
