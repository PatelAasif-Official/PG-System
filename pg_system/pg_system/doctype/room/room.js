// Copyright (c) 2024, patelasif52@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room', {
	refresh: function(frm) {
		if (frappe.user.has_role("PG Manager")){
			if(!frm.doc.__islocal && frm.is_dirty()==false){
				frm.add_custom_button(frm.doc.published == 1 ? "Unpublish":"Publish" ,function(){
					frm.set_value("published",frm.doc.published == 1 ? 0:1)
				})
				frm.add_custom_button("Update Price" ,function(){
					let d = new frappe.ui.Dialog({
						title: 'Enter details',
						fields: [
							{
								label: 'New Price',
								fieldname: 'price',
								fieldtype: 'Currency',
								default:frm.doc.price
							},
						],
						size: 'small',
						primary_action_label: 'Update',
						primary_action(values) {
							if(values.price == frm.doc.price){
								frappe.throw("Same Price")
							}else{
								frm.set_value("price",values.price)
							}
							frm.save_or_update()
							d.hide();
						}
					});
					d.show();
				})
			}
		}
		if(frm.doc.docstatus == 1 && frm.doc.status=="Available"){
			frm.add_custom_button("Under Maintenance",function(){
				set_status(frm,"Under Maintenance")
			})
		}
		if(frm.doc.docstatus == 1 && frm.doc.status=="Under Maintenance"){
			frm.add_custom_button("Make Available",function(){
				set_status(frm,"Available")
			})
		}
	},

	type_of_room:function(frm){
		if(frm.doc.type_of_room == "Single Occupancy"){
			frm.set_value("number_of_beds",1)
			frm.set_value("number_of_beds_available",1)
		}
		if( frm.doc.type_of_room == 'Double Sharing'){
			frm.set_value("number_of_beds",2)
			frm.set_value("number_of_beds_available",2)
		}
		if (frm.doc.type_of_room == 'Triple Sharing'){
			frm.set_value("number_of_beds",3)
			frm.set_value("number_of_beds_available",3)
		}
		if (!frm.doc.type_of_room){
			frm.set_value("number_of_beds",undefined)
			frm.set_value("number_of_beds_available",undefined)
		}
	}
});

function set_status(frm,status){
	frm.set_value("status",status)
	frm.save_or_update()
}
