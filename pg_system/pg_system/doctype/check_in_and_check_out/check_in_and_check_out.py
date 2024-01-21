# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CheckinandCheckout(Document):
	def before_submit(self):
		room = frappe.get_doc("Room",self.room)
		if room.number_of_beds_available == 0 and self.status=='Checked In':
			frappe.throw("Selected Room is not Available" if self.type_of_room == 'Single Occupancy' else "Bed is not Available in Selected Room.")
		room.number_of_beds_available = int(room.number_of_beds_available) - 1 if self.status=='Checked In' else int(room.number_of_beds_available) + 1
		room.save()
		room.run_method('update_status')
		


		# count = self.check_booked_room()
		# if self.type_of_room == 'Single Occupancy':
		# 	if count <= 1:
		# 		frappe.db.set_value('Room',self.room,'status','Occupied', update_modified=False)
		# 	else:
		# 		frappe.throw("Selected Room is not Available.")
		# else:
			
		# 	if self.type_of_room == 'Double Sharing':
		# 		if count == 2:
		# 			update_status(self.room,'Occupied',count)
		# 		elif count < 2:
		# 			update_status(self.room,'Partially Occupied',count)
		# 		elif count > 2:
		# 			frappe.throw("Selected Room is not Available.")
			
		# 	if self.type_of_room == 'Triple Sharing':
		# 		if count == 3:
		# 			update_status(self.room,'Occupied',count)
		# 		elif count < 3:
		# 			update_status(self.room,'Partially Occupied',count)
		# 		elif  count > 3:
		# 			frappe.throw("Selected Room is not Available.")
			
		# 	if self.type_of_room == "Multiple Sharing":
		# 		no_of_beds = frappe.db.get_value("Room",self.room,"number_of_beds")
		# 		if count == no_of_beds:
		# 			update_status(self.room,'Occupied',count)
		# 		elif count < no_of_beds:
		# 			update_status(self.room,'Partially Occupied',count)
		# 		elif count > no_of_beds:
		# 			frappe.throw("Selected Room is not Available.")

	def on_update_after_submit(self):
		self.before_submit()
		# if self.status=="Checked Out":
		# 	self.update_room_data()


	def update_room_data(self):
		frappe.db.set_value('Room',self.room,'status',status, update_modified=False)
	# def check_room_availability(self):
	# 	status = frappe.db.get_value("Room",self.room, 'status')
	# 	if status in ["Available",'Partially Occupied']:
	# 		return True
	# 	else:
	# 		return False

	def check_booked_room(self):
		count =  frappe.db.count("Check-in and Check-out",{"check_out":0,'docstatus':1,"room":self.room})
		#Adding one for self(Becouse selected document is not submitted yet)
		return count + 1
	
	
def update_status(room,status,no_of_beds):
	frappe.db.set_value('Room',room,'status',status, update_modified=False)
	frappe.db.set_value('Room',room,'number_of_beds_available',frappe.db.get_value('Room',room,"number_of_beds")-no_of_beds, update_modified=False)