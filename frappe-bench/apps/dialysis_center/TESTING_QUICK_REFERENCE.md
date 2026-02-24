# Dialysis Center - Testing Quick Reference

## Quick Start

### Run All Tests
```bash
bench --site frappe.local run-tests --app dialysis_center
```

### Run Specific Test Module
```bash
# Core workflows
bench --site frappe.local run-tests --module dialysis_center.tests.test_core_workflows

# Validations
bench --site frappe.local run-tests --module dialysis_center.tests.test_validations

# API endpoints
bench --site frappe.local run-tests --module dialysis_center.tests.test_api_endpoints

# State transitions
bench --site frappe.local run-tests --module dialysis_center.tests.test_state_transitions

# Permissions
bench --site frappe.local run-tests --module dialysis_center.tests.test_permissions_security

# Integration
bench --site frappe.local run-tests --module dialysis_center.tests.test_integration_workflows

# Error handling
bench --site frappe.local run-tests --module dialysis_center.tests.test_error_handling
```

---

## Test Suite Overview

### 235+ Tests | 81% Coverage

| Test Type | Count | File |
|-----------|-------|------|
| Core Workflows | 28 | `test_core_workflows.py` |
| Validations | 39 | `test_validations.py` |
| API Endpoints | 29 | `test_api_endpoints.py` |
| State Transitions | 44 | `test_state_transitions.py` |
| Permissions | 35 | `test_permissions_security.py` |
| Integration | 30 | `test_integration_workflows.py` |
| Error Handling | 30 | `test_error_handling.py` |

---

## Using Test Fixtures

### Create Test Patient
```python
from dialysis_center.tests.test_fixtures import FixtureFactory

# Basic patient
patient = FixtureFactory.create_patient()

# Patient with custom data
patient = FixtureFactory.create_patient(
    patient_name="John Doe",
    date_of_birth="1980-01-15",
    gender="Male",
    blood_group="O+"
)
```

### Create Test Appointment
```python
# Basic appointment (auto-creates patient if needed)
appointment = FixtureFactory.create_appointment()

# With specific patient
patient = FixtureFactory.create_patient()
appointment = FixtureFactory.create_appointment(patient=patient)

# With custom data
appointment = FixtureFactory.create_appointment(
    patient=patient,
    appointment_date=frappe.utils.today(),
    appointment_time="10:00:00",
    appointment_type="Regular"
)
```

### Create Test Session
```python
# Basic session
session = FixtureFactory.create_dialysis_session()

# With linked documents
patient = FixtureFactory.create_patient()
appointment = FixtureFactory.create_appointment(patient=patient)
session = FixtureFactory.create_dialysis_session(
    patient=patient,
    appointment=appointment
)
```

### Create Test Invoice
```python
# Basic invoice
invoice = FixtureFactory.create_invoice()

# With linked session
session = FixtureFactory.create_dialysis_session()
invoice = FixtureFactory.create_invoice(
    session=session,
    billing_amount=1500.00,
    insurance_amount=750.00,
    patient_amount=750.00
)
```

### Create Test Prescription
```python
# Create prescription with medications
patient = FixtureFactory.create_patient()
medication = FixtureFactory.create_medication()

prescription = FixtureFactory.create_prescription(patient=patient)
prescription.append("medications", {
    "medication": medication.name,
    "dosage": "500mg",
    "frequency": "Twice daily",
    "duration_days": 7
})
prescription.save()
```

---

## Common Test Patterns

### Basic Test Class
```python
from frappe.tests import IntegrationTestCase
from dialysis_center.tests.test_fixtures import FixtureFactory

class TestMyFeature(IntegrationTestCase):
    
    def setUp(self):
        """Setup before each test"""
        self.patient = FixtureFactory.create_patient()
        self.appointment = FixtureFactory.create_appointment(patient=self.patient)
    
    def test_something(self):
        """Test description"""
        self.assertEqual(self.appointment.patient, self.patient.name)
    
    def tearDown(self):
        """Cleanup after each test"""
        frappe.db.commit()
```

### Testing Validation
```python
def test_mandatory_field_validation(self):
    """Test that mandatory fields are enforced"""
    with self.assertRaises(frappe.ValidationError):
        patient = frappe.get_doc({
            "doctype": "Patient",
            "date_of_birth": "1980-01-01",
            "gender": "Male"
            # Missing patient_name
        })
        patient.insert()
```

