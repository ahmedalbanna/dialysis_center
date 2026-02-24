# Test Engineer Memory File

## Quick Facts
- **Specialty**: Unit tests, integration tests, test fixtures, mocking frameworks, test data management, UI testing with Cypress
- **Primary Tools**: File creation/editing, bash for running tests
- **Common Tasks**: Write unit/integration tests, create test fixtures, mock external services, test DocTypes and APIs
- **Estimated Task Time**: 30-45 minutes per test suite

---

## Most Common Patterns (80% of work)

### Pattern 1: Complete Unit Test Suite for DocType

**Scenario**: Create comprehensive tests for Order DocType with fixtures, child tables, and validations.

```python
# File: apps/myapp/myapp/doctype/order/test_order.py
import frappe
from frappe.tests import IntegrationTestCase

class TestOrder(IntegrationTestCase):
	"""Complete test suite for Order DocType"""
	
	@classmethod
	def setUpClass(cls):
		"""Called once before all tests - create test data"""
		# Create test customer
		if not frappe.db.exists("Customer", "TEST-CUST-001"):
			frappe.get_doc({
				"doctype": "Customer",
				"name": "TEST-CUST-001",
				"customer_name": "Test Customer",
				"customer_type": "Individual"
			}).insert()
		
		# Create test items
		for i in range(1, 4):
			if not frappe.db.exists("Item", f"TEST-ITEM-{i}"):
				frappe.get_doc({
					"doctype": "Item",
					"name": f"TEST-ITEM-{i}",
					"item_name": f"Test Item {i}",
					"item_group": "All Item Groups",
					"stock_uom": "Nos"
				}).insert()
	
	def setUp(self):
		"""Called before each test - create fresh order"""
		self.order = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUST-001",
			"order_date": frappe.utils.today()
		})
		
		# Add items
		for i in range(1, 3):
			self.order.append("items", {
				"item_code": f"TEST-ITEM-{i}",
				"qty": 5,
				"rate": 100
			})
	
	def test_order_creation(self):
		"""Test basic order creation"""
		self.order.insert()
		self.assertTrue(frappe.db.exists("Order", self.order.name))
		self.assertEqual(self.order.docstatus, 0)
	
	def test_mandatory_fields(self):
		"""Test mandatory field validation"""
		order = frappe.get_doc({
			"doctype": "Order",
			"order_date": frappe.utils.today()
			# Missing customer
		})
		
		with self.assertRaises(frappe.ValidationError):
			order.insert()
	
	def test_empty_items_validation(self):
		"""Test that order must have items"""
		order = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUST-001",
			"order_date": frappe.utils.today()
			# No items
		})
		
		with self.assertRaises(frappe.ValidationError):
			order.insert()
	
	def test_total_calculation(self):
		"""Test order total is calculated correctly"""
		self.order.insert()
		
		expected_total = sum(item.qty * item.rate for item in self.order.items)
		self.assertEqual(self.order.grand_total, expected_total)
	
	def test_invalid_item(self):
		"""Test validation with non-existent item"""
		self.order.items = []
		self.order.append("items", {
			"item_code": "NONEXISTENT",
			"qty": 1,
			"rate": 100
		})
		
		with self.assertRaises(frappe.ValidationError):
			self.order.insert()
	
	def test_negative_quantity(self):
		"""Test that negative quantities are rejected"""
		self.order.items[0].qty = -5
		
		with self.assertRaises(frappe.ValidationError):
			self.order.insert()
	
	def test_order_submission(self):
		"""Test order submission workflow"""
		self.order.insert()
		self.order.submit()
		
		self.assertEqual(self.order.docstatus, 1)
		self.assertTrue(frappe.db.exists("Order", self.order.name))
	
	def test_cannot_modify_submitted_order(self):
		"""Test submitted orders cannot be modified"""
		self.order.insert()
		self.order.submit()
		
		# Try to modify submitted order
		self.order.notes = "Modified"
		with self.assertRaises(frappe.ValidationError):
			self.order.save()
	
	def test_order_cancellation(self):
		"""Test order cancellation"""
		self.order.insert()
		self.order.submit()
		self.order.cancel()
		
		self.assertEqual(self.order.docstatus, 2)
	
	def test_child_table_operations(self):
		"""Test adding/removing items"""
		self.order.insert()
		initial_count = len(self.order.items)
		
		# Add item
		self.order.append("items", {
			"item_code": "TEST-ITEM-3",
			"qty": 10,
			"rate": 200
		})
		self.order.save()
		self.assertEqual(len(self.order.items), initial_count + 1)
		
		# Remove item
		self.order.items.pop()
		self.order.save()
		self.assertEqual(len(self.order.items), initial_count)
	
	def test_permissions(self):
		"""Test document-level permissions"""
		self.order.insert()
		
		# Check if current user has permission
		has_access = frappe.has_permission("Order", "write", doc=self.order.name)
		self.assertTrue(has_access)
	
	def tearDown(self):
		"""Called after each test - cleanup"""
		if self.order.name and frappe.db.exists("Order", self.order.name):
			frappe.delete_doc("Order", self.order.name, force=True)
```

