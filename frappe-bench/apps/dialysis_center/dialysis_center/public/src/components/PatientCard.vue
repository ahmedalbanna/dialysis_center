<template>
	<div class="patient-card" :class="{ 'card-clickable': clickable }" @click="handleClick">
		<div class="patient-card-header">
			<div class="patient-avatar">{{ initials }}</div>
			<div class="patient-info">
				<h4 class="patient-name">{{ patient.patient_name || patient.name }}</h4>
				<p class="patient-id">ID: {{ patient.name }}</p>
			</div>
			<div class="patient-status">
				<span :class="'indicator-pill ' + statusColor">{{ patient.status }}</span>
			</div>
		</div>
		
		<div class="patient-card-body">
			<div class="patient-details">
				<div class="detail-item" v-if="patient.age">
					<span class="detail-label">Age:</span>
					<span class="detail-value">{{ patient.age }} years</span>
				</div>
				<div class="detail-item" v-if="patient.blood_type">
					<span class="detail-label">Blood Type:</span>
					<span class="detail-value">{{ patient.blood_type }}</span>
				</div>
				<div class="detail-item" v-if="patient.phone">
					<span class="detail-label">Phone:</span>
					<span class="detail-value">{{ patient.phone }}</span>
				</div>
				<div class="detail-item" v-if="patient.email">
					<span class="detail-label">Email:</span>
					<span class="detail-value">{{ truncate(patient.email, 30) }}</span>
				</div>
			</div>
			
			<div class="patient-stats" v-if="showStats && stats">
				<div class="stat-item">
					<div class="stat-value">{{ stats.total_sessions || 0 }}</div>
					<div class="stat-label">Total Sessions</div>
				</div>
				<div class="stat-item">
					<div class="stat-value">{{ stats.upcoming_appointments || 0 }}</div>
					<div class="stat-label">Upcoming</div>
				</div>
				<div class="stat-item">
					<div class="stat-value">{{ formatCurrency(stats.outstanding || 0) }}</div>
					<div class="stat-label">Outstanding</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { computed } from 'vue';
import { getInitials, truncateText, formatCurrency } from '../utils/formatters.js';
import { STATUS_COLORS } from '../utils/constants.js';

export default {
	name: 'PatientCard',
	props: {
		patient: {
			type: Object,
			required: true
		},
		showStats: {
			type: Boolean,
			default: false
		},
		stats: {
			type: Object,
			default: null
		},
		clickable: {
			type: Boolean,
			default: false
		}
	},
	emits: ['click'],
	setup(props, { emit }) {
		const initials = computed(() => getInitials(props.patient.patient_name || props.patient.name));
		const statusColor = computed(() => STATUS_COLORS[props.patient.status] || 'gray');
		
		const handleClick = () => {
			if (props.clickable) {
				emit('click', props.patient);
			}
		};
		
		const truncate = (text, length) => truncateText(text, length);
		
		return {
			initials,
			statusColor,
			handleClick,
			truncate,
			formatCurrency
		};
	}
};
</script>

<style scoped>
.patient-card {
	background: white;
	border: 1px solid #e0e6ed;
	border-radius: 8px;
	padding: 16px;
	margin-bottom: 16px;
	transition: all 0.3s ease;
}

.patient-card.card-clickable {
	cursor: pointer;
}

.patient-card.card-clickable:hover {
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	transform: translateY(-2px);
}

.patient-card-header {
	display: flex;
	align-items: center;
	margin-bottom: 12px;
}

.patient-avatar {
	width: 48px;
	height: 48px;
	border-radius: 50%;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 18px;
	font-weight: bold;
	margin-right: 12px;
}

.patient-info {
	flex: 1;
}

.patient-name {
	margin: 0;
	font-size: 16px;
	font-weight: 600;
	color: #2c3e50;
}

.patient-id {
	margin: 4px 0 0;
	font-size: 13px;
	color: #6c757d;
}

.patient-card-body {
	border-top: 1px solid #f0f3f7;
	padding-top: 12px;
}

.patient-details {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 8px;
	margin-bottom: 12px;
}

.detail-item {
	font-size: 13px;
}

.detail-label {
	color: #6c757d;
	margin-right: 4px;
}

.detail-value {
	color: #2c3e50;
	font-weight: 500;
}

.patient-stats {
	display: flex;
	justify-content: space-around;
	background: #f8f9fa;
	border-radius: 6px;
	padding: 12px;
	margin-top: 12px;
}

.stat-item {
	text-align: center;
}

.stat-value {
	font-size: 20px;
	font-weight: bold;
	color: #667eea;
}

.stat-label {
	font-size: 11px;
	color: #6c757d;
	margin-top: 4px;
}

@media (max-width: 768px) {
	.patient-details {
		grid-template-columns: 1fr;
	}
}
</style>
