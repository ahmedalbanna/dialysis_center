/**
 * Dialysis Center - Session Dashboard
 * Real-time monitoring of active dialysis sessions
 */

import { SessionAPI, showError } from '../utils/api-helpers.js';
import { formatDate, formatTime, formatBloodPressure } from '../utils/formatters.js';
import { SESSION_STATUS, STATUS_COLORS } from '../utils/constants.js';

class SessionDashboard {
	constructor(wrapper) {
		this.wrapper = wrapper;
		this.activeSessions = [];
		this.refreshInterval = null;
		this.init();
	}

	init() {
		this.setupHTML();
		this.loadActiveSessions();
		this.setupRealtime();
		this.startAutoRefresh();
	}

	setupHTML() {
		this.wrapper.innerHTML = `
			<div class="session-dashboard">
				<div class="dashboard-header">
					<h2>Active Dialysis Sessions</h2>
					<div class="dashboard-actions">
						<button class="btn btn-primary btn-sm" onclick="sessionDashboard.refresh()">
							🔄 Refresh
						</button>
					</div>
				</div>
				
				<div class="dashboard-stats">
					<div class="stat-card stat-card-blue">
						<div class="stat-icon">🏥</div>
						<div class="stat-content">
							<div class="stat-label">Active Sessions</div>
							<div class="stat-value" id="stat-active">-</div>
						</div>
					</div>
					<div class="stat-card stat-card-green">
						<div class="stat-icon">✅</div>
						<div class="stat-content">
							<div class="stat-label">Completed Today</div>
							<div class="stat-value" id="stat-completed">-</div>
						</div>
					</div>
					<div class="stat-card stat-card-orange">
						<div class="stat-icon">⏰</div>
						<div class="stat-content">
							<div class="stat-label">Scheduled</div>
							<div class="stat-value" id="stat-scheduled">-</div>
						</div>
					</div>
					<div class="stat-card stat-card-red">
						<div class="stat-icon">⚠️</div>
						<div class="stat-content">
							<div class="stat-label">Alerts</div>
							<div class="stat-value" id="stat-alerts">-</div>
						</div>
					</div>
				</div>
				
				<div class="sessions-grid" id="sessions-grid">
					<div class="loading">Loading sessions...</div>
				</div>
			</div>
		`;
	}

	async loadActiveSessions() {
		try {
			const data = await SessionAPI.getActiveSessions();
			this.activeSessions = data.sessions || [];
			this.updateStats(data.statistics || {});
			this.renderSessions();
		} catch (error) {
			showError('Failed to load active sessions');
		}
	}

	updateStats(stats) {
		document.getElementById('stat-active').textContent = stats.active || 0;
		document.getElementById('stat-completed').textContent = stats.completed_today || 0;
		document.getElementById('stat-scheduled').textContent = stats.scheduled || 0;
		document.getElementById('stat-alerts').textContent = stats.alerts || 0;
	}

	renderSessions() {
		const grid = document.getElementById('sessions-grid');
		
		if (this.activeSessions.length === 0) {
			grid.innerHTML = '<div class="empty-state">No active sessions</div>';
			return;
		}

		grid.innerHTML = this.activeSessions.map(session => `
			<div class="session-card session-active" data-session="${session.name}">
				<div class="session-header">
					<div class="session-title">
						<h4>${session.patient_name}</h4>
						<span class="session-id">${session.name}</span>
					</div>
					<span class="indicator-pill ${STATUS_COLORS[session.status]}">${session.status}</span>
				</div>
				
				<div class="session-body">
					<div class="session-info">
						<div class="info-row">
							<span class="icon">🏥</span>
							<span>Machine: ${session.machine || 'Not assigned'}</span>
						</div>
						<div class="info-row">
							<span class="icon">⏰</span>
							<span>${formatTime(session.start_time)} - ${formatTime(session.end_time)}</span>
						</div>
						<div class="info-row">
							<span class="icon">⏱️</span>
							<span>Elapsed: <strong id="elapsed-${session.name}">--:--</strong></span>
						</div>
					</div>
					
					${session.latest_vitals ? `
						<div class="session-vitals">
							<div class="vital-item">
								<span class="vital-label">BP</span>
								<span class="vital-value">${formatBloodPressure(session.latest_vitals.systolic_bp, session.latest_vitals.diastolic_bp)}</span>
							</div>
							<div class="vital-item">
								<span class="vital-label">HR</span>
								<span class="vital-value">${session.latest_vitals.heart_rate} bpm</span>
							</div>
							<div class="vital-item">
								<span class="vital-label">Temp</span>
								<span class="vital-value">${session.latest_vitals.temperature}°C</span>
							</div>
						</div>
					` : ''}
				</div>
				
				<div class="session-footer">
					<button class="btn btn-sm btn-primary" onclick="sessionDashboard.viewSession('${session.name}')">
						View Details
					</button>
					<button class="btn btn-sm btn-success" onclick="sessionDashboard.completeSession('${session.name}')">
						Complete
					</button>
				</div>
			</div>
		`).join('');

		// Start elapsed time counters
		this.updateElapsedTimes();
	}

	updateElapsedTimes() {
		this.activeSessions.forEach(session => {
			const el = document.getElementById(`elapsed-${session.name}`);
			if (el && session.start_time) {
				const start = new Date(session.start_time);
				const now = new Date();
				const elapsed = Math.floor((now - start) / 1000 / 60); // minutes
				const hours = Math.floor(elapsed / 60);
				const mins = elapsed % 60;
				el.textContent = `${hours}:${mins.toString().padStart(2, '0')}`;
			}
		});
	}

	setupRealtime() {
		// Listen for session updates via Socket.IO
		frappe.realtime.on('session_updated', (data) => {
			console.log('Session updated:', data);
			this.refresh();
		});

		frappe.realtime.on('vital_signs_added', (data) => {
			console.log('Vital signs updated:', data);
			this.updateSessionVitals(data.session, data.vitals);
		});
	}

	updateSessionVitals(sessionName, vitals) {
		const session = this.activeSessions.find(s => s.name === sessionName);
		if (session) {
			session.latest_vitals = vitals;
			this.renderSessions();
		}
	}

	startAutoRefresh() {
		// Refresh every 30 seconds
		this.refreshInterval = setInterval(() => {
			this.loadActiveSessions();
		}, 30000);

		// Update elapsed times every second
		setInterval(() => {
			this.updateElapsedTimes();
		}, 1000);
	}

	refresh() {
		this.loadActiveSessions();
		frappe.show_alert({ message: 'Dashboard refreshed', indicator: 'green' }, 2);
	}

	viewSession(sessionName) {
		frappe.set_route('Form', 'Dialysis Session', sessionName);
	}

	completeSession(sessionName) {
		frappe.confirm(
			'Are you sure you want to complete this session?',
			() => {
				frappe.call({
					method: 'dialysis_center.api.session.complete_session',
					args: { session: sessionName },
					callback: (r) => {
						if (r.message) {
							frappe.show_alert({ message: 'Session completed', indicator: 'green' }, 3);
							this.refresh();
						}
					}
				});
			}
		);
	}

	destroy() {
		if (this.refreshInterval) {
			clearInterval(this.refreshInterval);
		}
	}
}

// Export for global use
window.SessionDashboard = SessionDashboard;

// Export default for ES6 module compatibility
export default SessionDashboard;
