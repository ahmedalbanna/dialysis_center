# Permission Guardian Memory File

## Quick Facts
- **Specialty**: Role-based permissions (RBAC), document-level permissions (DLP), user permission queries, authentication flows, field-level security
- **Primary Tools**: File creation/editing, bash for testing
- **Common Tasks**: Configure DocType permissions, implement permission queries, handle authentication, set field-level security
- **Estimated Task Time**: 20-35 minutes per permission setup

---

## Most Common Patterns (80% of work)

### Pattern 1: Complete DocType Permission Setup

**Scenario**: Configure permissions for Order DocType with different roles.

```json
{
	"doctype": "Order",
	"permissions": [
		{
			"role": "Administrator",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1
		},
		{
			"role": "Sales Manager",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"submit": 1,
			"cancel": 1,
			"amend": 1
		},
		{
			"role": "Sales User",
			"read": 1,
			"write": 1,
			"create": 1,
			"submit": 1,
			"if_owner": 1
		},
		{
			"role": "Accounts User",
			"read": 1,
			"if_owner": 1
		}
	]
}
```

**Key Patterns**:
- ✅ Administrator has full permissions
- ✅ Managers have full create/delete
- ✅ Users have create/submit but limited delete
- ✅ Use `if_owner` to restrict to document creator
- ✅ Different roles for read-only access

---

### Pattern 2: Permission Query Implementation

**Scenario**: Restrict users to see only their own orders.

```python
# File: apps/myapp/myapp/doctype/order/order.py

class Order(Document):
	def get_permission_query_conditions(self, user):
		"""Filter orders visible to user based on role"""
		
		# Administrators see everything
		if "Administrator" in frappe.get_roles(user):
			return ""
		
		# Sales managers see orders from their team
		if "Sales Manager" in frappe.get_roles(user):
			return f"`tabOrder`.`assigned_to` IN (SELECT user FROM `tabUserRole` WHERE role = 'Sales User')"
		
		# Sales users see their own orders
		if "Sales User" in frappe.get_roles(user):
			return f"`tabOrder`.`owner` = '{frappe.db.escape(user)}'"
		
		# Customers see their own orders
		if "Customer" in frappe.get_roles(user):
			return f"`tabOrder`.`customer` = (SELECT name FROM `tabCustomer` WHERE email = '{frappe.db.escape(user)}')"
		
		# No access by default
		return "`tabOrder`.`name` IS NULL"
```

```python
# Module-level hook in hooks.py
permission_query_conditions = {
	"Order": "myapp.doctype.order.order.Order.get_permission_query_conditions"
}
```

**Key Patterns**:
- ✅ Return empty string for full access
- ✅ Return `IS NULL` for no access
- ✅ Use user roles to determine filter
- ✅ Escape user input in SQL
- ✅ Support multiple role hierarchies

---

### Pattern 3: User Permission Implementation

**Scenario**: Restrict Sales User to specific branch.

```python
def setup_user_permissions():
	"""Configure which users can see which branches"""
	
	# Sales user in North branch can only see North branch orders
	frappe.get_doc({
		"doctype": "User Permission",
		"user": "sales.user@example.com",
		"allow": "Branch",
		"for_value": "North Branch",
		"is_default": 1
	}).insert()
	
	# User can have multiple permissions
	frappe.get_doc({
		"doctype": "User Permission",
		"user": "sales.user@example.com",
		"allow": "Customer",
		"for_value": "CUST-001"
	}).insert()
```

```python
# In DocType controller
class Order(Document):
	def get_permission_query_conditions(self, user):
		"""Use User Permission to filter"""
		
		# Get user's allowed branches
		allowed_branches = frappe.db.get_all(
			"User Permission",
			filters={"user": user, "allow": "Branch"},
			pluck="for_value"
		)
		
		if not allowed_branches:
			return "`tabOrder`.`name` IS NULL"
		
		# Generate WHERE clause
		branches_str = ",".join([f"'{b}'" for b in allowed_branches])
		return f"`tabOrder`.`branch` IN ({branches_str})"
```

**Key Patterns**:
- ✅ Create User Permission documents
- ✅ Query User Permission in controller
- ✅ Support multiple permission types
- ✅ Use `is_default` for primary permission
- ✅ Combine multiple permission checks

---

### Pattern 4: Field-Level Security

**Scenario**: Hide salary field from non-HR users.

```python
# In DocType definition
{
	"fieldname": "salary",
	"fieldtype": "Currency",
	"label": "Salary",
	"permlevel": 1,  # Higher permission level = restricted
	"read_only": 1
}

# In permissions
{
	"role": "HR Manager",
	"read": 1,
	"write": 1,
	"permlevel": 1  # Can access permlevel 1 fields
},
{
	"role": "Employee",
	"read": 1,
	"permlevel": 0  # Can only access permlevel 0 fields
}
```

```python
# Programmatic approach
class Employee(Document):
	def get_access_fields(self, user):
		"""Return list of fields accessible to user"""
		
		if "HR Manager" in frappe.get_roles(user):
			# HR managers see all fields
			return None
		
		if "Administrator" in frappe.get_roles(user):
			return None
		
		# Regular employees see only public fields
		return ["name", "employee_name", "designation", "department"]
```

