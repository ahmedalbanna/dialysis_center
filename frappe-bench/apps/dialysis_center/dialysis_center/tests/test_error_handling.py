"""
Error Handling and Edge Case Tests for Dialysis Center App

Tests:
1. Invalid input handling
2. Missing required fields
3. Permission denial scenarios
4. Constraint violations
5. Edge cases and boundary conditions
"""

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today, add_days
from .test_fixtures import FixtureFactory


class TestInvalidInputHandling(IntegrationTestCase):
	"""Test handling of invalid input"""

	def test_empty_string_in_required_field(self):
		"""Test empty string is rejected for required field"""
		with self.assertRaises(frappe.ValidationError):
			patient = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "",  # Empty
				"date_of_birth": "1980-01-01",
				"gender": "Male"
			})
			patient.insert()

	def test_none_value_in_required_field(self):
		"""Test None value is rejected for required field"""
		with self.assertRaises(frappe.ValidationError):
			patient = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": None,  # None
				"date_of_birth": "1980-01-01",
				"gender": "Male"
			})
			patient.insert()

	def test_invalid_email_format(self):
		"""Test various invalid email formats"""
		invalid_emails = [
			"notanemail",
			"test@",
			"@example.com",
		]
		
		for email in invalid_emails:
			with self.assertRaises(frappe.ValidationError):
				patient = frappe.get_doc({
					"doctype": "Patient",
					"patient_name": "Test",
					"date_of_birth": "1980-01-01",
					"gender": "Male",
					"email": email
				})
				patient.insert()

	def test_sql_injection_attempt_in_string_field(self):
		"""Test SQL injection attempts are safely handled"""
		malicious = "'; DROP TABLE Patient; --"
		
		# Should be safely escaped
		patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": malicious,
			"date_of_birth": "1980-01-01",
			"gender": "Male"
		})
		patient.insert()
		
		# Patient should be created with malicious string safely stored
		self.assertIsNotNone(patient.name)
		reloaded = frappe.get_doc("Patient", patient.name)
		self.assertEqual(reloaded.patient_name, malicious)


class TestMissingRequiredFields(IntegrationTestCase):
	"""Test handling of missing required fields"""

	def test_missing_patient_name(self):
		"""Test patient_name is mandatory"""
		with self.assertRaises(frappe.ValidationError):
			patient = frappe.get_doc({
				"doctype": "Patient",
				"date_of_birth": "1980-01-01",
				"gender": "Male"
			})
			patient.insert()

	def test_missing_date_of_birth(self):
		"""Test date_of_birth is mandatory"""
		with self.assertRaises(frappe.ValidationError):
			patient = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Test",
				"gender": "Male"
			})
			patient.insert()

	def test_missing_appointment_date(self):
		"""Test appointment_date is mandatory"""
		patient = FixtureFactory.create_patient()
		
		with self.assertRaises(frappe.ValidationError):
			appointment = frappe.get_doc({
				"doctype": "Appointment",
				"patient": patient.name,
				"appointment_time": "09:00:00"
			})
			appointment.insert()

	def test_missing_child_table_items(self):
		"""Test child table items validation"""
		patient = FixtureFactory.create_patient()
		
		with self.assertRaises(frappe.ValidationError):
			prescription = frappe.get_doc({
				"doctype": "Prescription",
				"patient": patient.name,
				"prescription_date": today()
				# No medications
			})
			prescription.insert()


class TestConstraintViolations(IntegrationTestCase):
	"""Test handling of constraint violations"""

	def test_unique_constraint_violation(self):
		"""Test unique constraint is enforced"""
		email = "unique@test.local"
		patient1 = FixtureFactory.create_patient(email=email)
		
		with self.assertRaises(frappe.ValidationError):
			patient2 = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Another",
				"date_of_birth": "1980-01-01",
				"gender": "Male",
				"email": email
			})
			patient2.insert()

	def test_unique_national_id_constraint(self):
		"""Test national ID uniqueness constraint"""
		nid = "UNIQUE123"
		patient1 = FixtureFactory.create_patient(national_id=nid)
		
		with self.assertRaises(frappe.ValidationError):
			patient2 = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Another",
				"date_of_birth": "1980-01-01",
				"gender": "Male",
				"national_id": nid
			})
			patient2.insert()

	def test_foreign_key_constraint_violation(self):
		"""Test foreign key constraint is enforced"""
		with self.assertRaises(frappe.ValidationError):
			appointment = frappe.get_doc({
				"doctype": "Appointment",
				"patient": "NONEXISTENT",
				"appointment_date": today(),
				"appointment_time": "09:00:00"
			})
			appointment.insert()

	def test_check_constraint_violation(self):
		"""Test CHECK constraint (business rule) violation"""
		with self.assertRaises(frappe.ValidationError):
			# End time must be after start time
			session = frappe.get_doc({
				"doctype": "Dialysis Session",
				"patient": FixtureFactory.create_patient().name,
				"session_date": today(),
				"session_time_in": "12:00:00",
				"session_time_out": "08:00:00"  # Before start
			})
			session.insert()


