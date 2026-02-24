# 🔍 Phase 2 Features - Interactive Exploration Guide

## Welcome to Phase 2!

This guide will walk you through all the new features added in Phase 2:
- Clinical Operations (Dialysis Sessions, Treatment Templates)
- Laboratory Integration (Lab Tests & Results)
- Billing & Financial Management (Invoices & Payments)

**Estimated Time:** 45 minutes for complete exploration

---

## 🌐 Getting Started

**Server Status:** Should be running at http://127.0.0.1:8000  
**Login:** Administrator / admin@123

If server is not running:
```bash
cd frappe-bench
bench start
```

---

## 📋 Section 1: Clinical Operations (15 minutes)

### **Step 1.1: View Dialysis Sessions** (5 min)

**Navigate to:** http://127.0.0.1:8000/app/dialysis-session

**What You'll See:**
- List view with 1 session: DS-2026-00001
- Patient: John Doe
- Session Date: Today
- Status: Scheduled

**Try These Actions:**

🔍 **Explore Filters:**
- Click "Add Filter" on the left
- Filter by Status = "Scheduled"
- Filter by Session Date = "Today"
- Try filtering by Patient

📊 **List View Features:**
- Click column headers to sort
- Use search box to find sessions
- Notice the status badges (color-coded)

---

### **Step 1.2: Open a Dialysis Session** (10 min)

**Click on:** DS-2026-00001  
**Or visit:** http://127.0.0.1:8000/app/dialysis-session/DS-2026-00001

**Explore the Form:**

#### **Section 1: Patient & Scheduling**
```
Patient: PT-2026-00001 (John Doe)
Patient Name: John Doe (auto-filled from patient)
Session Date: [Today's date]
Session Time: 09:00
```

**Try This:**
- Click on the Patient link → Opens patient record
- Notice Patient Name auto-fills when you select a patient

---

#### **Section 2: Treatment Details**
```
Dialysis Machine: DM-001 (Fresenius Medical Care 5008S)
Dialysis Modality: Hemodialysis
Treatment Duration: 240 minutes (4 hours)
Blood Flow Rate: 300 mL/min
Dialysate Flow Rate: 500 mL/min
Ultrafiltration Goal: 2.5 L
```

**Try This:**
- Click on Machine link → Opens machine record
- Change the modality dropdown (Hemodialysis, Hemodiafiltration, Hemofiltration)
- Notice how clinical parameters are displayed

---

#### **Section 3: Vital Signs Log** (Important!)
**This is a child table - you can add multiple readings**

Current vital signs:
```
Time: 09:00
├─ Systolic BP: 140 mmHg
├─ Diastolic BP: 85 mmHg
├─ Heart Rate: 72 bpm
└─ Temperature: 36.8°C

Time: 11:00
├─ Systolic BP: 135 mmHg
├─ Diastolic BP: 82 mmHg
├─ Heart Rate: 70 bpm
└─ Temperature: 36.9°C
```

**Try Adding a New Vital Sign Reading:**
1. Click "Add Row" in the Vital Signs table
2. Fill in:
   - Time: 13:00
   - Systolic BP: 130
   - Diastolic BP: 80
   - Heart Rate: 68
   - Temperature: 37.0
3. Click "Save" (top-right)
4. See the new reading added to the table!

---

#### **Section 4: Weight & Notes**
```
Pre-Dialysis Weight: 75.5 kg
Post-Dialysis Weight: 73.0 kg
Weight Loss: 2.5 kg (AUTO-CALCULATED!)
Complications: [Empty]
Notes: Patient tolerated treatment well
```

**Try This - Test Auto-Calculation:**
1. Change Pre-Dialysis Weight to 76.0
2. Change Post-Dialysis Weight to 73.5
3. Click anywhere outside the field
4. **Watch Weight Loss auto-update to 2.5!** ✨

This is business logic in action!

---

