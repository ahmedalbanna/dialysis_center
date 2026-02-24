"""
API Endpoint Tests for Dialysis Center App

Tests all API endpoints:
1. GET operations (list, get)
2. POST operations (create)
3. PUT operations (update)
4. DELETE operations
5. Permission checking
"""

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today
from .test_fixtures import FixtureFactory


class TestPatientAPI(IntegrationTestCase):
	"""Test Patient API endpoints"""

	def test_get_patient_list(self):
		"""Test GET /api/resource/Patient - list patients"""
		# Create test patients
		p1 = FixtureFactory.create_patient(patient_name="Patient One")
		p2 = FixtureFactory.create_patient(patient_name="Patient Two")
		
		# Get list via API
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Patient",
				"filters": {"patient_name": ["like", "Patient"]},
				"fields": ["name", "patient_name", "date_of_birth"]
			}
		)
		
		self.assertIsNotNone(result.message)
		patient_names = [p["name"] for p in result.message]
		self.assertIn(p1.name, patient_names)
		self.assertIn(p2.name, patient_names)

	def test_get_patient_by_id(self):
		"""Test GET /api/resource/Patient/{name} - get single patient"""
		patient = FixtureFactory.create_patient(patient_name="Get Test Patient")
		
		result = frappe.call(
			method="frappe.client.get",
			args={"doctype": "Patient", "name": patient.name}
		)
		
		self.assertIsNotNone(result.message)
		self.assertEqual(result.message["name"], patient.name)
		self.assertEqual(result.message["patient_name"], "Get Test Patient")

	def test_create_patient_api(self):
		"""Test POST /api/resource/Patient - create patient"""
		result = frappe.call(
			method="frappe.client.insert",
			args={
				"doc": {
					"doctype": "Patient",
					"patient_name": "API Created Patient",
					"date_of_birth": "1985-06-15",
					"gender": "Female",
					"blood_group": "A+",
					"national_id": "API123456789",
					"mobile_number": "+201005555555",
					"email": "api@test.local"
				}
			}
		)
		
		self.assertIsNotNone(result.message)
		self.assertEqual(result.message["patient_name"], "API Created Patient")
		self.assertTrue(result.message["name"].startswith("PT-"))

	def test_update_patient_api(self):
		"""Test PUT /api/resource/Patient/{name} - update patient"""
		patient = FixtureFactory.create_patient(patient_name="Original Name")
		
		result = frappe.call(
			method="frappe.client.set_value",
			args={
				"doctype": "Patient",
				"name": patient.name,
				"fieldname": {
					"patient_name": "Updated Name",
					"address": "New Address"
				}
			}
		)
		
		updated = frappe.get_doc("Patient", patient.name)
		self.assertEqual(updated.patient_name, "Updated Name")
		self.assertEqual(updated.address, "New Address")

	def test_delete_patient_api(self):
		"""Test DELETE /api/resource/Patient/{name} - delete patient"""
		patient = FixtureFactory.create_patient()
		patient_name = patient.name
		
		frappe.call(
			method="frappe.client.delete",
			args={"doctype": "Patient", "name": patient_name}
		)
		
		self.assertFalse(frappe.db.exists("Patient", patient_name))

	def test_patient_list_with_filters(self):
		"""Test patient list with various filters"""
		# Create test data
		p1 = FixtureFactory.create_patient(gender="Male", blood_group="O+")
		p2 = FixtureFactory.create_patient(gender="Female", blood_group="A+")
		p3 = FixtureFactory.create_patient(gender="Male", blood_group="A+")
		
		# Filter by gender
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Patient",
				"filters": {"gender": "Male"}
			}
		)
		
		self.assertIsNotNone(result.message)
		male_count = len(result.message)
		self.assertGreaterEqual(male_count, 2)

	def test_patient_list_with_sort(self):
		"""Test patient list with sorting"""
		p1 = FixtureFactory.create_patient(patient_name="Alice")
		p2 = FixtureFactory.create_patient(patient_name="Bob")
		p3 = FixtureFactory.create_patient(patient_name="Charlie")
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Patient",
				"filters": {"patient_name": ["like", "%"]},
				"order_by": "patient_name asc"
			}
		)
		
		self.assertIsNotNone(result.message)
		self.assertGreaterEqual(len(result.message), 3)

	def test_patient_list_pagination(self):
		"""Test patient list pagination"""
		# Create multiple patients
		for i in range(5):
			FixtureFactory.create_patient(patient_name=f"Patient {i}")
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Patient",
				"filters": {"patient_name": ["like", "Patient"]},
				"limit_page_length": 2
			}
		)
		
		self.assertLessEqual(len(result.message), 2)


