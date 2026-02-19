# Dialysis Center Management System - Technical Design Document

## Document Information

**Project Name:** Dialysis Center Management System (DCMS)  
**Platform:** Frappe Framework v15+  
**Document Version:** 1.0  
**Date:** February 19, 2026  
**Status:** Draft

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [DocType Design](#2-doctype-design)
3. [Database Schema](#3-database-schema)
4. [Data Relationships](#4-data-relationships)
5. [API Design](#5-api-design)
6. [Integration Points](#6-integration-points)
7. [Security Design](#7-security-design)
8. [Performance Considerations](#8-performance-considerations)

---

## 1. Architecture Overview

### 1.1 Application Structure

```
dcms/                                   # Frappe App Root
├── dcms/                              # Python Module
│   ├── __init__.py
│   ├── hooks.py                       # App configuration and hooks
│   ├── modules.txt                    # Module list
│   ├── patches.txt                    # Database migration patches
│   │
│   ├── patient_management/            # Module: Patient Management
│   │   ├── doctype/
│   │   │   ├── patient/
│   │   │   ├── patient_medical_history/
│   │   │   ├── patient_document/
│   │   │   └── patient_consent/
│   │   └── page/
│   │
│   ├── appointment_scheduling/        # Module: Appointment & Scheduling
│   │   ├── doctype/
│   │   │   ├── appointment/
│   │   │   ├── shift/
│   │   │   ├── shift_assignment/
│   │   │   └── recurring_appointment/
│   │   └── page/
│   │
│   ├── clinical_operations/           # Module: Clinical Operations
│   │   ├── doctype/
│   │   │   ├── dialysis_session/
│   │   │   ├── treatment_prescription/
│   │   │   ├── vital_signs_log/
│   │   │   ├── session_event/
│   │   │   └── treatment_template/
│   │   └── page/
│   │
│   ├── laboratory/                    # Module: Laboratory
│   │   ├── doctype/
│   │   │   ├── lab_test_order/
│   │   │   ├── lab_test_result/
│   │   │   ├── lab_test_template/
│   │   │   └── lab_parameter/
│   │   └── page/
│   │
│   ├── inventory/                     # Module: Inventory Management
│   │   ├── doctype/
│   │   │   ├── inventory_item/
│   │   │   ├── stock_receipt/
│   │   │   ├── stock_issuance/
│   │   │   ├── stock_movement/
│   │   │   └── supplier/
│   │   └── page/
│   │
│   ├── equipment/                     # Module: Equipment Management
│   │   ├── doctype/
│   │   │   ├── dialysis_machine/
│   │   │   ├── machine_maintenance/
│   │   │   └── water_quality_log/
│   │   └── page/
│   │
│   ├── billing/                       # Module: Billing & Finance
│   │   ├── doctype/
│   │   │   ├── patient_bill/
│   │   │   ├── payment_entry/
│   │   │   ├── insurance_claim/
│   │   │   └── price_list/
│   │   └── page/
│   │
│   ├── staff/                         # Module: Staff Management
│   │   ├── doctype/
│   │   │   ├── staff_member/
│   │   │   ├── staff_attendance/
│   │   │   └── credential_tracking/
│   │   └── page/
│   │
│   ├── reporting/                     # Module: Reporting
│   │   ├── report/
│   │   │   ├── daily_census/
│   │   │   ├── monthly_clinical_quality/
│   │   │   └── financial_summary/
│   │   └── dashboard/
│   │
│   ├── public/                        # Static Assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── templates/                     # Jinja Templates
│       ├── pages/
│       └── includes/
│
├── package.json                       # Node.js dependencies
├── requirements.txt                   # Python dependencies
└── README.md                          # App documentation
```

### 1.2 Technology Stack

**Backend:**
- Python 3.10+
- Frappe Framework 15+
- MariaDB 10.11+
- Redis 7.0+

**Frontend:**
- Vue.js 3
- Frappe UI Components
- esbuild

**Integrations:**
- SMS Gateway (Twilio/custom)
- Email Service (SMTP)
- Payment Gateway (Stripe/PayPal)
- HL7/FHIR for LIS integration

---

## 2. DocType Design

### 2.1 Module: Patient Management

#### DocType: Patient

**Purpose:** Core patient demographic and medical information

**Type:** Master DocType  
**Naming:** `PT-{YYYY}-{#####}` (e.g., PT-2026-00001)  
**Permissions:** Read: All Healthcare Roles, Write: Receptionist, Nurse, Doctor

**Fields:**

| Field Name | Field Type | Options | Mandatory | Description |
|------------|------------|---------|-----------|-------------|
| patient_id | Data | - | Yes | Auto-generated unique ID |
| first_name | Data | - | Yes | Patient's first name |
| middle_name | Data | - | No | Patient's middle name |
| last_name | Data | - | Yes | Patient's last name |
| full_name | Data | Read Only | Yes | Auto-computed full name |
| date_of_birth | Date | - | Yes | Date of birth |
| age | Int | Read Only | No | Auto-calculated from DOB |
| gender | Select | Male, Female, Other | Yes | Gender |
| blood_group | Select | A+, A-, B+, B-, AB+, AB-, O+, O- | No | Blood group |
| marital_status | Select | Single, Married, Divorced, Widowed | No | Marital status |
| national_id | Data | - | No | National ID number (unique) |
| phone | Data | - | Yes | Primary phone number |
| mobile | Data | - | No | Mobile number |
| email | Data | - | No | Email address |
| emergency_contact_name | Data | - | Yes | Emergency contact name |
| emergency_contact_phone | Data | - | Yes | Emergency contact phone |
| address_line_1 | Data | - | No | Address line 1 |
| address_line_2 | Data | - | No | Address line 2 |
| city | Data | - | No | City |
| state | Data | - | No | State/Province |
| postal_code | Data | - | No | Postal/ZIP code |
| country | Link | Country | No | Country |
| photo | Attach Image | - | No | Patient photo |
| insurance_provider | Link | Insurance Company | No | Insurance company |
| insurance_id | Data | - | No | Insurance policy number |
| insurance_expiry | Date | - | No | Insurance expiry date |
| ckd_stage | Select | Stage 1, Stage 2, Stage 3, Stage 4, Stage 5 | No | CKD stage |
| patient_status | Select | Active, Inactive, Deceased, Transferred | Yes | Patient status |
| status_reason | Small Text | - | No | Reason for status change |
| vip_patient | Check | - | No | VIP flag |
| vip_reason | Small Text | - | No | Reason for VIP status |
| referring_physician | Data | - | No | Referring physician name |
| registration_date | Date | - | Yes | Registration date |
| qr_code | Attach Image | Read Only | No | Auto-generated QR code |

**Child Tables:**
- Allergies (allergies)
- Chronic Conditions (chronic_conditions)
- Previous Surgeries (previous_surgeries)
- Family Medical History (family_history)
- Current Medications (current_medications)

**Controller Methods:**
```python
def autoname(self):
    # Auto-generate patient ID: PT-YYYY-#####
    
def validate(self):
    # Calculate age from DOB
    # Validate phone and email format
    # Check for duplicate national_id
    # Auto-generate full_name
    
def on_update(self):
    # Generate QR code if not exists
    # Update related appointments if status changed to Inactive
    
def get_medical_summary(self):
    # Return comprehensive medical summary
```

---

#### DocType: Patient Medical History (Child Table)

**Purpose:** Track medical conditions and history

**Fields:**

| Field Name | Field Type | Options | Mandatory |
|------------|------------|---------|-----------|
| condition_type | Select | Chronic Condition, Allergy, Surgery, Family History | Yes |
| condition_name | Data | - | Yes |
| severity | Select | Mild, Moderate, Severe | No |
| diagnosed_date | Date | - | No |
| notes | Text | - | No |
| is_active | Check | - | Yes |

---

#### DocType: Patient Document

**Purpose:** Store and manage patient documents

**Type:** Document  
**Naming:** `PD-{patient_id}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory | Description |
|------------|------------|-----------|-------------|
| patient | Link | Yes | Link to Patient |
| document_title | Data | Yes | Document title |
| document_category | Select | Yes | Lab Report, Imaging, Consent Form, Insurance, Other |
| document_file | Attach | Yes | Uploaded file |
| document_date | Date | Yes | Document date |
| description | Small Text | No | Description |
| uploaded_by | Link | Yes | User who uploaded |
| upload_date | Datetime | Yes | Upload timestamp |
| expiry_date | Date | No | Document expiry date |
| is_expired | Check | No | Auto-calculated |
| version | Int | Yes | Version number |

---

#### DocType: Patient Consent

**Purpose:** Track patient consent forms

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| patient | Link | Yes |
| consent_type | Select | Yes |
| consent_date | Date | Yes |
| consent_given_by | Data | Yes |
| witness_name | Data | No |
| signature | Signature | Yes |
| consent_document | Attach | No |
| valid_until | Date | No |
| status | Select | Yes |

---

### 2.2 Module: Appointment & Scheduling

#### DocType: Appointment

**Purpose:** Schedule and manage dialysis appointments

**Type:** Document  
**Naming:** `APT-{YYYY}-{#####}`  
**Permissions:** Read: All, Write: Receptionist, Nurse

**Fields:**

| Field Name | Field Type | Options | Mandatory | Description |
|------------|------------|---------|-----------|-------------|
| appointment_id | Data | Auto | Yes | Auto-generated ID |
| patient | Link | Patient | Yes | Patient link |
| patient_name | Data | Read Only | Yes | Fetched from Patient |
| appointment_date | Date | - | Yes | Appointment date |
| appointment_time | Time | - | Yes | Start time |
| shift | Link | Shift | Yes | Shift assignment |
| duration | Duration | Default: 04:00:00 | Yes | Session duration |
| end_time | Time | Read Only | Yes | Auto-calculated |
| dialysis_machine | Link | Dialysis Machine | Yes | Assigned machine |
| assigned_nurse | Link | Staff Member | Yes | Assigned nurse |
| assigned_technician | Link | Staff Member | No | Assigned technician |
| appointment_type | Select | Regular, Emergency, Walk-in | Yes | Type |
| recurrence_id | Link | Recurring Appointment | No | Link to recurrence |
| special_instructions | Text | - | No | Special notes |
| status | Select | Scheduled, Checked In, In Progress, Completed, Cancelled, No Show | Yes | Status |
| check_in_time | Datetime | - | No | Check-in timestamp |
| checked_in_by | Link | User | No | User who checked in |
| cancellation_reason | Small Text | - | No | Reason for cancellation |
| cancelled_by | Link | User | No | User who cancelled |
| cancellation_date | Datetime | - | No | Cancellation timestamp |
| rescheduled_from | Link | Appointment | No | Original appointment if rescheduled |
| location | Link | Location | Yes | Center location |

**Controller Methods:**
```python
def validate(self):
    # Check machine availability
    # Check staff availability
    # Validate patient is active
    # Calculate end_time
    # Check for double booking
    
def on_submit(self):
    # Update machine status
    # Send appointment reminder (if configured)
    
def on_cancel(self):
    # Free up machine slot
    # Update status to Cancelled
    
def check_in_patient(self):
    # Mark patient as checked in
    # Notify assigned nurse
```

---

#### DocType: Recurring Appointment

**Purpose:** Manage recurring appointment patterns

**Type:** Document  
**Naming:** `REC-{YYYY}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory | Description |
|------------|------------|-----------|-------------|
| patient | Link | Yes | Patient link |
| start_date | Date | Yes | Recurrence start date |
| end_date | Date | Yes | Recurrence end date |
| recurrence_pattern | Select | Yes | Mon-Wed-Fri, Tue-Thu-Sat, Daily, Custom |
| custom_days | Table | No | Custom day selection |
| preferred_time | Time | Yes | Preferred time slot |
| preferred_shift | Link | Yes | Preferred shift |
| preferred_machine | Link | No | Preferred machine |
| assigned_nurse | Link | Yes | Default nurse |
| duration | Duration | Yes | Default duration |
| is_active | Check | Yes | Active status |
| created_appointments | Int | No | Count of created appointments |

**Controller Methods:**
```python
def on_submit(self):
    # Generate appointments based on pattern
    # Create individual Appointment documents
    
def stop_recurrence(self):
    # Mark as inactive
    # Don't create future appointments
```

---

#### DocType: Shift

**Purpose:** Define operational shifts

**Type:** Master  
**Naming:** Field based naming

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| shift_name | Data | Yes |
| shift_type | Select | Yes |
| start_time | Time | Yes |
| end_time | Time | Yes |
| location | Link | Yes |
| max_capacity | Int | Yes |
| buffer_time | Duration | No |
| is_active | Check | Yes |

---

#### DocType: Shift Assignment

**Purpose:** Assign staff to shifts

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| shift | Link | Yes |
| staff_member | Link | Yes |
| assignment_date | Date | Yes |
| role_in_shift | Select | Yes |
| notes | Small Text | No |

---

### 2.3 Module: Clinical Operations

#### DocType: Dialysis Session

**Purpose:** Record complete dialysis treatment session

**Type:** Document (Submittable)  
**Naming:** `DS-{YYYY}-{#####}`  
**Permissions:** Read: All Healthcare, Write: Nurse, Doctor

**Fields:**

| Field Name | Field Type | Options | Mandatory | Description |
|------------|------------|---------|-----------|-------------|
| session_id | Data | Auto | Yes | Auto-generated ID |
| appointment | Link | Appointment | No | Linked appointment |
| patient | Link | Patient | Yes | Patient link |
| patient_name | Data | Read Only | Yes | Patient name |
| session_date | Date | - | Yes | Session date |
| dialysis_machine | Link | Dialysis Machine | Yes | Machine used |
| assigned_nurse | Link | Staff Member | Yes | Primary nurse |
| assigned_doctor | Link | Staff Member | No | Supervising doctor |

**Section: Pre-Dialysis Assessment**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| pre_dialysis_weight | Float | Yes |
| pre_dialysis_bp_systolic | Int | Yes |
| pre_dialysis_bp_diastolic | Int | Yes |
| pre_dialysis_hr | Int | Yes |
| pre_dialysis_temp | Float | Yes |
| sitting_bp_systolic | Int | No |
| sitting_bp_diastolic | Int | No |
| standing_bp_systolic | Int | No |
| standing_bp_diastolic | Int | No |
| access_site_type | Select | Yes |
| access_site_condition | Select | Yes |
| patient_complaints | Text | No |
| last_meal_time | Datetime | No |

**Section: Treatment Prescription**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| treatment_template | Link | No |
| dialysis_modality | Select | Yes |
| prescribed_duration | Duration | Yes |
| blood_flow_rate | Int | Yes |
| dialysate_flow_rate | Int | Yes |
| uf_goal | Float | Yes |
| dialyzer_type | Link | Yes |
| dialyzer_size | Data | No |
| anticoagulation_protocol | Select | Yes |
| heparin_loading_dose | Float | No |
| heparin_maintenance_dose | Float | No |
| special_instructions | Text | No |

**Section: Session Progress**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| session_start_time | Datetime | Yes |
| session_end_time | Datetime | No |
| actual_duration | Duration | No |
| session_status | Select | Yes |
| vital_signs_log | Table | No |
| session_events | Table | No |
| stock_issuance | Link | No |

**Section: Post-Dialysis Assessment**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| post_dialysis_weight | Float | Yes |
| post_dialysis_bp_systolic | Int | Yes |
| post_dialysis_bp_diastolic | Int | Yes |
| post_dialysis_hr | Int | Yes |
| post_dialysis_temp | Float | Yes |
| actual_uf_removed | Float | Yes |
| access_site_post_condition | Select | Yes |
| patient_condition_at_discharge | Select | Yes |
| complications | Text | No |
| adverse_events | Text | No |
| next_appointment | Link | No |

**Section: Clinical Calculations**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| weight_gain | Float | No |
| uf_rate | Float | No |
| kt_v | Float | No |
| urr | Float | No |

**Controller Methods:**
```python
def validate(self):
    # Validate vital signs ranges
    # Calculate weight_gain, uf_rate
    # Ensure session doesn't overlap
    
def on_submit(self):
    # Mark appointment as completed
    # Trigger billing
    # Update patient last session date
    # Calculate Kt/V if lab values available
    
def complete_session(self):
    # Set end_time
    # Calculate actual_duration
    # Validate all required fields
    # Submit document
```

---

#### DocType: Vital Signs Log (Child Table)

**Purpose:** Record vitals during dialysis

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| recording_time | Datetime | Yes |
| bp_systolic | Int | Yes |
| bp_diastolic | Int | Yes |
| heart_rate | Int | Yes |
| temperature | Float | No |
| blood_flow_rate | Int | Yes |
| dialysate_flow_rate | Int | Yes |
| tmp | Int | No |
| venous_pressure | Int | No |
| uf_removed_so_far | Float | Yes |
| recorded_by | Link | Yes |
| notes | Text | No |

---

#### DocType: Session Event (Child Table)

**Purpose:** Log events/incidents during session

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| event_time | Datetime | Yes |
| event_type | Select | Yes |
| event_description | Text | Yes |
| action_taken | Text | Yes |
| recorded_by | Link | Yes |
| severity | Select | No |

---

#### DocType: Treatment Template

**Purpose:** Reusable treatment prescriptions

**Type:** Master  
**Naming:** Field based

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| template_name | Data | Yes |
| patient | Link | No |
| dialysis_modality | Select | Yes |
| duration | Duration | Yes |
| blood_flow_rate | Int | Yes |
| dialysate_flow_rate | Int | Yes |
| uf_goal | Float | Yes |
| dialyzer_type | Link | Yes |
| anticoagulation_protocol | Select | Yes |
| heparin_loading_dose | Float | No |
| heparin_maintenance_dose | Float | No |
| is_standard | Check | Yes |
| approved_by | Link | No |
| approval_date | Date | No |

---

### 2.4 Module: Laboratory

#### DocType: Lab Test Order

**Purpose:** Order laboratory tests

**Type:** Document (Submittable)  
**Naming:** `LTO-{YYYY}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory | Description |
|------------|------------|-----------|-------------|
| patient | Link | Yes | Patient link |
| order_date | Date | Yes | Order date |
| ordered_by | Link | Yes | Ordering physician |
| priority | Select | Yes | Routine, Urgent, STAT |
| clinical_notes | Text | No | Clinical indication |
| test_items | Table | Yes | Ordered tests |
| status | Select | Yes | Ordered, Sample Collected, Sent to Lab, Completed |
| sample_collection_date | Datetime | No | Collection timestamp |
| collected_by | Link | No | Staff who collected |
| external_lab | Link | No | External laboratory |
| requisition_number | Data | No | External lab requisition |

**Child Table: Test Items**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| lab_test_template | Link | Yes |
| test_name | Data | Yes |
| test_code | Data | No |

**Controller Methods:**
```python
def on_submit(self):
    # Generate barcode for sample
    # Print requisition
    # Send to LIS if integrated
```

---

#### DocType: Lab Test Result

**Purpose:** Record lab test results

**Type:** Document  
**Naming:** `LTR-{YYYY}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| lab_test_order | Link | Yes |
| patient | Link | Yes |
| test_template | Link | Yes |
| result_date | Datetime | Yes |
| result_parameters | Table | Yes |
| interpretation | Text | No |
| entered_by | Link | Yes |
| verified_by | Link | No |
| verification_date | Datetime | No |
| critical_flag | Check | No |

**Child Table: Result Parameters**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| parameter_name | Data | Yes |
| result_value | Data | Yes |
| unit | Data | Yes |
| reference_range | Data | No |
| is_abnormal | Check | No |
| abnormal_flag | Select | No |

---

#### DocType: Lab Test Template

**Purpose:** Define lab test parameters

**Type:** Master

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| test_name | Data | Yes |
| test_code | Data | Yes |
| test_category | Select | Yes |
| sample_type | Select | Yes |
| parameters | Table | Yes |
| turnaround_time | Duration | No |
| is_panel | Check | No |

---

### 2.5 Module: Inventory Management

#### DocType: Inventory Item

**Purpose:** Master data for inventory items

**Type:** Master  
**Naming:** `ITEM-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory | Description |
|------------|------------|-----------|-------------|
| item_code | Data | Yes | Unique item code |
| item_name | Data | Yes | Item name |
| item_category | Select | Yes | Dialyzer, Medication, Consumable, Equipment |
| description | Text | No | Detailed description |
| unit_of_measure | Link | Yes | UOM (pcs, box, liter, etc.) |
| reorder_level | Float | Yes | Minimum stock level |
| max_stock_level | Float | No | Maximum stock level |
| default_supplier | Link | No | Preferred supplier |
| standard_rate | Currency | No | Standard price |
| is_active | Check | Yes | Active status |
| has_batch_no | Check | No | Batch tracking required |
| has_expiry_date | Check | No | Expiry tracking required |
| image | Attach Image | No | Item image |

---

#### DocType: Stock Receipt

**Purpose:** Record goods received

**Type:** Document (Submittable)  
**Naming:** `SR-{YYYY}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| receipt_date | Date | Yes |
| supplier | Link | Yes |
| purchase_order | Link | No |
| delivery_note_no | Data | No |
| delivery_note | Attach | No |
| items | Table | Yes |
| total_amount | Currency | No |
| received_by | Link | Yes |
| location | Link | Yes |

**Child Table: Items**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| item | Link | Yes |
| quantity | Float | Yes |
| batch_no | Data | No |
| expiry_date | Date | No |
| unit_rate | Currency | No |
| amount | Currency | No |

---

#### DocType: Stock Issuance

**Purpose:** Issue stock for sessions

**Type:** Document (Submittable)  
**Naming:** `SI-{YYYY}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| issuance_date | Date | Yes |
| dialysis_session | Link | No |
| patient | Link | Yes |
| issued_by | Link | Yes |
| items | Table | Yes |

**Child Table: Items**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| item | Link | Yes |
| quantity | Float | Yes |
| batch_no | Data | No |
| unit_rate | Currency | No |
| amount | Currency | No |

---

### 2.6 Module: Equipment Management

#### DocType: Dialysis Machine

**Purpose:** Register and track dialysis machines

**Type:** Master  
**Naming:** Field based

**Fields:**

| Field Name | Field Type | Mandatory | Description |
|------------|------------|-----------|-------------|
| machine_id | Data | Yes | Unique machine ID |
| serial_number | Data | Yes | Manufacturer serial |
| manufacturer | Data | Yes | Manufacturer name |
| model | Data | Yes | Model name |
| machine_type | Select | Yes | HD, HDF, etc. |
| installation_date | Date | Yes | Installation date |
| warranty_expiry | Date | No | Warranty expiry |
| location | Link | Yes | Center location |
| station_number | Data | Yes | Station/bed number |
| status | Select | Yes | Operational, Maintenance, Out of Service |
| specifications | Text | No | Technical specs |
| manual | Attach | No | User manual |
| last_maintenance_date | Date | No | Last maintenance |
| next_maintenance_date | Date | No | Next scheduled |
| total_hours_used | Float | No | Total usage hours |
| total_sessions | Int | No | Total sessions |

**Controller Methods:**
```python
def update_utilization(self, session_duration):
    # Update total_hours_used and total_sessions
    
def schedule_maintenance(self, maintenance_date):
    # Set next_maintenance_date
    # Block machine from scheduling
```

---

#### DocType: Machine Maintenance

**Purpose:** Track maintenance activities

**Type:** Document (Submittable)  
**Naming:** `MM-{YYYY}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| dialysis_machine | Link | Yes |
| maintenance_type | Select | Yes |
| scheduled_date | Date | Yes |
| actual_date | Date | No |
| assigned_technician | Link | Yes |
| maintenance_checklist | Table | Yes |
| findings | Text | No |
| parts_replaced | Table | No |
| photos | Attach Image | No |
| status | Select | Yes |
| next_maintenance_date | Date | No |

---

### 2.7 Module: Billing & Finance

#### DocType: Patient Bill

**Purpose:** Generate and manage patient bills

**Type:** Document (Submittable)  
**Naming:** `BILL-{YYYY}-{#####}`  
**Permissions:** Read: Patient, Healthcare Staff; Write: Billing Officer

**Fields:**

| Field Name | Field Type | Mandatory | Description |
|------------|------------|-----------|-------------|
| bill_number | Data | Yes | Auto-generated |
| patient | Link | Yes | Patient link |
| patient_name | Data | Read Only | Yes | Patient name |
| bill_date | Date | Yes | Bill date |
| due_date | Date | Yes | Payment due date |
| dialysis_session | Link | No | Linked session |
| billing_period_from | Date | No | For monthly bills |
| billing_period_to | Date | No | For monthly bills |
| bill_items | Table | Yes | Line items |
| subtotal | Currency | Read Only | Yes | Sum of items |
| discount_percentage | Float | No | Discount % |
| discount_amount | Currency | No | Discount amount |
| tax_percentage | Float | No | Tax % |
| tax_amount | Currency | No | Tax amount |
| total_amount | Currency | Read Only | Yes | Final total |
| amount_paid | Currency | Read Only | No | Amount paid so far |
| outstanding_amount | Currency | Read Only | No | Balance due |
| bill_status | Select | Yes | Draft, Submitted, Partially Paid, Paid, Cancelled |
| payment_mode | Select | No | Cash, Card, Transfer, Insurance |
| insurance_claim | Link | No | Linked claim |
| notes | Text | No | Billing notes |
| generated_by | Link | Yes | User who generated |

**Child Table: Bill Items**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| item_type | Select | Yes |
| item_description | Data | Yes |
| quantity | Float | Yes |
| rate | Currency | Yes |
| amount | Currency | Yes |

**Controller Methods:**
```python
def validate(self):
    # Calculate subtotal, tax, total
    # Apply discount
    # Update outstanding_amount
    
def on_submit(self):
    # Set bill_status to Submitted
    # Send bill to patient (email/SMS)
    
def apply_payment(self, payment_amount):
    # Update amount_paid and outstanding_amount
    # Update bill_status if fully paid
```

---

#### DocType: Payment Entry

**Purpose:** Record payments received

**Type:** Document (Submittable)  
**Naming:** `PAY-{YYYY}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| payment_date | Date | Yes |
| patient | Link | Yes |
| payment_mode | Select | Yes |
| amount | Currency | Yes |
| reference_number | Data | No |
| bills_paid | Table | Yes |
| received_by | Link | Yes |
| notes | Text | No |

**Child Table: Bills Paid**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| patient_bill | Link | Yes |
| bill_amount | Currency | Yes |
| amount_paid | Currency | Yes |

---

#### DocType: Insurance Claim

**Purpose:** Manage insurance claims

**Type:** Document (Submittable)  
**Naming:** `CLM-{YYYY}-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| patient | Link | Yes |
| insurance_company | Link | Yes |
| claim_date | Date | Yes |
| claim_type | Select | Yes |
| sessions | Table | Yes |
| total_claim_amount | Currency | Yes |
| approved_amount | Currency | No |
| rejection_reason | Text | No |
| claim_status | Select | Yes |
| submitted_date | Date | No |
| approval_date | Date | No |
| payment_received_date | Date | No |
| payment_entry | Link | No |

---

#### DocType: Price List

**Purpose:** Manage service pricing

**Type:** Master

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| price_list_name | Data | Yes |
| customer_tier | Select | Yes |
| is_default | Check | No |
| items | Table | Yes |

**Child Table: Items**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| service_type | Select | Yes |
| rate | Currency | Yes |
| valid_from | Date | No |
| valid_to | Date | No |

---

### 2.8 Module: Staff Management

#### DocType: Staff Member

**Purpose:** Manage staff information

**Type:** Master  
**Naming:** `STF-{#####}`

**Fields:**

| Field Name | Field Type | Mandatory | Description |
|------------|------------|-----------|-------------|
| staff_id | Data | Yes | Auto-generated |
| first_name | Data | Yes | First name |
| last_name | Data | Yes | Last name |
| full_name | Data | Read Only | Yes | Full name |
| date_of_birth | Date | No | DOB |
| gender | Select | Yes | Gender |
| phone | Data | Yes | Phone |
| email | Data | No | Email |
| designation | Select | Yes | Nephrologist, Nurse, Technician, etc. |
| department | Select | Yes | Clinical, Administrative, etc. |
| license_number | Data | No | Professional license |
| certifications | Table | No | Certifications |
| join_date | Date | Yes | Join date |
| employment_type | Select | Yes | Full-time, Part-time, Contract |
| shift_preference | Select | No | Preferred shift |
| location | Link | Yes | Primary location |
| emergency_contact_name | Data | Yes | Emergency contact |
| emergency_contact_phone | Data | Yes | Emergency phone |
| photo | Attach Image | No | Staff photo |
| user | Link | No | Linked user account |
| is_active | Check | Yes | Active status |

---

#### DocType: Staff Attendance

**Purpose:** Track staff attendance

**Fields:**

| Field Name | Field Type | Mandatory |
|------------|------------|-----------|
| staff_member | Link | Yes |
| attendance_date | Date | Yes |
| shift | Link | Yes |
| check_in_time | Datetime | No |
| check_out_time | Datetime | No |
| status | Select | Yes |
| late_entry | Check | No |
| early_exit | Check | No |
| overtime_hours | Float | No |

---

## 3. Database Schema

### 3.1 Core Tables (Auto-generated by Frappe)

Frappe automatically creates tables with prefix `tab` for each DocType.

**Example: Patient DocType → `tabPatient` table**

```sql
CREATE TABLE `tabPatient` (
  `name` varchar(140) NOT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `modified_by` varchar(140) DEFAULT NULL,
  `owner` varchar(140) DEFAULT NULL,
  `docstatus` int(1) NOT NULL DEFAULT 0,
  `idx` int(8) NOT NULL DEFAULT 0,
  
  -- Custom fields
  `patient_id` varchar(140) DEFAULT NULL,
  `first_name` varchar(140) DEFAULT NULL,
  `middle_name` varchar(140) DEFAULT NULL,
  `last_name` varchar(140) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` varchar(140) DEFAULT NULL,
  `blood_group` varchar(140) DEFAULT NULL,
  `national_id` varchar(140) DEFAULT NULL,
  `phone` varchar(140) DEFAULT NULL,
  `email` varchar(140) DEFAULT NULL,
  `insurance_provider` varchar(140) DEFAULT NULL,
  `ckd_stage` varchar(140) DEFAULT NULL,
  `patient_status` varchar(140) DEFAULT NULL,
  `vip_patient` int(1) DEFAULT 0,
  `registration_date` date DEFAULT NULL,
  
  PRIMARY KEY (`name`),
  KEY `modified` (`modified`),
  KEY `patient_status` (`patient_status`),
  UNIQUE KEY `national_id` (`national_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3.2 Key Indexes

**Performance-critical indexes to add:**

```sql
-- Patient table indexes
ALTER TABLE `tabPatient` ADD INDEX `idx_patient_status` (`patient_status`);
ALTER TABLE `tabPatient` ADD INDEX `idx_registration_date` (`registration_date`);
ALTER TABLE `tabPatient` ADD INDEX `idx_phone` (`phone`);

-- Appointment table indexes
ALTER TABLE `tabAppointment` ADD INDEX `idx_appointment_date` (`appointment_date`);
ALTER TABLE `tabAppointment` ADD INDEX `idx_patient_date` (`patient`, `appointment_date`);
ALTER TABLE `tabAppointment` ADD INDEX `idx_machine_date` (`dialysis_machine`, `appointment_date`);
ALTER TABLE `tabAppointment` ADD INDEX `idx_status` (`status`);

-- Dialysis Session indexes
ALTER TABLE `tabDialysis Session` ADD INDEX `idx_session_date` (`session_date`);
ALTER TABLE `tabDialysis Session` ADD INDEX `idx_patient_session` (`patient`, `session_date`);
ALTER TABLE `tabDialysis Session` ADD INDEX `idx_machine_session` (`dialysis_machine`, `session_date`);

-- Lab Test Result indexes
ALTER TABLE `tabLab Test Result` ADD INDEX `idx_patient_result` (`patient`, `result_date`);
ALTER TABLE `tabLab Test Result` ADD INDEX `idx_critical` (`critical_flag`);

-- Inventory indexes
ALTER TABLE `tabInventory Item` ADD INDEX `idx_reorder` (`reorder_level`);
ALTER TABLE `tabStock Receipt` ADD INDEX `idx_receipt_date` (`receipt_date`);

-- Bill indexes
ALTER TABLE `tabPatient Bill` ADD INDEX `idx_patient_bill` (`patient`, `bill_date`);
ALTER TABLE `tabPatient Bill` ADD INDEX `idx_bill_status` (`bill_status`);
ALTER TABLE `tabPatient Bill` ADD INDEX `idx_outstanding` (`outstanding_amount`);
```

---

## 4. Data Relationships

### 4.1 Entity Relationship Diagram (Text Format)

```
Patient (1) ──────< (M) Appointment
Patient (1) ──────< (M) Dialysis Session
Patient (1) ──────< (M) Lab Test Order
Patient (1) ──────< (M) Patient Bill
Patient (1) ──────< (M) Insurance Claim

Appointment (1) ────── (0..1) Dialysis Session
Appointment (M) ──────> (1) Dialysis Machine
Appointment (M) ──────> (1) Staff Member (Nurse)
Appointment (M) ──────> (1) Shift

Dialysis Session (1) ──────< (M) Vital Signs Log
Dialysis Session (1) ──────< (M) Session Event
Dialysis Session (1) ────── (0..1) Stock Issuance
Dialysis Session (1) ────── (0..1) Patient Bill

Dialysis Machine (1) ──────< (M) Appointment
Dialysis Machine (1) ──────< (M) Dialysis Session
Dialysis Machine (1) ──────< (M) Machine Maintenance

Lab Test Order (1) ──────< (M) Lab Test Result

Stock Receipt (M) ──────> (1) Supplier
Stock Receipt (1) ──────< (M) Stock Receipt Items

Stock Issuance (1) ──────< (M) Stock Issuance Items
Stock Issuance (M) ──────> (1) Dialysis Session

Patient Bill (1) ──────< (M) Bill Items
Patient Bill (M) ──────< (1) Payment Entry

Insurance Claim (M) ──────> (1) Insurance Company
Insurance Claim (1) ──────< (M) Sessions (table)

Staff Member (1) ──────< (M) Appointment (assigned_nurse)
Staff Member (1) ──────< (M) Dialysis Session (assigned_nurse)
Staff Member (1) ──────< (M) Shift Assignment
```

### 4.2 Key Relationships Detail

**Patient → Appointment → Session → Bill Flow:**
```
1. Patient registered
2. Appointment created for Patient
3. Patient checks in (Appointment.status = "Checked In")
4. Dialysis Session created from Appointment
5. Session completed (Session submitted)
6. Patient Bill auto-generated from Session
7. Payment Entry created and linked to Bill
```

**Inventory Flow:**
```
1. Stock Receipt created (goods received)
2. Stock balance updated in Inventory Item
3. Stock Issuance created during Dialysis Session
4. Stock balance reduced
5. Stock Issuance items added to Patient Bill
```

---

## 5. API Design

### 5.1 REST API Endpoints

**Base URL:** `/api/method/dcms.api.{module}.{function}`

#### Patient Management APIs

```python
# GET /api/resource/Patient/{patient_id}
# Get patient details
frappe.whitelist()
def get_patient(patient_id):
    return frappe.get_doc("Patient", patient_id)

# POST /api/method/dcms.api.patient.register_patient
# Register new patient
@frappe.whitelist()
def register_patient(patient_data):
    doc = frappe.get_doc({
        "doctype": "Patient",
        **patient_data
    })
    doc.insert()
    return doc

# GET /api/method/dcms.api.patient.get_medical_summary
# Get patient medical summary
@frappe.whitelist()
def get_medical_summary(patient_id):
    patient = frappe.get_doc("Patient", patient_id)
    return patient.get_medical_summary()

# POST /api/method/dcms.api.patient.upload_document
# Upload patient document
@frappe.whitelist()
def upload_document(patient_id, document_data):
    doc = frappe.get_doc({
        "doctype": "Patient Document",
        "patient": patient_id,
        **document_data
    })
    doc.insert()
    return doc
```

#### Appointment APIs

```python
# POST /api/method/dcms.api.appointment.book_appointment
@frappe.whitelist()
def book_appointment(appointment_data):
    doc = frappe.get_doc({
        "doctype": "Appointment",
        **appointment_data
    })
    doc.insert()
    return doc

# POST /api/method/dcms.api.appointment.check_availability
@frappe.whitelist()
def check_availability(date, machine_id=None, shift=None):
    # Return available slots
    pass

# POST /api/method/dcms.api.appointment.check_in
@frappe.whitelist()
def check_in_patient(appointment_id):
    appointment = frappe.get_doc("Appointment", appointment_id)
    appointment.check_in_patient()
    return appointment

# POST /api/method/dcms.api.appointment.create_recurring
@frappe.whitelist()
def create_recurring_appointments(recurrence_data):
    doc = frappe.get_doc({
        "doctype": "Recurring Appointment",
        **recurrence_data
    })
    doc.insert()
    doc.submit()
    return doc
```

#### Dialysis Session APIs

```python
# POST /api/method/dcms.api.session.start_session
@frappe.whitelist()
def start_session(session_data):
    doc = frappe.get_doc({
        "doctype": "Dialysis Session",
        **session_data
    })
    doc.insert()
    return doc

# POST /api/method/dcms.api.session.record_vitals
@frappe.whitelist()
def record_vitals(session_id, vitals_data):
    session = frappe.get_doc("Dialysis Session", session_id)
    session.append("vital_signs_log", vitals_data)
    session.save()
    return session

# POST /api/method/dcms.api.session.complete_session
@frappe.whitelist()
def complete_session(session_id, post_dialysis_data):
    session = frappe.get_doc("Dialysis Session", session_id)
    session.update(post_dialysis_data)
    session.complete_session()
    return session

# GET /api/method/dcms.api.session.get_active_sessions
@frappe.whitelist()
def get_active_sessions(location=None):
    filters = {"session_status": "In Progress"}
    if location:
        filters["location"] = location
    return frappe.get_all("Dialysis Session", filters=filters)
```

#### Billing APIs

```python
# POST /api/method/dcms.api.billing.generate_bill
@frappe.whitelist()
def generate_bill(session_id):
    # Auto-generate bill from session
    pass

# POST /api/method/dcms.api.billing.record_payment
@frappe.whitelist()
def record_payment(payment_data):
    doc = frappe.get_doc({
        "doctype": "Payment Entry",
        **payment_data
    })
    doc.insert()
    doc.submit()
    return doc

# GET /api/method/dcms.api.billing.get_outstanding_bills
@frappe.whitelist()
def get_outstanding_bills(patient_id):
    return frappe.get_all("Patient Bill",
        filters={"patient": patient_id, "outstanding_amount": [">", 0]})
```

---

## 6. Integration Points

### 6.1 Laboratory Information System (LIS) Integration

**Protocol:** HL7 v2.x or FHIR

**Outbound Messages (DCMS → LIS):**
- Lab Order Message (ORM^O01)
- Cancel Order (ORM^O01)

**Inbound Messages (LIS → DCMS):**
- Result Message (ORU^R01)
- Order Status Update

**Implementation:**
```python
# dcms/integrations/lis_integration.py

@frappe.whitelist()
def send_lab_order_to_lis(lab_order_id):
    order = frappe.get_doc("Lab Test Order", lab_order_id)
    hl7_message = generate_orm_message(order)
    response = send_to_lis(hl7_message)
    return response

def receive_lab_result_from_lis(hl7_message):
    result_data = parse_oru_message(hl7_message)
    create_lab_result(result_data)
```

### 6.2 SMS Gateway Integration

**Provider:** Twilio / Custom

```python
# dcms/integrations/sms.py

def send_appointment_reminder(appointment_id):
    appointment = frappe.get_doc("Appointment", appointment_id)
    message = f"Reminder: Dialysis appointment on {appointment.appointment_date} at {appointment.appointment_time}"
    send_sms(appointment.patient.phone, message)
```

### 6.3 Payment Gateway Integration

**Provider:** Stripe / PayPal

```python
# dcms/integrations/payment_gateway.py

@frappe.whitelist()
def process_online_payment(bill_id, payment_method):
    bill = frappe.get_doc("Patient Bill", bill_id)
    payment_intent = create_stripe_payment(bill.total_amount)
    return payment_intent
```

---

## 7. Security Design

### 7.1 Role-Based Access Control (RBAC)

**Roles:**

| Role | Permissions |
|------|-------------|
| Administrator | Full access to all modules |
| Medical Director | Read all, Write clinical |
| Nephrologist | Read all clinical, Write prescriptions |
| Nurse | Read clinical, Write sessions |
| Technician | Read equipment, Write maintenance |
| Receptionist | Read/Write appointments, patients |
| Billing Officer | Read/Write billing, payments |
| Inventory Manager | Read/Write inventory |
| Lab Coordinator | Read/Write lab orders/results |

**DocType Permissions Matrix:**

```python
# Patient DocType permissions
{
    "Patient": {
        "read": ["All"],
        "write": ["Receptionist", "Nurse", "Doctor"],
        "create": ["Receptionist"],
        "delete": ["Administrator"]
    },
    "Dialysis Session": {
        "read": ["All Healthcare Roles"],
        "write": ["Nurse", "Doctor"],
        "create": ["Nurse"],
        "submit": ["Nurse", "Doctor"]
    }
}
```

### 7.2 Data Encryption

**Sensitive Fields Encryption:**
```python
# Encrypt sensitive fields
encrypted_fields = [
    "Patient.national_id",
    "Patient.insurance_id",
    "Payment Entry.reference_number"
]
```

### 7.3 Audit Trail

**Tracked Actions:**
- All create, update, delete operations
- User login/logout
- Permission changes
- Sensitive data access

```python
# Auto-tracked by Frappe Version Control
# Additional custom audit logging
def log_sensitive_access(doctype, name, user):
    frappe.get_doc({
        "doctype": "Audit Log",
        "document_type": doctype,
        "document_name": name,
        "user": user,
        "action": "Viewed",
        "timestamp": now()
    }).insert()
```

---

## 8. Performance Considerations

### 8.1 Caching Strategy

**Redis Caching:**
```python
# Cache frequently accessed data
@frappe.whitelist()
def get_active_patients():
    cache_key = "active_patients"
    cached = frappe.cache().get_value(cache_key)
    
    if cached:
        return cached
    
    patients = frappe.get_all("Patient", 
        filters={"patient_status": "Active"},
        fields=["name", "full_name", "patient_id"])
    
    # Cache for 1 hour
    frappe.cache().set_value(cache_key, patients, expires_in_sec=3600)
    return patients

# Invalidate cache on patient update
def on_patient_update(doc, method):
    frappe.cache().delete_value("active_patients")
```

**Document-level Caching:**
```python
# Use get_cached_doc for frequently accessed documents
patient = frappe.get_cached_doc("Patient", patient_id)
```

### 8.2 Query Optimization

**Best Practices:**
```python
# Bad: SELECT * with unnecessary fields
patients = frappe.get_all("Patient")

# Good: Specify only needed fields
patients = frappe.get_all("Patient", 
    fields=["name", "patient_id", "full_name"],
    filters={"patient_status": "Active"})

# Bad: N+1 query problem
for appointment in appointments:
    patient_name = frappe.get_value("Patient", appointment.patient, "full_name")

# Good: Single query with join
appointments = frappe.get_all("Appointment",
    fields=["name", "patient.full_name"],
    filters={"appointment_date": today()})
```

### 8.3 Background Jobs

**Scheduled Tasks Configuration:**
```python
# hooks.py

scheduler_events = {
    "daily": [
        "dcms.tasks.daily_cleanup",
        "dcms.tasks.send_appointment_reminders",
        "dcms.tasks.check_expiring_stock"
    ],
    "hourly": [
        "dcms.tasks.sync_lab_results",
        "dcms.tasks.update_machine_status"
    ],
    "cron": {
        "0 6 * * *": [  # 6 AM daily
            "dcms.tasks.generate_daily_reports"
        ],
        "0 0 1 * *": [  # 1st of every month
            "dcms.tasks.generate_monthly_reports"
        ]
    }
}
```

**Background Job Queue:**
```python
# Use RQ for long-running tasks
@frappe.whitelist()
def generate_large_report(filters):
    frappe.enqueue(
        "dcms.reports.generate_clinical_report",
        queue="long",
        timeout=600,
        filters=filters,
        user=frappe.session.user
    )
    return {"status": "queued"}
```

### 8.4 Database Connection Pooling

**Configuration in site_config.json:**
```json
{
    "db_pool_size": 20,
    "db_max_overflow": 10,
    "db_timeout": 30
}
```

### 8.5 Asset Optimization

**Bundle Configuration:**
```python
# hooks.py

app_include_js = [
    "/assets/dcms/js/dcms.bundle.js"
]

app_include_css = [
    "/assets/dcms/css/dcms.bundle.css"
]

# Minify assets in production
build = {
    "minify": True,
    "source_map": False
}
```

---

## 9. Hooks Configuration

### 9.1 hooks.py Complete Example

```python
# dcms/hooks.py

from . import __version__ as app_version

app_name = "dcms"
app_title = "Dialysis Center Management System"
app_publisher = "Your Organization"
app_description = "Comprehensive dialysis center management"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "info@yourorg.com"
app_license = "MIT"

# Modules
# ----------
app_include_css = "/assets/dcms/css/dcms.css"
app_include_js = "/assets/dcms/js/dcms.js"

# Document Events
# ---------------
doc_events = {
    "Patient": {
        "validate": "dcms.patient_management.patient.validate_patient",
        "on_update": "dcms.patient_management.patient.on_patient_update",
        "after_insert": "dcms.patient_management.patient.after_patient_insert"
    },
    "Appointment": {
        "validate": "dcms.appointment_scheduling.appointment.validate_appointment",
        "on_submit": "dcms.appointment_scheduling.appointment.on_appointment_submit",
        "on_cancel": "dcms.appointment_scheduling.appointment.on_appointment_cancel"
    },
    "Dialysis Session": {
        "validate": "dcms.clinical_operations.dialysis_session.validate_session",
        "on_submit": "dcms.clinical_operations.dialysis_session.on_session_submit",
        "after_insert": "dcms.clinical_operations.dialysis_session.create_stock_issuance"
    },
    "Stock Receipt": {
        "on_submit": "dcms.inventory.stock_receipt.update_stock_balance"
    },
    "Stock Issuance": {
        "on_submit": "dcms.inventory.stock_issuance.reduce_stock_balance"
    },
    "Patient Bill": {
        "on_submit": "dcms.billing.patient_bill.on_bill_submit"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "dcms.tasks.send_appointment_reminders",
        "dcms.tasks.check_expiring_stock",
        "dcms.tasks.check_expiring_insurance",
        "dcms.tasks.generate_daily_census_report"
    ],
    "hourly": [
        "dcms.tasks.sync_lab_results",
        "dcms.tasks.check_low_stock_alerts"
    ],
    "weekly": [
        "dcms.tasks.generate_weekly_summary"
    ],
    "monthly": [
        "dcms.tasks.generate_monthly_clinical_report",
        "dcms.tasks.archive_old_data"
    ],
    "cron": {
        "0 8 * * *": [
            "dcms.tasks.send_morning_briefing"
        ],
        "0 0 1 * *": [
            "dcms.tasks.monthly_billing_cycle"
        ]
    }
}

# Permissions
# -----------
permission_query_conditions = {
    "Patient": "dcms.permissions.patient_query",
    "Dialysis Session": "dcms.permissions.session_query"
}

has_permission = {
    "Patient": "dcms.permissions.patient_permission",
    "Appointment": "dcms.permissions.appointment_permission"
}

# Fixtures
# --------
fixtures = [
    {"dt": "Custom Field", "filters": [["name", "in", ["Patient-custom_field"]]]},
    {"dt": "Role", "filters": [["name", "in", ["Nephrologist", "Dialysis Nurse"]]]},
    "Lab Test Template",
    "Treatment Template"
]

# Website Settings
# ----------------
website_route_rules = [
    {"from_route": "/patient-portal/<path:app_path>", "to_route": "patient-portal"}
]

# Jinja Filters
# -------------
jinja = {
    "methods": [
        "dcms.utils.format_session_duration",
        "dcms.utils.calculate_kt_v"
    ],
    "filters": [
        "dcms.utils.format_blood_pressure"
    ]
}

# Override Standard Frappe Methods
# ---------------------------------
override_whitelisted_methods = {
    "frappe.desk.form.save.savedocs": "dcms.overrides.custom_save"
}

# Email Notifications
# -------------------
email_notifications = {
    "Dialysis Session": {
        "on_submit": {
            "recipients": ["assigned_nurse", "assigned_doctor"],
            "subject": "Session Completed: {patient_name}",
            "template": "session_completed"
        }
    },
    "Lab Test Result": {
        "on_submit": {
            "recipients": ["ordered_by"],
            "subject": "Lab Results Available: {patient}",
            "template": "lab_results_ready",
            "condition": "doc.critical_flag == 1"
        }
    }
}

# Report Configurations
# ---------------------
standard_queries = {
    "Patient": "dcms.queries.patient_query"
}
```

---

## 10. Implementation Checklist

### 10.1 Phase 1: Foundation (Weeks 1-4)

**Week 1-2: Setup & Core**
- [ ] Create Frappe app: `bench new-app dcms`
- [ ] Setup module structure
- [ ] Configure hooks.py
- [ ] Create Patient DocType
- [ ] Create Staff Member DocType
- [ ] Setup roles and permissions
- [ ] Implement patient registration workflow

**Week 3-4: Appointment System**
- [ ] Create Dialysis Machine DocType
- [ ] Create Shift DocType
- [ ] Create Appointment DocType
- [ ] Implement appointment validation
- [ ] Create calendar view page
- [ ] Implement check-in functionality

### 10.2 Phase 2: Clinical Operations (Weeks 5-8)

**Week 5-6: Session Management**
- [ ] Create Dialysis Session DocType
- [ ] Create Vital Signs Log (child table)
- [ ] Create Session Event (child table)
- [ ] Create Treatment Template DocType
- [ ] Implement session workflow
- [ ] Add session monitoring page

**Week 7-8: Laboratory Integration**
- [ ] Create Lab Test Order DocType
- [ ] Create Lab Test Result DocType
- [ ] Create Lab Test Template DocType
- [ ] Implement Kt/V and URR calculations
- [ ] Setup LIS integration (if required)
- [ ] Create lab results trending charts

### 10.3 Phase 3: Business Operations (Weeks 9-12)

**Week 9-10: Inventory & Equipment**
- [ ] Create Inventory Item DocType
- [ ] Create Stock Receipt DocType
- [ ] Create Stock Issuance DocType
- [ ] Implement stock balance tracking
- [ ] Create Machine Maintenance DocType
- [ ] Setup low stock alerts

**Week 11-12: Billing & Finance**
- [ ] Create Patient Bill DocType
- [ ] Create Payment Entry DocType
- [ ] Create Insurance Claim DocType
- [ ] Create Price List DocType
- [ ] Implement billing automation
- [ ] Setup payment gateway integration

### 10.4 Phase 4: Analytics & Polish (Weeks 13-16)

**Week 13-14: Reporting**
- [ ] Create Executive Dashboard
- [ ] Create Daily Census Report
- [ ] Create Monthly Clinical Quality Report
- [ ] Create Financial Summary Report
- [ ] Create Machine Utilization Report
- [ ] Setup scheduled report generation

**Week 15-16: Communication & Testing**
- [ ] Setup SMS gateway integration
- [ ] Implement appointment reminders
- [ ] Implement critical alerts
- [ ] Comprehensive testing
- [ ] User acceptance testing
- [ ] Performance optimization

---

## 11. Development Guidelines

### 11.1 Naming Conventions

**DocTypes:**
- Use Title Case: `Patient`, `Dialysis Session`
- Descriptive names: `Lab Test Order` not `LTO`

**Fields:**
- Use snake_case: `patient_name`, `appointment_date`
- Prefix boolean fields: `is_active`, `has_batch_no`

**Python Files:**
- snake_case: `patient.py`, `dialysis_session.py`

**JavaScript Files:**
- snake_case: `appointment_calendar.js`

### 11.2 Code Organization

```python
# dcms/patient_management/doctype/patient/patient.py

import frappe
from frappe.model.document import Document
from frappe import _

class Patient(Document):
    """Patient DocType Controller"""
    
    def autoname(self):
        """Auto-generate patient ID"""
        self.name = generate_patient_id()
    
    def validate(self):
        """Validation logic"""
        self.validate_unique_national_id()
        self.calculate_age()
        self.set_full_name()
    
    def on_update(self):
        """After save logic"""
        self.generate_qr_code()
    
    def validate_unique_national_id(self):
        """Check for duplicate national ID"""
        if self.national_id:
            existing = frappe.db.exists("Patient", {
                "national_id": self.national_id,
                "name": ["!=", self.name]
            })
            if existing:
                frappe.throw(_("Patient with this National ID already exists"))
    
    def calculate_age(self):
        """Calculate age from DOB"""
        if self.date_of_birth:
            from frappe.utils import getdate, nowdate
            from dateutil.relativedelta import relativedelta
            
            dob = getdate(self.date_of_birth)
            today = getdate(nowdate())
            self.age = relativedelta(today, dob).years
    
    def set_full_name(self):
        """Set full name"""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        self.full_name = " ".join(parts)
    
    def generate_qr_code(self):
        """Generate QR code for patient"""
        if not self.qr_code:
            import qrcode
            from io import BytesIO
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.name)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            
            # Save as attachment
            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": f"{self.name}_qr.png",
                "content": buffer.getvalue(),
                "attached_to_doctype": "Patient",
                "attached_to_name": self.name
            })
            file_doc.insert()
            self.qr_code = file_doc.file_url


def generate_patient_id():
    """Generate unique patient ID"""
    from frappe.utils import nowdate
    year = nowdate()[:4]
    
    # Get last patient ID for the year
    last_id = frappe.db.sql("""
        SELECT MAX(CAST(SUBSTRING(name, 9) AS UNSIGNED))
        FROM `tabPatient`
        WHERE name LIKE %s
    """, (f"PT-{year}-%",))
    
    next_num = (last_id[0][0] or 0) + 1
    return f"PT-{year}-{next_num:05d}"
```

### 11.3 Testing

**Unit Test Example:**
```python
# dcms/patient_management/doctype/patient/test_patient.py

import frappe
import unittest
from frappe.utils import nowdate, add_years

class TestPatient(unittest.TestCase):
    
    def setUp(self):
        """Setup test data"""
        self.test_patient_data = {
            "doctype": "Patient",
            "first_name": "Test",
            "last_name": "Patient",
            "date_of_birth": add_years(nowdate(), -30),
            "gender": "Male",
            "phone": "1234567890",
            "emergency_contact_name": "Emergency Contact",
            "emergency_contact_phone": "0987654321",
            "patient_status": "Active"
        }
    
    def test_patient_creation(self):
        """Test patient creation"""
        patient = frappe.get_doc(self.test_patient_data)
        patient.insert()
        
        self.assertTrue(patient.name.startswith("PT-"))
        self.assertEqual(patient.full_name, "Test Patient")
        self.assertEqual(patient.age, 30)
        
        patient.delete()
    
    def test_duplicate_national_id(self):
        """Test duplicate national ID validation"""
        patient1 = frappe.get_doc(self.test_patient_data)
        patient1.national_id = "123456789"
        patient1.insert()
        
        patient2 = frappe.get_doc(self.test_patient_data)
        patient2.national_id = "123456789"
        
        with self.assertRaises(frappe.ValidationError):
            patient2.insert()
        
        patient1.delete()
```

---

## 12. Deployment Architecture

### 12.1 Production Setup

```
┌─────────────────────────────────────────────┐
│           Load Balancer (Nginx)             │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌───────▼────────┐
│  App Server 1  │  │  App Server 2  │
│  (Gunicorn)    │  │  (Gunicorn)    │
└───────┬────────┘  └───────┬────────┘
        │                   │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │   MariaDB Master  │
        │   (Primary DB)    │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │  MariaDB Replica  │
        │  (Read Replica)   │
        └───────────────────┘
                  
        ┌───────────────────┐
        │   Redis Cluster   │
        │  (Cache & Queue)  │
        └───────────────────┘
```

### 12.2 Docker Compose Example

```yaml
# docker-compose.yml

version: '3.8'

services:
  mariadb:
    image: mariadb:10.11
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: dcms
    volumes:
      - mariadb-data:/var/lib/mysql
    ports:
      - "3306:3306"
  
  redis-cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  redis-queue:
    image: redis:7-alpine
    ports:
      - "6380:6379"
  
  frappe:
    build: .
    volumes:
      - ./frappe-bench:/home/frappe/frappe-bench
    ports:
      - "8000:8000"
    depends_on:
      - mariadb
      - redis-cache
      - redis-queue
    environment:
      DB_HOST: mariadb
      REDIS_CACHE: redis-cache:6379
      REDIS_QUEUE: redis-queue:6379

volumes:
  mariadb-data:
```

---

## 13. Conclusion

This technical design document provides a comprehensive blueprint for implementing the Dialysis Center Management System on Frappe Framework. Key highlights:

- **25+ DocTypes** covering all modules
- **RESTful API** design for integrations
- **Optimized database** schema with proper indexing
- **Security-first** approach with RBAC and encryption
- **Performance optimization** strategies
- **Complete implementation** checklist

### Next Steps

1. **Review and approve** this technical design
2. **Setup development environment**
3. **Begin Phase 1 implementation**
4. **Iterative development** following sprint plan
5. **Continuous testing** and refinement

---

**Document Version:** 1.0  
**Last Updated:** February 19, 2026  
**Status:** Ready for Review

**End of Technical Design Document**