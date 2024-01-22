# Copyright (c) 2024, patelasif52@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Room(WebsiteGenerator):
	def before_save(self):
		self.published = 1
		if self.type_of_room == 'Single Occupancy':
			self.number_of_beds = 1
		if self.type_of_room == 'Double Sharing':
			self.number_of_beds = 2
		if self.type_of_room == 'Triple Sharing':
			self.number_of_beds = 3

	def on_submit(self):
		self.number_of_beds_available = self.number_of_beds
		self.validate_beds_available()

	def before_update_after_submit(self):
		self.validate_beds_available()
		self.update_status()

	def update_status(self):
		"""
		Updating status based on no of beds available
		"""
		if self.status != 'Under Maintenance':
			if self.number_of_beds_available == 0:
				self.status = "Occupied"
			elif self.number_of_beds_available == self.number_of_beds:
				self.status = "Available"
			elif self.number_of_beds_available > 0 and self.number_of_beds_available < self.number_of_beds:
				self.status = "Partially Occupied"

	def validate_beds_available(self):
		if self.type_of_room == 'Single Occupancy':
			if self.number_of_beds_available > 1: frappe.throw("Number Of Beds Available cannot be greater then total number of Beds")
		if self.type_of_room == 'Double Sharing':
			if self.number_of_beds_available > 2: frappe.throw("Number Of Beds Available cannot be greater then total number of Beds")
		if self.type_of_room == 'Triple Sharing':
			if self.number_of_beds_available > 3: frappe.throw("Number Of Beds Available cannot be greater then total number of Beds")
		if self.type_of_room == 'Multiple Sharing':
			if self.number_of_beds_available > self.number_of_beds: frappe.throw("Number Of Beds Available cannot be greater then total number of Beds")


