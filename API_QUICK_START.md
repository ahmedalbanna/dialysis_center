# Dialysis Center API - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Authentication

All APIs require Frappe authentication. Use your site URL and credentials:

```bash
# Set authentication
export AUTH="token YOUR_API_KEY:YOUR_API_SECRET"
export BASE_URL="http://localhost:8000"
```

### Basic API Call Pattern

```bash
curl -X GET "$BASE_URL/api/method/dialysis_center.api.patient.get_patient_list" \
  -H "Authorization: $AUTH"
```

---

## 📋 Most Used APIs

### 1. Patient Management

**Get all patients:**
```bash
curl "$BASE_URL/api/method/dialysis_center.api.patient.get_patient_list?page_length=20"
```

**Get specific patient:**
```bash
curl "$BASE_URL/api/method/dialysis_center.api.patient.get_patient_details?patient_id=P-001"
```

**Create patient:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.patient.create_patient" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "John Doe",
    "dob": "1980-01-15",
    "blood_group": "O+",
    "phone": "1234567890",
    "email": "john@example.com"
  }'
```

---

### 2. Appointments

**Create appointment:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.appointment.create_appointment" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P-001",
    "appointment_date": "2026-02-20",
    "machine_id": "M-001",
    "duration": 240
  }'
```

**Check machine availability:**
```bash
curl "$BASE_URL/api/method/dialysis_center.api.appointment.check_machine_availability?machine_id=M-001&date=2026-02-20"
```

**Check in patient:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.appointment.check_in_appointment" \
  -H "Content-Type: application/json" \
  -d '{"appointment_id": "APT-001"}'
```

---

### 3. Dialysis Sessions

**Start session:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.session.start_session" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "DS-001"}'
```

**Record vital signs:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.session.record_vital_signs" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "DS-001",
    "vital_signs_data": {
      "bp_systolic": 140,
      "bp_diastolic": 90,
      "heart_rate": 75,
      "temperature": 37.0,
      "oxygen_saturation": 98
    }
  }'
```

**End session:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.session.end_session" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "DS-001",
    "vital_signs": {
      "bp_systolic": 135,
      "bp_diastolic": 88
    }
  }'
```

---

### 4. Billing

**Create invoice:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.billing.create_invoice" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P-001",
    "session_ids": ["DS-001", "DS-002"]
  }'
```

**Record payment:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.billing.record_payment" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id": "INV-001",
    "amount": 1000,
    "payment_method": "Cash"
  }'
```

**Get outstanding invoices:**
```bash
curl "$BASE_URL/api/method/dialysis_center.api.billing.get_outstanding_invoices?patient_id=P-001"
```

---

### 5. Lab Tests

**Create lab test:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.lab.create_lab_test" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P-001",
    "test_type": "Creatinine",
    "test_date": "2026-02-19"
  }'
```

**Submit test results:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.lab.submit_lab_test" \
  -H "Content-Type: application/json" \
  -d '{
    "lab_test_id": "LT-001",
    "results": [
      {
        "parameter_name": "Creatinine",
        "result_value": 1.2,
        "normal_range": "0.6-1.2",
        "unit": "mg/dL"
      }
    ]
  }'
```

---

### 6. Inventory

**Get low stock items:**
```bash
curl "$BASE_URL/api/method/dialysis_center.api.inventory.get_low_stock_items"
```

**Record stock movement:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.inventory.create_stock_movement" \
  -H "Content-Type: application/json" \
  -d '{
    "medication_id": "MED-001",
    "quantity": 50,
    "movement_type": "In",
    "notes": "Stock received from vendor"
  }'
```

---

### 7. Equipment

**Get machines due maintenance:**
```bash
curl "$BASE_URL/api/method/dialysis_center.api.equipment.get_machines_due_maintenance"
```

**Record maintenance:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.equipment.record_machine_maintenance" \
  -H "Content-Type: application/json" \
  -d '{
    "machine_id": "M-001",
    "maintenance_date": "2026-02-19",
    "maintenance_type": "Preventive",
    "notes": "Regular maintenance"
  }'
```

---

### 8. Insurance

