# Dialysis Center Management System - User Stories

## Document Information

**Project Name:** Dialysis Center Management System (DCMS)  
**Platform:** Frappe Framework v15+  
**Document Version:** 1.0  
**Date:** February 19, 2026  
**Status:** Draft

---

## How to Use This Document

### User Story Format
Each user story follows the standard format:
- **As a** [role]
- **I want** [feature/functionality]
- **So that** [benefit/value]

### Story Components
- **Story ID:** Unique identifier (US-XXX)
- **Epic:** High-level feature grouping
- **Priority:** MoSCoW (Must have, Should have, Could have, Won't have)
- **Story Points:** Complexity estimate (1, 2, 3, 5, 8, 13, 21)
- **Acceptance Criteria:** Testable conditions for completion
- **Dependencies:** Related stories or technical requirements

### Priority Levels
- **Must Have:** Critical for MVP, blocks other features
- **Should Have:** Important but not critical
- **Could Have:** Nice to have, can be deferred
- **Won't Have:** Out of scope for current release

---

## Epic Overview

| Epic ID | Epic Name | Description | Story Count |
|---------|-----------|-------------|-------------|
| EP-01 | Patient Management | Patient registration, profiles, and medical records | 12 |
| EP-02 | Appointment & Scheduling | Booking, calendar management, and resource allocation | 10 |
| EP-03 | Treatment & Clinical | Dialysis sessions, vitals, and clinical documentation | 15 |
| EP-04 | Laboratory Integration | Lab orders, results, and clinical calculations | 8 |
| EP-05 | Inventory Management | Stock control, procurement, and consumption tracking | 10 |
| EP-06 | Equipment Management | Machine registry, maintenance, and utilization | 7 |
| EP-07 | Billing & Finance | Invoicing, payments, and insurance claims | 12 |
| EP-08 | Staff Management | Staff profiles, scheduling, and performance | 8 |
| EP-09 | Reporting & Analytics | Reports, dashboards, and business intelligence | 10 |
| EP-10 | Security & Compliance | Access control, audit trails, and regulatory compliance | 8 |
| EP-11 | Communication | Notifications, alerts, and messaging | 6 |
| EP-12 | System Administration | Multi-location, integrations, and system configuration | 8 |

**Total User Stories:** 114

---

## EPIC 01: Patient Management

### US-001: Register New Patient
**Epic:** EP-01 - Patient Management  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Receptionist**,  
I want to **register a new patient in the system**,  
So that **the patient's information is available for appointments and treatments**.

**Acceptance Criteria:**
- [ ] System captures full name (first, middle, last)
- [ ] Date of birth is mandatory and age is auto-calculated
- [ ] Unique patient ID is generated automatically (e.g., PT-0001)
- [ ] Contact information fields include phone and email
- [ ] Emergency contact can be recorded
- [ ] National ID and insurance ID fields available
- [ ] Blood group and Rh factor can be selected
- [ ] Patient photo can be uploaded
- [ ] Form validation prevents duplicate patient registration
- [ ] Success message displayed upon registration
- [ ] Patient profile is immediately searchable

**Dependencies:** None

**Technical Notes:**
- Create Patient DocType with required fields
- Implement auto-naming for patient ID
- Add duplicate check on National ID

---

### US-002: Update Patient Demographics
**Epic:** EP-01 - Patient Management  
**Priority:** Must Have  
**Story Points:** 3

**User Story:**
As a **Receptionist**,  
I want to **update patient demographic information**,  
So that **patient records remain current and accurate**.

**Acceptance Criteria:**
- [ ] All demographic fields are editable except Patient ID
- [ ] Change history is tracked with timestamp and user
- [ ] Validation prevents invalid data entry
- [ ] Changes are saved immediately
- [ ] Success notification displayed after update
- [ ] Updated information reflects in all related records

**Dependencies:** US-001

---

### US-003: Record Patient Medical History
**Epic:** EP-01 - Patient Management  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Nephrologist**,  
I want to **record comprehensive patient medical history**,  
So that **I have complete clinical information for treatment planning**.

**Acceptance Criteria:**
- [ ] Can record chronic conditions and comorbidities
- [ ] Allergies section with severity indicators
- [ ] Previous surgeries and procedures can be listed
- [ ] Family medical history can be documented
- [ ] Current medications list with dosages
- [ ] Referring physician details can be added
- [ ] CKD stage can be selected and tracked
- [ ] History is organized in chronological order
- [ ] All entries are timestamped with author

**Dependencies:** US-001

---

### US-004: Upload Patient Documents
**Epic:** EP-01 - Patient Management  
**Priority:** Should Have  
**Story Points:** 3

**User Story:**
As a **Nurse**,  
I want to **upload and organize patient documents**,  
So that **all medical records are accessible in one place**.

**Acceptance Criteria:**
- [ ] Support PDF and image file uploads (JPG, PNG)
- [ ] Maximum file size of 10MB per document
- [ ] Documents can be categorized (Lab Report, Imaging, Consent Form, etc.)
- [ ] Document title and description can be added
- [ ] Upload date and uploaded by user is recorded
- [ ] Documents can be previewed without downloading
- [ ] Documents can be downloaded
- [ ] Old documents can be marked as expired/superseded

**Dependencies:** US-001

---

### US-005: Search and Filter Patients
**Epic:** EP-01 - Patient Management  
**Priority:** Must Have  
**Story Points:** 3

**User Story:**
As a **Healthcare Provider**,  
I want to **search for patients using multiple criteria**,  
So that **I can quickly find the patient I need**.

**Acceptance Criteria:**
- [ ] Search by Patient ID, Name, Phone, or National ID
- [ ] Auto-suggest appears after typing 3 characters
- [ ] Filter by status (Active, Inactive)
- [ ] Filter by insurance type
- [ ] Filter by CKD stage
- [ ] Results display key information (ID, Name, Age, Last Visit)
- [ ] Clicking result opens patient profile
- [ ] Search performance < 2 seconds

**Dependencies:** US-001

---

### US-006: Manage Patient Consent
**Epic:** EP-01 - Patient Management  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Receptionist**,  
I want to **record and track patient consent forms**,  
So that **we maintain legal compliance and patient authorization**.

**Acceptance Criteria:**
- [ ] Treatment consent form can be recorded
- [ ] Data privacy consent can be captured
- [ ] Emergency treatment authorization can be stored
- [ ] Digital signature can be captured (tablet/mouse)
- [ ] Consent date and witness information recorded
- [ ] Physical consent forms can be uploaded as PDF
- [ ] Consent status shows as Complete/Pending
- [ ] Reminder alerts for expired consents
- [ ] Consent history is maintained

**Dependencies:** US-001

---

### US-007: Track Patient Disease Progression
**Epic:** EP-01 - Patient Management  
**Priority:** Should Have  
**Story Points:** 8

**User Story:**
As a **Nephrologist**,  
I want to **view patient disease progression over time**,  
So that **I can make informed clinical decisions**.

**Acceptance Criteria:**
- [ ] Timeline view of CKD stage changes
- [ ] eGFR values plotted on a graph
- [ ] Key clinical events marked on timeline
- [ ] Lab results trending over time
- [ ] Weight and vital signs graphs
- [ ] Dialysis adequacy (Kt/V) trending
- [ ] Export graph as image or PDF
- [ ] Configurable date range for views
- [ ] Color-coded indicators for worsening/improving trends

**Dependencies:** US-001, US-003

---

### US-008: Set Patient Status (Active/Inactive)
**Epic:** EP-01 - Patient Management  
**Priority:** Must Have  
**Story Points:** 2

**User Story:**
As a **Medical Director**,  
I want to **change patient status to active or inactive**,  
So that **only active patients appear in scheduling and billing**.

**Acceptance Criteria:**
- [ ] Status can be toggled between Active and Inactive
- [ ] Reason for inactivation must be provided
- [ ] Inactive date is automatically recorded
- [ ] Inactive patients cannot be scheduled for appointments
- [ ] Warning shown before inactivating patient
- [ ] Inactive patients can be reactivated
- [ ] Status change is logged in audit trail

**Dependencies:** US-001

---

### US-009: View Patient Summary Dashboard
**Epic:** EP-01 - Patient Management  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Nephrologist**,  
I want to **see a summary dashboard for each patient**,  
So that **I can quickly assess the patient's current status**.

**Acceptance Criteria:**
- [ ] Dashboard shows demographics at a glance
- [ ] Last dialysis session date and details
- [ ] Next scheduled appointment
- [ ] Recent lab results (last 30 days)
- [ ] Current medications list
- [ ] Outstanding balance (if any)
- [ ] Recent alerts or flags
- [ ] Quick action buttons (Schedule, View History, Add Note)

**Dependencies:** US-001, US-003

---

### US-010: Generate Patient QR Code
**Epic:** EP-01 - Patient Management  
**Priority:** Could Have  
**Story Points:** 3

**User Story:**
As a **Receptionist**,  
I want to **generate a QR code for each patient**,  
So that **patient check-in can be faster using QR scanning**.

**Acceptance Criteria:**
- [ ] QR code is auto-generated for each patient
- [ ] QR code encodes Patient ID
- [ ] QR code is printable on patient card
- [ ] Scanning QR code opens patient profile
- [ ] QR code can be regenerated if needed
- [ ] QR code includes error correction

**Dependencies:** US-001

---

### US-011: Mark Patient as VIP
**Epic:** EP-01 - Patient Management  
**Priority:** Could Have  
**Story Points:** 2

**User Story:**
As a **Administrator**,  
I want to **flag certain patients as VIP**,  
So that **staff provides appropriate special attention**.

**Acceptance Criteria:**
- [ ] VIP checkbox on patient profile
- [ ] VIP badge visible on patient name everywhere
- [ ] VIP patients highlighted in appointment calendar
- [ ] Reason for VIP status can be noted
- [ ] VIP status affects priority in scheduling conflicts
- [ ] Reports can filter by VIP status

**Dependencies:** US-001

---

### US-012: Merge Duplicate Patient Records
**Epic:** EP-01 - Patient Management  
**Priority:** Should Have  
**Story Points:** 8

**User Story:**
As a **Administrator**,  
I want to **merge duplicate patient records**,  
So that **patient data remains accurate and consolidated**.

**Acceptance Criteria:**
- [ ] System identifies potential duplicates based on name and DOB
- [ ] Administrator can review suggested duplicates
- [ ] Side-by-side comparison of records before merge
- [ ] Primary record can be selected
- [ ] All appointments, sessions, and bills are transferred
- [ ] Merged record is marked and archived (not deleted)
- [ ] Merge action is logged with reason
- [ ] Confirmation required before merge
- [ ] Merge cannot be undone (permanent action)

**Dependencies:** US-001

---

## EPIC 02: Appointment & Scheduling

### US-013: Book Dialysis Appointment
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Must Have  
**Story Points:** 8

**User Story:**
As a **Receptionist**,  
I want to **book a dialysis appointment for a patient**,  
So that **the patient has a confirmed time slot and machine**.

**Acceptance Criteria:**
- [ ] Select patient from searchable dropdown
- [ ] Choose appointment date from calendar
- [ ] Select available time slot (shift-based)
- [ ] Assign specific dialysis machine/station
- [ ] Set session duration (default 4 hours, editable)
- [ ] Assign nurse to the session
- [ ] Add special instructions or notes
- [ ] Prevent double-booking of machines
- [ ] Check staff availability
- [ ] Verify patient is active and eligible
- [ ] Confirmation message with appointment details
- [ ] Appointment appears on calendar immediately

**Dependencies:** US-001

**Technical Notes:**
- Create Appointment DocType
- Implement validation for machine and staff availability
- Add date/time picker with slot visualization

---

### US-014: Create Recurring Appointments
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Must Have  
**Story Points:** 8

**User Story:**
As a **Receptionist**,  
I want to **create recurring appointments for regular dialysis patients**,  
So that **I don't have to book each session individually**.

**Acceptance Criteria:**
- [ ] Define recurrence pattern (Mon-Wed-Fri, Tue-Thu-Sat, etc.)
- [ ] Set start date and end date for recurrence
- [ ] Apply same time slot and machine for all sessions
- [ ] Option to exclude specific dates (holidays)
- [ ] Preview all appointments before confirming
- [ ] Bulk creation of appointments
- [ ] Handle conflicts gracefully (skip or alert)
- [ ] Recurrence can be modified or stopped
- [ ] Individual sessions can be modified without affecting series

**Dependencies:** US-013

---

### US-015: View Appointment Calendar
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Receptionist**,  
I want to **view appointments in a calendar format**,  
So that **I can see the schedule at a glance**.

**Acceptance Criteria:**
- [ ] Day, week, and month view options
- [ ] Color-coded by status (Scheduled, In Progress, Completed, Cancelled)
- [ ] Each appointment shows patient name and machine
- [ ] Click appointment to view details
- [ ] Filter by machine, staff, or patient
- [ ] Today's date highlighted
- [ ] Navigation between dates is smooth
- [ ] Calendar loads in < 2 seconds

**Dependencies:** US-013

---

### US-016: Reschedule Appointment
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Receptionist**,  
I want to **reschedule an existing appointment**,  
So that **I can accommodate patient requests or conflicts**.

**Acceptance Criteria:**
- [ ] Select appointment to reschedule
- [ ] Choose new date and time
- [ ] Check availability of machine and staff
- [ ] Reason for rescheduling must be provided
- [ ] Original appointment details are preserved in history
- [ ] Patient notification sent (if configured)
- [ ] Calendar updates immediately
- [ ] Rescheduling is logged in audit trail

**Dependencies:** US-013

---

### US-017: Cancel Appointment
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Must Have  
**Story Points:** 3

**User Story:**
As a **Receptionist**,  
I want to **cancel an appointment**,  
So that **the time slot becomes available for other patients**.

**Acceptance Criteria:**
- [ ] Select appointment to cancel
- [ ] Cancellation reason is mandatory
- [ ] Cancelled appointments marked clearly in calendar
- [ ] Machine and staff resources are freed up
- [ ] Cancellation notification sent to patient (optional)
- [ ] Cancelled appointments retained in history
- [ ] Can filter/report on cancellations
- [ ] No-show can be marked separately from cancellation

**Dependencies:** US-013

---

### US-018: Check Patient In
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Must Have  
**Story Points:** 3

**User Story:**
As a **Receptionist**,  
I want to **check-in a patient when they arrive**,  
So that **the clinical staff knows the patient is ready for treatment**.

**Acceptance Criteria:**
- [ ] Search for patient or scan QR code
- [ ] Display today's appointments for the patient
- [ ] One-click check-in button
- [ ] Check-in time is recorded
- [ ] Appointment status changes to "Checked In"
- [ ] Notification sent to assigned nurse
- [ ] Late arrivals are flagged
- [ ] Cannot check-in more than 30 minutes before scheduled time

**Dependencies:** US-013

---

### US-019: View Machine Availability
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Receptionist**,  
I want to **view real-time machine availability**,  
So that **I can quickly find open slots for booking**.

**Acceptance Criteria:**
- [ ] Grid view showing all machines and time slots
- [ ] Color-coded availability (Available, Booked, Maintenance, Out of Service)
- [ ] Filter by shift (Morning, Afternoon, Evening)
- [ ] Click on available slot to book immediately
- [ ] Show machine details on hover
- [ ] Refresh button to update availability
- [ ] Utilization percentage displayed per machine

**Dependencies:** US-013

---

### US-020: Manage Shift Configuration
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Administrator**,  
I want to **configure shift timings and capacity**,  
So that **appointments are aligned with operational hours**.

**Acceptance Criteria:**
- [ ] Define shift names (Morning, Afternoon, Evening, Night)
- [ ] Set start and end time for each shift
- [ ] Define maximum patients per shift
- [ ] Configure days of operation per shift
- [ ] Set buffer time between sessions
- [ ] Apply to specific locations
- [ ] Changes affect future bookings only
- [ ] Validation prevents overlapping shifts

**Dependencies:** None

---

### US-021: Assign Staff to Shift
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Administrator**,  
I want to **assign staff members to specific shifts**,  
So that **adequate staffing is ensured for all sessions**.

**Acceptance Criteria:**
- [ ] Create shift roster by date range
- [ ] Assign multiple staff to each shift
- [ ] Define roles per shift (Nurse, Technician, etc.)
- [ ] Check staff availability before assignment
- [ ] Handle shift swaps between staff
- [ ] Minimum staffing alerts
- [ ] Print shift roster
- [ ] Staff can view their assigned shifts

**Dependencies:** US-020

---

### US-022: Send Appointment Reminders
**Epic:** EP-02 - Appointment & Scheduling  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Patient**,  
I want to **receive reminders for my upcoming appointments**,  
So that **I don't forget my dialysis sessions**.

**Acceptance Criteria:**
- [ ] SMS reminder sent 24 hours before appointment
- [ ] Email reminder sent with appointment details
- [ ] Reminder includes date, time, machine location
- [ ] Patient can opt-out of reminders
- [ ] Reminders sent only for active appointments
- [ ] Configurable reminder timing (24h, 48h, etc.)
- [ ] Delivery status tracked
- [ ] Multi-language support

**Dependencies:** US-013

**Technical Notes:**
- Integrate SMS gateway
- Configure scheduled job for reminder sending

---

## EPIC 03: Treatment & Clinical

### US-023: Start Dialysis Session
**Epic:** EP-03 - Treatment & Clinical  
**Priority:** Must Have  
**Story Points:** 8

**User Story:**
As a **Nurse**,  
I want to **start a dialysis session for a patient**,  
So that **treatment begins with proper documentation**.

**Acceptance Criteria:**
- [ ] Select appointment or patient to start session
- [ ] Record pre-dialysis weight
- [ ] Record pre-dialysis vital signs (BP, HR, Temp)
- [ ] Inspect and document access site condition
- [ ] Record patient complaints if any
- [ ] Confirm treatment prescription
- [ ] Set session start time automatically
- [ ] Session status changes to "In Progress"
- [ ] Cannot start if pre-dialysis assessment incomplete
- [ ] Session linked to appointment and patient

**Dependencies:** US-013

**Technical Notes:**
- Create Dialysis Session DocType
- Link to Appointment and Patient
- Implement validation workflows

---

### US-024: Record Treatment Prescription
**Epic:** EP-03 - Treatment & Clinical  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Nephrologist**,  
I want to **create and save treatment prescriptions**,  
So that **nurses follow the correct treatment protocol**.

**Acceptance Criteria:**
- [ ] Select dialysis modality (HD, HDF)
- [ ] Set treatment duration (2-5 hours)
- [ ] Define blood flow rate (QB)
- [ ] Define dialysate flow rate (QD)
- [ ] Set ultrafiltration target (UF goal in liters)
- [ ] Select dialyzer type and size
- [ ] Define anticoagulation protocol (heparin dose)
- [ ] Add special instructions
- [ ] Save as template for future use
- [ ] Prescription requires physician approval
- [ ] Version control for prescription changes

**Dependencies:** US-001

---

### US-025: Monitor Intra-Dialysis Vitals
**Epic:** EP-03 - Treatment & Clinical  
**Priority:** Must Have  
**Story Points:** 8

**User Story:**
As a **Nurse**,  
I want to **record patient vitals during dialysis**,  
So that **I can monitor patient safety throughout treatment**.

**Acceptance Criteria:**
- [ ] Record vitals at hourly intervals
- [ ] Capture BP, HR, Temperature
- [ ] Record blood flow rate (QB actual)
- [ ] Record transmembrane pressure (TMP)
- [ ] Record venous pressure
- [ ] Track actual vs target ultrafiltration
- [ ] Log machine alarms and events
- [ ] Document nurse interventions
- [ ] Alert for abnormal vital signs
- [ ] Timeline view of all recordings

**Dependencies:** US-023

---

### US-026: Complete Dialysis Session
**Epic:** EP-03 - Treatment & Clinical  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Nurse**,  
I want to **complete and close a dialysis session**,  
So that **treatment is properly documented and billed**.

**Acceptance Criteria:**
- [ ] Record post-dialysis weight
- [ ] Record post-dialysis vital signs
- [ ] Calculate total fluid removed (actual UF)
- [ ] Assess patient condition at discharge
- [ ] Inspect access site post-treatment
- [ ] Document any complications or adverse events
- [ ] Confirm next appointment
- [ ] Set session end time automatically
- [ ] Session status changes to "Completed"
- [ ] Automatically trigger billing process
- [ ] Generate session summary for patient

**Dependencies:** US-023

---

### US-027: Handle Emergency During Session
**Epic:** EP-03 - Treatment & Clinical  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Nurse**,  
I want to **document emergency situations during dialysis**,  
So that **proper medical response and reporting is ensured**.

**Acceptance Criteria:**
- [ ] Quick "Emergency" button on session screen
- [ ] Select emergency type (Hypotension, Chest Pain, etc.)
- [ ] Record emergency time
- [ ] Document symptoms and interventions
- [ ] Alert physician immediately
- [ ] Record medications administered
- [ ] Document outcome (Resolved, Transferred, etc.)
- [ ] Pause session timer during emergency
- [ ] Generate incident report
- [ ] Flag session for quality review

**Dependencies:** US-023

---

### US-028: Use Treatment Templates
**Epic:** EP-03 - Treatment & Clinical  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Nurse**,  
I want to **load saved treatment templates**,  
So that **I can quickly apply standard prescriptions**.

**Acceptance Criteria:**
- [ ] View list of templates for a patient
- [ ] Select template to apply
- [ ] Template populates all prescription fields
- [ ] Values can be modified before starting session
- [ ] Template includes dialyzer type, flow rates, UF goal
- [ ] Create new template from current prescription
- [ ] Update existing template
- [ ] Templates are physician-approved
- [ ] Template version history maintained

**Dependencies:** US-024

---

### US-029: View Session History
**Epic:** EP-03 - Treatment & Clinical  
**Priority:** Should Have  
**Story Points:** 3

**User Story:**
As a **Nephrologist**,  
I want to **view a patient's complete session history**,  
So that **I can assess treatment effectiveness over time**.

**Acceptance Criteria:**
- [ ] List all sessions for a patient in chronological order
- [ ] Display key metrics (date, duration, UF, Kt/V)
- [ ] Filter by date range
- [ ] Click session to view full details
- [ ] Export history to PDF
- [ ] Show graphs for trends (weight, BP, UF)
- [ ] Highlight sessions with complications
- [ ] Quick statistics (total sessions, average duration)

**Dependencies:** US-023, US-026

---

## EPIC 04: Laboratory Integration

### US-030: Create Lab Order
**Epic:** EP-04 - Laboratory Integration  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Nephrologist**,  
I want to **create lab test orders for patients**,  
So that **required tests are tracked and results can be linked**.

**Acceptance Criteria:**
- [ ] Select patient from dropdown
- [ ] Choose from predefined test panels or individual tests
- [ ] Set priority (Routine, Urgent, STAT)
- [ ] Add clinical notes for lab
- [ ] Order date and time auto-recorded
- [ ] Lab requisition printable with barcode
- [ ] Order status shows as "Ordered"
- [ ] Multiple tests can be ordered together
- [ ] Integration with external LIS (if available)

**Dependencies:** US-001

---

### US-031: Record Lab Results
**Epic:** EP-04 - Laboratory Integration  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Lab Coordinator**,  
I want to **enter lab results into the system**,  
So that **results are available to physicians**.

**Acceptance Criteria:**
- [ ] Search for pending lab orders
- [ ] Enter result values for each test
- [ ] Auto-flag abnormal values based on reference ranges
- [ ] Result date and time recorded
- [ ] Entered by user is logged
- [ ] Order status changes to "Completed"
- [ ] Results immediately visible to physicians
- [ ] Support for importing results from LIS

**Dependencies:** US-030

---

### US-032: View Lab Results Timeline
**Epic:** EP-04 - Laboratory Integration  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Nephrologist**,  
I want to **view lab results over time in a graphical format**,  
So that **I can identify trends in patient parameters**.

**Acceptance Criteria:**
- [ ] Select lab parameter to view (e.g., Creatinine, Hemoglobin)
- [ ] Graph shows values over last 6-12 months
- [ ] Reference range shown on graph
- [ ] Abnormal values highlighted
- [ ] Hover to see exact values and dates
- [ ] Multiple parameters can be plotted together
- [ ] Export graph as image or PDF
- [ ] Zoom and pan functionality

**Dependencies:** US-031

---

### US-033: Calculate Kt/V and URR
**Epic:** EP-04 - Laboratory Integration  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Nephrologist**,  
I want to **automatically calculate dialysis adequacy parameters**,  
So that **I can assess treatment effectiveness**.

**Acceptance Criteria:**
- [ ] Auto-calculate Kt/V using Daugirdas formula
- [ ] Auto-calculate URR from pre and post urea values
- [ ] Input fields for pre-dialysis urea, post-dialysis urea
- [ ] Session duration and blood flow considered
- [ ] Display calculation result with interpretation
- [ ] Flag if Kt/V < 1.2 or URR < 65%
- [ ] Save calculated values with session
- [ ] Trend over multiple sessions

**Dependencies:** US-023, US-031

---

### US-034: Alert for Critical Lab Values
**Epic:** EP-04 - Laboratory Integration  
**Priority:** Should Have  
**Story Points:** 3

**User Story:**
As a **Nephrologist**,  
I want to **receive alerts for critical lab values**,  
So that **I can take immediate action**.

**Acceptance Criteria:**
- [ ] Define critical ranges for each lab parameter
- [ ] Automatic alert when result enters critical range
- [ ] Email notification to assigned physician
- [ ] Alert shown on dashboard
- [ ] Alert requires acknowledgment
- [ ] Patient flagged in system until addressed
- [ ] Alert history maintained

**Dependencies:** US-031

---

## EPIC 05: Inventory Management

### US-035: Add Inventory Item
**Epic:** EP-05 - Inventory Management  
**Priority:** Must Have  
**Story Points:** 3

**User Story:**
As an **Inventory Manager**,  
I want to **add new items to inventory master**,  
So that **stock can be tracked**.

**Acceptance Criteria:**
- [ ] Item code auto-generated or manual
- [ ] Item name and description
- [ ] Category selection (Dialyzer, Medication, Consumable, etc.)
- [ ] Unit of measure
- [ ] Reorder level and maximum stock level
- [ ] Default supplier can be set
- [ ] Item can be marked as active/inactive
- [ ] Duplicate item code prevented

**Dependencies:** None

---

### US-036: Record Stock Receipt
**Epic:** EP-05 - Inventory Management  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As an **Inventory Manager**,  
I want to **record goods received from suppliers**,  
So that **stock levels are updated accurately**.

**Acceptance Criteria:**
- [ ] Select supplier from list
- [ ] Add multiple items in one receipt
- [ ] Enter quantity received per item
- [ ] Record batch/lot number
- [ ] Record expiry date
- [ ] Record purchase price
- [ ] Upload delivery note/invoice
- [ ] Stock balance updates immediately
- [ ] Receipt can be printed
- [ ] Link to purchase order (if exists)

**Dependencies:** US-035

---

### US-037: Issue Stock for Session
**Epic:** EP-05 - Inventory Management  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Nurse**,  
I want to **issue consumables for a dialysis session**,  
So that **usage is tracked and billed**.

**Acceptance Criteria:**
- [ ] Select patient/session
- [ ] Add items used (dialyzer, bloodlines, needles, etc.)
- [ ] Quantity defaults to 1, can be changed
- [ ] Batch selection with expiry visibility
- [ ] Stock balance checks before issuing
- [ ] Out of stock items flagged
- [ ] Issuance linked to session
- [ ] Stock balance reduced immediately
- [ ] Usage tracked for billing

**Dependencies:** US-023, US-036

---

### US-038: View Stock Levels
**Epic:** EP-05 - Inventory Management  
**Priority:** Must Have  
**Story Points:** 3

**User Story:**
As an **Inventory Manager**,  
I want to **view current stock levels for all items**,  
So that **I know what needs reordering**.

**Acceptance Criteria:**
- [ ] List all items with current quantity
- [ ] Show reorder level and max level
- [ ] Items below reorder level highlighted in red
- [ ] Filter by category
- [ ] Search by item name or code
- [ ] Show items expiring in next 30/60/90 days
- [ ] Export to Excel
- [ ] Refresh data in real-time

**Dependencies:** US-035, US-036

---

### US-039: Generate Stock Alerts
**Epic:** EP-05 - Inventory Management  
**Priority:** Should Have  
**Story Points:** 3

**User Story:**
As an **Inventory Manager**,  
I want to **receive automated alerts for low stock and expiry**,  
So that **I can take timely action**.

**Acceptance Criteria:**
- [ ] Email alert when item reaches reorder level
- [ ] Daily summary of items below reorder level
- [ ] Alert for items expiring in 30 days
- [ ] Alert for items expiring in 7 days
- [ ] Dashboard widget showing alerts count
- [ ] Alerts can be acknowledged/dismissed
- [ ] Alert history maintained

**Dependencies:** US-035, US-036

---

### US-040: Create Purchase Request
**Epic:** EP-05 - Inventory Management  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As an **Inventory Manager**,  
I want to **create purchase requisitions for low stock items**,  
So that **procurement is initiated**.

**Acceptance Criteria:**
- [ ] Auto-suggest items below reorder level
- [ ] Add items manually
- [ ] Specify quantity to order
- [ ] Select preferred supplier
- [ ] Add justification/notes
- [ ] Submit for approval
- [ ] Approval workflow (Manager → Director)
- [ ] Approved requests converted to purchase orders
- [ ] Track status of request

**Dependencies:** US-038

---

## EPIC 06: Equipment Management

### US-041: Register Dialysis Machine
**Epic:** EP-06 - Equipment Management  
**Priority:** Must Have  
**Story Points:** 3

**User Story:**
As an **Administrator**,  
I want to **register dialysis machines in the system**,  
So that **they can be tracked and scheduled**.

**Acceptance Criteria:**
- [ ] Machine ID/serial number
- [ ] Manufacturer and model
- [ ] Installation date
- [ ] Warranty expiry date
- [ ] Location/station assignment
- [ ] Current status (Operational, Maintenance, Out of Service)
- [ ] Machine specifications (type, capabilities)
- [ ] Upload machine manual/documentation

**Dependencies:** None

---

### US-042: Schedule Machine Maintenance
**Epic:** EP-06 - Equipment Management  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Technician**,  
I want to **schedule preventive maintenance for machines**,  
So that **equipment reliability is maintained**.

**Acceptance Criteria:**
- [ ] Select machine
- [ ] Choose maintenance type (Daily, Weekly, Monthly, Annual)
- [ ] Set maintenance date and time
- [ ] Assign technician
- [ ] Machine blocked from scheduling during maintenance
- [ ] Maintenance checklist template loaded
- [ ] Recurring maintenance can be set
- [ ] Reminder sent before due date

**Dependencies:** US-041

---

### US-043: Record Maintenance Activity
**Epic:** EP-06 - Equipment Management  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Technician**,  
I want to **record completed maintenance activities**,  
So that **maintenance history is documented**.

**Acceptance Criteria:**
- [ ] Select scheduled maintenance
- [ ] Complete checklist items
- [ ] Record findings and observations
- [ ] Document parts replaced
- [ ] Upload photos if needed
- [ ] Record technician and completion time
- [ ] Machine status updated after maintenance
- [ ] Generate maintenance report
- [ ] Next maintenance date calculated

**Dependencies:** US-042

---

### US-044: Track Machine Utilization
**Epic:** EP-06 - Equipment Management  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Medical Director**,  
I want to **view machine utilization reports**,  
So that **I can optimize resource allocation**.

**Acceptance Criteria:**
- [ ] Report by machine showing usage hours
- [ ] Number of sessions per machine
- [ ] Utilization percentage calculation
- [ ] Downtime tracking with reasons
- [ ] Filter by date range
- [ ] Compare utilization across machines
- [ ] Export to Excel/PDF
- [ ] Visual charts and graphs

**Dependencies:** US-041, US-023

---

## EPIC 07: Billing & Finance

### US-045: Generate Patient Bill
**Epic:** EP-07 - Billing & Finance  
**Priority:** Must Have  
**Story Points:** 8

**User Story:**
As a **Billing Officer**,  
I want to **generate bills for completed dialysis sessions**,  
So that **patients can be invoiced**.

**Acceptance Criteria:**
- [ ] Auto-generate bill after session completion
- [ ] Itemized charges (session fee, consumables, medications)
- [ ] Apply patient's pricing tier
- [ ] Apply package rates if applicable
- [ ] Calculate taxes if applicable
- [ ] Show total amount due
- [ ] Bill number auto-generated
- [ ] Bill date and due date
- [ ] Professional invoice format
- [ ] Print or email bill to patient

**Dependencies:** US-026, US-037

---

### US-046: Record Payment
**Epic:** EP-07 - Billing & Finance  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Billing Officer**,  
I want to **record payments received from patients**,  
So that **accounts are updated**.

**Acceptance Criteria:**
- [ ] Select patient and outstanding bills
- [ ] Enter payment amount
- [ ] Select payment mode (Cash, Card, Transfer, etc.)
- [ ] Record transaction reference
- [ ] Payment date auto-recorded
- [ ] Generate receipt with unique number
- [ ] Outstanding balance updated
- [ ] Partial payments supported
- [ ] Overpayment recorded as advance
- [ ] Receipt printable

**Dependencies:** US-045

---

### US-047: Manage Insurance Claims
**Epic:** EP-07 - Billing & Finance  
**Priority:** Must Have  
**Story Points:** 8

**User Story:**
As a **Billing Officer**,  
I want to **submit and track insurance claims**,  
So that **reimbursement is obtained**.

**Acceptance Criteria:**
- [ ] Patient insurance details linked to profile
- [ ] Pre-authorization request creation
- [ ] Claim form generation with required details
- [ ] Attach supporting documents
- [ ] Submit claim to insurance company
- [ ] Track claim status (Submitted, Under Review, Approved, Rejected, Paid)
- [ ] Record approval amount
- [ ] Handle partial approvals
- [ ] Link payment received to claim
- [ ] Claim history per patient

**Dependencies:** US-001, US-045

---

### US-048: Apply Discounts
**Epic:** EP-07 - Billing & Finance  
**Priority:** Should Have  
**Story Points:** 3

**User Story:**
As a **Billing Officer**,  
I want to **apply discounts to patient bills**,  
So that **special pricing can be offered**.

**Acceptance Criteria:**
- [ ] Discount percentage or fixed amount
- [ ] Discount reason mandatory
- [ ] Approval required for discounts > 10%
- [ ] Discount reflected on bill
- [ ] Discount tracked in reports
- [ ] Cannot exceed maximum discount limit

**Dependencies:** US-045

---

### US-049: View Outstanding Receivables
**Epic:** EP-07 - Billing & Finance  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As a **Billing Officer**,  
I want to **view all outstanding patient balances**,  
So that **I can follow up on collections**.

**Acceptance Criteria:**
- [ ] List all patients with outstanding balance
- [ ] Show total outstanding per patient
- [ ] Aging analysis (0-30, 31-60, 61-90, 90+ days)
- [ ] Sort by amount or aging
- [ ] Filter by insurance type or payment mode
- [ ] Send payment reminder from list
- [ ] Export to Excel
- [ ] Total receivables summary

**Dependencies:** US-045, US-046

---

## EPIC 08: Staff Management

### US-050: Add Staff Member
**Epic:** EP-08 - Staff Management  
**Priority:** Must Have  
**Story Points:** 3

**User Story:**
As an **Administrator**,  
I want to **add staff members to the system**,  
So that **they can be assigned to shifts and sessions**.

**Acceptance Criteria:**
- [ ] Staff ID auto-generated
- [ ] Personal details (name, DOB, contact)
- [ ] Professional credentials (license number, certifications)
- [ ] Designation and department
- [ ] Join date and employment type
- [ ] Upload photo
- [ ] Emergency contact information
- [ ] Create user account with role assignment
- [ ] Active/Inactive status

**Dependencies:** None

---

### US-051: View Staff Schedule
**Epic:** EP-08 - Staff Management  
**Priority:** Should Have  
**Story Points:** 3

**User Story:**
As a **Staff Member**,  
I want to **view my assigned shifts and sessions**,  
So that **I know my work schedule**.

**Acceptance Criteria:**
- [ ] Calendar view of assigned shifts
- [ ] List of patients assigned
- [ ] Shift timings clearly shown
- [ ] Mobile-friendly view
- [ ] Filter by date range
- [ ] Export schedule to calendar app
- [ ] Notifications for schedule changes

**Dependencies:** US-021, US-050

---

### US-052: Track Staff Performance
**Epic:** EP-08 - Staff Management  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Medical Director**,  
I want to **track staff performance metrics**,  
So that **I can provide feedback and recognition**.

**Acceptance Criteria:**
- [ ] Number of sessions handled per staff
- [ ] Patient feedback scores
- [ ] Incident reports count
- [ ] Training completion percentage
- [ ] Attendance and punctuality
- [ ] Performance trends over time
- [ ] Export performance report
- [ ] Comparison across staff members

**Dependencies:** US-050, US-023

---

## EPIC 09: Reporting & Analytics

### US-053: View Executive Dashboard
**Epic:** EP-09 - Reporting & Analytics  
**Priority:** Must Have  
**Story Points:** 8

**User Story:**
As a **Medical Director**,  
I want to **see key performance indicators on a dashboard**,  
So that **I can monitor center performance at a glance**.

**Acceptance Criteria:**
- [ ] Total active patients count
- [ ] Today's sessions (completed/scheduled)
- [ ] This month's revenue
- [ ] Machine utilization percentage
- [ ] Outstanding receivables total
- [ ] Quality metrics (Kt/V achievement, infection rate)
- [ ] Recent alerts and notifications
- [ ] Graphical widgets for trends
- [ ] Auto-refresh every 5 minutes
- [ ] Customizable layout

**Dependencies:** Multiple (US-001, US-023, US-045)

---

### US-054: Generate Monthly Clinical Report
**Epic:** EP-09 - Reporting & Analytics  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **Medical Director**,  
I want to **generate monthly clinical quality reports**,  
So that **I can track compliance with clinical standards**.

**Acceptance Criteria:**
- [ ] Select month and year
- [ ] Total sessions conducted
- [ ] Dialysis adequacy (% patients with Kt/V > 1.2)
- [ ] Anemia management (% patients in target Hb range)
- [ ] Vascular access statistics
- [ ] Incident and complication rates
- [ ] Patient hospitalizations
- [ ] Export to PDF
- [ ] Compare with previous months

**Dependencies:** US-023, US-031

---

### US-055: Export Data to Excel
**Epic:** EP-09 - Reporting & Analytics  
**Priority:** Should Have  
**Story Points:** 3

**User Story:**
As a **User**,  
I want to **export any report or list to Excel**,  
So that **I can perform additional analysis**.

**Acceptance Criteria:**
- [ ] Export button available on all list views
- [ ] Export includes all columns shown in view
- [ ] Export respects current filters
- [ ] File downloads immediately
- [ ] File named appropriately (with date/time)
- [ ] Large datasets handled efficiently
- [ ] Excel file formatted properly

**Dependencies:** None

---

## EPIC 10: Security & Compliance

### US-056: Manage User Roles
**Epic:** EP-10 - Security & Compliance  
**Priority:** Must Have  
**Story Points:** 5

**User Story:**
As an **Administrator**,  
I want to **assign roles and permissions to users**,  
So that **data access is controlled**.

**Acceptance Criteria:**
- [ ] Predefined roles (Admin, Doctor, Nurse, etc.)
- [ ] Assign one or multiple roles to user
- [ ] Role defines access to modules
- [ ] Role defines create/read/update/delete permissions
- [ ] Custom roles can be created
- [ ] Permission changes take effect immediately
- [ ] Audit log of role changes

**Dependencies:** None

---

### US-057: View Audit Trail
**Epic:** EP-10 - Security & Compliance  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As an **Administrator**,  
I want to **view complete audit trail of system activities**,  
So that **I can ensure accountability and compliance**.

**Acceptance Criteria:**
- [ ] Log all create, update, delete operations
- [ ] Capture user, timestamp, action
- [ ] Show before and after values
- [ ] Filter by user, date, document type
- [ ] Search audit logs
- [ ] Export audit trail
- [ ] Tamper-proof storage
- [ ] Retention for minimum 7 years

**Dependencies:** None

---

## EPIC 11: Communication

### US-058: Send SMS Notification
**Epic:** EP-11 - Communication  
**Priority:** Should Have  
**Story Points:** 5

**User Story:**
As a **System**,  
I want to **send SMS notifications to patients and staff**,  
So that **important information is communicated quickly**.

**Acceptance Criteria:**
- [ ] SMS for appointment reminders
- [ ] SMS for payment reminders
- [ ] SMS for lab results ready
- [ ] SMS for urgent alerts
- [ ] SMS delivery status tracking
- [ ] SMS templates configurable
- [ ] Multi-language support
- [ ] Opt-out mechanism

**Dependencies:** SMS gateway integration

---

## EPIC 12: System Administration

### US-059: Configure Multi-Location
**Epic:** EP-12 - System Administration  
**Priority:** Should Have  
**Story Points:** 8

**User Story:**
As an **Administrator**,  
I want to **configure multiple dialysis center locations**,  
So that **all centers can use one system**.

**Acceptance Criteria:**
- [ ] Add new location with name and address
- [ ] Location-specific configuration
- [ ] Assign machines to location
- [ ] Assign staff to location
- [ ] Location-wise inventory
- [ ] Consolidated reporting across locations
- [ ] Data isolation between locations
- [ ] User access control by location

**Dependencies:** None

---

## Sprint Planning Reference

### Suggested Sprint Breakdown (2-week sprints)

**Sprint 1-2: Foundation**
- US-001, US-002, US-003, US-005, US-008 (Patient Management basics)
- US-056 (User roles)

**Sprint 3-4: Scheduling**
- US-013, US-015, US-016, US-017, US-018 (Appointment management)
- US-041 (Machine registry)

**Sprint 5-6: Clinical Core**
- US-023, US-024, US-025, US-026 (Session management)
- US-030, US-031 (Lab basics)

**Sprint 7-8: Billing**
- US-045, US-046, US-047 (Billing basics)
- US-035, US-036, US-037, US-038 (Inventory basics)

**Sprint 9-10: Analytics & Polish**
- US-053, US-054, US-055 (Reporting)
- US-014, US-022 (Advanced scheduling)
- US-058 (SMS notifications)

---

## Story Point Summary by Epic

| Epic | Must Have | Should Have | Could Have | Total Points |
|------|-----------|-------------|------------|--------------|
| EP-01: Patient Management | 26 | 18 | 5 | 49 |
| EP-02: Appointment & Scheduling | 32 | 20 | 0 | 52 |
| EP-03: Treatment & Clinical | 31 | 8 | 0 | 39 |
| EP-04: Laboratory | 15 | 13 | 0 | 28 |
| EP-05: Inventory | 16 | 8 | 0 | 24 |
| EP-06: Equipment | 13 | 5 | 0 | 18 |
| EP-07: Billing | 21 | 3 | 0 | 24 |
| EP-08: Staff | 6 | 8 | 0 | 14 |
| EP-09: Reporting | 8 | 8 | 0 | 16 |
| EP-10: Security | 5 | 5 | 0 | 10 |
| EP-11: Communication | 0 | 5 | 0 | 5 |
| EP-12: System Admin | 0 | 8 | 0 | 8 |

**Total Story Points: 287** (approximately 6-8 months for a team of 3-4 developers)

---

**End of User Stories Document**

*Note: This document should be maintained in a project management tool (Jira, Azure DevOps, etc.) for active sprint planning and tracking.*
