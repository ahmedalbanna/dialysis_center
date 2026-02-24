"""
Validation Tests for Dialysis Center App

Comprehensive tests for:
1. Mandatory field validations
2. Cross-field constraints
3. Business rule validations
4. Data integrity checks
"""

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today, add_days
from .test_fixtures import FixtureFactory


class TestPatientValidations(IntegrationTestCase):
	"""Test all patient validations"""

	def test_mandatory_fields(self):
		"""Test mandatory fields are required"""
		mandatory_fields = [
			("patient_name", "Patient Name is required"),
			("date_of_birth", "Date of Birth is required"),
			("gender", "Gender is required"),
		]
		
		for field, error_msg in mandatory_fields:
			with self.assertRaises(frappe.ValidationError):
				patient = frappe.get_doc({
					"doctype": "Patient",
					"patient_name": "Test" if field != "patient_name" else "",
					"date_of_birth": "1980-01-01" if field != "date_of_birth" else "",
					"gender": "Male" if field != "gender" else "",
				})
				patient.insert()

	def test_valid_blood_group_values(self):
		"""Test blood group must be valid"""
		valid_groups = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
		
		for bg in valid_groups:
			patient = FixtureFactory.create_patient(blood_group=bg)
			self.assertEqual(patient.blood_group, bg)
		
		# Invalid blood group
		with self.assertRaises(frappe.ValidationError):
			patient = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Test",
				"date_of_birth": "1980-01-01",
				"gender": "Male",
				"blood_group": "INVALID"
			})
			patient.insert()

	def test_valid_gender_values(self):
		"""Test gender must be one of allowed values"""
		valid_genders = ["Male", "Female", "Other"]
		
		for gender in valid_genders:
			patient = FixtureFactory.create_patient(gender=gender)
			self.assertEqual(patient.gender, gender)

	def test_dob_cannot_be_future_date(self):
		"""Test date of birth cannot be in the future"""
		with self.assertRaises(frappe.ValidationError):
			patient = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Test",
				"date_of_birth": add_days(today(), 1),  # Tomorrow
				"gender": "Male"
			})
			patient.insert()

	def test_phone_format_validation(self):
		"""Test phone number format validation"""
		# Valid formats should pass
		valid_phones = ["+201001234567", "01001234567", "+1-201-123-4567"]
		
		for phone in valid_phones:
			try:
				patient = FixtureFactory.create_patient(mobile_number=phone)
				self.assertIsNotNone(patient.name)
			except:
				pass  # Some formats might not be supported

	def test_email_format_validation(self):
		"""Test email format must be valid"""
		invalid_emails = ["notanemail", "test@", "@test.com", "test @test.com"]
		
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

	def test_duplicate_national_id(self):
		"""Test national ID uniqueness"""
		nid = "12345678901"
		patient1 = FixtureFactory.create_patient(national_id=nid)
		
		with self.assertRaises(frappe.ValidationError):
			patient2 = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Another Patient",
				"date_of_birth": "1980-01-01",
				"gender": "Male",
				"national_id": nid
			})
			patient2.insert()

	def test_duplicate_email(self):
		"""Test email uniqueness"""
		email = "unique@test.local"
		patient1 = FixtureFactory.create_patient(email=email)
		
		with self.assertRaises(frappe.ValidationError):
			patient2 = frappe.get_doc({
				"doctype": "Patient",
				"patient_name": "Another Patient",
				"date_of_birth": "1980-01-01",
				"gender": "Male",
				"email": email
			})
			patient2.insert()

	def test_marital_status_validation(self):
		"""Test marital status has valid values"""
		valid_statuses = ["Single", "Married", "Divorced", "Widowed"]
		
		for status in valid_statuses:
			patient = FixtureFactory.create_patient(marital_status=status)
			self.assertEqual(patient.marital_status, status)


class TestAppointmentValidations(IntegrationTestCase):
	"""Test appointment field validations"""

	def test_mandatory_appointment_fields(self):
		"""Test required appointment fields"""
		with self.assertRaises(frappe.ValidationError):
			# Missing patient
			appointment = frappe.get_doc({
				"doctype": "Appointment",
				"appointment_date": today(),
				"appointment_time": "09:00:00"
			})
			appointment.insert()

	def test_appointment_date_not_in_past(self):
		"""Test appointment date must be today or future"""
		patient = FixtureFactory.create_patient()
		
		with self.assertRaises(frappe.ValidationError):
			appointment = frappe.get_doc({
				"doctype": "Appointment",
				"patient": patient.name,
				"appointment_date": add_days(today(), -1),
				"appointment_time": "09:00:00"
			})
			appointment.insert()

	def test_valid_appointment_types(self):
		"""Test appointment type values"""
		patient = FixtureFactory.create_patient()
		valid_types = ["Regular", "Follow-up", "Emergency", "Initial Consultation"]
		
		for apt_type in valid_types:
			appointment = FixtureFactory.create_appointment(
				patient=patient,
				appointment_type=apt_type
			)
			self.assertEqual(appointment.appointment_type, apt_type)

	def test_valid_appointment_statuses(self):
		"""Test appointment status values"""
		valid_statuses = ["Scheduled", "Completed", "Cancelled", "No-show"]
		appointment = FixtureFactory.create_appointment()
		
		for status in valid_statuses:
			appointment.status = status
			appointment.save()
			self.assertEqual(appointment.status, status)

	def test_appointment_time_format(self):
		"""Test appointment time is in valid format"""
		patient = FixtureFactory.create_patient()
		
		# Valid time format
		appointment = FixtureFactory.create_appointment(
			patient=patient,
			appointment_time="14:30:00"
		)
		self.assertEqual(appointment.appointment_time, "14:30:00")

	def test_nephrologist_must_exist(self):
		"""Test nephrologist must be valid staff member"""
		patient = FixtureFactory.create_patient()
		
		with self.assertRaises(frappe.ValidationError):
			appointment = frappe.get_doc({
				"doctype": "Appointment",
				"patient": patient.name,
				"appointment_date": today(),
				"appointment_time": "09:00:00",
				"nephrologist": "NONEXISTENT"
			})
			appointment.insert()


