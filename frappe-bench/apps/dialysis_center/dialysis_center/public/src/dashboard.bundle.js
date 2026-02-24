/**
 * Dialysis Center - Dashboard Bundle
 * Exports dashboard classes globally
 */

import SessionDashboard from './pages/SessionDashboard.js';
import AnalyticsDashboard from './pages/AnalyticsDashboard.js';

// Make available globally
window.SessionDashboard = SessionDashboard;
window.AnalyticsDashboard = AnalyticsDashboard;

console.log('✅ Dialysis Center dashboards loaded');

// Export as default for bundler
export default {
	SessionDashboard,
	AnalyticsDashboard
};
