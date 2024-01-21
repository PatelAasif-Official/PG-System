frappe.ready(function() {
	frappe.web_form.on('guest_first_name',(field, value) =>{
		get_full_name(value,frappe.web_form.get_value("guest_last_name"))
	}),

	frappe.web_form.on('guest_last_name',(field, value) =>{
		get_full_name(frappe.web_form.get_value("guest_first_name"),value)
	}),

	frappe.web_form.set_df_property('room','read_only',1)
	frappe.web_form.set_df_property('email_address','read_only',0)
	frappe.web_form.set_value('check_in_date',frappe.datetime.get_datetime_as_string())
})

function get_full_name(first_name,last_name){
	console.log("Thisjkbsdjkbg")
	frappe.web_form.set_value('guest_name',last_name ? first_name+' '+last_name:first_name)
}