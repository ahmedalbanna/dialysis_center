# Developer Guide
## Dialysis Center Management System - Architecture & Extension

**Version**: 1.0.0  
**Last Updated**: February 19, 2026  
**Audience**: Software Developers, System Architects, Integration Engineers

---

## Part 1: Application Architecture

### 1.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Browser / Client                      │
│  (Vue.js Frontend, Frappe Desk, Custom Pages)          │
└────────────────────────┬────────────────────────────────┘
                         │ HTTPS
┌────────────────────────▼────────────────────────────────┐
│              Frappe Web Server (Werkzeug)               │
│  - Request routing                                      │
│  - Session management                                   │
│  - Authentication                                       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│         Dialysis Center Application Layer               │
│  - API Controllers (/api directory)                     │
│  - Document Controllers (DocType .py files)             │
│  - Business Logic                                       │
│  - Validations                                          │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│         Frappe ORM / Data Layer                         │
│  - Document model                                       │
│  - DocType metadata                                     │
│  - Permissions system                                   │
│  - Hooks system                                         │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│      Database Layer (MariaDB)                           │
│  - Patient, Appointment, Session tables                 │
│  - User & Permission tables                             │
│  - Audit & Log tables                                   │
└─────────────────────────────────────────────────────────┘

Side Components:
├─ Redis: Session cache, job queue
├─ Worker: Background jobs, scheduled tasks
└─ File Storage: Attachments, uploads
```

### 1.2 Module Organization

```
dialysis_center/
├── patient_management/              # Patient data & workflows
│   ├── doctype/
│   │   ├── patient/
│   │   ├── patient_document/
│   │   ├── patient_category/
│   │   └── patient_insurance/
│   ├── page/                        # Custom pages
│   ├── report/                      # Patient-related reports
│   └── __init__.py
├── appointment_scheduling/          # Appointment workflows
│   ├── doctype/
│   │   ├── appointment/
│   │   ├── recurring_appointment/
│   │   └── appointment_reminder/
│   ├── page/
│   └── __init__.py
├── dialysis_center_management/     # Session workflows
│   ├── doctype/
│   │   ├── dialysis_session/
│   │   ├── vital_signs_log/
│   │   └── machine_schedule/
│   └── __init__.py
├── billing_management/              # Billing & invoices
│   ├── doctype/
│   │   ├── patient_bill/
│   │   └── bill_payment/
│   └── __init__.py
├── laboratory_management/           # Lab tests
│   ├── doctype/
│   │   ├── lab_test/
│   │   ├── lab_test_template/
│   │   └── lab_test_result/
│   └── __init__.py
├── equipment_management/            # Dialysis machines
│   ├── doctype/
│   │   ├── dialysis_machine/
│   │   ├── machine_maintenance/
│   │   └── water_system/
│   └── __init__.py
├── staff_management/                # Staff & schedules
│   ├── doctype/
│   │   ├── staff/
│   │   ├── staff_shift/
│   │   └── staff_schedule/
│   └── __init__.py
├── api/                             # REST API endpoints
│   ├── patient_api.py
│   ├── appointment_api.py
│   ├── session_api.py
│   ├── billing_api.py
│   └── __init__.py
├── hooks.py                         # App configuration
├── modules.txt                      # Module listing
└── __init__.py
```

### 1.3 Data Model Architecture

**Core Entities**:
1. **Patient** (Master)
   - Basic demographics
   - Medical history
   - Insurance info
   - Vascular access details

2. **Appointment** (Transaction)
   - References Patient
   - Scheduled time/machine
   - Status tracking

3. **Dialysis Session** (Transaction)
   - References Patient & Appointment
   - Treatment parameters
   - Vital signs (child table)
   - Session workflow

4. **Patient Bill** (Transaction)
   - References Patient & Session
   - Line items (services)
   - Payment tracking

5. **Lab Test** (Transaction)
   - References Patient
   - Test orders & results
   - Linked to sessions

**Supporting Entities**:
- Staff, Dialysis Machine, Water System
- Insurance, Insurance Claim
- Recurring Appointment
- Staff Schedule

---

## Part 2: Extending the Application

### 2.1 Adding a New DocType

**Step 1: Create DocType Structure**
```bash
# From bench directory
cd apps/dialysis_center/dialysis_center/patient_management/doctype
mkdir patient_referral
cd patient_referral
```

**Step 2: Create DocType JSON** (`patient_referral.json`):
```json
{
  "autoname": "format:REF-{YYYY}-{#####}",
  "creation": "2026-02-19",
  "doctype": "DocType",
  "document_type": "Document",
  "editable_grid": 1,
  "engine": "InnoDB",
  "field": [
    {
      "fieldname": "patient",
      "fieldtype": "Link",
      "label": "Patient",
      "options": "Patient",
      "reqd": 1
    },
    {
      "fieldname": "referring_doctor",
      "fieldtype": "Data",
      "label": "Referring Doctor",
      "reqd": 1
    },
    {
      "fieldname": "referral_date",
      "fieldtype": "Date",
      "label": "Referral Date",
      "reqd": 1
    },
    {
      "fieldname": "reason",
      "fieldtype": "Text Editor",
      "label": "Reason for Referral"
    },
    {
      "fieldname": "status",
      "fieldtype": "Select",
      "label": "Status",
      "options": "New\nProcessing\nCompleted\nCancelled"
    }
  ],
  "idx": 0,
  "issingle": 0,
  "istable": 0,
  "modified": "2026-02-19",
  "modified_by": "Administrator",
  "module": "Patient Management",
  "name": "Patient Referral",
  "owner": "Administrator",
  "permissions": [
    {
      "create": 1,
      "default": 1,
      "delete": 1,
      "read": 1,
      "role": "Dialysis Administrator",
      "write": 1
    }
  ],
  "sort_field": "modified",
  "sort_order": "DESC",
  "states": [],
  "track_changes": 1
}
```

**Step 3: Create Controller** (`patient_referral.py`):
```python
import frappe
from frappe.model.document import Document

