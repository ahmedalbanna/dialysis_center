# DocType Architect Memory File

## Quick Facts
- **Specialty**: Designing and implementing Frappe DocTypes with fields, validations, relationships, and migrations
- **Primary Tools**: File creation/editing, bash for testing
- **Common Tasks**: New DocType design, field definitions, validation logic, permission setup, migration patterns
- **Estimated Task Time**: 25-40 minutes per DocType

---

## Most Common Patterns (80% of work)

### Pattern 1: Complete DocType Creation (Master Data)

**Scenario**: Create a Customer DocType with name, email, phone, and address fields.

```python
# File: apps/myapp/myapp/doctype/customer/customer.json
{
	"doctype": "Customer",
	"name": "Customer",
	"label": "Customer",
	"document_type": "Master",
	"autoname": "field:customer_name",
	"title_field": "customer_name",
	"fields": [
		{
			"fieldname": "customer_name",
			"label": "Customer Name",
			"fieldtype": "Data",
			"reqd": 1,
			"unique": 1
		},
		{
			"fieldname": "email",
			"label": "Email",
			"fieldtype": "Data",
			"options": "Email"
		},
		{
			"fieldname": "phone",
			"label": "Phone",
			"fieldtype": "Data"
		},
		{
			"fieldname": "address",
			"label": "Address",
			"fieldtype": "Text"
		},
		{
			"fieldname": "customer_type",
			"label": "Customer Type",
			"fieldtype": "Select",
			"options": "\nIndividual\nBusiness"
		},
		{
			"fieldname": "credit_limit",
			"label": "Credit Limit",
			"fieldtype": "Currency",
			"default": 0
		}
	],
	"permissions": [
		{
			"role": "Administrator",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1
		},
		{
			"role": "Sales User",
			"read": 1,
			"write": 1,
			"create": 1
		}
	]
}
```

```python
# File: apps/myapp/myapp/doctype/customer/customer.py
import frappe
from frappe.model.document import Document

class Customer(Document):
	def validate(self):
		"""Validate customer data"""
		# Email format validation
		if self.email and "@" not in self.email:
			frappe.throw(frappe._("Invalid email format"))
		
		# Check for duplicates
		duplicate = frappe.db.exists("Customer", {
			"customer_name": self.customer_name,
			"name": ["!=", self.name]
		})
		if duplicate:
			frappe.throw(frappe._("Customer with this name already exists"))
	
	def before_save(self):
		"""Normalize data before saving"""
		self.customer_name = self.customer_name.strip().title() if self.customer_name else ""
		self.email = self.email.lower() if self.email else ""
	
	def on_update(self):
		"""Update related documents"""
		# Clear cache for customer orders
		frappe.cache.delete_value(f"customer_{self.name}_orders")
```

**Key Decisions**:
- Use `autoname` for auto-generated names (not UUID)
- Add `title_field` for better UI display
- Set `reqd: 1` for mandatory fields
- Use `unique: 1` for email/phone if needed
- Validate in both JSON (frontend) and Python (backend)
- Clear caches on update

---

### Pattern 2: Transaction DocType with Child Table (Order + Items)

**Scenario**: Create an Order DocType with items table, amounts, and submission workflow.

