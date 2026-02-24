frappe.ui.form.on('Medication', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Record Stock Movement'), function() {
				frappe.new_doc('Stock Movement', {
					medication: frm.doc.name,
					current_stock: frm.doc.current_stock
				});
			});
		}
	}
});