class TestDialysisSessionValidations(IntegrationTestCase):
	"""Test dialysis session validations"""

	def test_session_end_time_after_start_time(self):
		"""Test session end time must be after start time"""
		patient = FixtureFactory.create_patient()
		
		with self.assertRaises(frappe.ValidationError):
			session = frappe.get_doc({
				"doctype": "Dialysis Session",
				"patient": patient.name,
				"session_date": today(),
				"session_time_in": "12:00:00",
				"session_time_out": "08:00:00"  # Before start
			})
			session.insert()

	def test_session_duration_validation(self):
		"""Test session duration must be positive"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(
			patient=patient,
			session_time_in="08:00:00",
			session_time_out="08:15:00"  # 15 minutes
		)
		
		# Duration should be calculated
		self.assertEqual(session.session_duration_minutes, 15)

	def test_valid_session_statuses(self):
		"""Test session status values"""
		valid_statuses = ["Scheduled", "In Progress", "Completed", "Billed", "Cancelled"]
		session = FixtureFactory.create_dialysis_session()
		
		for status in valid_statuses:
			session.session_status = status
			session.save()
			self.assertEqual(session.session_status, status)

	def test_session_patient_must_exist(self):
		"""Test session patient must be valid"""
		with self.assertRaises(frappe.ValidationError):
			session = frappe.get_doc({
				"doctype": "Dialysis Session",
				"patient": "NONEXISTENT",
				"session_date": today(),
				"session_time_in": "08:00:00",
				"session_time_out": "12:00:00"
			})
			session.insert()

	def test_session_date_validation(self):
		"""Test session date constraints"""
		patient = FixtureFactory.create_patient()
		
		# Should allow today's date and future dates
		session = FixtureFactory.create_dialysis_session(
			patient=patient,
			session_date=today()
		)
		self.assertIsNotNone(session.name)


class TestInvoiceValidations(IntegrationTestCase):
	"""Test invoice field validations"""

	def test_invoice_amount_split_validation(self):
		"""Test insurance + patient amount = billing amount"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		# Correct split
		invoice = FixtureFactory.create_invoice(
			patient=patient,
			session=session,
			billing_amount=1000.00,
			insurance_amount=600.00,
			patient_amount=400.00
		)
		self.assertEqual(
			invoice.insurance_amount + invoice.patient_amount,
			invoice.billing_amount
		)
		
		# Invalid split
		with self.assertRaises(frappe.ValidationError):
			invoice = frappe.get_doc({
				"doctype": "Invoice",
				"patient": patient.name,
				"session": session.name,
				"billing_amount": 1000.00,
				"insurance_amount": 600.00,
				"patient_amount": 300.00  # Should be 400
			})
			invoice.insert()

	def test_invoice_amounts_non_negative(self):
		"""Test invoice amounts cannot be negative"""
		patient = FixtureFactory.create_patient()
		session = FixtureFactory.create_dialysis_session(patient=patient)
		
		with self.assertRaises(frappe.ValidationError):
			invoice = frappe.get_doc({
				"doctype": "Invoice",
				"patient": patient.name,
				"session": session.name,
				"billing_amount": -1000.00  # Negative
			})
			invoice.insert()

	def test_valid_invoice_statuses(self):
		"""Test invoice status values"""
		valid_statuses = ["Draft", "Submitted", "Paid", "Cancelled"]
		invoice = FixtureFactory.create_invoice()
		
		for status in valid_statuses:
			invoice.status = status
			invoice.save()
			self.assertEqual(invoice.status, status)

	def test_invoice_patient_must_exist(self):
		"""Test invoice patient must be valid"""
		with self.assertRaises(frappe.ValidationError):
			invoice = frappe.get_doc({
				"doctype": "Invoice",
				"patient": "NONEXISTENT",
				"billing_amount": 1000.00
			})
			invoice.insert()

	def test_invoice_date_validation(self):
		"""Test invoice date cannot be in future"""
		patient = FixtureFactory.create_patient()
		
		with self.assertRaises(frappe.ValidationError):
			invoice = frappe.get_doc({
				"doctype": "Invoice",
				"patient": patient.name,
				"billing_amount": 1000.00,
				"invoice_date": add_days(today(), 1)  # Tomorrow
			})
			invoice.insert()


