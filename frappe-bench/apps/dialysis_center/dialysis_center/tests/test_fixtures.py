"""
Test Fixtures for Dialysis Center App

Provides reusable test data and fixtures for all DocTypes.
This module centralizes test data creation to ensure consistency across test suites.
"""

import frappe
from frappe.utils import today, add_days, get_time, now_datetime
import random


class FixtureFactory:
	"""
	Central factory for creating test documents with sensible defaults.
	Ensures test data consistency across all test suites.
	"""

	# Test data counters for unique names
	_patient_counter = 0
	_appointment_counter = 0
	_session_counter = 0
	_staff_counter = 0
	_medication_counter = 0

	@classmethod
	def create_patient(cls, **kwargs):
		"""
		Create a test Patient with defaults.
		
		Args:
			**kwargs: Override any default field values
			
		Returns:
			Patient document
		"""
		cls._patient_counter += 1
		
		defaults = {
			"doctype": "Patient",
			"patient_name": f"Test Patient {cls._patient_counter}",
			"date_of_birth": "1980-01-15",
			"gender": "Male",
			"blood_group": "O+",
			"national_id": f"NID{cls._patient_counter:06d}",
			"mobile_number": f"+201001000{cls._patient_counter:02d}",
			"email": f"patient{cls._patient_counter}@test.local",
			"address": "123 Test Street",
			"marital_status": "Married",
			"contact_person": f"Contact {cls._patient_counter}",
			"contact_number": f"+201001000{cls._patient_counter:02d}",
		}
		defaults.update(kwargs)
		
		patient = frappe.get_doc(defaults)
		patient.insert(ignore_permissions=True)
		return patient

	@classmethod
	def create_staff(cls, **kwargs):
		"""
		Create a test Staff member with defaults.
		
		Args:
			**kwargs: Override any default field values
			
		Returns:
			Staff document
		"""
		cls._staff_counter += 1
		
		defaults = {
			"doctype": "Staff",
			"staff_name": f"Dr. Test {cls._staff_counter}",
			"role": "Nephrologist",
			"specialization": "Nephrology",
			"license_number": f"LIC{cls._staff_counter:06d}",
			"mobile": f"+201001100{cls._staff_counter:02d}",
			"email": f"staff{cls._staff_counter}@test.local",
			"status": "Active",
		}
		defaults.update(kwargs)
		
		staff = frappe.get_doc(defaults)
		staff.insert(ignore_permissions=True)
		return staff

	@classmethod
	def create_appointment(cls, patient=None, nephrologist=None, **kwargs):
		"""
		Create a test Appointment with defaults.
		
		Args:
			patient: Patient document or name (creates one if not provided)
			nephrologist: Staff document or name (creates one if not provided)
			**kwargs: Override any default field values
			
		Returns:
			Appointment document
		"""
		if patient is None:
			patient = cls.create_patient()
		patient_name = patient.name if hasattr(patient, 'name') else patient
		
		if nephrologist is None:
			nephrologist = cls.create_staff(role="Nephrologist")
		nephrologist_name = nephrologist.name if hasattr(nephrologist, 'name') else nephrologist
		
		cls._appointment_counter += 1
		
		defaults = {
			"doctype": "Appointment",
			"patient": patient_name,
			"appointment_date": today(),
			"appointment_time": "09:00:00",
			"nephrologist": nephrologist_name,
			"appointment_type": "Regular",
			"status": "Scheduled",
			"notes": f"Test appointment {cls._appointment_counter}",
		}
		defaults.update(kwargs)
		
		appointment = frappe.get_doc(defaults)
		appointment.insert(ignore_permissions=True)
		return appointment

	@classmethod
	def create_dialysis_session(cls, patient=None, appointment=None, nephrologist=None, **kwargs):
		"""
		Create a test Dialysis Session with defaults.
		
		Args:
			patient: Patient document or name
			appointment: Appointment document or name
			nephrologist: Staff document or name
			**kwargs: Override any default field values
			
		Returns:
			Dialysis Session document
		"""
		if patient is None:
			patient = cls.create_patient()
		patient_name = patient.name if hasattr(patient, 'name') else patient
		
		if nephrologist is None:
			nephrologist = cls.create_staff(role="Nephrologist")
		nephrologist_name = nephrologist.name if hasattr(nephrologist, 'name') else nephrologist
		
		if appointment is None:
			appointment = cls.create_appointment(patient=patient_name, nephrologist=nephrologist_name)
		appointment_name = appointment.name if hasattr(appointment, 'name') else appointment
		
		cls._session_counter += 1
		
		defaults = {
			"doctype": "Dialysis Session",
			"patient": patient_name,
			"appointment": appointment_name,
			"session_date": today(),
			"session_time_in": "08:00:00",
			"session_time_out": "12:00:00",
			"nephrologist": nephrologist_name,
			"session_status": "Scheduled",
			"treatment_template": cls.create_treatment_template().name if not kwargs.get("treatment_template") else kwargs.get("treatment_template"),
		}
		defaults.update(kwargs)
		
		session = frappe.get_doc(defaults)
		session.insert(ignore_permissions=True)
		return session

	@classmethod
	def create_treatment_template(cls, **kwargs):
		"""
		Create a test Treatment Template with defaults.
		
		Args:
			**kwargs: Override any default field values
			
		Returns:
			Treatment Template document
		"""
		defaults = {
			"doctype": "Treatment Template",
			"template_name": "Standard Dialysis",
			"dialysate_temperature": 37,
			"blood_flow_rate": 350,
			"dialysate_flow_rate": 500,
			"session_duration": 240,
			"frequency_per_week": 3,
		}
		defaults.update(kwargs)
		
		# Check if already exists
		existing = frappe.db.exists("Treatment Template", "Standard Dialysis")
		if existing:
			return frappe.get_doc("Treatment Template", "Standard Dialysis")
		
		template = frappe.get_doc(defaults)
		template.insert(ignore_permissions=True)
		return template

	@classmethod
	def create_medication(cls, **kwargs):
		"""
		Create a test Medication with defaults.
		
		Args:
			**kwargs: Override any default field values
			
		Returns:
			Medication document
		"""
		cls._medication_counter += 1
		
		defaults = {
			"doctype": "Medication",
			"medication_name": f"Test Drug {cls._medication_counter}",
			"medication_code": f"MED{cls._medication_counter:06d}",
			"category": "Antibiotics",
			"generic_name": f"Generic Name {cls._medication_counter}",
			"strength": "500mg",
			"unit_of_measure": "Tablet",
			"price": 10.00,
			"stock_quantity": 100,
			"status": "Active",
		}
		defaults.update(kwargs)
		
		medication = frappe.get_doc(defaults)
		medication.insert(ignore_permissions=True)
		return medication

	@classmethod
	def create_prescription(cls, patient=None, nephrologist=None, **kwargs):
		"""
		Create a test Prescription with defaults.
		
		Args:
			patient: Patient document or name
			nephrologist: Staff document or name
			**kwargs: Override any default field values
			
		Returns:
			Prescription document
		"""
		if patient is None:
			patient = cls.create_patient()
		patient_name = patient.name if hasattr(patient, 'name') else patient
		
		if nephrologist is None:
			nephrologist = cls.create_staff(role="Nephrologist")
		nephrologist_name = nephrologist.name if hasattr(nephrologist, 'name') else nephrologist
		
		defaults = {
			"doctype": "Prescription",
			"patient": patient_name,
			"nephrologist": nephrologist_name,
			"prescription_date": today(),
			"status": "Active",
		}
		defaults.update(kwargs)
		
		prescription = frappe.get_doc(defaults)
		prescription.insert(ignore_permissions=True)
		return prescription

	@classmethod
	def create_prescription_item(cls, prescription=None, medication=None, **kwargs):
		"""
		Create a test Prescription Item.
		
		Args:
			prescription: Prescription document
			medication: Medication document or name
			**kwargs: Override any default field values
			
		Returns:
			Prescription Item document (appended to prescription)
		"""
		if medication is None:
			medication = cls.create_medication()
		medication_name = medication.name if hasattr(medication, 'name') else medication
		
		defaults = {
			"medication": medication_name,
			"dosage": "500mg",
			"frequency": "Twice daily",
			"duration_days": 7,
			"quantity": 14,
		}
		defaults.update(kwargs)
		
		item = frappe.get_doc(defaults)
		return item

	@classmethod
	def create_invoice(cls, patient=None, session=None, **kwargs):
		"""
		Create a test Invoice with defaults.
		
		Args:
			patient: Patient document or name
			session: Dialysis Session document or name
			**kwargs: Override any default field values
			
		Returns:
			Invoice document
		"""
		if patient is None:
			patient = cls.create_patient()
		patient_name = patient.name if hasattr(patient, 'name') else patient
		
		if session is None:
			session = cls.create_dialysis_session(patient=patient_name)
		session_name = session.name if hasattr(session, 'name') else session
		
		defaults = {
			"doctype": "Invoice",
			"patient": patient_name,
			"session": session_name,
			"invoice_date": today(),
			"billing_amount": 1000.00,
			"insurance_amount": 500.00,
			"patient_amount": 500.00,
			"status": "Draft",
		}
		defaults.update(kwargs)
		
		invoice = frappe.get_doc(defaults)
		invoice.insert(ignore_permissions=True)
		return invoice

	@classmethod
	def create_lab_test(cls, patient=None, nephrologist=None, **kwargs):
		"""
		Create a test Lab Test with defaults.
		
		Args:
			patient: Patient document or name
			nephrologist: Staff document or name
			**kwargs: Override any default field values
			
		Returns:
			Lab Test document
		"""
		if patient is None:
			patient = cls.create_patient()
		patient_name = patient.name if hasattr(patient, 'name') else patient
		
		if nephrologist is None:
			nephrologist = cls.create_staff(role="Nephrologist")
		nephrologist_name = nephrologist.name if hasattr(nephrologist, 'name') else nephrologist
		
		defaults = {
			"doctype": "Lab Test",
			"patient": patient_name,
			"ordered_by": nephrologist_name,
			"test_date": today(),
			"test_type": "Blood Test",
			"status": "Pending",
		}
		defaults.update(kwargs)
		
		lab_test = frappe.get_doc(defaults)
		lab_test.insert(ignore_permissions=True)
		return lab_test

	@classmethod
	def create_lab_test_parameter(cls, lab_test, **kwargs):
		"""
		Create a test Lab Test Parameter (child table item).
		
		Args:
			lab_test: Lab Test document
			**kwargs: Override any default field values
			
		Returns:
			Lab Test Parameter item
		"""
		defaults = {
			"parameter_name": "Potassium",
			"normal_range": "3.5-5.0",
			"unit": "mmol/L",
		}
		defaults.update(kwargs)
		
		return defaults

	@classmethod
	def create_insurance_claim(cls, patient=None, invoice=None, **kwargs):
		"""
		Create a test Insurance Claim with defaults.
		
		Args:
			patient: Patient document or name
			invoice: Invoice document or name
			**kwargs: Override any default field values
			
		Returns:
			Insurance Claim document
		"""
		if patient is None:
			patient = cls.create_patient()
		patient_name = patient.name if hasattr(patient, 'name') else patient
		
		if invoice is None:
			invoice = cls.create_invoice(patient=patient_name)
		invoice_name = invoice.name if hasattr(invoice, 'name') else invoice
		
		defaults = {
			"doctype": "Insurance Claim",
			"patient": patient_name,
			"invoice": invoice_name,
			"claim_amount": 500.00,
			"claim_date": today(),
			"claim_status": "Submitted",
		}
		defaults.update(kwargs)
		
		claim = frappe.get_doc(defaults)
		claim.insert(ignore_permissions=True)
		return claim

	@classmethod
	def cleanup(cls):
		"""
		Clean up all test data created by this factory.
		Call at the end of test suites to ensure no test data persists.
		"""
		# Clear counters
		cls._patient_counter = 0
		cls._appointment_counter = 0
		cls._session_counter = 0
		cls._staff_counter = 0
		cls._medication_counter = 0
