// Copyright (c) 2024, patelasif52@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee', {
	refresh: function(frm) {
		if(!frm.doc.user_id && !frm.doc.__islocal){
			frm.add_custom_button("Create User" ,function(){
				frm.call({
					method:"create_user",
					doc:frm.doc,
					callback:function(r){
						if(r.message){
							frm.set_value("user_id",r.message)
							frm.save()
						}
					}
				})
			})
		}
	}
});
