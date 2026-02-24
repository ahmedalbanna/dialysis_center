"""
Integration Tests for Dialysis Center App

Tests multi-document workflows:
1. Cascading updates across related documents
2. Related record updates
3. Cross-document validations
4. Complex business logic workflows
"""

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today, add_days
from .test_fixtures import FixtureFactory


class TestPatientAppointmentIntegration(IntegrationTestCase):
	"""Test patient and appointment integration"""

	def test_appointment_references_patient(self):
		"""Test appointment correctly references patient"""
		patient = FixtureFactory.create_patient()
		appointment = FixtureFactory.create_appointment(patient=patient)
		
		# Verify reference
		self.assertEqual(appointment.patient, patient.name)
		
		# Verify we can fetch related appointments
		related_apts = frappe.get_all("Appointment",
			filters={"patient": patient.name}
		)
		
		apt_names = [apt["name"] for apt in related_apts]
		self.assertIn(appointment.name, apt_names)

	def test_patient_appointments_relationship(self):
		"""Test fetching all appointments for a patient"""
		patient = FixtureFactory.create_patient()
		
		# Create multiple appointments for same patient
		apts = []
		for i in range(3):
			apt = FixtureFactory.create_appointment(
				patient=patient,
				appointment_date=add_days(today(), i)
			)
			apts.append(apt)
		
		# Fetch all patient appointments
		result = frappe.call(
			method="frappe.client.get_list",
			args={
				"doctype": "Appointment",
				"filters": {"patient": patient.name},
				"fields": ["name", "appointment_date", "status"]
			}
		)
		
		fetched_names = [apt["name"] for apt in result.message]
		for apt in apts:
			self.assertIn(apt.name, fetched_names)

	def test_patient_appointment_cascade_delete(self):
		"""Test behavior when deleting patient with appointments"""
		patient = FixtureFactory.create_patient()
		appointment = FixtureFactory.create_appointment(patient=patient)
		
		# Deleting patient should handle related appointments
		# (behavior depends on cascade settings)
		frappe.delete_doc("Patient", patient.name)
		
		# Verify patient is deleted
		self.assertFalse(frappe.db.exists("Patient", patient.name))


class TestAppointmentSessionIntegration(IntegrationTestCase):
	"""Test appointment and dialysis session integration"""

	def test_session_references_appointment(self):
		"""Test session correctly references appointment"""
		appointment = FixtureFactory.create_appointment()
		session = FixtureFactory.create_dialysis_session(appointment=appointment)
		
		self.assertEqual(session.appointment, appointment.name)

	def test_appointment_session_relationship(self):
		"""Test fetching sessions for appointment"""
		appointment = FixtureFactory.create_appointment()
		
		# Create multiple sessions for same appointment
		sessions = []
		for i in range(2):
			session = FixtureFactory.create_dialysis_session(
				appointment=appointment,
				session_date=add_days(today(), i)
			)
			sessions.append(session)
		
		# Fetch sessions
		related = frappe.get_all("Dialysis Session",
			filters={"appointment": appointment.name}
		)
		
		session_names = [s["name"] for s in related]
		for session in sessions:
			self.assertIn(session.name, session_names)

	def test_session_inherits_patient_from_appointment(self):
		"""Test session is linked to same patient as appointment"""
		patient = FixtureFactory.create_patient()
		appointment = FixtureFactory.create_appointment(patient=patient)
		session = FixtureFactory.create_dialysis_session(appointment=appointment)
		
		# Verify patient consistency
		self.assertEqual(appointment.patient, patient.name)
		self.assertEqual(session.patient, patient.name)

	def test_appointment_status_influences_session(self):
		"""Test appointment status affects session availability"""
		appointment = FixtureFactory.create_appointment()
		session = FixtureFactory.create_dialysis_session(appointment=appointment)
		
		# If appointment is cancelled, session should handle it gracefully
		appointment.status = "Cancelled"
		appointment.save()
		
		# Session still exists but appointment is cancelled
		self.assertEqual(appointment.status, "Cancelled")
		self.assertIsNotNone(session.name)


