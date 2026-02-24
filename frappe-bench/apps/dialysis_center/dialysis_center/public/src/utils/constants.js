/**
 * Dialysis Center - Constants & Enums
 * Centralized constants for consistent UI across the application
 */

export const BLOOD_TYPES = [
	'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
];

export const PATIENT_STATUS = {
	ACTIVE: 'Active',
	INACTIVE: 'Inactive',
	DECEASED: 'Deceased',
	TRANSFERRED: 'Transferred'
};

export const SESSION_STATUS = {
	SCHEDULED: 'Scheduled',
	IN_PROGRESS: 'In Progress',
	COMPLETED: 'Completed',
	CANCELLED: 'Cancelled',
	INTERRUPTED: 'Interrupted'
};

export const APPOINTMENT_STATUS = {
	SCHEDULED: 'Scheduled',
	CONFIRMED: 'Confirmed',
	CHECKED_IN: 'Checked In',
	IN_PROGRESS: 'In Progress',
	COMPLETED: 'Completed',
	CANCELLED: 'Cancelled',
	NO_SHOW: 'No Show'
};

export const INVOICE_STATUS = {
	DRAFT: 'Draft',
	SUBMITTED: 'Submitted',
	PAID: 'Paid',
	PARTIALLY_PAID: 'Partially Paid',
	OVERDUE: 'Overdue',
	CANCELLED: 'Cancelled'
};

export const MACHINE_STATUS = {
	AVAILABLE: 'Available',
	IN_USE: 'In Use',
	MAINTENANCE: 'Under Maintenance',
	OUT_OF_SERVICE: 'Out of Service',
	RESERVED: 'Reserved'
};

export const STATUS_COLORS = {
	Active: 'green',
	Inactive: 'orange',
	Deceased: 'red',
	Transferred: 'blue',
	Scheduled: 'blue',
	'In Progress': 'orange',
	Completed: 'green',
	Cancelled: 'red',
	Interrupted: 'red',
	Confirmed: 'cyan',
	'Checked In': 'purple',
	'No Show': 'darkgray',
	Draft: 'gray',
	Submitted: 'blue',
	Paid: 'green',
	'Partially Paid': 'orange',
	Overdue: 'red',
	Available: 'green',
	'In Use': 'orange',
	'Under Maintenance': 'yellow',
	'Out of Service': 'red',
	Reserved: 'blue'
};

export const VITALS_RANGES = {
	systolic_bp: { min: 90, max: 140, unit: 'mmHg', label: 'Systolic BP' },
	diastolic_bp: { min: 60, max: 90, unit: 'mmHg', label: 'Diastolic BP' },
	heart_rate: { min: 60, max: 100, unit: 'bpm', label: 'Heart Rate' },
	temperature: { min: 36.1, max: 37.2, unit: '°C', label: 'Temperature' },
	weight: { min: 0, max: 300, unit: 'kg', label: 'Weight' }
};

export const API_ENDPOINTS = {
	PATIENT: {
		LIST: 'dialysis_center.api.patient.get_patient_list',
		DETAILS: 'dialysis_center.api.patient.get_patient_details',
		DASHBOARD: 'dialysis_center.api.patient.get_patient_dashboard',
		VITAL_TRENDS: 'dialysis_center.api.patient.get_patient_vital_trends',
		SEARCH: 'dialysis_center.api.patient.search_patients'
	},
	SESSION: {
		LIST: 'dialysis_center.api.session.get_session_list',
		DETAILS: 'dialysis_center.api.session.get_session_details',
		ACTIVE: 'dialysis_center.api.session.get_active_sessions',
		STATISTICS: 'dialysis_center.api.session.get_session_statistics',
		VITAL_HISTORY: 'dialysis_center.api.session.get_session_vital_history',
		ADD_VITAL: 'dialysis_center.api.session.add_vital_reading'
	},
	APPOINTMENT: {
		LIST: 'dialysis_center.api.appointment.get_appointment_list',
		DAILY_SCHEDULE: 'dialysis_center.api.appointment.get_daily_schedule',
		AVAILABLE_SLOTS: 'dialysis_center.api.appointment.get_available_slots'
	},
	BILLING: {
		REVENUE_SUMMARY: 'dialysis_center.api.billing.get_revenue_summary',
		OUTSTANDING: 'dialysis_center.api.billing.get_outstanding_invoices'
	}
};
