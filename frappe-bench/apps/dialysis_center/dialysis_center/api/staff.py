import frappe
from frappe import _
from frappe.utils import nowdate, getdate
import json

# Helper function for standardized API responses
def api_response(status="success", data=None, message=""):
	"""Standardized API response format"""
	return {
		"status": status,
		"data": data,
		"message": message
	}

# ==================== STAFF LIST & MANAGEMENT ====================

@frappe.whitelist()
def get_staff_list(filters=None, start=0, page_length=20):
	"""
	Get list of staff members with filtering
	
	Args:
		filters (str/dict): Additional filters (department, status, role)
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: staff, message}
	"""
	try:
		start = int(start)
		page_length = min(int(page_length), 100)
		
		filter_dict = {"status": "Active"}
		if filters:
			if isinstance(filters, str):
				filters = frappe.parse_json(filters)
			filter_dict.update(filters)
		
		staff = frappe.get_all("Staff",
			filters=filter_dict,
			fields=["name", "staff_name", "staff_role", "department", "phone_number", 
					"email", "status", "hire_date"],
			order_by="staff_name asc",
			start=start,
			page_length=page_length
		)
		
		frappe.get_logger().info(f"API: get_staff_list - {len(staff)} staff retrieved")
		
		return api_response(data={
			"staff": staff,
			"count": len(staff),
			"total": frappe.db.count("Staff", filter_dict)
		})
	except Exception as e:
		frappe.log_error(f"get_staff_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_staff_details(staff_id):
	"""
	Get detailed staff information
	
	Args:
		staff_id (str): Staff ID
	
	Returns:
		dict: {status, data: staff_details, message}
	"""
	try:
		if not staff_id:
			return api_response(status="error", message="Staff ID is required")
		
		if not frappe.db.exists("Staff", staff_id):
			return api_response(status="error", message="Staff not found")
		
		staff = frappe.get_doc("Staff", staff_id)
		
		# Get assigned shifts
		shifts = frappe.get_all("Shift",
			filters={"staff": staff_id},
			fields=["name", "shift_date", "shift_type", "start_time", "end_time", "status"],
			order_by="shift_date desc",
			limit=10
		)
		
		return api_response(data={
			"staff": staff.as_dict(),
			"recent_shifts": shifts,
			"total_shifts": frappe.db.count("Shift", {"staff": staff_id}),
			"current_status": staff.status
		})
	except Exception as e:
		frappe.log_error(f"get_staff_details error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_staff_shifts(staff_id, from_date=None, to_date=None):
	"""
	Get staff shift schedule
	
	Args:
		staff_id (str): Staff ID
		from_date (str): Start date filter (YYYY-MM-DD)
		to_date (str): End date filter (YYYY-MM-DD)
	
	Returns:
		dict: {status, data: shifts, message}
	"""
	try:
		if not staff_id:
			return api_response(status="error", message="Staff ID is required")
		
		if not frappe.db.exists("Staff", staff_id):
			return api_response(status="error", message="Staff not found")
		
		filters = {"staff": staff_id}
		if from_date:
			filters["shift_date"] = [">=", from_date]
		if to_date:
			if "shift_date" in filters:
				filters["shift_date"] = ["between", [from_date, to_date]]
			else:
				filters["shift_date"] = ["<=", to_date]
		
		shifts = frappe.get_all("Shift",
			filters=filters,
			fields=["name", "shift_date", "shift_type", "start_time", "end_time", 
					"status", "notes"],
			order_by="shift_date asc"
		)
		
		return api_response(data={
			"staff": staff_id,
			"shifts": shifts,
			"count": len(shifts)
		})
	except Exception as e:
		frappe.log_error(f"get_staff_shifts error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_available_staff(date, shift_type=None):
	"""
	Get available staff for a specific date and shift
	
	Args:
		date (str): Date to check (YYYY-MM-DD)
		shift_type (str): Shift type (Morning, Afternoon, Evening)
	
	Returns:
		dict: {status, data: available_staff, message}
	"""
	try:
		if not date:
			return api_response(status="error", message="Date is required")
		
		# Get all active staff
		all_staff = frappe.get_all("Staff",
			filters={"status": "Active"},
			fields=["name", "staff_name", "staff_role", "department"]
		)
		
		# Get assigned shifts for this date
		assigned_filters = {"shift_date": date}
		if shift_type:
			assigned_filters["shift_type"] = shift_type
		
		assigned_shifts = frappe.get_all("Shift",
			filters=assigned_filters,
			fields=["staff"]
		)
		
		assigned_staff_ids = [s.staff for s in assigned_shifts]
		available_staff = [s for s in all_staff if s.name not in assigned_staff_ids]
		
		return api_response(data={
			"date": date,
			"shift_type": shift_type or "Any",
			"available_staff": available_staff,
			"count": len(available_staff)
		})
	except Exception as e:
		frappe.log_error(f"get_available_staff error: {str(e)}")
		return api_response(status="error", message=str(e))