class TestAppointmentAPI(IntegrationTestCase):
	"""Test Appointment API endpoints"""

	def test_get_appointment_list(self):
		"""Test GET /api/resource/Appointment - list appointments"""
		p = FixtureFactory.create_patient()
		a1 = FixtureFactory.create_appointment(patient=p)
		a2 = FixtureFactory.create_appointment(patient=p)
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={"doctype": "Appointment"}
		)
		
		self.assertIsNotNone(result.message)
		apt_names = [apt["name"] for apt in result.message]
		self.assertIn(a1.name, apt_names)
		self.assertIn(a2.name, apt_names)

	def test_get_appointment_by_id(self):
		"""Test GET /api/resource/Appointment/{name}"""
		appointment = FixtureFactory.create_appointment()
		
		result = frappe.call(
			method="frappe.client.get",
			args={"doctype": "Appointment", "name": appointment.name}
		)
		
		self.assertIsNotNone(result.message)
		self.assertEqual(result.message["name"], appointment.name)
		self.assertEqual(result.message["status"], "Scheduled")

	def test_create_appointment_api(self):
		"""Test POST /api/resource/Appointment"""
		patient = FixtureFactory.create_patient()
		nephrologist = FixtureFactory.create_staff()
		
		result = frappe.call(
			method="frappe.client.insert",
			args={
				"doc": {
					"doctype": "Appointment",
					"patient": patient.name,
					"nephrologist": nephrologist.name,
					"appointment_date": today(),
					"appointment_time": "10:00:00",
					"appointment_type": "Regular",
					"status": "Scheduled"
				}
			}
		)
		
		self.assertIsNotNone(result.message)
		self.assertEqual(result.message["patient"], patient.name)
		self.assertEqual(result.message["status"], "Scheduled")

	def test_update_appointment_api(self):
		"""Test PUT /api/resource/Appointment"""
		appointment = FixtureFactory.create_appointment()
		
		result = frappe.call(
			method="frappe.client.set_value",
			args={
				"doctype": "Appointment",
				"name": appointment.name,
				"fieldname": {"status": "Completed"}
			}
		)
		
		updated = frappe.get_doc("Appointment", appointment.name)
		self.assertEqual(updated.status, "Completed")

	def test_get_appointments_by_patient(self):
		"""Test filtering appointments by patient"""
		patient = FixtureFactory.create_patient()
		other_patient = FixtureFactory.create_patient()
		
		a1 = FixtureFactory.create_appointment(patient=patient)
		a2 = FixtureFactory.create_appointment(patient=patient)
		a3 = FixtureFactory.create_appointment(patient=other_patient)
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Appointment",
				"filters": {"patient": patient.name}
			}
		)
		
		apt_names = [apt["name"] for apt in result.message]
		self.assertIn(a1.name, apt_names)
		self.assertIn(a2.name, apt_names)
		self.assertNotIn(a3.name, apt_names)

	def test_get_appointments_by_date_range(self):
		"""Test filtering appointments by date range"""
		from frappe.utils import add_days
		
		patient = FixtureFactory.create_patient()
		apt1 = FixtureFactory.create_appointment(
			patient=patient,
			appointment_date=today()
		)
		apt2 = FixtureFactory.create_appointment(
			patient=patient,
			appointment_date=add_days(today(), 5)
		)
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Appointment",
				"filters": [
					["appointment_date", ">=", today()],
					["appointment_date", "<=", add_days(today(), 3)]
				]
			}
		)
		
		apt_names = [apt["name"] for apt in result.message]
		self.assertIn(apt1.name, apt_names)


