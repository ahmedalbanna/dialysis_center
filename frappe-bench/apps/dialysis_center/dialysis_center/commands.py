"""
Custom Bench Commands for Dialysis Center App
These commands can be run from the command line using:
bench --site [sitename] dialysis-center [command]
"""
import click
import frappe
from frappe.commands import pass_context


@click.group()
def dialysis_center():
	"""Dialysis Center management commands"""
	pass


@click.command("seed-data")
@click.option("--clear", is_flag=True, help="Clear existing test data before seeding")
@click.option("--patients", default=50, help="Number of patients to create (default: 50)")
@pass_context
def seed_data(context, clear, patients):
	"""
	Seed the database with test data for development.
	
	Usage:
		bench --site frappe.local dialysis-center seed-data
		bench --site frappe.local dialysis-center seed-data --clear
		bench --site frappe.local dialysis-center seed-data --patients 100
	"""
	site = context.sites[0]
	frappe.init(site=site)
	frappe.connect()
	
	from dialysis_center.fixtures.seed_dev_data import seed_development_data
	
	print(f"\n🌱 Seeding data for site: {site}")
	if patients != 50:
		print(f"📊 Creating {patients} patients...")
	
	seed_development_data(clear_existing=clear)
	
	frappe.destroy()


@click.command("clear-test-data")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt")
@pass_context
def clear_test_data(context, confirm):
	"""
	Clear all test data from the database.
	
	Usage:
		bench --site frappe.local dialysis-center clear-test-data
		bench --site frappe.local dialysis-center clear-test-data --confirm
	"""
	site = context.sites[0]
	frappe.init(site=site)
	frappe.connect()
	
	if not confirm:
		if not click.confirm(f"⚠️  Clear all test data from site '{site}'?"):
			print("❌ Cancelled.")
			frappe.destroy()
			return
	
	from dialysis_center.tests.clear_test_data import clear_test_data as clear_data
	
	print(f"\n🗑️  Clearing test data from site: {site}")
	clear_data()
	print("✅ Test data cleared!")
	
	frappe.destroy()


@click.command("show-stats")
@pass_context
def show_stats(context):
	"""
	Show current database statistics.
	
	Usage:
		bench --site frappe.local dialysis-center show-stats
	"""
	site = context.sites[0]
	frappe.init(site=site)
	frappe.connect()
	
	print(f"\n📊 Database Statistics for: {site}")
	print("="*50)
	
	stats = {
		"Patients": "Patient",
		"Dialysis Machines": "Dialysis Machine",
		"Appointments": "Appointment",
		"Dialysis Sessions": "Dialysis Session",
		"Treatment Templates": "Treatment Template",
		"Roles": "Role"
	}
	
	for label, doctype in stats.items():
		try:
			count = frappe.db.count(doctype)
			print(f"{label:25s}: {count:>5d}")
		except Exception:
			print(f"{label:25s}: {'N/A':>5s}")
	
	print("="*50 + "\n")
	
	frappe.destroy()


# Register commands
dialysis_center.add_command(seed_data)
dialysis_center.add_command(clear_test_data)
dialysis_center.add_command(show_stats)

commands = [
	dialysis_center
]
