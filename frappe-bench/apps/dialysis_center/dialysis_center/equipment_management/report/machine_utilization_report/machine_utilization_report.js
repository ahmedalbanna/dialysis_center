frappe.query_reports["Machine Utilization Report"] = {
	"filters": [
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nAvailable\nIn Use\nMaintenance\nOut of Service"
		}
	]
};