class PatientReferral(Document):
    def validate(self):
        """Validate referral data"""
        # Check patient exists
        if not frappe.db.exists("Patient", self.patient):
            frappe.throw(f"Patient {self.patient} not found")
        
        # Referral date cannot be in future
        from frappe.utils import getdate, today
        if getdate(self.referral_date) > getdate(today()):
            frappe.throw("Referral date cannot be in the future")
    
    def on_submit(self):
        """Actions on submit"""
        # Log the referral
        frappe.log(f"Referral created for {self.patient}")
        
        # Send notification to clinic manager
        frappe.sendmail(
            recipients=["manager@clinic.com"],
            subject=f"New Patient Referral: {self.patient}",
            message=f"Referral {self.name} from {self.referring_doctor}"
        )
```

**Step 4: Create Tests** (`test_patient_referral.py`):
```python
import frappe
from frappe.tests import IntegrationTestCase

class TestPatientReferral(IntegrationTestCase):
    def test_referral_creation(self):
        """Test creating a referral"""
        referral = frappe.get_doc({
            "doctype": "Patient Referral",
            "patient": "PT-001",
            "referring_doctor": "Dr. Smith",
            "referral_date": "2026-02-19",
            "reason": "Dialysis treatment"
        })
        referral.insert()
        
        self.assertEqual(referral.status, "New")
        self.assertTrue(frappe.db.exists("Patient Referral", referral.name))
```

**Step 5: Register in Module**
- Add to `modules.txt`:
  ```
  Patient Management
  ```
- Update `__init__.py`:
  ```python
  from .doctype.patient_referral import patient_referral
  ```

**Step 6: Migrate & Test**
```bash
cd frappe-bench
bench --site dialysis.local migrate
bench --site dialysis.local run-tests --module dialysis_center
```

### 2.2 Adding Custom Fields to Existing DocType

**Method 1: Programmatic** (in hooks.py or install script):
```python
def add_custom_fields():
    """Add custom fields to Patient DocType"""
    frappe.get_doc({
        "doctype": "Custom Field",
        "dt": "Patient",
        "fieldname": "custom_patient_code",
        "fieldtype": "Data",
        "label": "Custom Patient Code",
        "insert_after": "name",
        "is_mandatory": 0,
        "read_only": 0,
        "in_list_view": 1,
        "unique": 1
    }).insert(ignore_permissions=True)
```

**Method 2: UI**:
1. Go to Patient DocType
2. Click "Customize Form"
3. Click "Add Row"
4. Fill field details
5. Click "Save Customization"

### 2.3 Creating Custom Reports

**Step 1: Create Report File** (`patient_dialysis_frequency_report.py`):
```python
import frappe
from frappe import _

def execute(filters=None):
    """Generate patient dialysis frequency report"""
    columns = [
        {"label": _("Patient"), "fieldname": "patient_name", "width": 200},
        {"label": _("Frequency"), "fieldname": "frequency", "width": 100},
        {"label": _("Sessions/Month"), "fieldname": "sessions_per_month", "width": 150},
    ]
    
    data = frappe.db.sql("""
        SELECT 
            p.name,
            p.patient_name,
            p.dialysis_frequency,
            CASE 
                WHEN p.dialysis_frequency = '2x/week' THEN 8
                WHEN p.dialysis_frequency = '3x/week' THEN 12
                ELSE 0
            END as sessions_per_month
        FROM `tabPatient` p
        WHERE p.docstatus != 2
        ORDER BY p.patient_name
    """, as_dict=True)
    
    return columns, data
