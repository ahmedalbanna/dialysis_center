# 🎯 Dialysis Center - Interactive UI Walkthrough

## 🌐 Access Information

**URL:** http://127.0.0.1:8000  
**Username:** Administrator  
**Password:** admin@123

---

## 📍 Step-by-Step Exploration Guide

### **Step 1: Login & Desk Overview** (2 minutes)

1. Open your browser and navigate to: http://127.0.0.1:8000
2. Enter credentials:
   - Username: `Administrator`
   - Password: `admin@123`
3. Click "Login"

**What You'll See:**
- Frappe Desk home page
- Left sidebar with modules
- Search bar (Awesome Bar) at the top
- Workspace area in the center

**Try This:**
- Press `Ctrl + K` or `Cmd + K` to open the Awesome Bar (quick search)
- Type "Patient" and see the quick navigation options
- Notice the search suggests DocTypes, reports, and pages

---

### **Step 2: Explore Patient Management** (5 minutes)

#### **View Patient List:**

1. Click on the Awesome Bar (search at top)
2. Type "Patient" and press Enter
3. OR navigate directly to: http://127.0.0.1:8000/app/patient

**What You'll See:**
- List view showing 3 patients:
  - PT-2026-00001: John Doe
  - PT-2026-00004: John Smith
  - PT-2026-00005: Mary Johnson
- Filters on the left sidebar
- Column headers (Name, Patient Name, Gender, Status)

**Try These Actions:**

📊 **Filters:**
- Click "Add Filter" on the left
- Filter by Gender = "Male" (should show 2 patients)
- Clear filter and try Status = "Active"

🔍 **Search:**
- Use the search box to find "John"
- Notice it searches across patient names

📋 **Sorting:**
- Click column headers to sort
- Try sorting by "Patient Name"

#### **View Individual Patient:**

1. Click on "PT-2026-00001" (John Doe)
2. OR visit: http://127.0.0.1:8000/app/patient/PT-2026-00001

**What You'll See:**
- Patient form with all details
- Sections: Basic Information, Contact Details, Medical Information
- Action buttons at top (Save, Menu, etc.)

**Explore the Form:**

📝 **Field Types:**
- Text fields: Patient Name, National ID
- Select dropdowns: Gender, Blood Group, Status
- Date picker: Date of Birth
- Text area: Diagnosis, Address

🔘 **Custom Buttons:**
- "View Medical History" button (will create report later)
- "Schedule Appointment" button (creates new appointment for this patient)

✏️ **Try Editing:**
- Click in the "Address" field
- Change the address to "456 Oak Avenue"
- Notice the "Save" button becomes blue/active
- Click "Save" to save changes
- See the success message at bottom-right

---

### **Step 3: Create a New Patient** (5 minutes)

1. From Patient List, click the blue "+ Add Patient" button
2. OR visit: http://127.0.0.1:8000/app/patient/new

**Fill in the Form:**

```
Patient Name: Sarah Williams
Date of Birth: 1975-03-20
Gender: Female
Blood Group: A+
National ID: 9876543210
Mobile Number: +12025559876
Email: sarah.williams@example.com
Address: 789 Pine Street, Boston
City: Boston
Diagnosis: Chronic Kidney Disease Stage 5
Dialysis Type: Hemodialysis
Status: Active
```

**Try These Features:**

🎯 **Auto-calculations:**
- After entering Date of Birth, notice the Age field updates automatically

✅ **Validations:**
- Try entering an invalid email (e.g., "notanemail")
- Try entering a short phone number
- See validation errors appear

📱 **Mobile Number Formatting:**
- Enter phone with country code: +12025559876
- Notice it validates international format

💾 **Save the Patient:**
- Click the blue "Save" button
- See success message
- New patient ID assigned: PT-2026-00006

---

### **Step 4: Appointment Management** (5 minutes)

#### **View Appointment List:**

1. Navigate to: http://127.0.0.1:8000/app/appointment
2. OR use Awesome Bar: Type "Appointment"

**What You'll See:**
- List showing 1 appointment
- APT-2026-00003: John Doe scheduled for 2026-02-20

