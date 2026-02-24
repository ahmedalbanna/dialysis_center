import frappe
from frappe import _
from frappe.utils import nowdate, add_days, getdate, get_datetime, time_diff_in_hours, flt
from datetime import datetime, timedelta
import json

# Helper function for standardized API responses
def api_response(status="success", data=None, message=""):
	"""Standardized API response format"""
	return {
		"status": status,
		"data": data,
		"message": message
	}

# ==================== APPOINTMENT LIST & DETAILS ====================

@frappe.whitelist()
def get_appointment_list(filters=None, start=0, page_length=20):
	"""
	Get list of appointments with filtering
	
	Args:
		filters (str/dict): Additional filters
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: appointments, message}
	"""
	try:
		start = int(start)
		page_length = min(int(page_length), 100)
		
		filter_dict = {}
		if filters:
			if isinstance(filters, str):
				filters = frappe.parse_json(filters)
			filter_dict.update(filters)
		
		appointments = frappe.get_all("Appointment",
			filters=filter_dict,
			fields=["name", "patient", "patient_name", "appointment_date", "appointment_time", 
					"machine", "status", "duration", "checked_in_time"],
			order_by="appointment_date desc, appointment_time desc",
			start=start,
			page_length=page_length
		)
		
		frappe.get_logger().info(f"API: get_appointment_list - {len(appointments)} appointments retrieved")
		
		return api_response(data={
			"appointments": appointments,
			"count": len(appointments),
			"total": frappe.db.count("Appointment", filter_dict)
		})
	except Exception as e:
		frappe.log_error(f"get_appointment_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_appointment_details(appointment_id):
	"""
	Get full appointment information
	
	Args:
		appointment_id (str): Appointment ID
	
	Returns:
		dict: {status, data: appointment_details, message}
	"""
	try:
		if not appointment_id:
			return api_response(status="error", message="Appointment ID is required")
		
		if not frappe.db.exists("Appointment", appointment_id):
			return api_response(status="error", message="Appointment not found")
		
		appointment = frappe.get_doc("Appointment", appointment_id)
		
		return api_response(data={
			"appointment": appointment.as_dict(),
			"patient_details": frappe.get_value("Patient", appointment.patient, 
				["patient_name", "blood_group", "age", "mobile_number", "email"]),
			"machine_details": frappe.get_value("Dialysis Machine", appointment.machine,
				["machine_name", "status", "location"]) if appointment.machine else None
		})
	except Exception as e:
		frappe.log_error(f"get_appointment_details error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def create_appointment(patient_id, appointment_date, machine_id, duration=240):
	"""
	Create new appointment
	
	Args:
		patient_id (str): Patient ID
		appointment_date (str): Appointment date (YYYY-MM-DD)
		machine_id (str): Dialysis machine ID
		duration (int): Duration in minutes
	
	Returns:
		dict: {status, data: appointment, message}
	"""
	try:
		if not all([patient_id, appointment_date, machine_id]):
			return api_response(status="error", message="patient_id, appointment_date, and machine_id are required")
		
		# Validate patient exists
		if not frappe.db.exists("Patient", patient_id):
			return api_response(status="error", message="Patient not found")
		
		# Validate machine exists and available
		if not frappe.db.exists("Dialysis Machine", machine_id):
			return api_response(status="error", message="Machine not found")
		
		# Check if machine already booked for this date
		existing = frappe.db.count("Appointment", {
			"machine": machine_id,
			"appointment_date": appointment_date,
			"status": ["not in", ["Cancelled", "Completed"]]
		})
		
		if existing > 0:
			return api_response(status="error", message="Machine already booked for this date")
		
		appointment = frappe.get_doc({
			"doctype": "Appointment",
			"patient": patient_id,
			"appointment_date": appointment_date,
			"appointment_time": "08:00:00",
			"machine": machine_id,
			"duration": int(duration),
			"status": "Scheduled"
		})
		
		appointment.insert(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: create_appointment - {appointment.name} created")
		
		return api_response(data=appointment.as_dict(), message="Appointment created successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"create_appointment error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def update_appointment(appointment_id, **fields):
	"""
	Update appointment information
	
	Args:
		appointment_id (str): Appointment ID
		**fields: Fields to update
	
	Returns:
		dict: {status, data: appointment, message}
	"""
	try:
		if not appointment_id:
			return api_response(status="error", message="Appointment ID is required")
		
		if not frappe.db.exists("Appointment", appointment_id):
			return api_response(status="error", message="Appointment not found")
		
		appointment = frappe.get_doc("Appointment", appointment_id)
		
		# Remove restricted fields
		restricted_fields = ["name", "creation", "modified", "docstatus"]
		for field in restricted_fields:
			fields.pop(field, None)
		
		appointment.update(fields)
		appointment.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: update_appointment - {appointment_id} updated")
		
		return api_response(data=appointment.as_dict(), message="Appointment updated successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"update_appointment error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def check_machine_availability(machine_id, date, time=None):
	"""
	Check if machine is available for appointment
	
	Args:
		machine_id (str): Machine ID
		date (str): Date to check (YYYY-MM-DD)
		time (str): Time to check (HH:MM:SS, optional)
	
	Returns:
		dict: {status, data: {available: bool, reason: str}, message}
	"""
	try:
		if not all([machine_id, date]):
			return api_response(status="error", message="machine_id and date are required")
		
		# Check if machine exists
		if not frappe.db.exists("Dialysis Machine", machine_id):
			return api_response(status="error", message="Machine not found")
		
		# Check machine status
		machine = frappe.get_value("Dialysis Machine", machine_id, ["status", "next_maintenance_date"])
		if machine[0] != "Available":
			return api_response(data={
				"available": False,
				"reason": f"Machine status is {machine[0]}"
			})
		
		# Check for scheduled maintenance
		if machine[1] and getdate(machine[1]) == getdate(date):
			return api_response(data={
				"available": False,
				"reason": "Machine scheduled for maintenance on this date"
			})
		
		# Check existing appointments
		existing = frappe.db.count("Appointment", {
			"machine": machine_id,
			"appointment_date": date,
			"status": ["not in", ["Cancelled", "Completed"]]
		})
		
		if existing > 0:
			return api_response(data={
				"available": False,
				"reason": "Machine already booked for this date"
			})
		
		return api_response(data={
			"available": True,
			"reason": "Machine is available"
		})
	except Exception as e:
		frappe.log_error(f"check_machine_availability error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def check_in_appointment(appointment_id):
	"""
	Check in patient for appointment
	
	Args:
		appointment_id (str): Appointment ID
	
	Returns:
		dict: {status, data: appointment, message}
	"""
	try:
		if not appointment_id:
			return api_response(status="error", message="Appointment ID is required")
		
		if not frappe.db.exists("Appointment", appointment_id):
			return api_response(status="error", message="Appointment not found")
		
		appointment = frappe.get_doc("Appointment", appointment_id)
		
		if appointment.status in ["Completed", "Cancelled"]:
			return api_response(status="error", message=f"Cannot check in appointment with status {appointment.status}")
		
		appointment.status = "Checked In"
		appointment.checked_in_time = frappe.utils.now_datetime()
		appointment.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: check_in_appointment - {appointment_id} checked in")
		
		return api_response(data=appointment.as_dict(), message="Appointment check-in successful")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"check_in_appointment error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_available_slots(date, machine=None, duration=240):
	"""Get available time slots for a given date and machine"""
	if not date:
		frappe.throw(_("Date is required"))
	
	duration = int(duration)
	
	# Define shift timings (can be made configurable)
	shifts = [
		{"time": "08:00:00", "label": "Morning Shift (8:00 AM)"},
		{"time": "14:00:00", "label": "Afternoon Shift (2:00 PM)"},
		{"time": "20:00:00", "label": "Evening Shift (8:00 PM)"}
	]
	
	available_slots = []
	
	# Get all machines if not specified
	machines = [machine] if machine else [m.name for m in frappe.get_all("Dialysis Machine", 
		filters={"status": "Available"}, fields=["name"])]
	
	for m in machines:
		for shift in shifts:
			# Check if slot is available
			is_available = check_slot_availability(date, m, shift["time"], duration)
			
			if is_available:
				available_slots.append({
					"machine": m,
					"date": date,
					"time": shift["time"],
					"label": shift["label"],
					"duration": duration
				})
	
	return available_slots

def check_slot_availability(date, machine, time, duration):
	"""Check if a specific slot is available"""
	# Get existing appointments for this slot
	existing = frappe.db.count("Appointment", {
		"appointment_date": date,
		"machine": machine,
		"appointment_time": time,
		"status": ["not in", ["Cancelled", "Completed"]]
	})
	
	return existing == 0

@frappe.whitelist()
def bulk_schedule_appointments(patient, start_date, frequency="3x per week", duration=240, machine=None, weeks=4):
	"""Bulk schedule appointments for a patient"""
	if not patient or not start_date:
		frappe.throw(_("Patient and start date are required"))
	
	frequency = int(frequency.split('x')[0]) if 'x' in frequency else 3
	weeks = int(weeks)
	duration = int(duration)
	
	appointments = []
	current_date = getdate(start_date)
	end_date = add_days(current_date, weeks * 7)
	
	# Determine days of week (e.g., Monday, Wednesday, Friday for 3x per week)
	days_map = {
		2: [0, 3],  # Monday, Thursday
		3: [0, 2, 4],  # Monday, Wednesday, Friday
		4: [0, 2, 4, 6]  # Monday, Wednesday, Friday, Sunday
	}
	
	target_days = days_map.get(frequency, [0, 2, 4])
	
	while current_date <= end_date:
		if current_date.weekday() in target_days:
			# Try to create appointment
			try:
				appt = frappe.get_doc({
					"doctype": "Appointment",
					"patient": patient,
					"appointment_date": current_date,
					"appointment_time": "08:00:00",  # Default to morning
					"duration": duration,
					"machine": machine,
					"status": "Scheduled"
				})
				appt.insert(ignore_permissions=True)
				appointments.append(appt.name)
			except Exception as e:
				frappe.log_error(message=str(e), title=f"Failed to create appointment for {current_date}")
		
		current_date = add_days(current_date, 1)
	
	return {
		"created": len(appointments),
		"appointments": appointments
	}

@frappe.whitelist()
def get_daily_schedule(date=None):
	"""Get daily appointment schedule"""
	if not date:
		date = nowdate()
	
	appointments = frappe.get_all("Appointment",
		filters={"appointment_date": date},
		fields=["name", "patient", "patient_name", "appointment_time", "duration", 
				"machine", "status", "assigned_staff"],
		order_by="appointment_time asc"
	)
	
	# Group by time slots
	schedule = {}
	for appt in appointments:
		time_slot = appt.appointment_time
		if time_slot not in schedule:
			schedule[time_slot] = []
		schedule[time_slot].append(appt)
	
	return {
		"date": date,
		"total_appointments": len(appointments),
		"schedule": schedule,
		"appointments": appointments
	}

@frappe.whitelist()
def check_in_appointment(appointment):
	"""Check in a patient for their appointment"""
	if not appointment:
		frappe.throw(_("Appointment is required"))
	
	doc = frappe.get_doc("Appointment", appointment)
	doc.status = "Checked In"
	doc.checked_in_time = frappe.utils.now_datetime()
	doc.save(ignore_permissions=True)
	
	return doc

@frappe.whitelist()
def cancel_appointment(appointment, reason):
	"""Cancel an appointment"""
	if not appointment:
		frappe.throw(_("Appointment is required"))
	
	doc = frappe.get_doc("Appointment", appointment)
	doc.status = "Cancelled"
	doc.notes = (doc.notes or "") + f"\nCancelled: {reason}"
	doc.save(ignore_permissions=True)
	
	return doc

@frappe.whitelist()
def reschedule_appointment(appointment, new_date, new_time):
	"""Reschedule an appointment"""
	if not appointment or not new_date or not new_time:
		frappe.throw(_("Appointment, new date and new time are required"))
	
	doc = frappe.get_doc("Appointment", appointment)
	
	old_date = doc.appointment_date
	old_time = doc.appointment_time
	
	doc.appointment_date = new_date
	doc.appointment_time = new_time
	doc.notes = (doc.notes or "") + f"\nRescheduled from {old_date} {old_time} to {new_date} {new_time}"
	doc.save(ignore_permissions=True)
	
	return doc
