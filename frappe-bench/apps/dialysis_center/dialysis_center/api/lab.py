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

# ==================== LAB TEST LIST & RESULTS ====================

@frappe.whitelist()
def get_lab_test_list(filters=None, start=0, page_length=20):
	"""
	Get list of lab tests with filtering
	
	Args:
		filters (str/dict): Additional filters
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		dict: {status, data: tests, message}
	"""
	try:
		start = int(start)
		page_length = min(int(page_length), 100)
		
		filter_dict = {}
		if filters:
			if isinstance(filters, str):
				filters = frappe.parse_json(filters)
			filter_dict.update(filters)
		
		tests = frappe.get_all("Lab Test",
			filters=filter_dict,
			fields=["name", "patient", "patient_name", "test_date", "test_type", "status", "notes"],
			order_by="test_date desc",
			start=start,
			page_length=page_length
		)
		
		frappe.get_logger().info(f"API: get_lab_test_list - {len(tests)} tests retrieved")
		
		return api_response(data={
			"tests": tests,
			"count": len(tests),
			"total": frappe.db.count("Lab Test", filter_dict)
		})
	except Exception as e:
		frappe.log_error(f"get_lab_test_list error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def create_lab_test(patient_id, test_type, test_date=None):
	"""
	Create lab test order
	
	Args:
		patient_id (str): Patient ID
		test_type (str): Type of test (e.g., Creatinine, Potassium, Hemoglobin)
		test_date (str): Test date (YYYY-MM-DD)
	
	Returns:
		dict: {status, data: test, message}
	"""
	try:
		if not all([patient_id, test_type]):
			return api_response(status="error", message="patient_id and test_type are required")
		
		if not frappe.db.exists("Patient", patient_id):
			return api_response(status="error", message="Patient not found")
		
		patient = frappe.get_value("Patient", patient_id, ["patient_name"])
		
		lab_test = frappe.get_doc({
			"doctype": "Lab Test",
			"patient": patient_id,
			"patient_name": patient[0],
			"test_date": test_date or nowdate(),
			"test_type": test_type,
			"status": "Pending"
		})
		
		lab_test.insert(ignore_permissions=True)
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: create_lab_test - {lab_test.name} created")
		
		return api_response(data=lab_test.as_dict(), message="Lab test created successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"create_lab_test error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def submit_lab_test(lab_test_id, results=None):
	"""
	Submit lab test results
	
	Args:
		lab_test_id (str): Lab test ID
		results (str/list): Test results with parameters
	
	Returns:
		dict: {status, data: test, message}
	"""
	try:
		if not lab_test_id:
			return api_response(status="error", message="Lab test ID is required")
		
		if not frappe.db.exists("Lab Test", lab_test_id):
			return api_response(status="error", message="Lab test not found")
		
		lab_test = frappe.get_doc("Lab Test", lab_test_id)
		
		# Add results if provided
		if results:
			if isinstance(results, str):
				results = frappe.parse_json(results)
			
			for result in results:
				lab_test.append("lab_test_parameters", {
					"parameter_name": result.get("parameter_name"),
					"result_value": result.get("result_value"),
					"normal_range": result.get("normal_range"),
					"unit": result.get("unit"),
					"status": result.get("status", "Normal")
				})
		
		lab_test.status = "Completed"
		lab_test.save(ignore_permissions=True)
		
		if lab_test.docstatus == 0:
			lab_test.submit()
		
		frappe.db.commit()
		
		frappe.get_logger().info(f"API: submit_lab_test - {lab_test_id} submitted")
		
		return api_response(data=lab_test.as_dict(), message="Lab test results submitted successfully")
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"submit_lab_test error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_lab_results(patient_id, test_type=None, from_date=None, to_date=None):
	"""
	Get lab test results for a patient with filtering
	
	Args:
		patient_id (str): Patient ID
		test_type (str): Filter by test type
		from_date (str): Start date filter (YYYY-MM-DD)
		to_date (str): End date filter (YYYY-MM-DD)
	
	Returns:
		dict: {status, data: results, message}
	"""
	try:
		if not patient_id:
			return api_response(status="error", message="Patient ID is required")
		
		filters = {"patient": patient_id, "status": "Completed"}
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
			test_results = frappe.get_all("Lab Test Parameter",
				filters={"parent": test.name},
				fields=["parameter_name", "result_value", "normal_range", "unit", "status"]
			)
			results.append({
				**test,
				"parameters": test_results
			})
		
		return api_response(data={
			"patient": patient_id,
			"test_type_filter": test_type or "All",
			"results": results,
			"count": len(results)
		})
	except Exception as e:
		frappe.log_error(f"get_lab_results error: {str(e)}")
		return api_response(status="error", message=str(e))

@frappe.whitelist()
def get_trending_results(patient_id, test_type, days=90):
	"""
	Get trending lab results for analysis
	
	Args:
		patient_id (str): Patient ID
		test_type (str): Test type to trend
		days (int): Number of days to look back
	
	Returns:
		dict: {status, data: trending_data, message}
	"""
	try:
		if not all([patient_id, test_type]):
			return api_response(status="error", message="patient_id and test_type are required")
		
		from frappe.utils import add_days
		from_date = add_days(nowdate(), -int(days))
		
		filters = {
			"patient": patient_id,
			"test_type": test_type,
			"status": "Completed",
			"test_date": [">=", from_date]
		}
		
		lab_tests = frappe.get_all("Lab Test",
			filters=filters,
			fields=["name", "test_date"],
			order_by="test_date asc"
		)
		
		# Collect trending data
		trending_data = []
		for test in lab_tests:
			parameters = frappe.get_all("Lab Test Parameter",
				filters={"parent": test.name},
				fields=["parameter_name", "result_value", "unit"]
			)
			trending_data.append({
				"test_date": test.test_date,
				"parameters": parameters
			})
		
		return api_response(data={
			"patient": patient_id,
			"test_type": test_type,
			"period_days": days,
			"from_date": from_date,
			"to_date": nowdate(),
			"trending_data": trending_data,
			"count": len(trending_data)
		})
	except Exception as e:
		frappe.log_error(f"get_trending_results error: {str(e)}")
		return api_response(status="error", message=str(e))
