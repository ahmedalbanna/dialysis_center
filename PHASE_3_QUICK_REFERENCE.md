# Phase 3: Quick Reference Guide

## File Locations & Registration

### JavaScript Files Created
```
dialysis_center/public/js/
├── appointment.js                    # Appointment scheduling form
├── dialysis_session_enhanced.js      # Session monitoring (replaces dialysis_session.js)
├── invoice.js                        # Invoice & payment tracking
├── lab_test.js                       # Laboratory test results
├── medication.js                     # Medication inventory
├── staff.js                          # Staff management
├── dialysis_machine.js               # Equipment management
└── patient.js                        # (already exists, enhanced)
```

### CSS Files Created
```
dialysis_center/public/css/
└── responsive_design.scss            # Mobile-first responsive styles
```

---

## Form Features at a Glance

| DocType | Key Features | Status Indicators | Custom Buttons |
|---------|-------------|------------------|----------------|
| **Patient** | Medical history, vitals chart, session summary | Active/Inactive/Deceased | View Dashboard, Schedule Appointment |
| **Appointment** | Availability checker, check-in, reschedule | Scheduled/Confirmed/Checked In/Completed | Check In, Reschedule, Cancel |
| **Dialysis Session** | Real-time vitals, event log, timeline | Scheduled/In Progress/Completed/Emergency Stop | Start Session, End Session, Log Event |
| **Invoice** | Payment tracker, printable preview, history | Unpaid/Partial/Paid | Print, Record Payment, Send Email |
| **Lab Test** | Abnormal flagging, trending, history | Pending/Completed/Reviewed | View Trending, Mark Complete |
| **Staff** | Qualifications, schedule, performance | Active/Inactive/On Leave | View Schedule, Performance Metrics |
| **Dialysis Machine** | Maintenance tracking, service history | Operational/Out of Service/Maintenance | Schedule Maintenance, Record Service |
| **Medication** | Stock tracking, expiration alerts, history | Good/Low Stock/Out of Stock | Add Stock, View Stock History |

---

## Validation Rules Summary

### Patient
- National ID must be unique
- Email must be valid format
- Age calculated from DOB

### Appointment
- Date cannot be in past
- Cannot double-book patient
- Time must be within available slots

### Dialysis Session
- Requires patient and appointment
- Start time before end time
- Status transitions are sequential

### Invoice
- Subtotal = sum of items
- Total = subtotal + tax - discount
- Payment cannot exceed total

### Lab Test
- Test date cannot be future
- Parameter values required
- Abnormal values auto-flagged

### Staff
- Email must be valid
- Phone must be valid format
- Designation required

### Dialysis Machine
- Machine name required
- Status tracks operational state
- Maintenance alerts if overdue 90+ days

### Medication
- Expiration date cannot be past
- Stock cannot be negative
- Low stock alerts at minimum level

---

## Dialog/Modal Quick Reference

### Appointment
- **Reschedule Dialog**: New date, time, reason
- **Cancel Dialog**: Confirmation prompt

### Dialysis Session
- **Vital Signs Dialog**: BP, HR, Temp, RR, O2 Sat, Notes
- **Event Log Dialog**: Type, description, severity, intervention
- **End Session Dialog**: End time, reviewer, notes, tolerance

### Invoice
- **Payment Dialog**: Amount, date, method, reference, notes
- **Bulk Payment Dialog**: Date, method, reference, total amount
- **Preview Dialog**: Full invoice HTML preview
- **Email Dialog**: Recipient, message body

### Lab Test
- **Trend Analysis Dialog**: 6-month parameter trends

### Staff
- **Schedule Dialog**: Weekly schedule view
- **Performance Dialog**: Metrics, evaluations, ratings

### Dialysis Machine
- **Maintenance Dialog**: Date, type, reason
- **Service Dialog**: Date, type, description, performer

### Medication
- **Stock Dialog**: Quantity, date, expiration, batch, supplier, cost
- **Bulk Adjustment Dialog**: Type, quantity, reason

---

## Status Color Coding

### Universal Status Colors
```
Green:   Active, Operational, Good, Success, Completed, Confirmed, Paid
Orange:  Warning, Pending, Low Stock, Rescheduled, Maintenance, Partial
Red:     Error, Inactive, Out of Service, Cancelled, Unpaid, Danger
Blue:    Info, In Progress, Checked In, Processing
Gray:    Retired, Discontinued, Inactive
```

---

## API Methods Called by Frontend

### Appointment
- `dialysis_center.api.appointment.check_availability`
- `dialysis_center.api.appointment.check_conflicts`
- `dialysis_center.api.appointment.check_in`
- `dialysis_center.api.appointment.reschedule`
- `dialysis_center.api.appointment.cancel`

### Dialysis Session
- `dialysis_center.api.dialysis_session.start_session`
- `dialysis_center.api.dialysis_session.end_session`
- `dialysis_center.api.dialysis_session.emergency_stop`
- `dialysis_center.api.dialysis_session.add_vital_signs`
- `dialysis_center.api.dialysis_session.log_session_event`
- `dialysis_center.api.dialysis_session.get_vital_signs`
- `dialysis_center.api.dialysis_session.get_session_events`
- `dialysis_center.api.dialysis_session.get_session_summary`

### Invoice
- `dialysis_center.api.invoice.get_payment_history`
- `dialysis_center.api.invoice.record_payment`
- `dialysis_center.api.invoice.record_bulk_payments`
- `dialysis_center.api.invoice.send_invoice_email`
- `dialysis_center.api.invoice.process_refund`

### Lab Test
- `dialysis_center.api.lab_test.get_test_history`
- `dialysis_center.api.lab_test.get_parameter_trend`
- `dialysis_center.api.lab_test.mark_complete`

