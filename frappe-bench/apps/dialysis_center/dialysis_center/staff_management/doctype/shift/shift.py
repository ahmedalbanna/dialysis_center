import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours, getdate, get_datetime, nowdate, flt
from frappe import _

class Shift(Document):
	def validate(self):
		self.validate_staff()
		self.validate_times()
		self.validate_overlapping_shifts()
		self.calculate_hours()
		self.set_status()
	
	def validate_staff(self):
		"""Validate staff exists and is active"""
		if self.staff:
			staff_status = frappe.db.get_value("Staff", self.staff, "status")
			if staff_status != "Active":
				frappe.msgprint(_("Warning: Shift assigned to inactive staff member"),
					indicator="orange", alert=True)
	
	def validate_times(self):
		"""Validate shift times"""
		if self.shift_start and self.shift_end:
			# For same-day shifts
			if get_datetime(self.shift_end) <= get_datetime(self.shift_start):
				frappe.throw(_("Shift End time must be after Shift Start time"))
		
		if self.actual_start and self.actual_end:
			if get_datetime(self.actual_end) <= get_datetime(self.actual_start):
				frappe.throw(_("Actual End time must be after Actual Start time"))
	
	def validate_overlapping_shifts(self):
		"""Check for overlapping shifts for the same staff"""
		if not self.staff or not self.shift_date or not self.shift_start or not self.shift_end:
			return
		
		# Check for overlapping shifts
		overlapping = frappe.db.sql("""
			SELECT name 
			FROM `tabShift`
			WHERE staff = %s 
			AND shift_date = %s
			AND name != %s
			AND (
				(shift_start <= %s AND shift_end > %s)
				OR (shift_start < %s AND shift_end >= %s)
				OR (shift_start >= %s AND shift_end <= %s)
			)
		""", (self.staff, self.shift_date, self.name or '',
			  self.shift_start, self.shift_start,
			  self.shift_end, self.shift_end,
			  self.shift_start, self.shift_end))
		
		if overlapping:
			frappe.throw(_("Staff {0} already has an overlapping shift on {1}").format(
				self.staff, self.shift_date))
	
	def calculate_hours(self):
		"""Calculate total working hours"""
		# Use actual times if available, otherwise use scheduled times
		start_time = self.actual_start or self.shift_start
		end_time = self.actual_end or self.shift_end
		
		if start_time and end_time:
			total_hours = time_diff_in_hours(end_time, start_time)
			break_hours = flt(self.break_duration or 0) / 60.0
			self.total_hours = flt(total_hours - break_hours, 2)
			
			# Validate break duration
			if break_hours > total_hours:
				frappe.throw(_("Break duration cannot exceed shift duration"))
	
	def set_status(self):
		"""Auto-set shift status"""
		if not self.status:
			if self.actual_end:
				self.status = "Completed"
			elif self.actual_start:
				self.status = "In Progress"
			else:
				self.status = "Scheduled"
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from notes
		if self.notes:
			self.notes = self.notes.strip()
		
		# Recalculate hours before save
		self.calculate_hours()
	
	def on_submit(self):
		"""Called when shift is submitted - assign staff to shift"""
		self.assign_staff_to_shift()
	
	def assign_staff_to_shift(self):
		"""Assign staff member to this shift"""
		if self.staff:
			try:
				# You can add shift assignment logic here if needed
				# For now, just log the submission
				frappe.db.set_value("Shift", self.name, "is_submitted", 1)
			except Exception as e:
				frappe.log_error(message=str(e), title="Shift Assignment Failed")

@frappe.whitelist()
def get_staff_schedule(staff, from_date, to_date):
	"""Get staff schedule for a date range"""
	if not staff:
		return []
	
	shifts = frappe.get_all("Shift",
		filters={
			"staff": staff,
			"shift_date": ["between", [from_date, to_date]]
		},
		fields=["name", "shift_date", "shift_start", "shift_end", "total_hours", "status"],
		order_by="shift_date, shift_start"
	)
	
	return shifts
