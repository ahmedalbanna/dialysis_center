import frappe
from frappe.utils import random_string
import random


class PatientFactory:
	"""Factory for creating test patient records"""

	@staticmethod
	def create(patient_id=None, **kwargs):
		"""Create a single patient with optional overrides"""

		if not patient_id:
			patient_id = f"PT-TEST-{random_string(5)}"

		first_name = kwargs.get("first_name", f"Test{random_string(3)}")
		last_name = kwargs.get("last_name", f"Patient{random_string(3)}")
		patient_name = f"{first_name} {last_name}"
		
		patient_data = {
			"doctype": "Patient",
			"patient_id": patient_id,
			"patient_name": patient_name,
			"date_of_birth": kwargs.get("date_of_birth", "1970-01-01"),
			"gender": kwargs.get("gender", random.choice(["Male", "Female"])),
			"blood_group": kwargs.get("blood_group", random.choice(["A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"])),
			"national_id": kwargs.get("national_id", random_string(10)),
			"email": kwargs.get("email", f"test{random_string(5)}@example.com"),
			"address": kwargs.get("address", "Test Address"),
			"emergency_contact_name": kwargs.get("emergency_contact_name", "Emergency Contact"),
			"status": kwargs.get("status", "Active"),
		}
		
		# Add phone if provided
		if "phone" in kwargs:
			patient_data["mobile_number"] = kwargs["phone"]

		# Override with any additional kwargs
		patient_data.update(kwargs)

		patient = frappe.get_doc(patient_data)
		patient.insert(ignore_permissions=True, ignore_mandatory=True)
		frappe.db.commit()

		return patient

	@staticmethod
	def create_batch(count=10, **kwargs):
		"""Create multiple test patients"""
		patients = []
		for i in range(count):
			patient = PatientFactory.create(**kwargs)
			patients.append(patient)
		return patients

	@staticmethod
	def create_with_medical_history(patient_id=None):
		"""Create patient with complete medical history"""
		patient = PatientFactory.create(patient_id)

		# Add comorbidities
		patient.append("comorbidities", {
			"condition": "Diabetes Mellitus Type 2",
			"diagnosed_date": "2015-01-01",
			"status": "Active"
		})
		patient.append("comorbidities", {
			"condition": "Hypertension",
			"diagnosed_date": "2014-06-15",
			"status": "Active"
		})

		# Add allergies
		patient.append("allergies", {
			"allergen": "Penicillin",
			"reaction": "Rash",
			"severity": "Moderate"
		})

		# Add medications
		patient.append("medications", {
			"medication_name": "Lisinopril",
			"dosage": "10mg",
			"frequency": "Once daily",
			"start_date": "2015-03-01",
			"status": "Active"
		})

		patient.save(ignore_permissions=True)
		frappe.db.commit()

		return patient
