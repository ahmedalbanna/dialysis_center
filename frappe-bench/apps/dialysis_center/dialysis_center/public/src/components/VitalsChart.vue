<template>
	<div class="vitals-chart">
		<div class="chart-header">
			<h4>{{ title }}</h4>
			<div class="chart-controls">
				<select v-model="selectedVital" @change="updateChart" class="form-control">
					<option value="blood_pressure">Blood Pressure</option>
					<option value="heart_rate">Heart Rate</option>
					<option value="temperature">Temperature</option>
					<option value="weight">Weight</option>
				</select>
			</div>
		</div>
		<div class="chart-container">
			<canvas ref="chartCanvas"></canvas>
		</div>
	</div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

export default {
	name: 'VitalsChart',
	props: {
		data: {
			type: Array,
			required: true
		},
		title: {
			type: String,
			default: 'Vital Signs Trends'
		}
	},
	setup(props) {
		const chartCanvas = ref(null);
		const selectedVital = ref('blood_pressure');
		let chartInstance = null;
		
		const createChart = () => {
			if (!chartCanvas.value) return;
			
			const ctx = chartCanvas.value.getContext('2d');
			
			// Destroy existing chart
			if (chartInstance) {
				chartInstance.destroy();
			}
			
			// Prepare data based on selected vital
			const labels = props.data.map(d => new Date(d.recorded_at).toLocaleTimeString('en-US', { 
				hour: '2-digit', 
				minute: '2-digit' 
			}));
			
			let datasets = [];
			
			if (selectedVital.value === 'blood_pressure') {
				datasets = [
					{
						label: 'Systolic',
						data: props.data.map(d => d.systolic_bp),
						borderColor: '#ef4444',
						backgroundColor: 'rgba(239, 68, 68, 0.1)',
						tension: 0.4
					},
					{
						label: 'Diastolic',
						data: props.data.map(d => d.diastolic_bp),
						borderColor: '#3b82f6',
						backgroundColor: 'rgba(59, 130, 246, 0.1)',
						tension: 0.4
					}
				];
			} else if (selectedVital.value === 'heart_rate') {
				datasets = [{
					label: 'Heart Rate (bpm)',
					data: props.data.map(d => d.heart_rate),
					borderColor: '#f59e0b',
					backgroundColor: 'rgba(245, 158, 11, 0.1)',
					tension: 0.4
				}];
			} else if (selectedVital.value === 'temperature') {
				datasets = [{
					label: 'Temperature (°C)',
					data: props.data.map(d => d.temperature),
					borderColor: '#10b981',
					backgroundColor: 'rgba(16, 185, 129, 0.1)',
					tension: 0.4
				}];
			} else if (selectedVital.value === 'weight') {
				datasets = [{
					label: 'Weight (kg)',
					data: props.data.map(d => d.weight),
					borderColor: '#8b5cf6',
					backgroundColor: 'rgba(139, 92, 246, 0.1)',
					tension: 0.4
				}];
			}
			
			chartInstance = new Chart(ctx, {
				type: 'line',
				data: {
					labels,
					datasets
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					plugins: {
						legend: {
							display: true,
							position: 'top'
						},
						tooltip: {
							mode: 'index',
							intersect: false
						}
					},
					scales: {
						y: {
							beginAtZero: false,
							grid: {
								color: '#f0f3f7'
							}
						},
						x: {
							grid: {
								display: false
							}
						}
					}
				}
			});
		};
		
		const updateChart = () => {
			createChart();
		};
		
		onMounted(() => {
			createChart();
		});
		
		watch(() => props.data, () => {
			createChart();
		}, { deep: true });
		
		return {
			chartCanvas,
			selectedVital,
			updateChart
		};
	}
};
</script>

<style scoped>
.vitals-chart {
	background: white;
	border: 1px solid #e0e6ed;
	border-radius: 8px;
	padding: 20px;
}

.chart-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 20px;
}

.chart-header h4 {
	margin: 0;
	font-size: 18px;
	font-weight: 600;
	color: #2c3e50;
}

.chart-controls select {
	padding: 6px 12px;
	font-size: 14px;
	border: 1px solid #d1d5db;
	border-radius: 6px;
}

.chart-container {
	height: 300px;
	position: relative;
}
</style>
