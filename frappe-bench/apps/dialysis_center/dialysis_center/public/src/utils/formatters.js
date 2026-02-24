/**
 * Dialysis Center - Formatters Utility
 * Functions for formatting dates, currency, numbers, and other data types
 */

export function formatDate(date, includeTime = false) {
	if (!date) return '';
	const dateObj = typeof date === 'string' ? new Date(date) : date;
	if (includeTime) {
		return frappe.datetime.str_to_user(dateObj);
	}
	return frappe.datetime.str_to_user(dateObj.toISOString().split('T')[0]);
}

export function formatDateTime(datetime) {
	if (!datetime) return '';
	return frappe.datetime.str_to_user(datetime);
}

export function formatTime(datetime) {
	if (!datetime) return '';
	const dateObj = typeof datetime === 'string' ? new Date(datetime) : datetime;
	return dateObj.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
}

export function formatCurrency(amount, currency = null) {
	if (amount === null || amount === undefined) return '';
	const cur = currency || frappe.boot.sysdefaults.currency || 'USD';
	return frappe.format(amount, { fieldtype: 'Currency', options: cur });
}

export function formatNumber(number, decimals = 2) {
	if (number === null || number === undefined) return '';
	return parseFloat(number).toFixed(decimals);
}

export function formatPercent(value, decimals = 1) {
	if (value === null || value === undefined) return '';
	return `${parseFloat(value).toFixed(decimals)}%`;
}

export function formatDuration(minutes) {
	if (!minutes) return '0m';
	const hours = Math.floor(minutes / 60);
	const mins = minutes % 60;
	if (hours === 0) return `${mins}m`;
	if (mins === 0) return `${hours}h`;
	return `${hours}h ${mins}m`;
}

export function formatBloodPressure(systolic, diastolic) {
	if (!systolic || !diastolic) return '';
	return `${systolic}/${diastolic} mmHg`;
}

export function formatTemperature(temp, unit = 'C') {
	if (temp === null || temp === undefined) return '';
	return `${formatNumber(temp, 1)}°${unit}`;
}

export function getInitials(name) {
	if (!name) return '';
	const parts = name.trim().split(' ');
	if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
	return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
}

export function formatRelativeTime(date) {
	if (!date) return '';
	return frappe.datetime.comment_when(date);
}

export function truncateText(text, maxLength = 50) {
	if (!text) return '';
	if (text.length <= maxLength) return text;
	return text.substring(0, maxLength) + '...';
}
