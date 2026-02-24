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

# ==================== MACHINE LIST & MAINTENANCE ====================

@frappe.whitelist()
def get_machine_list(filters=None, start=0, page_length=20):
	"""
	Get list of dialysis machines with filtering
	
	Args:
		filters (str/dict): Additional filters
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: machines, message}
	"""
	try:
		start = int(start)
		page_length = min(int(page_length), 100)
		
		filter_dict = {}
		if filters:
			if isinstance(filters, str):
				filters = frappe.parse_json(filters)
			filter_dict.update(filters)
		
		machines = frappe.get_all("Dialysis Machine",
			filters=filter_dict,
			fields=["name", "machine_name", "machine_type", "status", "location", 
					"manufacturer", "purchase_date", "last_maintenance_date", "next_maintenance_date"],
			order_by="machine_name asc",
			start=start,
			page_length=page_length
		)
		
		frappe.get_logger().info(f"API: get_machine_list - {len(machines)} machines retrieved")
		
		return api_response(data={
			"machines": machines,
			"count": len(machines),
			"total": frappe.db.count("Dialysis Machine", filter_dict)
		})
	except Exception as e:
		frappe.log_error(f"get_machine_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_machine_details(machine_id):
	"""
	Get machine details with status and maintenance info
	
	Args:
		machine_id (str): Machine ID
	
	Returns:
		dict: {status, data: machine_details, message}
	"""
	try:
		if not machine_id:
			return api_response(status="error", message="Machine ID is required")
		
		if not frappe.db.exists("Dialysis Machine", machine_id):
			return api_response(status="error", message="Machine not found")
		
		machine = frappe.get_doc("Dialysis Machine", machine_id)
		
		# Get recent maintenance records
		maintenance_records = frappe.get_all("Machine Maintenance",
			filters={"dialysis_machine": machine_id},
			fields=["name", "maintenance_date", "maintenance_type", "notes", "status"],
			order_by="maintenance_date desc",
			limit=5
		)
		
		return api_response(data={
			"machine": machine.as_dict(),
			"recent_maintenance": maintenance_records,
			"is_due_maintenance": machine.next_maintenance_date and 
				getdate(machine.next_maintenance_date) <= getdate(nowdate()),
			"maintenance_status": "Due" if machine.next_maintenance_date and 
				getdate(machine.next_maintenance_date) <= getdate(nowdate()) else "Scheduled"
		})
	except Exception as e:
		frappe.log_error(f"get_machine_details error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_machine_maintenance_schedule(machine_id):
	"""
	Get upcoming maintenance schedule for a machine
	
	Args:
		machine_id (str): Machine ID
	
	Returns:
		dict: {status, data: maintenance_schedule, message}
	"""
	try:
		if not machine_id:
			return api_response(status="error", message="Machine ID is required")
		
		if not frappe.db.exists("Dialysis Machine", machine_id):
			return api_response(status="error", message="Machine not found")
		
		machine = frappe.get_doc("Dialysis Machine", machine_id)
		
		# Get all maintenance records (past and future)
		maintenance_records = frappe.get_all("Machine Maintenance",
			filters={"dialysis_machine": machine_id},
			fields=["name", "maintenance_date", "maintenance_type", "status", "notes"],
			order_by="maintenance_date desc"
		)
		
		# Separate past and future maintenance
		today = getdate(nowdate())
		past_maintenance = [m for m in maintenance_records if getdate(m.maintenance_date) < today]
		future_maintenance = [m for m in maintenance_records if getdate(m.maintenance_date) >= today]
		
		return api_response(data={
			"machine": machine_id,
			"next_maintenance_date": machine.next_maintenance_date,
			"last_maintenance_date": machine.last_maintenance_date,
			"future_maintenance": future_maintenance,
			"past_maintenance": past_maintenance,
			"total_maintenance": len(maintenance_records)
		})
	except Exception as e:
		frappe.log_error(f"get_machine_maintenance_schedule error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def record_machine_maintenance(machine_id, maintenance_date, maintenance_type, parts=None, notes=None):
	"""
	Record machine maintenance activity
	
	Args:
		machine_id (str): Machine ID
		maintenance_date (str): Maintenance date (YYYY-MM-DD)
		maintenance_type (str): Type (Preventive, Corrective, Emergency)
		parts (str/list): Parts replaced
		notes (str): Maintenance notes
	
	Returns:
		dict: {status, data: maintenance, message}
	"""
	try:
		if not all([machine_id, maintenance_date, maintenance_type]):
			return api_response(status="error", message="machine_id, maintenance_date, and maintenance_type are required")
		
		if not frappe.db.exists("Dialysis Machine", machine_id):
			return api_response(status="error", message="Machine not found")
		
		maintenance = frappe.get_doc({
			"doctype": "Machine Maintenance",
			"dialysis_machine": machine_id,
			"maintenance_date": maintenance_date,
			"maintenance_type": maintenance_type,
			"notes": notes,
			"status": "Completed"
		})
		
		# Add parts if provided
		if parts:
			if isinstance(parts, str):
				parts = frappe.parse_json(parts)
			
			for part in parts:
				maintenance.append("maintenance_parts", {
					"part_name": part.get("part_name"),
					"quantity": part.get("quantity", 1),
					"notes": part.get("notes")
				})
		
		maintenance.insert(ignore_permissions=True)
		
		# Update machine maintenance dates
		machine = frappe.get_doc("Dialysis Machine", machine_id)
		machine.last_maintenance_date = maintenance_date
		# Calculate next maintenance (typically 3 months from now)
		from frappe.utils import add_months
		machine.next_maintenance_date = add_months(getdate(nowdate()), 3)
		machine.status = "Available"
		machine.save(ignore_permissions=True)
		
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: record_machine_maintenance - {maintenance.name} recorded")
		
		return api_response(data=maintenance.as_dict(), message="Maintenance recorded successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"record_machine_maintenance error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_machines_due_maintenance():
	"""
	Get machines that are due for maintenance
	
	Returns:
		dict: {status, data: machines_due, message}
	"""
	try:
		today = getdate(nowdate())
		
		# Get all machines with next maintenance date <= today
		machines = frappe.get_all("Dialysis Machine",
			filters={"status": "Available"},
			fields=["name", "machine_name", "location", "last_maintenance_date", 
					"next_maintenance_date"],
			order_by="next_maintenance_date asc"
		)
		
		# Filter for those due maintenance
		due_maintenance = []
		for machine in machines:
			if machine.next_maintenance_date and getdate(machine.next_maintenance_date) <= today:
				due_maintenance.append({
					**machine,
					"days_overdue": (today - getdate(machine.next_maintenance_date)).days
				})
		
		return api_response(data={
			"machines_due": due_maintenance,
			"count": len(due_maintenance),
			"urgent_count": len([m for m in due_maintenance if m.get("days_overdue", 0) > 30])
		})
	except Exception as e:
		frappe.log_error(f"get_machines_due_maintenance error: {str(e)}")
		return api_response(status="error", message=str(e))
