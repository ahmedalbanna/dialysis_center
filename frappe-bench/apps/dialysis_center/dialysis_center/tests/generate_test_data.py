import frappe
from frappe.utils import now_datetime, add_days
import random
from dialysis_center.tests.factories.patient_factory import PatientFactory
from dialysis_center.tests.factories.appointment_factory import AppointmentFactory
from dialysis_center.tests.factories.session_factory import SessionFactory


def generate_complete_test_data():
	"""Generate a complete test dataset for the dialysis center"""

	frappe.set_user("Administrator")

	print("🔄 Generating test data...")

	# 1. Create master data
	print("📋 Creating master data...")
	create_machines()
	try:
		create_staff()
	except Exception as e:
		print(f"⚠️  Skipping staff creation (DocType not available): {str(e)[:60]}")
	try:
		create_inventory_items()
	except Exception as e:
		print(f"⚠️  Skipping inventory items (DocType not available): {str(e)[:60]}")

	# 2. Create patients
	print("👥 Creating test patients...")
	patients = PatientFactory.create_batch(50)
	print(f"✅ Created {len(patients)} patients")

	# 3. Create appointments (next 30 days)
	print("📅 Creating appointments...")
	appointments_created = 0
	try:
		for patient in patients[:30]:  # 30 patients get appointments
			try:
				appointments = AppointmentFactory.create_batch(
					count=3,  # 3 appointments each
					patient=patient,
					status="Scheduled"
				)
				appointments_created += len(appointments)
			except Exception as e:
				print(f"  ⚠️  Skipping appointments for patient (DocType issue): {str(e)[:40]}")
				break
		print(f"✅ Created {appointments_created} appointments")
	except Exception as e:
		print(f"⚠️  Skipping appointments (DocType not available): {str(e)[:60]}")

	# 4. Create historical sessions (last 90 days)
	print("🏥 Creating historical dialysis sessions...")
	sessions_created = 0
	try:
		for patient in patients[:5]:  # Limit to 5 patients for now
			# Create 5 historical sessions per patient
			for i in range(5, 10):
				try:
					session_date = add_days(now_datetime(), -i)
					session = SessionFactory.create_completed_session(
						patient=patient,
						session_date=session_date
					)
					sessions_created += 1
				except Exception as e:
					print(f"  ⚠️  Skipping session creation (DocType issue)")
					break
	except Exception as e:
		print(f"⚠️  Skipping sessions (DocType not available): {str(e)[:60]}")
	print(f"✅ Created {sessions_created} historical sessions")

	# 5. Create lab results
	print("🧪 Creating lab results...")
	try:
		create_lab_results(patients)
	except Exception as e:
		print(f"⚠️  Skipping lab results (DocType not available): {str(e)[:60]}")

	# 6. Create invoices
	print("💰 Creating invoices...")
	try:
		create_invoices(patients)
	except Exception as e:
		print(f"⚠️  Skipping invoices (DocType not available): {str(e)[:60]}")

	print("\n✨ Test data generation complete!")
	print_summary()


def create_machines():
	"""Create test dialysis machines"""
	machines = [
		{"machine_id": "MCH-001", "machine_name": "Machine A1", "manufacturer": "Fresenius", "model": "5008S", "location": "Main Floor"},
		{"machine_id": "MCH-002", "machine_name": "Machine A2", "manufacturer": "Fresenius", "model": "5008S", "location": "Main Floor"},
		{"machine_id": "MCH-003", "machine_name": "Machine B1", "manufacturer": "Gambro", "model": "AK200", "location": "Second Floor"},
		{"machine_id": "MCH-004", "machine_name": "Machine B2", "manufacturer": "Gambro", "model": "AK200", "location": "Second Floor"},
		{"machine_id": "MCH-005", "machine_name": "Machine C1", "manufacturer": "Baxter", "model": "Phoenix", "location": "Third Floor"},
	]

	for machine_data in machines:
		if not frappe.db.exists("Dialysis Machine", {"machine_id": machine_data["machine_id"]}):
			machine = frappe.get_doc({
				"doctype": "Dialysis Machine",
				**machine_data,
				"status": "Available",
				"installation_date": "2020-01-01"
			})
			machine.insert(ignore_permissions=True)

	frappe.db.commit()


