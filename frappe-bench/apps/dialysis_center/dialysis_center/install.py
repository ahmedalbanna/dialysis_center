"""
Installation hooks for Dialysis Center App
"""
import frappe


def after_install():
	"""
	Called after app installation.
	Loads fixtures and optionally seeds development data.
	"""
	from dialysis_center.fixtures.load_fixtures import load_fixtures
	
	print("\n" + "="*70)
	print("🏥 DIALYSIS CENTER APP - POST-INSTALLATION SETUP")
	print("="*70)
	
	# Load fixtures
	print("\n📦 Loading fixtures...")
	try:
		load_fixtures()
	except Exception as e:
		print(f"⚠️  Error loading fixtures: {str(e)[:80]}")
		frappe.log_error(message=str(e), title="Fixture Loading Error")
	
	# Check if we should seed development data
	if frappe.conf.get("developer_mode"):
		print("\n🔧 Developer mode detected!")
		auto_seed = frappe.conf.get("dialysis_center_auto_seed_data", False)
		
		if auto_seed:
			print("🌱 Auto-seeding development data...")
			from dialysis_center.fixtures.seed_dev_data import seed_development_data
			try:
				seed_development_data(clear_existing=False)
			except Exception as e:
				print(f"⚠️  Error seeding data: {str(e)[:80]}")
				frappe.log_error(message=str(e), title="Dev Data Seeding Error")
		else:
			print("\n💡 TIP: To auto-seed test data on install, add to site_config.json:")
			print('   "dialysis_center_auto_seed_data": true')
			print("\n   Or run manually:")
			print("   bench --site [sitename] dialysis-center seed-data")
	
	print("\n✅ Dialysis Center installation complete!")
	print("="*70 + "\n")


def before_uninstall():
	"""
	Called before app uninstallation.
	"""
	print("\n" + "="*70)
	print("🗑️  DIALYSIS CENTER APP - PRE-UNINSTALLATION")
	print("="*70)
	
	# Optionally clear test data
	clear_test_data = frappe.conf.get("dialysis_center_clear_on_uninstall", False)
	
	if clear_test_data:
		print("\n🗑️  Clearing test data...")
		from dialysis_center.tests.clear_test_data import clear_test_data
		try:
			clear_test_data()
		except Exception as e:
			print(f"⚠️  Error clearing data: {str(e)[:80]}")
	
	print("\n✅ Dialysis Center uninstallation cleanup complete!")
	print("="*70 + "\n")
