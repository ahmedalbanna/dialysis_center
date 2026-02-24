# Phase 4 Quick Reference Guide
## Workflows & Automation for Dialysis Center

---

## 📋 Five Workflows at a Glance

### 1. Appointment Workflow
```
Draft → Scheduled → Check-In → In-Progress → Completed ✓
                          ↓
                       Cancelled ✗
```
**Auto-Actions**: Creates dialysis session on check-in, sends notifications
**Key Validations**: Machine availability, patient status, no double-booking

### 2. Dialysis Session Workflow
```
Draft → In-Progress → Completed ✓
   ↓                      ↓
   └─→ Cancelled ✗ ←──────┘
```
**Auto-Actions**: Event logging, vital signs tracking, medication recording
**Key Validations**: Machine availability, patient status

### 3. Invoice Workflow
```
Draft → Submitted → Partially Paid → Paid ✓
   ↓         ↓              ↓
   └────────→ Cancelled ✗ ←─┘
```
**Auto-Actions**: Creates payment records, issues refunds, sends reminders
**Conditional Logic**: Invoices > 5000 require manager approval to cancel

### 4. Lab Test Workflow
```
Draft → Submitted → Results Received → Reviewed ✓
```
**Auto-Actions**: Creates lab result record, notifies doctor
**Key Validations**: Patient exists, test parameters valid

### 5. Insurance Claim Workflow
```
Draft → Submitted → Pending → Approved ✓
                         ↓
                    Rejected ✗
                         ↓
                    Cancelled ✗
```
**Auto-Actions**: Routes to insurance provider, sends notifications
**Key Validations**: Patient, provider, and amount required

---

## 🔧 Hooks Quick Reference

### Appointment Hooks
```python
before_insert  → Set defaults (status, priority, type, duration)
before_save    → Normalize notes, calculate end time
on_submit      → Update status, log event, send notification
on_cancel      → Cancel session, refund, send notification
```

### Dialysis Session Hooks
```python
before_insert  → Set defaults (status, start time)
before_save    → Normalize notes, calculate duration
on_submit      → Log start event, create event log, update appointment
on_cancel      → Log cancellation, reverse charges, create event log
```

### Invoice Hooks
```python
before_insert  → Set defaults (status, payment status, dates)
before_save    → Normalize notes, calculate totals, update payment status
on_submit      → Log submission, send notification, update session
on_cancel      → Process refunds, reverse entries, update session
```

### Lab Test Hooks
```python
before_insert  → Set defaults (status, test date)
before_save    → Normalize notes
on_submit      → Log submission, create result record, notify doctor
```

### Insurance Claim Hooks
```python
before_insert  → Set defaults (status, submission date)
before_save    → Normalize notes, calculate amounts
on_submit      → Log submission, send notification to provider
on_cancel      → Log cancellation, clear invoice reference
```

---

## ⏰ Scheduled Tasks Summary

### Daily Tasks (Run at 6-10 AM)
1. **daily_invoice_reminders** - Overdue and upcoming payment reminders
2. **daily_equipment_maintenance_alerts** - Equipment maintenance due within 7 days
3. **daily_lab_result_notifications** - Notify doctors of available results
4. **daily_patient_followup_tasks** - Create follow-up tasks for completed sessions
5. **daily_patient_vitals_alert** - Alert doctors of abnormal vitals from previous day

### Weekly Tasks (Run on Monday 8-9 AM)
1. **weekly_equipment_status_report** - Equipment status summary by count
2. **weekly_invoice_aging_report** - Invoice aging by category (0-30, 30-60, 60-90, 90+)

### Monthly Tasks (Run 1st of month)
1. **monthly_machine_performance_report** - Machine utilization and performance metrics
2. **monthly_patient_treatment_compliance** - Treatment compliance tracking and alerts

---

## 📊 Audit Logging Events

### Workflow Events
- State transitions with before/after values
- User performing transition
- Timestamp with microsecond precision
- Notes/comments

### Session Events
- Session started/completed/cancelled
- Abnormal vital signs
- Machine issues
- Medication administration
- Complication tracking

### Billing Events
- Invoice created
- Payment received (full or partial)
- Refund issued
- Invoice cancelled

### Access Events
- Document viewed/edited/deleted
- User and IP address
- Timestamp

---

## 🎯 Implementation Checklist

### Pre-Deployment
- [ ] Review all workflow definitions
- [ ] Test hooks in development
- [ ] Set up email templates for notifications
- [ ] Configure scheduler for background tasks
- [ ] Set up audit logging DocTypes

### Deployment
- [ ] Create audit DocTypes: `frappe_console > from dialysis_center.workflows.audit_doctypes import create_audit_doctypes > create_audit_doctypes()`
- [ ] Create workflows: `frappe_console > from dialysis_center.workflows.workflow_definitions import create_all_workflows > create_all_workflows()`
- [ ] Clear cache: `bench clear-cache`
- [ ] Build assets: `bench build`
- [ ] Restart services: `bench restart`