def create_staff():
	"""Create test staff members"""
	staff_members = [
		{"first_name": "Dr. Ahmed", "last_name": "Hassan", "practitioner_type": "Nephrologist"},
		{"first_name": "Dr. Sarah", "last_name": "Ali", "practitioner_type": "Nephrologist"},
		{"first_name": "Nurse Fatima", "last_name": "Mohammed", "practitioner_type": "Nurse"},
		{"first_name": "Nurse Aisha", "last_name": "Abdullah", "practitioner_type": "Nurse"},
		{"first_name": "Tech Omar", "last_name": "Ibrahim", "practitioner_type": "Technician"},
	]

	for staff_data in staff_members:
		if not frappe.db.exists("Healthcare Practitioner", {"first_name": staff_data["first_name"]}):
			staff = frappe.get_doc({
				"doctype": "Healthcare Practitioner",
				**staff_data,
				"gender": "Male" if "Dr. Ahmed" in staff_data["first_name"] or "Omar" in staff_data["first_name"] else "Female"
			})
			staff.insert(ignore_permissions=True)

	frappe.db.commit()


def create_inventory_items():
	"""Create test inventory items"""
	items = [
		{"item_code": "DIAL-F60", "item_name": "Dialyzer F60", "category": "Dialyzer", "unit": "Piece"},
		{"item_code": "DIAL-F80", "item_name": "Dialyzer F80", "category": "Dialyzer", "unit": "Piece"},
		{"item_code": "BLOODSET-STD", "item_name": "Standard Blood Line Set", "category": "Consumable", "unit": "Set"},
		{"item_code": "HEPARIN-5ML", "item_name": "Heparin 5ml", "category": "Medication", "unit": "Vial"},
		{"item_code": "SALINE-500ML", "item_name": "Normal Saline 500ml", "category": "Medication", "unit": "Bag"},
	]

	for item_data in items:
		if not frappe.db.exists("Inventory Item", {"item_code": item_data["item_code"]}):
			item = frappe.get_doc({
				"doctype": "Inventory Item",
				**item_data,
				"reorder_level": 50,
				"reorder_quantity": 100,
				"current_stock": 200
			})
			item.insert(ignore_permissions=True)

	frappe.db.commit()


def create_lab_results(patients):
	"""Create lab results for patients"""
	for patient in patients[:20]:  # Create lab results for 20 patients
		lab_result = frappe.get_doc({
			"doctype": "Lab Result",
			"patient": patient.name,
			"test_date": add_days(now_datetime(), -7),
			"hemoglobin": round(random.uniform(9.0, 12.0), 1),
			"hematocrit": round(random.uniform(27, 36), 1),
			"creatinine": round(random.uniform(5.0, 10.0), 1),
			"urea": round(random.uniform(100, 180), 1),
			"potassium": round(random.uniform(4.0, 6.0), 1),
			"sodium": round(random.uniform(135, 145), 1),
			"calcium": round(random.uniform(8.0, 10.0), 1),
			"phosphorus": round(random.uniform(3.5, 6.5), 1),
		})
		lab_result.insert(ignore_permissions=True)

	frappe.db.commit()


def create_invoices(patients):
	"""Create invoices for completed sessions"""
	for patient in patients[:15]:  # Create invoices for 15 patients
		invoice = frappe.get_doc({
			"doctype": "Invoice",
			"patient": patient.name,
			"invoice_date": add_days(now_datetime(), -5),
			"total_amount": 1500.00,
			"status": "Paid",
			"payment_method": "Insurance"
		})
		invoice.insert(ignore_permissions=True)

	frappe.db.commit()


def print_summary():
	"""Print summary of generated data"""
	print("\n" + "="*50)
	print("📊 TEST DATA SUMMARY")
	print("="*50)
	print(f"Patients: {frappe.db.count('Patient')}")
	print(f"Appointments: {frappe.db.count('Appointment')}")
	print(f"Dialysis Sessions: {frappe.db.count('Dialysis Session')}")
	print(f"Dialysis Machines: {frappe.db.count('Dialysis Machine')}")
	print(f"Healthcare Practitioners: {frappe.db.count('Healthcare Practitioner')}")
	print(f"Lab Results: {frappe.db.count('Lab Result')}")
	print(f"Invoices: {frappe.db.count('Invoice')}")
	print("="*50)
