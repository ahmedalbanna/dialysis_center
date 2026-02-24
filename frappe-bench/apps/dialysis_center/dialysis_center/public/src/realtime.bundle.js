/**
 * Dialysis Center - Realtime Bundle
 * Exports store and real-time handlers globally
 */

import sessionStore from './store/session-store.js';
import realtimeSessionHandler from './realtime/session-updates.js';
import notificationManager from './realtime/notifications.js';

// Make available globally
window.DialysisCenter = window.DialysisCenter || {};
window.DialysisCenter.store = {
	sessionStore
};
window.DialysisCenter.realtime = {
	sessionHandler: realtimeSessionHandler,
	notifications: notificationManager
};

console.log('✅ Dialysis Center real-time system loaded');
