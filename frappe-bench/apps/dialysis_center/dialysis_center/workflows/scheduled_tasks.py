"""
Scheduled Background Tasks for Dialysis Center
Runs automatically based on schedule defined in hooks
"""
import frappe
from frappe import _
from frappe.utils import now_datetime, getdate, add_to_date, time_diff_in_hours
from datetime import datetime, timedelta


# ============================================================================
# DAILY SCHEDULED TASKS
# ============================================================================

def daily_invoice_reminders():
	"""Send daily reminders for overdue and upcoming invoices"""
	frappe.set_user("Administrator")
	
	# Find overdue invoices (due date passed, not paid)
	overdue_invoices = frappe.get_all(
		"Invoice",
		filters={
			"payment_status": ["!=", "Paid"],
			"due_date": ["<", getdate()],
			"status": ["!=", "Cancelled"]
		},
		fields=["name", "patient", "due_date", "pending_amount", "email"],
		limit_page_length=500
	)
	
	for invoice in overdue_invoices:
		patient_email = frappe.db.get_value("Patient", invoice.patient, "email")
		
		if patient_email:
			try:
				frappe.sendmail(
					recipients=[patient_email],
					subject=f"Payment Reminder - Invoice {invoice.name}",
					message=f"""
Dear Patient,

This is a reminder that your invoice {invoice.name} is overdue.

Amount Due: {invoice.pending_amount}
Original Due Date: {invoice.due_date}

Please arrange payment at your earliest convenience.

Thank you.
"""
				)
				
				# Log the reminder
				frappe.get_doc({
					"doctype": "Invoice Reminder Log",
					"invoice": invoice.name,
					"reminder_type": "Overdue",
					"sent_to": patient_email,
					"sent_date": now_datetime()
				}).insert(ignore_permissions=True)
			except Exception as e:
				frappe.log_error(f"Failed to send invoice reminder for {invoice.name}: {str(e)}")
	
	# Find invoices due within next 3 days
	upcoming_invoices = frappe.get_all(
		"Invoice",
		filters={
			"payment_status": ["!=", "Paid"],
			"due_date": [">=", getdate()],
			"due_date": ["<=", add_to_date(getdate(), days=3)],
			"status": ["!=", "Cancelled"]
		},
		fields=["name", "patient", "due_date", "pending_amount"],
		limit_page_length=500
	)
	
	for invoice in upcoming_invoices:
		patient_email = frappe.db.get_value("Patient", invoice.patient, "email")
		
		if patient_email:
			try:
				frappe.sendmail(
					recipients=[patient_email],
					subject=f"Payment Due Soon - Invoice {invoice.name}",
					message=f"""
Dear Patient,

This is a reminder that your payment for invoice {invoice.name} is due soon.

Amount Due: {invoice.pending_amount}
Due Date: {invoice.due_date}

Please arrange payment by the due date.

Thank you.
"""
				)
			except Exception as e:
				frappe.log_error(f"Failed to send upcoming invoice reminder: {str(e)}")


def daily_equipment_maintenance_alerts():
	"""Alert staff about equipment maintenance due"""
	frappe.set_user("Administrator")
	
	# Find machines due for maintenance
	machines_due = frappe.get_all(
		"Dialysis Machine",
		filters={
			"next_maintenance_date": ["<=", add_to_date(getdate(), days=7)],
			"status": ["!=", "Out of Service"]
		},
		fields=["name", "model", "next_maintenance_date"],
		limit_page_length=100
	)
	
	if machines_due:
		# Get maintenance coordinator emails
		maintenance_staff = frappe.db.sql_list(
			"SELECT email FROM `tabUser` WHERE name IN (SELECT user FROM `tabUserRole` WHERE role='Maintenance Staff')"
		)
		
		if maintenance_staff:
			machine_list = "\n".join([f"- {m['name']} ({m['model']}) - Due: {m['next_maintenance_date']}" for m in machines_due])
			
			frappe.sendmail(
				recipients=maintenance_staff,
				subject="Equipment Maintenance Schedule Alert",
				message=f"""
The following equipment is due for maintenance:

{machine_list}

Please schedule maintenance at your earliest convenience.

Thank you.
"""
			)
			
			# Log the alert
			frappe.get_doc({
				"doctype": "Maintenance Alert Log",
				"alert_type": "Maintenance Due",
				"machines_count": len(machines_due),
				"alert_date": getdate(),
				"details": json.dumps([m.name for m in machines_due])
			}).insert(ignore_permissions=True)