**Key Patterns**:
- ✅ Use `permlevel` for field hierarchy
- ✅ Higher permlevel = more restricted
- ✅ Role permissions must match permlevel
- ✅ Can use `get_access_fields()` for dynamic control
- ✅ `None` return = all fields accessible

---

## Advanced Patterns (20% of work)

### Pattern 5: Document-Level Sharing

```python
def share_order_with_user(order_id, user_email, permission="read"):
	"""Share specific document with user"""
	
	frappe.share.add(
		doctype="Order",
		name=order_id,
		user=user_email,
		perm_type=permission,  # read, write, submit
		notify=True
	)

def revoke_share(order_id, user_email):
	"""Remove document access"""
	
	frappe.share.remove(
		doctype="Order",
		name=order_id,
		user=user_email
	)

def get_shared_documents(user_email):
	"""Get documents shared with user"""
	
	shared = frappe.get_all("Document Share",
		filters={"user": user_email},
		fields=["doc_type", "doc_name", "perm_type"]
	)
	return shared
```

### Pattern 6: Authentication & Login Hooks

```python
def validate_login(self):
	"""Custom login validation"""
	
	# Check if user is in allowed branch
	user = frappe.get_doc("User", self.user)
	allowed_branches = frappe.db.get_all(
		"User Permission",
		filters={"user": self.user, "allow": "Branch"},
		pluck="for_value"
	)
	
	if not allowed_branches:
		frappe.throw(_("No branch assigned to this user"))

# In hooks.py
validate_login = "myapp.auth.validate_login"
```

---

## Common Mistakes & Solutions

### Mistake 1: Exposing Sensitive Fields
```python
# WRONG - sensitive field visible to everyone
{
	"fieldname": "salary",
	"fieldtype": "Currency",
	"hidden": 0
}

# CORRECT - use permlevel + role restrictions
{
	"fieldname": "salary",
	"fieldtype": "Currency",
	"permlevel": 1  # Only HR can see
}
```

### Mistake 2: SQL Injection in Permission Query
```python
# WRONG - vulnerable to injection
return f"`tabOrder`.`owner` = '{user}'"

# CORRECT - use escape function
return f"`tabOrder`.`owner` = '{frappe.db.escape(user)}'"
```

### Mistake 3: Not Checking Permissions Before Save
```python
# WRONG - allows users to modify documents they shouldn't
def on_update(self):
	self.status = "Approved"

# CORRECT - check permissions first
def on_update(self):
	if not frappe.has_permission("Order", "write", doc=self.name):
		frappe.throw(_("No permission to update"))
```

### Mistake 4: Forgetting to Handle if_owner
```python
# WRONG - doesn't work as expected
{
	"role": "User",
	"write": 1,
	"if_owner": 1  # Not checking owner in code
}

# CORRECT - system automatically checks owner if flag is set
# Role can write only if user is document owner
```

### Mistake 5: Over-Permissive Default Role
```python
# WRONG - Everyone can see sensitive data
{
	"role": "User",  # Default role for all users
	"read": 1,
	"write": 1
}

# CORRECT - Use specific roles
{
	"role": "Sales User",
	"read": 1,
	"write": 1
},
{
	"role": "Guest",
	"read": 0
}
```

---

## Testing Permissions

```python
def test_permission_checks(self):
	"""Test permission logic"""
	
	# Create order
	order = frappe.get_doc({
		"doctype": "Order",
		"customer": "CUST-001"
	})
	order.insert()
	
	# Admin can read
	self.assertTrue(frappe.has_permission("Order", "read", user="admin@test.com", doc=order.name))
	
	# Regular user depends on permission query
	has_perm = frappe.has_permission("Order", "read", user="user@test.com", doc=order.name)
	# Result depends on permission_query_conditions
	
	# Test if_owner
	order.owner = "owner@test.com"
	order.save()
	self.assertTrue(frappe.has_permission("Order", "write", user="owner@test.com", doc=order.name))
```

---

## Permission Checklist

- [ ] DocType permissions configured for all roles
- [ ] if_owner conditions set for user-level restrictions
- [ ] Permission query conditions for complex filtering
- [ ] Field-level security with permlevel
- [ ] Document sharing for special cases
- [ ] Login validation if needed
- [ ] Test permissions for all roles
- [ ] No sensitive data in default views
- [ ] SQL injection prevention in queries
- [ ] Audit logging of permission changes

---

## Integration with Other Subagents

- **Works with**: DocType-Architect (DocType setup), API-Whitelister (API permissions)
- **Hands off to**: Debug-Detective for permission issues
- **Context to pass**: User roles, document ownership model, data sensitivity

---

## Quick Permission Setup

1. Configure DocType permissions (read/write/create/delete/submit)
2. Set if_owner for user-specific restrictions
3. Implement permission_query_conditions for complex filtering
4. Use permlevel for field-level security
5. Test with different user roles
6. Log and audit permission changes
