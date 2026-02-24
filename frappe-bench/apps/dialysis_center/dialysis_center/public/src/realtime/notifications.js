/**
 * Dialysis Center - Notification System
 * Centralized notification management
 */

class NotificationManager {
	constructor() {
		this.notifications = [];
		this.maxNotifications = 50;
		this.init();
	}

	init() {
		this.loadFromStorage();
		this.requestPermission();
	}

	/**
	 * Add notification
	 */
	add(notification) {
		const notif = {
			id: this.generateId(),
			timestamp: new Date().toISOString(),
			read: false,
			...notification
		};

		this.notifications.unshift(notif);

		// Keep only last N notifications
		if (this.notifications.length > this.maxNotifications) {
			this.notifications = this.notifications.slice(0, this.maxNotifications);
		}

		this.saveToStorage();
		return notif;
	}

	/**
	 * Mark as read
	 */
	markAsRead(notificationId) {
		const notif = this.notifications.find(n => n.id === notificationId);
		if (notif) {
			notif.read = true;
			this.saveToStorage();
		}
	}

	/**
	 * Mark all as read
	 */
	markAllAsRead() {
		this.notifications.forEach(n => n.read = true);
		this.saveToStorage();
	}

	/**
	 * Get unread count
	 */
	getUnreadCount() {
		return this.notifications.filter(n => !n.read).length;
	}

	/**
	 * Get all notifications
	 */
	getAll() {
		return this.notifications;
	}

	/**
	 * Get unread notifications
	 */
	getUnread() {
		return this.notifications.filter(n => !n.read);
	}

	/**
	 * Clear all notifications
	 */
	clear() {
		this.notifications = [];
		this.saveToStorage();
	}

	/**
	 * Save to localStorage
	 */
	saveToStorage() {
		try {
			localStorage.setItem('dialysis_center_notifications', JSON.stringify(this.notifications));
		} catch (error) {
			console.error('Failed to save notifications:', error);
		}
	}

	/**
	 * Load from localStorage
	 */
	loadFromStorage() {
		try {
			const stored = localStorage.getItem('dialysis_center_notifications');
			if (stored) {
				this.notifications = JSON.parse(stored);
			}
		} catch (error) {
			console.error('Failed to load notifications:', error);
		}
	}

	/**
	 * Request browser notification permission
	 */
	async requestPermission() {
		if ('Notification' in window && Notification.permission === 'default') {
			await Notification.requestPermission();
		}
	}

	/**
	 * Show browser notification
	 */
	showBrowserNotification(title, body, icon = null) {
		if ('Notification' in window && Notification.permission === 'granted') {
			new Notification(title, {
				body,
				icon: icon || '/assets/dialysis_center/images/logo.png',
				badge: '/assets/dialysis_center/images/badge.png',
				tag: this.generateId()
			});
		}
	}

	/**
	 * Generate unique ID
	 */
	generateId() {
		return `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
	}
}

// Global singleton
window.notificationManager = new NotificationManager();

export default window.notificationManager;