def daily_lab_result_notifications():
	"""Notify doctors when lab results are available"""
	frappe.set_user("Administrator")
	
	# Find lab tests with results received but not yet reviewed
	pending_reviews = frappe.get_all(
		"Lab Test",
		filters={
			"status": "Results Received",
			"created": [">=", add_to_date(now_datetime(), days=-1)]  # Results received in last 24 hours
		},
		fields=["name", "patient", "ordered_by", "test_date"],
		limit_page_length=100
	)
	
	for test in pending_reviews:
		doctor_email = frappe.db.get_value("User", test.ordered_by, "email") if test.ordered_by else None
		patient_name = frappe.db.get_value("Patient", test.patient, "patient_name")
		
		if doctor_email:
			try:
				frappe.sendmail(
					recipients=[doctor_email],
					subject=f"Lab Results Available - {patient_name}",
					message=f"""
Dear Doctor,

Lab results are now available for {patient_name}.

Lab Test ID: {test.name}
Test Date: {test.test_date}

Please review the results at your earliest convenience.

Thank you.
"""
				)
			except Exception as e:
				frappe.log_error(f"Failed to send lab result notification: {str(e)}")


def daily_patient_followup_tasks():
	"""Create follow-up tasks for patients based on their treatment plans"""
	frappe.set_user("Administrator")
	
	# Find patients with completed sessions from previous day
	yesterday = add_to_date(getdate(), days=-1)
	completed_sessions = frappe.get_all(
		"Dialysis Session",
		filters={
			"status": "Completed",
			"session_date": yesterday
		},
		fields=["name", "patient", "dialysis_machine"],
		limit_page_length=500
	)
	
	for session in completed_sessions:
		# Check if patient has any outstanding lab tests
		pending_tests = frappe.db.count("Lab Test", {
			"patient": session.patient,
			"status": "Draft"
		})
		
		if pending_tests > 0:
			# Create a task for the doctor
			doctor = frappe.db.get_value("Patient", session.patient, "assigned_doctor")
			
			if doctor:
				# Check if task already exists
				existing_task = frappe.db.exists("ToDo", {
					"reference_type": "Lab Test",
					"reference_name": session.patient,
					"status": "Open"
				})
				
				if not existing_task:
					frappe.get_doc({
						"doctype": "ToDo",
						"owner": doctor,
						"title": f"Review Lab Tests - {session.patient}",
						"description": f"Patient {session.patient} has pending lab tests",
						"reference_type": "Patient",
						"reference_name": session.patient,
						"status": "Open",
						"priority": "Medium",
						"due_date": getdate()
					}).insert(ignore_permissions=True)


