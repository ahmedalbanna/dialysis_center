# User Guides - Part 3: Laboratory, Equipment & Staff Management
## Dialysis Center Management System

**Last Updated**: February 19, 2026  
**Version**: 1.0.0

---

## 5. Laboratory Management Guide

### Overview
Laboratory Management handles patient test orders, result tracking, and lab data integration.

### 5.1 Creating Lab Test Orders

**From Patient Record**:
1. Open patient record
2. Click "Lab Tests" tab
3. Click "Add Row" in Lab Tests section
4. Select **Test Type**:
   - Complete Blood Count (CBC)
   - Comprehensive Metabolic Panel (CMP)
   - Electrolytes (K, Na, Cl, CO2)
   - Kidney Function (Creatinine, BUN, eGFR)
   - Bone Panel (Calcium, Phosphate, Magnesium)
   - Lipid Panel
   - Coagulation Studies (PT, PTT)
5. Set **Frequency**:
   - Once
   - Weekly
   - Monthly
   - Quarterly
   - As needed
6. Click "Save"

**From Dialysis Session**:
1. Open completed Dialysis Session
2. Click "Create" > "Lab Test"
3. Session auto-linked
4. Select test type
5. System notes: "Post-dialysis sample"
6. Assign to lab

**Standalone Lab Test Order**:
1. Go to "Laboratory Management" > "Lab Test"
2. Click "New Lab Test"
3. Fill form:
   - **Patient**: Select
   - **Test Template**: Select from predefined templates
   - **Ordered By**: Doctor/Nephrologist
   - **Order Date**: Today
   - **Collection Date**: When sample collected
   - **Specimen Type**: Blood/Urine/Other
   - **Urgent**: Yes/No (affects priority)
   - **Clinical Indication**: Reason for test

### 5.2 Managing Lab Test Templates

**Using Predefined Templates**:
1. Templates include standard test panels:
   - Monthly Dialysis Panel (K, Creatinine, Calcium, etc.)
   - Quarterly Extended Panel
   - PRN (as needed) tests

**Create Custom Template** (Admin only):
1. Go to "Lab Test Template"
2. Click "New Template"
3. Enter:
   - **Template Name**: e.g., "Pre-Transplant Workup"
   - **Description**: Purpose
   - Add tests by clicking "Add Row"
   - Select each test parameter
4. Save template
5. Available for future orders

### 5.3 Specimen Collection & Tracking

**Collect Specimen**:
1. Identify patient (ID bracelet)
2. Collect sample:
   - Blood: Specific tube color per test
   - Urine: Clean-catch or 24-hour
   - Other: Per protocol
3. Label with:
   - Patient name
   - Date/time collected
   - Collector initials
4. Transport immediately to lab

**Mark as Collected**:
1. Open lab test order
2. Click "Mark as Collected"
3. Enter:
   - **Collection Time**: Exact time
   - **Collected By**: Staff member
   - **Comments**: Any issues?
4. Status changes to "Collected"
5. System notifies lab

### 5.4 Entering Lab Results

**Option 1: Manual Entry**:
1. Open lab test order (Collected status)
2. Click "Enter Results"
3. For each parameter:
   - **Value**: Numeric result
   - **Unit**: Per test (mg/dL, mEq/L, etc.)
   - **Status**: Normal/Low/High
   - System shows reference range
4. Click "Save Results"
5. Status changes to "Completed"

**Option 2: Import from Lab System**:
1. Lab system exports CSV/HL7
2. Go to Lab Test > Import
3. Upload file
4. System matches by patient/test
5. Auto-populates results
6. Verify accuracy before saving

**Results Review**:
1. Nephrologist reviews results
2. Verifies against reference ranges
3. Notes abnormalities
4. Adds clinical interpretation
5. May order follow-up tests

### 5.5 Viewing Lab Results

**In Patient Record**:
1. Open patient
2. Click "Lab Results" tab
3. View results by date
4. Click to expand result details
5. See values, reference ranges, status flags

