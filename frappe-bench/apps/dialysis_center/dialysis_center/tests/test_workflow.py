"""
Smoke tests for Dialysis Center App
Tests basic creation and workflow for core DocTypes
"""

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import nowdate, now_datetime, add_days

class TestDialysisCenterWorkflow(FrappeTestCase):
	"""Test complete workflow from patient registration to payment"""
	
	def setUp(self):
		"""Set up test data"""
		self.cleanup_test_data()
		self.create_test_machine()
	
	def tearDown(self):
		"""Clean up test data"""
		self.cleanup_test_data()
	
	def cleanup_test_data(self):
		"""Remove any existing test data"""
		# Delete in reverse dependency order
		for doctype in ["Payment", "Invoice", "Dialysis Session", "Appointment", 
						"Lab Test", "Stock Movement", "Patient", "Medication", "Dialysis Machine"]:
			frappe.db.sql(f"DELETE FROM `tab{doctype}` WHERE name LIKE 'TEST-%'")
		frappe.db.commit()
	
	def create_test_machine(self):
		"""Create test dialysis machine"""
		if not frappe.db.exists("Dialysis Machine", "TEST-MACHINE-001"):
			machine = frappe.get_doc({
				"doctype": "Dialysis Machine",
				"machine_id": "TEST-MACHINE-001",
				"machine_name": "Test Machine",
				"manufacturer": "Test Manufacturer",
				"model": "Test Model",
				"serial_number": "TEST001",
				"status": "Available",
				"location": "Test Station"
			})
			machine.insert(ignore_permissions=True)
			frappe.db.commit()
	
	def test_01_patient_creation(self):
		"""Test: Create a new patient"""
		patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": "TEST-Patient-001",
			"date_of_birth": "1970-01-01",
			"gender": "Male",
			"blood_group": "O+",
			"national_id": "TEST-ID-001",
			"mobile_number": "+15551234001",
			"status": "Active"
		})
		patient.insert()
		
		# Verify patient was created
		self.assertTrue(frappe.db.exists("Patient", patient.name))
		self.assertEqual(patient.status, "Active")
		self.assertIsNotNone(patient.age)
	
	def test_02_appointment_creation(self):
		"""Test: Create appointment for patient"""
		# Create patient first
		patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": "TEST-Patient-002",
			"date_of_birth": "1975-05-15",
			"gender": "Female",
			"national_id": "TEST-ID-002",
			"mobile_number": "+15551234002",
			"status": "Active"
		})
		patient.insert()
		
		# Create appointment
		appointment = frappe.get_doc({
			"doctype": "Appointment",
			"patient": patient.name,
			"appointment_date": nowdate(),
			"appointment_time": "10:00:00",
			"machine": "TEST-MACHINE-001",
			"duration": 240,
			"status": "Scheduled"
		})
		appointment.insert()
		
		# Verify appointment
		self.assertTrue(frappe.db.exists("Appointment", appointment.name))
		self.assertEqual(appointment.patient_name, patient.patient_name)
	
	def test_03_dialysis_session_workflow(self):
		"""Test: Complete dialysis session workflow"""
		# Create patient
		patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": "TEST-Patient-003",
			"date_of_birth": "1980-06-20",
			"gender": "Male",
			"national_id": "TEST-ID-003",
			"mobile_number": "+15551234003",
			"status": "Active",
			"dry_weight": 70
		})
		patient.insert()
		
		# Create session
		session = frappe.get_doc({
			"doctype": "Dialysis Session",
			"patient": patient.name,
			"session_date": nowdate(),
			"session_time": "08:00:00",
			"dialysis_machine": "TEST-MACHINE-001",
			"treatment_duration": 240,
			"pre_dialysis_weight": 72.5,
			"post_dialysis_weight": 70.0,
			"pre_systolic_bp": 140,
			"pre_diastolic_bp": 90,
			"post_systolic_bp": 120,
			"post_diastolic_bp": 80,
			"started_at": now_datetime(),
			"completed_at": now_datetime(),
			"status": "Completed"
		})
		session.insert()
		
		# Verify calculations
		self.assertEqual(session.weight_loss, 2.5)
		
		# Submit session
		session.submit()
		self.assertEqual(session.docstatus, 1)
	
	def test_04_invoice_and_payment_workflow(self):
		"""Test: Create invoice and record payment"""
		# Create patient
		patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": "TEST-Patient-004",
			"date_of_birth": "1985-03-10",
			"gender": "Female",
			"national_id": "TEST-ID-004",
			"mobile_number": "+15551234004",
			"status": "Active"
		})
		patient.insert()
		
		# Create invoice
		invoice = frappe.get_doc({
			"doctype": "Invoice",
			"patient": patient.name,
			"invoice_date": nowdate(),
			"items": [{
				"description": "Dialysis Session",
				"quantity": 1,
				"rate": 500.00
			}]
		})
		invoice.insert()
		
		# Verify calculations
		self.assertEqual(invoice.subtotal, 500.00)
		self.assertEqual(invoice.total_amount, 500.00)
		self.assertEqual(invoice.payment_status, "Unpaid")
		
		# Submit invoice
		invoice.submit()
		
		# Create payment
		payment = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": patient.name,
			"amount": 500.00,
			"payment_method": "Cash",
			"payment_date": nowdate()
		})
		payment.insert()
		payment.submit()
		
		# Verify invoice is paid
		invoice.reload()
		self.assertEqual(invoice.payment_status, "Paid")
		self.assertEqual(invoice.outstanding_amount, 0)
	
	def test_05_stock_movement(self):
		"""Test: Stock movement workflow"""
		# Create medication
		medication = frappe.get_doc({
			"doctype": "Medication",
			"medication_name": "TEST-Medication",
			"current_stock": 100,
			"reorder_level": 20,
			"minimum_stock": 10
		})
		medication.insert()
		
		# Create stock issue
		movement = frappe.get_doc({
			"doctype": "Stock Movement",
			"medication": medication.name,
			"movement_type": "Issue",
			"quantity": 10,
			"movement_date": nowdate()
		})
		movement.insert()
		movement.submit()
		
		# Verify stock updated
		medication.reload()
		self.assertEqual(medication.current_stock, 90)
	
	def test_06_lab_test_workflow(self):
		"""Test: Lab test creation and submission"""
		# Create patient
		patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": "TEST-Patient-006",
			"date_of_birth": "1990-08-15",
			"gender": "Male",
			"national_id": "TEST-ID-006",
			"mobile_number": "+15551234006",
			"status": "Active"
		})
		patient.insert()
		
		# Create lab test
		lab_test = frappe.get_doc({
			"doctype": "Lab Test",
			"patient": patient.name,
			"test_name": "Blood Test",
			"test_date": nowdate(),
			"results": [{
				"test_parameter": "Hemoglobin",
				"result_value": 12.5,
				"unit": "g/dL",
				"normal_range_min": 12.0,
				"normal_range_max": 16.0
			}]
		})
		lab_test.insert()
		
		# Submit lab test
		lab_test.submit()
		
		# Verify lab results created
		self.assertTrue(frappe.db.exists("Lab Result", {"lab_test": lab_test.name}))


def run_smoke_tests():
	"""Run all smoke tests and return results"""
	import unittest
	
	# Create test suite
	suite = unittest.TestLoader().loadTestsFromTestCase(TestDialysisCenterWorkflow)
	
	# Run tests
	runner = unittest.TextTestRunner(verbosity=2)
	result = runner.run(suite)
	
	return result.wasSuccessful()
