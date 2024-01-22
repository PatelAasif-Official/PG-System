# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, get_datetime

class CheckinandCheckout(Document):
	def before_insert(self):
		if self.from_portal == 1:
			self.guest = self.create_customer()

	def validate(self):
		if self.docstatus==1 and get_datetime(self.check_in_date) > get_datetime(now()):
			frappe.throw("Can not submit before Check In Date.")

	def before_submit(self):
		"""
		Updating rooms doctype with latest data on checkin available beds will substracted by 1 and on checkout
		adding one, the no of beds is the main field which automatically update the status of the room.
		"""
		room = frappe.get_doc("Room",self.room)
		if room.number_of_beds_available == 0 and self.status=='Checked In':
			frappe.throw("Selected Room is not Available" if self.type_of_room == 'Single Occupancy' else "Bed is not Available in Selected Room.")
		room.number_of_beds_available = int(room.number_of_beds_available) - 1 if self.status=='Checked In' else int(room.number_of_beds_available) + 1
		room.save()
		room.run_method('update_status')

	def on_update_after_submit(self):
		#Calling before submit for checkout
		self.before_submit()
	
	def create_customer(self):
		"""
		This method will call if the checkin is comming from Wefbform, otherwise it will not trigger.
		"""
		cust=frappe.new_doc("Customer")
		cust.first_name = self.guest_first_name
		cust.last_name = self.guest_last_name
		cust.mobile_number = self.mobile_number
		cust.email_address = self.email_address
		cust.flags.ignore_mandatory = True
		cust.save(ignore_permissions=True)
		return cust.name
	
def update_status(room,status,no_of_beds):
	frappe.db.set_value('Room',room,'status',status, update_modified=False)
	frappe.db.set_value('Room',room,'number_of_beds_available',frappe.db.get_value('Room',room,"number_of_beds")-no_of_beds, update_modified=False)