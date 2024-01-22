# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employee(Document):
	def before_save(self):
		self.full_name = self.first_name+" "+ self.middle_name+" "+self.last_name if self.middle_name else self.first_name+" "+self.last_name
		if self.create_user_emp:
			self.user_id = self.create_user()

		if self.designation != 'Manager' and self.user_id:
			create_user_permisssion(self.user_id, self.name)

	@frappe.whitelist()
	def create_user(self):
		user = frappe.new_doc("User")
		user.email = self.email
		user.first_name = self.first_name
		user.last_name = self.last_name
		user.append('roles', {"doctype": "Has Role", "role": "PG Employee" if self.designation != 'Manager' else "PG Manager"})
		user.save(ignore_permissions=True)
		frappe.db.commit()
		return user.name


def create_user_permisssion(name, employee_id):
	user_perm = frappe.new_doc("User Permission")
	user_perm.user = name
	user_perm.allow = "Employee"
	user_perm.for_value = employee_id
	user_perm.save(ignore_permissions=True)
