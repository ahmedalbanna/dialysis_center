# Phase 1 Validations Quick Reference Guide

## For Developers Extending These DocTypes

### Standard Validation Pattern Used

```python
def validate(self):
    """Main validation method - called before save"""
    self.validate_required_fields()
    self.validate_business_rules()
    self.validate_relationships()
    self.calculate_derived_fields()

def before_save(self):
    """Data preparation - normalize and calculate"""
    # Trim whitespace
    # Normalize formats (lowercase email, uppercase IDs)
    # Calculate dependent fields
    # Set defaults

def on_update(self):
    """Post-save cleanup - update caches and related docs"""
    # Clear caches
    frappe.cache.delete_value(f"doctype_{self.name}")

def on_submit(self):
    """Handle submission - create related docs, update summaries"""
    # Update related documents
    # Create audit trails
    # Update statistics

def on_cancel(self):
    """Reverse operations on cancellation"""
    # Undo on_submit changes
    # Clear caches
```

---

## Validation Error Patterns

### Pattern 1: Required Field
```python
def validate_required_fields(self):
    if not self.field_name:
        frappe.throw(_("Field Name is required"))
```

### Pattern 2: Format Validation
```python
def validate_contact_info(self):
    if self.email:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            frappe.throw(_("Invalid email address format"))
```

### Pattern 3: Range Validation
```python
def validate_amounts(self):
    if flt(self.amount) <= 0:
        frappe.throw(_("Amount must be greater than 0"))
```

### Pattern 4: Cross-Field Validation
```python
def validate_dates(self):
    if self.start_date and self.end_date:
        if getdate(self.start_date) > getdate(self.end_date):
            frappe.throw(_("Start date must be before end date"))
```

### Pattern 5: Related Document Validation
```python
def validate_patient(self):
    if self.patient:
        patient_status = frappe.db.get_value("Patient", self.patient, "status")
        if patient_status != "Active":
            frappe.throw(_("Patient must be Active"))
```

### Pattern 6: Uniqueness Validation
```python
def validate_unique_id(self):
    if self.unique_id:
        duplicate = frappe.db.exists("DocType", {
            "unique_id": self.unique_id,
            "name": ["!=", self.name or '']
        })
        if duplicate:
            frappe.throw(_("ID already exists"))
```

### Pattern 7: Warning/Alert (Non-blocking)
```python
def check_warning_condition(self):
    if condition:
        frappe.msgprint(_("Warning message"),
            indicator="orange", alert=True)
```

### Pattern 8: Critical Alert (Non-blocking)
```python
def check_critical_condition(self):
    if critical_condition:
        frappe.msgprint(_("CRITICAL: Message"),
            indicator="red", alert=True)
```

---

## Data Normalization Pattern

```python
def before_save(self):
    """Normalize all text fields consistently"""
    
    # Trim whitespace
    if self.text_field:
        self.text_field = self.text_field.strip()
    
    # Lowercase email
    if self.email:
        self.email = self.email.lower().strip()
    
    # Uppercase ID
    if self.id_field:
        self.id_field = self.id_field.strip().upper()
    
    # Set defaults
    if not self.status:
        self.status = "Active"
    
    # Calculate derived fields
    self.calculate_totals()
```

---

## Cache Management Pattern

```python
def on_update(self):
    """Always clear caches after update"""
    
    # Document-specific cache
    frappe.cache.delete_value(f"doctype_{self.name}")
    
    # Related document caches
    frappe.cache.delete_value(f"patient_{self.patient}_documents")
    frappe.cache.delete_value(f"patient_{self.patient}_summary")
    
    # List caches
    frappe.cache.delete_value("doctype_list")
```

---

## Hook Execution Guarantee

For each save operation:

```
1. validate()           ← Business logic validation
2. before_save()        ← Data normalization
3. [Database Save]      ← Insert/Update
4. on_update()          ← Post-save cleanup
5. [End of Save]
```

For submission:
```
1. before_submit()      ← Final validation
2. on_submit()          ← Create related docs
3. [Status → Submitted]
```

For cancellation:
```
1. on_cancel()          ← Reverse operations
2. [Status → Cancelled]
```

---

## Error Message Standards

### Always Use Localization
```python
# ✅ CORRECT - Localized
frappe.throw(_("Patient Name is required"))

# ❌ WRONG - Not localized
frappe.throw("Patient Name is required")
```

### Use Proper Indicators
```python
# Error (stops save)
frappe.throw(_("Error: Something failed"))

# Warning (allows save)
frappe.msgprint(_("Warning: Check this"),
    indicator="orange", alert=True)

# Critical (allows save, red alert)
frappe.msgprint(_("CRITICAL: Immediate action needed"),
    indicator="red", alert=True)

# Info (allows save, blue alert)
frappe.msgprint(_("Info: For your reference"),
    indicator="blue", alert=True)
```

---

## Common Validation Checks by DocType Type

### Master DocTypes (Customer, Product, etc.)
- ✅ Mandatory field checks
- ✅ Format validation (email, phone, ID)
- ✅ Uniqueness checks
- ✅ Data normalization
- ✅ Default value setting

