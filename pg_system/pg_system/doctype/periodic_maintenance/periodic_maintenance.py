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


@frappe.whitelist()
def create_work_log(pm=None):
	if pm:
		all_task = [pm]
	else:
		all_task = frappe.db.get_all("Periodic Maintenance",{"schedule_date":today(),"docstatus":1, "status":"Scheduled"},pluck="name")
	
	if all_task:
		#Getting all Active Emp
		all_emp = frappe.db.get_all("Employee",{'status':'Active'},pluck="name")
		#Getting all the Rooms which are not in Maintenance Already
		all_rooms = frappe.db.get_all("Room",{"status":['!=','Under Maintenance']},pluck="name")
		min_works_per_employee = len(all_rooms) // len(all_emp)

		#Making list of list to discribute the Rooms to Employees as evenly as possible, as we do have Odd condition also.
		extra_employees = len(all_rooms) % len(all_emp)
		group = [all_rooms[i * min_works_per_employee:(i + 1) * min_works_per_employee] for i in range(len(all_emp) - extra_employees)]
		group.extend([all_rooms[i * (min_works_per_employee + 1):(i + 1) * (min_works_per_employee + 1)] for i in range(extra_employees)])
		
		#No Need to Enque as it will automatically goes to Background job as it will be run Hourly to check and assign the task
		create_log(all_task,all_emp,group)
		return 1

def create_log(all_task,all_emp,group):
	for task in all_task:
		i = 0
		task = frappe.get_doc("Periodic Maintenance",task)
		for emp in all_emp:
			work_log  = frappe.new_doc("Work Log")
			work_log.employee=emp
			work_log.status = "Pending"
			work_log.type_of_work = task.type_of_work
			work_log.periodic_maintenance = task.name
			work_log.duration = task.duration
			work_log.schedule_date = task.schedule_date
			work_log.schedule_time = task.schedule_time
			for room in group[i]:
				work_log.append("list_of_rooms",{
					"room":room,
					"room_number":frappe.db.get_value("Room",room,'room_number'),
					"status":frappe.db.get_value("Room",room,'status')
					})
			work_log.description = task.description
			work_log.save(ignore_permissions=True)
			i += 1

		task.status="Work Log Created"
		task.save(ignore_permissions=True)
		frappe.db.commit()
			

 