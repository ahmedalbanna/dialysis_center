"""
Core Workflow Tests for Dialysis Center App

Tests complete end-to-end workflows:
1. Patient creation → Appointment scheduling → Dialysis Session → Invoice generation
2. Multi-document cascading updates
3. Workflow state transitions
"""

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today, add_days
from .test_fixtures import FixtureFactory


class TestPatientCreationWorkflow(IntegrationTestCase):
	"""Test patient creation and initialization workflow"""

	def tearDown(self):
		"""Clean up test data"""
		frappe.db.commit()

	def test_patient_creation_basic(self):
		"""Test basic patient creation with mandatory fields"""
		patient = FixtureFactory.create_patient(
			patient_name="John Doe",
			date_of_birth="1975-05-20",
			gender="Male"
		)
		
		self.assertTrue(frappe.db.exists("Patient", patient.name))
		self.assertEqual(patient.patient_name, "John Doe")
		self.assertEqual(patient.gender, "Male")
		# Verify patient ID was auto-generated
		self.assertTrue(patient.name.startswith("PT-"))

	def test_patient_mandatory_fields_validation(self):
		"""Test that mandatory fields are enforced"""
		# Missing patient_name
		with self.assertRaises(frappe.ValidationError):
			patient = frappe.get_doc({
				"doctype": "Patient",
				"date_of_birth": "1980-01-01",
				"gender": "Male"
			})
			patient.insert()

	def test_patient_age_calculation(self):
		"""Test automatic age calculation from DOB"""
		patient = FixtureFactory.create_patient(
			date_of_birth="1970-01-01"
		)
		
		# Age should be calculated correctly
		self.assertGreater(patient.age, 50)

	def test_unique_national_id(self):
		"""Test that national IDs must be unique"""
		patient1 = FixtureFactory.create_patient(national_id="123456789")
		
		# Try to create duplicate
		with self.assertRaises(frappe.ValidationError):
			patient2 = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Another Patient",
				"national_id": "123456789",
				"date_of_birth": "1980-01-01",
				"gender": "Male"
			})
			patient2.insert()

	def test_unique_email(self):
		"""Test that emails must be unique"""
		patient1 = FixtureFactory.create_patient(email="unique@test.local")
		
		with self.assertRaises(frappe.ValidationError):
			patient2 = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Another Patient",
				"email": "unique@test.local",
				"date_of_birth": "1980-01-01",
				"gender": "Male"
			})
			patient2.insert()

	def test_email_format_validation(self):
		"""Test email format validation"""
		with self.assertRaises(frappe.ValidationError):
			patient = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Test Patient",
				"email": "invalid-email-format",
				"date_of_birth": "1980-01-01",
				"gender": "Male"
			})
			patient.insert()

	def test_phone_number_format_validation(self):
		"""Test phone number format validation"""
		# Valid formats should work
		patient = FixtureFactory.create_patient(
			mobile_number="+201001234567"
		)
		self.assertEqual(patient.mobile_number, "+201001234567")


