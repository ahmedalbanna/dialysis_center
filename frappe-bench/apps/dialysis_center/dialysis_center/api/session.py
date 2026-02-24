import frappe
from frappe import _
from frappe.utils import nowdate, now_datetime, time_diff_in_hours, get_datetime, flt
import json

# Helper function for standardized API responses
def api_response(status="success", data=None, message=""):
	"""Standardized API response format"""
	return {
		"status": status,
		"data": data,
		"message": message
	}

# ==================== SESSION LIST & DETAILS ====================

@frappe.whitelist()
def get_session_list(filters=None, start=0, page_length=20):
	"""
	Get list of dialysis sessions with filtering
	
	Args:
		filters (str/dict): Additional filters
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: sessions, message}
	"""
	try:
		start = int(start)
		page_length = min(int(page_length), 100)
		
		filter_dict = {}
		if filters:
			if isinstance(filters, str):
				filters = frappe.parse_json(filters)
			filter_dict.update(filters)
		
		sessions = frappe.get_all("Dialysis Session",
			filters=filter_dict,
			fields=["name", "patient", "patient_name", "session_date", "status", "dialysis_machine",
					"treatment_duration", "pre_dialysis_weight", "post_dialysis_weight"],
			order_by="session_date desc",
			start=start,
			page_length=page_length
		)
		
		frappe.get_logger().info(f"API: get_session_list - {len(sessions)} sessions retrieved")
		
		return api_response(data={
			"sessions": sessions,
			"count": len(sessions),
			"total": frappe.db.count("Dialysis Session", filter_dict)
		})
	except Exception as e:
		frappe.log_error(f"get_session_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_session_details(session_id):
	"""
	Get full dialysis session details
	
	Args:
		session_id (str): Session ID
	
	Returns:
		dict: {status, data: session_details, message}
	"""
	try:
		if not session_id:
			return api_response(status="error", message="Session ID is required")
		
		if not frappe.db.exists("Dialysis Session", session_id):
			return api_response(status="error", message="Session not found")
		
		session = frappe.get_doc("Dialysis Session", session_id)
		
		return api_response(data={
			"session": session.as_dict(),
			"vital_signs": session.vital_signs if hasattr(session, 'vital_signs') else [],
			"session_events": session.session_events if hasattr(session, 'session_events') else [],
			"patient_details": frappe.get_value("Patient", session.patient,
				["patient_name", "blood_group", "age", "date_of_birth"]),
			"machine_details": frappe.get_value("Dialysis Machine", session.dialysis_machine,
				["machine_name", "status", "location"]) if session.dialysis_machine else None
		})
	except Exception as e:
		frappe.log_error(f"get_session_details error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def start_session(session_id):
	"""
	Start a dialysis session
	
	Args:
		session_id (str): Session ID
	
	Returns:
		dict: {status, data: session, message}
	"""
	try:
		if not session_id:
			return api_response(status="error", message="Session ID is required")
		
		if not frappe.db.exists("Dialysis Session", session_id):
			return api_response(status="error", message="Session not found")
		
		session = frappe.get_doc("Dialysis Session", session_id)
		
		if session.status != "Scheduled":
			return api_response(status="error", message=f"Session must be Scheduled to start (current: {session.status})")
		
		session.status = "In Progress"
		session.started_at = now_datetime()
		session.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: start_session - {session_id} started")
		
		return api_response(data=session.as_dict(), message="Session started successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"start_session error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def end_session(session_id, vital_signs=None):
	"""
	End dialysis session with final vital signs
	
	Args:
		session_id (str): Session ID
		vital_signs (str/dict): Final vital signs data
	
	Returns:
		dict: {status, data: session, message}
	"""
	try:
		if not session_id:
			return api_response(status="error", message="Session ID is required")
		
		if not frappe.db.exists("Dialysis Session", session_id):
			return api_response(status="error", message="Session not found")
		
		session = frappe.get_doc("Dialysis Session", session_id)
		
		if session.status != "In Progress":
			return api_response(status="error", message=f"Session must be In Progress to end (current: {session.status})")
		
		# Add final vital signs if provided
		if vital_signs:
			if isinstance(vital_signs, str):
				vital_signs = frappe.parse_json(vital_signs)
			
			vital_row = session.append("vital_signs", {
				"reading_time": vital_signs.get("reading_time") or now_datetime(),
				"bp_systolic": vital_signs.get("bp_systolic"),
				"bp_diastolic": vital_signs.get("bp_diastolic"),
				"heart_rate": vital_signs.get("heart_rate"),
				"temperature": vital_signs.get("temperature"),
				"respiratory_rate": vital_signs.get("respiratory_rate"),
				"oxygen_saturation": vital_signs.get("oxygen_saturation"),
				"blood_flow_rate": vital_signs.get("blood_flow_rate"),
				"dialysate_flow_rate": vital_signs.get("dialysate_flow_rate"),
				"venous_pressure": vital_signs.get("venous_pressure"),
				"transmembrane_pressure": vital_signs.get("transmembrane_pressure"),
				"uf_removed": vital_signs.get("uf_removed"),
				"uf_rate": vital_signs.get("uf_rate")
			})
		
		session.status = "Completed"
		session.completed_at = now_datetime()
		
		# Calculate actual duration
		if session.started_at and session.completed_at:
			duration_hours = time_diff_in_hours(session.completed_at, session.started_at)
			session.actual_duration = int(duration_hours * 60)  # Convert to minutes
		
		session.save(ignore_permissions=True)
		
		# Submit the session
		if session.docstatus == 0:
			session.submit()
		
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: end_session - {session_id} completed")
		
		return api_response(data=session.as_dict(), message="Session ended and submitted successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"end_session error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def record_vital_signs(session_id, vital_signs_data):
	"""
	Record vital signs during a session
	
	Args:
		session_id (str): Session ID
		vital_signs_data (str/dict): Vital signs reading data
	
	Returns:
		dict: {status, data: vital_reading, message}
	"""
	try:
		if not session_id:
			return api_response(status="error", message="Session ID is required")
		
		if not vital_signs_data:
			return api_response(status="error", message="vital_signs_data is required")
		
		if not frappe.db.exists("Dialysis Session", session_id):
			return api_response(status="error", message="Session not found")
		
		if isinstance(vital_signs_data, str):
			vital_signs_data = frappe.parse_json(vital_signs_data)
		
		session = frappe.get_doc("Dialysis Session", session_id)
		
		if session.status not in ["Scheduled", "In Progress"]:
			return api_response(status="error", message=f"Cannot record vitals for session with status {session.status}")
		
		vital_row = session.append("vital_signs", {
			"reading_time": vital_signs_data.get("reading_time") or now_datetime(),
			"bp_systolic": vital_signs_data.get("bp_systolic"),
			"bp_diastolic": vital_signs_data.get("bp_diastolic"),
			"heart_rate": vital_signs_data.get("heart_rate"),
			"temperature": vital_signs_data.get("temperature"),
			"respiratory_rate": vital_signs_data.get("respiratory_rate"),
			"oxygen_saturation": vital_signs_data.get("oxygen_saturation"),
			"blood_flow_rate": vital_signs_data.get("blood_flow_rate"),
			"dialysate_flow_rate": vital_signs_data.get("dialysate_flow_rate"),
			"venous_pressure": vital_signs_data.get("venous_pressure"),
			"transmembrane_pressure": vital_signs_data.get("transmembrane_pressure"),
			"uf_removed": vital_signs_data.get("uf_removed"),
			"uf_rate": vital_signs_data.get("uf_rate")
		})
		
		session.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: record_vital_signs - {session_id} vital recorded")
		
		return api_response(data=vital_row, message="Vital signs recorded successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"record_vital_signs error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_session_events(session_id):
	"""
	Get all events logged during a session
	
	Args:
		session_id (str): Session ID
	
	Returns:
		dict: {status, data: events, message}
	"""
	try:
		if not session_id:
			return api_response(status="error", message="Session ID is required")
		
		if not frappe.db.exists("Dialysis Session", session_id):
			return api_response(status="error", message="Session not found")
		
		session = frappe.get_doc("Dialysis Session", session_id)
		
		return api_response(data={
			"session": session_id,
			"events": session.session_events if hasattr(session, 'session_events') else [],
			"count": len(session.session_events) if hasattr(session, 'session_events') else 0
		})
	except Exception as e:
		frappe.log_error(f"get_session_events error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def start_session(session):
	"""Start a dialysis session"""
	if not session:
		frappe.throw(_("Session is required"))
	
	doc = frappe.get_doc("Dialysis Session", session)
	
	if doc.status != "Scheduled":
		frappe.throw(_("Session must be in Scheduled status to start"))
	
	doc.status = "In Progress"
	doc.started_at = now_datetime()
	doc.save(ignore_permissions=True)
	
	return doc

@frappe.whitelist()
def complete_session(session):
	"""Complete a dialysis session"""
	if not session:
		frappe.throw(_("Session is required"))
	
	doc = frappe.get_doc("Dialysis Session", session)
	
	if doc.status != "In Progress":
		frappe.throw(_("Session must be in progress to complete"))
	
	if not doc.post_dialysis_weight:
		frappe.throw(_("Post-dialysis weight is required"))
	
	doc.status = "Completed"
	doc.completed_at = now_datetime()
	
	# Calculate actual duration
	if doc.started_at and doc.completed_at:
		duration_hours = time_diff_in_hours(doc.completed_at, doc.started_at)
		doc.actual_duration = int(duration_hours * 60)  # Convert to minutes
	
	doc.save(ignore_permissions=True)
	
	# Submit the document
	if doc.docstatus == 0:
		doc.submit()
	
	return doc

@frappe.whitelist()
def add_vital_reading(session, vital_data):
	"""Add a vital signs reading to a session"""
	import json
	
	if not session:
		frappe.throw(_("Session is required"))
	
	if isinstance(vital_data, str):
		vital_data = json.loads(vital_data)
	
	doc = frappe.get_doc("Dialysis Session", session)
	
	vital_row = doc.append("vital_signs", {
		"reading_time": vital_data.get("reading_time") or now_datetime(),
		"bp_systolic": vital_data.get("bp_systolic"),
		"bp_diastolic": vital_data.get("bp_diastolic"),
		"heart_rate": vital_data.get("heart_rate"),
		"temperature": vital_data.get("temperature"),
		"respiratory_rate": vital_data.get("respiratory_rate"),
		"oxygen_saturation": vital_data.get("oxygen_saturation"),
		"blood_flow_rate": vital_data.get("blood_flow_rate"),
		"dialysate_flow_rate": vital_data.get("dialysate_flow_rate"),
		"venous_pressure": vital_data.get("venous_pressure"),
		"transmembrane_pressure": vital_data.get("transmembrane_pressure"),
		"uf_removed": vital_data.get("uf_removed"),
		"uf_rate": vital_data.get("uf_rate")
	})
	
	doc.save(ignore_permissions=True)
	
	return vital_row

@frappe.whitelist()
def log_session_event(session, event_data):
	"""Log an event during a dialysis session"""
	import json
	
	if not session:
		frappe.throw(_("Session is required"))
	
	if isinstance(event_data, str):
		event_data = json.loads(event_data)
	
	doc = frappe.get_doc("Dialysis Session", session)
	
	event_row = doc.append("session_events", {
		"event_time": event_data.get("event_time") or now_datetime(),
		"event_type": event_data.get("event_type"),
		"severity": event_data.get("severity", "Low"),
		"description": event_data.get("description"),
		"action_taken": event_data.get("action_taken"),
		"handled_by": event_data.get("handled_by"),
		"notes": event_data.get("notes")
	})
	
	doc.save(ignore_permissions=True)
	
	return event_row

@frappe.whitelist()
def get_active_sessions():
	"""Get all active (in progress) sessions"""
	sessions = frappe.get_all("Dialysis Session",
		filters={"status": "In Progress"},
		fields=["name", "patient", "patient_name", "session_date", "started_at", 
				"dialysis_machine", "treatment_duration"],
		order_by="started_at desc"
	)
	
	# Calculate elapsed time for each session
	for session in sessions:
		if session.started_at:
			elapsed = time_diff_in_hours(now_datetime(), session.started_at)
			session["elapsed_minutes"] = int(elapsed * 60)
			session["progress_percent"] = min(100, (session["elapsed_minutes"] / session.treatment_duration) * 100)
	
	return sessions

@frappe.whitelist()
def get_session_vital_history(session):
	"""Get vital signs history for a session"""
	if not session:
		frappe.throw(_("Session is required"))
	
	doc = frappe.get_doc("Dialysis Session", session)
	
	return {
		"session": session,
		"patient": doc.patient,
		"vital_signs": doc.vital_signs,
		"session_events": doc.session_events
	}

@frappe.whitelist()
def get_session_statistics(from_date=None, to_date=None):
	"""Get session statistics"""
	filters = {}
	
	if from_date:
		filters["session_date"] = [">=", from_date]
	if to_date:
		if "session_date" in filters:
			filters["session_date"] = ["between", [from_date, to_date]]
		else:
			filters["session_date"] = ["<=", to_date]
	
	total_sessions = frappe.db.count("Dialysis Session", filters)
	completed_sessions = frappe.db.count("Dialysis Session", {**filters, "status": "Completed"})
	in_progress = frappe.db.count("Dialysis Session", {**filters, "status": "In Progress"})
	scheduled = frappe.db.count("Dialysis Session", {**filters, "status": "Scheduled"})
	
	# Get sessions with complications
	with_complications = frappe.db.count("Dialysis Session", {
		**filters,
		"complications": ["is", "set"]
	})
	
	return {
		"total_sessions": total_sessions,
		"completed_sessions": completed_sessions,
		"in_progress": in_progress,
		"scheduled": scheduled,
		"with_complications": with_complications,
		"completion_rate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
	}
