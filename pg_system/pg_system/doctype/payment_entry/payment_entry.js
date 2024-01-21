// Copyright (c) 2024, patelasif52@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	refresh: function(frm) {
		frm.set_query("booking",function(frm){
			return{
				filters:{"status":"Checked Out", "docstatus":1}
			}
		})
	},
	booking:function(frm){
		frm.trigger('calculate_amount')
	},
	discount:function(frm){
		frm.trigger('calculate_amount')
	},
	calculate_amount:function(frm){
		frm.call({
			method:'calculate_ammount',
			doc:frm.doc,
		})
	}
});
