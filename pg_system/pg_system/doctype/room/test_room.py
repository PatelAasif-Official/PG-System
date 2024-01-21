# Copyright (c) 2024, patelasif52@gmail.com and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestRoom(FrappeTestCase):
	def test_status(self):
		room = frappe.new_doc("Room")
		room.typ_of_room = "Multiple Sharing"
		room.number_of_beds = 4
		room.room_number = "G4"
		room.price = 3456
		room.photo1 = '/files/QRCode_CN-22-23-00073.png'
		room.save()
		room.submit()

		self.assertEqual(room.status,"Partially Occupied")