```python
# File: apps/myapp/myapp/doctype/order/order.json
{
	"doctype": "Order",
	"name": "Order",
	"label": "Order",
	"document_type": "Document",
	"is_submittable": 1,
	"autoname": "naming_series:",
	"naming_series": "ORD-YYYY-MM-",
	"title_field": "customer_name",
	"fields": [
		{
			"fieldname": "customer",
			"label": "Customer",
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1
		},
		{
			"fieldname": "customer_name",
			"label": "Customer Name",
			"fieldtype": "Data",
			"read_only": 1
		},
		{
			"fieldname": "order_date",
			"label": "Order Date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": "today"
		},
		{
			"fieldname": "items_section",
			"label": "Items",
			"fieldtype": "Section Break"
		},
		{
			"fieldname": "items",
			"label": "Items",
			"fieldtype": "Table",
			"options": "Order Item"
		},
		{
			"fieldname": "totals_section",
			"label": "Totals",
			"fieldtype": "Section Break"
		},
		{
			"fieldname": "total_quantity",
			"label": "Total Quantity",
			"fieldtype": "Int",
			"read_only": 1
		},
		{
			"fieldname": "total_amount",
			"label": "Total Amount",
			"fieldtype": "Currency",
			"read_only": 1
		},
		{
			"fieldname": "tax_rate",
			"label": "Tax Rate %",
			"fieldtype": "Percent",
			"default": 0
		},
		{
			"fieldname": "tax_amount",
			"label": "Tax Amount",
			"fieldtype": "Currency",
			"read_only": 1
		},
		{
			"fieldname": "grand_total",
			"label": "Grand Total",
			"fieldtype": "Currency",
			"read_only": 1
		}
	],
	"permissions": [
		{
			"role": "Administrator",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1
		}
	]
}

# Child DocType: Order Item
{
	"doctype": "Order Item",
	"name": "Order Item",
	"document_type": "Child",
	"fields": [
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item",
			"reqd": 1
		},
		{
			"fieldname": "item_name",
			"label": "Item Name",
			"fieldtype": "Data",
			"read_only": 1
		},
		{
			"fieldname": "qty",
			"label": "Quantity",
			"fieldtype": "Int",
			"reqd": 1,
			"default": 1
		},
		{
			"fieldname": "rate",
			"label": "Rate",
			"fieldtype": "Currency",
			"reqd": 1
		},
		{
			"fieldname": "line_total",
			"label": "Line Total",
			"fieldtype": "Currency",
			"read_only": 1
		}
	]
}
```

```python
# File: apps/myapp/myapp/doctype/order/order.py
class Order(Document):
	def validate(self):
		"""Validate order"""
		# Check customer exists
		if not frappe.db.exists("Customer", self.customer):
			frappe.throw(frappe._("Customer does not exist"))
		
		# Check items not empty
		if not self.items:
			frappe.throw(frappe._("Order must have at least one item"))
		
		# Validate each item
		for i, item in enumerate(self.items, 1):
			if item.qty <= 0:
				frappe.throw(frappe._("Row {0}: Quantity must be positive").format(i))
			
			if not frappe.db.exists("Item", item.item_code):
				frappe.throw(frappe._("Row {0}: Item does not exist").format(i))
			
			# Calculate line total
			item.line_total = item.qty * item.rate
		
		# Calculate totals
		self.calculate_totals()
	
	def before_save(self):
		"""Calculate and set customer name"""
		self.customer_name = frappe.db.get_value("Customer", self.customer, "customer_name")
	
	def calculate_totals(self):
		"""Calculate order totals"""
		self.total_quantity = sum(item.qty for item in self.items)
		self.total_amount = sum(item.line_total for item in self.items)
		self.tax_amount = self.total_amount * (self.tax_rate / 100) if self.tax_rate else 0
		self.grand_total = self.total_amount + self.tax_amount
	
	def on_submit(self):
		"""Actions when order is submitted"""
		# Update customer's last order
		frappe.db.set_value("Customer", self.customer, "last_order_id", self.name)
		
		# Create invoice if auto-create enabled
		if frappe.db.get_single_value("Settings", "auto_create_invoice"):
			self.create_invoice()
	
	def on_cancel(self):
		"""Reverse actions on cancellation"""
		# Clear customer's last order if this was it
		if frappe.db.get_value("Customer", self.customer, "last_order_id") == self.name:
			frappe.db.set_value("Customer", self.customer, "last_order_id", None)
	
	def create_invoice(self):
		"""Create invoice from this order"""
		invoice = frappe.get_doc({
			"doctype": "Invoice",
			"order_id": self.name,
			"customer": self.customer,
			"amount": self.grand_total
		})
		invoice.insert()
```

**Key Decisions**:
- Use `is_submittable: 1` for documents with workflow
- Use `naming_series` for formatted names (ORD-YYYY-MM-)
- Separate child table (`Order Item`) for line items
- Read-only fields for calculations (qty, rate → line_total)
- Validate child table rows in parent's validate()
- Calculate totals in before_save()
- Handle state changes in on_submit() and on_cancel()

---

### Pattern 3: Advanced Field Validation with Conditions

**Scenario**: Create a Invoice DocType with conditional validation based on invoice type.

