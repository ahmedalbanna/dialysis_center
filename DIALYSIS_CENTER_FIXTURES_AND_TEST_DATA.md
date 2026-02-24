# Dialysis Center Management System
## Fixtures and Test Data Documentation

**Version:** 1.0  
**Last Updated:** 2026-02-19  
**Framework:** Frappe v15.100.1

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Understanding Fixtures](#2-understanding-fixtures)
3. [Core System Fixtures](#3-core-system-fixtures)
4. [Master Data Fixtures](#4-master-data-fixtures)
5. [Test Data Factory Patterns](#5-test-data-factory-patterns)
6. [Test Data Generation Scripts](#6-test-data-generation-scripts)
7. [Running Fixtures and Test Data](#7-running-fixtures-and-test-data)
8. [Integration with Tests](#8-integration-with-tests)
9. [Best Practices](#9-best-practices)
10. [Summary](#10-summary)

---

## 1. Introduction

### 1.1 Purpose

This document provides comprehensive guidance on:
- **Fixtures**: Pre-defined master data that ships with the application
- **Test Data**: Generated data for development, testing, and demonstration
- **Factory Patterns**: Reusable code for creating test records
- **Data Generation**: Scripts to populate the system with realistic data

### 1.2 Benefits

**Fixtures provide:**
- ✅ Consistent initial setup across all installations
- ✅ Required master data for application functionality
- ✅ Standard roles, permissions, and configurations
- ✅ Template data for common use cases

**Test Data enables:**
- ✅ Development without production data
- ✅ Automated testing with predictable datasets
- ✅ Demo environments for stakeholders
- ✅ Performance testing with realistic volumes

### 1.3 Fixtures vs Test Data

| Aspect | Fixtures | Test Data |
|--------|----------|-----------|
| **Purpose** | Production master data | Development/testing only |
| **Installation** | Auto-installed with app | Manually generated |
| **Versioning** | Version controlled | Generated on-demand |
| **Updates** | Managed via migrations | Recreated as needed |
| **Examples** | Roles, Settings, Templates | Sample patients, appointments |

---

## 2. Understanding Fixtures

### 2.1 What Are Fixtures?

Fixtures are JSON files containing DocType records that are automatically imported when an app is installed. They ensure every installation starts with consistent master data.

### 2.2 Fixture Configuration

Fixtures are defined in `hooks.py`:

**File:** `dialysis_center/hooks.py`

```python
# Fixtures - Auto-installed with the app
fixtures = [
    # Export all records from specific DocTypes
    "Role",
    "Workflow",
    "Workflow State",
    
    # Export specific records using filters
    {
        "dt": "Custom Field",
        "filters": [
            ["module", "=", "Dialysis Center"]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["module", "=", "Dialysis Center"]
        ]
    },
    
    # Export with specific fields
    {
        "dt": "Treatment Template",
        "filters": [
            ["is_standard", "=", 1]
        ]
    },
]
```

### 2.3 Creating Fixtures

#### Method 1: Export from Site

```bash
# Export specific DocType
bench --site [sitename] export-fixtures

# This reads fixtures from hooks.py and exports them to:
# dialysis_center/dialysis_center/fixtures/
```

#### Method 2: Manual Creation

Create JSON files in `dialysis_center/dialysis_center/fixtures/`:

```
dialysis_center/
└── dialysis_center/
    └── fixtures/
        ├── role.json
        ├── workflow.json
        ├── custom_field.json
        └── treatment_template.json
```

### 2.4 Fixture File Structure

```json
[
    {
        "doctype": "Role",
        "name": "Dialysis Nurse",
        "role_name": "Dialysis Nurse",
        "desk_access": 1,
        "disabled": 0
    },
    {
        "doctype": "Role",
        "name": "Dialysis Doctor",
        "role_name": "Dialysis Doctor",
        "desk_access": 1,
        "disabled": 0
    }
]
```

---

## 3. Core System Fixtures

### 3.1 Roles and Permissions

**File:** `dialysis_center/dialysis_center/fixtures/role.json`

```json
[
    {
        "doctype": "Role",
        "name": "Dialysis Administrator",
        "role_name": "Dialysis Administrator",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1,
        "restrict_to_domain": ""
    },
    {
        "doctype": "Role",
        "name": "Dialysis Doctor",
        "role_name": "Dialysis Doctor",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "name": "Dialysis Nurse",
        "role_name": "Dialysis Nurse",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "name": "Dialysis Technician",
        "role_name": "Dialysis Technician",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "name": "Dialysis Receptionist",
        "role_name": "Dialysis Receptionist",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "name": "Dialysis Billing Clerk",
        "role_name": "Dialysis Billing Clerk",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "name": "Dialysis Lab Technician",
        "role_name": "Dialysis Lab Technician",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "name": "Dialysis Inventory Manager",
        "role_name": "Dialysis Inventory Manager",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "name": "Dialysis Manager",
        "role_name": "Dialysis Manager",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "name": "Dialysis Viewer",
        "role_name": "Dialysis Viewer",
        "desk_access": 1,
        "disabled": 0,
        "is_custom": 1
    }
]
```

### 3.2 Workflow Fixtures

**File:** `dialysis_center/dialysis_center/fixtures/workflow.json`

```json
[
    {
        "doctype": "Workflow",
        "name": "Dialysis Session Workflow",
        "workflow_name": "Dialysis Session Workflow",
        "document_type": "Dialysis Session",
        "is_active": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Draft",
                "doc_status": 0,
                "allow_edit": "Dialysis Nurse",
                "style": "info"
            },
            {
                "state": "In Progress",
                "doc_status": 0,
                "allow_edit": "Dialysis Nurse",
                "style": "primary"
            },
            {
                "state": "Completed",
                "doc_status": 1,
                "allow_edit": "Dialysis Doctor",
                "style": "success"
            },
            {
                "state": "Cancelled",
                "doc_status": 2,
                "style": "danger"
            }
        ],
        "transitions": [
            {
                "state": "Draft",
                "action": "Start Session",
                "next_state": "In Progress",
                "allowed": "Dialysis Nurse",
                "allow_self_approval": 1
            },
            {
                "state": "In Progress",
                "action": "Complete",
                "next_state": "Completed",
                "allowed": "Dialysis Nurse",
                "allow_self_approval": 1
            },
            {
                "state": "In Progress",
                "action": "Cancel",
                "next_state": "Cancelled",
                "allowed": "Dialysis Doctor",
                "allow_self_approval": 0
            },
            {
                "state": "Draft",
                "action": "Cancel",
                "next_state": "Cancelled",
                "allowed": "Dialysis Nurse",
                "allow_self_approval": 1
            }
        ]
    },
    {
        "doctype": "Workflow",
        "name": "Invoice Approval Workflow",
        "workflow_name": "Invoice Approval Workflow",
        "document_type": "Invoice",
        "is_active": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Draft",
                "doc_status": 0,
                "allow_edit": "Dialysis Billing Clerk",
                "style": "info"
            },
            {
                "state": "Pending Approval",
                "doc_status": 0,
                "allow_edit": "Dialysis Manager",
                "style": "warning"
            },
            {
                "state": "Approved",
                "doc_status": 1,
                "style": "success"
            },
            {
                "state": "Rejected",
                "doc_status": 2,
                "style": "danger"
            }
        ],
        "transitions": [
            {
                "state": "Draft",
                "action": "Submit for Approval",
                "next_state": "Pending Approval",
                "allowed": "Dialysis Billing Clerk",
                "allow_self_approval": 1
            },
            {
                "state": "Pending Approval",
                "action": "Approve",
                "next_state": "Approved",
                "allowed": "Dialysis Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Pending Approval",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Dialysis Manager",
                "allow_self_approval": 0
            },
            {
                "state": "Rejected",
                "action": "Resubmit",
                "next_state": "Draft",
                "allowed": "Dialysis Billing Clerk",
                "allow_self_approval": 1
            }
        ]
    }
]
```

### 3.3 Custom Fields Fixtures

**File:** `dialysis_center/dialysis_center/fixtures/custom_field.json`

```json
[
    {
        "doctype": "Custom Field",
        "dt": "User",
        "fieldname": "employee_id",
        "label": "Employee ID",
        "fieldtype": "Data",
        "insert_after": "email",
        "module": "Dialysis Center"
    },
    {
        "doctype": "Custom Field",
        "dt": "User",
        "fieldname": "staff_type",
        "label": "Staff Type",
        "fieldtype": "Select",
        "options": "Nurse\nDoctor\nTechnician\nAdministrator\nReceptionist",
        "insert_after": "employee_id",
        "module": "Dialysis Center"
    },
    {
        "doctype": "Custom Field",
        "dt": "User",
        "fieldname": "license_number",
        "label": "License Number",
        "fieldtype": "Data",
        "insert_after": "staff_type",
        "depends_on": "eval:doc.staff_type == 'Doctor' || doc.staff_type == 'Nurse'",
        "module": "Dialysis Center"
    },
    {
        "doctype": "Custom Field",
        "dt": "User",
        "fieldname": "shift_preference",
        "label": "Shift Preference",
        "fieldtype": "Select",
        "options": "Morning\nEvening\nNight\nRotating",
        "insert_after": "license_number",
        "module": "Dialysis Center"
    }
]
```

### 3.4 Property Setters

**File:** `dialysis_center/dialysis_center/fixtures/property_setter.json`

```json
[
    {
        "doctype": "Property Setter",
        "doctype_or_field": "DocType",
        "doc_type": "Patient",
        "property": "quick_entry",
        "property_type": "Check",
        "value": "0",
        "module": "Dialysis Center"
    },
    {
        "doctype": "Property Setter",
        "doctype_or_field": "DocType",
        "doc_type": "Patient",
        "property": "track_changes",
        "property_type": "Check",
        "value": "1",
        "module": "Dialysis Center"
    },
    {
        "doctype": "Property Setter",
        "doctype_or_field": "DocType",
        "doc_type": "Dialysis Session",
        "property": "is_submittable",
        "property_type": "Check",
        "value": "1",
        "module": "Dialysis Center"
    }
]
```

### 3.5 System Settings Fixtures

**File:** `dialysis_center/dialysis_center/fixtures/dialysis_settings.json`

```json
[
    {
        "doctype": "Dialysis Settings",
        "name": "Dialysis Settings",
        "default_session_duration": 240,
        "default_blood_flow_rate": 300,
        "default_dialysate_flow_rate": 500,
        "allow_overlapping_appointments": 0,
        "appointment_buffer_time": 30,
        "auto_generate_invoices": 1,
        "session_rate": 1500.00,
        "require_doctor_approval": 1,
        "enable_sms_notifications": 1,
        "enable_email_notifications": 1,
        "reminder_hours_before": 24,
        "low_stock_alert_level": 20,
        "critical_stock_alert_level": 10,
        "enable_audit_trail": 1,
        "data_retention_days": 3650,
        "backup_frequency": "Daily",
        "enable_two_factor_auth": 1
    }
]
```

---

## 4. Master Data Fixtures

### 4.1 Treatment Templates

**File:** `dialysis_center/dialysis_center/fixtures/treatment_template.json`

```json
[
    {
        "doctype": "Treatment Template",
        "template_name": "Standard Hemodialysis",
        "dialysis_type": "Hemodialysis",
        "duration_minutes": 240,
        "blood_flow_rate_qb": 300,
        "dialysate_flow_rate_qd": 500,
        "dialyzer_type": "F60",
        "ultrafiltration_goal": 2.5,
        "heparin_protocol": "Standard",
        "heparin_loading_dose": 3000,
        "heparin_maintenance_dose": 1000,
        "is_standard": 1,
        "is_active": 1,
        "description": "Standard 4-hour hemodialysis treatment"
    },
    {
        "doctype": "Treatment Template",
        "template_name": "Short Hemodialysis",
        "dialysis_type": "Hemodialysis",
        "duration_minutes": 180,
        "blood_flow_rate_qb": 350,
        "dialysate_flow_rate_qd": 600,
        "dialyzer_type": "F80",
        "ultrafiltration_goal": 2.0,
        "heparin_protocol": "Standard",
        "heparin_loading_dose": 2500,
        "heparin_maintenance_dose": 800,
        "is_standard": 1,
        "is_active": 1,
        "description": "Short 3-hour high-efficiency dialysis"
    },
    {
        "doctype": "Treatment Template",
        "template_name": "Hemodiafiltration",
        "dialysis_type": "Hemodiafiltration",
        "duration_minutes": 240,
        "blood_flow_rate_qb": 350,
        "dialysate_flow_rate_qd": 500,
        "dialyzer_type": "FX80",
        "ultrafiltration_goal": 3.0,
        "convection_volume": 20,
        "heparin_protocol": "Standard",
        "heparin_loading_dose": 3000,
        "heparin_maintenance_dose": 1000,
        "is_standard": 1,
        "is_active": 1,
        "description": "High-flux hemodiafiltration treatment"
    },
    {
        "doctype": "Treatment Template",
        "template_name": "Low Heparin Protocol",
        "dialysis_type": "Hemodialysis",
        "duration_minutes": 240,
        "blood_flow_rate_qb": 280,
        "dialysate_flow_rate_qd": 500,
        "dialyzer_type": "F60",
        "ultrafiltration_goal": 2.5,
        "heparin_protocol": "Low Dose",
        "heparin_loading_dose": 1500,
        "heparin_maintenance_dose": 500,
        "is_standard": 1,
        "is_active": 1,
        "description": "For patients at risk of bleeding"
    },
    {
        "doctype": "Treatment Template",
        "template_name": "Heparin-Free Protocol",
        "dialysis_type": "Hemodialysis",
        "duration_minutes": 240,
        "blood_flow_rate_qb": 250,
        "dialysate_flow_rate_qd": 500,
        "dialyzer_type": "F60",
        "ultrafiltration_goal": 2.0,
        "heparin_protocol": "None",
        "heparin_loading_dose": 0,
        "heparin_maintenance_dose": 0,
        "saline_flush_interval": 30,
        "is_standard": 1,
        "is_active": 1,
        "description": "For patients with active bleeding or heparin allergy"
    }
]
```

### 4.2 Lab Test Templates

**File:** `dialysis_center/dialysis_center/fixtures/lab_test_template.json`

```json
[
    {
        "doctype": "Lab Test Template",
        "template_name": "Complete Blood Count (CBC)",
        "test_code": "CBC",
        "category": "Hematology",
        "frequency": "Monthly",
        "parameters": [
            {"parameter": "Hemoglobin", "unit": "g/dL", "normal_range": "12-16"},
            {"parameter": "Hematocrit", "unit": "%", "normal_range": "36-48"},
            {"parameter": "WBC Count", "unit": "×10³/μL", "normal_range": "4-11"},
            {"parameter": "Platelet Count", "unit": "×10³/μL", "normal_range": "150-450"}
        ],
        "is_standard": 1
    },
    {
        "doctype": "Lab Test Template",
        "template_name": "Kidney Function Panel",
        "test_code": "KFP",
        "category": "Clinical Chemistry",
        "frequency": "Monthly",
        "parameters": [
            {"parameter": "Creatinine", "unit": "mg/dL", "normal_range": "0.7-1.3"},
            {"parameter": "Urea/BUN", "unit": "mg/dL", "normal_range": "7-20"},
            {"parameter": "Uric Acid", "unit": "mg/dL", "normal_range": "3.5-7.2"},
            {"parameter": "eGFR", "unit": "mL/min", "normal_range": ">60"}
        ],
        "is_standard": 1
    },
    {
        "doctype": "Lab Test Template",
        "template_name": "Electrolyte Panel",
        "test_code": "ELEC",
        "category": "Clinical Chemistry",
        "frequency": "Weekly",
        "parameters": [
            {"parameter": "Sodium", "unit": "mmol/L", "normal_range": "136-145"},
            {"parameter": "Potassium", "unit": "mmol/L", "normal_range": "3.5-5.0"},
            {"parameter": "Chloride", "unit": "mmol/L", "normal_range": "98-106"},
            {"parameter": "Bicarbonate", "unit": "mmol/L", "normal_range": "22-29"}
        ],
        "is_standard": 1
    },
    {
        "doctype": "Lab Test Template",
        "template_name": "Dialysis Adequacy",
        "test_code": "KTVA",
        "category": "Dialysis Monitoring",
        "frequency": "Monthly",
        "parameters": [
            {"parameter": "Pre-Dialysis BUN", "unit": "mg/dL", "normal_range": ""},
            {"parameter": "Post-Dialysis BUN", "unit": "mg/dL", "normal_range": ""},
            {"parameter": "Kt/V", "unit": "", "normal_range": ">1.2"},
            {"parameter": "URR", "unit": "%", "normal_range": ">65"}
        ],
        "is_standard": 1
    },
    {
        "doctype": "Lab Test Template",
        "template_name": "Hepatitis Screening",
        "test_code": "HEP",
        "category": "Serology",
        "frequency": "Quarterly",
        "parameters": [
            {"parameter": "HBsAg", "unit": "", "normal_range": "Non-Reactive"},
            {"parameter": "Anti-HCV", "unit": "", "normal_range": "Non-Reactive"},
            {"parameter": "Anti-HBs", "unit": "mIU/mL", "normal_range": ">10"}
        ],
        "is_standard": 1
    }
]
```

### 4.3 Notification Templates

**File:** `dialysis_center/dialysis_center/fixtures/notification_template.json`

```json
[
    {
        "doctype": "Email Template",
        "name": "Appointment Confirmation",
        "subject": "Appointment Confirmed - {{ doc.appointment_date }}",
        "response": "<p>Dear {{ doc.patient_name }},</p>\n<p>Your dialysis appointment has been confirmed:</p>\n<ul>\n<li><strong>Date:</strong> {{ doc.appointment_date }}</li>\n<li><strong>Time:</strong> {{ doc.appointment_time }}</li>\n<li><strong>Machine:</strong> {{ doc.machine }}</li>\n<li><strong>Duration:</strong> {{ doc.duration }} minutes</li>\n</ul>\n<p>Please arrive 15 minutes before your scheduled time.</p>\n<p>If you need to reschedule, please contact us at least 24 hours in advance.</p>\n<p>Best regards,<br>Dialysis Center Team</p>",
        "module": "Dialysis Center"
    },
    {
        "doctype": "Email Template",
        "name": "Appointment Reminder",
        "subject": "Reminder: Dialysis Appointment Tomorrow",
        "response": "<p>Dear {{ doc.patient_name }},</p>\n<p>This is a reminder of your dialysis appointment:</p>\n<ul>\n<li><strong>Date:</strong> {{ doc.appointment_date }}</li>\n<li><strong>Time:</strong> {{ doc.appointment_time }}</li>\n<li><strong>Location:</strong> {{ doc.location }}</li>\n</ul>\n<p><strong>Important Reminders:</strong></p>\n<ul>\n<li>Take your morning medications as prescribed</li>\n<li>Bring your medication list</li>\n<li>Wear comfortable, loose-fitting clothing</li>\n<li>Avoid eating a large meal before treatment</li>\n</ul>\n<p>See you tomorrow!</p>",
        "module": "Dialysis Center"
    },
    {
        "doctype": "Email Template",
        "name": "Lab Results Available",
        "subject": "Your Lab Results Are Available",
        "response": "<p>Dear {{ doc.patient_name }},</p>\n<p>Your recent lab results from {{ doc.test_date }} are now available.</p>\n<p>Please log in to the patient portal to view your results, or contact your doctor for a detailed discussion.</p>\n<p>If you have any concerns, please don't hesitate to reach out to us.</p>\n<p>Best regards,<br>Dialysis Center Lab Team</p>",
        "module": "Dialysis Center"
    },
    {
        "doctype": "Email Template",
        "name": "Invoice Generated",
        "subject": "Invoice #{{ doc.name }} - Amount Due",
        "response": "<p>Dear {{ doc.patient_name }},</p>\n<p>An invoice has been generated for your recent dialysis sessions.</p>\n<ul>\n<li><strong>Invoice Number:</strong> {{ doc.name }}</li>\n<li><strong>Invoice Date:</strong> {{ doc.invoice_date }}</li>\n<li><strong>Total Amount:</strong> {{ doc.currency }} {{ doc.total_amount }}</li>\n<li><strong>Due Date:</strong> {{ doc.due_date }}</li>\n</ul>\n<p>You can view and download your invoice from the patient portal or visit our billing office.</p>\n<p>Payment options:</p>\n<ul>\n<li>Cash/Card at reception</li>\n<li>Bank transfer</li>\n<li>Insurance claim (if applicable)</li>\n</ul>\n<p>Thank you for your continued trust in our services.</p>",
        "module": "Dialysis Center"
    }
]
```

### 4.4 Print Format Fixtures

**File:** `dialysis_center/dialysis_center/fixtures/print_format.json`

```json
[
    {
        "doctype": "Print Format",
        "name": "Dialysis Session Report",
        "doc_type": "Dialysis Session",
        "module": "Dialysis Center",
        "standard": "Yes",
        "html": "<!-- Print format HTML will be here -->",
        "print_format_builder": 0,
        "print_format_type": "Server"
    },
    {
        "doctype": "Print Format",
        "name": "Patient Treatment Summary",
        "doc_type": "Patient",
        "module": "Dialysis Center",
        "standard": "Yes",
        "html": "<!-- Print format HTML will be here -->",
        "print_format_builder": 0,
        "print_format_type": "Server"
    },
    {
        "doctype": "Print Format",
        "name": "Invoice - Dialysis",
        "doc_type": "Invoice",
        "module": "Dialysis Center",
        "standard": "Yes",
        "html": "<!-- Print format HTML will be here -->",
        "print_format_builder": 0,
        "print_format_type": "Server"
    }
]
```

---

## 5. Test Data Factory Patterns

### 5.1 Patient Factory

**File:** `dialysis_center/tests/factories/patient_factory.py`

```python
import frappe
from frappe.utils import now_datetime, add_days, random_string
import random

class PatientFactory:
	"""Factory for creating test patient records"""
	
	@staticmethod
	def create(patient_id=None, **kwargs):
		"""Create a single patient with optional overrides"""
		
		if not patient_id:
			patient_id = f"PT-TEST-{random_string(5)}"
		
		patient_data = {
			"doctype": "Patient",
			"patient_id": patient_id,
			"first_name": kwargs.get("first_name", f"Test{random_string(3)}"),
			"last_name": kwargs.get("last_name", f"Patient{random_string(3)}"),
			"date_of_birth": kwargs.get("date_of_birth", "1970-01-01"),
			"gender": kwargs.get("gender", random.choice(["Male", "Female"])),
			"blood_group": kwargs.get("blood_group", random.choice(["A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"])),
			"national_id": kwargs.get("national_id", random_string(10)),
			"phone": kwargs.get("phone", f"+967{random.randint(500000000, 599999999)}"),
			"email": kwargs.get("email", f"test{random_string(5)}@example.com"),
			"address": kwargs.get("address", "Test Address"),
			"emergency_contact_name": kwargs.get("emergency_contact_name", "Emergency Contact"),
			"emergency_contact_phone": kwargs.get("emergency_contact_phone", "+967500000000"),
			"status": kwargs.get("status", "Active"),
			"diagnosis": kwargs.get("diagnosis", "Chronic Kidney Disease"),
			"dialysis_type": kwargs.get("dialysis_type", "Hemodialysis"),
			"vascular_access": kwargs.get("vascular_access", "AV Fistula"),
		}
		
		# Override with any additional kwargs
		patient_data.update(kwargs)
		
		patient = frappe.get_doc(patient_data)
		patient.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return patient
	
	@staticmethod
	def create_batch(count=10, **kwargs):
		"""Create multiple test patients"""
		patients = []
		for i in range(count):
			patient = PatientFactory.create(**kwargs)
			patients.append(patient)
		return patients
	
	@staticmethod
	def create_with_medical_history(patient_id=None):
		"""Create patient with complete medical history"""
		patient = PatientFactory.create(patient_id)
		
		# Add comorbidities
		patient.append("comorbidities", {
			"condition": "Diabetes Mellitus Type 2",
			"diagnosed_date": "2015-01-01",
			"status": "Active"
		})
		patient.append("comorbidities", {
			"condition": "Hypertension",
			"diagnosed_date": "2014-06-15",
			"status": "Active"
		})
		
		# Add allergies
		patient.append("allergies", {
			"allergen": "Penicillin",
			"reaction": "Rash",
			"severity": "Moderate"
		})
		
		# Add medications
		patient.append("medications", {
			"medication_name": "Lisinopril",
			"dosage": "10mg",
			"frequency": "Once daily",
			"start_date": "2015-03-01",
			"status": "Active"
		})
		
		patient.save(ignore_permissions=True)
		frappe.db.commit()
		
		return patient
```

### 5.2 Appointment Factory

**File:** `dialysis_center/tests/factories/appointment_factory.py`

```python
import frappe
from frappe.utils import now_datetime, add_days, add_hours
import random

class AppointmentFactory:
	"""Factory for creating test appointments"""
	
	@staticmethod
	def create(patient=None, machine=None, **kwargs):
		"""Create a single appointment"""
		
		if not patient:
			from dialysis_center.tests.factories.patient_factory import PatientFactory
			patient = PatientFactory.create()
		
		if not machine:
			machine = AppointmentFactory._get_or_create_machine()
		
		if not kwargs.get("staff"):
			kwargs["staff"] = AppointmentFactory._get_or_create_staff()
		
		appointment_date = kwargs.get("appointment_date", add_days(now_datetime(), random.randint(1, 30)))
		
		appointment_data = {
			"doctype": "Appointment",
			"patient": patient.name if hasattr(patient, 'name') else patient,
			"appointment_date": appointment_date,
			"appointment_time": kwargs.get("appointment_time", "09:00:00"),
			"duration": kwargs.get("duration", 240),  # 4 hours
			"machine": machine,
			"staff": kwargs.get("staff"),
			"shift": kwargs.get("shift", "Morning"),
			"status": kwargs.get("status", "Scheduled"),
			"notes": kwargs.get("notes", "Test appointment"),
		}
		
		appointment = frappe.get_doc(appointment_data)
		appointment.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return appointment
	
	@staticmethod
	def create_batch(count=10, patient=None, **kwargs):
		"""Create multiple appointments"""
		appointments = []
		for i in range(count):
			appointment = AppointmentFactory.create(patient=patient, **kwargs)
			appointments.append(appointment)
		return appointments
	
	@staticmethod
	def _get_or_create_machine():
		"""Get existing machine or create one"""
		machine = frappe.db.get_value("Dialysis Machine", {"status": "Available"}, "name")
		if machine:
			return machine
		
		# Create a test machine
		machine_doc = frappe.get_doc({
			"doctype": "Dialysis Machine",
			"machine_id": f"MCH-TEST-{random_string(3)}",
			"machine_name": f"Test Machine {random_string(3)}",
			"manufacturer": "Fresenius",
			"model": "5008S",
			"status": "Available",
			"location": "Main Floor"
		})
		machine_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return machine_doc.name
	
	@staticmethod
	def _get_or_create_staff():
		"""Get existing staff or create one"""
		staff = frappe.db.get_value("Healthcare Practitioner", {"practitioner_type": "Nurse"}, "name")
		if staff:
			return staff
		
		# Create a test staff member
		staff_doc = frappe.get_doc({
			"doctype": "Healthcare Practitioner",
			"first_name": "Test",
			"last_name": "Nurse",
			"practitioner_type": "Nurse",
			"gender": "Female"
		})
		staff_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return staff_doc.name
```

### 5.3 Dialysis Session Factory

**File:** `dialysis_center/tests/factories/session_factory.py`

```python
import frappe
from frappe.utils import now_datetime, add_to_date
import random

class SessionFactory:
	"""Factory for creating test dialysis sessions"""
	
	@staticmethod
	def create(patient=None, appointment=None, **kwargs):
		"""Create a dialysis session"""
		
		if not patient:
			from dialysis_center.tests.factories.patient_factory import PatientFactory
			patient = PatientFactory.create()
		
		if not appointment:
			from dialysis_center.tests.factories.appointment_factory import AppointmentFactory
			appointment = AppointmentFactory.create(patient=patient)
		
		session_data = {
			"doctype": "Dialysis Session",
			"patient": patient.name if hasattr(patient, 'name') else patient,
			"appointment": appointment.name if hasattr(appointment, 'name') else appointment,
			"session_date": kwargs.get("session_date", now_datetime()),
			"start_time": kwargs.get("start_time", "09:00:00"),
			"machine": kwargs.get("machine", appointment.machine if hasattr(appointment, 'machine') else None),
			"nurse": kwargs.get("nurse", appointment.staff if hasattr(appointment, 'staff') else None),
			"dialyzer_type": kwargs.get("dialyzer_type", "F60"),
			"blood_flow_rate": kwargs.get("blood_flow_rate", 300),
			"dialysate_flow_rate": kwargs.get("dialysate_flow_rate", 500),
			"ultrafiltration_goal": kwargs.get("ultrafiltration_goal", 2.5),
			"heparin_dose": kwargs.get("heparin_dose", 3000),
			"status": kwargs.get("status", "In Progress"),
		}
		
		session = frappe.get_doc(session_data)
		session.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return session
	
	@staticmethod
	def create_completed_session(patient=None, **kwargs):
		"""Create a completed session with vitals and events"""
		session = SessionFactory.create(patient=patient, status="Completed", **kwargs)
		
		# Add pre-dialysis vitals
		session.append("vital_signs", {
			"measurement_time": session.start_time,
			"measurement_type": "Pre-Dialysis",
			"systolic_bp": random.randint(130, 160),
			"diastolic_bp": random.randint(80, 100),
			"heart_rate": random.randint(70, 90),
			"temperature": round(random.uniform(36.5, 37.2), 1),
			"weight": round(random.uniform(65, 85), 1),
		})
		
		# Add post-dialysis vitals
		session.append("vital_signs", {
			"measurement_time": add_to_date(session.start_time, hours=4),
			"measurement_type": "Post-Dialysis",
			"systolic_bp": random.randint(110, 140),
			"diastolic_bp": random.randint(70, 90),
			"heart_rate": random.randint(65, 85),
			"temperature": round(random.uniform(36.3, 37.0), 1),
			"weight": round(random.uniform(63, 83), 1),
		})
		
		# Add session events
		session.append("session_events", {
			"event_time": add_to_date(session.start_time, hours=2),
			"event_type": "Clinical Note",
			"description": "Patient tolerated treatment well",
			"severity": "Info"
		})
		
		session.end_time = add_to_date(session.start_time, hours=4)
		session.actual_duration = 240
		session.save(ignore_permissions=True)
		frappe.db.commit()
		
		return session
```

## 6. Test Data Generation Scripts

### 6.1 Complete Dataset Generator

**File:** `dialysis_center/tests/generate_test_data.py`

```python
import frappe
from frappe.utils import now_datetime, add_days
import random
from dialysis_center.tests.factories.patient_factory import PatientFactory
from dialysis_center.tests.factories.appointment_factory import AppointmentFactory
from dialysis_center.tests.factories.session_factory import SessionFactory

def generate_complete_test_data():
	"""Generate a complete test dataset for the dialysis center"""
	
	frappe.set_user("Administrator")
	
	print("🔄 Generating test data...")
	
	# 1. Create master data
	print("📋 Creating master data...")
	create_machines()
	create_staff()
	create_inventory_items()
	
	# 2. Create patients
	print("👥 Creating test patients...")
	patients = PatientFactory.create_batch(50)
	print(f"✅ Created {len(patients)} patients")
	
	# 3. Create appointments (next 30 days)
	print("📅 Creating appointments...")
	appointments_created = 0
	for patient in patients[:30]:  # 30 patients get appointments
		appointments = AppointmentFactory.create_batch(
			count=3,  # 3 appointments each
			patient=patient,
			status="Scheduled"
		)
		appointments_created += len(appointments)
	print(f"✅ Created {appointments_created} appointments")
	
	# 4. Create historical sessions (last 90 days)
	print("🏥 Creating historical dialysis sessions...")
	sessions_created = 0
	for patient in patients:
		# Create 20-30 historical sessions per patient
		for i in range(20, 31):
			session_date = add_days(now_datetime(), -i)
			session = SessionFactory.create_completed_session(
				patient=patient,
				session_date=session_date
			)
			sessions_created += 1
	print(f"✅ Created {sessions_created} historical sessions")
	
	# 5. Create lab results
	print("🧪 Creating lab results...")
	create_lab_results(patients)
	
	# 6. Create invoices
	print("💰 Creating invoices...")
	create_invoices(patients)
	
	print("\n✨ Test data generation complete!")
	print_summary()

def create_machines():
	"""Create test dialysis machines"""
	machines = [
		{"machine_id": "MCH-001", "machine_name": "Machine A1", "manufacturer": "Fresenius", "model": "5008S", "location": "Main Floor"},
		{"machine_id": "MCH-002", "machine_name": "Machine A2", "manufacturer": "Fresenius", "model": "5008S", "location": "Main Floor"},
		{"machine_id": "MCH-003", "machine_name": "Machine B1", "manufacturer": "Gambro", "model": "AK200", "location": "Second Floor"},
		{"machine_id": "MCH-004", "machine_name": "Machine B2", "manufacturer": "Gambro", "model": "AK200", "location": "Second Floor"},
		{"machine_id": "MCH-005", "machine_name": "Machine C1", "manufacturer": "Baxter", "model": "Phoenix", "location": "Third Floor"},
	]
	
	for machine_data in machines:
		if not frappe.db.exists("Dialysis Machine", {"machine_id": machine_data["machine_id"]}):
			machine = frappe.get_doc({
				"doctype": "Dialysis Machine",
				**machine_data,
				"status": "Available",
				"installation_date": "2020-01-01"
			})
			machine.insert(ignore_permissions=True)
	
	frappe.db.commit()

def create_staff():
	"""Create test staff members"""
	staff_members = [
		{"first_name": "Dr. Ahmed", "last_name": "Hassan", "practitioner_type": "Nephrologist"},
		{"first_name": "Dr. Sarah", "last_name": "Ali", "practitioner_type": "Nephrologist"},
		{"first_name": "Nurse Fatima", "last_name": "Mohammed", "practitioner_type": "Nurse"},
		{"first_name": "Nurse Aisha", "last_name": "Abdullah", "practitioner_type": "Nurse"},
		{"first_name": "Tech Omar", "last_name": "Ibrahim", "practitioner_type": "Technician"},
	]
	
	for staff_data in staff_members:
		if not frappe.db.exists("Healthcare Practitioner", {"first_name": staff_data["first_name"]}):
			staff = frappe.get_doc({
				"doctype": "Healthcare Practitioner",
				**staff_data,
				"gender": "Male" if "Dr. Ahmed" in staff_data["first_name"] or "Omar" in staff_data["first_name"] else "Female"
			})
			staff.insert(ignore_permissions=True)
	
	frappe.db.commit()

def create_inventory_items():
	"""Create test inventory items"""
	items = [
		{"item_code": "DIAL-F60", "item_name": "Dialyzer F60", "category": "Dialyzer", "unit": "Piece"},
		{"item_code": "DIAL-F80", "item_name": "Dialyzer F80", "category": "Dialyzer", "unit": "Piece"},
		{"item_code": "BLOODSET-STD", "item_name": "Standard Blood Line Set", "category": "Consumable", "unit": "Set"},
		{"item_code": "HEPARIN-5ML", "item_name": "Heparin 5ml", "category": "Medication", "unit": "Vial"},
		{"item_code": "SALINE-500ML", "item_name": "Normal Saline 500ml", "category": "Medication", "unit": "Bag"},
	]
	
	for item_data in items:
		if not frappe.db.exists("Inventory Item", {"item_code": item_data["item_code"]}):
			item = frappe.get_doc({
				"doctype": "Inventory Item",
				**item_data,
				"reorder_level": 50,
				"reorder_quantity": 100,
				"current_stock": 200
			})
			item.insert(ignore_permissions=True)
	
	frappe.db.commit()

def create_lab_results(patients):
	"""Create lab results for patients"""
	for patient in patients[:20]:  # Create lab results for 20 patients
		lab_result = frappe.get_doc({
			"doctype": "Lab Result",
			"patient": patient.name,
			"test_date": add_days(now_datetime(), -7),
			"hemoglobin": round(random.uniform(9.0, 12.0), 1),
			"hematocrit": round(random.uniform(27, 36), 1),
			"creatinine": round(random.uniform(5.0, 10.0), 1),
			"urea": round(random.uniform(100, 180), 1),
			"potassium": round(random.uniform(4.0, 6.0), 1),
			"sodium": round(random.uniform(135, 145), 1),
			"calcium": round(random.uniform(8.0, 10.0), 1),
			"phosphorus": round(random.uniform(3.5, 6.5), 1),
		})
		lab_result.insert(ignore_permissions=True)
	
	frappe.db.commit()

def create_invoices(patients):
	"""Create invoices for completed sessions"""
	for patient in patients[:15]:  # Create invoices for 15 patients
		invoice = frappe.get_doc({
			"doctype": "Invoice",
			"patient": patient.name,
			"invoice_date": add_days(now_datetime(), -5),
			"total_amount": 1500.00,
			"status": "Paid",
			"payment_method": "Insurance"
		})
		invoice.insert(ignore_permissions=True)
	
	frappe.db.commit()

def print_summary():
	"""Print summary of generated data"""
	print("\n" + "="*50)
	print("📊 TEST DATA SUMMARY")
	print("="*50)
	print(f"Patients: {frappe.db.count('Patient')}")
	print(f"Appointments: {frappe.db.count('Appointment')}")
	print(f"Dialysis Sessions: {frappe.db.count('Dialysis Session')}")
	print(f"Dialysis Machines: {frappe.db.count('Dialysis Machine')}")
	print(f"Healthcare Practitioners: {frappe.db.count('Healthcare Practitioner')}")
	print(f"Lab Results: {frappe.db.count('Lab Result')}")
	print(f"Invoices: {frappe.db.count('Invoice')}")
	print("="*50)
```

### 6.2 Clear Test Data Script

**File:** `dialysis_center/tests/clear_test_data.py`

```python
import frappe

def clear_test_data():
	"""Clear all test data"""
	frappe.set_user("Administrator")
	
	print("🗑️  Clearing test data...")
	
	# Delete in reverse dependency order
	doctypes = [
		"Invoice",
		"Lab Result",
		"Dialysis Session",
		"Appointment",
		"Patient",
		"Healthcare Practitioner",
		"Dialysis Machine",
		"Inventory Item"
	]
	
	for doctype in doctypes:
		count = frappe.db.count(doctype)
		frappe.db.sql(f"DELETE FROM `tab{doctype}`")
		print(f"✅ Deleted {count} {doctype} records")
	
	frappe.db.commit()
	print("✨ Test data cleared!")
```

## 7. Running Fixtures and Test Data

### 7.1 Install Fixtures

```bash
# Install app with fixtures
bench --site [sitename] install-app dialysis_center

# Reinstall app (includes fixtures)
bench --site [sitename] reinstall

# Import specific fixture
bench --site [sitename] import-doc path/to/fixture.json

# Export fixtures
bench --site [sitename] export-fixtures
```

### 7.2 Generate Test Data

```bash
# From bench console
bench --site [sitename] console

# Then in Python console:
>>> from dialysis_center.tests.generate_test_data import generate_complete_test_data
>>> generate_complete_test_data()
```

### 7.3 Clear Test Data

```bash
# From bench console
bench --site [sitename] console

# Then in Python console:
>>> from dialysis_center.tests.clear_test_data import clear_test_data
>>> clear_test_data()
```

## 8. Integration with Tests

### 8.1 Using Factories in Unit Tests

```python
# test_patient.py
import frappe
from frappe.tests import IntegrationTestCase
from dialysis_center.tests.factories.patient_factory import PatientFactory

class TestPatient(IntegrationTestCase):
	def setUp(self):
		"""Setup test data before each test"""
		self.patient = PatientFactory.create()
	
	def tearDown(self):
		"""Cleanup after each test"""
		frappe.delete_doc("Patient", self.patient.name, force=True)
	
	def test_patient_creation(self):
		"""Test patient can be created"""
		self.assertEqual(self.patient.status, "Active")
		self.assertIsNotNone(self.patient.patient_id)
	
	def test_patient_with_medical_history(self):
		"""Test patient with medical history"""
		patient = PatientFactory.create_with_medical_history()
		self.assertTrue(len(patient.comorbidities) > 0)
		self.assertTrue(len(patient.medications) > 0)
		frappe.delete_doc("Patient", patient.name, force=True)
```

### 8.2 Fixture-Based Testing

```python
# test_appointment.py
import frappe
from frappe.tests import IntegrationTestCase
from dialysis_center.tests.factories.appointment_factory import AppointmentFactory
from dialysis_center.tests.factories.patient_factory import PatientFactory

class TestAppointment(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup once for all tests in this class"""
		cls.patient = PatientFactory.create()
	
	@classmethod
	def tearDownClass(cls):
		"""Cleanup once after all tests"""
		frappe.delete_doc("Patient", cls.patient.name, force=True)
	
	def test_create_appointment(self):
		"""Test appointment creation"""
		appointment = AppointmentFactory.create(patient=self.patient)
		self.assertEqual(appointment.status, "Scheduled")
		self.assertEqual(appointment.patient, self.patient.name)
		frappe.delete_doc("Appointment", appointment.name, force=True)
	
	def test_batch_appointments(self):
		"""Test creating multiple appointments"""
		appointments = AppointmentFactory.create_batch(5, patient=self.patient)
		self.assertEqual(len(appointments), 5)
		
		# Cleanup
		for apt in appointments:
			frappe.delete_doc("Appointment", apt.name, force=True)
```

## 9. Best Practices

### 9.1 Fixture Design

✅ **Do:**
- Keep fixtures minimal and focused
- Use real-world representative data
- Version control fixtures in Git
- Document fixture purpose in comments
- Use ISO date formats (YYYY-MM-DD)
- Include only essential master data
- Test fixtures in clean environment

❌ **Don't:**
- Include sensitive or production data
- Create overly complex fixture dependencies
- Hard-code site-specific values
- Include temporary test data
- Use production IDs or names
- Skip validation during fixture creation

### 9.2 Factory Pattern

✅ **Do:**
- Provide sensible defaults
- Allow overrides for customization
- Handle dependencies automatically
- Clean up after tests
- Use randomization for uniqueness
- Document factory methods
- Include batch creation methods

❌ **Don't:**
- Create tightly coupled factories
- Ignore database constraints
- Leave orphaned test records
- Use production data in factories
- Hard-code timestamps
- Skip permission checks

### 9.3 Test Data Management

✅ **Do:**
- Generate fresh data per test run
- Use transactions for isolation
- Cleanup after tests
- Seed random generators for reproducibility
- Document data generation process
- Separate test data from fixtures
- Use descriptive names for test records

❌ **Don't:**
- Rely on specific data order
- Share state between tests
- Accumulate test data over time
- Use production databases for testing
- Mix test data with real data
- Skip cleanup in tearDown methods

### 9.4 Performance Considerations

✅ **Do:**
- Use bulk insert operations
- Commit in batches
- Index frequently queried fields
- Use `ignore_permissions=True` for test data
- Profile data generation scripts
- Monitor database size during generation

❌ **Don't:**
- Create unnecessary relationships
- Generate excessive data volumes
- Run migrations during test data creation
- Use slow queries in loops

## 10. Summary

### 10.1 What's Included

This document provides:
- ✅ **Core System Fixtures** - Roles, workflows, custom fields, settings
- ✅ **Master Data Fixtures** - Treatment templates, lab tests, notifications
- ✅ **Factory Classes** - Patient, Appointment, Session factories
- ✅ **Generation Scripts** - Complete dataset generation with 1000+ records
- ✅ **Test Integration** - Examples of using fixtures in unit tests
- ✅ **Best Practices** - Comprehensive guidelines for fixture management

### 10.2 Quick Reference Commands

```bash
# Install with fixtures
bench --site [sitename] install-app dialysis_center

# Export fixtures after modifications
bench --site [sitename] export-fixtures

# Generate test data
bench --site [sitename] console
>>> from dialysis_center.tests.generate_test_data import generate_complete_test_data
>>> generate_complete_test_data()

# Clear test data
>>> from dialysis_center.tests.clear_test_data import clear_test_data
>>> clear_test_data()

# Run tests with fixtures
bench --site [sitename] run-tests --app dialysis_center

# Reinstall app (reloads fixtures)
bench --site [sitename] reinstall
```

### 10.3 Fixture Checklist

Before deploying to production, ensure:
- [ ] All fixtures are version controlled
- [ ] Fixtures pass validation
- [ ] No sensitive data in fixtures
- [ ] Workflows are properly configured
- [ ] Roles and permissions are set correctly
- [ ] Email templates are tested
- [ ] Print formats render correctly
- [ ] Custom fields don't conflict with standard fields
- [ ] Test data is separated from fixtures
- [ ] Documentation is up-to-date

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-19  
**Framework:** Frappe v15.100.1  
**Status:** Complete

