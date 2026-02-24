frappe.ui.form.on('Shift', {
	shift_type: function(frm) {
		if (frm.doc.shift_type === 'Morning (6AM-2PM)') {
			frm.set_value('start_time', '06:00:00');
			frm.set_value('end_time', '14:00:00');
		} else if (frm.doc.shift_type === 'Evening (2PM-10PM)') {
			frm.set_value('start_time', '14:00:00');
			frm.set_value('end_time', '22:00:00');
		} else if (frm.doc.shift_type === 'Night (10PM-6AM)') {
			frm.set_value('start_time', '22:00:00');
			frm.set_value('end_time', '06:00:00');
		}
	}
});
