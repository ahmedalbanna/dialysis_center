import frappe
from frappe import _
from frappe.utils import nowdate, add_days, getdate

def send_appointment_reminders():
	"""Send appointment reminders for next day"""
	tomorrow = add_days(nowdate(), 1)
	
	appointments = frappe.get_all("Appointment",
		filters={
			"appointment_date": tomorrow,
			"status": "Scheduled"
		},
		fields=["name", "patient", "patient_name", "appointment_time"]
	)
	
	for appt in appointments:
		# Get patient contact
		patient = frappe.get_doc("Patient", appt.patient)
		
		if patient.mobile_number or patient.email:
			# Send SMS or email reminder
			message = f"Reminder: You have a dialysis appointment tomorrow at {appt.appointment_time}"
			
			# Log the reminder (actual SMS/email sending would go here)
			frappe.logger().info(f"Appointment reminder sent to {appt.patient_name} for {tomorrow}")

def check_overdue_invoices():
	"""Check and flag overdue invoices"""
	today = getdate(nowdate())
	
	overdue_invoices = frappe.get_all("Invoice",
		filters={
			"due_date": ["<", today],
			"payment_status": ["!=", "Paid"],
			"docstatus": 1
		},
		fields=["name", "patient", "patient_name", "due_date", "outstanding_amount"]
	)
	
	for invoice in overdue_invoices:
		# Flag as overdue (you could add a custom field for this)
		frappe.logger().warning(f"Overdue invoice: {invoice.name} for {invoice.patient_name}")

def update_machine_status():
	"""Update machine status based on active sessions"""
	# Get machines with active sessions
	active_sessions = frappe.get_all("Dialysis Session",
		filters={"status": "In Progress"},
		fields=["dialysis_machine"]
	)
	
	active_machines = [s.dialysis_machine for s in active_sessions if s.dialysis_machine]
	
	# Update machine status
	all_machines = frappe.get_all("Dialysis Machine", fields=["name", "status"])
	
	for machine in all_machines:
		if machine.name in active_machines:
			if machine.status != "In Use":
				frappe.db.set_value("Dialysis Machine", machine.name, "status", "In Use")
		else:
			if machine.status == "In Use":
				frappe.db.set_value("Dialysis Machine", machine.name, "status", "Available")
	
	frappe.db.commit()

def generate_daily_schedule_report():
	"""Generate daily schedule report at 8 AM"""
	today = nowdate()
	
	appointments = frappe.get_all("Appointment",
		filters={"appointment_date": today},
		fields=["name", "patient_name", "appointment_time", "machine", "status"],
		order_by="appointment_time asc"
	)
	
	frappe.logger().info(f"Daily schedule: {len(appointments)} appointments for {today}")
	
	# Could send email report to administrators here
