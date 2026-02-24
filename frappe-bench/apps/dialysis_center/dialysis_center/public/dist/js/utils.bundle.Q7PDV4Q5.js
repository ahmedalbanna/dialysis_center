(() => {
  var __defProp = Object.defineProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };

  // ../dialysis_center/dialysis_center/public/src/utils/constants.js
  var constants_exports = {};
  __export(constants_exports, {
    API_ENDPOINTS: () => API_ENDPOINTS,
    APPOINTMENT_STATUS: () => APPOINTMENT_STATUS,
    BLOOD_TYPES: () => BLOOD_TYPES,
    INVOICE_STATUS: () => INVOICE_STATUS,
    MACHINE_STATUS: () => MACHINE_STATUS,
    PATIENT_STATUS: () => PATIENT_STATUS,
    SESSION_STATUS: () => SESSION_STATUS,
    STATUS_COLORS: () => STATUS_COLORS,
    VITALS_RANGES: () => VITALS_RANGES
  });
  var BLOOD_TYPES = [
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-"
  ];
  var PATIENT_STATUS = {
    ACTIVE: "Active",
    INACTIVE: "Inactive",
    DECEASED: "Deceased",
    TRANSFERRED: "Transferred"
  };
  var SESSION_STATUS = {
    SCHEDULED: "Scheduled",
    IN_PROGRESS: "In Progress",
    COMPLETED: "Completed",
    CANCELLED: "Cancelled",
    INTERRUPTED: "Interrupted"
  };
  var APPOINTMENT_STATUS = {
    SCHEDULED: "Scheduled",
    CONFIRMED: "Confirmed",
    CHECKED_IN: "Checked In",
    IN_PROGRESS: "In Progress",
    COMPLETED: "Completed",
    CANCELLED: "Cancelled",
    NO_SHOW: "No Show"
  };
  var INVOICE_STATUS = {
    DRAFT: "Draft",
    SUBMITTED: "Submitted",
    PAID: "Paid",
    PARTIALLY_PAID: "Partially Paid",
    OVERDUE: "Overdue",
    CANCELLED: "Cancelled"
  };
  var MACHINE_STATUS = {
    AVAILABLE: "Available",
    IN_USE: "In Use",
    MAINTENANCE: "Under Maintenance",
    OUT_OF_SERVICE: "Out of Service",
    RESERVED: "Reserved"
  };
  var STATUS_COLORS = {
    Active: "green",
    Inactive: "orange",
    Deceased: "red",
    Transferred: "blue",
    Scheduled: "blue",
    "In Progress": "orange",
    Completed: "green",
    Cancelled: "red",
    Interrupted: "red",
    Confirmed: "cyan",
    "Checked In": "purple",
    "No Show": "darkgray",
    Draft: "gray",
    Submitted: "blue",
    Paid: "green",
    "Partially Paid": "orange",
    Overdue: "red",
    Available: "green",
    "In Use": "orange",
    "Under Maintenance": "yellow",
    "Out of Service": "red",
    Reserved: "blue"
  };
  var VITALS_RANGES = {
    systolic_bp: { min: 90, max: 140, unit: "mmHg", label: "Systolic BP" },
    diastolic_bp: { min: 60, max: 90, unit: "mmHg", label: "Diastolic BP" },
    heart_rate: { min: 60, max: 100, unit: "bpm", label: "Heart Rate" },
    temperature: { min: 36.1, max: 37.2, unit: "\xB0C", label: "Temperature" },
    weight: { min: 0, max: 300, unit: "kg", label: "Weight" }
  };
  var API_ENDPOINTS = {
    PATIENT: {
      LIST: "dialysis_center.api.patient.get_patient_list",
      DETAILS: "dialysis_center.api.patient.get_patient_details",
      DASHBOARD: "dialysis_center.api.patient.get_patient_dashboard",
      VITAL_TRENDS: "dialysis_center.api.patient.get_patient_vital_trends",
      SEARCH: "dialysis_center.api.patient.search_patients"
    },
    SESSION: {
      LIST: "dialysis_center.api.session.get_session_list",
      DETAILS: "dialysis_center.api.session.get_session_details",
      ACTIVE: "dialysis_center.api.session.get_active_sessions",
      STATISTICS: "dialysis_center.api.session.get_session_statistics",
      VITAL_HISTORY: "dialysis_center.api.session.get_session_vital_history",
      ADD_VITAL: "dialysis_center.api.session.add_vital_reading"
    },
    APPOINTMENT: {
      LIST: "dialysis_center.api.appointment.get_appointment_list",
      DAILY_SCHEDULE: "dialysis_center.api.appointment.get_daily_schedule",
      AVAILABLE_SLOTS: "dialysis_center.api.appointment.get_available_slots"
    },
    BILLING: {
      REVENUE_SUMMARY: "dialysis_center.api.billing.get_revenue_summary",
      OUTSTANDING: "dialysis_center.api.billing.get_outstanding_invoices"
    }
  };

  // ../dialysis_center/dialysis_center/public/src/utils/formatters.js
  var formatters_exports = {};
  __export(formatters_exports, {
    formatBloodPressure: () => formatBloodPressure,
    formatCurrency: () => formatCurrency,
    formatDate: () => formatDate,
    formatDateTime: () => formatDateTime,
    formatDuration: () => formatDuration,
    formatNumber: () => formatNumber,
    formatPercent: () => formatPercent,
    formatRelativeTime: () => formatRelativeTime,
    formatTemperature: () => formatTemperature,
    formatTime: () => formatTime,
    getInitials: () => getInitials,
    truncateText: () => truncateText
  });
  function formatDate(date, includeTime = false) {
    if (!date)
      return "";
    const dateObj = typeof date === "string" ? new Date(date) : date;
    if (includeTime) {
      return frappe.datetime.str_to_user(dateObj);
    }
    return frappe.datetime.str_to_user(dateObj.toISOString().split("T")[0]);
  }
  function formatDateTime(datetime) {
    if (!datetime)
      return "";
    return frappe.datetime.str_to_user(datetime);
  }
  function formatTime(datetime) {
    if (!datetime)
      return "";
    const dateObj = typeof datetime === "string" ? new Date(datetime) : datetime;
    return dateObj.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", hour12: false });
  }
  function formatCurrency(amount, currency = null) {
    if (amount === null || amount === void 0)
      return "";
    const cur = currency || frappe.boot.sysdefaults.currency || "USD";
    return frappe.format(amount, { fieldtype: "Currency", options: cur });
  }
  function formatNumber(number, decimals = 2) {
    if (number === null || number === void 0)
      return "";
    return parseFloat(number).toFixed(decimals);
  }
  function formatPercent(value, decimals = 1) {
    if (value === null || value === void 0)
      return "";
    return `${parseFloat(value).toFixed(decimals)}%`;
  }
  function formatDuration(minutes) {
    if (!minutes)
      return "0m";
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours === 0)
      return `${mins}m`;
    if (mins === 0)
      return `${hours}h`;
    return `${hours}h ${mins}m`;
  }
  function formatBloodPressure(systolic, diastolic) {
    if (!systolic || !diastolic)
      return "";
    return `${systolic}/${diastolic} mmHg`;
  }
  function formatTemperature(temp, unit = "C") {
    if (temp === null || temp === void 0)
      return "";
    return `${formatNumber(temp, 1)}\xB0${unit}`;
  }
  function getInitials(name) {
    if (!name)
      return "";
    const parts = name.trim().split(" ");
    if (parts.length === 1)
      return parts[0].charAt(0).toUpperCase();
    return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
  }
  function formatRelativeTime(date) {
    if (!date)
      return "";
    return frappe.datetime.comment_when(date);
  }
  function truncateText(text, maxLength = 50) {
    if (!text)
      return "";
    if (text.length <= maxLength)
      return text;
    return text.substring(0, maxLength) + "...";
  }

  // ../dialysis_center/dialysis_center/public/src/utils/validators.js
  var validators_exports = {};
  __export(validators_exports, {
    validateForm: () => validateForm,
    validators: () => validators
  });
  var validators = {
    email: (value) => {
      if (!value)
        return { valid: true };
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return {
        valid: emailPattern.test(value),
        message: "Please enter a valid email address"
      };
    },
    phone: (value) => {
      if (!value)
        return { valid: true };
      const phonePattern = /^[\d\s\-\+\(\)]+$/;
      const isValid = phonePattern.test(value) && value.replace(/\D/g, "").length >= 10;
      return {
        valid: isValid,
        message: "Please enter a valid phone number (min 10 digits)"
      };
    },
    required: (value, fieldName = "This field") => {
      const isValid = value !== null && value !== void 0 && value !== "";
      return {
        valid: isValid,
        message: `${fieldName} is required`
      };
    },
    notFutureDate: (value) => {
      if (!value)
        return { valid: true };
      const inputDate = new Date(value);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return {
        valid: inputDate <= today,
        message: "Date cannot be in the future"
      };
    },
    futureDate: (value) => {
      if (!value)
        return { valid: true };
      const inputDate = new Date(value);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return {
        valid: inputDate >= today,
        message: "Date must be in the future"
      };
    },
    ageRange: (dob, minAge = 18, maxAge = 100) => {
      if (!dob)
        return { valid: true };
      const birthDate = new Date(dob);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      if (monthDiff < 0 || monthDiff === 0 && today.getDate() < birthDate.getDate()) {
        age--;
      }
      const isValid = age >= minAge && age <= maxAge;
      return {
        valid: isValid,
        message: `Age must be between ${minAge} and ${maxAge} years`
      };
    },
    numberRange: (value, min, max, fieldName = "Value") => {
      if (value === null || value === void 0)
        return { valid: true };
      const num = parseFloat(value);
      const isValid = !isNaN(num) && num >= min && num <= max;
      return {
        valid: isValid,
        message: `${fieldName} must be between ${min} and ${max}`
      };
    },
    bloodPressure: (systolic, diastolic) => {
      const sysValid = validators.numberRange(systolic, 70, 200, "Systolic BP");
      const diaValid = validators.numberRange(diastolic, 40, 130, "Diastolic BP");
      if (!sysValid.valid)
        return sysValid;
      if (!diaValid.valid)
        return diaValid;
      if (systolic && diastolic && parseInt(systolic) <= parseInt(diastolic)) {
        return {
          valid: false,
          message: "Systolic BP must be greater than Diastolic BP"
        };
      }
      return { valid: true };
    },
    vitals: (vitalName, value) => {
      const ranges = {
        systolic_bp: { min: 90, max: 140 },
        diastolic_bp: { min: 60, max: 90 },
        heart_rate: { min: 60, max: 100 },
        temperature: { min: 36.1, max: 37.2 },
        weight: { min: 30, max: 250 }
      };
      const range = ranges[vitalName];
      if (!range || !value)
        return { valid: true };
      const num = parseFloat(value);
      if (num < range.min || num > range.max) {
        return {
          valid: false,
          message: `Warning: Value outside normal range (${range.min}-${range.max})`,
          warning: true
        };
      }
      return { valid: true };
    }
  };
  function validateForm(fields) {
    const errors = {};
    let isValid = true;
    for (const [fieldName, config] of Object.entries(fields)) {
      const { value, rules } = config;
      for (const rule of rules) {
        const result = rule(value);
        if (!result.valid) {
          errors[fieldName] = result.message;
          isValid = false;
          break;
        }
      }
    }
    return { isValid, errors };
  }

  // ../dialysis_center/dialysis_center/public/src/utils/api-helpers.js
  var api_helpers_exports = {};
  __export(api_helpers_exports, {
    AppointmentAPI: () => AppointmentAPI,
    BillingAPI: () => BillingAPI,
    PatientAPI: () => PatientAPI,
    SessionAPI: () => SessionAPI,
    hideLoading: () => hideLoading,
    showError: () => showError,
    showLoading: () => showLoading,
    showSuccess: () => showSuccess
  });
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
          console.error("API Error:", err);
          frappe.msgprint({
            title: __("Error"),
            message: __("An error occurred while fetching data"),
            indicator: "red"
          });
          reject(err);
        }
      });
    });
  }
  var PatientAPI = {
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
  var SessionAPI = {
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
  var AppointmentAPI = {
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
  var BillingAPI = {
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
  function showLoading(message = "Loading...") {
    frappe.freeze(message);
  }
  function hideLoading() {
    frappe.unfreeze();
  }
  function showSuccess(message) {
    frappe.show_alert({
      message: __(message),
      indicator: "green"
    }, 3);
  }
  function showError(message) {
    frappe.msgprint({
      title: __("Error"),
      message: __(message),
      indicator: "red"
    });
  }

  // ../dialysis_center/dialysis_center/public/src/utils.bundle.js
  window.DialysisCenter = {
    constants: constants_exports,
    formatters: formatters_exports,
    validators: validators_exports,
    api: api_helpers_exports
  };
  console.log("\u2705 Dialysis Center utilities loaded");
})();
//# sourceMappingURL=utils.bundle.Q7PDV4Q5.js.map
