import frappe
from frappe.model.document import Document
from frappe import _
import re

class InsuranceProvider(Document):
	def validate(self):
		"""Validate insurance provider details"""
		self.validate_provider_details()
		self.validate_contact_info()
	
	def validate_provider_details(self):
		"""Validate provider details are complete"""
		if not self.provider_name:
			frappe.throw(_("Provider Name is required"))
		
		if not self.provider_code:
			frappe.throw(_("Provider Code is required"))
	
	def validate_contact_info(self):
		"""Validate contact information"""
		if self.email:
			email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
			if not re.match(email_pattern, self.email):
				frappe.throw(_("Invalid email address format"))
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from text fields
		if self.provider_name:
			self.provider_name = self.provider_name.strip()
		
		if self.provider_code:
			self.provider_code = self.provider_code.strip().upper()
		
		# Normalize email to lowercase
		if self.email:
			self.email = self.email.lower().strip()
		
		if self.phone_number:
			self.phone_number = self.phone_number.strip()
		
		if self.address:
			self.address = self.address.strip()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"insurance_provider_{self.name}")
		frappe.cache.delete_value("insurance_providers_list")