#### **Section 5: Status & Timing**
```
Status: Scheduled
Started At: [Empty]
Completed At: [Empty]
Actual Duration: [Empty]
```

**Try This - Simulate Session Progress:**
1. Change Status to "In Progress"
2. Fill in Started At: [Click to set current datetime]
3. Click "Save"
4. Notice the form updates

**To Complete the Session:**
1. Change Status to "Completed"
2. Fill in Completed At: [Set a time 4 hours later]
3. Click "Save"
4. The system will auto-calculate Actual Duration!

---

### **Step 1.3: Create a New Dialysis Session** (Extra Credit)

**Navigate to:** http://127.0.0.1:8000/app/dialysis-session/new

**Create a session for tomorrow:**
```
Patient: Select PT-2026-00004 (John Smith)
Session Date: [Tomorrow's date]
Session Time: 14:00
Dialysis Machine: DM-002
Dialysis Modality: Hemodialysis
Treatment Duration: 240
Blood Flow Rate: 300
Dialysate Flow Rate: 500
Ultrafiltration Goal: 3.0
Status: Scheduled
```

Click "Save" → New session created: DS-2026-00002!

---

### **Step 1.4: Treatment Templates** (5 min)

**Navigate to:** http://127.0.0.1:8000/app/treatment-template

**What You'll See:**
- 1 template: "Standard Hemodialysis"

**Open the Template:**
**Visit:** http://127.0.0.1:8000/app/treatment-template/Standard%20Hemodialysis

**Explore the Template:**
```
Template Name: Standard Hemodialysis
Dialysis Modality: Hemodialysis
Treatment Duration: 240 minutes
Blood Flow Rate: 300 mL/min
Dialysate Flow Rate: 500 mL/min
Dialyzer Type: High Flux
Description: Standard 4-hour hemodialysis treatment
Is Active: ✓ (checked)
```

**Try the Custom Button:**
1. Click "Create Session from Template"
2. A new Dialysis Session form opens
3. Notice all treatment parameters are pre-filled! 🎯
4. Just add patient, date, machine and save!

**Create Another Template:**
1. Go back to template list
2. Click "+ Add Treatment Template"
3. Create "Acute Dialysis Protocol":
   ```
   Template Name: Acute Dialysis Protocol
   Dialysis Modality: Hemodiafiltration
   Treatment Duration: 180 (3 hours)
   Blood Flow Rate: 350
   Dialysate Flow Rate: 600
   Dialyzer Type: High Flux
   Description: Short-duration acute treatment
   Is Active: ✓
   ```
4. Save it and try creating a session from this template!

---

## 🧪 Section 2: Laboratory Integration (15 minutes)

### **Step 2.1: View Lab Tests** (5 min)

**Navigate to:** http://127.0.0.1:8000/app/lab-test

**What You'll See:**
- 1 lab test: LAB-2026-00001
- Patient: John Doe
- Test Type: Pre-Dialysis Labs
- Status: Pending

**List View Features:**
- Filter by Test Type, Status, Patient
- Search by patient name
- Sort by test date

---

### **Step 2.2: Open a Lab Test** (10 min)

**Click on:** LAB-2026-00001  
**Or visit:** http://127.0.0.1:8000/app/lab-test/LAB-2026-00001

**Explore the Form:**

#### **Section 1: Test Information**
```
Patient: PT-2026-00001 (John Doe)
Patient Name: John Doe (auto-filled)
Test Date: [Today]
Test Type: Pre-Dialysis Labs
```

**Test Types Available:**
- Pre-Dialysis Labs
- Monthly Labs
- Quarterly Labs
- Custom

---

#### **Section 2: Test Results** (Important!)
**This is where lab values are entered**

Current results:
```
Test Parameter    | Result | Unit   | Normal Range | Abnormal
------------------|--------|--------|--------------|----------
Hemoglobin        | 10.5   | g/dL   | 13.5-17.5    | ✓
Creatinine        | 8.2    | mg/dL  | 0.7-1.3      | ✓
Potassium         | 5.1    | mEq/L  | 3.5-5.0      | ✓
```