### Staff
- `dialysis_center.api.staff.get_designation_permissions`
- `dialysis_center.api.staff.get_staff_schedule`
- `dialysis_center.api.staff.get_performance_metrics`
- `dialysis_center.api.staff.update_staff_status`

### Dialysis Machine
- `dialysis_center.api.dialysis_machine.schedule_maintenance`
- `dialysis_center.api.dialysis_machine.record_service`
- `dialysis_center.api.dialysis_machine.get_maintenance_history`
- `dialysis_center.api.dialysis_machine.update_status`
- `dialysis_center.api.dialysis_machine.schedule_bulk_maintenance`

### Medication
- `dialysis_center.api.medication.add_stock`
- `dialysis_center.api.medication.get_stock_history`
- `dialysis_center.api.medication.bulk_stock_adjustment`

---

## Mobile Breakpoints

```
Mobile:  < 576px   (Phones - single column, full width buttons)
Tablet:  576-768px (Tablets - 2 columns)
Desktop: > 768px   (Desktops - 3+ columns)
```

### Responsive Changes
- Forms stack vertically on mobile
- Buttons become full width on mobile
- Tables scroll horizontally on mobile
- Modals take 95% width on mobile
- Font sizes increase slightly on mobile for readability

---

## Performance Optimization Tips

### Reduce API Calls
```javascript
// Bad: Separate calls
frm.doc.items.forEach(item => {
	frappe.call({method: '...', args: {item: item.name}});
});

// Good: Batch call
frappe.call({method: '...', args: {items: frm.doc.items.map(i => i.name)}});
```

### Cache Frequently Accessed Data
```javascript
// Check cache first
let data = frappe.cache.get_value('cache_key');
if (!data) {
	frappe.call({method: '...', callback: function(r) {
		frappe.cache.set_value('cache_key', r.message, 3600);
	}});
}
```

### Debounce Frequent Events
```javascript
const search_fn = frappe.debounce(function() {
	// Search logic here
}, 300);

search_field: function(frm) {
	search_fn();
}
```

---

## Common Customization Patterns

### Add Custom Button
```javascript
frm.add_custom_button(__('Button Label'), function() {
	// Action here
}, __('Button Group'));
```

### Update Field Display
```javascript
// Make read-only
frm.set_df_property('field_name', 'read_only', 1);

// Hide field
frm.set_df_property('field_name', 'hidden', 1);

// Make mandatory
frm.set_df_property('field_name', 'reqd', 1);

// Refresh display
frm.refresh_field('field_name');
```

### Show Alert/Message
```javascript
// Info
frappe.msgprint(__('Information message'));

// Warning
frappe.msgprint({
	title: __('Title'),
	message: __('Message text'),
	indicator: 'orange'
});

// Error
frappe.throw(__('Error message'));
```

### Create Dialog
```javascript
const dialog = new frappe.ui.Dialog({
	title: __('Dialog Title'),
	fields: [
		{fieldtype: 'Data', fieldname: 'field1', label: __('Label')}
	],
	primary_action_label: __('Save'),
	primary_action(values) {
		// Handle submission
		dialog.hide();
	}
});
dialog.show();
```

---

## Testing Checklist

### Form Testing
- [ ] Save document successfully
- [ ] All validations trigger correctly
- [ ] Field dependencies work
- [ ] Custom buttons appear
- [ ] Status indicators update

### List View Testing
- [ ] Filters work correctly
- [ ] Bulk actions select items
- [ ] Formatters display properly
- [ ] Quick filters work

### Mobile Testing
- [ ] Forms readable at 320px width
- [ ] Touch targets are ≥ 44x44px
- [ ] No horizontal scroll needed
- [ ] Modals fit within viewport
- [ ] Buttons don't overlap

### Cross-Browser Testing
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

---

## Troubleshooting Quick Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Form not loading | Script not registered | Check hooks.py doctype_js |
| Field not updating | Missing frm.refresh_field() | Add refresh after set_value |
| Dialog not showing | Missing dialog.show() | Ensure dialog.show() is called |
| Mobile layout broken | Wrong breakpoint | Check $mobile variable in SCSS |
| API call failing | Missing API method | Implement in api/module.py |
| Validation not working | Logic error in validate() | Check console for errors |
| Slow form load | Too many API calls | Implement caching/debouncing |

---

## Next Steps for Implementation

1. **Register Forms in hooks.py**:
```python
doctype_js = {
	"Appointment": "public/js/appointment.js",
	"Dialysis Session": "public/js/dialysis_session_enhanced.js",
	"Invoice": "public/js/invoice.js",
	"Lab Test": "public/js/lab_test.js",
	"Medication": "public/js/medication.js",
	"Staff": "public/js/staff.js",
	"Dialysis Machine": "public/js/dialysis_machine.js"
}
```

2. **Register CSS**:
```python
app_include_css = [
	"dialysis_center:///public/css/responsive_design.css"
]
```

3. **Implement Backend APIs** (See API-Whitelister for implementation)

4. **Test All Forms** (See Testing Checklist above)

5. **Deploy to Production**:
```bash
bench build
bench --site frappe.local clear-cache
bench --site frappe.local migrate
```

---

## Support & Documentation

- **Comprehensive Guide**: PHASE_3_FRONTEND_IMPLEMENTATION_GUIDE.md
- **Frontend Design**: DIALYSIS_CENTER_FRONTEND_DESIGN.md
- **API Specification**: DIALYSIS_CENTER_API_SPECIFICATION.yaml
- **Technical Design**: DIALYSIS_CENTER_TECHNICAL_DESIGN.md

