import frappe
from frappe import _
from frappe.utils import nowdate, add_days, getdate
import json

# Helper function for standardized API responses
def api_response(status="success", data=None, message=""):
	"""Standardized API response format"""
	return {
		"status": status,
		"data": data,
		"message": message
	}

# ==================== PATIENT LIST & SEARCH ====================

@frappe.whitelist()
def get_patient_list(filters=None, search_term=None, start=0, page_length=20):
	"""
	Get list of patients with filtering and search
	
	Args:
		filters (str/dict): Additional filters
		search_term (str): Search by name, ID, phone, email
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: [patients], message}
	"""
	try:
		# Validate pagination
		start = int(start)
		page_length = min(int(page_length), 100)  # Max 100 per request
		
		filter_dict = {"status": "Active"}
		
		# Parse filters if string
		if filters:
			if isinstance(filters, str):
				filters = frappe.parse_json(filters)
			filter_dict.update(filters)
		
		# Add search filter
		if search_term:
			patients = frappe.get_all("Patient",
				filters=filter_dict,
				fields=["name", "patient_name", "mobile_number", "national_id", "blood_group", 
						"age", "gender", "status", "creation"],
				order_by="patient_name asc",
				start=start,
				page_length=page_length
			)
			# Further filter by search term in memory (simple approach)
			search_term_lower = search_term.lower()
			patients = [p for p in patients if 
				search_term_lower in (p.patient_name or "").lower() or
				search_term_lower in (p.mobile_number or "") or
				search_term_lower in (p.national_id or "") or
				search_term_lower in p.name.lower()
			]
		else:
			patients = frappe.get_all("Patient",
				filters=filter_dict,
				fields=["name", "patient_name", "mobile_number", "national_id", "blood_group",
						"age", "gender", "status", "creation"],
				order_by="patient_name asc",
				start=start,
				page_length=page_length
			)
		
		# Log API call
		frappe.get_logger().info(f"API: get_patient_list - {len(patients)} patients retrieved")
		
		return api_response(data={
			"patients": patients,
			"count": len(patients),
			"total": frappe.db.count("Patient", filter_dict)
		})
	except Exception as e:
		frappe.log_error(f"get_patient_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_patient_details(patient_id):
	"""
	Get comprehensive patient profile with medical history
	
	Args:
		patient_id (str): Patient ID
	
	Returns:
		dict: {status, data: patient_details, message}
	"""
	try:
		if not patient_id:
			return api_response(status="error", message="Patient ID is required")
		
		if not frappe.db.exists("Patient", patient_id):
			return api_response(status="error", message="Patient not found")
		
		# Check permission
		if not frappe.has_permission("Patient", "read", doc=patient_id):
			return api_response(status="error", message="You do not have permission to view this patient")
		
		patient_doc = frappe.get_doc("Patient", patient_id)
		
		return api_response(data={
			"patient": patient_doc.as_dict(),
			"medical_history": patient_doc.medical_history if hasattr(patient_doc, 'medical_history') else [],
			"total_sessions": frappe.db.count("Dialysis Session", {"patient": patient_id}),
			"total_appointments": frappe.db.count("Appointment", {"patient": patient_id}),
			"total_outstanding": frappe.db.sql(
				"SELECT COALESCE(SUM(outstanding_amount), 0) FROM `tabInvoice` WHERE patient=%s AND payment_status!='Paid'",
				(patient_id,)
			)[0][0]
		})
	except Exception as e:
		frappe.log_error(f"get_patient_details error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def create_patient(patient_name, dob, blood_group, phone, email, medical_history=None, gender=None):
	"""
	Create new patient
	
	Args:
		patient_name (str): Patient name
		dob (str): Date of birth (YYYY-MM-DD)
		blood_group (str): Blood group
		phone (str): Phone number
		email (str): Email address
		medical_history (str/list): Medical history items
		gender (str): Gender
	
	Returns:
		dict: {status, data: patient, message}
	"""
	try:
		# Validate required fields
		if not all([patient_name, dob, blood_group, phone, email]):
			return api_response(status="error", message="patient_name, dob, blood_group, phone, and email are required")
		
		# Parse medical history if string
		if medical_history and isinstance(medical_history, str):
			medical_history = frappe.parse_json(medical_history)
		
		patient_doc = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": patient_name,
			"date_of_birth": dob,
			"blood_group": blood_group,
			"mobile_number": phone,
			"email": email,
			"gender": gender or "Not Specified",
			"status": "Active"
		})
		
		# Add medical history items
		if medical_history and isinstance(medical_history, list):
			for item in medical_history:
				patient_doc.append("medical_history", item)
		
		patient_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: create_patient - {patient_doc.name} created")
		
		return api_response(data=patient_doc.as_dict(), message="Patient created successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"create_patient error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def update_patient(patient_id, **fields):
	"""
	Update patient information
	
	Args:
		patient_id (str): Patient ID
		**fields: Fields to update
	
	Returns:
		dict: {status, data: updated_patient, message}
	"""
	try:
		if not patient_id:
			return api_response(status="error", message="Patient ID is required")
		
		if not frappe.db.exists("Patient", patient_id):
			return api_response(status="error", message="Patient not found")
		
		# Check permission
		if not frappe.has_permission("Patient", "write", doc=patient_id):
			return api_response(status="error", message="You do not have permission to update this patient")
		
		patient_doc = frappe.get_doc("Patient", patient_id)
		
		# Remove non-writable fields
		restricted_fields = ["name", "creation", "modified", "docstatus"]
		for field in restricted_fields:
			fields.pop(field, None)
		
		patient_doc.update(fields)
		patient_doc.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: update_patient - {patient_id} updated")
		
		return api_response(data=patient_doc.as_dict(), message="Patient updated successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"update_patient error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_patient_sessions(patient_id, status=None, from_date=None, to_date=None):
	"""
	Get all dialysis sessions for a patient
	
	Args:
		patient_id (str): Patient ID
		status (str): Filter by status (Scheduled, In Progress, Completed)
		from_date (str): Start date filter
		to_date (str): End date filter
	
	Returns:
		dict: {status, data: sessions, message}
	"""
	try:
		if not patient_id:
			return api_response(status="error", message="Patient ID is required")
		
		filters = {"patient": patient_id}
		if status:
			filters["status"] = status
		if from_date:
			filters["session_date"] = [">=", from_date]
		if to_date:
			if "session_date" in filters:
				filters["session_date"] = ["between", [from_date, to_date]]
			else:
				filters["session_date"] = ["<=", to_date]
		
		sessions = frappe.get_all("Dialysis Session",
			filters=filters,
			fields=["name", "session_date", "status", "pre_dialysis_weight", "post_dialysis_weight",
					"treatment_duration", "dialysis_machine", "complications"],
			order_by="session_date desc"
		)
		
		return api_response(data={
			"patient": patient_id,
			"sessions": sessions,
			"count": len(sessions)
		})
	except Exception as e:
		frappe.log_error(f"get_patient_sessions error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_patient_lab_results(patient_id, test_type=None, from_date=None, to_date=None):
	"""
	Get recent lab results for a patient
	
	Args:
		patient_id (str): Patient ID
		test_type (str): Filter by test type
		from_date (str): Start date filter
		to_date (str): End date filter
	
	Returns:
		dict: {status, data: lab_results, message}
	"""
	try:
		if not patient_id:
			return api_response(status="error", message="Patient ID is required")
		
		filters = {"patient": patient_id}
		if test_type:
			filters["test_type"] = test_type
		if from_date:
			filters["test_date"] = [">=", from_date]
		if to_date:
			if "test_date" in filters:
				filters["test_date"] = ["between", [from_date, to_date]]
			else:
				filters["test_date"] = ["<=", to_date]
		
		lab_tests = frappe.get_all("Lab Test",
			filters=filters,
			fields=["name", "test_date", "test_type", "status", "notes"],
			order_by="test_date desc"
		)
		
		# Get results for each test
		results = []
		for test in lab_tests:
			test_results = frappe.get_all("Lab Result",
				filters={"lab_test": test.name},
				fields=["name", "parameter_name", "result_value", "normal_range", "status"]
			)
			results.append({
				**test,
				"results": test_results
			})
		
		return api_response(data={
			"patient": patient_id,
			"lab_results": results,
			"count": len(results)
		})
	except Exception as e:
		frappe.log_error(f"get_patient_lab_results error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_patient_dashboard(patient):
	"""Get comprehensive patient dashboard data"""
	if not patient:
		frappe.throw(_("Patient is required"))
	
	patient_doc = frappe.get_doc("Patient", patient)
	
	# Get recent sessions
	recent_sessions = frappe.get_all("Dialysis Session",
		filters={"patient": patient},
		fields=["name", "session_date", "status", "treatment_duration", "dialysis_machine"],
		order_by="session_date desc",
		limit=10
	)
	
	# Get upcoming appointments
	upcoming_appointments = frappe.get_all("Appointment",
		filters={
			"patient": patient,
			"appointment_date": [">=", nowdate()],
			"status": ["not in", ["Cancelled", "Completed"]]
		},
		fields=["name", "appointment_date", "appointment_time", "machine", "status"],
		order_by="appointment_date asc",
		limit=5
	)
	
	# Get outstanding invoices
	outstanding_invoices = frappe.get_all("Invoice",
		filters={
			"patient": patient,
			"payment_status": ["!=", "Paid"],
			"docstatus": 1
		},
		fields=["name", "invoice_date", "total_amount", "outstanding_amount", "payment_status"]
	)
	
	total_outstanding = sum([inv.outstanding_amount for inv in outstanding_invoices])
	
	# Get recent lab results
	recent_labs = frappe.get_all("Lab Test",
		filters={"patient": patient},
		fields=["name", "test_date", "test_type", "status"],
		order_by="test_date desc",
		limit=5
	)
	
	return {
		"patient": patient_doc.as_dict(),
		"recent_sessions": recent_sessions,
		"upcoming_appointments": upcoming_appointments,
		"outstanding_invoices": outstanding_invoices,
		"total_outstanding": total_outstanding,
		"recent_labs": recent_labs,
		"statistics": {
			"total_sessions": frappe.db.count("Dialysis Session", {"patient": patient}),
			"completed_sessions": frappe.db.count("Dialysis Session", {"patient": patient, "status": "Completed"}),
			"upcoming_appointments": len(upcoming_appointments),
			"total_outstanding": total_outstanding
		}
	}

@frappe.whitelist()
def get_patient_medical_history(patient):
	"""Get patient's medical history"""
	if not patient:
		frappe.throw(_("Patient is required"))
	
	patient_doc = frappe.get_doc("Patient", patient)
	
	return {
		"patient": patient,
		"patient_name": patient_doc.patient_name,
		"medical_history": patient_doc.medical_history if hasattr(patient_doc, 'medical_history') else [],
		"allergies": [item for item in (patient_doc.medical_history or []) if item.condition_type == "Allergy"],
		"chronic_conditions": [item for item in (patient_doc.medical_history or []) if item.condition_type == "Chronic Condition"],
		"surgeries": [item for item in (patient_doc.medical_history or []) if item.condition_type == "Surgery"]
	}

@frappe.whitelist()
def get_patient_treatment_timeline(patient, from_date=None, to_date=None):
	"""Get patient's treatment timeline"""
	if not patient:
		frappe.throw(_("Patient is required"))
	
	filters = {"patient": patient}
	
	if from_date:
		filters["session_date"] = [">=", from_date]
	if to_date:
		if "session_date" in filters:
			filters["session_date"] = ["between", [from_date, to_date]]
		else:
			filters["session_date"] = ["<=", to_date]
	
	sessions = frappe.get_all("Dialysis Session",
		filters=filters,
		fields=["name", "session_date", "status", "pre_dialysis_weight", "post_dialysis_weight", 
				"weight_loss", "treatment_duration", "complications"],
		order_by="session_date desc"
	)
	
	return {
		"patient": patient,
		"sessions": sessions,
		"total_sessions": len(sessions)
	}

@frappe.whitelist()
def search_patients(query, filters=None):
	"""Search patients by name, ID, or phone"""
	if not query:
		return []
	
	search_filters = filters or {}
	
	# Search in multiple fields
	patients = frappe.db.sql("""
		SELECT name, patient_name, mobile_number, national_id, status, age
		FROM `tabPatient`
		WHERE (patient_name LIKE %(query)s 
			OR mobile_number LIKE %(query)s 
			OR national_id LIKE %(query)s
			OR name LIKE %(query)s)
		ORDER BY patient_name
		LIMIT 20
	""", {"query": f"%{query}%"}, as_dict=True)
	
	return patients

@frappe.whitelist()
def get_patient_vital_trends(patient, days=30):
	"""Get patient's vital signs trends"""
	if not patient:
		frappe.throw(_("Patient is required"))
	
	from_date = add_days(nowdate(), -int(days))
	
	# Get sessions with vital signs
	sessions = frappe.get_all("Dialysis Session",
		filters={
			"patient": patient,
			"session_date": [">=", from_date],
			"status": "Completed"
		},
		fields=["name", "session_date"],
		order_by="session_date asc"
	)
	
	vital_data = []
	for session in sessions:
		# Get vital signs for this session
		vitals = frappe.get_all("Vital Signs Reading",
			filters={"parent": session.name},
			fields=["reading_time", "bp_systolic", "bp_diastolic", "heart_rate", 
					"temperature", "oxygen_saturation"],
			order_by="reading_time asc"
		)
		
		if vitals:
			vital_data.extend([{
				**vital,
				"session": session.name,
				"session_date": session.session_date
			} for vital in vitals])
	
	return {
		"patient": patient,
		"from_date": from_date,
		"to_date": nowdate(),
		"vital_signs": vital_data
	}
