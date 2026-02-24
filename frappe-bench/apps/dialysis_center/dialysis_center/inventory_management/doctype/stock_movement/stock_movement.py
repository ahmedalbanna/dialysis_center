import frappe
from frappe.model.document import Document
from frappe.utils import flt, nowdate, getdate
from frappe import _

class StockMovement(Document):
	def validate(self):
		self.validate_medication()
		self.validate_quantity()
		self.fetch_current_stock()
		self.calculate_new_stock()
		self.validate_stock_availability()
		self.set_movement_date()
	
	def validate_medication(self):
		"""Validate medication exists"""
		if not self.medication:
			frappe.throw(_("Medication is required"))
		
		if not frappe.db.exists("Medication", self.medication):
			frappe.throw(_("Medication {0} does not exist").format(self.medication))
	
	def validate_quantity(self):
		"""Validate quantity is positive"""
		if flt(self.quantity) <= 0:
			frappe.throw(_("Quantity must be greater than 0"))
	
	def fetch_current_stock(self):
		"""Fetch current stock from medication master"""
		if self.medication and not self.current_stock:
			self.current_stock = frappe.db.get_value("Medication", self.medication, "current_stock") or 0
		
		self.previous_stock = self.current_stock or 0
	
	def calculate_new_stock(self):
		"""Calculate new stock level based on movement type"""
		if self.movement_type in ["Receipt", "Return"]:
			# Increase stock
			self.new_stock = flt(self.previous_stock) + flt(self.quantity)
		elif self.movement_type in ["Issue", "Expired", "Damaged"]:
			# Decrease stock
			self.new_stock = flt(self.previous_stock) - flt(self.quantity)
		elif self.movement_type == "Adjustment":
			# Set to specific quantity
			self.new_stock = flt(self.quantity)
		else:
			frappe.throw(_("Invalid movement type: {0}").format(self.movement_type))
	
	def validate_stock_availability(self):
		"""Ensure sufficient stock for issue/expired movements"""
		if self.movement_type in ["Issue", "Expired", "Damaged"]:
			if flt(self.new_stock) < 0:
				frappe.throw(_("Insufficient stock. Available: {0}, Requested: {1}").format(
					self.previous_stock, self.quantity))
	
	def set_movement_date(self):
		"""Set movement date if not set"""
		if not self.movement_date:
			self.movement_date = nowdate()
		
		# Validate movement date is not in future
		if getdate(self.movement_date) > getdate():
			frappe.throw(_("Movement date cannot be in the future"))
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from notes
		if self.remarks:
			self.remarks = self.remarks.strip()
		
		# Recalculate stock before saving
		self.fetch_current_stock()
		self.calculate_new_stock()
	
	def before_submit(self):
		"""Validate before submission"""
		if not self.movement_type:
			frappe.throw(_("Movement type is required"))
		
		# Recalculate to ensure accuracy
		self.fetch_current_stock()
		self.calculate_new_stock()
		self.validate_stock_availability()
	
	def on_submit(self):
		"""Update medication stock after submission"""
		self.update_medication_stock()
		self.create_stock_ledger_entry()
	
	def on_update(self):
		"""Called after saving"""
		# Clear related caches
		frappe.cache.delete_value(f"stock_movement_{self.name}")
		frappe.cache.delete_value(f"medication_{self.medication}_stock")
	
	def update_medication_stock(self):
		"""Update medication master with new stock level"""
		if self.medication:
			medication = frappe.get_doc("Medication", self.medication)
			medication.current_stock = flt(self.new_stock)
			medication.last_stock_movement = self.name
			medication.last_movement_date = self.movement_date
			medication.save(ignore_permissions=True)
			
			# Add comment
			medication.add_comment("Comment", _("Stock updated via {0}: {1} → {2}").format(
				self.movement_type, self.previous_stock, self.new_stock))
	
	def create_stock_ledger_entry(self):
		"""Create stock ledger entry for audit trail"""
		# This is a placeholder for future stock ledger functionality
		pass
	
	def on_cancel(self):
		"""Reverse stock movement on cancellation"""
		self.reverse_stock_movement()
	
	def reverse_stock_movement(self):
		"""Reverse the stock update"""
		if self.medication:
			medication = frappe.get_doc("Medication", self.medication)
			
			# Reverse the movement
			if self.movement_type in ["Receipt", "Return"]:
				# Was increase, now decrease
				medication.current_stock = max(flt(medication.current_stock) - flt(self.quantity), 0)
			elif self.movement_type in ["Issue", "Expired", "Damaged"]:
				# Was decrease, now increase
				medication.current_stock = flt(medication.current_stock) + flt(self.quantity)
			elif self.movement_type == "Adjustment":
				# Restore previous stock
				medication.current_stock = flt(self.previous_stock)
			
			medication.save(ignore_permissions=True)
			medication.add_comment("Comment", _("Stock movement {0} cancelled").format(self.name))

@frappe.whitelist()
def get_medication_stock(medication):
	"""Get current stock level for a medication"""
	if not medication:
		return 0
	
	current_stock = frappe.db.get_value("Medication", medication, "current_stock") or 0
	return current_stock

@frappe.whitelist()
def create_stock_issue(medication, quantity, patient=None, session=None, remarks=None):
	"""Create stock issue for medication usage"""
	if not medication or not quantity:
		frappe.throw(_("Medication and quantity are required"))
	
	# Check stock availability
	current_stock = frappe.db.get_value("Medication", medication, "current_stock") or 0
	if flt(current_stock) < flt(quantity):
		frappe.throw(_("Insufficient stock. Available: {0}").format(current_stock))
	
	# Create stock movement
	movement = frappe.get_doc({
		"doctype": "Stock Movement",
		"medication": medication,
		"movement_type": "Issue",
		"quantity": quantity,
		"patient": patient,
		"session": session,
		"remarks": remarks or "Stock issued for patient treatment",
		"movement_date": nowdate()
	})
	movement.insert()
	movement.submit()
	
	return movement.name
