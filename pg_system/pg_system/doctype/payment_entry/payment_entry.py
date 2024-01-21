# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff, getdate
from frappe.model.document import Document

class PaymentEntry(Document):
	def before_submit(self):
		self.calculate_ammount()

	def before_save(self):
		if frappe.db.exists("Payment Entry",{'Booking':self.booking}):
			frappe.throw("Payment Entry for {0} is already exist.".format(self.guest_full_name))

	@frappe.whitelist()
	def calculate_ammount(self):
		no_of_night = date_diff(getdate(self.check_out_date), getdate(self.check_in_date))
		if no_of_night==0:
			no_of_night = 1

		self.no_of_night_stay = no_of_night
		self.total = no_of_night*self.rate_per_night
		if self.discount:
			self.grand_total = self.total - self.total*(self.discount/100)
		else:
			self.grand_total = self.total