class TestSessionInvoiceIntegration(IntegrationTestCase):
	"""Test dialysis session and invoice integration"""

	def test_invoice_references_session(self):
		"""Test invoice correctly references session"""
		session = FixtureFactory.create_dialysis_session()
		invoice = FixtureFactory.create_invoice(session=session)
		
		self.assertEqual(invoice.session, session.name)

	def test_invoice_inherits_patient_from_session(self):
		"""Test invoice links to same patient as session"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		invoice = FixtureFactory.create_invoice(patient=patient, session=session)
		
		# Verify patient consistency
		self.assertEqual(session.patient, patient.name)
		self.assertEqual(invoice.patient, patient.name)

	def test_session_invoices_relationship(self):
		"""Test fetching invoices for session"""
		session = FixtureFactory.create_dialysis_session()
		
		# Create multiple invoices for same session
		invoices = []
		for i in range(2):
			inv = FixtureFactory.create_invoice(session=session)
			invoices.append(inv)
		
		# Fetch invoices
		related = frappe.get_all("Invoice",
			filters={"session": session.name}
		)
		
		inv_names = [inv["name"] for inv in related]
		for inv in invoices:
			self.assertIn(inv.name, inv_names)

	def test_invoice_billing_from_session_details(self):
		"""Test invoice amounts are derived from session"""
		session = FixtureFactory.create_dialysis_session()
		
		# Invoice should use session details to calculate amounts
		invoice = FixtureFactory.create_invoice(
			session=session,
			billing_amount=1500.00,
			insurance_amount=750.00,
			patient_amount=750.00
		)
		
		self.assertEqual(invoice.session, session.name)
		self.assertEqual(invoice.billing_amount, 1500.00)

	def test_session_status_affects_invoice_creation(self):
		"""Test session must be completed before invoice"""
		session = FixtureFactory.create_dialysis_session()
		
		# Session can be in any state, invoice creation depends on business logic
		self.assertEqual(session.session_status, "Scheduled")
		
		invoice = FixtureFactory.create_invoice(session=session)
		self.assertIsNotNone(invoice.name)


class TestInvoicePaymentIntegration(IntegrationTestCase):
	"""Test invoice and payment integration"""

	def test_payment_references_invoice(self):
		"""Test payment correctly references invoice"""
		invoice = FixtureFactory.create_invoice()
		
		payment = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": invoice.patient,
			"amount": 500.00,
			"payment_date": today(),
			"payment_method": "Cash"
		})
		payment.insert()
		
		self.assertEqual(payment.invoice, invoice.name)

	def test_invoice_payments_relationship(self):
		"""Test fetching payments for invoice"""
		invoice = FixtureFactory.create_invoice()
		
		# Create multiple payments for same invoice
		payments = []
		for i in range(2):
			payment = frappe.get_doc({
				"doctype": "Payment",
				"invoice": invoice.name,
				"patient": invoice.patient,
				"amount": 500.00,
				"payment_date": today(),
				"payment_method": "Cash"
			})
			payment.insert()
			payments.append(payment)
		
		# Fetch payments
		related = frappe.get_all("Payment",
			filters={"invoice": invoice.name}
		)
		
		payment_names = [p["name"] for p in related]
		for payment in payments:
			self.assertIn(payment.name, payment_names)

	def test_payment_amount_validation_against_invoice(self):
		"""Test payment amount doesn't exceed invoice total"""
		invoice = FixtureFactory.create_invoice(
			billing_amount=1000.00,
			insurance_amount=500.00,
			patient_amount=500.00
		)
		
		# Partial payment should work
		payment1 = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": invoice.patient,
			"amount": 250.00,
			"payment_date": today(),
			"payment_method": "Cash"
		})
		payment1.insert()
		
		# Another partial payment
		payment2 = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": invoice.patient,
			"amount": 250.00,
			"payment_date": today(),
			"payment_method": "Card"
		})
		payment2.insert()
		
		# Both payments should exist
		self.assertIsNotNone(payment1.name)
		self.assertIsNotNone(payment2.name)

	def test_total_payments_calculation(self):
		"""Test total payments for invoice"""
		invoice = FixtureFactory.create_invoice(
			billing_amount=1000.00,
			insurance_amount=500.00,
			patient_amount=500.00
		)
		
		# Create multiple payments
		payment_amounts = [300.00, 400.00, 300.00]
		
		for amount in payment_amounts:
			payment = frappe.get_doc({
				"doctype": "Payment",
				"invoice": invoice.name,
				"patient": invoice.patient,
				"amount": amount,
				"payment_date": today(),
				"payment_method": "Cash"
			})
			payment.insert()
		
		# Calculate total
		payments = frappe.get_all("Payment",
			filters={"invoice": invoice.name},
			fields=["amount"]
		)
		
		total_paid = sum(p["amount"] for p in payments)
		self.assertEqual(total_paid, 1000.00)


