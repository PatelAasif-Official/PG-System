# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WorkLog(Document):
	def before_insert(self):
		if frappe.db.exists(self.doctype,{"employee":self.employee,"periodic_maintenance":self.periodic_maintenance}):
			frappe.throw(f"Work Already created using {self.periodic_maintenance}")
