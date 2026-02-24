import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate, nowdate, flt, date_diff
from frappe import _

class DialysisMachine(Document):
	def validate(self):
		"""Validate machine data"""
		self.validate_machine_details()
		self.validate_status_transition()
		self.check_maintenance_schedule()
		self.calculate_next_maintenance()
	
	def validate_machine_details(self):
		"""Validate machine details are complete"""
		if not self.machine_name:
			frappe.throw(_("Machine Name is required"))
		
		if not self.machine_id:
			frappe.throw(_("Machine ID is required"))
	
	def validate_status_transition(self):
		"""Validate status transitions"""
		if self.status not in ["Available", "Maintenance", "Out of Service"]:
			frappe.throw(_("Invalid machine status: {0}").format(self.status))
	
	def check_maintenance_schedule(self):
		"""Check if maintenance is due"""
		if self.next_maintenance_date:
			days_until_maintenance = date_diff(self.next_maintenance_date, getdate())
			
			if days_until_maintenance <= 0:
				frappe.msgprint(_("CRITICAL: Machine maintenance is overdue"),
					indicator="red", alert=True)
			elif days_until_maintenance <= 7:
				frappe.msgprint(_("Warning: Machine maintenance is due within 7 days"),
					indicator="orange", alert=True)
	
	def calculate_next_maintenance(self):
		"""Calculate next maintenance date based on last maintenance and frequency"""
		if self.last_maintenance_date and self.maintenance_frequency_days:
			self.next_maintenance_date = add_days(
				self.last_maintenance_date, 
				self.maintenance_frequency_days
			)
	
	def update_usage(self, session_duration_minutes):
		"""Update machine usage statistics after a session"""
		self.total_sessions = (self.total_sessions or 0) + 1
		self.total_hours_used = (self.total_hours_used or 0) + (session_duration_minutes / 60)
		self.save()
	
	def mark_maintenance(self, maintenance_date=None):
		"""Mark machine as under maintenance"""
		if not maintenance_date:
			maintenance_date = getdate()
		
		self.status = "Maintenance"
		self.last_maintenance_date = maintenance_date
		self.calculate_next_maintenance()
		self.save()
	
	def mark_available(self):
		"""Mark machine as available after maintenance"""
		self.status = "Available"
		self.save()
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from text fields
		if self.machine_name:
			self.machine_name = self.machine_name.strip()
		
		if self.machine_id:
			self.machine_id = self.machine_id.strip()
		
		if self.location:
			self.location = self.location.strip()
		
		if self.notes:
			self.notes = self.notes.strip()
	
	def on_update(self):
		"""Called after saving - check maintenance schedule"""
		# Clear related caches
		frappe.cache.delete_value(f"machine_{self.name}")
		frappe.cache.delete_value("available_machines")
		
		# Check and alert if maintenance is due
		if self.next_maintenance_date:
			days_until = date_diff(self.next_maintenance_date, getdate())
			if days_until <= 0 and self.status == "Available":
				# Auto-flag for maintenance
				frappe.msgprint(_("Machine {0} requires maintenance").format(self.machine_name),
					indicator="red", alert=True)

@frappe.whitelist()
def get_available_machines(date, shift=None):
	"""Get list of available machines for a given date and shift"""
	filters = {
		"status": "Available"
	}
	
	machines = frappe.get_all(
		"Dialysis Machine",
		filters=filters,
		fields=["name", "machine_id", "machine_name", "location"]
	)
	
	# Filter out machines that are already booked
	if date:
		booked_machines = frappe.get_all(
			"Appointment",
			filters={
				"appointment_date": date,
				"status": ["not in", ["Cancelled", "Completed"]]
			},
			fields=["machine"],
			pluck="machine"
		)
		
		machines = [m for m in machines if m.name not in booked_machines]
	
	return machines
