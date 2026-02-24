"""
Automated Test Data Seeding for Development
Automatically seeds the database with test data for development purposes.
"""
import frappe
from dialysis_center.tests.generate_test_data import generate_complete_test_data
from dialysis_center.tests.clear_test_data import clear_test_data


def seed_development_data(clear_existing=False):
	"""
	Seed the database with test data for development.
	
	Args:
		clear_existing (bool): If True, clear existing test data before seeding
	"""
	frappe.set_user("Administrator")
	
	print("\n" + "="*70)
	print("🌱 DIALYSIS CENTER - AUTOMATED DEV DATA SEEDING")
	print("="*70)
	
	if clear_existing:
		print("\n🗑️  Clearing existing test data...")
		try:
			clear_test_data()
		except Exception as e:
			print(f"⚠️  Error clearing data: {str(e)[:80]}")
	
	print("\n🔄 Generating test data...")
	try:
		generate_complete_test_data()
		print("\n✅ Development data seeding complete!")
	except Exception as e:
		print(f"\n❌ Error generating data: {str(e)[:100]}")
		frappe.log_error(message=str(e), title="Dev Data Seeding Error")
	
	print("="*70 + "\n")


def check_and_seed_if_empty():
	"""
	Check if the database is empty and seed if needed.
	Useful for automated setup on first install or site creation.
	"""
	patient_count = frappe.db.count("Patient")
	
	if patient_count == 0:
		print("\n📊 No patient data found. Auto-seeding development data...")
		seed_development_data(clear_existing=False)
	else:
		print(f"\n📊 Found {patient_count} patients. Skipping auto-seed.")


if __name__ == "__main__":
	seed_development_data(clear_existing=False)