```

**Step 2: Register in Hooks**:
```python
# In hooks.py
fixture = [
    {"dt": "Report", "filters": [["name", "=", "Patient Dialysis Frequency Report"]]}
]
```

### 2.4 Creating API Endpoints

**Add to `/api` Directory** (`custom_api.py`):
```python
import frappe

@frappe.whitelist()
def get_patient_statistics():
    """Get summary statistics for all patients"""
    total_patients = frappe.db.count("Patient")
    active_patients = frappe.db.count("Patient", {"docstatus": 0})
    
    return {
        "total": total_patients,
        "active": active_patients,
        "inactive": total_patients - active_patients
    }

@frappe.whitelist()
def search_patients_advanced(patient_name, blood_type=None, vascular_access=None):
    """Advanced patient search"""
    filters = {"docstatus": 0}
    
    if patient_name:
        filters["patient_name"] = ["like", f"%{patient_name}%"]
    if blood_type:
        filters["blood_type"] = blood_type
    if vascular_access:
        filters["vascular_access_type"] = vascular_access
    
    patients = frappe.get_all("Patient", 
        filters=filters,
        fields=["name", "patient_name", "blood_type"],
        limit=20
    )
    
    return patients
```

**Register in Hooks** (`hooks.py`):
```python
# Add to hooks
from dialysis_center.api.custom_api import get_patient_statistics, search_patients_advanced
```

**Call via REST API**:
```bash
# GET request
curl "http://localhost:8000/api/method/dialysis_center.api.custom_api.get_patient_statistics"

# POST request with parameters
curl -X POST "http://localhost:8000/api/method/dialysis_center.api.custom_api.search_patients_advanced" \
  -H "Content-Type: application/json" \
  -d '{"patient_name": "John", "blood_type": "O+"}'
```

### 2.5 Implementing Workflows

**Create Workflow for Patient Bill Approval**:

1. Go to Workflow (in Frappe setup)
2. Create workflow:
   - **Document Type**: Patient Bill
   - **States**:
     - Draft (initial)
     - Pending Approval
     - Approved
     - Rejected
   
3. **Transitions**:
   - Draft → Pending Approval (on submit)
   - Pending Approval → Approved (by Accounts Manager)
   - Pending Approval → Rejected (by Accounts Manager)
   - Approved → Paid (when payment recorded)

4. **Notifications**:
   - On state change: Send email to approver

5. **Conditions** (optional):
   - If amount > $5000: Require Manager approval
   - If amount < $1000: Auto-approve

**Workflow Implementation in Code**:
```python
class PatientBill(Document):
    def before_submit(self):
        """Before submission - change workflow state"""
        if self.grand_total > 5000:
            # Set to pending approval
            frappe.db.set_value("Workflow State", self.name, "state", "Pending Approval")
    
    def on_update_after_submit(self):
        """Handle workflow state changes"""
        if self.workflow_state == "Approved":
            # Auto-generate invoice
            self.generate_invoice()
```

---

## Part 3: Development Environment Setup

### 3.1 Local Development Setup

**Prerequisites**:
- Python 3.10+
- Node.js 18+
- MariaDB 10.11+
- Redis 7.0+
- Git

**Clone & Setup**:
```bash
# Clone repository
git clone https://github.com/your-org/dialysis-center.git
cd dialysis-center

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Frappe & dependencies
pip install frappe-bench
bench init frappe-bench
cd frappe-bench

# Clone app into apps directory
git clone https://github.com/your-org/dialysis-center apps/dialysis_center

# Create site
bench new-site dev.local

# Install app
bench --site dev.local install-app dialysis_center

# Start development server
bench start
```

**Access Application**:
- Browser: `http://127.0.0.1:8000`
- Username: Administrator
- Password: admin

### 3.2 Git Workflow

**Feature Branch**:
```bash
# Create feature branch
git checkout -b feature/add-referral-system

# Make changes
vim dialysis_center/patient_management/doctype/patient_referral/patient_referral.py

# Commit with conventional message
git add .
git commit -m "feat: add patient referral DocType with validation"

# Push to remote
git push origin feature/add-referral-system

# Create Pull Request on GitHub
# - Add description
# - Link to issues
# - Request review
```

**Commit Message Convention**:
```
feat: add new feature
fix: fix bug
docs: documentation changes
style: code style changes (formatting, semicolons)
refactor: code refactoring
test: add/modify tests
chore: build process, dependencies
```