**Notice:** All 3 results are flagged as abnormal!

**Try Adding More Results:**
1. Click "Add Row" in the Results table
2. Add these common dialysis parameters:

```
Test Parameter: Urea
Result Value: 120
Unit: mg/dL
Normal Range: 7-20
Is Abnormal: ✓ (check it)

Test Parameter: Albumin
Result Value: 3.8
Unit: g/dL
Normal Range: 3.5-5.5
Is Abnormal: [Leave unchecked - normal!]

Test Parameter: Calcium
Result Value: 9.2
Unit: mg/dL
Normal Range: 8.5-10.5
Is Abnormal: [Leave unchecked]
```

3. Click "Save"
4. Now you have 6 test results!

---

#### **Section 3: Status & Review**
```
Clinical Notes: [Add observations about abnormal values]
Status: Pending
Reviewed By: [Empty]
Reviewed Date: [Empty]
```

**Try the Workflow:**
1. Add Clinical Notes: "Patient has anemia and high creatinine, continue EPO therapy"
2. Change Status to "Completed"
3. Click "Save"
4. The test is now marked as completed!

**To Mark as Reviewed:**
1. Change Status to "Reviewed"
2. Reviewed By: Administrator
3. Reviewed Date: [Current datetime]
4. Click "Save"

---

### **Step 2.3: Submit a Lab Test** (Advanced)

Lab Tests are submittable documents!

