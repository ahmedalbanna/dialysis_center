# Hooks Orchestrator Memory File

## Quick Facts
- **Specialty**: Frappe event-driven hooks system, document lifecycle hooks, scheduled tasks, boot hooks, fixture management, and hook registration
- **Primary Tools**: File creation/editing (hooks.py), bash for testing
- **Common Tasks**: Setting up doc_events, scheduler_events, before_request/after_request hooks, custom fixtures
- **Estimated Task Time**: 20-35 minutes per hook implementation

---

## Core Hooks Overview

### Hook Types in Frappe
1. **Document Lifecycle Hooks** (doc_events) - Triggered on document CRUD operations
2. **Scheduled Tasks** (scheduler_events) - Triggered at specific times/intervals
3. **Request Lifecycle Hooks** (before_request/after_request) - HTTP request handling
4. **Boot Hooks** (boot) - Page load initialization
5. **Page Methods** - Custom methods attached to pages
6. **Website Hooks** - Website rendering customization
7. **Fixture Management** - Pre-defined data loading

---

## Most Common Patterns

### Pattern 1: Document Lifecycle Hooks

**Location**: `apps/myapp/myapp/hooks.py`

```python
doc_events = {
	"Order": {
		"before_insert": "myapp.order.before_order_insert",
		"after_insert": "myapp.order.after_order_insert",
		"validate": "myapp.order.validate_order",
		"before_save": "myapp.order.before_order_save",
		"on_update": "myapp.order.on_order_update",
		"on_submit": "myapp.order.on_order_submit",
		"on_cancel": "myapp.order.on_order_cancel",
		"on_trash": "myapp.order.on_order_trash",
	},
	"*": {
		"after_insert": "myapp.utils.log_document_creation",
		"on_trash": "myapp.utils.log_document_deletion",
	}
}
```

**Implementation**:
```python
# File: apps/myapp/myapp/order.py

def before_order_insert(doc, method):
	"""Called before new Order is inserted"""
	if not doc.order_date:
		doc.order_date = frappe.utils.today()

def on_order_submit(doc, method):
	"""Called when Order is submitted"""
	# Create warehouse entries, send emails, etc.
	create_warehouse_entries(doc)
	send_order_confirmation(doc)
```

### Pattern 2: Scheduled Tasks

**Location**: `apps/myapp/myapp/hooks.py`

```python
scheduler_events = {
	"daily": [
		"myapp.tasks.daily_cleanup",
		"myapp.tasks.send_daily_digest"
	],
	"hourly": [
		"myapp.tasks.sync_external_data"
	],
	"all": [  # Every minute
		"myapp.tasks.check_alerts"
	],
	"cron": {
		"0 0 * * *": ["myapp.tasks.midnight_task"],  # Daily at midnight
		"0 */6 * * *": ["myapp.tasks.six_hourly_task"],  # Every 6 hours
		"0 0 * * 0": ["myapp.tasks.weekly_task"],  # Weekly on Sunday
		"0 0 1 * *": ["myapp.tasks.monthly_task"],  # First of month
	}
}
```

**Implementation**:
```python
# File: apps/myapp/myapp/tasks.py

def daily_cleanup():
	"""Scheduled task - runs daily"""
	# Delete old temporary records
	frappe.db.delete("Temp Data", filters={
		"created": ("<", frappe.utils.add_days(frappe.utils.today(), -30))
	})
	frappe.db.commit()

def send_daily_digest():
	"""Send daily digest to users"""
	users = frappe.get_all("User", filters={"enabled": 1})
	for user in users:
		send_digest_email(user.name)
```

### Pattern 3: Request Lifecycle Hooks

**Location**: `apps/myapp/myapp/hooks.py`

```python
before_request = ["myapp.utils.before_request_handler"]
after_request = ["myapp.utils.after_request_handler"]
```

**Implementation**:
```python
# File: apps/myapp/myapp/utils.py

def before_request_handler():
	"""Called before every request"""
	# Log request
	frappe.logger().info(f"Request: {frappe.request.method} {frappe.request.path}")
	
	# Check custom permissions
	if frappe.request.path.startswith("/custom-api/"):
		check_custom_auth()

def after_request_handler(response):
	"""Called after every request"""
	# Add custom headers
	response.headers["X-Custom-Header"] = "value"
	return response
```

### Pattern 4: Boot Hooks (Page Load)

**Location**: `apps/myapp/myapp/hooks.py`

```python
boot = ["myapp.boot.before_boot"]
```

**Implementation**:
```python
# File: apps/myapp/myapp/boot.py

def before_boot():
	"""Called before page loads"""
	# Customize boot data sent to frontend
	frappe.cache.set_value("app_config", get_app_config())
```

### Pattern 5: Fixtures (Pre-defined Data)

**Location**: `apps/myapp/myapp/hooks.py`

```python
fixtures = [
	{"dt": "Custom Field", "filters": {"module": "My App"}},
	{"dt": "Workspace", "filters": {"module": "My App"}},
	"Role",
	"Print Format",
	{"dt": "DocType", "filters": {"app": "myapp"}}
]
```

---

## Execution Order & Guarantees

### Document Lifecycle Order
```
1. before_insert (new documents only)
2. validate (all saves)
3. before_save (all saves)
4. [Database INSERT/UPDATE]
5. after_insert (new documents only)
6. on_update (updates only)
7. on_submit (submittable, on submit)
8. on_cancel (submitted, on cancel)
9. before_trash (before delete)
10. on_trash / after_delete (after delete)
```

