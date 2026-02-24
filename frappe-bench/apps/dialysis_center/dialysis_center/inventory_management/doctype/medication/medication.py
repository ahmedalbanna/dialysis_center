import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate
from frappe import _

class Medication(Document):
	def validate(self):
		self.validate_quantities()
		self.validate_unit()
		self.check_reorder_level()
		self.check_expiry_date()
		self.set_stock_status()
	
	def validate_unit(self):
		"""Validate medication unit is specified"""
		if not self.unit:
			frappe.throw(_("Unit of Measurement is required"))
	
	def validate_quantities(self):
		"""Validate stock quantities"""
		if flt(self.current_stock) < 0:
			frappe.throw(_("Current stock cannot be negative"))
		
		if self.reorder_level and flt(self.reorder_level) < 0:
			frappe.throw(_("Reorder level cannot be negative"))
		
		if self.minimum_stock and flt(self.minimum_stock) < 0:
			frappe.throw(_("Minimum stock cannot be negative"))
	
	def check_reorder_level(self):
		"""Alert if stock is below reorder level"""
		if self.reorder_level and flt(self.current_stock) <= flt(self.reorder_level):
			frappe.msgprint(_("Stock is below reorder level for {0}. Current: {1}, Reorder at: {2}").format(
				self.medication_name, self.current_stock, self.reorder_level), 
				indicator="orange", alert=True)
		
		# Critical stock level (below minimum)
		if self.minimum_stock and flt(self.current_stock) < flt(self.minimum_stock):
			frappe.msgprint(_("CRITICAL: Stock is below minimum level for {0}").format(
				self.medication_name), indicator="red", alert=True)
	
	def check_expiry_date(self):
		"""Check if medication is expired or near expiry"""
		if hasattr(self, 'expiry_date') and self.expiry_date:
			from frappe.utils import date_diff, nowdate
			days_to_expiry = date_diff(self.expiry_date, nowdate())
			
			if days_to_expiry < 0:
				frappe.msgprint(_("Medication {0} has EXPIRED on {1}").format(
					self.medication_name, self.expiry_date), 
					indicator="red", alert=True)
			elif days_to_expiry <= 30:
				frappe.msgprint(_("Medication {0} will expire in {1} days").format(
					self.medication_name, days_to_expiry), 
					indicator="orange", alert=True)
	
	def set_stock_status(self):
		"""Set stock status indicator"""
		if not self.current_stock or flt(self.current_stock) == 0:
			self.stock_status = "Out of Stock"
		elif self.minimum_stock and flt(self.current_stock) < flt(self.minimum_stock):
			self.stock_status = "Critical"
		elif self.reorder_level and flt(self.current_stock) <= flt(self.reorder_level):
			self.stock_status = "Low Stock"
		else:
			self.stock_status = "In Stock"
	
	def before_save(self):
		"""Normalize data before saving"""
		# Trim whitespace from name and description
		if self.medication_name:
			self.medication_name = self.medication_name.strip()
		
		if self.description:
			self.description = self.description.strip()
		
		# Normalize unit
		if self.unit:
			self.unit = self.unit.strip()
		
		# Validate reorder level logic
		if self.reorder_level and self.minimum_stock:
			if flt(self.reorder_level) < flt(self.minimum_stock):
				frappe.msgprint(_("Warning: Reorder level is less than minimum stock level"),
					indicator="orange", alert=True)
