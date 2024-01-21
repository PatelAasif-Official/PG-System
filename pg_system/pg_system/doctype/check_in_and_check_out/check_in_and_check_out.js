// Copyright (c) 2024, patelasif52@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Check-in and Check-out', {
	refresh: function(frm) {
		frm.set_query("room",function(){
			return{
				filters:{'status':['IN',['Available','Partially Occupied']], 'docstatus':1}
			}
		})
	}
});