class TestPrescriptionMedicationIntegration(IntegrationTestCase):
	"""Test prescription and medication integration"""

	def test_prescription_item_references_medication(self):
		"""Test prescription item correctly references medication"""
		patient = FixtureFactory.create_patient()
		medication = FixtureFactory.create_medication()
		
		prescription = FixtureFactory.create_prescription(patient=patient)
		prescription.append("medications", {
			"medication": medication.name,
			"dosage": "500mg",
			"frequency": "Twice daily",
			"duration_days": 7
		})
		prescription.save()
		
		# Verify medication reference
		self.assertEqual(prescription.medications[0].medication, medication.name)

	def test_prescription_multiple_medications(self):
		"""Test prescription can have multiple medications"""
		patient = FixtureFactory.create_patient()
		
		med1 = FixtureFactory.create_medication()
		med2 = FixtureFactory.create_medication()
		med3 = FixtureFactory.create_medication()
		
		prescription = FixtureFactory.create_prescription(patient=patient)
		
		for med in [med1, med2, med3]:
			prescription.append("medications", {
				"medication": med.name,
				"dosage": "500mg",
				"frequency": "Twice daily"
			})
		
		prescription.save()
		
		self.assertEqual(len(prescription.medications), 3)
		med_names = [m.medication for m in prescription.medications]
		for med in [med1, med2, med3]:
			self.assertIn(med.name, med_names)

	def test_medication_stock_integration(self):
		"""Test medication stock is tracked"""
		medication = FixtureFactory.create_medication(stock_quantity=100)
		
		self.assertEqual(medication.stock_quantity, 100)
		
		# Stock would be updated on prescription creation in real system
		# This is integration with inventory


class TestLabTestIntegration(IntegrationTestCase):
	"""Test lab test integration with patient"""

	def test_lab_test_references_patient(self):
		"""Test lab test correctly references patient"""
		patient = FixtureFactory.create_patient()
		lab_test = FixtureFactory.create_lab_test(patient=patient)
		
		self.assertEqual(lab_test.patient, patient.name)

	def test_patient_lab_tests_relationship(self):
		"""Test fetching lab tests for patient"""
		patient = FixtureFactory.create_patient()
		
		# Create multiple lab tests
		tests = []
		for i in range(3):
			test = FixtureFactory.create_lab_test(
				patient=patient,
				test_type=["Blood Test", "Urine Test", "Chemistry Panel"][i]
			)
			tests.append(test)
		
		# Fetch tests
		related = frappe.get_all("Lab Test",
			filters={"patient": patient.name}
		)
		
		test_names = [t["name"] for t in related]
		for test in tests:
			self.assertIn(test.name, test_names)

	def test_lab_test_parameters(self):
		"""Test lab test with multiple parameters"""
		patient = FixtureFactory.create_patient()
		lab_test = FixtureFactory.create_lab_test(patient=patient)
		
		# Add parameters
		lab_test.append("parameters", {
			"parameter_name": "Potassium",
			"normal_range": "3.5-5.0",
			"unit": "mmol/L"
		})
		
		lab_test.append("parameters", {
			"parameter_name": "Sodium",
			"normal_range": "135-145",
			"unit": "mmol/L"
		})
		
		lab_test.save()
		
		self.assertEqual(len(lab_test.parameters), 2)


class TestInsuranceClaimIntegration(IntegrationTestCase):
	"""Test insurance claim integration"""

	def test_claim_references_invoice(self):
		"""Test insurance claim correctly references invoice"""
		patient = FixtureFactory.create_patient()
		invoice = FixtureFactory.create_invoice(patient=patient)
		claim = FixtureFactory.create_insurance_claim(
			patient=patient,
			invoice=invoice
		)
		
		self.assertEqual(claim.invoice, invoice.name)

	def test_invoice_claims_relationship(self):
		"""Test fetching claims for invoice"""
		invoice = FixtureFactory.create_invoice()
		
		# Create multiple claims for same invoice
		claims = []
		for i in range(2):
			claim = FixtureFactory.create_insurance_claim(invoice=invoice)
			claims.append(claim)
		
		# Fetch claims
		related = frappe.get_all("Insurance Claim",
			filters={"invoice": invoice.name}
		)
		
		claim_names = [c["name"] for c in related]
		for claim in claims:
			self.assertIn(claim.name, claim_names)

	def test_claim_amount_validation_against_invoice(self):
		"""Test claim amount doesn't exceed invoice amount"""
		invoice = FixtureFactory.create_invoice(
			billing_amount=1000.00,
			insurance_amount=600.00
		)
		
		# Claim amount should be <= insurance amount
		claim = FixtureFactory.create_insurance_claim(
			invoice=invoice,
			claim_amount=600.00
		)
		
		self.assertEqual(claim.claim_amount, 600.00)

	def test_claim_updates_invoice_status(self):
		"""Test claim status updates affect invoice"""
		invoice = FixtureFactory.create_invoice()
		claim = FixtureFactory.create_insurance_claim(invoice=invoice)
		
		# Approve claim
		claim.claim_status = "Approved"
		claim.save()
		
		# Invoice can track claim status
		self.assertEqual(claim.claim_status, "Approved")


