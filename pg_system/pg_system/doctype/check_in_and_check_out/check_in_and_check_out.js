// Copyright (c) 2024, patelasif52@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Check-in and Check-out', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			frm.set_value("status",'Checked In')
			frm.set_value("check_in_date",frappe.datetime.get_datetime_as_string())
		}
		frm.set_query("room",function(){
			return{
				filters:[['status','IN',['Available','Partially Occupied']], ['docstatus','=',1],['type','=',frm.doc.room_type]]
			}
		})
		if(frm.doc.docstatus == 1 && frm.doc.status!="Checked Out"){
			frm.add_custom_button("Process Checkout" ,function(){
				let d = new frappe.ui.Dialog({
					title: 'Enter details',
					fields: [
						{
							label: 'Check Out Date',
							fieldname: 'check_out_date',
							fieldtype: 'Datetime',
							default:frappe.datetime.get_datetime_as_string()
						},
						{
							label: 'Rating',
							fieldname: 'customer_rating',
							fieldtype: 'Rating',
						},
					],
					size: 'small',
					primary_action_label: 'Checkout',
					primary_action(values) {
						console.log(values);
						frm.set_value("status",'Checked Out')
						frm.set_value("customer_rating",values.customer_rating)
						frm.set_value("check_out_date",values.check_out_date)
						frm.save_or_update()
						d.hide();
					}
				});
				d.show();
			})
		}
	}
});
