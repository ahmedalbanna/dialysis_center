import frappe
from frappe import _
from frappe.utils import nowdate, getdate, flt, add_days
import json

# Helper function for standardized API responses
def api_response(status="success", data=None, message=""):
	"""Standardized API response format"""
	return {
		"status": status,
		"data": data,
		"message": message
	}

# ==================== MEDICATION LIST & INVENTORY ====================

@frappe.whitelist()
def get_medication_list(filters=None, start=0, page_length=20):
	"""
	Get list of medications with stock information
	
	Args:
		filters (str/dict): Additional filters
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: medications, message}
	"""
	try:
		start = int(start)
		page_length = min(int(page_length), 100)
		
		filter_dict = {}
		if filters:
			if isinstance(filters, str):
				filters = frappe.parse_json(filters)
			filter_dict.update(filters)
		
		medications = frappe.get_all("Medication",
			filters=filter_dict,
			fields=["name", "medication_name", "category", "quantity_on_hand", "reorder_level", 
					"unit", "expiry_date", "manufacturer", "cost_per_unit"],
			order_by="medication_name asc",
			start=start,
			page_length=page_length
		)
		
		frappe.get_logger().info(f"API: get_medication_list - {len(medications)} medications retrieved")
		
		return api_response(data={
			"medications": medications,
			"count": len(medications),
			"total": frappe.db.count("Medication", filter_dict)
		})
	except Exception as e:
		frappe.log_error(f"get_medication_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_medication_details(medication_id):
	"""
	Get medication details with stock information
	
	Args:
		medication_id (str): Medication ID
	
	Returns:
		dict: {status, data: medication_details, message}
	"""
	try:
		if not medication_id:
			return api_response(status="error", message="Medication ID is required")
		
		if not frappe.db.exists("Medication", medication_id):
			return api_response(status="error", message="Medication not found")
		
		medication = frappe.get_doc("Medication", medication_id)
		
		# Get stock movements
		stock_movements = frappe.get_all("Stock Movement",
			filters={"medication": medication_id},
			fields=["name", "movement_date", "quantity", "movement_type", "notes"],
			order_by="movement_date desc",
			limit=10
		)
		
		return api_response(data={
			"medication": medication.as_dict(),
			"stock_movements": stock_movements,
			"is_low_stock": medication.quantity_on_hand <= medication.reorder_level,
			"is_expired": medication.expiry_date and getdate(medication.expiry_date) <= getdate(nowdate())
		})
	except Exception as e:
		frappe.log_error(f"get_medication_details error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def create_stock_movement(medication_id, quantity, movement_type, notes=None):
	"""
	Record stock movement (addition/removal)
	
	Args:
		medication_id (str): Medication ID
		quantity (float): Quantity moved
		movement_type (str): Type (In, Out, Adjustment, Return)
		notes (str): Notes about movement
	
	Returns:
		dict: {status, data: movement, message}
	"""
	try:
		if not all([medication_id, quantity, movement_type]):
			return api_response(status="error", message="medication_id, quantity, and movement_type are required")
		
		if not frappe.db.exists("Medication", medication_id):
			return api_response(status="error", message="Medication not found")
		
		medication = frappe.get_doc("Medication", medication_id)
		quantity = flt(quantity)
		
		if quantity <= 0:
			return api_response(status="error", message="Quantity must be positive")
		
		# Create stock movement
		movement = frappe.get_doc({
			"doctype": "Stock Movement",
			"medication": medication_id,
			"movement_date": nowdate(),
			"quantity": quantity,
			"movement_type": movement_type,
			"notes": notes
		})
		
		movement.insert(ignore_permissions=True)
		
		# Update medication quantity
		if movement_type in ["In", "Return"]:
			medication.quantity_on_hand = flt(medication.quantity_on_hand or 0) + quantity
		elif movement_type in ["Out", "Adjustment"]:
			medication.quantity_on_hand = flt(medication.quantity_on_hand or 0) - quantity
		
		medication.save(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: create_stock_movement - {movement.name} recorded")
		
		return api_response(data={
			"movement": movement.as_dict(),
			"medication_quantity": medication.quantity_on_hand
		}, message="Stock movement recorded successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"create_stock_movement error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_low_stock_items():
	"""
	Get medications below reorder level
	
	Returns:
		dict: {status, data: low_stock_items, message}
	"""
	try:
		# Get all medications below reorder level
		medications = frappe.get_all("Medication",
			fields=["name", "medication_name", "quantity_on_hand", "reorder_level", "unit"],
			order_by="quantity_on_hand asc"
		)
		
		low_stock = [m for m in medications if flt(m.quantity_on_hand) <= flt(m.reorder_level)]
		
		return api_response(data={
			"low_stock_items": low_stock,
			"count": len(low_stock)
		})
	except Exception as e:
		frappe.log_error(f"get_low_stock_items error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def check_medication_expiry():
	"""
	Get medications that are expired or expiring soon
	
	Args:
		days_threshold (int): Days to consider as "expiring soon" (default: 30)
	
	Returns:
		dict: {status, data: expiry_info, message}
	"""
	try:
		medications = frappe.get_all("Medication",
			fields=["name", "medication_name", "expiry_date", "quantity_on_hand"],
			order_by="expiry_date asc"
		)
		
		today = getdate(nowdate())
		expired = []
		expiring_soon = []
		
		for med in medications:
			if med.expiry_date:
				expiry_date = getdate(med.expiry_date)
				if expiry_date < today:
					expired.append(med)
				elif (expiry_date - today).days <= 30:
					expiring_soon.append({
						**med,
						"days_until_expiry": (expiry_date - today).days
					})
		
		return api_response(data={
			"expired": expired,
			"expired_count": len(expired),
			"expiring_soon": expiring_soon,
			"expiring_count": len(expiring_soon)
		})
	except Exception as e:
		frappe.log_error(f"check_medication_expiry error: {str(e)}")
		return api_response(status="error", message=str(e))
