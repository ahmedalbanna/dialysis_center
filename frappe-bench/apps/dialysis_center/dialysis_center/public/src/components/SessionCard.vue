<template>
	<div class="session-card" :class="statusClass">
		<div class="session-header">
			<div class="session-title">
				<h4>{{ session.patient_name }}</h4>
				<span class="session-id">{{ session.name }}</span>
			</div>
			<span :class="'indicator-pill ' + statusColor">{{ session.status }}</span>
		</div>
		
		<div class="session-body">
			<div class="session-info">
				<div class="info-row">
					<span class="icon">🏥</span>
					<span>Machine: {{ session.machine || 'Not assigned' }}</span>
				</div>
				<div class="info-row" v-if="session.session_date">
					<span class="icon">📅</span>
					<span>{{ formatDate(session.session_date) }}</span>
				</div>
				<div class="info-row" v-if="session.start_time">
					<span class="icon">⏰</span>
					<span>{{ formatTime(session.start_time) }} - {{ formatTime(session.end_time) }}</span>
				</div>
				<div class="info-row" v-if="session.duration">
					<span class="icon">⏱️</span>
					<span>{{ formatDuration(session.duration) }}</span>
				</div>
			</div>
			
			<div class="session-vitals" v-if="showVitals && latestVitals">
				<div class="vital-item">
					<span class="vital-label">BP</span>
					<span class="vital-value">{{ formatBP(latestVitals.systolic_bp, latestVitals.diastolic_bp) }}</span>
				</div>
				<div class="vital-item">
					<span class="vital-label">HR</span>
					<span class="vital-value">{{ latestVitals.heart_rate }} bpm</span>
				</div>
				<div class="vital-item" v-if="latestVitals.temperature">
					<span class="vital-label">Temp</span>
					<span class="vital-value">{{ latestVitals.temperature }}°C</span>
				</div>
			</div>
		</div>
		
		<div class="session-footer" v-if="showActions">
			<button class="btn btn-sm btn-primary" @click="handleAction('view')">
				View Details
			</button>
			<button v-if="session.status === 'In Progress'" class="btn btn-sm btn-success" @click="handleAction('complete')">
				Complete
			</button>
		</div>
	</div>
</template>

<script>
import { computed } from 'vue';
import { formatDate, formatTime, formatDuration, formatBloodPressure } from '../utils/formatters.js';
import { STATUS_COLORS, SESSION_STATUS } from '../utils/constants.js';

export default {
	name: 'SessionCard',
	props: {
		session: {
			type: Object,
			required: true
		},
		showVitals: {
			type: Boolean,
			default: false
		},
		showActions: {
			type: Boolean,
			default: false
		}
	},
	emits: ['action'],
	setup(props, { emit }) {
		const statusColor = computed(() => STATUS_COLORS[props.session.status] || 'gray');
		const statusClass = computed(() => {
			const status = props.session.status;
			if (status === SESSION_STATUS.IN_PROGRESS) return 'session-active';
			if (status === SESSION_STATUS.COMPLETED) return 'session-completed';
			return '';
		});
		
		const latestVitals = computed(() => {
			if (!props.session.vitals || props.session.vitals.length === 0) return null;
			return props.session.vitals[props.session.vitals.length - 1];
		});
		
		const handleAction = (action) => {
			emit('action', { action, session: props.session });
		};
		
		const formatBP = (sys, dia) => formatBloodPressure(sys, dia);
		
		return {
			statusColor,
			statusClass,
			latestVitals,
			handleAction,
			formatDate,
			formatTime,
			formatDuration,
			formatBP
		};
	}
};
</script>

<style scoped>
.session-card {
	background: white;
	border: 1px solid #e0e6ed;
	border-radius: 8px;
	padding: 16px;
	margin-bottom: 12px;
	transition: all 0.3s ease;
}

.session-card.session-active {
	border-left: 4px solid #f59e0b;
	background: linear-gradient(to right, #fffbeb 0%, white 100%);
}

.session-card.session-completed {
	opacity: 0.8;
}

.session-header {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	margin-bottom: 12px;
}

.session-title h4 {
	margin: 0;
	font-size: 16px;
	font-weight: 600;
	color: #2c3e50;
}

.session-id {
	font-size: 12px;
	color: #6c757d;
}

.session-body {
	margin-bottom: 12px;
}

.session-info {
	margin-bottom: 12px;
}

.info-row {
	display: flex;
	align-items: center;
	padding: 6px 0;
	font-size: 14px;
	color: #4b5563;
}

.info-row .icon {
	margin-right: 8px;
	font-size: 16px;
}

.session-vitals {
	display: flex;
	gap: 16px;
	padding: 12px;
	background: #f8f9fa;
	border-radius: 6px;
}

.vital-item {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.vital-label {
	font-size: 11px;
	color: #6c757d;
	margin-bottom: 4px;
}

.vital-value {
	font-size: 14px;
	font-weight: 600;
	color: #2c3e50;
}

.session-footer {
	display: flex;
	gap: 8px;
	padding-top: 12px;
	border-top: 1px solid #f0f3f7;
}

.session-footer button {
	flex: 1;
}
</style>
