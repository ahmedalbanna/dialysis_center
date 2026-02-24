# Automated Development Data Seeding

This document explains how to use the automated test data seeding system for the Dialysis Center app.

## Overview

The seeding system provides:
- **Automated fixture loading** on app installation
- **Custom bench commands** for data management
- **Optional auto-seeding** for development environments
- **Graceful error handling** for missing DocTypes

---

## Quick Start

### 1. Seed Test Data Manually

```bash
# Seed 50 test patients and machines
bench --site frappe.local dialysis-center seed-data

# Seed with clearing existing data first
bench --site frappe.local dialysis-center seed-data --clear

# Seed custom number of patients
bench --site frappe.local dialysis-center seed-data --patients 100
```

### 2. Clear Test Data

```bash
# Clear all test data (with confirmation)
bench --site frappe.local dialysis-center clear-test-data

# Skip confirmation prompt
bench --site frappe.local dialysis-center clear-test-data --confirm
```

### 3. View Database Statistics

```bash
# Show current data counts
bench --site frappe.local dialysis-center show-stats
```

---

## Automated Seeding on Installation

The app automatically loads fixtures (roles, treatment templates) on installation.

### Enable Auto-Seeding of Test Data

Add to `site_config.json`:

```json
{
  "developer_mode": 1,
  "dialysis_center_auto_seed_data": true
}
```

Then reinstall the app:

```bash
bench --site frappe.local reinstall
```

---

## Auto-Seed After Each Migration (Optional)

To automatically seed data after running migrations (useful for development):

1. Edit `dialysis_center/hooks.py`
2. Uncomment the line:
   ```python
   after_migrate = "dialysis_center.fixtures.seed_dev_data.check_and_seed_if_empty"
   ```
3. This will check if the database is empty after each migration and seed if needed

---

## Python API Usage

### Seed Data Programmatically

```python
from dialysis_center.fixtures.seed_dev_data import seed_development_data

# Seed without clearing existing data
seed_development_data(clear_existing=False)

# Clear and reseed
seed_development_data(clear_existing=True)
```

### Check and Auto-Seed

```python
from dialysis_center.fixtures.seed_dev_data import check_and_seed_if_empty

# Only seeds if database is empty
check_and_seed_if_empty()
```

### Clear Test Data

```python
from dialysis_center.tests.clear_test_data import clear_test_data

clear_test_data()
```

### Use Factories Directly

```python
from dialysis_center.tests.factories.patient_factory import PatientFactory

# Create a single patient
patient = PatientFactory.create(patient_id="PT-001")

# Create batch of patients
patients = PatientFactory.create_batch(count=50)

# Create patient with medical history
patient = PatientFactory.create_with_medical_history()
```

---

## What Gets Seeded

### Fixtures (Loaded on Install)
- **10 Roles**: Administrator, Doctor, Nurse, Technician, Receptionist, Billing Clerk, Lab Technician, Inventory Manager, Manager, Viewer
- **5 Treatment Templates**: Standard Hemodialysis, Short Hemodialysis, Hemodiafiltration, Low Blood Flow Protocol, High Efficiency Protocol

### Test Data (Manual Seeding)
- **50 Patients** (default, configurable)
- **8 Dialysis Machines**
- **Appointments** (if Healthcare Practitioner exists)
- **Dialysis Sessions** (if Appointment exists)
- **Lab Results** (if Lab Result DocType exists)
- **Invoices** (if Invoice DocType is customized)

---

## Error Handling

The seeding system gracefully handles missing DocTypes:

```
⚠️  Skipping staff creation (DocType not available)
⚠️  Skipping appointments (DocType not available)
⚠️  Skipping sessions (DocType not available)
✅ Created 55 patients
✅ Created 8 dialysis machines
```

This allows you to seed data even if all DocTypes aren't created yet.

---

## Configuration Options

### Site Config Options

Add to `frappe-bench/sites/frappe.local/site_config.json`:

```json
{
  "developer_mode": 1,
  "dialysis_center_auto_seed_data": true,
  "dialysis_center_clear_on_uninstall": true
}
```

**Options:**
- `developer_mode`: Enable developer mode (required for auto-seeding)
- `dialysis_center_auto_seed_data`: Auto-seed on installation (default: false)
- `dialysis_center_clear_on_uninstall`: Clear test data on uninstall (default: false)

---

## Console Commands

### From Bench Console

```bash
bench --site frappe.local console
```

```python
# In console:
from dialysis_center.tests.generate_test_data import generate_complete_test_data
generate_complete_test_data()

# Or use the seed wrapper
from dialysis_center.fixtures.seed_dev_data import seed_development_data
seed_development_data(clear_existing=True)
```

---

## File Structure

```
dialysis_center/
├── fixtures/
│   ├── role.json                    # Role fixtures
│   ├── treatment_template.json      # Treatment template fixtures
│   ├── load_fixtures.py             # Fixture loader
│   ├── seed_dev_data.py             # Dev data seeding wrapper
│   └── README_DEV_DATA_SEEDING.md   # This file
├── tests/
│   ├── factories/
│   │   ├── patient_factory.py       # Patient test data factory
│   │   ├── appointment_factory.py   # Appointment factory
│   │   └── session_factory.py       # Session factory
│   ├── generate_test_data.py        # Main test data generator
│   └── clear_test_data.py           # Test data cleanup
├── commands.py                      # Custom bench commands
├── install.py                       # Installation hooks
└── hooks.py                         # App hooks configuration
```

---

## Troubleshooting

### "Module import failed for Healthcare Practitioner"

This is expected if the DocType hasn't been created yet. The system will skip creating appointments and sessions.

### "mobile_number is required"

The Patient DocType requires a mobile number. The factory skips validation using `ignore_mandatory=True`.

### Commands not found

Restart bench after creating new commands:

```bash
bench restart
```

### Clear all data and reseed

```bash
bench --site frappe.local dialysis-center clear-test-data --confirm
bench --site frappe.local dialysis-center seed-data
```

---

## Best Practices

### For Development

1. **Use auto-seeding on fresh installs**: Set `dialysis_center_auto_seed_data: true`
2. **Don't auto-seed after migrations**: Keep `after_migrate` commented unless needed
3. **Clear and reseed periodically**: Keep test data fresh

### For Production

1. **Never enable auto-seeding**: Only load fixtures, not test data
2. **Don't install test data**: Use real patient data
3. **Keep fixtures minimal**: Only essential roles and templates

### For Testing

1. **Use factories in unit tests**: Create specific test scenarios
2. **Clean up after tests**: Delete test data in tearDown
3. **Use unique IDs**: Avoid conflicts with `random_string()`

---

## Performance

**Seeding 50 patients:**
- Time: ~1-2 seconds
- Database commits: 1 per patient
- Concurrent safe: No (use transactions)

**Clearing test data:**
- Time: <1 second
- Deletes in dependency order
- Irreversible: Always confirm first

---

## Next Steps

Once you create the missing DocTypes, the seeding system will automatically:
- Generate appointments (when Healthcare Practitioner exists)
- Create dialysis sessions (when Appointment exists)
- Add lab results (when Lab Result exists)
- Generate invoices (when Invoice is customized)

No code changes needed - the error handling will adapt automatically!

---

**Last Updated:** 2026-02-19  
**App Version:** dialysis_center v0.0.1  
**Frappe Version:** v15.100.1