def daily_patient_vitals_alert():
	"""Alert doctors about abnormal patient vitals from previous day"""
	frappe.set_user("Administrator")
	
	yesterday = add_to_date(getdate(), days=-1)
	
	# Find abnormal vitals recorded yesterday
	abnormal_vitals = frappe.db.sql("""
		SELECT DISTINCT svr.session, svr.patient, COUNT(*) as abnormal_count
		FROM `tabSession Vital Reading` svr
		WHERE DATE(svr.recorded_at) = %s
		AND (
			svr.blood_pressure_systolic > 180 OR svr.blood_pressure_systolic < 90
			OR svr.blood_pressure_diastolic > 110 OR svr.blood_pressure_diastolic < 60
			OR svr.pulse_rate > 120 OR svr.pulse_rate < 50
			OR svr.temperature > 38.5 OR svr.temperature < 36
		)
		GROUP BY svr.session, svr.patient
	""", (yesterday,), as_dict=True)
	
	for vital_record in abnormal_vitals:
		patient = vital_record.patient
		doctor = frappe.db.get_value("Patient", patient, "assigned_doctor")
		doctor_email = frappe.db.get_value("User", doctor, "email") if doctor else None
		
		if doctor_email:
			try:
				frappe.sendmail(
					recipients=[doctor_email],
					subject=f"Alert: Abnormal Vitals - {patient}",
					message=f"""
Dear Doctor,

Patient {patient} had abnormal vital signs recorded during their last dialysis session.

Number of abnormal readings: {vital_record.abnormal_count}

Please review the patient's vital signs and take appropriate action.

Thank you.
"""
				)
			except Exception as e:
				frappe.log_error(f"Failed to send vitals alert: {str(e)}")


# ============================================================================
# WEEKLY SCHEDULED TASKS
# ============================================================================

def weekly_equipment_status_report():
	"""Generate weekly equipment status report"""
	frappe.set_user("Administrator")
	
	# Find equipment requiring attention
	equipment_status = frappe.get_all(
		"Dialysis Machine",
		fields=["name", "model", "status", "last_maintenance_date", "next_maintenance_date"],
		limit_page_length=1000
	)
	
	# Group by status
	status_summary = {
		"Operational": 0,
		"Maintenance": 0,
		"Out of Service": 0,
		"Inactive": 0
	}
	
	for machine in equipment_status:
		status_summary[machine.status] = status_summary.get(machine.status, 0) + 1
	
	# Send report to administrators
	admin_emails = frappe.db.sql_list(
		"SELECT email FROM `tabUser` WHERE name IN (SELECT user FROM `tabUserRole` WHERE role='Dialysis Administrator')"
	)
	
	if admin_emails:
		report_content = f"""
Weekly Equipment Status Report
Generated: {getdate()}

Summary:
- Operational: {status_summary.get('Operational', 0)}
- Under Maintenance: {status_summary.get('Maintenance', 0)}
- Out of Service: {status_summary.get('Out of Service', 0)}
- Inactive: {status_summary.get('Inactive', 0)}

Total Machines: {len(equipment_status)}

For detailed equipment information, please log in to the system.
"""
		
		frappe.sendmail(
			recipients=admin_emails,
			subject="Weekly Equipment Status Report",
			message=report_content
		)


def weekly_invoice_aging_report():
	"""Generate weekly invoice aging report"""
	frappe.set_user("Administrator")
	
	# Calculate invoice aging
	invoices = frappe.get_all(
		"Invoice",
		filters={"payment_status": ["!=", "Paid"]},
		fields=["name", "patient", "due_date", "pending_amount"],
		limit_page_length=1000
	)
	
	# Group by aging
	aging = {
		"current": [],
		"30_60_days": [],
		"60_90_days": [],
		"90_plus_days": []
	}
	
	today = getdate()
	
	for invoice in invoices:
		days_overdue = (today - invoice.due_date).days
		
		if days_overdue <= 0:
			aging["current"].append(invoice)
		elif days_overdue <= 30:
			aging["30_60_days"].append(invoice)
		elif days_overdue <= 60:
			aging["60_90_days"].append(invoice)
		else:
			aging["90_plus_days"].append(invoice)
	
	# Send report to finance team
	finance_emails = frappe.db.sql_list(
		"SELECT email FROM `tabUser` WHERE name IN (SELECT user FROM `tabUserRole` WHERE role='Dialysis Accountant')"
	)
	
	if finance_emails:
		report_content = f"""
Weekly Invoice Aging Report
Generated: {getdate()}

Current (Due Soon): {len(aging['current'])} invoices
30-60 Days Overdue: {len(aging['30_60_days'])} invoices
60-90 Days Overdue: {len(aging['60_90_days'])} invoices
90+ Days Overdue: {len(aging['90_plus_days'])} invoices

Total Outstanding: {len(invoices)} invoices

For detailed aging information, please log in to the system.
"""
		
		frappe.sendmail(
			recipients=finance_emails,
			subject="Weekly Invoice Aging Report",
			message=report_content
		)


