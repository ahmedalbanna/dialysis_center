/**
 * Dialysis Center - Real-time Session Updates
 * Socket.IO handlers for live session monitoring
 */

import sessionStore from '../store/session-store.js';

class RealtimeSessionHandler {
	constructor() {
		this.connected = false;
		this.init();
	}

	/**
	 * Initialize real-time connections
	 */
	init() {
		if (!frappe.realtime) {
			console.warn('Frappe realtime not available');
			return;
		}

		this.setupEventListeners();
		this.connected = true;
		console.log('✅ Real-time session updates enabled');
	}

	/**
	 * Setup Socket.IO event listeners
	 */
	setupEventListeners() {
		// Session created
		frappe.realtime.on('session_created', (data) => {
			console.log('Session created:', data);
			sessionStore.upsert(data.session);
			this.showNotification('New Session', `Session started for ${data.session.patient_name}`);
		});

		// Session updated
		frappe.realtime.on('session_updated', (data) => {
			console.log('Session updated:', data);
			sessionStore.upsert(data.session);
		});

		// Session completed
		frappe.realtime.on('session_completed', (data) => {
			console.log('Session completed:', data);
			sessionStore.upsert(data.session);
			this.showNotification('Session Completed', `Session for ${data.session.patient_name} completed`);
			
			// Remove from active sessions after a delay
			setTimeout(() => {
				sessionStore.remove(data.session.name);
			}, 5000);
		});

		// Vital signs added
		frappe.realtime.on('vital_signs_added', (data) => {
			console.log('Vital signs added:', data);
			sessionStore.updateVitals(data.session, data.vitals);
			this.checkVitalAlerts(data.vitals, data.session);
		});

		// Session event logged
		frappe.realtime.on('session_event_logged', (data) => {
			console.log('Session event:', data);
			
			if (data.event.event_type === 'Complication') {
				this.showNotification(
					'⚠️ Complication Alert',
					`${data.event.description} - Session: ${data.session}`,
					'orange'
				);
			}
		});

		// Machine status changed
		frappe.realtime.on('machine_status_changed', (data) => {
			console.log('Machine status changed:', data);
			
			if (data.status === 'Out of Service') {
				this.showNotification(
					'Machine Alert',
					`Machine ${data.machine} is out of service`,
					'red'
				);
			}
		});

		// Appointment checked in
		frappe.realtime.on('appointment_checked_in', (data) => {
			console.log('Appointment checked in:', data);
			this.showNotification(
				'Patient Checked In',
				`${data.patient_name} checked in`,
				'green'
			);
		});
	}

	/**
	 * Check vital signs for alerts
	 */
	checkVitalAlerts(vitals, sessionName) {
		const alerts = [];

		// Check blood pressure
		if (vitals.systolic_bp > 140 || vitals.systolic_bp < 90) {
			alerts.push(`Abnormal systolic BP: ${vitals.systolic_bp} mmHg`);
		}
		if (vitals.diastolic_bp > 90 || vitals.diastolic_bp < 60) {
			alerts.push(`Abnormal diastolic BP: ${vitals.diastolic_bp} mmHg`);
		}

		// Check heart rate
		if (vitals.heart_rate > 100 || vitals.heart_rate < 60) {
			alerts.push(`Abnormal heart rate: ${vitals.heart_rate} bpm`);
		}

		// Check temperature
		if (vitals.temperature && (vitals.temperature > 37.5 || vitals.temperature < 36.0)) {
			alerts.push(`Abnormal temperature: ${vitals.temperature}°C`);
		}

		// Show alerts if any
		if (alerts.length > 0) {
			this.showNotification(
				'⚠️ Vital Signs Alert',
				alerts.join(', ') + ` - Session: ${sessionName}`,
				'orange'
			);
		}
	}

	/**
	 * Show desktop notification
	 */
	showNotification(title, message, indicator = 'blue') {
		// Frappe toast notification
		frappe.show_alert({
			message: `<strong>${title}</strong><br>${message}`,
			indicator: indicator
		}, 5);

		// Browser notification (if permitted)
		if ('Notification' in window && Notification.permission === 'granted') {
			new Notification(title, {
				body: message,
				icon: '/assets/dialysis_center/images/logo.png',
				badge: '/assets/dialysis_center/images/badge.png'
			});
		}
	}

	/**
	 * Request browser notification permission
	 */
	async requestNotificationPermission() {
		if ('Notification' in window && Notification.permission === 'default') {
			const permission = await Notification.requestPermission();
			return permission === 'granted';
		}
		return false;
	}

	/**
	 * Emit custom event to server
	 */
	emit(event, data) {
		if (frappe.realtime && frappe.realtime.socket) {
			frappe.realtime.socket.emit(event, data);
		}
	}

	/**
	 * Disconnect real-time
	 */
	disconnect() {
		// Socket.IO cleanup would go here
		this.connected = false;
		console.log('Real-time disconnected');
	}
}

// Create global singleton
window.realtimeSessionHandler = new RealtimeSessionHandler();

export default window.realtimeSessionHandler;
