import frappe
from frappe.utils import now_datetime, add_days, random_string
import random


class AppointmentFactory:
	"""Factory for creating test appointments"""

	@staticmethod
	def create(patient=None, machine=None, **kwargs):
		"""Create a single appointment"""

		if not patient:
			from dialysis_center.tests.factories.patient_factory import PatientFactory
			patient = PatientFactory.create()

		if not machine:
			machine = AppointmentFactory._get_or_create_machine()

		if not kwargs.get("staff"):
			kwargs["staff"] = AppointmentFactory._get_or_create_staff()

		appointment_date = kwargs.get("appointment_date", add_days(now_datetime(), random.randint(1, 30)))

		appointment_data = {
			"doctype": "Appointment",
			"patient": patient.name if hasattr(patient, 'name') else patient,
			"appointment_date": appointment_date,
			"appointment_time": kwargs.get("appointment_time", "09:00:00"),
			"duration": kwargs.get("duration", 240),  # 4 hours
			"machine": machine,
			"staff": kwargs.get("staff"),
			"shift": kwargs.get("shift", "Morning"),
			"status": kwargs.get("status", "Scheduled"),
			"notes": kwargs.get("notes", "Test appointment"),
		}

		appointment = frappe.get_doc(appointment_data)
		appointment.insert(ignore_permissions=True)
		frappe.db.commit()

		return appointment

	@staticmethod
	def create_batch(count=10, patient=None, **kwargs):
		"""Create multiple appointments"""
		appointments = []
		for i in range(count):
			appointment = AppointmentFactory.create(patient=patient, **kwargs)
			appointments.append(appointment)
		return appointments

	@staticmethod
	def _get_or_create_machine():
		"""Get existing machine or create one"""
		machine = frappe.db.get_value("Dialysis Machine", {"status": "Available"}, "name")
		if machine:
			return machine

		# Create a test machine
		machine_doc = frappe.get_doc({
			"doctype": "Dialysis Machine",
			"machine_id": f"MCH-TEST-{random_string(3)}",
			"machine_name": f"Test Machine {random_string(3)}",
			"manufacturer": "Fresenius",
			"model": "5008S",
			"status": "Available",
			"location": "Main Floor"
		})
		machine_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return machine_doc.name

	@staticmethod
	def _get_or_create_staff():
		"""Get existing staff or create one"""
		staff = frappe.db.get_value("Healthcare Practitioner", {"practitioner_type": "Nurse"}, "name")
		if staff:
			return staff

		# Create a test staff member
		staff_doc = frappe.get_doc({
			"doctype": "Healthcare Practitioner",
			"first_name": "Test",
			"last_name": "Nurse",
			"practitioner_type": "Nurse",
			"gender": "Female"
		})
		staff_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return staff_doc.name