# ============================================================================
# MONTHLY SCHEDULED TASKS
# ============================================================================

def monthly_machine_performance_report():
	"""Generate monthly machine performance report"""
	frappe.set_user("Administrator")
	
	# Get sessions from last month
	last_month_start = add_to_date(getdate(), months=-1, day=1)
	last_month_end = add_to_date(getdate(), day=1, days=-1)
	
	sessions = frappe.get_all(
		"Dialysis Session",
		filters={
			"status": "Completed",
			"session_date": [">=", last_month_start],
			"session_date": ["<=", last_month_end]
		},
		fields=["dialysis_machine", "actual_duration"],
		limit_page_length=5000
	)
	
	# Calculate machine utilization
	machine_stats = {}
	for session in sessions:
		machine = session.dialysis_machine
		if machine not in machine_stats:
			machine_stats[machine] = {"sessions": 0, "total_hours": 0}
		
		machine_stats[machine]["sessions"] += 1
		machine_stats[machine]["total_hours"] += session.actual_duration / 60 if session.actual_duration else 0
	
	# Send report
	admin_emails = frappe.db.sql_list(
		"SELECT email FROM `tabUser` WHERE name IN (SELECT user FROM `tabUserRole` WHERE role='Dialysis Administrator')"
	)
	
	if admin_emails:
		report_lines = "\n".join([
			f"- {machine}: {stats['sessions']} sessions, {stats['total_hours']:.1f} hours"
			for machine, stats in sorted(machine_stats.items())
		])
		
		frappe.sendmail(
			recipients=admin_emails,
			subject="Monthly Machine Performance Report",
			message=f"""
Monthly Machine Performance Report
Period: {last_month_start} to {last_month_end}

Machine Utilization:
{report_lines}

Total Sessions: {len(sessions)}
"""
		)


def monthly_patient_treatment_compliance():
	"""Generate monthly patient treatment compliance report"""
	frappe.set_user("Administrator")
	
	# Get patients with sessions in last month
	last_month_start = add_to_date(getdate(), months=-1, day=1)
	last_month_end = add_to_date(getdate(), day=1, days=-1)
	
	# Find patients with low compliance
	low_compliance = frappe.db.sql("""
		SELECT p.name, p.patient_name, 
			COUNT(ds.name) as sessions_completed,
			p.scheduled_sessions as sessions_scheduled
		FROM `tabPatient` p
		LEFT JOIN `tabDialysis Session` ds ON p.name = ds.patient 
			AND ds.status = 'Completed'
			AND ds.session_date BETWEEN %s AND %s
		GROUP BY p.name
		HAVING sessions_completed < (sessions_scheduled * 0.8)
		ORDER BY sessions_completed ASC
	""", (last_month_start, last_month_end), as_dict=True)
	
	if low_compliance:
		# Notify doctors about patients with low compliance
		doctors = frappe.db.sql_list(
			"SELECT DISTINCT assigned_doctor FROM `tabPatient` WHERE assigned_doctor IS NOT NULL"
		)
		
		for doctor in doctors:
			doctor_email = frappe.db.get_value("User", doctor, "email")
			
			if doctor_email:
				patients_list = "\n".join([
					f"- {p['patient_name']}: {p['sessions_completed']} sessions (Target: {int(p['sessions_scheduled'] * 0.8)})"
					for p in low_compliance
				])
				
				frappe.sendmail(
					recipients=[doctor_email],
					subject="Patient Treatment Compliance Alert",
					message=f"""
The following patients have low treatment compliance this month:

{patients_list}

Please review these patients' cases and take appropriate action.

Thank you.
"""
				)


# ============================================================================
# HELPER FUNCTION
# ============================================================================

import json
