# Integration Specialist Memory File

## Quick Facts
- **Specialty**: Third-party integrations, payment gateways, email systems, webhooks, OAuth flows, API authentication, data synchronization, error handling
- **Primary Tools**: File creation, API testing (curl), webhook setup, authentication patterns
- **Common Tasks**: Payment gateway integration, external API sync, webhook handlers, OAuth setup, data import/export
- **Estimated Task Time**: 45-120 minutes per integration

---

## Core Integration Patterns

### Pattern 1: Webhook Implementation

**Scenario**: Sync order data to external fulfillment system when order is submitted

**Setup in hooks.py**:
```python
doc_events = {
	"Order": {
		"on_submit": "myapp.integrations.webhooks.on_order_submit"
	}
}
```

**Implementation**:
```python
# File: apps/myapp/myapp/integrations/webhooks.py

import requests
import json
from frappe import logger

def on_order_submit(doc, method):
	"""Webhook: Send order to fulfillment system"""
	
	# Get external API config
	api_key = frappe.db.get_single_value("Fulfillment Settings", "api_key")
	api_url = frappe.db.get_single_value("Fulfillment Settings", "api_url")
	
	if not api_key or not api_url:
		logger().warning("Fulfillment API not configured")
		return
	
	# Prepare payload
	payload = {
		"order_id": doc.name,
		"customer_name": doc.customer_name,
		"items": [{
			"product_id": item.product_code,
			"quantity": item.qty,
			"price": item.rate
		} for item in doc.items],
		"shipping_address": doc.shipping_address,
		"total": doc.grand_total
	}
	
	# Send webhook with retry logic
	try:
		response = requests.post(
			f"{api_url}/orders",
			json=payload,
			headers={
				"Authorization": f"Bearer {api_key}",
				"Content-Type": "application/json"
			},
			timeout=10
		)
		
		if response.status_code == 201:
			# Success - log it
			frappe.db.set_value("Order", doc.name, "fulfillment_id", response.json()["id"])
			log_integration_request(doc.name, "Fulfillment", "Success", response.text)
		else:
			# Failure - create retry job
			log_integration_request(doc.name, "Fulfillment", "Failed", response.text)
			frappe.enqueue("myapp.integrations.retry.retry_webhook", queue="long", 
				order_id=doc.name, retry_count=1)
			
	except requests.Timeout:
		log_integration_request(doc.name, "Fulfillment", "Timeout", "Request timeout")
		frappe.enqueue("myapp.integrations.retry.retry_webhook", queue="long",
			order_id=doc.name, retry_count=1)
	except Exception as e:
		frappe.log_error(f"Webhook error: {str(e)}", title="Order Fulfillment Webhook")
		log_integration_request(doc.name, "Fulfillment", "Error", str(e))

def log_integration_request(doc_name, service, status, response):
	"""Log webhook call for audit trail"""
	frappe.get_doc({
		"doctype": "Integration Log",
		"doc_type": "Order",
		"doc_name": doc_name,
		"service": service,
		"status": status,
		"response": response,
		"timestamp": frappe.utils.now_datetime()
	}).insert(ignore_permissions=True)
```

### Pattern 2: API Integration with Polling

**Scenario**: Sync customer data from external CRM hourly

**Setup in hooks.py**:
```python
scheduler_events = {
	"hourly": [
		"myapp.integrations.crm_sync.sync_customers_from_crm"
	]
}
```

**Implementation**:
```python
# File: apps/myapp/myapp/integrations/crm_sync.py

import requests
from datetime import datetime, timedelta

def sync_customers_from_crm():
	"""Sync customers from external CRM every hour"""
	
	# Get last sync time
	last_sync = frappe.db.get_single_value("CRM Settings", "last_sync_time") or \
		(datetime.now() - timedelta(hours=24)).isoformat()
	
	api_key = frappe.db.get_single_value("CRM Settings", "api_key")
	api_url = frappe.db.get_single_value("CRM Settings", "api_url")
	
	try:
		# Fetch changed customers since last sync
		response = requests.get(
			f"{api_url}/customers/changed",
			params={"since": last_sync},
			headers={"Authorization": f"Bearer {api_key}"},
			timeout=30
		)
		response.raise_for_status()
		
		customers = response.json()
		created = 0
		updated = 0
		failed = []
		
		for customer_data in customers:
			try:
				# Check if exists
				existing = frappe.db.exists("Customer", {"crm_id": customer_data["id"]})
				
				if existing:
					# Update existing
					doc = frappe.get_doc("Customer", existing)
					doc.customer_name = customer_data["name"]
					doc.phone = customer_data.get("phone")
					doc.email_id = customer_data.get("email")
					doc.save(ignore_permissions=True)
					updated += 1
				else:
					# Create new
					doc = frappe.get_doc({
						"doctype": "Customer",
						"customer_name": customer_data["name"],
						"crm_id": customer_data["id"],
						"phone": customer_data.get("phone"),
						"email_id": customer_data.get("email"),
						"customer_type": "Individual"
					})
					doc.insert(ignore_permissions=True)
					created += 1
					
			except Exception as e:
				failed.append({"id": customer_data["id"], "error": str(e)})
				frappe.log_error(f"Customer sync error for {customer_data['id']}: {str(e)}")
		
		# Update last sync time
		frappe.db.set_single_value("CRM Settings", "last_sync_time", datetime.now().isoformat())
		
		# Log summary
		frappe.logger().info(f"CRM Sync: {created} created, {updated} updated, {len(failed)} failed")
		
	except requests.RequestException as e:
		frappe.log_error(f"CRM API error: {str(e)}", title="CRM Sync Failed")

def retry_failed_syncs():
	"""Retry failed customer syncs"""
	failed_logs = frappe.get_all("Integration Log",
		filters={"service": "CRM", "status": "Failed", "retry_count": ("<", 3)},
		limit=50
	)
	
	for log in failed_logs:
		sync_single_customer(log.doc_name)
```

