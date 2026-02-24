# User Guides - Part 2: Dialysis Operations & Billing
## Dialysis Center Management System

**Last Updated**: February 19, 2026  
**Version**: 1.0.0

---

## 3. Dialysis Session Operations Guide

### Overview
This guide covers the complete dialysis session workflow from pre-treatment preparation to post-treatment documentation.

### 3.1 Pre-Session Preparation

**Before Patient Arrival** (30 minutes prior):
1. **Check Appointment**:
   - Go to Appointment list
   - Find today's appointments
   - Verify patient name, time, machine assignment
   - Check patient notes for special requirements

2. **Verify Machine Status**:
   - Go to Equipment Management > Dialysis Machine
   - Check assigned machine status
   - Verify: Water supply, electricity, alarm system
   - Check maintenance history (no outstanding issues?)
   - Confirm dialyzer and bloodline availability

3. **Prepare Supplies**:
   - Gather dialyzer (check expiration)
   - Prepare blood lines (arterial/venous)
   - Get saline bags, heparin, anticoagulants
   - Prepare vital signs monitoring equipment
   - Set up patient file/chart

**Patient Arrival Process**:
1. Greet patient and verify identity
2. Ask about health status since last session
3. Take initial weight (compare to dry weight target)
4. Record temperature, blood pressure, pulse
5. Help patient change into gown
6. Prepare vascular access (fistula/graft/catheter)

### 3.2 Starting a Dialysis Session

**Create Session Record**:
1. Go to "Dialysis Center Management" > "Dialysis Session"
2. Click "New Dialysis Session"
3. Or create from Appointment (Appointment > Create > Dialysis Session)

**Fill Session Header**:
- **Patient**: Auto-filled from appointment
- **Appointment**: Link to original appointment
- **Session Date**: Auto-filled with today's date
- **Start Time**: Current time (auto-filled)
- **Assigned Technician**: Current user (can change)
- **Dialysis Machine**: Pre-assigned machine
- **Nephrologist On Call**: Doctor responsible for today

**Pre-Treatment Assessment**:
- **Patient Weight**: Current weight (kg)
- **Dry Weight Target**: Expected post-dialysis weight
- **Ultrafiltration Needed**: System calculates (Weight - Target)
- **Access Type**: Fistula/Graft/Catheter (pre-filled)
- **Access Status**: Good/Fair/Poor
- **General Condition**: Patient's appearance and mood notes

### 3.3 Recording Treatment Parameters

**Initial Blood Work** (before treatment):
1. Scroll to "Pre-Treatment Blood Work" section
2. Record: Potassium, Creatinine, Calcium, Phosphate, Hemoglobin
3. System shows reference ranges
4. Review values against normal ranges
5. Alert triggered if abnormal

**Dialyzer Setup**:
- **Dialyzer Type**: Select from dropdown (e.g., Fresenius FX8, Nippon Baxter)
- **Dialyzer Batch Number**: For tracking
- **Priming Method**: Manual/Machine prime
- **Membrane Flux**: Low/High flux
- **Surface Area**: Typical 1.3-2.2 m²
- **Biocompatibility**: Standard/High
- **Check "Dialyzer Primed"** when ready

**Treatment Settings**:
- **Blood Flow Rate**: Typical 300-400 mL/min
- **Dialysate Flow Rate**: Typical 500-800 mL/min
- **Dialysate Temperature**: Typical 37°C
- **Dialysate Conductivity**: Typical 14 mS/cm
- **Ultrafiltration Rate**: Calculated per patient
- **Anticoagulation Type**: Heparin/LMWH/None
- **Heparin Dose**: Calculate based on weight

**Click "Start Session"** button:
- System records start time
- Treatment timer begins
- Monitors activated
- Session status changes to "In Progress"

### 3.4 Recording Vital Signs During Treatment

**Every 30-60 Minutes**:
1. Click "Record Vital Signs" in session
2. Enter time and vital signs:
   - **Blood Pressure**: Systolic/Diastolic (mmHg)
   - **Pulse**: Beats per minute
   - **Respiratory Rate**: Breaths per minute
   - **Temperature**: Degrees Celsius
   - **Oxygen Saturation**: % (if available)
   - **Dialyzer Pressure**: Venous/Arterial (from machine)
   - **Ultrafiltration Volume**: Current total (mL)
3. **Observations**: Notes on patient status
   - Any symptoms?
   - Any alarms?
   - Patient comfort level?
4. Click "Save Vital Signs"
5. Record added to vital signs log

**Monitoring Alerts**:
- System alerts if BP drops > 20% from baseline
- Alert if HR > 110 or < 50
- Alert if temp > 37.5°C
- Alert if fluid removal too fast (cramping risk)
- **Action**: Notify nephrologist if concerning trends

### 3.5 Managing Treatment Complications

**Common Complications & Responses**:

**Muscle Cramps**:
1. Reduce ultrafiltration rate
2. Give normal saline bolus (100-200 mL)
3. Massage affected muscle
4. Record event in session notes
5. Adjust next session parameters

