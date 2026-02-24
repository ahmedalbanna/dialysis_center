# API Whitelister Memory File

## Quick Facts
- **Specialty**: Creating server-side API methods with @frappe.whitelist() decorator, authentication, permissions, and REST API design
- **Primary Tools**: File creation/editing, bash for testing APIs
- **Common Tasks**: API endpoint creation, permission checking, authentication flows, error handling, API documentation
- **Estimated Task Time**: 20-30 minutes per endpoint

---

## Most Common Patterns (80% of work)

### Pattern 1: Simple Whitelisted GET API

**Scenario**: Create an API to fetch a list of orders for the current user.

```python
# File: apps/myapp/myapp/api/order_api.py
import frappe
from frappe.utils import get_safe_limit

@frappe.whitelist()
def get_my_orders(filters=None, start=0, page_length=20):
	"""
	GET /api/method/myapp.api.order_api.get_my_orders
	
	Fetch orders for the current user
	
	Args:
		filters (dict): Additional filters
		start (int): Pagination start
		page_length (int): Items per page
	
	Returns:
		list: Order documents
	"""
	# Validate pagination
	page_length = get_safe_limit(page_length)
	
	# Build filters - only user's orders
	filter_dict = {
		"owner": frappe.session.user,
		"docstatus": 1  # Only submitted orders
	}
	
	# Add user-provided filters if any
	if filters:
		if isinstance(filters, str):
			filters = frappe.parse_json(filters)
		filter_dict.update(filters)
	
	# Fetch orders
	orders = frappe.get_all(
		"Order",
		filters=filter_dict,
		fields=["name", "customer", "order_date", "grand_total", "status"],
		order_by="creation desc",
		start=start,
		page_length=page_length
	)
	
	return orders

# Test with: curl "http://localhost:8000/api/method/myapp.api.order_api.get_my_orders"
```

```python
# File: apps/myapp/hooks.py
# Register in hooks to whitelist
whitelisted_methods = {
	"myapp.api.order_api.get_my_orders": "read"
}
```

**Key Decisions**:
- Use `@frappe.whitelist()` for all public methods
- Validate and sanitize pagination parameters
- Default to authenticated user (`frappe.session.user`)
- Return limited fields (not `*`)
- Use `order_by` and pagination for performance
- Document with docstring including API path

---

### Pattern 2: POST API with Input Validation & Error Handling

**Scenario**: Create an API to create a new order with validation and error handling.

```python
@frappe.whitelist(methods=["POST"])
def create_order(customer, items, notes=None):
	"""
	POST /api/method/myapp.api.order_api.create_order
	
	Create a new order
	
	Args:
		customer (str): Customer ID
		items (str/list): JSON string or list of items [{item_code, qty, rate}]
		notes (str): Optional order notes
	
	Returns:
		dict: Created order details
	
	Raises:
		frappe.ValidationError: Invalid input
	"""
	try:
		# Validate inputs
		if not customer:
			frappe.throw(frappe._("Customer is required"))
		
		if not frappe.db.exists("Customer", customer):
			frappe.throw(frappe._("Customer does not exist"))
		
		# Parse items if string
		if isinstance(items, str):
			items = frappe.parse_json(items)
		
		if not items or not isinstance(items, list):
			frappe.throw(frappe._("Items must be a non-empty list"))
		
		# Validate each item
		for i, item in enumerate(items):
			if not item.get("item_code"):
				frappe.throw(frappe._("Row {0}: Item code required").format(i + 1))
			
			if not frappe.db.exists("Item", item["item_code"]):
				frappe.throw(frappe._("Row {0}: Item does not exist").format(i + 1))
			
			if not item.get("qty") or item["qty"] <= 0:
				frappe.throw(frappe._("Row {0}: Qty must be positive").format(i + 1))
		
		# Create order document
		order = frappe.get_doc({
			"doctype": "Order",
			"customer": customer,
			"order_date": frappe.utils.today(),
			"notes": notes
		})
		
		# Add items
		for item in items:
			order.append("items", {
				"item_code": item["item_code"],
				"qty": item["qty"],
				"rate": item.get("rate", 0)
			})
		
		# Insert and return
		order.insert()
		frappe.db.commit()
		
		return {
			"status": "success",
			"message": frappe._("Order created successfully"),
			"order_id": order.name,
			"order": order.as_dict()
		}
	
	except frappe.ValidationError as e:
		frappe.db.rollback()
		return {
			"status": "error",
			"type": "validation",
			"message": str(e),
			"code": 400
		}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Order creation failed: {str(e)}")
		return {
			"status": "error",
			"type": "internal",
			"message": frappe._("An error occurred while creating the order"),
			"code": 500
		}
```

**Key Decisions**:
- Restrict to POST method with `methods=["POST"]`
- Parse JSON strings to dict/list
- Validate all inputs before processing
- Use transactions with try/except/rollback
- Return standardized error response
- Log unexpected errors
- Return success with full document details

---

### Pattern 3: API with Permission Checks

**Scenario**: Create an API to update an order, with permission validation.

