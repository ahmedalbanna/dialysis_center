import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime, getdate, add_to_date, time_diff_in_hours
from frappe import _

class Appointment(Document):
	def validate(self):
		"""Validate appointment data"""
		self.validate_patient_status()
		self.validate_machine_availability()
		self.validate_patient_double_booking()
		self.validate_staff_availability()
		self.validate_appointment_date()
		self.set_default_duration()
		self.set_patient_name()
	
	def validate_patient_status(self):
		"""Ensure patient is active"""
		if self.patient:
			patient = frappe.get_doc("Patient", self.patient)
			if patient.status != "Active":
				frappe.throw(_("Cannot create appointment for inactive patient: {0}").format(self.patient))
	
	def validate_machine_availability(self):
		"""Check if machine is available at the scheduled time"""
		if not self.machine or not self.appointment_date or not self.appointment_time:
			return
		
		# Validate machine exists and is available
		machine_status = frappe.db.get_value("Dialysis Machine", self.machine, "status")
		if machine_status == "Maintenance":
			frappe.msgprint(_("Warning: Machine {0} is currently under maintenance").format(self.machine),
				indicator="orange", alert=True)
		elif machine_status == "Out of Service":
			frappe.throw(_("Machine {0} is out of service").format(self.machine))
		
		# Check for overlapping appointments on the same machine
		overlapping = frappe.db.sql("""
			SELECT name 
			FROM `tabAppointment`
			WHERE machine = %s 
			AND appointment_date = %s
			AND name != %s
			AND status NOT IN ('Cancelled', 'Completed')
			AND (
				(appointment_time <= %s AND DATE_ADD(appointment_time, INTERVAL duration MINUTE) > %s)
				OR (appointment_time < DATE_ADD(%s, INTERVAL %s MINUTE) AND appointment_time >= %s)
			)
		""", (self.machine, self.appointment_date, self.name or '', 
			  self.appointment_time, self.appointment_time,
			  self.appointment_time, self.duration or 240, self.appointment_time))
		
		if overlapping:
			frappe.throw(_("Machine {0} is not available at the selected time").format(self.machine))
	
	def validate_patient_double_booking(self):
		"""Ensure patient doesn't have overlapping appointments"""
		if not self.patient or not self.appointment_date:
			return
		
		overlapping = frappe.db.count("Appointment", {
			"patient": self.patient,
			"appointment_date": self.appointment_date,
			"name": ["!=", self.name or ''],
			"status": ["not in", ["Cancelled", "Completed"]]
		})
		
		if overlapping > 0:
			frappe.throw(_("Patient {0} already has an appointment on {1}").format(
				self.patient, self.appointment_date))
	
	def validate_staff_availability(self):
		"""Check if assigned staff is available"""
		if not self.assigned_staff or not self.appointment_date:
			return
		
		# Check if staff has conflicting appointments
		conflicting = frappe.db.count("Appointment", {
			"assigned_staff": self.assigned_staff,
			"appointment_date": self.appointment_date,
			"appointment_time": self.appointment_time,
			"name": ["!=", self.name or ''],
			"status": ["not in", ["Cancelled", "Completed"]]
		})
		
		if conflicting > 0:
			frappe.msgprint(_("Warning: Staff {0} has another appointment at this time").format(
				self.assigned_staff), indicator="orange", alert=True)
	
	def validate_appointment_date(self):
		"""Validate appointment is not in the past"""
		if self.appointment_date and getdate(self.appointment_date) < getdate():
			if not self.is_new():
				# Allow past dates for existing appointments (rescheduling)
				pass
			else:
				frappe.throw(_("Cannot create appointment in the past"))
	
	def set_default_duration(self):
		"""Set default duration based on patient's treatment plan"""
		if not self.duration and self.patient:
			patient = frappe.get_doc("Patient", self.patient)
			self.duration = patient.duration or 240  # Default 4 hours
	
	def set_patient_name(self):
		"""Auto-fetch patient name"""
		if self.patient and not self.patient_name:
			self.patient_name = frappe.db.get_value("Patient", self.patient, "patient_name")
	
	def before_save(self):
		"""Normalize data and set appointment end time"""
		# Trim whitespace from notes
		if self.notes:
			self.notes = self.notes.strip()
		
		# Set appointment end time
		if self.appointment_time and self.duration:
			from datetime import datetime, timedelta
			# Calculate end time
			time_obj = datetime.strptime(str(self.appointment_time), "%H:%M:%S")
			end_time = time_obj + timedelta(minutes=self.duration)
			self.appointment_end_time = end_time.strftime("%H:%M:%S")
		
		# Normalize patient name
		if self.patient_name:
			self.patient_name = self.patient_name.strip()
	
	def on_update(self):
		"""Called after saving"""
		if self.status == "Checked In" and not self.checked_in_time:
			self.db_set("checked_in_time", now_datetime())
		
		if self.status == "Completed" and not self.completed_time:
			self.db_set("completed_time", now_datetime())
		
		# Clear related caches
		frappe.cache.delete_value(f"appointment_{self.name}")
		frappe.cache.delete_value(f"patient_{self.patient}_appointments")
		frappe.cache.delete_value(f"machine_{self.machine}_schedule")
	
	def on_submit(self):
		"""Called when appointment is submitted - create session if applicable"""
		# Auto-create dialysis session if patient is checked in
		if self.status == "Checked In":
			try:
				self.create_session_on_checkin()
			except Exception as e:
				frappe.log_error(message=str(e), title="Auto Session Creation Failed")
	
	def on_cancel(self):
		"""Called when appointment is cancelled"""
		self.db_set("status", "Cancelled")
		self.add_comment("Comment", _("Appointment cancelled"))
		
		# Clear caches
		frappe.cache.delete_value(f"appointment_{self.name}")
		frappe.cache.delete_value(f"patient_{self.patient}_appointments")
	
	def create_session_on_checkin(self):
		"""Helper method to auto-create session when patient checks in"""
		# Only create if not already created
		existing = frappe.db.exists("Dialysis Session", {
			"appointment": self.name,
			"patient": self.patient
		})
		
		if not existing:
			self.create_session()
	
	def create_session(self):
		"""Create dialysis session from appointment"""
		if self.status != "Checked In":
			frappe.throw(_("Patient must be checked in before creating session"))
		
		# Check if session already exists
		existing = frappe.db.exists("Dialysis Session", {
			"patient": self.patient,
			"session_date": self.appointment_date,
			"appointment": self.name
		})
		
		if existing:
			frappe.throw(_("Session already created for this appointment"))
		
		# Create new session
		session = frappe.get_doc({
			"doctype": "Dialysis Session",
			"patient": self.patient,
			"patient_name": self.patient_name,
			"session_date": self.appointment_date,
			"session_time": self.appointment_time,
			"dialysis_machine": self.machine,
			"treatment_duration": self.duration,
			"appointment": self.name,
			"status": "Scheduled"
		})
		session.insert(ignore_permissions=True)
		
		# Update appointment status
		self.db_set("status", "In Progress")
		
		return session.name

@frappe.whitelist()
def check_in_appointment(appointment):
	"""Check in a patient for their appointment"""
	doc = frappe.get_doc("Appointment", appointment)
	doc.status = "Checked In"
	doc.checked_in_time = now_datetime()
	doc.save()
	return doc

@frappe.whitelist()
def get_available_slots(date, machine=None):
	"""Get available time slots for a given date and machine"""
	# This would return available time slots based on existing appointments
	# Implementation depends on your business logic
	slots = []
	
	# Example: 3 shifts per day
	shifts = [
		{"time": "08:00:00", "label": "Morning Shift (8:00 AM)"},
		{"time": "14:00:00", "label": "Afternoon Shift (2:00 PM)"},
		{"time": "20:00:00", "label": "Evening Shift (8:00 PM)"}
	]
	
	return slots
