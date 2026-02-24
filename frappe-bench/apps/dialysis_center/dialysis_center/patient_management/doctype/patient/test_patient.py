import frappe
from frappe.tests import IntegrationTestCase

class TestPatient(IntegrationTestCase):
	def setUp(self):
		"""Setup test data"""
		self.test_patient_data = {
			"doctype": "Patient",
			"patient_name": "Test Patient",
			"date_of_birth": "1980-01-01",
			"gender": "Male",
			"blood_group": "O+",
			"national_id": "1234567890",
			"mobile_number": "+1234567890",
			"email": "test@patient.com"
		}
	
	def test_patient_creation(self):
		"""Test patient can be created"""
		patient = frappe.get_doc(self.test_patient_data)
		patient.insert()
		self.assertEqual(patient.patient_name, "Test Patient")
		patient.delete()
	
	def test_patient_id_generation(self):
		"""Test patient ID auto-generation"""
		patient = frappe.get_doc(self.test_patient_data)
		patient.insert()
		self.assertTrue(patient.name.startswith("PT-"))
		patient.delete()
	
	def test_age_calculation(self):
		"""Test age calculation from DOB"""
		patient = frappe.get_doc(self.test_patient_data)
		patient.insert()
		self.assertGreater(patient.age, 40)
		patient.delete()