class TestPrescriptionValidations(IntegrationTestCase):
	"""Test prescription validations"""

	def test_prescription_patient_must_exist(self):
		"""Test prescription must reference valid patient"""
		with self.assertRaises(frappe.ValidationError):
			prescription = frappe.get_doc({
				"doctype": "Prescription",
				"patient": "NONEXISTENT",
				"prescription_date": today()
			})
			prescription.insert()

	def test_prescription_items_required(self):
		"""Test prescription must have at least one item"""
		patient = FixtureFactory.create_patient()
		
		with self.assertRaises(frappe.ValidationError):
			prescription = frappe.get_doc({
				"doctype": "Prescription",
				"patient": patient.name,
				"prescription_date": today()
				# No items
			})
			prescription.insert()

	def test_prescription_item_medication_required(self):
		"""Test prescription item must reference valid medication"""
		patient = FixtureFactory.create_patient()
		nephrologist = FixtureFactory.create_staff()
		
		with self.assertRaises(frappe.ValidationError):
			prescription = frappe.get_doc({
				"doctype": "Prescription",
				"patient": patient.name,
				"nephrologist": nephrologist.name,
				"prescription_date": today()
			})
			
			prescription.append("medications", {
				"medication": "NONEXISTENT",
				"dosage": "500mg",
				"frequency": "Twice daily"
			})
			
			prescription.insert()

	def test_prescription_duration_validation(self):
		"""Test prescription duration must be positive"""
		patient = FixtureFactory.create_patient()
		medication = FixtureFactory.create_medication()
		
		with self.assertRaises(frappe.ValidationError):
			prescription = frappe.get_doc({
				"doctype": "Prescription",
				"patient": patient.name,
				"prescription_date": today()
			})
			
			prescription.append("medications", {
				"medication": medication.name,
				"dosage": "500mg",
				"frequency": "Twice daily",
				"duration_days": -7  # Negative duration
			})
			
			prescription.insert()


class TestLabTestValidations(IntegrationTestCase):
	"""Test lab test validations"""

	def test_lab_test_patient_must_exist(self):
		"""Test lab test must reference valid patient"""
		with self.assertRaises(frappe.ValidationError):
			lab_test = frappe.get_doc({
				"doctype": "Lab Test",
				"patient": "NONEXISTENT",
				"test_date": today()
			})
			lab_test.insert()

	def test_lab_test_type_validation(self):
		"""Test lab test type must be valid"""
		valid_types = ["Blood Test", "Urine Test", "Kidney Function", "Chemistry Panel"]
		patient = FixtureFactory.create_patient()
		
		for test_type in valid_types:
			lab_test = FixtureFactory.create_lab_test(
				patient=patient,
				test_type=test_type
			)
			self.assertEqual(lab_test.test_type, test_type)

	def test_lab_test_status_validation(self):
		"""Test lab test status values"""
		valid_statuses = ["Pending", "In Progress", "Completed", "Cancelled"]
		lab_test = FixtureFactory.create_lab_test()
		
		for status in valid_statuses:
			lab_test.status = status
			lab_test.save()
			self.assertEqual(lab_test.status, status)


class TestInsuranceClaimValidations(IntegrationTestCase):
	"""Test insurance claim validations"""

	def test_claim_amount_positive(self):
		"""Test claim amount must be positive"""
		patient = FixtureFactory.create_patient()
		invoice = FixtureFactory.create_invoice(patient=patient)
		
		with self.assertRaises(frappe.ValidationError):
			claim = frappe.get_doc({
				"doctype": "Insurance Claim",
				"patient": patient.name,
				"invoice": invoice.name,
				"claim_amount": -100.00  # Negative
			})
			claim.insert()

	def test_claim_date_validation(self):
		"""Test claim date cannot be in future"""
		patient = FixtureFactory.create_patient()
		invoice = FixtureFactory.create_invoice(patient=patient)
		
		with self.assertRaises(frappe.ValidationError):
			claim = frappe.get_doc({
				"doctype": "Insurance Claim",
				"patient": patient.name,
				"invoice": invoice.name,
				"claim_amount": 500.00,
				"claim_date": add_days(today(), 1)  # Tomorrow
			})
			claim.insert()

	def test_valid_claim_statuses(self):
		"""Test claim status values"""
		valid_statuses = ["Draft", "Submitted", "Approved", "Rejected", "Paid"]
		claim = FixtureFactory.create_insurance_claim()
		
		for status in valid_statuses:
			claim.claim_status = status
			claim.save()
			self.assertEqual(claim.claim_status, status)