**Lab Results Dashboard**:
1. Go to Reports > Patient Lab Results
2. Select patient
3. View results over time (table/graph)
4. Track trends in potassium, creatinine, etc.
5. Identify patterns requiring intervention

**Export Lab Data**:
1. Go to Lab Test list
2. Filter by patient/date range
3. Click "Export"
4. Choose CSV/Excel
5. Use for external provider sharing

### 5.6 Critical Values & Alerts

**Automatic Alerts**:
- System alerts if critical value detected
- Critical ranges:
  - Potassium > 6.5 or < 3.0 mEq/L
  - Glucose < 70 or > 300 mg/dL
  - Hemoglobin < 7 or > 18 g/dL
  - Creatinine > 10 mg/dL
- Alert: Email/SMS to nephrologist and technician
- Must be acknowledged in system

**Manual Flag**:
1. If critical value detected manually
2. Click "Mark Critical"
3. Reason/notes
4. Notify: Select recipients
5. System sends notification immediately

### 5.7 Trending & Analysis

**View Patient Trends**:
1. Open patient record
2. Click "Lab Trends" or Dashboard
3. Graphs show:
   - Potassium over 6 months
   - Creatinine trend
   - Hemoglobin trend
   - Calcium/Phosphate ratio
4. Identify improving/declining trends
5. Adjust treatment if needed

**Generate Trend Report**:
1. Go to Reports > Lab Trend Analysis
2. Select patient, date range
3. Select parameters to analyze
4. System generates:
   - Line graphs
   - Summary statistics
   - Variance from target
   - Recommendations
5. Use for clinical decision-making

---

## 6. Equipment Management Guide

### Overview
Equipment Management tracks dialysis machines, maintenance, and equipment availability.

### 6.1 Viewing Equipment Status

**Machine Inventory**:
1. Go to "Equipment Management" > "Dialysis Machine"
2. View all machines with status:
   - Green = Available/Functional
   - Yellow = Maintenance scheduled
   - Red = Out of service
   - Blue = In use (current patient)
3. Click machine for details

**Machine Details**:
- **Machine Name**: ID (e.g., "M-001")
- **Model**: Manufacturer and model
- **Serial Number**: For tracking
- **Installed Date**: When put into service
- **Status**: Active/Inactive/Maintenance/Decommissioned
- **Water System**: Linked water purification
- **Dialysate System**: Dialysate preparation

### 6.2 Machine Schedule & Availability

**View Weekly Schedule**:
1. Open machine record
2. Click "Schedule" tab
3. See booked appointments by day
4. Green time slots = Available
5. Blue time slots = Booked
6. Drag to reschedule (if enabled)

**Check Availability for Date**:
1. Go to Equipment Management > Machine Availability
2. Enter date range
3. Select machines
4. System shows:
   - Booked time slots
   - Available slots
   - Maintenance windows
5. Use to schedule appointments

### 6.3 Maintenance Scheduling & Logging

**View Maintenance Schedule**:
1. Open machine record
2. Click "Maintenance" tab
3. View scheduled maintenance:
   - Preventive maintenance dates
   - Service history
   - Last calibration
   - Next scheduled service

**Schedule Maintenance**:
1. Click "Schedule Maintenance" button
2. Enter:
   - **Type**: Preventive / Repair / Calibration / Inspection
   - **Date**: When needed
   - **Duration**: How long (2-4 hours typical)
   - **Reason/Notes**: Specific work needed
   - **Technician**: Assign responsible person
3. Click "Save"
4. Machine marked unavailable during maintenance

**Log Maintenance Completion**:
1. After maintenance done
2. Click "Log Maintenance Completion"
3. Enter:
   - **Completion Date/Time**: When finished
   - **Work Performed**: Description of work
   - **Parts Replaced**: Any components changed
   - **Test Results**: Function tests passed?
   - **Next Service Due**: Schedule follow-up if needed
   - **Cost**: Parts + labor (for budgeting)
4. Click "Save"
5. Machine status returns to Available (if cleared)

### 6.4 Machine Performance Tracking