**Hypotension (Low BP)**:
1. Stop ultrafiltration temporarily
2. Position patient flat (Trendelenburg)
3. Give normal saline bolus
4. Reduce blood flow rate
5. Notify nephrologist
6. Record incident details

**Bleeding/Clotting**:
1. Check vascular access
2. If arterial puncture: Apply pressure 10 minutes
3. If graft bleeding: Contact vascular surgeon
4. Document in session notes
5. May require access revision

**Fever During Treatment**:
1. Record temperature
2. Check vital signs
3. May indicate infection (pyrogens)
4. Stop treatment if > 38.5°C
5. Notify nephrologist immediately
6. May need blood culture

**Nausea/Vomiting**:
1. Check blood pressure (may be hypotension)
2. Reduce ultrafiltration rate
3. Give antiemetic if available
4. Consider shorter session length next time
5. Dietary counseling about fluid/sodium intake

**Chest Pain**:
1. Stop treatment immediately
2. Notify nephrologist
3. Perform cardiac assessment (if trained)
4. Record vital signs continuously
5. May need EKG
6. Consider emergency transport

### 3.6 Pausing Sessions

**If Patient Needs Temporary Break**:
1. Click "Pause Session" button
2. Reason: Comfort break, medical issue, etc.
3. Note time paused
4. Keep blood lines in place if < 30 min pause
5. Disconnect if pause > 30 min

**Resuming After Pause**:
1. Patient returns, vital signs checked
2. Click "Resume Session"
3. Adjust treatment parameters if needed
4. Continue monitoring
5. System tracks total pause duration

### 3.7 Completing the Dialysis Session

**Final Treatment Phase**:
1. Check ultrafiltration goal achieved (or close)
2. Begin rinsing back blood (saline flush)
3. Monitor vital signs closely
4. Blood pressure may drop during rinsing
5. Stop machine when blood returned

**Post-Treatment Assessment**:
1. Record final vital signs:
   - Final weight (should be close to dry weight target)
   - Final BP and HR
   - Temperature
   - O2 saturation
2. Record total ultrafiltration volume
3. Record total treatment time
4. Any remaining issues to note?

**Post-Treatment Blood Work**:
1. If ordered by nephrologist, draw blood sample
2. Record: Potassium, Hemoglobin (checks for blood loss)
3. Send to lab immediately
4. Record sample info in session

**Vascular Access Care**:
1. Inspect access site for bleeding
2. Apply bandage if arterial puncture
3. Educate patient on home care
4. Schedule thrill check next session
5. Note any concerns for follow-up

**Patient Discharge**:
1. Allow rest time (15-30 min)
2. Patient drinks and eats as tolerated
3. Verify patient feels okay before leaving
4. Schedule next appointment if not recurring
5. Provide any take-home instructions

### 3.8 Completing Session Documentation

**Click "Complete Session"** button:
1. System prompts for final documentation
2. Confirm all vital signs recorded
3. Confirm blood work completed (if applicable)
4. Confirm dialyzer disposal planned
5. Add clinical notes summary:
   - Overall session quality (good/fair/poor)
   - Patient tolerance
   - Any complications
   - Recommendations for next session
6. Click "Submit"
7. Session locked for editing (audit trail)

**Generate Session Report** (optional):
1. Click "Print Session Report"
2. Report includes:
   - Patient demographics
   - Treatment parameters
   - Vital signs graph
   - Fluid removal summary
   - Complications/events
   - Nephrologist notes
3. Print or save as PDF
4. Provide copy to patient if requested

### 3.9 Quality Assurance Checklist

**Use this checklist for each session**:
- [ ] Patient identity verified
- [ ] Vital signs recorded every 30-60 min
- [ ] Blood work done (pre and post if ordered)
- [ ] Treatment parameters documented
- [ ] Ultrafiltration goal achieved
- [ ] Dialyzer priming proper
- [ ] Anticoagulation adequate
- [ ] No complications or all documented
- [ ] Session time on target
- [ ] Patient discharged safely
- [ ] All documentation complete
- [ ] Session report generated

---

## 4. Billing & Invoice Management Guide

### Overview
The Billing module manages patient invoicing, payment tracking, and financial records.

### 4.1 Creating a Patient Bill

**Method 1: Manual Bill Creation**:
1. Go to "Billing Management" > "Patient Bill"
2. Click "New Patient Bill"
3. Select **Patient**: Auto-complete search
4. System auto-fills:
   - Patient name
   - Insurance information
   - Outstanding balance (if any)

**Method 2: From Completed Dialysis Session**:
1. Open completed Dialysis Session
2. Click "Create" > "Patient Bill"
3. Patient and session auto-filled
4. Services automatically added

**Bill Header Information**:
- **Billing Date**: Today's date (auto-filled)
- **Due Date**: Set payment deadline (e.g., 15 days)
- **Billing Period**: Month/Year being billed
- **Patient Class**: Individual/Insurance/Cash/Medicare

### 4.2 Adding Services & Charges

