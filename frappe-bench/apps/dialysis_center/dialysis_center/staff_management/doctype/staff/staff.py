import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, date_diff
from frappe import _
import re

class Staff(Document):
	def validate(self):
		self.validate_required_fields()
		self.validate_staff_id_uniqueness()
		self.validate_contact_info()
		self.validate_license_expiry()
		self.validate_employment_dates()
		self.set_status()
	
	def validate_staff_id_uniqueness(self):
		"""Validate staff ID is unique"""
		if self.staff_id:
			duplicate = frappe.db.exists("Staff", {
				"staff_id": self.staff_id,
				"name": ["!=", self.name or '']
			})
			if duplicate:
				frappe.throw(_("Staff ID {0} already exists").format(self.staff_id))
	
	def validate_required_fields(self):
		"""Validate required staff information"""
		if not self.staff_name:
			frappe.throw(_("Staff Name is required"))
		
		if not self.staff_type:
			frappe.throw(_("Staff Type is required"))
	
	def validate_contact_info(self):
		"""Validate contact information"""
		if self.email:
			email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
			if not re.match(email_pattern, self.email):
				frappe.throw(_("Invalid email address format"))
	
	def validate_license_expiry(self):
		"""Check license expiry for licensed professionals"""
		if self.license_number and self.license_expiry:
			days_to_expiry = date_diff(self.license_expiry, nowdate())
			
			if days_to_expiry < 0:
				frappe.msgprint(_("CRITICAL: Professional license has EXPIRED on {0}").format(
					self.license_expiry), indicator="red", alert=True)
				# Auto-set status to inactive for expired license
				if self.status == "Active":
					frappe.msgprint(_("Staff status should be set to Inactive due to expired license"),
						indicator="red", alert=True)
			elif days_to_expiry <= 30:
				frappe.msgprint(_("Warning: License will expire in {0} days on {1}").format(
					days_to_expiry, self.license_expiry), indicator="orange", alert=True)
	
	def validate_employment_dates(self):
		"""Validate employment dates"""
		if hasattr(self, 'date_of_joining') and self.date_of_joining:
			if getdate(self.date_of_joining) > getdate(nowdate()):
				frappe.throw(_("Date of Joining cannot be in the future"))
		
		if hasattr(self, 'date_of_leaving') and self.date_of_leaving:
			if hasattr(self, 'date_of_joining') and self.date_of_joining:
				if getdate(self.date_of_leaving) < getdate(self.date_of_joining):
					frappe.throw(_("Date of Leaving cannot be before Date of Joining"))
	
	def set_status(self):
		"""Auto-set status based on dates"""
		if not self.status:
			self.status = "Active"
		
		# Auto-inactive if left
		if hasattr(self, 'date_of_leaving') and self.date_of_leaving:
			if getdate(self.date_of_leaving) <= getdate(nowdate()):
				if self.status == "Active":
					frappe.msgprint(_("Staff has left on {0}. Status should be Inactive").format(
						self.date_of_leaving), indicator="orange", alert=True)
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from text fields
		if self.staff_name:
			self.staff_name = self.staff_name.strip()
		
		# Normalize email to lowercase
		if self.email:
			self.email = self.email.lower().strip()
		
		# Normalize phone number
		if self.phone_number:
			self.phone_number = self.phone_number.strip()
		
		# Normalize staff ID
		if self.staff_id:
			self.staff_id = self.staff_id.strip().upper()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"staff_{self.name}")
		frappe.cache.delete_value("staff_list")