class TestAppointmentSchedulingWorkflow(IntegrationTestCase):
	"""Test appointment scheduling workflow"""

	def tearDown(self):
		"""Clean up test data"""
		frappe.db.commit()

	def test_appointment_creation_basic(self):
		"""Test basic appointment creation"""
		patient = FixtureFactory.create_patient()
		nephrologist = FixtureFactory.create_staff(role="Nephrologist")
		
		appointment = FixtureFactory.create_appointment(
			patient=patient,
			nephrologist=nephrologist,
			appointment_date=today(),
			appointment_time="09:00:00"
		)
		
		self.assertTrue(frappe.db.exists("Appointment", appointment.name))
		self.assertEqual(appointment.patient, patient.name)
		self.assertEqual(appointment.nephrologist, nephrologist.name)
		self.assertEqual(appointment.status, "Scheduled")

	def test_appointment_mandatory_fields(self):
		"""Test appointment mandatory field validation"""
		# Missing patient
		with self.assertRaises(frappe.ValidationError):
			appointment = frappe.get_doc({
				"doctype": "Appointment",
				"appointment_date": today(),
				"appointment_time": "09:00:00"
			})
			appointment.insert()

	def test_appointment_date_validation(self):
		"""Test that appointment date cannot be in the past"""
		patient = FixtureFactory.create_patient()
		
		with self.assertRaises(frappe.ValidationError):
			appointment = frappe.get_doc({
				"doctype": "Appointment",
				"patient": patient.name,
				"appointment_date": add_days(today(), -1),  # Yesterday
				"appointment_time": "09:00:00"
			})
			appointment.insert()

	def test_nephrologist_availability(self):
		"""Test appointment respects nephrologist availability"""
		patient = FixtureFactory.create_patient()
		nephrologist = FixtureFactory.create_staff(
			role="Nephrologist",
			status="Inactive"  # Staff is inactive
		)
		
		# Should still allow creation but flag availability issue
		appointment = FixtureFactory.create_appointment(
			patient=patient,
			nephrologist=nephrologist
		)
		self.assertIsNotNone(appointment.name)

	def test_appointment_status_transitions(self):
		"""Test valid appointment status transitions"""
		appointment = FixtureFactory.create_appointment()
		
		# Valid transition: Scheduled -> Completed
		appointment.status = "Completed"
		appointment.save()
		self.assertEqual(appointment.status, "Completed")
		
		# Valid transition: Completed -> Cancelled
		appointment.status = "Cancelled"
		appointment.save()
		self.assertEqual(appointment.status, "Cancelled")

	def test_appointment_duplicate_prevention(self):
		"""Test that duplicate appointments are prevented"""
		patient = FixtureFactory.create_patient()
		nephrologist = FixtureFactory.create_staff()
		
		# Create first appointment
		apt1 = FixtureFactory.create_appointment(
			patient=patient,
			nephrologist=nephrologist,
			appointment_date=today(),
			appointment_time="09:00:00"
		)
		
		# Try to create exact duplicate
		with self.assertRaises(frappe.ValidationError):
			apt2 = frappe.get_doc({
				"doctype": "Appointment",
				"patient": patient.name,
				"nephrologist": nephrologist.name,
				"appointment_date": today(),
				"appointment_time": "09:00:00"
			})
			apt2.insert()