1. Open LAB-2026-00001
2. Ensure Status = "Completed" or "Reviewed"
3. Click "Submit" button (top-right)
4. Confirm submission
5. **Document is now locked!** (Can't edit)
6. DocStatus changes to "Submitted"

**Try This:**
- After submitting, try to edit a field
- Notice you can't - document is read-only
- You can "Cancel" if needed (creates audit trail)

---

### **Step 2.4: Create a New Lab Test** (Extra Credit)

**Navigate to:** http://127.0.0.1:8000/app/lab-test/new

**Create Monthly Labs for Mary Johnson:**
```
Patient: PT-2026-00005 (Mary Johnson)
Test Date: [Today]
Test Type: Monthly Labs
```

**Add Common Monthly Panel:**
```
1. Hemoglobin: 11.2, g/dL, 13.5-17.5, ✓ Abnormal
2. Hematocrit: 34, %, 38-50, ✓ Abnormal
3. WBC: 7.5, 10³/µL, 4.0-11.0, Normal
4. Platelets: 180, 10³/µL, 150-400, Normal
5. Sodium: 138, mEq/L, 135-145, Normal
6. Potassium: 4.8, mEq/L, 3.5-5.0, Normal
```

Save it! Now you have 2 lab tests.

---

## 💰 Section 3: Billing & Financial Management (15 minutes)

### **Step 3.1: View Invoices** (5 min)

**Navigate to:** http://127.0.0.1:8000/app/invoice

**What You'll See:**
- 1 invoice: INV-2026-00001
- Patient: John Doe
- Total: $4,950
- Payment Status: Partially Paid

**List View Features:**
- Filter by Payment Status, Patient, Date
- Color-coded status badges
- Outstanding amount visible

---

### **Step 3.2: Open an Invoice** (10 min)

**Click on:** INV-2026-00001  
**Or visit:** http://127.0.0.1:8000/app/invoice/INV-2026-00001

**Explore the Form:**

#### **Section 1: Invoice Header**
```
Patient: PT-2026-00001 (John Doe)
Patient Name: John Doe (auto-filled)
Invoice Date: [Today]
Due Date: [30 days from today]
```

---

#### **Section 2: Invoice Details**
```
Dialysis Session: DS-2026-00001 (linked!)
Description: Hemodialysis Session - 4 hours
Quantity: 1
Rate: $5,000
```

**Click on Dialysis Session link** → Opens the linked session!

---

#### **Section 3: Calculations** (AUTO-MAGIC! ✨)
```
Subtotal: $5,000 (quantity × rate)
Discount %: 10%
Discount Amount: $500 (AUTO-CALCULATED!)
Tax Amount: $450
Total Amount: $4,950 (AUTO-CALCULATED!)
```

**Try This - Watch Auto-Calculation:**
1. Change Rate to $6,000
2. Click outside the field
3. **Watch Subtotal update to $6,000**
4. **Watch Discount Amount update to $600**
5. **Watch Total Amount update to $5,850**
6. This is real-time calculation!

Change it back to $5,000 and save.

---

#### **Section 4: Payment Tracking**
```
Payment Status: Partially Paid (auto-updated based on paid amount!)
Paid Amount: $2,000
Outstanding Amount: $2,950 (total - paid)
```

**Payment Status Logic:**
- If Outstanding = 0 → "Paid"
- If Paid > 0 but Outstanding > 0 → "Partially Paid"
- If Paid = 0 → "Unpaid"
- If past Due Date → "Overdue"

---

### **Step 3.3: View Payments** (5 min)

**Navigate to:** http://127.0.0.1:8000/app/payment

**What You'll See:**
- 1 payment: PAY-2026-00001
- Invoice: INV-2026-00001
- Amount: $2,000
- Method: Cash

**Open the Payment:**
**Visit:** http://127.0.0.1:8000/app/payment/PAY-2026-00001

**Explore the Payment Form:**
```
Invoice: INV-2026-00001 (linked!)
Patient: PT-2026-00001 (auto-fetched from invoice)
Patient Name: John Doe (auto-fetched)
Payment Date: [Today]
Payment Method: Cash
Amount: $2,000
Amount Tendered: $2,000 (for cash payments)
Change Amount: $0 (auto-calculated!)
Reference Number: CASH-001
```

**Try the Cash Change Calculator:**
1. Change Amount to $3,000
2. Change Amount Tendered to $3,500
3. Click outside the field
4. **Watch Change Amount auto-calculate to $500!** 💵

---

### **Step 3.4: Create a New Payment** (10 min)

Let's pay the remaining balance on the invoice!

**Navigate to:** http://127.0.0.1:8000/app/payment/new

**Create Payment:**
```
Invoice: INV-2026-00001
(Patient and Patient Name auto-fill!)
Payment Date: [Today]
Payment Method: Credit Card
Amount: $2,950 (the outstanding amount)
Reference Number: CC-12345678
Notes: Final payment - Credit Card
```

Click "Save" → Payment created: PAY-2026-00002!

**What Happens Next:**
1. Click "Submit" on the payment
2. The system updates the invoice automatically!
3. Go back to the invoice: INV-2026-00001
4. **Notice:**
   - Paid Amount is now $4,950
   - Outstanding Amount is now $0
   - Payment Status is now "Paid"! ✅

**This is integrated workflow in action!**

---

### **Step 3.5: Create an Invoice from Scratch** (Extra Credit)

**Navigate to:** http://127.0.0.1:8000/app/invoice/new

**Create Invoice for Mary Johnson:**
```
Patient: PT-2026-00005 (Mary Johnson)
Invoice Date: [Today]
Due Date: [14 days from today]
Description: Initial Consultation and Assessment
Quantity: 1
Rate: $250
Discount %: 0
Tax Amount: $25
Payment Status: Unpaid
```

Save it! Invoice INV-2026-00002 created.

**Now Create a Payment:**
1. Click "Record Payment" custom button (if available)
2. Or manually create a payment linking to INV-2026-00002
3. Pay full amount: $275
4. Submit the payment
5. Watch the invoice status change to "Paid"!

---

## 🎯 Section 4: Testing Integrated Workflows (Bonus - 10 min)

### **Complete Patient Journey Simulation**

Let's simulate a complete patient journey through all Phase 2 features:

#### **Day 1: Patient Arrives for Treatment**

**Step 1: Create Dialysis Session**
1. Go to: http://127.0.0.1:8000/app/dialysis-session/new
2. Use "Standard Hemodialysis" template (click template, then "Create Session from Template")
3. Fill in:
   ```
   Patient: PT-2026-00004 (John Smith)
   Session Date: [Tomorrow]
   Session Time: 08:00
   Dialysis Machine: DM-003
   ```
4. Save → Session DS-2026-00003 created

**Step 2: Record Vital Signs During Treatment**
1. Open DS-2026-00003
2. Change Status to "In Progress"
3. Set Started At to current time
4. Add vital signs readings every hour:
   ```
   08:00 - BP: 145/90, HR: 75, Temp: 36.7
   09:00 - BP: 140/88, HR: 72, Temp: 36.8
   10:00 - BP: 135/85, HR: 70, Temp: 36.9
   11:00 - BP: 138/86, HR: 71, Temp: 37.0
   ```
5. Set Pre-weight: 78.5, Post-weight: 76.0
6. Set Status to "Completed"
7. Set Completed At
8. Save → Weight Loss auto-calculated, Actual Duration computed!

**Step 3: Submit the Session**
1. Click "Submit"
2. Session is now locked
3. Machine utilization is updated

---

#### **Day 2: Order Lab Tests**

**Step 1: Create Lab Test Order**
1. Go to: http://127.0.0.1:8000/app/lab-test/new
2. Fill in:
   ```
   Patient: PT-2026-00004 (John Smith)
   Test Date: [Today]
   Test Type: Pre-Dialysis Labs
   ```
3. Save → LAB-2026-00002 created

**Step 2: Enter Lab Results**
1. Add standard panel results
2. Flag abnormal values
3. Add clinical notes
4. Set Status to "Completed"
5. Submit the test

---

#### **Day 3: Generate Invoice and Process Payment**

**Step 1: Create Invoice for Session**
1. Go to: http://127.0.0.1:8000/app/invoice/new
2. Fill in:
   ```
   Patient: PT-2026-00004
   Dialysis Session: DS-2026-00003
   Description: Hemodialysis Session - 4 hours
   Quantity: 1
   Rate: $5,500
   Discount %: 5
   Tax Amount: $260
   ```
3. Save → Total auto-calculated!
4. Submit the invoice

**Step 2: Record Payment**
1. Create new payment
2. Link to the invoice
3. Payment Method: Insurance
4. Amount: $5,200 (partial payment)
5. Submit → Invoice updates to "Partially Paid"

**Step 3: Record Final Payment**
1. Create second payment
2. Amount: Remaining outstanding
3. Payment Method: Credit Card
4. Submit → Invoice status changes to "Paid"!

**🎉 Complete workflow tested!**

---

## 📊 Section 5: Data Analysis & Insights

### **Check Your Progress:**

**Run this in your browser console or Frappe Console:**

Visit: http://127.0.0.1:8000/app

```javascript
// Open browser console (F12)
frappe.call({
    method: 'frappe.client.get_count',
    args: { doctype: 'Dialysis Session' },
    callback: (r) => console.log('Sessions:', r.message)
});

frappe.call({
    method: 'frappe.client.get_count',
    args: { doctype: 'Lab Test' },
    callback: (r) => console.log('Lab Tests:', r.message)
});

frappe.call({
    method: 'frappe.client.get_count',
    args: { doctype: 'Invoice' },
    callback: (r) => console.log('Invoices:', r.message)
});
```

**Or check via backend:**
```bash
cd frappe-bench
bench --site frappe.local console
```

```python
print(f"Dialysis Sessions: {frappe.db.count('Dialysis Session')}")
print(f"Lab Tests: {frappe.db.count('Lab Test')}")
print(f"Invoices: {frappe.db.count('Invoice')}")
print(f"Payments: {frappe.db.count('Payment')}")
print(f"Treatment Templates: {frappe.db.count('Treatment Template')}")
```

---

## ✅ Exploration Checklist

Track your progress:

### **Clinical Operations:**
- [ ] Viewed dialysis session list
- [ ] Opened and explored a dialysis session
- [ ] Added vital signs readings
- [ ] Tested weight loss auto-calculation
- [ ] Created a new dialysis session
- [ ] Used treatment template to create session
- [ ] Created a custom treatment template
- [ ] Submitted a dialysis session

### **Laboratory:**
- [ ] Viewed lab test list
- [ ] Opened and explored a lab test
- [ ] Added lab result rows
- [ ] Flagged abnormal results
- [ ] Created a new lab test
- [ ] Submitted a lab test
- [ ] Reviewed lab results

### **Billing:**
- [ ] Viewed invoice list
- [ ] Opened and explored an invoice
- [ ] Tested invoice auto-calculations
- [ ] Viewed payment list
- [ ] Opened and explored a payment
- [ ] Tested cash change calculation
- [ ] Created a new payment
- [ ] Watched invoice status auto-update
- [ ] Created invoice from scratch
- [ ] Completed full payment workflow

### **Integration:**
- [ ] Linked dialysis session to invoice
- [ ] Created payment for invoice
- [ ] Verified auto-update of invoice status
- [ ] Completed end-to-end patient journey

---

## 💡 Power User Tips

### **Keyboard Shortcuts:**
- `Ctrl + S` - Save current document
- `Ctrl + K` - Open Awesome Bar (search)
- `Ctrl + G` - Go to next field
- `Esc` - Close dialog

### **Quick Navigation:**
- Type "new dialysis" in Awesome Bar → Quick create
- Type "invoice john" → Search invoices for John
- Bookmark frequently used pages

### **Filtering Tips:**
- Combine multiple filters for powerful queries
- Use "Between" filter for date ranges
- Save custom filter sets

### **Data Entry Tips:**
- Use Tab key to move between fields
- Child tables support copy-paste from Excel
- Link fields support type-ahead search

---

## 🔍 What to Look For

### **Smart Features:**
1. **Auto-Calculations:**
   - Weight loss in sessions
   - Invoice totals
   - Payment change amounts
   - Actual duration

2. **Auto-Fetching:**
   - Patient name from patient link
   - Invoice details when creating payment

3. **Status Updates:**
   - Invoice payment status changes automatically
   - Lab test workflow states

4. **Business Logic:**
   - Machine utilization updates on session submit
   - Abnormal lab value detection
   - Payment allocation to invoices

5. **Data Integrity:**
   - Can't edit submitted documents
   - Links maintain referential integrity
   - Audit trail on all changes

---

## 📞 Need Help?

**If something doesn't work:**
1. Check browser console (F12) for errors
2. Verify server is running
3. Clear cache: `bench --site frappe.local clear-cache`
4. Check logs: `frappe-bench/logs/`

**Common Issues:**
- **Can't edit field:** Document might be submitted
- **Calculation not working:** Try saving first
- **Link not showing:** Make sure linked document exists
- **Button missing:** Check permissions or document state

---

## 🎊 Congratulations!

After completing this guide, you've:
- ✅ Explored all 7 new DocTypes
- ✅ Tested auto-calculations and business logic
- ✅ Created multiple test records
- ✅ Experienced integrated workflows
- ✅ Understood the complete patient journey

**You're now ready to use Phase 2 features in production!**

---

## 🚀 What's Next?

After exploring Phase 2:
1. **Create more test data** for realistic scenarios
2. **Setup user roles** for different staff members
3. **Build custom reports** for analytics
4. **Configure print formats** for invoices and receipts
5. **Add email notifications** for appointments and payments

**Or explore Phase 3 features:**
- Inventory Management
- Staff Scheduling
- Advanced Reporting
- Mobile App

---

*Happy Exploring!* 🎉

*Last Updated: 2026-02-19*  
*Phase: 2 Complete*  
*App Version: 0.0.1*
