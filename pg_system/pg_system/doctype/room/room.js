// Copyright (c) 2024, patelasif52@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room', {
	// refresh: function(frm) {
	// 	if(frm.doc.docstatus == 1 && frm.doc.status=="Available"){
	// 		frm.add_custom_button("Under Maintenance",function(){
	// 			frm.set_value("status",'Under Maintenance')
	// 			frm.reload_doc()
	// 		})
	// 	}
	// 	if(frm.doc.docstatus == 1 && frm.doc.status=="Under Maintenance"){
	// 		frm.add_custom_button("Make Available",function(){
	// 			frm.set_value("status",'Available')
	// 			frm.reload_doc()
	// 		})
	// 	}
	// },
	// type_of_room:function(frm){
	// 	if(frm.doc.type_of_room == "Single Occupancy"){
	// 		frm.set_value("number_of_beds",1)
	// 		frm.set_value("number_of_beds_available",1)
	// 	}
	// 	if( frm.doc.type_of_room == 'Double Sharing'){
	// 		frm.set_value("number_of_beds",2)
	// 		frm.set_value("number_of_beds_available",2)
	// 	}
	// 	if (frm.doc.type_of_room == 'Triple Sharing'){
	// 		frm.set_value("number_of_beds",3)
	// 		frm.set_value("number_of_beds_available",3)
	// 	}
	// 	if (!frm.doc.type_of_room){
	// 		frm.set_value("number_of_beds",undefined)
	// 		frm.set_value("number_of_beds_available",undefined)
	// 	}
	// }
});