### 3.3 Hot Reload & Development Features

**Enable Hot Reload**:
```bash
cd frappe-bench
bench watch
```

**Development Tools**:
- Browser console: Press F12
- Frappe console: Type in page
- Error messages: Detailed in browser
- Form errors: Highlighted in red

### 3.4 Debugging

**Python Debugging**:
```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use ipdb (better formatting)
import ipdb; ipdb.set_trace()

# Commands:
# n = next line
# s = step into
# c = continue
# p variable_name = print variable
# l = list code
# h = help
```

**Frappe Console Debugging**:
```javascript
// In browser console
frappe.db.get_doc("Patient", "PT-001", function(r) {
    console.log(r.message);
});

// Check current form
console.log(cur_frm.doc);

// Reload form
cur_frm.reload_doc();
```

---

## Part 4: Testing

### 4.1 Unit Tests

**Write Test** (`test_patient.py`):
```python
import frappe
from frappe.tests import IntegrationTestCase

class TestPatient(IntegrationTestCase):
    def setUp(self):
        """Setup before each test"""
        self.patient = frappe.get_doc({
            "doctype": "Patient",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "contact_number": "555-1234",
            "email": "john@example.com"
        })
        self.patient.insert()
    
    def test_patient_creation(self):
        """Test patient can be created"""
        self.assertTrue(frappe.db.exists("Patient", self.patient.name))
    
    def test_patient_validation(self):
        """Test patient validation"""
        bad_patient = frappe.get_doc({
            "doctype": "Patient",
            "first_name": "Jane"
            # Missing required fields
        })
        
        with self.assertRaises(frappe.ValidationError):
            bad_patient.insert()
    
    def tearDown(self):
        """Cleanup after each test"""
        frappe.delete_doc("Patient", self.patient.name)
```

**Run Tests**:
```bash
# Run all tests
bench --site dev.local run-tests

# Run module tests
bench --site dev.local run-tests --module dialysis_center

# Run specific test
bench --site dev.local run-tests --test dialysis_center.patient_management.doctype.patient.test_patient.TestPatient.test_patient_creation

# With coverage
bench --site dev.local run-tests --coverage
```

### 4.2 API Testing

**Test API Endpoint** (with curl):
```bash
# GET request
curl "http://localhost:8000/api/method/dialysis_center.api.patient_api.get_patient_list"

# POST request
curl -X POST "http://localhost:8000/api/method/dialysis_center.api.patient_api.create_patient" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "date_of_birth": "1985-05-15",
    "gender": "Female",
    "contact_number": "555-5678",
    "email": "jane@example.com"
  }'
```

**Test with Python**:
```python
import requests

# Setup
url = "http://localhost:8000/api/method/dialysis_center.api.patient_api.get_patient_list"
session = requests.Session()

# Test API
response = session.get(url)
assert response.status_code == 200
data = response.json()
print(data["message"])
```

---

## Part 5: Deployment

### 5.1 Production Deployment

**Build Assets**:
```bash
cd frappe-bench
bench build
```

**Create Production Site**:
```bash
bench new-site production.clinic.com --admin-password=SecurePassword123
```

**Install App**:
```bash
bench --site production.clinic.com install-app dialysis_center
```

**Configure Supervisor** (for process management):
```ini
[program:frappe-web]
command=bench serve --port 8000
directory=/path/to/frappe-bench
user=frappe
autostart=true
autorestart=true
startsecs=0
stopwaitsecs=10

[program:frappe-worker]
command=bench worker default
directory=/path/to/frappe-bench
user=frappe
autostart=true
autorestart=true
```

### 5.2 Deployment Checklist

- [ ] Code reviewed and tested
- [ ] Database backed up
- [ ] Assets built
- [ ] Migrations run
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Performance verified
- [ ] Security audit completed
- [ ] Rollback plan prepared

---

## Quick Reference: Frappe API

```python
# Create document
doc = frappe.get_doc({
    "doctype": "Patient",
    "first_name": "John"
})
doc.insert()

# Read document
doc = frappe.get_doc("Patient", "PT-001")

# Update document
doc.first_name = "Jane"
doc.save()

# Delete document
frappe.delete_doc("Patient", "PT-001")

# Query
docs = frappe.get_all("Patient", filters={"status": "Active"})
count = frappe.db.count("Patient")
exists = frappe.db.exists("Patient", "PT-001")

# Validate
frappe.throw("Error message")
frappe.msgprint("Warning message")

# Log
frappe.log("Log message")
frappe.log_error("Error for debugging")
```

---

**End of Developer Guide**

