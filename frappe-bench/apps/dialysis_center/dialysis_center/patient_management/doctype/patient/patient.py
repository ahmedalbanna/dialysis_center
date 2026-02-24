import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, nowdate
from frappe import _
import re

class Patient(Document):
	def validate(self):
		"""Validate patient data before saving"""
		self.validate_required_fields()
		self.validate_contact_info()
		self.calculate_age()
		self.set_default_status()
		self.validate_national_id()
		self.validate_dialysis_settings()
	
	def validate_required_fields(self):
		"""Validate required patient information"""
		if not self.patient_name:
			frappe.throw(_("Patient Name is required"))
		
		if not self.date_of_birth:
			frappe.throw(_("Date of Birth is required"))
		
		if not self.gender:
			frappe.throw(_("Gender is required"))
		
		# Blood group is critical for dialysis patients
		if not self.blood_group:
			frappe.throw(_("Blood Group is required for dialysis patients"))
		
		# Mobile number validation is handled by Frappe's Phone field type
		# Skip custom validation to allow field-level validation
	
	def validate_contact_info(self):
		"""Validate contact information"""
		# Validate email format
		if self.email:
			email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
			if not re.match(email_pattern, self.email):
				frappe.throw(_("Invalid email address format"))
		
		# Validate mobile number format (basic check)
		if self.mobile_number:
			# Remove common separators
			clean_number = self.mobile_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
			if not clean_number.startswith("+") and not clean_number.isdigit():
				frappe.msgprint(_("Warning: Mobile number format may be invalid"), 
					indicator="orange", alert=True)
	
	def calculate_age(self):
		"""Calculate age from date of birth"""
		if self.date_of_birth:
			from dateutil.relativedelta import relativedelta
			dob = getdate(self.date_of_birth)
			today_date = getdate(today())
			
			# Validate DOB is not in future
			if dob > today_date:
				frappe.throw(_("Date of Birth cannot be in the future"))
			
			age = relativedelta(today_date, dob).years
			self.age = age
			
			# Warning for very young or very old patients
			if age < 18:
				frappe.msgprint(_("Patient is under 18 years old"), indicator="orange", alert=True)
			elif age > 100:
				frappe.msgprint(_("Please verify patient age: {0} years").format(age), 
					indicator="orange", alert=True)
	
	def set_default_status(self):
		"""Set default status if not set"""
		if not self.status:
			self.status = "Active"
		
		if not self.registration_date:
			self.registration_date = nowdate()
	
	def validate_national_id(self):
		"""Validate national ID uniqueness"""
		if self.national_id:
			duplicate = frappe.db.exists("Patient", {
				"national_id": self.national_id,
				"name": ["!=", self.name or '']
			})
			if duplicate:
				frappe.throw(_("Patient with National ID {0} already exists: {1}").format(
					self.national_id, duplicate))
	
	def validate_dialysis_settings(self):
		"""Validate dialysis-specific settings"""
		if self.dry_weight and self.dry_weight <= 0:
			frappe.throw(_("Dry weight must be greater than 0"))
		
		if self.duration and self.duration <= 0:
			frappe.throw(_("Treatment duration must be greater than 0"))
		
		# Set default frequency if not set
		if not self.frequency and self.status == "Active":
			self.frequency = "3x per week"
	
	def before_save(self):
		"""Normalize patient data before saving"""
		# Trim whitespace from text fields
		if self.patient_name:
			self.patient_name = self.patient_name.strip()
		
		# Normalize email to lowercase
		if self.email:
			self.email = self.email.lower().strip()
		
		# Normalize phone number - remove common separators
		if self.mobile_number:
			self.mobile_number = self.mobile_number.strip()
	
	def on_update(self):
		"""Called after saving the document"""
		# Update patient name in related documents if changed
		if self.has_value_changed("patient_name"):
			self.update_patient_name_in_linked_docs()
		
		# Clear related caches for performance
		frappe.cache.delete_value(f"patient_{self.name}_summary")
		frappe.cache.delete_value(f"patient_{self.name}_sessions")
	
	def update_patient_name_in_linked_docs(self):
		"""Update patient name in linked documents"""
		# This could be optimized with background job for large datasets
		try:
			# Update appointments
			frappe.db.set_value("Appointment", {"patient": self.name}, "patient_name", self.patient_name)
			# Update sessions
			frappe.db.set_value("Dialysis Session", {"patient": self.name}, "patient_name", self.patient_name)
			# Update invoices
			frappe.db.set_value("Invoice", {"patient": self.name}, "patient_name", self.patient_name)
		except Exception as e:
			frappe.log_error(message=str(e), title="Patient Name Update Failed")
	
	def on_trash(self):
		"""Called before deleting the document"""
		# Check if patient has any active appointments or sessions
		active_appointments = frappe.db.count("Appointment", {
			"patient": self.name,
			"status": ["in", ["Scheduled", "Checked In"]]
		})
		
		if active_appointments > 0:
			frappe.throw(_("Cannot delete patient with {0} active appointment(s)").format(active_appointments))
		
		# Check for submitted sessions
		submitted_sessions = frappe.db.count("Dialysis Session", {
			"patient": self.name,
			"docstatus": 1
		})
		
		if submitted_sessions > 0:
			frappe.throw(_("Cannot delete patient with {0} submitted session(s)").format(submitted_sessions))

@frappe.whitelist()
def get_patient_summary(patient):
	"""Get patient summary including recent sessions and appointments"""
	if not patient:
		return {}
	
	patient_doc = frappe.get_doc("Patient", patient)
	
	# Get recent sessions
	recent_sessions = frappe.get_all("Dialysis Session",
		filters={"patient": patient},
		fields=["name", "session_date", "status"],
		order_by="session_date desc",
		limit=5
	)
	
	# Get upcoming appointments
	upcoming_appointments = frappe.get_all("Appointment",
		filters={
			"patient": patient,
			"appointment_date": [">=", nowdate()],
			"status": ["!=", "Cancelled"]
		},
		fields=["name", "appointment_date", "appointment_time"],
		order_by="appointment_date asc",
		limit=5
	)
	
	# Get outstanding invoices
	outstanding_invoices = frappe.get_all("Invoice",
		filters={
			"patient": patient,
			"payment_status": ["!=", "Paid"],
			"docstatus": 1
		},
		fields=["name", "invoice_date", "total_amount", "outstanding_amount"]
	)
	
	return {
		"patient": patient_doc.as_dict(),
		"recent_sessions": recent_sessions,
		"upcoming_appointments": upcoming_appointments,
		"outstanding_invoices": outstanding_invoices,
		"total_outstanding": sum([inv.outstanding_amount for inv in outstanding_invoices])
	}