```python
class Invoice(Document):
	def validate(self):
		"""Comprehensive validation"""
		# Mandatory field validation
		if not self.customer:
			frappe.throw(frappe._("Customer is required"))
		
		# Type-based validation
		if self.invoice_type == "Sales":
			self.validate_sales_invoice()
		elif self.invoice_type == "Purchase":
			self.validate_purchase_invoice()
		
		# Check date ranges
		if self.due_date and self.invoice_date:
			if self.due_date < self.invoice_date:
				frappe.throw(frappe._("Due date must be after invoice date"))
		
		# Validate amounts
		if self.grand_total < 0:
			frappe.throw(frappe._("Grand total cannot be negative"))
		
		# Business rules
		if self.grand_total > 100000 and not self.approval_required:
			frappe.throw(frappe._("High-value invoices require approval"))
	
	def validate_sales_invoice(self):
		"""Sales-specific validation"""
		if not self.terms:
			frappe.throw(frappe._("Sales invoices require payment terms"))
		
		# Check customer credit
		customer = frappe.get_doc("Customer", self.customer)
		if customer.credit_limit and self.grand_total > customer.credit_limit:
			frappe.throw(frappe._("Invoice exceeds customer credit limit"))
	
	def validate_purchase_invoice(self):
		"""Purchase-specific validation"""
		if not self.supplier:
			frappe.throw(frappe._("Supplier is required for purchase invoices"))
	
	def before_save(self):
		"""Pre-save transformations"""
		# Normalize data
		self.customer_name = self.customer_name.strip().title() if self.customer_name else ""
		
		# Set defaults
		if not self.invoice_date:
			self.invoice_date = frappe.utils.today()
		
		# Calculate based on type
		if self.invoice_type == "Sales":
			self.calculate_sales_tax()
		elif self.invoice_type == "Purchase":
			self.calculate_purchase_tax()
	
	def calculate_sales_tax(self):
		"""Calculate sales tax"""
		tax_rate = frappe.db.get_value("Customer", self.customer, "sales_tax_rate") or 10
		self.tax_amount = self.subtotal * (tax_rate / 100)
		self.grand_total = self.subtotal + self.tax_amount
	
	def calculate_purchase_tax(self):
		"""Calculate purchase tax"""
		self.tax_amount = self.subtotal * 0.05  # Fixed 5% purchase tax
		self.grand_total = self.subtotal + self.tax_amount
	
	def on_update(self):
		"""Update related records"""
		# Update customer balance if sales
		if self.invoice_type == "Sales":
			current_balance = frappe.db.get_value("Customer", self.customer, "outstanding_balance") or 0
			frappe.db.set_value("Customer", self.customer, "outstanding_balance", current_balance + self.grand_total)
		
		# Clear cache
		frappe.cache.delete_value(f"invoice_{self.name}")
```

**Key Decisions**:
- Use method-based validation for complex logic
- Separate validation methods by type
- Fetch related data once and reuse
- Validate interdependent fields together
- Use before_save() for calculations
- Update related docs in on_update()

---

## Advanced Patterns (20% of work)

### Pattern 4: DocType with Dependent Fields

**Scenario**: Show/hide fields based on document type.

```json
{
	"fieldname": "is_company",
	"label": "Is Company?",
	"fieldtype": "Check"
},
{
	"fieldname": "company_name",
	"label": "Company Name",
	"fieldtype": "Data",
	"depends_on": "eval: doc.is_company == 1"
},
{
	"fieldname": "registration_number",
	"label": "Registration Number",
	"fieldtype": "Data",
	"depends_on": "eval: doc.is_company == 1 && doc.country == 'USA'"
}
```

**Use `depends_on`** for conditional field visibility (evaluated on client-side).

### Pattern 5: Link Fields with Filters

```json
{
	"fieldname": "warehouse",
	"label": "Warehouse",
	"fieldtype": "Link",
	"options": "Warehouse",
	"filters": [
		["active", "=", 1],
		["location", "=", "docstatus", 0]
	]
}
```

Filters restrict link field options based on conditions.

---

## Common Mistakes & Solutions

### Mistake 1: Using Field Type for Wrong Data
```python
# WRONG - using Data for amounts
"rate": {"fieldtype": "Data"}

# CORRECT - use Currency or Float
"rate": {"fieldtype": "Currency", "precision": 2}
```

### Mistake 2: Missing Child Table Validation
```python
# WRONG - not validating child rows
def validate(self):
	if not self.items:
		frappe.throw("Items required")

# CORRECT - validate each child row
def validate(self):
	if not self.items:
		frappe.throw("Items required")
	
	for i, item in enumerate(self.items, 1):
		if item.qty <= 0:
			frappe.throw(frappe._("Row {0}: Qty must be > 0").format(i))
```