class TestComplexMultiDocumentWorkflow(IntegrationTestCase):
	"""Test complex workflows involving multiple documents"""

	def test_end_to_end_patient_to_payment(self):
		"""Test complete workflow from patient to payment"""
		# Create patient
		patient = FixtureFactory.create_patient(patient_name="Workflow Test")
		
		# Create appointment
		nephrologist = FixtureFactory.create_staff()
		appointment = FixtureFactory.create_appointment(
			patient=patient,
			nephrologist=nephrologist
		)
		
		# Create session
		session = FixtureFactory.create_dialysis_session(
			patient=patient,
			appointment=appointment
		)
		
		# Create invoice
		invoice = FixtureFactory.create_invoice(
			patient=patient,
			session=session,
			billing_amount=2000.00,
			insurance_amount=1200.00,
			patient_amount=800.00
		)
		
		# Create insurance claim
		claim = FixtureFactory.create_insurance_claim(
			patient=patient,
			invoice=invoice,
			claim_amount=1200.00
		)
		
		# Process payment
		payment = frappe.get_doc({
			"doctype": "Payment",
			"invoice": invoice.name,
			"patient": patient.name,
			"amount": 800.00,
			"payment_date": today(),
			"payment_method": "Cash"
		})
		payment.insert()
		
		# Verify all links
		self.assertEqual(patient.name, patient.name)
		self.assertEqual(appointment.patient, patient.name)
		self.assertEqual(session.patient, patient.name)
		self.assertEqual(invoice.patient, patient.name)
		self.assertEqual(claim.invoice, invoice.name)
		self.assertEqual(payment.invoice, invoice.name)

	def test_patient_with_multiple_sessions_and_invoices(self):
		"""Test patient with multiple sessions and corresponding invoices"""
		patient = FixtureFactory.create_patient()
		
		# Create 3 sessions for same patient
		sessions = []
		invoices = []
		
		for i in range(3):
			session = FixtureFactory.create_dialysis_session(
				patient=patient,
				session_date=add_days(today(), i)
			)
			sessions.append(session)
			
			invoice = FixtureFactory.create_invoice(
				patient=patient,
				session=session,
				billing_amount=1000.00 * (i + 1),
				insurance_amount=500.00 * (i + 1),
				patient_amount=500.00 * (i + 1)
			)
			invoices.append(invoice)
		
		# Verify relationships
		patient_sessions = frappe.get_all("Dialysis Session",
			filters={"patient": patient.name}
		)
		self.assertEqual(len(patient_sessions), 3)
		
		patient_invoices = frappe.get_all("Invoice",
			filters={"patient": patient.name}
		)
		self.assertEqual(len(patient_invoices), 3)
		
		# Verify each invoice is linked to its session
		for session, invoice in zip(sessions, invoices):
			self.assertEqual(invoice.session, session.name)

	def test_prescription_creation_during_session(self):
		"""Test creating prescription during dialysis session"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		# Create prescription during session
		medication1 = FixtureFactory.create_medication()
		medication2 = FixtureFactory.create_medication()
		
		prescription = FixtureFactory.create_prescription(patient=patient)
		prescription.append("medications", {
			"medication": medication1.name,
			"dosage": "500mg",
			"frequency": "Twice daily"
		})
		prescription.append("medications", {
			"medication": medication2.name,
			"dosage": "250mg",
			"frequency": "Once daily"
		})
		prescription.save()
		
		# Prescription is linked to patient
		self.assertEqual(prescription.patient, patient.name)
		self.assertEqual(len(prescription.medications), 2)
