import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today, add_days

class TestAppointment(IntegrationTestCase):
	def setUp(self):
		"""Setup test data"""
		# Create a test patient if not exists
		if not frappe.db.exists("Patient", {"national_id": "TEST123"}):
			self.patient = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Test Patient",
				"date_of_birth": "1980-01-01",
				"gender": "Male",
				"national_id": "TEST123",
				"mobile_number": "+1234567890",
				"status": "Active"
			}).insert()
		else:
			self.patient = frappe.get_doc("Patient", {"national_id": "TEST123"})
	
	def test_appointment_creation(self):
		"""Test appointment can be created"""
		appointment = frappe.get_doc({
			"doctype": "Appointment",
			"patient": self.patient.name,
			"appointment_date": today(),
			"appointment_time": "08:00:00",
			"duration": 240,
			"status": "Scheduled"
		})
		appointment.insert()
		self.assertEqual(appointment.status, "Scheduled")
		appointment.delete()
	
	def test_patient_double_booking(self):
		"""Test patient cannot have multiple appointments on same day"""
		apt1 = frappe.get_doc({
			"doctype": "Appointment",
			"patient": self.patient.name,
			"appointment_date": add_days(today(), 1),
			"appointment_time": "08:00:00",
			"status": "Scheduled"
		}).insert()
		
		with self.assertRaises(frappe.ValidationError):
			apt2 = frappe.get_doc({
				"doctype": "Appointment",
				"patient": self.patient.name,
				"appointment_date": add_days(today(), 1),
				"appointment_time": "14:00:00",
				"status": "Scheduled"
			}).insert()
		
		apt1.delete()
