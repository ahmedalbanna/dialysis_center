import frappe
from frappe.model.document import Document

class InvoiceItem(Document):
	def before_save(self):
		"""Calculate amount before saving"""
		if self.quantity and self.rate:
			self.amount = self.quantity * self.rate
