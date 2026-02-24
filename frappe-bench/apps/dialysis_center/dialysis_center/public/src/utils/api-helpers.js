/**
 * Dialysis Center - API Helpers
 * Wrapper functions for frappe.call() organized by module
 */

import { API_ENDPOINTS } from './constants.js';

/**
 * Generic API call wrapper
 */
async function callAPI(method, args = {}) {
	return new Promise((resolve, reject) => {
		frappe.call({
			method,
			args,
			callback: (r) => {
				if (r.message) {
					resolve(r.message);
				} else {
					resolve(null);
				}
			},
			error: (err) => {
				console.error('API Error:', err);
				frappe.msgprint({
					title: __('Error'),
					message: __('An error occurred while fetching data'),
					indicator: 'red'
				});
				reject(err);
			}
		});
	});
}

/**
 * Patient API Helpers
 */
export const PatientAPI = {
	async getList(filters = {}) {
		return callAPI(API_ENDPOINTS.PATIENT.LIST, { filters });
	},
	
	async getDetails(patientId) {
		return callAPI(API_ENDPOINTS.PATIENT.DETAILS, { patient: patientId });
	},
	
	async getDashboard(patientId) {
		return callAPI(API_ENDPOINTS.PATIENT.DASHBOARD, { patient: patientId });
	},
	
	async getVitalTrends(patientId, days = 30) {
		return callAPI(API_ENDPOINTS.PATIENT.VITAL_TRENDS, { patient: patientId, days });
	},
	
	async search(query) {
		return callAPI(API_ENDPOINTS.PATIENT.SEARCH, { query });
	}
};

/**
 * Session API Helpers
 */
export const SessionAPI = {
	async getList(filters = {}) {
		return callAPI(API_ENDPOINTS.SESSION.LIST, { filters });
	},
	
	async getDetails(sessionId) {
		return callAPI(API_ENDPOINTS.SESSION.DETAILS, { session: sessionId });
	},
	
	async getActiveSessions() {
		return callAPI(API_ENDPOINTS.SESSION.ACTIVE);
	},
	
	async getStatistics(filters = {}) {
		return callAPI(API_ENDPOINTS.SESSION.STATISTICS, { filters });
	},
	
	async getVitalHistory(sessionId) {
		return callAPI(API_ENDPOINTS.SESSION.VITAL_HISTORY, { session: sessionId });
	},
	
	async addVitalReading(sessionId, vitals) {
		return callAPI(API_ENDPOINTS.SESSION.ADD_VITAL, { 
			session: sessionId, 
			vitals 
		});
	}
};

/**
 * Appointment API Helpers
 */
export const AppointmentAPI = {
	async getList(filters = {}) {
		return callAPI(API_ENDPOINTS.APPOINTMENT.LIST, { filters });
	},
	
	async getDailySchedule(date) {
		return callAPI(API_ENDPOINTS.APPOINTMENT.DAILY_SCHEDULE, { date });
	},
	
	async getAvailableSlots(date, machineId = null) {
		return callAPI(API_ENDPOINTS.APPOINTMENT.AVAILABLE_SLOTS, { 
			date, 
			machine: machineId 
		});
	}
};

/**
 * Billing API Helpers
 */
export const BillingAPI = {
	async getRevenueSummary(startDate, endDate) {
		return callAPI(API_ENDPOINTS.BILLING.REVENUE_SUMMARY, { 
			start_date: startDate, 
			end_date: endDate 
		});
	},
	
	async getOutstandingInvoices() {
		return callAPI(API_ENDPOINTS.BILLING.OUTSTANDING);
	}
};

/**
 * Helper to show loading indicator
 */
export function showLoading(message = 'Loading...') {
	frappe.freeze(message);
}

export function hideLoading() {
	frappe.unfreeze();
}

/**
 * Helper to show success message
 */
export function showSuccess(message) {
	frappe.show_alert({
		message: __(message),
		indicator: 'green'
	}, 3);
}

/**
 * Helper to show error message
 */
export function showError(message) {
	frappe.msgprint({
		title: __('Error'),
		message: __(message),
		indicator: 'red'
	});
}
