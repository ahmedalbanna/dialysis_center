frappe.ui.form.on('Treatment Template', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Create Session from Template'), function() {
				frappe.new_doc('Dialysis Session', {
					dialysis_modality: frm.doc.dialysis_modality,
					treatment_duration: frm.doc.treatment_duration,
					blood_flow_rate: frm.doc.blood_flow_rate,
					dialysate_flow_rate: frm.doc.dialysate_flow_rate,
					dialyzer_type: frm.doc.dialyzer_type
				});
			});
		}
	}
});