**Track Machine Alarms**:
1. System logs all machine alarms during sessions
2. View by:
   - Going to machine record
   - Click "Alarms" tab
   - See alarm history by date
   - Alarm type, frequency, resolution

**Common Alarms & Actions**:
- **Low Pressure**: Check blood line, access
- **High Pressure**: Possible clotting, flush line
- **Temperature**: Machine cooling system issue
- **Conductivity**: Dialysate preparation problem
- **Ultrafiltration**: Flow rate issue

**Monitor Reliability**:
1. Open machine record
2. Click "Performance" tab
3. View:
   - Total session hours
   - Number of unplanned stoppages
   - Mean time between failures (MTBF)
   - Maintenance cost YTD
4. If reliability declining: Schedule major service

### 6.5 Water & Dialysate Systems

**Water System Status**:
1. Go to Equipment Management > Water System
2. View:
   - Reverse osmosis machine status
   - Filter status & age
   - Water quality parameters
   - Last servicing date

**Schedule Water System Maintenance**:
1. Note: Water system maintenance per manufacturer (e.g., every 3 months)
2. Click "Schedule Water Maintenance"
3. Maintain production schedule around maintenance
4. Test water quality after service (conductivity, microbial count)

**Dialysate Preparation**:
1. View dialysate mixing system status
2. Check concentrate availability
3. Monitor concentrate usage
4. Reorder when inventory low
5. Note expiration dates on concentrate

### 6.6 Equipment Decommissioning

**When Machine Reaches End of Life**:
1. Open machine record
2. Click "Decommission"
3. Enter:
   - **Decommission Date**: When taken out of service
   - **Reason**: Age/Repair cost/Upgrade
   - **Final Status**: Archive/Dispose/Donate
   - **Notes**: Any special handling?
4. Click "Save"
5. Machine no longer available for scheduling
6. Retained in records for audit trail

### 6.7 Equipment Inventory

**View Equipment Supplies**:
1. Go to Inventory Management > Equipment Supplies
2. Track:
   - Dialyzers (stock level)
   - Blood lines (arterial/venous)
   - Needles (various gauges)
   - Saline bags
   - Anticoagulants
   - Concentrates
3. Set reorder points
4. System alerts when stock low

**Reorder Equipment**:
1. When inventory below reorder point
2. Go to Purchase Order
3. Select supplier
4. Add items and quantities
5. Submit for approval
6. Track delivery

---

## 7. Staff Management Guide

### Overview
Staff Management handles employee information, schedules, and certifications.

### 7.1 Staff Directory

**View All Staff**:
1. Go to "Staff Management" > "Staff"
2. View staff list with:
   - Name
   - Title/Role (Technician, Nephrologist, Nurse)
   - Department
   - Contact info
   - Status (Active/Inactive)

**Staff Details**:
1. Click staff member
2. View:
   - Personal information
   - Contact details
   - Employment details
   - Certifications & licenses
   - Schedule
   - Assigned patients/shifts
   - Performance metrics

### 7.2 Staff Scheduling

**View Staff Schedule**:
1. Open staff member record
2. Click "Schedule" tab
3. View weekly/monthly schedule
4. Shifts shown by color/time block

**Create Shift**:
1. Click "Add Shift"
2. Enter:
   - **Date**: Shift date
   - **Start Time**: HH:MM
   - **End Time**: HH:MM
   - **Shift Type**: Morning/Afternoon/Night
   - **Department**: Where assigned
3. Save

**Recurring Shifts** (e.g., Tuesday-Thursday-Saturday):
1. Click "Add Recurring Shift"
2. Enter:
   - **Days**: Select multiple days
   - **Start Time**: 08:00
   - **End Time**: 16:00
   - **Valid From/To**: Date range
3. Save
4. System auto-generates shifts

**Shift Swap/Time Off**:
1. Staff member submits request
2. Manager reviews
3. Click "Approve" or "Deny"
4. If approved: Schedule updated
5. If denied: Notified with reason

### 7.3 Staff Certifications & Credentials