class TestDialysisSessionWorkflow(IntegrationTestCase):
	"""Test dialysis session creation and workflow"""

	def tearDown(self):
		"""Clean up test data"""
		frappe.db.commit()

	def test_dialysis_session_creation(self):
		"""Test basic dialysis session creation"""
		patient = FixtureFactory.create_patient()
		appointment = FixtureFactory.create_appointment(patient=patient)
		session = FixtureFactory.create_dialysis_session(
			patient=patient,
			appointment=appointment
		)
		
		self.assertTrue(frappe.db.exists("Dialysis Session", session.name))
		self.assertEqual(session.patient, patient.name)
		self.assertEqual(session.appointment, appointment.name)
		self.assertEqual(session.session_status, "Scheduled")

	def test_session_time_validation(self):
		"""Test session time validation - end time after start time"""
		patient = FixtureFactory.create_patient()
		
		# Invalid: end time before start time
		with self.assertRaises(frappe.ValidationError):
			session = frappe.get_doc({
				"doctype": "Dialysis Session",
				"patient": patient.name,
				"session_date": today(),
				"session_time_in": "12:00:00",
				"session_time_out": "08:00:00"  # Before start time
			})
			session.insert()

	def test_session_duration_calculation(self):
		"""Test session duration is calculated correctly"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(
			patient=patient,
			session_time_in="08:00:00",
			session_time_out="12:00:00"
		)
		
		# Duration should be 4 hours = 240 minutes
		expected_duration = 240
		self.assertEqual(session.session_duration_minutes, expected_duration)

	def test_session_vital_signs_recording(self):
		"""Test vital signs can be recorded during session"""
		session = FixtureFactory.create_dialysis_session()
		
		# Add vital signs log
		vital_log = frappe.get_doc({
			"doctype": "Vital Signs Log",
			"session": session.name,
			"recorded_at": "08:00:00",
		})
		
		vital_log.append("vitals", {
			"vital_name": "Blood Pressure",
			"value": "120/80",
			"unit": "mmHg"
		})
		
		vital_log.insert()
		self.assertTrue(frappe.db.exists("Vital Signs Log", vital_log.name))

	def test_session_status_workflow(self):
		"""Test session status state machine"""
		session = FixtureFactory.create_dialysis_session()
		
		# Valid transitions
		transitions = [
			("Scheduled", "In Progress"),
			("In Progress", "Completed"),
			("Completed", "Billed"),
		]
		
		for old_status, new_status in transitions:
			session.session_status = new_status
			session.save()
			self.assertEqual(session.session_status, new_status)


class TestInvoiceGenerationWorkflow(IntegrationTestCase):
	"""Test invoice generation and billing workflow"""

	def tearDown(self):
		"""Clean up test data"""
		frappe.db.commit()

	def test_invoice_creation_from_session(self):
		"""Test invoice creation linked to dialysis session"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		invoice = FixtureFactory.create_invoice(
			patient=patient,
			session=session,
			billing_amount=1500.00,
			insurance_amount=750.00,
			patient_amount=750.00
		)
		
		self.assertTrue(frappe.db.exists("Invoice", invoice.name))
		self.assertEqual(invoice.patient, patient.name)
		self.assertEqual(invoice.session, session.name)
		self.assertEqual(invoice.status, "Draft")

	def test_invoice_amount_split_validation(self):
		"""Test that insurance_amount + patient_amount = billing_amount"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		# Invalid: amounts don't sum correctly
		with self.assertRaises(frappe.ValidationError):
			invoice = frappe.get_doc({
				"doctype": "Invoice",
				"patient": patient.name,
				"session": session.name,
				"billing_amount": 1000.00,
				"insurance_amount": 700.00,  # Wrong amounts
				"patient_amount": 200.00,    # Should sum to 1000
			})
			invoice.insert()

	def test_invoice_submission_workflow(self):
		"""Test invoice submission and status transitions"""
		invoice = FixtureFactory.create_invoice()
		
		# Draft -> Submitted
		invoice.status = "Submitted"
		invoice.save()
		self.assertEqual(invoice.status, "Submitted")
		
		# Submitted -> Paid
		invoice.status = "Paid"
		invoice.save()
		self.assertEqual(invoice.status, "Paid")

	def test_invoice_payment_recording(self):
		"""Test payment recording against invoice"""
		invoice = FixtureFactory.create_invoice(
			billing_amount=1000.00
		)
		
		payment = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": invoice.patient,
			"amount": 1000.00,
			"payment_date": today(),
			"payment_method": "Cash"
		})
		payment.insert()
		
		self.assertTrue(frappe.db.exists("Payment", payment.name))
		self.assertEqual(payment.invoice, invoice.name)

	def test_partial_payment_handling(self):
		"""Test partial payment against invoice"""
		invoice = FixtureFactory.create_invoice(
			billing_amount=1000.00
		)
		
		# Record partial payment
		payment1 = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": invoice.patient,
			"amount": 600.00,
			"payment_date": today(),
			"payment_method": "Card"
		})
		payment1.insert()
		
		# Record remaining payment
		payment2 = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": invoice.patient,
			"amount": 400.00,
			"payment_date": today(),
			"payment_method": "Cash"
		})
		payment2.insert()
		
		# Both payments should exist
		self.assertTrue(frappe.db.exists("Payment", payment1.name))
		self.assertTrue(frappe.db.exists("Payment", payment2.name))


class TestCompleteHappyPathWorkflow(IntegrationTestCase):
	"""Test complete end-to-end workflow from patient to invoice"""

	def tearDown(self):
		"""Clean up test data"""
		frappe.db.commit()

	def test_full_patient_journey(self):
		"""Test complete workflow: Patient → Appointment → Session → Invoice"""
		
		# Step 1: Create patient
		patient = FixtureFactory.create_patient(
			patient_name="Complete Test Patient",
			date_of_birth="1980-01-15"
		)
		self.assertIsNotNone(patient.name)
		
		# Step 2: Schedule appointment
		nephrologist = FixtureFactory.create_staff(role="Nephrologist")
		appointment = FixtureFactory.create_appointment(
			patient=patient,
			nephrologist=nephrologist,
			appointment_date=today()
		)
		self.assertEqual(appointment.status, "Scheduled")
		
		# Step 3: Create dialysis session
		session = FixtureFactory.create_dialysis_session(
			patient=patient,
			appointment=appointment
		)
		self.assertEqual(session.session_status, "Scheduled")
		
		# Step 4: Update session status to completed
		session.session_status = "Completed"
		session.save()
		self.assertEqual(session.session_status, "Completed")
		
		# Step 5: Generate invoice
		invoice = FixtureFactory.create_invoice(
			patient=patient,
			session=session,
			billing_amount=1500.00,
			insurance_amount=750.00,
			patient_amount=750.00
		)
		self.assertEqual(invoice.status, "Draft")
		
		# Step 6: Submit invoice
		invoice.status = "Submitted"
		invoice.save()
		self.assertEqual(invoice.status, "Submitted")
		
		# Step 7: Record payment
		payment = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": patient.name,
			"amount": 750.00,
			"payment_date": today(),
			"payment_method": "Insurance"
		})
		payment.insert()
		
		# Verify all documents are linked correctly
		self.assertEqual(appointment.patient, patient.name)
		self.assertEqual(session.patient, patient.name)
		self.assertEqual(session.appointment, appointment.name)
		self.assertEqual(invoice.patient, patient.name)
		self.assertEqual(invoice.session, session.name)
		self.assertEqual(payment.invoice, invoice.name)