**Create insurance claim:**
```bash
curl -X POST "$BASE_URL/api/method/dialysis_center.api.insurance.create_insurance_claim" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P-001",
    "invoice_id": "INV-001",
    "claim_amount": 5000
  }'
```

**Get patient claims:**
```bash
curl "$BASE_URL/api/method/dialysis_center.api.insurance.get_patient_claims?patient_id=P-001"
```

---

## 📊 Response Format

All APIs return:

```json
{
  "status": "success",
  "data": {
    /* API-specific data */
  },
  "message": "Descriptive message"
}
```

---

## 🔍 Common Query Parameters

### Pagination
```bash
?start=0&page_length=20
```

### Filtering
```bash
?filters={"status":"Active","blood_group":"O+"}
```

### Date Filtering
```bash
?from_date=2026-01-01&to_date=2026-02-28
```

### Search
```bash
?search_term=Ahmed
```

---

## ⚠️ Error Responses

**Missing Required Parameter:**
```json
{
  "status": "error",
  "data": null,
  "message": "Patient ID is required"
}
```

**Permission Denied:**
```json
{
  "status": "error",
  "data": null,
  "message": "You do not have permission to view this patient"
}
```

**Not Found:**
```json
{
  "status": "error",
  "data": null,
  "message": "Patient not found"
}
```

---

## 🔐 Security Tips

1. **Never expose API keys** - Use environment variables
2. **Use HTTPS in production** - Ensure encrypted transmission
3. **Limit permissions** - Grant minimum required permissions
4. **Rotate keys regularly** - Update API credentials
5. **Monitor usage** - Check API logs for suspicious activity

---

## 🧪 Testing with Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

auth = (f"token {API_KEY}", API_SECRET)

# Get patients
response = requests.get(
    f"{BASE_URL}/api/method/dialysis_center.api.patient.get_patient_list",
    auth=auth
)
print(response.json())

# Create appointment
data = {
    "patient_id": "P-001",
    "appointment_date": "2026-02-20",
    "machine_id": "M-001"
}
response = requests.post(
    f"{BASE_URL}/api/method/dialysis_center.api.appointment.create_appointment",
    json=data,
    auth=auth
)
print(response.json())
```

---

## 🧪 Testing with JavaScript/Node.js

```javascript
const fetch = require('node-fetch');
const Base64 = require('js-base64').Base64;

const baseUrl = "http://localhost:8000";
const apiKey = "YOUR_API_KEY";
const apiSecret = "YOUR_API_SECRET";
const auth = Base64.encode(`token ${apiKey}:${apiSecret}`);

// Get patients
fetch(`${baseUrl}/api/method/dialysis_center.api.patient.get_patient_list`, {
  headers: { "Authorization": `Basic ${auth}` }
})
  .then(r => r.json())
  .then(data => console.log(data));

// Create appointment
fetch(`${baseUrl}/api/method/dialysis_center.api.appointment.create_appointment`, {
  method: "POST",
  headers: {
    "Authorization": `Basic ${auth}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    patient_id: "P-001",
    appointment_date: "2026-02-20",
    machine_id: "M-001"
  })
})
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## 📚 Complete API Documentation

See `PHASE_2_API_IMPLEMENTATION_GUIDE.md` for complete documentation of all 80+ APIs.

---

## 🆘 Troubleshooting

**API returns 404?**
- Check method path is correct
- Verify method is in `whitelisted_methods` in hooks.py
- Ensure Frappe is running

**Permission denied?**
- Check user has appropriate role
- Verify DocType permissions are set
- Check user's page permissions

**Slow response?**
- Use pagination with `page_length` parameter
- Add filters to reduce result set
- Check database indexes

**Invalid JSON?**
- Verify JSON syntax
- Check field names match API parameters
- Use proper date format (YYYY-MM-DD)

---

## 📞 Support

For issues:
1. Check API documentation
2. Review error message carefully
3. Check logs: `bench logs`
4. Enable debug mode: Set `developer_mode = 1`

---

## ✅ API Checklist

All 80+ APIs include:
- ✅ Standard response format
- ✅ Error handling
- ✅ Permission checks
- ✅ Input validation
- ✅ Pagination support
- ✅ API logging
- ✅ Documentation

---

**Last Updated:** February 19, 2026
**Status:** Production Ready ✅
