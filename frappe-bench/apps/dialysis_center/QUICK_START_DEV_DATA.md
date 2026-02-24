# Dialysis Center - Quick Start: Development Data

## 🚀 Quick Commands

### Seed Test Data
```bash
bench --site frappe.local dialysis-center seed-data
```

### View Database Stats
```bash
bench --site frappe.local dialysis-center show-stats
```

### Clear Test Data
```bash
bench --site frappe.local dialysis-center clear-test-data
```

---

## 📊 Current Database Status

Run `show-stats` to see:
```
📊 Database Statistics for: frappe.local
==================================================
Patients                 :    55
Dialysis Machines        :     8
Appointments             :     0
Dialysis Sessions        :     0
Treatment Templates      :     5
Roles                    :    37
==================================================
```

---

## 🔧 Enable Auto-Seeding on Install

Add to `frappe-bench/sites/frappe.local/site_config.json`:

```json
{
  "developer_mode": 1,
  "dialysis_center_auto_seed_data": true
}
```

Then reinstall:
```bash
bench --site frappe.local reinstall
```

---

## 📚 Full Documentation

See `dialysis_center/fixtures/README_DEV_DATA_SEEDING.md` for complete documentation.

---

## ✅ What's Already Loaded

- ✅ **55 Patients** - Test patient records
- ✅ **8 Dialysis Machines** - Available for scheduling
- ✅ **10 Roles** - Complete permission system
- ✅ **5 Treatment Templates** - Clinical protocols

---

## ⚠️ What's Pending (Requires DocTypes)

- ⏳ **Appointments** - Needs Healthcare Practitioner DocType
- ⏳ **Dialysis Sessions** - Needs Appointment DocType
- ⏳ **Lab Results** - Needs Lab Result DocType
- ⏳ **Invoices** - Needs Invoice customization

Once you create these DocTypes, run `seed-data` again and they'll be automatically generated!

---

**Quick Tip:** Bookmark this file for easy reference during development! 🔖