```python
@frappe.whitelist(methods=["PUT"])
def update_order(order_id, status=None, notes=None):
	"""
	PUT /api/method/myapp.api.order_api.update_order
	
	Update order status or notes
	
	Args:
		order_id (str): Order ID
		status (str): New status (Draft, Submitted, Cancelled)
		notes (str): Updated notes
	
	Returns:
		dict: Updated order
	"""
	# Check if order exists
	if not frappe.db.exists("Order", order_id):
		frappe.throw(frappe._("Order not found"), frappe.DoesNotExistError)
	
	# Check permission - user must be owner or admin
	order = frappe.get_doc("Order", order_id)
	
	if order.owner != frappe.session.user and "Administrator" not in frappe.get_roles():
		frappe.throw(frappe._("You do not have permission to modify this order"))
	
	# Verify order state
	if order.docstatus == 2:
		frappe.throw(frappe._("Cannot modify cancelled orders"))
	
	# Update fields
	if notes is not None:
		order.notes = notes
	
	# Handle status change
	if status and status != order.status:
		# Only allow specific transitions
		valid_transitions = {
			"Draft": ["Submitted"],
			"Submitted": ["Cancelled"],
			"Cancelled": []
		}
		
		current_status = order.status or "Draft"
		if status not in valid_transitions.get(current_status, []):
			frappe.throw(frappe._("Invalid status transition from {0} to {1}").format(
				current_status, status
			))
		
		# Perform state change
		if status == "Submitted":
			order.submit()
		elif status == "Cancelled":
			order.cancel()
	
	order.save()
	frappe.db.commit()
	
	return {
		"status": "success",
		"message": frappe._("Order updated"),
		"order": order.as_dict()
	}
```

**Key Decisions**:
- Check document existence first
- Verify user permission (owner, admin, or role-based)
- Validate state transitions
- Use document methods (submit(), cancel()) for state changes
- Return updated document
- Wrap in try/except at top level

---

### Pattern 4: API with Rate Limiting & Authentication

**Scenario**: Create a payment API with rate limiting and authentication.

```python
@frappe.whitelist()
def process_payment(order_id, amount, payment_method):
	"""
	POST /api/method/myapp.api.payment_api.process_payment
	
	Process payment for an order
	
	Requires: API token in Authorization header
	Rate limit: 10 calls per hour
	"""
	# Rate limiting
	user = frappe.session.user
	rate_limit_key = f"payment_api_{user}"
	call_count = frappe.cache.get_value(rate_limit_key) or 0
	
	if call_count >= 10:
		frappe.throw(frappe._("Rate limit exceeded. Max 10 calls/hour"))
	
	# Check API access
	if not frappe.db.get_value("User", user, "enabled"):
		frappe.throw(frappe._("User account disabled"))
	
	# Get order and validate
	if not frappe.db.exists("Order", order_id):
		frappe.throw(frappe._("Order not found"))
	
	order = frappe.get_doc("Order", order_id)
	
	# Verify payment amount
	if abs(float(amount) - float(order.grand_total)) > 0.01:
		frappe.throw(frappe._("Payment amount does not match order total"))
	
	# Process payment with external gateway
	try:
		result = call_payment_gateway(
			order_id=order_id,
			amount=amount,
			method=payment_method
		)
		
		if not result.get("success"):
			frappe.log_error(f"Payment failed: {result.get('error')}")
			frappe.throw(frappe._("Payment processing failed"))
		
		# Create payment record
		payment = frappe.get_doc({
			"doctype": "Payment",
			"order_id": order_id,
			"amount": amount,
			"method": payment_method,
			"status": "Completed",
			"reference": result.get("transaction_id")
		})
		payment.insert()
		
		# Update order status
		order.payment_status = "Paid"
		order.save()
		
		frappe.db.commit()
		
		# Increment rate limiter
		frappe.cache.set_value(rate_limit_key, call_count + 1, expires_in_sec=3600)
		
		return {
			"status": "success",
			"payment_id": payment.name,
			"transaction_id": result.get("transaction_id")
		}
	
	except Exception as e:
		frappe.log_error(f"Payment error: {str(e)}")
		frappe.throw(frappe._("Payment processing error"))
```

**Key Decisions**:
- Implement rate limiting with cache
- Check user account status
- Validate amounts and data
- Call external payment gateway safely
- Create audit trail (Payment record)
- Log all errors for debugging
- Increment counter after success

---

## Advanced Patterns (20% of work)

### Pattern 5: API with File Upload

```python
@frappe.whitelist()
def upload_invoice_document(order_id):
	"""
	POST /api/method/myapp.api.order_api.upload_invoice_document
	
	Upload invoice PDF for an order
	"""
	from frappe.utils.file_manager import upload_file
	
	file = frappe.request.files.get('file')
	if not file:
		frappe.throw(frappe._("No file provided"))
	
	order = frappe.get_doc("Order", order_id)
	
	try:
		file_doc = upload_file(
			fname=file.filename,
			content=file.read(),
			doctype="Order",
			docname=order_id
		)
		
		return {
			"status": "success",
			"file_url": file_doc.file_url,
			"file_name": file_doc.file_name
		}
	except Exception as e:
		frappe.log_error(f"File upload failed: {str(e)}")
		frappe.throw(frappe._("File upload failed"))
```

