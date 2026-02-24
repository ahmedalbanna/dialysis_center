# User Guides - Part 1: Patient & Appointment Management
## Dialysis Center Management System

**Last Updated**: February 19, 2026  
**Version**: 1.0.0

---

## 1. Patient Management Guide

### Overview
The Patient Management module handles all patient-related operations including registration, medical history, and patient information updates.

### 1.1 Registering a New Patient

**Step 1: Navigate to Patient List**
1. Click "Patient Management" in sidebar
2. Click "Patient" or "New Patient"
3. You'll see the Patient form

**Step 2: Fill Patient Information**
- **Name** (Auto-generated): System generates unique ID like PT-001
- **First Name**: Patient's first name (Required)
- **Last Name**: Patient's last name
- **Date of Birth**: Select from calendar (Required)
- **Gender**: Select Male/Female/Other (Required)
- **Contact Number**: Primary phone number (Required)
- **Email**: Patient's email address (Required)
- **Address**: Full residential address
- **City**: City name
- **State/Province**: Region/state
- **Postal Code**: ZIP code
- **Country**: Country name

**Step 3: Medical Information**
- **Blood Type**: Select O+, O-, A+, A-, B+, B-, AB+, AB-
- **Allergies**: List any known allergies (comma-separated)
- **Comorbidities**: Existing medical conditions (e.g., Diabetes, Hypertension)
- **Current Medications**: List current medications
- **Insurance Provider**: Select from available providers (if using insurance)
- **Insurance ID**: Insurance policy number
- **Emergency Contact Name**: Contact person name
- **Emergency Contact Number**: Contact phone number

**Step 4: Dialysis-Specific Information**
- **Vascular Access Type**: Fistula / Graft / Catheter / Other
- **Vascular Access Location**: Arm / Leg / Neck / Chest
- **Access Creation Date**: Date vascular access was created
- **Dialysis Frequency**: 2x/week, 3x/week, or custom schedule
- **Session Duration**: Default 240 minutes (4 hours)
- **Target Dry Weight**: Patient's ideal body weight in kg
- **Nephrologist**: Assign responsible nephrologist
- **Dialysis Technician**: Assign primary technician

**Step 5: Save Patient Record**
1. Click "Save" button (Ctrl+S)
2. System confirms patient created
3. You'll see patient details page
4. Print registration form if needed (Print button)

### 1.2 Updating Patient Information

**Quick Edit**:
1. Open patient record
2. Click "Edit" button
3. Update fields
4. Click "Save"

**Add Medical History**:
1. Open patient record
2. Scroll to "Medical History" section
3. Click "Add Row"
4. Enter: Date, Condition, Treatment, Notes
5. Click "Save"

**Update Contact Information**:
1. Open patient record
2. Find "Contact Information" section
3. Edit phone, email, address
4. Click "Save"

### 1.3 Managing Patient Documents

**Upload Documents**:
1. Open patient record
2. Click "Attachments" section
3. Click "Add" button
4. Select file (PDF, image, document)
5. Drag and drop or browse
6. Document attached to patient record

**Supported Document Types**:
- Medical reports
- Test results
- Prescriptions
- Insurance documents
- Lab reports
- X-rays / scans

### 1.4 Viewing Patient Dashboard

**Access Dashboard**:
1. Open patient record
2. Click "Dashboard" tab
3. View real-time information:
   - Patient overview (basic info)
   - Upcoming appointments
   - Recent dialysis sessions
   - Lab test results
   - Billing summary
   - Vital signs trends

### 1.5 Searching & Filtering Patients

**Search by Name**:
1. Go to Patient list
2. Enter name in search box
3. Results update in real-time

**Filter by Criteria**:
1. Go to Patient list
2. Click "Filter" button
3. Select filter field:
   - Blood Type
   - Gender
   - Vascular Access Type
   - Dialysis Frequency
4. Click "Apply"

**Export Patient List**:
1. Go to Patient list
2. Click "Menu" (three dots)
3. Select "Export"
4. Choose CSV or Excel format
5. Download file

### 1.6 Patient Privacy & Compliance

**View Access Log**:
1. Open patient record
2. Click "Timeline" tab
3. See all access and modifications

**Change Sharing**:
1. Open patient record
2. Click "Share" button
3. Add users/roles
4. Set permission level (Read/Write)
5. Save

---

## 2. Appointment Scheduling Guide

### Overview
Appointment Scheduling manages patient appointments for dialysis sessions, consultations, and follow-ups.

### 2.1 Creating a New Appointment

**Method 1: From Appointment List**
1. Go to "Appointment Scheduling" > "Appointment"
2. Click "New Appointment"
3. Fill appointment form (see details below)

