/**
 * Dialysis Center - Components Bundle
 * Registers all Vue 3 components globally for use in Frappe forms and pages
 */

import { createApp } from 'vue';
import PatientCard from './components/PatientCard.vue';
import SessionCard from './components/SessionCard.vue';
import VitalsChart from './components/VitalsChart.vue';
import StatCard from './components/StatCard.vue';
import AlertBanner from './components/AlertBanner.vue';

// Global component registry
window.DialysisCenterComponents = {
	PatientCard,
	SessionCard,
	VitalsChart,
	StatCard,
	AlertBanner
};

// Helper function to mount Vue component in Frappe
window.mountVueComponent = function(componentName, props, el) {
	const component = window.DialysisCenterComponents[componentName];
	if (!component) {
		console.error(`Component ${componentName} not found`);
		return;
	}
	
	const app = createApp(component, props);
	app.mount(el);
	return app;
};

console.log('✅ Dialysis Center Vue components loaded');
