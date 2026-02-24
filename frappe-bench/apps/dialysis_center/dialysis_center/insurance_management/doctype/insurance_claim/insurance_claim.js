frappe.ui.form.on('Insurance Claim', {
	invoice: function(frm) {
		if (frm.doc.invoice) {
			frappe.db.get_value('Invoice', frm.doc.invoice, ['total_amount', 'patient'], (r) => {
				frm.set_value('invoice_amount', r.total_amount);
				frm.set_value('patient', r.patient);
				frm.set_value('claim_amount', r.total_amount);
			});
		}
	}
});
