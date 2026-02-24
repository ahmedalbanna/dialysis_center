/**
 * Dialysis Center - Analytics Dashboard
 * Charts and KPIs for operational insights
 */

import { SessionAPI, BillingAPI, showError } from '../utils/api-helpers.js';
import { formatCurrency, formatNumber } from '../utils/formatters.js';
import Chart from 'chart.js/auto';

class AnalyticsDashboard {
	constructor(wrapper) {
		this.wrapper = wrapper;
		this.charts = {};
		this.init();
	}

	init() {
		this.setupHTML();
		this.loadData();
	}

	setupHTML() {
		this.wrapper.innerHTML = `
			<div class="analytics-dashboard">
				<div class="dashboard-header">
					<h2>Analytics Dashboard</h2>
					<div class="date-range">
						<input type="date" class="form-control" id="start-date" />
						<span>to</span>
						<input type="date" class="form-control" id="end-date" />
						<button class="btn btn-primary btn-sm" onclick="analyticsDashboard.filterByDate()">
							Apply
						</button>
					</div>
				</div>
				
				<div class="kpi-grid">
					<div class="stat-card stat-card-blue">
						<div class="stat-icon">📊</div>
						<div class="stat-content">
							<div class="stat-label">Total Sessions</div>
							<div class="stat-value" id="kpi-sessions">-</div>
						</div>
					</div>
					<div class="stat-card stat-card-green">
						<div class="stat-icon">💰</div>
						<div class="stat-content">
							<div class="stat-label">Revenue</div>
							<div class="stat-value" id="kpi-revenue">-</div>
						</div>
					</div>
					<div class="stat-card stat-card-orange">
						<div class="stat-icon">👥</div>
						<div class="stat-content">
							<div class="stat-label">Active Patients</div>
							<div class="stat-value" id="kpi-patients">-</div>
						</div>
					</div>
					<div class="stat-card stat-card-purple">
						<div class="stat-icon">⚙️</div>
						<div class="stat-content">
							<div class="stat-label">Machine Utilization</div>
							<div class="stat-value" id="kpi-utilization">-</div>
						</div>
					</div>
				</div>
				
				<div class="charts-grid">
					<div class="chart-card">
						<h4>Sessions by Day</h4>
						<canvas id="sessions-chart"></canvas>
					</div>
					<div class="chart-card">
						<h4>Revenue Trend</h4>
						<canvas id="revenue-chart"></canvas>
					</div>
					<div class="chart-card">
						<h4>Session Status Distribution</h4>
						<canvas id="status-chart"></canvas>
					</div>
					<div class="chart-card">
						<h4>Top Performing Machines</h4>
						<canvas id="machines-chart"></canvas>
					</div>
				</div>
			</div>
		`;

		// Set default date range (last 30 days)
		const endDate = new Date();
		const startDate = new Date();
		startDate.setDate(startDate.getDate() - 30);
		
		document.getElementById('start-date').value = startDate.toISOString().split('T')[0];
		document.getElementById('end-date').value = endDate.toISOString().split('T')[0];
	}

	async loadData() {
		try {
			const startDate = document.getElementById('start-date').value;
			const endDate = document.getElementById('end-date').value;

			// Load session statistics
			const sessionStats = await SessionAPI.getStatistics({
				start_date: startDate,
				end_date: endDate
			});

			// Load revenue data
			const revenueData = await BillingAPI.getRevenueSummary(startDate, endDate);

			this.updateKPIs(sessionStats, revenueData);
			this.renderCharts(sessionStats, revenueData);
		} catch (error) {
			showError('Failed to load analytics data');
		}
	}

	updateKPIs(sessionStats, revenueData) {
		document.getElementById('kpi-sessions').textContent = formatNumber(sessionStats.total_sessions || 0, 0);
		document.getElementById('kpi-revenue').textContent = formatCurrency(revenueData.total_revenue || 0);
		document.getElementById('kpi-patients').textContent = formatNumber(sessionStats.active_patients || 0, 0);
		document.getElementById('kpi-utilization').textContent = formatNumber(sessionStats.machine_utilization || 0, 1) + '%';
	}

	renderCharts(sessionStats, revenueData) {
		this.renderSessionsChart(sessionStats.sessions_by_day || []);
		this.renderRevenueChart(revenueData.revenue_by_day || []);
		this.renderStatusChart(sessionStats.by_status || {});
		this.renderMachinesChart(sessionStats.by_machine || []);
	}

	renderSessionsChart(data) {
		const ctx = document.getElementById('sessions-chart').getContext('2d');
		
		if (this.charts.sessions) {
			this.charts.sessions.destroy();
		}

		this.charts.sessions = new Chart(ctx, {
			type: 'line',
			data: {
				labels: data.map(d => d.date),
				datasets: [{
					label: 'Sessions',
					data: data.map(d => d.count),
					borderColor: '#667eea',
					backgroundColor: 'rgba(102, 126, 234, 0.1)',
					tension: 0.4,
					fill: true
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: { display: false }
				}
			}
		});
	}

	renderRevenueChart(data) {
		const ctx = document.getElementById('revenue-chart').getContext('2d');
		
		if (this.charts.revenue) {
			this.charts.revenue.destroy();
		}

		this.charts.revenue = new Chart(ctx, {
			type: 'bar',
			data: {
				labels: data.map(d => d.date),
				datasets: [{
					label: 'Revenue',
					data: data.map(d => d.amount),
					backgroundColor: '#10b981'
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: { display: false }
				}
			}
		});
	}

	renderStatusChart(data) {
		const ctx = document.getElementById('status-chart').getContext('2d');
		
		if (this.charts.status) {
			this.charts.status.destroy();
		}

		this.charts.status = new Chart(ctx, {
			type: 'doughnut',
			data: {
				labels: Object.keys(data),
				datasets: [{
					data: Object.values(data),
					backgroundColor: ['#667eea', '#10b981', '#f59e0b', '#ef4444']
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false
			}
		});
	}

	renderMachinesChart(data) {
		const ctx = document.getElementById('machines-chart').getContext('2d');
		
		if (this.charts.machines) {
			this.charts.machines.destroy();
		}

		this.charts.machines = new Chart(ctx, {
			type: 'bar',
			data: {
				labels: data.map(d => d.machine),
				datasets: [{
					label: 'Sessions',
					data: data.map(d => d.count),
					backgroundColor: '#8b5cf6'
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				indexAxis: 'y',
				plugins: {
					legend: { display: false }
				}
			}
		});
	}

	filterByDate() {
		this.loadData();
	}

	destroy() {
		Object.values(this.charts).forEach(chart => chart.destroy());
	}
}

// Export for global use
window.AnalyticsDashboard = AnalyticsDashboard;

// Export default for ES6 module compatibility
export default AnalyticsDashboard;