### Pattern 6: Async API with Job Queue

```python
@frappe.whitelist()
def bulk_create_orders(csv_file_url):
	"""
	Enqueue long-running bulk order creation as background job
	"""
	job = frappe.enqueue(
		"myapp.api.order_api.bulk_create_orders_job",
		queue="long",
		timeout=1800,
		csv_file_url=csv_file_url,
		job_id=f"bulk_orders_{frappe.utils.now_timestamp()}"
	)
	
	return {
		"status": "queued",
		"job_id": job.id
	}

def bulk_create_orders_job(csv_file_url):
	"""Background job - create orders from CSV"""
	import csv
	
	# Download and parse CSV
	# Create orders in loop with error handling
	# Update job progress
	pass
```

---

## Common Mistakes & Solutions

### Mistake 1: Not Validating Input Types
```python
# WRONG - assumes string is dict
def create_order(items):
	for item in items:  # Crash if items is string!
		process(item)

# CORRECT - parse and validate
def create_order(items):
	if isinstance(items, str):
		items = frappe.parse_json(items)
	if not isinstance(items, list):
		frappe.throw("Items must be list")
```

### Mistake 2: Missing Error Handling
```python
# WRONG - unhandled exceptions
def create_order(order_data):
	order = frappe.get_doc(order_data)
	order.insert()  # What if validation fails?
	return order

# CORRECT - handle errors
def create_order(order_data):
	try:
		order = frappe.get_doc(order_data)
		order.insert()
		frappe.db.commit()
		return {"status": "success", "order": order.as_dict()}
	except frappe.ValidationError as e:
		frappe.db.rollback()
		return {"status": "error", "message": str(e)}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(str(e))
		return {"status": "error", "message": "Internal error"}
```

### Mistake 3: Not Checking Permissions
```python
# WRONG - any user can update any order
def update_order(order_id, status):
	order = frappe.get_doc("Order", order_id)
	order.status = status
	order.save()

# CORRECT - verify permission
def update_order(order_id, status):
	if not frappe.has_permission("Order", "write", doc=order_id):
		frappe.throw("No permission")
	order = frappe.get_doc("Order", order_id)
	order.status = status
	order.save()
```

### Mistake 4: Exposing Sensitive Data
```python
# WRONG - returns internal fields
def get_orders():
	return frappe.get_all("Order", fields=["*"])

# CORRECT - return only needed fields
def get_orders():
	return frappe.get_all("Order", 
		fields=["name", "customer", "order_date", "grand_total"]
	)
```

### Mistake 5: Missing Database Commits
```python
# WRONG - changes not saved
def create_order(order_data):
	order = frappe.get_doc(order_data)
	order.insert()  # Inserted but might not commit
	return order

# CORRECT - explicit commit
def create_order(order_data):
	order = frappe.get_doc(order_data)
	order.insert()
	frappe.db.commit()
	return order
```

---

## Testing This Work

```python
# File: apps/myapp/myapp/api/test_order_api.py
import frappe
from frappe.tests import IntegrationTestCase

class TestOrderAPI(IntegrationTestCase):
	def test_get_orders(self):
		"""Test fetching orders"""
		result = frappe.call("myapp.api.order_api.get_my_orders")
		self.assertIsInstance(result.message, list)
	
	def test_create_order_validation(self):
		"""Test input validation"""
		with self.assertRaises(frappe.ValidationError):
			frappe.call("myapp.api.order_api.create_order",
				kwargs={"customer": "NONEXISTENT", "items": []}
			)
	
	def test_create_order_success(self):
		"""Test successful order creation"""
		result = frappe.call("myapp.api.order_api.create_order",
			kwargs={
				"customer": "CUST-001",
				"items": [{"item_code": "ITEM-001", "qty": 5, "rate": 100}]
			}
		)
		self.assertEqual(result.message["status"], "success")
		self.assertIn("order_id", result.message)
```

---

## Performance Considerations

- Limit returned fields (not `*`)
- Use pagination for large result sets
- Add indexes to frequently filtered columns
- Cache read-heavy APIs
- Use `get_safe_limit()` for pagination
- Batch operations for bulk APIs

---

## Integration with Other Subagents

- **Works with**: Permission-Guardian (auth), Database-Navigator (queries)
- **Hands off to**: Permission-Guardian for complex permission logic
- **Context to pass**: Required fields, expected response format, authentication type

---

## API Checklist

- [ ] Uses @frappe.whitelist() decorator
- [ ] Validates all input parameters
- [ ] Checks user permissions
- [ ] Handles errors with try/except
- [ ] Commits database changes
- [ ] Returns standardized response format
- [ ] Logs errors for debugging
- [ ] Documented with docstring + API path
- [ ] Tested with unit tests
- [ ] Returns only necessary fields