### Transaction DocTypes (Invoice, Order, etc.)
- ✅ Mandatory field checks
- ✅ Related master validation
- ✅ Child table validation
- ✅ Amount/quantity validation
- ✅ Total calculations
- ✅ Date range validation
- ✅ Status validation

### Submittable DocTypes (Session, Payment, etc.)
- ✅ All transaction validations
- ✅ Pre-submission state checks
- ✅ Post-submission cascading updates
- ✅ Reversal on cancellation
- ✅ Audit trail creation

---

## Testing Your Validations

### Unit Test Template
```python
import frappe
from frappe.tests import IntegrationTestCase

class TestYourDocType(IntegrationTestCase):
    def test_required_field_validation(self):
        """Test mandatory field check"""
        with self.assertRaises(frappe.ValidationError):
            doc = frappe.get_doc({
                "doctype": "YourDocType",
                # Missing required field
            })
            doc.insert()
    
    def test_format_validation(self):
        """Test email/phone format"""
        with self.assertRaises(frappe.ValidationError):
            doc = frappe.get_doc({
                "doctype": "YourDocType",
                "email": "invalid-email"
            })
            doc.insert()
    
    def test_warning_alert(self):
        """Test non-blocking warning"""
        doc = frappe.get_doc({
            "doctype": "YourDocType",
            "some_field": "value"
        })
        doc.insert()
        # Should succeed with warning
        self.assertTrue(frappe.db.exists("YourDocType", doc.name))
```

---

## Common Pitfalls to Avoid

### ❌ DON'T: Use unescaped SQL
```python
# WRONG - SQL injection vulnerable
result = frappe.db.sql(f"SELECT * FROM tabPatient WHERE name = '{patient_id}'")
```

### ✅ DO: Use parameterized queries
```python
# CORRECT - Safe from SQL injection
result = frappe.db.sql("SELECT * FROM tabPatient WHERE name = %s", (patient_id,))
```

### ❌ DON'T: Forget to normalize data
```python
# WRONG - Data quality issues
self.email = data['email']  # May have spaces
```

### ✅ DO: Normalize in before_save
```python
# CORRECT - Clean data
self.email = self.email.lower().strip() if self.email else ""
```

### ❌ DON'T: Forget cache clearing
```python
# WRONG - Stale data served
def on_update(self):
    self.update_related_docs()
```

### ✅ DO: Clear caches
```python
# CORRECT - Fresh data
def on_update(self):
    self.update_related_docs()
    frappe.cache.delete_value(f"doc_{self.name}")
```

### ❌ DON'T: Hardcode error messages
```python
# WRONG - Not translatable
frappe.throw("Patient Name is required")
```

### ✅ DO: Use localization
```python
# CORRECT - Translatable
frappe.throw(_("Patient Name is required"))
```

---

## Extending Existing Validations

When you need to add validation to an existing DocType:

```python
class PatientExtended(Patient):
    def validate(self):
        """Add custom validation without breaking existing ones"""
        # Call parent validation first
        super().validate()
        
        # Add your custom validation
        self.validate_custom_requirement()
    
    def validate_custom_requirement(self):
        """Your custom validation logic"""
        if some_condition:
            frappe.throw(_("Your custom error"))
```

---

## Performance Tips

### ✅ DO: Batch database queries
```python
# Good - Single query
patient_ids = ["P001", "P002", "P003"]
patients = frappe.get_all("Patient",
    filters={"name": ["in", patient_ids]}
)
```

### ❌ DON'T: N+1 queries
```python
# Bad - Multiple queries in loop
for id in patient_ids:
    patient = frappe.get_doc("Patient", id)  # Query for each!
```

### ✅ DO: Use flt() for safe number comparison
```python
if flt(self.amount) > 0:  # Safe comparison
```

### ✅ DO: Cache frequently accessed data
```python
cache_key = f"patient_{self.patient}_summary"
cached = frappe.cache.get_value(cache_key)
if not cached:
    cached = expensive_calculation()
    frappe.cache.set_value(cache_key, cached)
```

---

## Debugging Tips

### Enable detailed logging
```python
def validate(self):
    frappe.logger().info(f"Validating {self.doctype} {self.name}")
    frappe.logger().debug(f"Patient status: {self.patient_status}")
```

### Print SQL queries
```python
# In your method
frappe.db.print_sql(True)  # Show SQL being executed
result = frappe.db.sql("...")
frappe.db.print_sql(False)  # Turn off
```

### Check hook execution
```python
def validate(self):
    print("validate() called")

def before_save(self):
    print("before_save() called")

def on_update(self):
    print("on_update() called")
```

---

## Version & Compatibility

- **Framework Version:** v15.100.1
- **Python Version:** 3.10+
- **Database:** MariaDB 10.11+
- **Cache:** Redis 7.0+

---

## Related Documentation

- [Frappe Model & ORM](https://frappeframework.com/docs/user/en/api)
- [Document Lifecycle](https://frappeframework.com/docs/user/en/doc-api/lifecycle)
- [Validation & Permissions](https://frappeframework.com/docs/user/en/desk-api/validation)
- [Internationalization](https://frappeframework.com/docs/user/en/translations)

---

**Last Updated:** 2026-02-19  
**Maintained By:** DocType-Architect Subagent