**View Current Certifications**:
1. Open staff member record
2. Click "Certifications" tab
3. View:
   - Certification name
   - Issuing body
   - Issue date
   - Expiration date
   - Renewal status

**Add New Certification**:
1. Click "Add Certification"
2. Enter:
   - **Type**: RN / LPN / CNT / Nephrologist / Other
   - **Issuing Organization**: State board, etc.
   - **License Number**: For verification
   - **Issue Date**: When received
   - **Expiration Date**: When expires
   - **Document**: Upload copy
3. Save

**Certification Renewal Alerts**:
1. System monitors expiration dates
2. Alert sent 30 days before expiration
3. Staff member updates documentation
4. Manager verifies new cert
5. Record updated

### 7.4 Staff Availability & Assignments

**Check Staff Availability**:
1. Go to Staff Management > Staff Availability
2. Select date/time range
3. View:
   - Available staff by shift
   - Busy staff (already assigned sessions)
   - On-leave staff
   - On-call staff

**Assign Staff to Session**:
1. Open Dialysis Session (in progress or upcoming)
2. Click "Assign Staff"
3. Select:
   - **Primary Technician**: Main care provider
   - **Secondary Technician**: Support (if multi-person shift)
   - **Nephrologist On Call**: Doctor responsible
4. Save
5. Staff notified of assignment

### 7.5 Performance Tracking

**Session Completion Rate**:
1. Open staff member
2. Click "Performance" tab
3. View:
   - Sessions completed this month
   - Average session duration
   - Complication rate
   - Patient satisfaction rating

**Training & Development**:
1. Click "Training" section
2. View completed trainings
3. View required trainings
4. Assign new training course
5. Track completion date

**Performance Review**:
1. Annual/periodic reviews documented
2. Click "Reviews" section
3. View previous reviews
4. Manager can add new review

### 7.6 Staff Workload Distribution

**View Workload Balance**:
1. Go to Reports > Staff Workload
2. View:
   - Sessions per staff member (month)
   - Average patients assigned
   - Overtime hours
   - Shift distribution
3. Identify overload situations
4. Rebalance if needed

**Workload Alerts**:
- System alerts if staff overbooked
- Warns if overtime excessive
- Suggests load balancing
- Manager can reassign sessions

---

## 8. Insurance Management Guide

### Overview
Insurance Management handles patient insurance information and claims processing.

### 8.1 Patient Insurance Setup

**Add Insurance to Patient**:
1. Open patient record
2. Click "Insurance" section
3. Click "Add Insurance"
4. Enter:
   - **Insurance Provider**: Select or create
   - **Policy Number**: Insurance ID
   - **Group Number**: Employer group
   - **Coverage Start Date**: When effective
   - **Coverage End Date**: When expires (if known)
   - **Co-pay Amount**: Per visit (e.g., $25)
   - **Deductible**: Annual deductible
   - **Coverage Percentage**: % covered (typically 80%)
5. Save

### 8.2 Insurance Verification

**Verify Coverage**:
1. Before scheduling appointment
2. Or before dialysis session
3. Click "Verify Insurance"
4. System attempts to verify:
   - Policy active
   - Coverage still valid
   - Patient information matches
5. Shows verification status

**Prior Authorization**:
1. Some dialysis requires pre-approval
2. Click "Request Prior Auth"
3. System prepares request with:
   - Patient info
   - Procedure/treatment
   - Medical necessity
4. Send to insurance
5. Track approval status

### 8.3 Claims Management

**View Insurance Claims**:
1. Open patient bill
2. Click "Insurance" tab
3. View submitted claims:
   - Claim number
   - Amount claimed
   - Status (Submitted/Approved/Denied/Paid)
   - Remittance advice

**Process Remittance**:
1. When insurance pays
2. Click "Record Insurance Payment"
3. Enter:
   - Amount paid by insurance
   - Insurance deduction
   - Patient responsibility updated
4. Save
5. Patient billed for remaining balance

---

**End of User Guides - Part 3**

