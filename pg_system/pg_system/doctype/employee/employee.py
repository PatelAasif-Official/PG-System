# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employee(Document):
	def before_save(self):
		self.full_name = self.first_name+" "+ self.middle_name+" "+self.last_name if self.middle_name else self.first_name+" "+self.last_name
		if self.create_user_emp and not self.user_id:
			self.user_id = self.create_user()

	@frappe.whitelist()
	def create_user(self):
		"""
		White listed class method so we can use this from backend as well as from end, it will create user for the employee
		User lined field becouse we can use user permission for the employee
		"""
		try:
			user = frappe.new_doc("User")
			user.email = self.email
			user.first_name = self.first_name
			user.last_name = self.last_name
			user.append('roles', {"doctype": "Has Role", "role": "PG Employee" if self.designation != 'Manager' else "PG Manager"})
			user.save(ignore_permissions=True)
			frappe.db.commit()
			return user.name
		except:
			self.log_error()