#### **Create New Appointment:**

1. Click "+ Add Appointment"
2. OR visit: http://127.0.0.1:8000/app/appointment/new

**Fill in the Form:**

```
Patient: PT-2026-00001 (John Doe)
Appointment Date: 2026-02-21
Appointment Time: 14:00
Duration (minutes): 240
Appointment Type: Regular
Status: Scheduled
Notes: Regular hemodialysis session
```

**Try These Features:**

🔗 **Link Field (Patient):**
- Start typing "John" in Patient field
- See dropdown with matching patients
- Select a patient
- Notice Patient Name auto-fills

📅 **Date & Time Pickers:**
- Click the Date field - see calendar popup
- Click the Time field - see time selector
- Select future dates only (past dates may show warning)

⏱️ **Duration Field:**
- Enter 240 (minutes)
- This represents 4-hour dialysis session

💾 **Save:**
- Click Save
- New appointment created: APT-2026-00004

#### **Try the Custom Button:**

1. Open a patient form (e.g., John Doe)
2. Click "Schedule Appointment" button
3. Notice it opens a new appointment with patient pre-filled
4. This is a custom workflow button!

---

### **Step 5: Equipment Management** (5 minutes)

#### **View Dialysis Machines:**

1. Navigate to: http://127.0.0.1:8000/app/dialysis-machine
2. OR use Awesome Bar: Type "Dialysis Machine"

**What You'll See:**
- 3 machines listed:
  - DM-001: Fresenius Medical Care 5008S
  - DM-002: Fresenius Medical Care 5008S
  - DM-003: Gambro AK 200
- All showing "Available" status

#### **View Machine Details:**

1. Click on "DM-001"
2. OR visit: http://127.0.0.1:8000/app/dialysis-machine/DM-001

**Explore the Form:**

📋 **Machine Information:**
- Machine ID: DM-001
- Manufacturer: Fresenius Medical Care
- Model: 5008S
- Serial Number: FM5008S-2024-001
- Status: Available

📅 **Maintenance Fields:**
- Installation Date
- Last Maintenance Date
- Next Maintenance Due
- Maintenance Interval (days)

📊 **Usage Statistics:**
- Total Sessions: 0 (new machine)
- Total Hours Used: 0.0
- Utilization Rate: 0.0

**Try Changing Status:**

1. Click on "Status" dropdown
2. Change from "Available" to "In Use"
3. Click Save
4. Change back to "Available"
5. Notice status badge colors change

---

### **Step 6: Advanced List View Features** (3 minutes)

Go back to any list view (e.g., Patient List)

**Try These Features:**

🎨 **List View Customization:**
- Click the "⋮" (three dots) menu
- Select "Customize"
- Add/remove columns
- Rearrange column order
- Save customization

📊 **Grouping:**
- In Patient list, try grouping by Gender
- See patients organized by Male/Female groups

📤 **Export:**
- Click the "⋮" menu
- Select "Export" → "Excel"
- Download patient data as spreadsheet

🖨️ **Print:**
- Select any document
- Click Menu → Print
- See print preview
- Can create custom print formats later

---

### **Step 7: Awesome Bar Power Features** (3 minutes)

Press `Ctrl + K` (or `Cmd + K` on Mac)

**Try These Commands:**

```
Type: "new patient"     → Creates new patient
Type: "patient john"    → Searches for John in patients
Type: "apt"             → Shows appointment options
Type: "dm"              → Shows dialysis machine
Type: "report"          → Shows available reports
Type: "user"            → User management
Type: "role"            → Role management
```

**Calculator:**
- Type: `= 240 / 60` (converts minutes to hours)
- Type: `= 75 * 1.2` (quick calculations)

---

### **Step 8: Form Keyboard Shortcuts** (2 minutes)

Open any document form and try:

```
Ctrl + S        → Save
Ctrl + Shift + S → Save and Submit (if submittable)
Ctrl + B        → Add bookmark
Ctrl + G        → Go to next field
Ctrl + K        → Open Awesome Bar
Esc             → Close dialog/go back
```

---

### **Step 9: Notifications & Updates** (2 minutes)

