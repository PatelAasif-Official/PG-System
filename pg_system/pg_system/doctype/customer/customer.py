# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Customer(Document):
	def before_save(self):
		self.full_name = self.first_name+" "+ self.middle_name+" "+self.last_name if self.middle_name else self.first_name+" "+self.last_name