**Method 2: From Patient Record**
1. Open patient record
2. Scroll to "Appointments" section
3. Click "Add Row" in child table
4. Or click "New Appointment" button
5. Patient auto-filled

**Appointment Form - Required Fields**:
- **Patient**: Select patient (auto-complete search)
- **Appointment Type**: Dialysis / Consultation / Lab Test / Follow-up
- **Appointment Date**: Select date from calendar
- **Start Time**: HH:MM format (e.g., 08:00)
- **End Time**: HH:MM format (e.g., 12:00)
- **Status**: Draft (auto-set, change after confirmation)

**Optional Fields**:
- **Assigned To**: Assign to specific technician
- **Room/Machine**: Assign specific dialysis machine
- **Notes**: Special instructions or patient notes
- **Patient Contact**: Confirmed phone number
- **Reminder Sent**: System tracks reminders

### 2.2 Checking Available Slots

**Method 1: Calendar View**
1. Go to Appointment Scheduling > Calendar
2. View all appointments by date
3. Green slots = Available
4. Red slots = Booked

**Method 2: Machine Availability**
1. Go to Equipment Management > Dialysis Machine
2. Click specific machine
3. View Schedule tab
4. Check availability for date range

**Method 3: Staff Availability**
1. Go to Staff Management > Staff
2. Click staff member
3. View Availability tab
4. See busy and available times

### 2.3 Confirming Appointments

**From Appointment**:
1. Open appointment record
2. Click "Confirm" button
3. System updates status to "Confirmed"
4. Confirmation email sent to patient
5. SMS reminder scheduled (if configured)

**Bulk Confirmation**:
1. Go to Appointment list
2. Filter by Status = "Draft"
3. Select multiple appointments (checkbox)
4. Click "Confirm All" action
5. System confirms all selected

### 2.4 Rescheduling Appointments

**Single Appointment**:
1. Open appointment
2. Click "Reschedule" button
3. System shows available slots
4. Select new date/time
5. Click "Save"
6. Notification sent to patient

**Patient-Requested Changes**:
1. Patient calls/emails
2. Open appointment
3. Change date/time fields
4. Add note: "Patient requested reschedule"
5. Save
6. Confirmation sent

### 2.5 Canceling Appointments

**Cancel Appointment**:
1. Open appointment
2. Click "Cancel" button
3. Provide reason (optional):
   - Patient no-show
   - Medical reason
   - Patient request
   - Staff unavailable
4. Confirm cancellation
5. Notification sent to patient

**Impact of Cancellation**:
- Machine freed up for other patients
- Staff marked as available
- Patient can be rescheduled
- Record retained for audit trail

### 2.6 Managing Recurring Appointments

**Create Recurring Schedule** (e.g., every Tuesday/Thursday/Saturday):
1. Go to "Recurring Appointment"
2. Click "New Recurring Appointment"
3. Fill form:
   - **Patient**: Select
   - **Appointment Type**: Dialysis
   - **Day of Week**: Tuesday, Thursday, Saturday
   - **Start Time**: 08:00
   - **Duration**: 240 minutes
   - **Valid From**: Start date
   - **Valid To**: End date (or ongoing)
4. Click "Save"
5. System auto-generates appointments

**Modify Recurring Schedule**:
1. Open Recurring Appointment
2. Change day/time
3. Click "Save"
4. Option to apply to:
   - This appointment only
   - This and future appointments
   - All appointments in series

### 2.7 Viewing Appointment Calendar

**Calendar Features**:
1. Go to Calendar view
2. Navigate months with arrows
3. Color-coded by type:
   - Blue = Dialysis
   - Green = Consultation
   - Orange = Lab Test
   - Red = Follow-up
4. Click appointment to view details
5. Drag to reschedule (if enabled)

**Filter Calendar**:
1. Click "Filter" in calendar
2. Select:
   - Patient
   - Appointment Type
   - Status
3. View filtered calendar

### 2.8 No-Show Tracking

**Mark Patient as No-Show**:
1. Open appointment (day after scheduled)
2. Click "Mark as No-Show"
3. Reason: Select from dropdown
4. Add notes if needed
5. System records no-show

**View No-Show Trends**:
1. Go to Reports > Patient No-Show Report
2. Filter by date range
3. View:
   - Number of no-shows
   - % no-show rate
   - Patients with pattern
4. Export for follow-up action

### 2.9 Reminders & Notifications

**Automatic Reminders**:
- 24 hours before: SMS/Email sent
- 2 hours before: SMS sent
- Configurable in Settings

**Manual Reminder**:
1. Open appointment
2. Click "Send Reminder"
3. Choose: SMS / Email / Both
4. Confirmation shown
5. Activity logged

---

**Next Section**: Dialysis Operations & Billing Guides (Part 2)

