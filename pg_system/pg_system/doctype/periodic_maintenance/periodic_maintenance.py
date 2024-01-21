# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, getdate
from frappe.model.document import Document

class PeriodicMaintenance(Document):
	def validate(self):
		if getdate(self.schedule_date) < getdate(today()):
			frappe.throw("Schedule Date cannot be Past Date.")
		
		exist = frappe.db.exists(self.doctype,{"name":['!=',self.name], "type_of_work":self.type_of_work,"schedule_date":self.schedule_date})
		if exist:
			frappe.throw(f"{self.type_of_work} is already Scheduled for date {self.schedule_date}.")


def create_work_log():
	pass