**Add Dialysis Session Charge**:
1. Click "Add Row" in Services section
2. Enter:
   - **Service**: Dialysis Treatment
   - **Description**: "Regular dialysis session 4 hours"
   - **Quantity**: 1
   - **Unit Price**: Set by clinic ($200-300 typical)
   - **Amount**: Auto-calculated (Qty × Price)
3. Click Save

**Add Lab Test Charges**:
1. Click "Add Row"
2. Service: Lab Test
3. Description: Specific test (e.g., "Serum Potassium")
4. Unit Price: Set per clinic pricing
5. Save

**Other Charges**:
- Vascular access care
- Medication administration
- Consultation fees
- Emergency charges
- Administrative fees

**Discounts**:
1. Click "Discounts" section
2. Enter discount type:
   - Percentage discount (e.g., 10%)
   - Fixed amount discount (e.g., $50)
3. System auto-calculates

**Insurance Coverage**:
1. If insurance: Click "Insurance" section
2. Enter Insurance Provider
3. Insurance ID
4. Coverage percentage
5. Co-pay amount
6. System calculates patient responsibility

### 4.3 Calculating Total & Taxes

**Subtotal**: Sum of all services
**Taxes** (if applicable):
- Sales tax (varies by location)
- Healthcare tax
- System auto-applies based on configuration

**Grand Total**: Subtotal + Tax - Discount

### 4.4 Processing Payments

**Record Payment**:
1. Open bill (Draft or Submitted status)
2. Click "Add Payment" button
3. Enter:
   - **Amount Paid**: Exact payment amount
   - **Payment Method**: Cash/Check/Credit Card/Bank Transfer/Insurance
   - **Payment Date**: Date payment received
   - **Reference**: Check number or transaction ID
   - **Notes**: Payment details
4. Click "Save Payment"

**Payment Status Updates**:
- Full payment: Bill marked "Paid"
- Partial payment: Shows "Partially Paid"
- Overdue: System marks if past due date
- System tracks payment history

**Credit Notes** (if overcharging):
1. Click "Create Credit Note" on bill
2. Reason: Overcharge, adjustment, etc.
3. Amount: Enter refund amount
4. Create new bill to reconcile

### 4.5 Viewing Billing History

**Patient Billing Summary**:
1. Open patient record
2. Click "Billing" tab
3. View:
   - Total bills generated
   - Total paid
   - Outstanding balance
   - Average bill amount
   - Recent transaction history

**Outstanding Bills Report**:
1. Go to Reports > Outstanding Bills
2. View all unpaid bills
3. Filter by date range, patient
4. Export to send payment reminders

### 4.6 Generating & Sending Invoices

**View Invoice**:
1. Open bill
2. Click "Print" button
3. Select "Invoice"
4. Review invoice layout

**Send Invoice to Patient**:
1. Click "Email Invoice"
2. System composes email
3. Invoice PDF attached
4. Add custom message if needed
5. Click "Send"
6. Email logged in activity

**Print Invoice**:
1. Click "Print" > "Invoice"
2. Select printer
3. Print copies for records

### 4.7 Managing Insurance Claims

**Submit to Insurance**:
1. Open bill
2. If insurance billed: Click "Submit Insurance Claim"
3. System prepares claim document
4. Verify all required fields filled
5. Submit to insurance company (via portal or email)
6. Track claim status

**Track Claim Status**:
1. Open bill
2. View "Insurance Claim Status" field:
   - Submitted: Sent to insurance
   - Acknowledged: Insurance received
   - Approved: Approved for payment
   - Rejected: Denied (review reason)
3. Follow up as needed

**Appeal Denied Claims**:
1. If claim rejected
2. Click "Appeal Claim"
3. Add appeal reason
4. Attach supporting documents
5. Resubmit to insurance
6. Update tracking

### 4.8 Collection & Follow-up

**Send Payment Reminder**:
1. Open overdue bill
2. Click "Send Reminder"
3. Email reminder sent to patient
4. Default: 10 days after due date
5. Can send multiple reminders

**Call Patient for Payment**:
1. Open bill
2. Click "Log Call"
3. Document:
   - Call date/time
   - Patient response
   - Promise to pay date
   - Notes
4. System tracks follow-up

**Write Off Bad Debt** (if necessary):
1. Only for uncollectible accounts
2. Requires manager approval
3. Open bill
4. Click "Write Off"
5. Reason: Bankruptcy, patient deceased, etc.
6. Amount written off recorded
7. Tax documentation prepared

### 4.9 Financial Reports

**Run Billing Reports**:
1. Go to Reports section
2. Available reports:
   - Daily Revenue Report
   - Patient Billing Summary
   - Insurance Claims Status
   - Outstanding Receivables
   - Payment Methods Report
   - Aged Receivables (overdue analysis)

**Export Billing Data**:
1. Open report
2. Click "Export"
3. Choose CSV or Excel
4. Download file
5. Use for accounting/bookkeeping

---

**Next Section**: Laboratory, Equipment & Staff Guides (Part 3)

