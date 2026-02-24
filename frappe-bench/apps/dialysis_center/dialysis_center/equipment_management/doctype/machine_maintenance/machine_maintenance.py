import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate, nowdate, flt
from frappe import _

class MachineMaintenance(Document):
	def validate(self):
		"""Validate maintenance record"""
		self.validate_machine()
		self.validate_maintenance_type()
		self.validate_dates()
		self.validate_parts()
		self.calculate_next_maintenance()
	
	def validate_machine(self):
		"""Validate machine exists"""
		if self.dialysis_machine:
			if not frappe.db.exists("Dialysis Machine", self.dialysis_machine):
				frappe.throw(_("Machine {0} does not exist").format(self.dialysis_machine))
	
	def validate_maintenance_type(self):
		"""Validate maintenance type is specified"""
		if not self.maintenance_type:
			frappe.throw(_("Maintenance Type is required"))
	
	def validate_dates(self):
		"""Validate date logic"""
		if not self.scheduled_date:
			frappe.throw(_("Scheduled Date is required"))
		
		# Scheduled date should not be in the past for future maintenance
		if self.status == "Scheduled" and getdate(self.scheduled_date) < getdate():
			frappe.msgprint(_("Scheduled date is in the past"), 
				indicator="orange", alert=True)
		
		if self.actual_date and self.scheduled_date:
			if getdate(self.actual_date) < getdate(self.scheduled_date):
				frappe.msgprint(_("Actual date is before scheduled date"),
					indicator="orange", alert=True)
	
	def validate_parts(self):
		"""Validate maintenance parts if applicable"""
		if self.parts and len(self.parts) > 0:
			for part in self.parts:
				if not part.part_name:
					frappe.throw(_("Row {0}: Part Name is required").format(part.idx))
				
				if part.quantity and flt(part.quantity) <= 0:
					frappe.throw(_("Row {0}: Quantity must be greater than 0").format(part.idx))
	
	def calculate_next_maintenance(self):
		"""Calculate next maintenance date based on type"""
		if self.status == "Completed" and self.actual_date:
			# Get machine maintenance frequency
			machine = frappe.get_doc("Dialysis Machine", self.dialysis_machine)
			frequency_days = machine.maintenance_frequency_days or 90
			
			# Calculate based on actual completion date
			self.next_maintenance_date = add_days(self.actual_date, frequency_days)
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from notes
		if self.notes:
			self.notes = self.notes.strip()
		
		# Set scheduled date if not set
		if not self.scheduled_date:
			self.scheduled_date = nowdate()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"machine_maintenance_{self.name}")
		if self.dialysis_machine:
			frappe.cache.delete_value(f"machine_{self.dialysis_machine}_maintenance")
	
	def on_submit(self):
		"""Update machine maintenance date"""
		if self.status == "Completed":
			# Update machine's last maintenance date
			frappe.db.set_value(
				"Dialysis Machine",
				self.dialysis_machine,
				"last_maintenance_date",
				self.actual_date or self.scheduled_date
			)
			
			# Update next maintenance date on machine
			if self.next_maintenance_date:
				frappe.db.set_value(
					"Dialysis Machine",
					self.dialysis_machine,
					"next_maintenance_due",
					self.next_maintenance_date
				)
