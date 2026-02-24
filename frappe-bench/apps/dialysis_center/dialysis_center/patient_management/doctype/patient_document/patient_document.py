import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class PatientDocument(Document):
	def validate(self):
		"""Validate patient document"""
		self.check_expiry()
		self.set_version()
	
	def check_expiry(self):
		"""Check if document is expired"""
		if self.expiry_date:
			if getdate(self.expiry_date) < getdate(nowdate()):
				self.is_expired = 1
			else:
				self.is_expired = 0
	
	def set_version(self):
		"""Auto-increment version for same document title"""
		if self.is_new():
			# Check for existing documents with same title
			existing_count = frappe.db.count("Patient Document", {
				"patient": self.patient,
				"document_title": self.document_title
			})
			if existing_count > 0:
				self.version = existing_count + 1