### Mistake 3: Not Handling Duplicates
```python
# WRONG - creating duplicate records allowed
class Customer(Document):
	pass

# CORRECT - prevent duplicates
class Customer(Document):
	def validate(self):
		duplicate = frappe.db.exists("Customer", {
			"email": self.email,
			"name": ["!=", self.name]
		})
		if duplicate:
			frappe.throw(frappe._("Customer with this email exists"))
```

### Mistake 4: Forgetting to Set Read-Only on Computed Fields
```python
# WRONG - user can edit calculated field
"line_total": {"fieldtype": "Currency"}

# CORRECT - computed field is read-only
"line_total": {
	"fieldtype": "Currency",
	"read_only": 1
}
```

### Mistake 5: Not Clearing Cache on Updates
```python
# WRONG - stale data served from cache
def on_update(self):
	frappe.db.set_value("Customer", self.customer, "balance", self.balance)

# CORRECT - invalidate cache
def on_update(self):
	frappe.db.set_value("Customer", self.customer, "balance", self.balance)
	frappe.cache.delete_value(f"customer_{self.customer}")
```

---

## Testing This Work

### Test DocType Creation
```python
# File: apps/myapp/myapp/doctype/order/test_order.py
import frappe
from frappe.tests import IntegrationTestCase

class TestOrder(IntegrationTestCase):
	def test_order_creation(self):
		"""Test basic order creation"""
		order = frappe.get_doc({
			"doctype": "Order",
			"customer": "CUST-001",
			"order_date": frappe.utils.today()
		})
		order.append("items", {
			"item_code": "ITEM-001",
			"qty": 5,
			"rate": 100
		})
		order.insert()
		
		self.assertEqual(order.total_amount, 500)
		self.assertEqual(order.grand_total, 500)
	
	def test_validation(self):
		"""Test validation rules"""
		with self.assertRaises(frappe.ValidationError):
			order = frappe.get_doc({
				"doctype": "Order",
				"customer": "NONEXISTENT"
			})
			order.insert()
	
	def test_child_validation(self):
		"""Test child table validation"""
		with self.assertRaises(frappe.ValidationError):
			order = frappe.get_doc({
				"doctype": "Order",
				"customer": "CUST-001"
			})
			order.append("items", {
				"item_code": "ITEM-001",
				"qty": -1,  # Invalid
				"rate": 100
			})
			order.insert()
```

Run with: `bench --site frappe.local run-tests --doctype Order`

---

## Performance Considerations

### Indexing Strategy
```json
{
	"fieldname": "customer",
	"fieldtype": "Link",
	"index": 1
},
{
	"fieldname": "order_date",
	"fieldtype": "Date",
	"index": 1
}
```

Add indexes to frequently filtered fields (customer, date, status).

### Avoid N+1 Queries
```python
# WRONG - loads document 100 times
orders = frappe.get_all("Order", fields=["name"])
for order in orders:
	doc = frappe.get_doc("Order", order.name)  # N queries!

# CORRECT - load all at once
orders = frappe.get_all("Order", fields=["*"])
```

### Cache Computed Fields
```python
def get_customer_balance(customer):
	cache_key = f"customer_balance_{customer}"
	balance = frappe.cache.get_value(cache_key)
	if not balance:
		balance = frappe.db.get_value("Customer", customer, "balance")
		frappe.cache.set_value(cache_key, balance, expires_in_sec=3600)
	return balance
```

---

## Integration with Other Subagents

- **Works with**: Database-Navigator (queries), API-Whitelister (CRUD APIs), Permission-Guardian (permissions)
- **Hands off to**: 
  - Database-Navigator when needing query optimization
  - API-Whitelister when building APIs for this DocType
  - Permission-Guardian for access control setup
- **Context to pass**: DocType structure, field definitions, child tables

---

## Quick Checklist for New DocType

- [ ] Name follows convention (PascalCase, singular)
- [ ] All mandatory fields have `reqd: 1`
- [ ] Searchable fields are marked correctly
- [ ] Read-only fields for calculations
- [ ] validate() checks all business rules
- [ ] before_save() normalizes and calculates
- [ ] Permissions configured for roles
- [ ] Child tables validated in parent
- [ ] Caches cleared on updates
- [ ] Tests written and passing
- [ ] Indexes added to frequent filters