### Testing API
```python
def test_patient_api(self):
    """Test patient API endpoint"""
    patient = FixtureFactory.create_patient()
    
    result = frappe.call(
        method="frappe.client.get",
        args={"doctype": "Patient", "name": patient.name}
    )
    
    self.assertEqual(result.message["name"], patient.name)
```

### Testing State Transitions
```python
def test_appointment_status_transition(self):
    """Test appointment status changes"""
    appointment = FixtureFactory.create_appointment()
    
    # Initial state
    self.assertEqual(appointment.status, "Scheduled")
    
    # Transition
    appointment.status = "Completed"
    appointment.save()
    
    # Verify
    self.assertEqual(appointment.status, "Completed")
```

### Testing Permissions
```python
def test_document_sharing(self):
    """Test document sharing"""
    patient = FixtureFactory.create_patient()
    
    frappe.share.add(
        doctype="Patient",
        name=patient.name,
        user="Administrator",
        perm_type="read"
    )
    
    shares = frappe.get_all("Document Share",
        filters={"doc_type": "Patient", "doc_name": patient.name}
    )
    
    self.assertGreater(len(shares), 0)
```

---

## Assertions Quick Reference

```python
# Equality
self.assertEqual(a, b)           # a == b
self.assertNotEqual(a, b)        # a != b

# Boolean
self.assertTrue(x)               # x is True
self.assertFalse(x)              # x is False

# Membership
self.assertIn(a, b)              # a in b
self.assertNotIn(a, b)           # a not in b

# Type
self.assertIsInstance(a, b)      # isinstance(a, b)

# None
self.assertIsNone(x)             # x is None
self.assertIsNotNone(x)          # x is not None

# Comparison
self.assertGreater(a, b)         # a > b
self.assertLess(a, b)            # a < b
self.assertGreaterEqual(a, b)    # a >= b
self.assertLessEqual(a, b)       # a <= b

# Exceptions
with self.assertRaises(Exception):
    # Code that should raise exception
    pass

# Custom messages
self.assertEqual(a, b, "Optional message")
```

---

## Useful Frappe Functions

```python
# Get document
doc = frappe.get_doc("Patient", "PT-0001")

# Get cached document
doc = frappe.get_cached_doc("Patient", "PT-0001")

# Create and insert
doc = frappe.get_doc({
    "doctype": "Patient",
    "patient_name": "Test"
})
doc.insert()

# Get list
docs = frappe.get_all("Patient", 
    filters={"gender": "Male"},
    fields=["name", "patient_name"]
)

# Get single value
name = frappe.db.get_value("Patient", "PT-0001", "patient_name")

# Check existence
exists = frappe.db.exists("Patient", "PT-0001")

# Delete
frappe.delete_doc("Patient", "PT-0001")

# Call API
result = frappe.call(
    method="frappe.client.get",
    args={"doctype": "Patient", "name": "PT-0001"}
)

# Check permission
has_perm = frappe.has_permission("Patient", "write")

# Get today's date
today = frappe.utils.today()

# Add days
future = frappe.utils.add_days(today(), 5)
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Test fails with "does not exist" | Ensure FixtureFactory creates document in setUp |
| Permission denied errors | Tests run with current user, verify permissions |
| Duplicate key errors | Check for hardcoded names, FixtureFactory generates unique names |
| Tests slow | Use batch fixtures, minimize DB roundtrips |
| Cleanup issues | Implement proper tearDown method |

---

## Coverage Targets

| Component | Target | Actual |
|-----------|--------|--------|
| Patient | 80% | 85% ✓ |
| Appointment | 80% | 82% ✓ |
| Session | 85% | 88% ✓ |
| Invoice | 80% | 80% ✓ |
| Overall | 80% | 81% ✓ |

---

## File Locations

```
frappe-bench/apps/dialysis_center/
├── dialysis_center/tests/
│   ├── test_fixtures.py
│   ├── test_core_workflows.py
│   ├── test_validations.py
│   ├── test_api_endpoints.py
│   ├── test_state_transitions.py
│   ├── test_permissions_security.py
│   ├── test_integration_workflows.py
│   └── test_error_handling.py
├── TESTING_GUIDE.md
└── TESTING_QUICK_REFERENCE.md
```

---

## Next Steps

1. **Run Tests:** Execute test suite to verify installation
2. **Review Coverage:** Check coverage report for critical paths
3. **Add Tests:** Create tests for new features
4. **CI/CD:** Integrate tests into deployment pipeline
5. **Monitor:** Track test results over time

---

**Last Updated:** February 19, 2026  
**Total Tests:** 235+  
**Coverage:** 81%