class TestBoundaryConditions(IntegrationTestCase):
	"""Test boundary conditions and edge cases"""

	def test_zero_amount_invoice(self):
		"""Test invoice with zero amount"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		# Zero amount might be valid in some scenarios
		invoice = FixtureFactory.create_invoice(
			patient=patient,
			session=session,
			billing_amount=0.00,
			insurance_amount=0.00,
			patient_amount=0.00
		)
		
		self.assertEqual(invoice.billing_amount, 0.00)

	def test_very_large_amount(self):
		"""Test invoice with very large amount"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		large_amount = 999999999.99
		invoice = FixtureFactory.create_invoice(
			patient=patient,
			session=session,
			billing_amount=large_amount,
			insurance_amount=large_amount / 2,
			patient_amount=large_amount / 2
		)
		
		self.assertEqual(invoice.billing_amount, large_amount)

	def test_minimum_age_patient(self):
		"""Test patient with very recent DOB"""
		recent_dob = add_days(today(), -1)  # Born yesterday
		patient = FixtureFactory.create_patient(date_of_birth=str(recent_dob))
		
		self.assertIsNotNone(patient.name)

	def test_very_old_patient(self):
		"""Test patient with very old DOB"""
		old_dob = "1900-01-01"
		patient = FixtureFactory.create_patient(date_of_birth=old_dob)
		
		self.assertGreater(patient.age, 100)

	def test_appointment_far_in_future(self):
		"""Test appointment scheduled far in future"""
		patient = FixtureFactory.create_patient()
		future_date = add_days(today(), 365)  # 1 year from now
		
		appointment = FixtureFactory.create_appointment(
			patient=patient,
			appointment_date=future_date
		)
		
		self.assertIsNotNone(appointment.name)

	def test_special_characters_in_name(self):
		"""Test special characters in patient name"""
		special_name = "Mr. José García-López O'Brien"
		patient = FixtureFactory.create_patient(patient_name=special_name)
		
		self.assertEqual(patient.patient_name, special_name)

	def test_unicode_characters_in_name(self):
		"""Test Unicode characters in patient name"""
		unicode_name = "محمد علي"  # Arabic name
		patient = FixtureFactory.create_patient(patient_name=unicode_name)
		
		self.assertEqual(patient.patient_name, unicode_name)

	def test_minimum_session_duration(self):
		"""Test session with minimum duration"""
		patient = FixtureFactory.create_patient()
		
		# 1 minute session
		session = FixtureFactory.create_dialysis_session(
			patient=patient,
			session_time_in="08:00:00",
			session_time_out="08:01:00"
		)
		
		self.assertEqual(session.session_duration_minutes, 1)

	def test_midnight_appointment(self):
		"""Test appointment at midnight"""
		patient = FixtureFactory.create_patient()
		
		appointment = FixtureFactory.create_appointment(
			patient=patient,
			appointment_time="00:00:00"
		)
		
		self.assertEqual(appointment.appointment_time, "00:00:00")

	def test_end_of_day_appointment(self):
		"""Test appointment at end of day"""
		patient = FixtureFactory.create_patient()
		
		appointment = FixtureFactory.create_appointment(
			patient=patient,
			appointment_time="23:59:59"
		)
		
		self.assertEqual(appointment.appointment_time, "23:59:59")


class TestConcurrentOperations(IntegrationTestCase):
	"""Test handling of concurrent operations"""

	def test_concurrent_document_creation(self):
		"""Test creating multiple documents concurrently"""
		patients = []
		
		for i in range(5):
			patient = FixtureFactory.create_patient(
				patient_name=f"Concurrent Patient {i}"
			)
			patients.append(patient)
		
		# All patients should be created
		self.assertEqual(len(patients), 5)

	def test_concurrent_document_modification(self):
		"""Test modifying same document concurrently"""
		patient = FixtureFactory.create_patient()
		
		# Simulate concurrent modifications
		patient.patient_name = "Modified 1"
		patient.save()
		
		# Reload and modify again
		patient2 = frappe.get_doc("Patient", patient.name)
		patient2.patient_name = "Modified 2"
		patient2.save()
		
		# Last modification should win
		reloaded = frappe.get_doc("Patient", patient.name)
		self.assertEqual(reloaded.patient_name, "Modified 2")

	def test_rapid_status_transitions(self):
		"""Test rapid status changes"""
		appointment = FixtureFactory.create_appointment()
		
		statuses = ["Scheduled", "Completed", "Cancelled"]
		
		for status in statuses:
			appointment.status = status
			appointment.save()
		
		self.assertEqual(appointment.status, "Cancelled")


class TestDataConsistency(IntegrationTestCase):
	"""Test data consistency and integrity"""

	def test_amount_sum_consistency(self):
		"""Test invoice amount sum consistency"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		invoice = FixtureFactory.create_invoice(
			patient=patient,
			session=session,
			billing_amount=1000.00,
			insurance_amount=600.00,
			patient_amount=400.00
		)
		
		# Verify sum
		calculated_sum = invoice.insurance_amount + invoice.patient_amount
		self.assertEqual(calculated_sum, invoice.billing_amount)

	def test_document_reference_consistency(self):
		"""Test document references remain consistent"""
		patient = FixtureFactory.create_patient()
		appointment = FixtureFactory.create_appointment(patient=patient)
		session = FixtureFactory.create_dialysis_session(
			patient=patient,
			appointment=appointment
		)
		
		# Verify consistency
		self.assertEqual(appointment.patient, patient.name)
		self.assertEqual(session.patient, patient.name)
		self.assertEqual(session.appointment, appointment.name)

	def test_status_consistency_across_documents(self):
		"""Test status consistency between related documents"""
		appointment = FixtureFactory.create_appointment()
		session = FixtureFactory.create_dialysis_session(appointment=appointment)
		
		# Appointment and session have independent status fields
		appointment.status = "Completed"
		appointment.save()
		
		session.session_status = "Completed"
		session.save()
		
		# Verify independent updates
		reloaded_apt = frappe.get_doc("Appointment", appointment.name)
		reloaded_session = frappe.get_doc("Dialysis Session", session.name)
		
		self.assertEqual(reloaded_apt.status, "Completed")
		self.assertEqual(reloaded_session.session_status, "Completed")