**Key Patterns**:
- ✅ Use `setUpClass` for one-time data creation
- ✅ Use `setUp` for fresh data for each test
- ✅ Use `tearDown` for cleanup
- ✅ Test both success and failure cases
- ✅ Use `assertRaises` for exception testing
- ✅ Name tests clearly with `test_` prefix

---

### Pattern 2: Mock External API Calls

**Scenario**: Test API that calls external payment gateway.

```python
from unittest.mock import patch, MagicMock

class TestOrderPaymentAPI(IntegrationTestCase):
	"""Test API with mocked external calls"""
	
	def test_payment_with_mocked_gateway(self):
		"""Test payment API with mocked external service"""
		
		# Create order first
		order = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUST-001",
			"order_date": frappe.utils.today(),
			"grand_total": 1000
		})
		order.insert()
		
		# Mock the payment gateway
		with patch("myapp.api.payment_api.call_payment_gateway") as mock_gateway:
			# Set up mock to return success
			mock_gateway.return_value = {
				"success": True,
				"transaction_id": "TXN-12345"
			}
			
			# Call payment API
			result = frappe.call(
				"myapp.api.payment_api.process_payment",
				kwargs={
					"order_id": order.name,
					"amount": 1000,
					"payment_method": "Credit Card"
				}
			)
			
			# Verify result
			self.assertEqual(result.message["status"], "success")
			
			# Verify mock was called with correct args
			mock_gateway.assert_called_once()
			call_args = mock_gateway.call_args
			self.assertEqual(call_args.kwargs["order_id"], order.name)
	
	def test_payment_gateway_failure(self):
		"""Test API handles gateway failure"""
		
		order = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUST-001"
		})
		order.insert()
		
		# Mock gateway to fail
		with patch("myapp.api.payment_api.call_payment_gateway") as mock_gateway:
			mock_gateway.return_value = {
				"success": False,
				"error": "Insufficient funds"
			}
			
			# Payment should fail gracefully
			with self.assertRaises(frappe.ValidationError):
				frappe.call(
					"myapp.api.payment_api.process_payment",
					kwargs={"order_id": order.name, "amount": 1000}
				)
```

**Key Patterns**:
- ✅ Use `@patch` decorator or context manager
- ✅ Mock return values to test different scenarios
- ✅ Assert mock was called with correct arguments
- ✅ Test success and failure paths

---

### Pattern 3: Test Fixtures for Reusable Test Data

**Scenario**: Create factory pattern for test data.

```python
class TestDataFactory:
	"""Factory for creating test documents"""
	
	@staticmethod
	def create_customer(name=None, **kwargs):
		"""Create test customer with defaults"""
		doc = frappe.get_doc({
			"doctype": "Customer",
			"name": name or frappe.utils.generate_hash(),
			"customer_name": kwargs.get("customer_name", "Test Customer"),
			"customer_type": kwargs.get("customer_type", "Individual"),
			**{k: v for k, v in kwargs.items() if k not in ["customer_name", "customer_type"]}
		})
		doc.insert()
		return doc
	
	@staticmethod
	def create_order(customer=None, items=None, **kwargs):
		"""Create test order with items"""
		doc = frappe.get_doc({
			"doctype": "Order",
			"customer": customer or "TEST-CUST",
			"order_date": frappe.utils.today(),
			**kwargs
		})
		
		for item_data in items or []:
			doc.append("items", item_data)
		
		doc.insert()
		return doc

class TestWithFactory(IntegrationTestCase):
	"""Use factory for cleaner tests"""
	
	def setUp(self):
		self.customer = TestDataFactory.create_customer(
			customer_name="Factory Customer"
		)
		self.order = TestDataFactory.create_order(
			customer=self.customer.name,
			items=[
				{"item_code": "ITEM-1", "qty": 5, "rate": 100},
				{"item_code": "ITEM-2", "qty": 3, "rate": 150}
			]
		)
	
	def test_with_factory_data(self):
		"""Test using factory-created data"""
		self.assertEqual(self.order.customer, self.customer.name)
		self.assertEqual(len(self.order.items), 2)
```

