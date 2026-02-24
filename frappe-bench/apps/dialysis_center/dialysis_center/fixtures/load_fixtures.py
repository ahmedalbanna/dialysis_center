import frappe
import json
import os

def load_fixtures():
	"""Load all fixtures for dialysis_center app"""
	
	frappe.set_user("Administrator")
	
	print("🔄 Loading fixtures...")
	
	# Load JSON fixtures from fixtures directory
	fixtures_dir = os.path.dirname(__file__)
	fixture_files = [
		"role.json",
		"treatment_template.json"
	]
	
	for fixture_file in fixture_files:
		fixture_path = os.path.join(fixtures_dir, fixture_file)
		if os.path.exists(fixture_path):
			print(f"\n📄 Loading {fixture_file}...")
			load_json_fixture(fixture_path)
		else:
			print(f"⚠️  Fixture file not found: {fixture_file}")
	
	# Create Roles (fallback if JSON loading failed)
	roles = [
		{"doctype": "Role", "role_name": "Dialysis Administrator", "desk_access": 1},
		{"doctype": "Role", "role_name": "Dialysis Doctor", "desk_access": 1},
		{"doctype": "Role", "role_name": "Dialysis Nurse", "desk_access": 1},
		{"doctype": "Role", "role_name": "Dialysis Technician", "desk_access": 1},
		{"doctype": "Role", "role_name": "Dialysis Receptionist", "desk_access": 1},
	]
	
	for role_data in roles:
		if not frappe.db.exists('Role', role_data['role_name']):
			role = frappe.get_doc(role_data)
			role.insert(ignore_permissions=True)
			print(f"✓ Created role: {role_data['role_name']}")
		else:
			print(f"- Role already exists: {role_data['role_name']}")
	
	# Create Sample Machines
	machines = [
		{
			"doctype": "Dialysis Machine",
			"machine_id": "DM-001",
			"machine_name": "Fresenius 5008S #1",
			"manufacturer": "Fresenius Medical Care",
			"model": "5008S",
			"serial_number": "FS5008S001",
			"status": "Available",
			"location": "Station 1",
			"max_blood_flow_rate": 500,
			"max_dialysate_flow_rate": 800,
			"has_hdf": 1,
			"has_biofeedback": 1,
			"maintenance_frequency_days": 90
		},
		{
			"doctype": "Dialysis Machine",
			"machine_id": "DM-002",
			"machine_name": "Fresenius 5008S #2",
			"manufacturer": "Fresenius Medical Care",
			"model": "5008S",
			"serial_number": "FS5008S002",
			"status": "Available",
			"location": "Station 2",
			"max_blood_flow_rate": 500,
			"max_dialysate_flow_rate": 800,
			"has_hdf": 1,
			"has_biofeedback": 1,
			"maintenance_frequency_days": 90
		},
		{
			"doctype": "Dialysis Machine",
			"machine_id": "DM-003",
			"machine_name": "Gambro AK 200",
			"manufacturer": "Gambro",
			"model": "AK 200",
			"serial_number": "GB200003",
			"status": "Available",
			"location": "Station 3",
			"max_blood_flow_rate": 450,
			"max_dialysate_flow_rate": 750,
			"has_hdf": 0,
			"has_biofeedback": 0,
			"maintenance_frequency_days": 90
		}
	]
	
	for machine_data in machines:
		if not frappe.db.exists('Dialysis Machine', machine_data['machine_id']):
			machine = frappe.get_doc(machine_data)
			machine.insert(ignore_permissions=True)
			print(f"✓ Created machine: {machine_data['machine_id']} - {machine_data['machine_name']}")
		else:
			print(f"- Machine already exists: {machine_data['machine_id']}")
	
	# Create Sample Patients
	patients = [
		{
			"doctype": "Patient",
			"patient_name": "John Smith",
			"date_of_birth": "1965-05-15",
			"gender": "Male",
			"blood_group": "O+",
			"national_id": "ID001",
			"mobile_number": "+12345678900",
			"email": "john.smith@example.com",
			"status": "Active",
			"dialysis_type": "Hemodialysis",
			"access_type": "AV Fistula",
			"dry_weight": 70.5,
			"frequency": "3x per week",
			"duration": 240
		},
		{
			"doctype": "Patient",
			"patient_name": "Mary Johnson",
			"date_of_birth": "1970-08-22",
			"gender": "Female",
			"blood_group": "A+",
			"national_id": "ID002",
			"mobile_number": "+12345678911",
			"email": "mary.johnson@example.com",
			"status": "Active",
			"dialysis_type": "Hemodialysis",
			"access_type": "AV Graft",
			"dry_weight": 65.0,
			"frequency": "3x per week",
			"duration": 240
		}
	]
	
	for patient_data in patients:
		if not frappe.db.exists('Patient', {"national_id": patient_data['national_id']}):
			patient = frappe.get_doc(patient_data)
			patient.insert(ignore_permissions=True)
			print(f"✓ Created patient: {patient.name} - {patient_data['patient_name']}")
		else:
			print(f"- Patient already exists: {patient_data['patient_name']}")
	
	frappe.db.commit()
	print("\\n✅ All fixtures loaded successfully!")


def load_json_fixture(fixture_path):
	"""Load a JSON fixture file into the database"""
	try:
		with open(fixture_path, 'r') as f:
			fixtures = json.load(f)
		
		if not isinstance(fixtures, list):
			fixtures = [fixtures]
		
		count = 0
		for fixture_data in fixtures:
			if not fixture_data.get("doctype"):
				print(f"  ⚠️  Skipping invalid fixture (no doctype)")
				continue
			
			doctype = fixture_data.get("doctype")
			name = fixture_data.get("name")
			
			# Check if document already exists
			if name and frappe.db.exists(doctype, name):
				print(f"  - {doctype} '{name}' already exists")
				continue
			
			try:
				doc = frappe.get_doc(fixture_data)
				doc.insert(ignore_permissions=True)
				count += 1
				print(f"  ✓ Created {doctype}: {doc.name}")
			except Exception as e:
				print(f"  ✗ Error creating {doctype}: {str(e)}")
		
		frappe.db.commit()
		print(f"  ✅ Loaded {count} records from {os.path.basename(fixture_path)}")
	
	except Exception as e:
		print(f"  ✗ Error loading fixture: {str(e)}")


if __name__ == "__main__":
	load_fixtures()
