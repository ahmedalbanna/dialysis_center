import frappe
from frappe.utils import now_datetime, add_to_date
import random


class SessionFactory:
	"""Factory for creating test dialysis sessions"""

	@staticmethod
	def create(patient=None, appointment=None, **kwargs):
		"""Create a dialysis session"""

		if not patient:
			from dialysis_center.tests.factories.patient_factory import PatientFactory
			patient = PatientFactory.create()

		if not appointment:
			from dialysis_center.tests.factories.appointment_factory import AppointmentFactory
			appointment = AppointmentFactory.create(patient=patient)

		session_data = {
			"doctype": "Dialysis Session",
			"patient": patient.name if hasattr(patient, 'name') else patient,
			"appointment": appointment.name if hasattr(appointment, 'name') else appointment,
			"session_date": kwargs.get("session_date", now_datetime()),
			"start_time": kwargs.get("start_time", "09:00:00"),
			"machine": kwargs.get("machine", appointment.machine if hasattr(appointment, 'machine') else None),
			"nurse": kwargs.get("nurse", appointment.staff if hasattr(appointment, 'staff') else None),
			"dialyzer_type": kwargs.get("dialyzer_type", "F60"),
			"blood_flow_rate": kwargs.get("blood_flow_rate", 300),
			"dialysate_flow_rate": kwargs.get("dialysate_flow_rate", 500),
			"ultrafiltration_goal": kwargs.get("ultrafiltration_goal", 2.5),
			"heparin_dose": kwargs.get("heparin_dose", 3000),
			"status": kwargs.get("status", "In Progress"),
		}

		session = frappe.get_doc(session_data)
		session.insert(ignore_permissions=True)
		frappe.db.commit()

		return session

	@staticmethod
	def create_completed_session(patient=None, **kwargs):
		"""Create a completed session with vitals and events"""
		session = SessionFactory.create(patient=patient, status="Completed", **kwargs)

		# Add pre-dialysis vitals
		session.append("vital_signs", {
			"measurement_time": session.start_time,
			"measurement_type": "Pre-Dialysis",
			"systolic_bp": random.randint(130, 160),
			"diastolic_bp": random.randint(80, 100),
			"heart_rate": random.randint(70, 90),
			"temperature": round(random.uniform(36.5, 37.2), 1),
			"weight": round(random.uniform(65, 85), 1),
		})

		# Add post-dialysis vitals
		session.append("vital_signs", {
			"measurement_time": add_to_date(session.start_time, hours=4),
			"measurement_type": "Post-Dialysis",
			"systolic_bp": random.randint(110, 140),
			"diastolic_bp": random.randint(70, 90),
			"heart_rate": random.randint(65, 85),
			"temperature": round(random.uniform(36.3, 37.0), 1),
			"weight": round(random.uniform(63, 83), 1),
		})

		# Add session events
		session.append("session_events", {
			"event_time": add_to_date(session.start_time, hours=2),
			"event_type": "Clinical Note",
			"description": "Patient tolerated treatment well",
			"severity": "Info"
		})

		session.end_time = add_to_date(session.start_time, hours=4)
		session.actual_duration = 240
		session.save(ignore_permissions=True)
		frappe.db.commit()

		return session