**Key Patterns**:
- ✅ Create factory methods for common test documents
- ✅ Use **kwargs for flexible parameters
- ✅ Set sensible defaults
- ✅ Reuse across multiple tests

---

## Advanced Patterns (20% of work)

### Pattern 4: Test with Transactions & Rollback

```python
def test_atomic_operations(self):
	"""Test multiple operations with rollback"""
	try:
		with frappe.db.transaction():
			order = frappe.get_doc({
				"doctype": "Order",
				"customer": "TEST-CUST"
			})
			order.insert()
			
			# This will cause rollback
			raise Exception("Test error")
	except:
		pass
	
	# Order should not exist (rolled back)
	self.assertFalse(frappe.db.exists("Order", order.name))
```

### Pattern 5: Permission Testing

```python
def test_user_permissions(self):
	"""Test document permissions"""
	# Create order
	order = frappe.get_doc({
		"doctype": "Order",
		"customer": "TEST-CUST"
	})
	order.insert()
	
	# Test permission with different users
	admin_perm = frappe.has_permission("Order", "write", user="Administrator", doc=order.name)
	self.assertTrue(admin_perm)
	
	# Test guest cannot access
	guest_perm = frappe.has_permission("Order", "read", user="Guest", doc=order.name)
	self.assertFalse(guest_perm)
```

---

## Common Mistakes & Solutions

### Mistake 1: Not Cleaning Up Test Data
```python
# WRONG - leaves test data in database
def test_something(self):
	order = frappe.get_doc({"doctype": "Order", ...}).insert()
	# Test never deletes order

# CORRECT - cleanup in tearDown
def tearDown(self):
	if self.order.name:
		frappe.delete_doc("Order", self.order.name, force=True)
```

### Mistake 2: Flaky Tests with Timing Issues
```python
# WRONG - assumes async operation completes
frappe.enqueue(process_order, order_id="ORD-1")
time.sleep(0.1)  # Might not be enough
verify_order_processed()

# CORRECT - use polling or callback
for i in range(30):  # Wait max 3 seconds
	if frappe.db.exists("ProcessedOrder", "ORD-1"):
		break
	time.sleep(0.1)
```

### Mistake 3: Not Mocking External Dependencies
```python
# WRONG - test fails if API is down
def test_order(self):
	frappe.call("myapp.api.fetch_shipping_cost", ...)

# CORRECT - mock external calls
@patch("myapp.api.fetch_shipping_cost")
def test_order(self, mock_shipping):
	mock_shipping.return_value = 50.0
```

### Mistake 4: Importing Wrong Test Class
```python
# WRONG - missing frappe context
from unittest import TestCase

# CORRECT - use frappe's test class
from frappe.tests import IntegrationTestCase
```

### Mistake 5: Hard-coded Test Data Names
```python
# WRONG - conflicts with other tests
order = frappe.get_doc({
	"doctype": "Order",
	"name": "TEST-ORDER-1"  # Fixed name
})

# CORRECT - generate unique names
order = frappe.get_doc({
	"doctype": "Order",
	"name": f"TEST-ORDER-{frappe.utils.generate_hash()}"
})
```

---

## Running Tests

```bash
# Run all tests for a DocType
bench --site frappe.local run-tests --doctype Order

# Run specific test class
bench --site frappe.local run-tests --module myapp.doctype.order.test_order.TestOrder

# Run with verbose output
bench --site frappe.local run-tests --doctype Order -v

# Run with coverage
bench --site frappe.local run-tests --doctype Order --coverage
```

---

## Performance Checklist

- [ ] setUpClass for expensive one-time setup
- [ ] setUp for data per test
- [ ] tearDown for proper cleanup
- [ ] Mock external API calls
- [ ] Use factories for complex test data
- [ ] Test success and failure cases
- [ ] Test permissions and validation
- [ ] Test child table operations
- [ ] Use assertions correctly
- [ ] Isolate tests (no dependencies between tests)

---

## Integration with Other Subagents

- **Works with**: DocType-Architect (testing DocTypes), API-Whitelister (testing APIs)
- **Hands off to**: Debug-Detective if tests fail
- **Context to pass**: Test data structure, edge cases to test

---

## Quick Testing Checklist

- [ ] Unit tests for validate()
- [ ] Tests for before_save() and on_update()
- [ ] Child table add/remove tests
- [ ] Permission tests
- [ ] Negative case tests (invalid inputs)
- [ ] Boundary condition tests
- [ ] Integration tests for multiple DocTypes
- [ ] API endpoint tests with mocks
- [ ] Test cleanup in tearDown()
- [ ] Descriptive test names
