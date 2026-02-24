/**
 * Dialysis Center - Session Store
 * Client-side state management for active sessions
 */

class SessionStore {
	constructor() {
		this.sessions = [];
		this.listeners = [];
		this.loadFromCache();
	}

	/**
	 * Get all active sessions
	 */
	getAll() {
		return this.sessions;
	}

	/**
	 * Get session by ID
	 */
	getById(sessionId) {
		return this.sessions.find(s => s.name === sessionId);
	}

	/**
	 * Add or update session
	 */
	upsert(session) {
		const index = this.sessions.findIndex(s => s.name === session.name);
		
		if (index >= 0) {
			this.sessions[index] = { ...this.sessions[index], ...session };
		} else {
			this.sessions.push(session);
		}
		
		this.saveToCache();
		this.notify('session_updated', session);
	}

	/**
	 * Remove session
	 */
	remove(sessionId) {
		const index = this.sessions.findIndex(s => s.name === sessionId);
		
		if (index >= 0) {
			const removed = this.sessions.splice(index, 1)[0];
			this.saveToCache();
			this.notify('session_removed', removed);
		}
	}

	/**
	 * Update session vitals
	 */
	updateVitals(sessionId, vitals) {
		const session = this.getById(sessionId);
		
		if (session) {
			if (!session.vitals) {
				session.vitals = [];
			}
			session.vitals.push(vitals);
			session.latest_vitals = vitals;
			
			this.saveToCache();
			this.notify('vitals_updated', { session: sessionId, vitals });
		}
	}

	/**
	 * Clear all sessions
	 */
	clear() {
		this.sessions = [];
		this.saveToCache();
		this.notify('sessions_cleared');
	}

	/**
	 * Subscribe to store changes
	 */
	subscribe(callback) {
		this.listeners.push(callback);
		
		// Return unsubscribe function
		return () => {
			const index = this.listeners.indexOf(callback);
			if (index >= 0) {
				this.listeners.splice(index, 1);
			}
		};
	}

	/**
	 * Notify all listeners
	 */
	notify(event, data) {
		this.listeners.forEach(listener => {
			try {
				listener(event, data);
			} catch (error) {
				console.error('Store listener error:', error);
			}
		});
	}

	/**
	 * Save to localStorage
	 */
	saveToCache() {
		try {
			localStorage.setItem('dialysis_center_sessions', JSON.stringify(this.sessions));
		} catch (error) {
			console.error('Failed to save to cache:', error);
		}
	}

	/**
	 * Load from localStorage
	 */
	loadFromCache() {
		try {
			const cached = localStorage.getItem('dialysis_center_sessions');
			if (cached) {
				this.sessions = JSON.parse(cached);
			}
		} catch (error) {
			console.error('Failed to load from cache:', error);
			this.sessions = [];
		}
	}

	/**
	 * Get sessions by status
	 */
	getByStatus(status) {
		return this.sessions.filter(s => s.status === status);
	}

	/**
	 * Get sessions count
	 */
	getCount() {
		return this.sessions.length;
	}

	/**
	 * Get statistics
	 */
	getStats() {
		return {
			total: this.sessions.length,
			in_progress: this.sessions.filter(s => s.status === 'In Progress').length,
			scheduled: this.sessions.filter(s => s.status === 'Scheduled').length,
			completed: this.sessions.filter(s => s.status === 'Completed').length
		};
	}
}

// Create global singleton instance
window.sessionStore = new SessionStore();

export default window.sessionStore;