**Real-time Updates:**
- Open Patient list in one browser tab
- Open same list in another tab
- Create/edit a patient in one tab
- See the list auto-refresh in the other tab!

**Notifications:**
- Look for notification bell icon (top-right)
- Shows system notifications
- Document assignments
- Mentions and comments

---

### **Step 10: Data Verification** (3 minutes)

Let's verify what we've created:

**Check Your Data:**

1. **Patients:** Should have 4 now (3 original + 1 Sarah Williams)
   - Visit: http://127.0.0.1:8000/app/patient

2. **Appointments:** Should have 2 (1 original + 1 new)
   - Visit: http://127.0.0.1:8000/app/appointment

3. **Machines:** Still 3 machines
   - Visit: http://127.0.0.1:8000/app/dialysis-machine

---

## 🎨 UI Elements Reference

### **Status Indicators:**

| Color | Meaning |
|-------|---------|
| 🟢 Green | Active, Completed, Available |
| 🟡 Yellow | Scheduled, Pending |
| 🔴 Red | Inactive, Cancelled, Maintenance |
| 🔵 Blue | Draft, In Progress |

### **Form Sections:**

- **Tabs:** Organize related fields
- **Sections:** Group fields within a tab
- **Columns:** Side-by-side field layout
- **Tables:** Child tables (grid view)

### **Field Icons:**

- 🔗 Link field (references another DocType)
- 📅 Date/DateTime field
- ✅ Checkbox field
- #️⃣ Number field
- 📄 Text field
- 📋 Select dropdown

---

## 🧪 Advanced Testing Scenarios

### **Scenario 1: Complete Patient Journey**

1. Create new patient
2. Schedule appointment for patient
3. Assign machine to appointment (if field exists)
4. Mark appointment as "Checked In"
5. View patient's appointment history

### **Scenario 2: Machine Maintenance Workflow**

1. Open machine DM-001
2. Change status to "Maintenance"
3. Set "Next Maintenance Due" date
4. Save machine
5. Try to assign this machine to appointment (should show warning/prevent)

### **Scenario 3: Bulk Operations**

1. Go to Patient list
2. Select multiple patients (checkboxes)
3. Click "Actions" dropdown
4. Try bulk operations (e.g., Export, Print)

---

## 🚀 What to Try Next

### **Immediate Actions:**
- ✅ Create 2-3 more patients
- ✅ Schedule appointments for the week
- ✅ Update machine maintenance dates
- ✅ Test all validations (try invalid data)
- ✅ Explore filter combinations

### **Tomorrow:**
- Build Clinical Operations (Dialysis Sessions)
- Create custom reports
- Add dashboard charts
- Setup user roles and permissions

---

## 💡 Pro Tips

1. **Use Awesome Bar:** Fastest way to navigate (Ctrl+K)
2. **Bookmark Frequently Used:** Right-click → Add to Favorites
3. **Learn Shortcuts:** Hover over buttons to see shortcuts
4. **Customize Views:** Every list can be customized to your needs
5. **Check Logs:** Menu → View Logs to see all changes

---

## 📞 Help & Support

**If something doesn't work:**
1. Check browser console (F12) for JavaScript errors
2. Check Frappe logs: `frappe-bench/logs/`
3. Use `bench --site frappe.local console` for debugging
4. Review the TESTING_GUIDE.md for common issues

---

## ✅ Exploration Checklist

Track your progress:

- [ ] Logged in successfully
- [ ] Viewed all 3 DocTypes (Patient, Appointment, Machine)
- [ ] Created at least 1 new patient
- [ ] Created at least 1 new appointment
- [ ] Tested filters and search
- [ ] Tried custom buttons
- [ ] Exported data to Excel
- [ ] Used Awesome Bar shortcuts
- [ ] Customized a list view
- [ ] Tested form validations

---

**🎉 Once you complete this walkthrough, you'll be fully comfortable with the Dialysis Center Management System UI!**

**Estimated Time:** 30-40 minutes for complete walkthrough

---

*Created: 2026-02-19*  
*App Version: 0.0.1*  
*Framework: Frappe v15.100.1*
