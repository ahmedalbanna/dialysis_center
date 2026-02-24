import frappe


def clear_test_data():
	"""Clear all test data"""
	frappe.set_user("Administrator")

	print("🗑️  Clearing test data...")

	# Delete in reverse dependency order
	doctypes = [
		"Invoice",
		"Lab Result",
		"Dialysis Session",
		"Appointment",
		"Patient",
		"Healthcare Practitioner",
		"Dialysis Machine",
		"Inventory Item"
	]

	for doctype in doctypes:
		count = frappe.db.count(doctype)
		frappe.db.sql(f"DELETE FROM `tab{doctype}`")
		print(f"✅ Deleted {count} {doctype} records")

	frappe.db.commit()
	print("✨ Test data cleared!")