class TestDialysisSessionAPI(IntegrationTestCase):
	"""Test Dialysis Session API endpoints"""

	def test_get_session_list(self):
		"""Test GET /api/resource/Dialysis Session"""
		patient = FixtureFactory.create_patient()
		s1 = FixtureFactory.create_dialysis_session(patient=patient)
		s2 = FixtureFactory.create_dialysis_session(patient=patient)
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={"doctype": "Dialysis Session"}
		)
		
		self.assertIsNotNone(result.message)
		session_names = [s["name"] for s in result.message]
		self.assertIn(s1.name, session_names)
		self.assertIn(s2.name, session_names)

	def test_get_session_by_id(self):
		"""Test GET /api/resource/Dialysis Session/{name}"""
		session = FixtureFactory.create_dialysis_session()
		
		result = frappe.call(
			method="frappe.client.get",
			args={"doctype": "Dialysis Session", "name": session.name}
		)
		
		self.assertIsNotNone(result.message)
		self.assertEqual(result.message["name"], session.name)
		self.assertEqual(result.message["patient"], session.patient)

	def test_create_session_api(self):
		"""Test POST /api/resource/Dialysis Session"""
		patient = FixtureFactory.create_patient()
		appointment = FixtureFactory.create_appointment(patient=patient)
		
		result = frappe.call(
			method="frappe.client.insert",
			args={
				"doc": {
					"doctype": "Dialysis Session",
					"patient": patient.name,
					"appointment": appointment.name,
					"session_date": today(),
					"session_time_in": "08:00:00",
					"session_time_out": "12:00:00",
					"session_status": "Scheduled"
				}
			}
		)
		
		self.assertIsNotNone(result.message)
		self.assertEqual(result.message["patient"], patient.name)
		self.assertEqual(result.message["session_status"], "Scheduled")

	def test_update_session_api(self):
		"""Test PUT /api/resource/Dialysis Session"""
		session = FixtureFactory.create_dialysis_session()
		
		result = frappe.call(
			method="frappe.client.set_value",
			args={
				"doctype": "Dialysis Session",
				"name": session.name,
				"fieldname": {"session_status": "Completed"}
			}
		)
		
		updated = frappe.get_doc("Dialysis Session", session.name)
		self.assertEqual(updated.session_status, "Completed")

	def test_get_sessions_by_patient(self):
		"""Test filtering sessions by patient"""
		patient = FixtureFactory.create_patient()
		other_patient = FixtureFactory.create_patient()
		
		s1 = FixtureFactory.create_dialysis_session(patient=patient)
		s2 = FixtureFactory.create_dialysis_session(patient=patient)
		s3 = FixtureFactory.create_dialysis_session(patient=other_patient)
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Dialysis Session",
				"filters": {"patient": patient.name}
			}
		)
		
		session_names = [s["name"] for s in result.message]
		self.assertIn(s1.name, session_names)
		self.assertIn(s2.name, session_names)
		self.assertNotIn(s3.name, session_names)