### Key Execution Guarantees
- ✅ `validate` and `before_save` ALWAYS run before database operations
- ✅ `after_insert` and `on_update` ALWAYS run after database operations
- ✅ Child table `validate()` runs BEFORE parent validate
- ✅ Hook order is preserved (top-to-bottom in hooks.py)
- ⚠️ Hooks can run asynchronously (use `frappe.enqueue()` for async operations)

---

## Common Patterns by Scenario

### Scenario 1: Update Related Documents on Submit
```python
def on_order_submit(doc, method):
	"""When Order is submitted, update Customer"""
	frappe.db.set_value("Customer", doc.customer, "last_order_id", doc.name)
	frappe.cache.delete_value(f"customer_{doc.customer}_orders")
```

### Scenario 2: Prevent Submission Under Conditions
```python
def on_order_submit(doc, method):
	"""Prevent submission if conditions not met"""
	if doc.grand_total == 0:
		frappe.throw(_("Cannot submit order with zero total"))
```

### Scenario 3: Create Related Documents
```python
def on_order_submit(doc, method):
	"""Create invoice when order is submitted"""
	if doc.auto_create_invoice:
		invoice = frappe.get_doc({
			"doctype": "Invoice",
			"order_id": doc.name,
			"customer": doc.customer,
			"grand_total": doc.grand_total
		})
		invoice.insert()
		invoice.submit()
```

### Scenario 4: Sync to External System
```python
def on_order_update(doc, method):
	"""Sync order changes to external API"""
	frappe.enqueue(
		"myapp.integrations.sync_order",
		queue="long",
		order_id=doc.name
	)
```

### Scenario 5: Send Notifications
```python
def on_order_submit(doc, method):
	"""Send order confirmation email"""
	frappe.sendmail(
		recipients=[doc.customer_email],
		subject=f"Order {doc.name} Confirmed",
		message=f"Your order total: {doc.grand_total}"
	)
```

---

## Anti-Patterns & What NOT to Do

❌ **Don't**: Call `doc.save()` inside `before_save()` hook
```python
# WRONG - causes infinite loop
def before_save(doc, method):
	doc.field = "value"
	doc.save()  # ❌ DO NOT DO THIS
```

❌ **Don't**: Use synchronous long-running operations in hooks
```python
# WRONG - blocks request
def on_submit(doc, method):
	requests.post("https://slow-external-api.com/sync", data=doc)  # ❌ SLOW
```

✅ **Do**: Use `frappe.enqueue()` for async work
```python
# CORRECT - async background job
def on_submit(doc, method):
	frappe.enqueue("myapp.tasks.sync_to_external", queue="long", order_id=doc.name)
```

❌ **Don't**: Ignore exceptions in hooks
```python
# WRONG - errors silently fail
def on_update(doc, method):
	try:
		external_sync(doc)
	except:
		pass  # ❌ SILENT FAILURE
```

✅ **Do**: Log errors for debugging
```python
# CORRECT - log for visibility
def on_update(doc, method):
	try:
		external_sync(doc)
	except Exception as e:
		frappe.log_error(f"Sync failed: {str(e)}", title="External Sync Error")
```

---

## Decision Tree: When to Call Hooks-Orchestrator

**Use Hooks-Orchestrator when:**
- ✅ Setting up document lifecycle automation
- ✅ Creating scheduled/background tasks
- ✅ Implementing event-driven workflows
- ✅ Managing request-level customization
- ✅ Setting up fixture data loading
- ✅ Integrating external systems via hooks

**Don't use for:**
- ❌ DocType field design (use DocType-Architect)
- ❌ API endpoint creation (use API-Whitelister)
- ❌ Complex business logic (separate into modules)
- ❌ Permission management (use Permission-Guardian)

---

## Common Issues & Solutions

**Issue**: Hook not firing
```
Solution:
1. Check hook is registered in hooks.py
2. Verify method path is correct (module.function)
3. Check method has correct signature: def method_name(doc, method)
4. Run: bench --site mysite.local clear-cache
```

**Issue**: Hook fires multiple times
```
Solution:
1. Check for recursive save() calls
2. Add guard: if doc.flags.skip_custom_hook: return
3. Use doc.get_doc_before_save() to check changes
```

**Issue**: Scheduled task not running
```
Solution:
1. Verify RQ worker is running: ps aux | grep rq
2. Check Redis connection: redis-cli ping
3. Verify hook syntax in hooks.py
4. Check scheduler is enabled in site_config
```

---

## Integration Points

**Works closely with:**
- DocType-Architect: Validates field changes via hooks
- API-Whitelister: Calls APIs from hook functions
- Database-Navigator: Executes database operations in hooks
- Integration-Specialist: Syncs external systems via hooks
- Workflow-Wizard: Triggers workflow changes via hooks

**Key files:**
- `apps/myapp/myapp/hooks.py` - Hook registration
- `apps/myapp/myapp/tasks.py` - Scheduled task implementations
- `apps/myapp/myapp/doctype/{name}/{name}.py` - Document hooks (alternative location)

---

**Last Updated**: 2026-02-19
**Frappe Version**: v15.100.1
**Framework Stability**: Production-ready