### Pattern 3: Payment Gateway Integration

**Scenario**: Process payment through Stripe

**Implementation**:
```python
# File: apps/myapp/myapp/integrations/payment.py

import stripe

def init_stripe():
	"""Initialize Stripe API"""
	stripe.api_key = frappe.db.get_single_value("Payment Settings", "stripe_secret_key")

@frappe.whitelist()
def create_payment_intent(order_id, amount):
	"""Create Stripe payment intent"""
	init_stripe()
	
	order = frappe.get_doc("Order", order_id)
	
	try:
		intent = stripe.PaymentIntent.create(
			amount=int(amount * 100),  # Convert to cents
			currency="usd",
			metadata={"order_id": order_id},
			description=f"Payment for {order_id}"
		)
		
		return {
			"status": "success",
			"client_secret": intent.client_secret,
			"amount": amount
		}
		
	except stripe.error.CardError as e:
		frappe.throw(f"Payment error: {e.user_message}")
	except stripe.error.RateLimitError:
		frappe.throw("Rate limit reached. Please try again.")
	except stripe.error.AuthenticationError:
		frappe.log_error("Stripe authentication failed")
		frappe.throw("Payment service error")

@frappe.whitelist()
def confirm_payment(order_id, payment_intent_id):
	"""Confirm payment and update order"""
	init_stripe()
	
	try:
		intent = stripe.PaymentIntent.retrieve(payment_intent_id)
		
		if intent.status == "succeeded":
			frappe.db.set_value("Order", order_id, {
				"payment_status": "Paid",
				"payment_id": payment_intent_id,
				"payment_date": frappe.utils.today()
			})
			
			# Trigger order completion workflow
			order = frappe.get_doc("Order", order_id)
			order.submit()
			
			return {"status": "success"}
		else:
			return {"status": "pending"}
			
	except Exception as e:
		frappe.log_error(f"Payment confirmation error: {str(e)}")
		frappe.throw("Failed to confirm payment")
```

### Pattern 4: OAuth2 Authentication

**Scenario**: Authenticate with Google to access user's calendar

**Implementation**:
```python
# File: apps/myapp/myapp/integrations/oauth.py

from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
import google.auth

def get_google_auth():
	"""Get authenticated Google client"""
	service_account_file = frappe.get_app_path("myapp") + "/integrations/google_service_account.json"
	
	credentials = Credentials.from_service_account_file(
		service_account_file,
		scopes=['https://www.googleapis.com/auth/calendar.readonly']
	)
	
	# Refresh if needed
	if credentials.expired:
		credentials.refresh(Request())
	
	return credentials

@frappe.whitelist()
def sync_google_calendar():
	"""Sync events from Google Calendar"""
	from googleapiclient.discovery import build
	
	credentials = get_google_auth()
	service = build('calendar', 'v3', credentials=credentials)
	
	try:
		events_result = service.events().list(
			calendarId='primary',
			maxResults=10,
			singleEvents=True,
			orderBy='startTime'
		).execute()
		
		events = events_result.get('items', [])
		created = 0
		
		for event in events:
			# Create event in Frappe
			if not frappe.db.exists("Event", {"google_id": event["id"]}):
				frappe.get_doc({
					"doctype": "Event",
					"subject": event["summary"],
					"starts_on": event["start"]["dateTime"],
					"ends_on": event["end"]["dateTime"],
					"google_id": event["id"],
					"description": event.get("description", "")
				}).insert()
				created += 1
		
		return {"status": "success", "events_created": created}
		
	except Exception as e:
		frappe.log_error(f"Google Calendar sync error: {str(e)}")
		frappe.throw("Failed to sync calendar")
```

---

## Common Integration Scenarios

### Email Notification Integration
```python
def send_email_via_third_party(recipient, subject, body):
	"""Send email through third-party service (SendGrid, Mailgun, etc.)"""
	api_key = frappe.db.get_single_value("Email Settings", "sendgrid_api_key")
	
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}
	
	payload = {
		"personalizations": [{"to": [{"email": recipient}]}],
		"from": {"email": "noreply@myapp.com"},
		"subject": subject,
		"content": [{"type": "text/html", "value": body}]
	}
	
	requests.post("https://api.sendgrid.com/v3/mail/send", 
		json=payload, headers=headers)
```

### Error Handling & Retry Logic
```python
def api_call_with_retry(url, method="GET", max_retries=3, backoff_factor=2):
	"""API call with exponential backoff retry"""
	import time
	
	for attempt in range(max_retries):
		try:
			response = requests.request(method, url, timeout=10)
			response.raise_for_status()
			return response
		except requests.RequestException as e:
			if attempt < max_retries - 1:
				wait_time = backoff_factor ** attempt
				time.sleep(wait_time)
			else:
				raise
```

---

## Decision Tree: When to Call Integration-Specialist

**Use Integration-Specialist when:**
- ✅ Connecting to payment gateway (Stripe, PayPal, etc.)
- ✅ Syncing with external CRM/ERP systems
- ✅ Setting up OAuth/authentication flows
- ✅ Building webhook receivers
- ✅ Implementing data import/export
- ✅ Connecting to third-party APIs
- ✅ Email system integration

**Don't use for:**
- ❌ Internal Frappe APIs (use API-Whitelister)
- ❌ Database operations (use Database-Navigator)
- ❌ Permission setup (use Permission-Guardian)
- ❌ DocType design (use DocType-Architect)

---

**Last Updated**: 2026-02-19
**Frappe Version**: v15.100.1
**Common Integrations**: Payment, CRM, Email, OAuth, Webhooks
