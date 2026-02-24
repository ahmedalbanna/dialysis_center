frappe.ui.form.on('Stock Movement', {
	medication: function(frm) {
		if (frm.doc.medication) {
			frappe.db.get_value('Medication', frm.doc.medication, 'current_stock', (r) => {
				frm.set_value('current_stock', r.current_stock);
			});
		}
	}
});
