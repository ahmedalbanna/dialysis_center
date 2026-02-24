frappe.ui.form.on('Payment', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Print Receipt'), function() {
				frappe.set_route('print', 'Payment', frm.doc.name);
			});
		}
	},
	
	amount: function(frm) {
		// Calculate change if cash payment
		if (frm.doc.payment_method === 'Cash' && frm.doc.amount_tendered) {
			frm.set_value('change_amount', frm.doc.amount_tendered - frm.doc.amount);
		}
	},
	
	amount_tendered: function(frm) {
		if (frm.doc.payment_method === 'Cash' && frm.doc.amount) {
			frm.set_value('change_amount', frm.doc.amount_tendered - frm.doc.amount);
		}
	}
});
