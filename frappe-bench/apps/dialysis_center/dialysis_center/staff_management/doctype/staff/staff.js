frappe.ui.form.on('Staff', {
	refresh: function(frm) {
		if (!frm.is_new() && frm.doc.status === 'Active') {
			frm.add_custom_button(__('Assign Shift'), function() {
				frappe.new_doc('Shift', {
					staff: frm.doc.name,
					staff_name: frm.doc.full_name
				});
			});
		}
	}
});