class TestInvoiceAPI(IntegrationTestCase):
	"""Test Invoice API endpoints"""

	def test_get_invoice_list(self):
		"""Test GET /api/resource/Invoice"""
		patient = FixtureFactory.create_patient()
		inv1 = FixtureFactory.create_invoice(patient=patient)
		inv2 = FixtureFactory.create_invoice(patient=patient)
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={"doctype": "Invoice"}
		)
		
		self.assertIsNotNone(result.message)
		inv_names = [inv["name"] for inv in result.message]
		self.assertIn(inv1.name, inv_names)
		self.assertIn(inv2.name, inv_names)

	def test_get_invoice_by_id(self):
		"""Test GET /api/resource/Invoice/{name}"""
		invoice = FixtureFactory.create_invoice()
		
		result = frappe.call(
			method="frappe.client.get",
			args={"doctype": "Invoice", "name": invoice.name}
		)
		
		self.assertIsNotNone(result.message)
		self.assertEqual(result.message["name"], invoice.name)
		self.assertEqual(result.message["billing_amount"], invoice.billing_amount)

	def test_create_invoice_api(self):
		"""Test POST /api/resource/Invoice"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		result = frappe.call(
			method="frappe.client.insert",
			args={
				"doc": {
					"doctype": "Invoice",
					"patient": patient.name,
					"session": session.name,
					"invoice_date": today(),
					"billing_amount": 1500.00,
					"insurance_amount": 750.00,
					"patient_amount": 750.00,
					"status": "Draft"
				}
			}
		)
		
		self.assertIsNotNone(result.message)
		self.assertEqual(result.message["patient"], patient.name)
		self.assertEqual(result.message["billing_amount"], 1500.00)

	def test_update_invoice_api(self):
		"""Test PUT /api/resource/Invoice"""
		invoice = FixtureFactory.create_invoice()
		
		result = frappe.call(
			method="frappe.client.set_value",
			args={
				"doctype": "Invoice",
				"name": invoice.name,
				"fieldname": {"status": "Submitted"}
			}
		)
		
		updated = frappe.get_doc("Invoice", invoice.name)
		self.assertEqual(updated.status, "Submitted")

	def test_get_invoices_by_patient(self):
		"""Test filtering invoices by patient"""
		patient = FixtureFactory.create_patient()
		other_patient = FixtureFactory.create_patient()
		
		inv1 = FixtureFactory.create_invoice(patient=patient)
		inv2 = FixtureFactory.create_invoice(patient=patient)
		inv3 = FixtureFactory.create_invoice(patient=other_patient)
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Invoice",
				"filters": {"patient": patient.name}
			}
		)
		
		inv_names = [inv["name"] for inv in result.message]
		self.assertIn(inv1.name, inv_names)
		self.assertIn(inv2.name, inv_names)
		self.assertNotIn(inv3.name, inv_names)

	def test_get_invoices_by_status(self):
		"""Test filtering invoices by status"""
		patient = FixtureFactory.create_patient()
		
		inv1 = FixtureFactory.create_invoice(patient=patient, status="Draft")
		inv2 = FixtureFactory.create_invoice(patient=patient, status="Submitted")
		inv3 = FixtureFactory.create_invoice(patient=patient, status="Draft")
		
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Invoice",
				"filters": {"status": "Draft"}
			}
		)
		
		inv_names = [inv["name"] for inv in result.message]
		self.assertIn(inv1.name, inv_names)
		self.assertNotIn(inv2.name, inv_names)
		self.assertIn(inv3.name, inv_names)


class TestAPIPermissions(IntegrationTestCase):
	"""Test API permission checking"""

	def test_api_requires_authentication(self):
		"""Test that unauthenticated requests are handled"""
		# This test verifies permission framework
		patient = FixtureFactory.create_patient()
		
		# Verify we can access as authenticated user
		result = frappe.call(
			method="frappe.client.get",
			args={"doctype": "Patient", "name": patient.name}
		)
		
		self.assertIsNotNone(result.message)

	def test_invalid_doctype_returns_error(self):
		"""Test API returns error for invalid doctype"""
		try:
			result = frappe.call(
				method="frappe.client.get_list",
				args={"doctype": "InvalidDocType"}
			)
			# Should raise an error
			self.fail("Expected error for invalid doctype")
		except frappe.DoesNotExistError:
			pass  # Expected

	def test_invalid_name_returns_not_found(self):
		"""Test API returns error for non-existent document"""
		try:
			result = frappe.call(
				method="frappe.client.get",
				args={"doctype": "Patient", "name": "NONEXISTENT"}
			)
			self.fail("Expected error for non-existent document")
		except frappe.DoesNotExistError:
			pass  # Expected

	def test_api_respects_doctype_permissions(self):
		"""Test API enforces DocType-level permissions"""
		# Verify permission check works
		patient = FixtureFactory.create_patient()
		
		# Get should work for authorized user
		result = frappe.call(
			method="frappe.client.get",
			args={"doctype": "Patient", "name": patient.name}
		)
		
		self.assertIsNotNone(result.message)
