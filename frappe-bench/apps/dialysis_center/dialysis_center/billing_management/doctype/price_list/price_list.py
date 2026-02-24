import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class PriceList(Document):
	def validate(self):
		"""Validate price list"""
		self.validate_dates()
		self.check_default()
	
	def validate_dates(self):
		"""Validate date range"""
		if self.valid_from and self.valid_to:
			if getdate(self.valid_to) < getdate(self.valid_from):
				frappe.throw("Valid To date cannot be before Valid From date")
	
	def check_default(self):
		"""Ensure only one default price list per customer tier"""
		if self.is_default:
			existing = frappe.db.exists("Price List", {
				"name": ["!=", self.name],
				"customer_tier": self.customer_tier,
				"is_default": 1
			})
			if existing:
				frappe.throw(f"A default price list already exists for {self.customer_tier} tier")
	
	def is_active(self):
		"""Check if price list is currently active"""
		today = getdate(nowdate())
		
		if self.valid_from and getdate(self.valid_from) > today:
			return False
		
		if self.valid_to and getdate(self.valid_to) < today:
			return False
		
		return True

@frappe.whitelist()
def get_price(service_type, customer_tier="Standard"):
	"""Get price for a service type and customer tier"""
	# Try to find active default price list for tier
	price_list = frappe.db.get_value("Price List", {
		"customer_tier": customer_tier,
		"is_default": 1
	}, "name")
	
	if not price_list:
		# Fall back to standard tier
		price_list = frappe.db.get_value("Price List", {
			"customer_tier": "Standard",
			"is_default": 1
		}, "name")
	
	if price_list:
		# Get price from price list items
		price = frappe.db.get_value("Price List Item", {
			"parent": price_list,
			"service_type": service_type
		}, "rate")
		
		return price or 0
	
	return 0
