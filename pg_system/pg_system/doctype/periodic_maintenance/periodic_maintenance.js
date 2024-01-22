// Copyright (c) 2024, patelasif52@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Periodic Maintenance', {
	refresh: function(frm) {
		if(frm.doc.status == "Scheduled" && !frm.doc.__islocal && frm.doc.docstatus==1){
			frm.add_custom_button("Create Work Log" ,function(){
				frm.call({
					method:"pg_system.pg_system.doctype.periodic_maintenance.periodic_maintenance.create_work_log",
					args:{
						pm:frm.doc.name
					},
					callback:function(r){
						if(r.message==1){
							frappe.msgprint("Work Log Create Successfully.")
						}
					}
				})
			})
		}
	}
});