### Post-Deployment
- [ ] Verify workflows are created (Setup → Workflow)
- [ ] Test appointment creation and state transitions
- [ ] Test session creation and vital tracking
- [ ] Test invoice submission and payment recording
- [ ] Verify scheduled tasks are registered
- [ ] Test email notifications
- [ ] Verify audit logs are being created

---

## 💡 Usage Examples

### Creating an Appointment
```python
apt = frappe.get_doc({
    "doctype": "Appointment",
    "patient": "PATIENT-001",
    "appointment_date": "2026-02-20",
    "appointment_time": "09:00:00",
    "machine": "MACHINE-001"
})
apt.insert()
# Status automatically set to Draft

# Schedule appointment
frappe.workflow.apply_workflow(apt, action="Schedule")
# Status changed to Scheduled, notification sent to patient
```

### Recording Session Vitals
```python
from dialysis_center.workflows.audit_logging import SessionEventLogger

SessionEventLogger.log_vital_reading(
    session_name="DSESSION-2026-00001",
    patient="PATIENT-001",
    systolic=145,
    diastolic=85,
    pulse=75,
    temperature=37.2,
    notes="Pre-dialysis assessment"
)
# If abnormal, alert is logged automatically
```

### Processing Invoice Payment
```python
inv = frappe.get_doc("Invoice", "INV-2026-00001")
inv.paid_amount = 500  # Partial payment
inv.save()
# Status auto-updated to "Partially Paid"
# Payment record created
# Audit trail logged
```

### Getting Audit Trail
```python
from dialysis_center.workflows.audit_logging import get_document_audit_trail

audit = get_document_audit_trail("Invoice", "INV-2026-00001")

# View workflow transitions
for event in audit["workflow_events"]:
    print(f"{event.old_state} → {event.new_state} by {event.transition_user}")

# View all changes
for change in audit["field_changes"]:
    print(f"{change.field_name}: {change.old_value} → {change.new_value}")

# View access logs
for access in audit["access_logs"]:
    print(f"Accessed by {access.access_user} at {access.access_timestamp}")
```

---

## ⚙️ Configuration Reference

### Workflow Definitions Location
`dialysis_center/workflows/workflow_definitions.py`

### Hooks Location
- `dialysis_center/workflows/hooks_automation.py`
- `dialysis_center/hooks.py` (doc_events and scheduler_events)

### Scheduled Tasks Location
`dialysis_center/workflows/scheduled_tasks.py`

### Audit Logging Location
`dialysis_center/workflows/audit_logging.py`

### DocType Schemas Location
`dialysis_center/workflows/audit_doctypes.py`

---

## 🚨 Troubleshooting

### Issue: Workflows not showing
**Solution**: 
1. Verify in database: `frappe.db.count("Workflow")`
2. Check DocType has workflow_state field
3. Clear cache: `bench clear-cache`

### Issue: Hooks not executing
**Solution**:
1. Verify hook path in hooks.py matches function
2. Check function signature: `def func_name(doc, method):`
3. Test: `frappe.get_doc(...).insert()`

### Issue: Scheduled tasks not running
**Solution**:
1. Check scheduler: `ps aux | grep scheduler`
2. Verify in hooks.py scheduler_events
3. Test manually: `bench scheduler trigger daily_invoice_reminders`

### Issue: Notifications not sending
**Solution**:
1. Check email settings: Setup → Email Account
2. Test email: `frappe.sendmail(...)`
3. Check logs: `tail -f frappe-bench/logs/`

---

## 📚 DocTypes Created

### Audit Trail DocTypes
1. **Workflow Event Log** - Tracks state transitions
2. **Field Change Log** - Tracks field changes
3. **Session Event Log** - Tracks session activities
4. **Session Vital Reading** - Vital signs records
5. **Billing Audit Log** - Financial transactions
6. **Invoice Reminder Log** - Payment reminders sent
7. **Payment Record** - Payment and refund records

---

## 🔐 Security Features

✅ **Role-Based Access Control**
- Different roles can perform different transitions
- Invoice cancellation > 5000 requires manager approval
- Doctor-only session cancellation after start

✅ **Audit Trail**
- All actions logged with user and timestamp
- Field changes tracked before/after
- Access logs for compliance

✅ **Data Integrity**
- Validation before state transitions
- Rollback on error
- Referential integrity checks

✅ **Compliance**
- HIPAA-ready audit logging
- Financial transaction tracking
- Clinical documentation requirements

---

## 📞 Support & Documentation

- **Full Implementation Guide**: `PHASE_4_WORKFLOWS_IMPLEMENTATION.md`
- **API Documentation**: `DIALYSIS_CENTER_API_SPECIFICATION.yaml`
- **Technical Design**: `DIALYSIS_CENTER_TECHNICAL_DESIGN.md`
- **Workflow-Wizard Memory**: `.rovodev/subagents/memory/Workflow-Wizard.memory.md`

---

**Version**: 1.0
**Last Updated**: February 19, 2026
**Status**: Production Ready ✅
