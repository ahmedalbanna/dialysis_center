<template>
	<div class="stat-card" :class="colorClass">
		<div class="stat-icon">
			<span>{{ icon }}</span>
		</div>
		<div class="stat-content">
			<div class="stat-label">{{ label }}</div>
			<div class="stat-value">{{ formattedValue }}</div>
			<div class="stat-change" v-if="change" :class="changeClass">
				<span>{{ changeIcon }}</span>
				<span>{{ Math.abs(change) }}% from last period</span>
			</div>
		</div>
	</div>
</template>

<script>
import { computed } from 'vue';
import { formatNumber, formatCurrency } from '../utils/formatters.js';

export default {
	name: 'StatCard',
	props: {
		label: {
			type: String,
			required: true
		},
		value: {
			type: [Number, String],
			required: true
		},
		icon: {
			type: String,
			default: '📊'
		},
		color: {
			type: String,
			default: 'blue',
			validator: (value) => ['blue', 'green', 'orange', 'red', 'purple'].includes(value)
		},
		format: {
			type: String,
			default: 'number',
			validator: (value) => ['number', 'currency', 'text'].includes(value)
		},
		change: {
			type: Number,
			default: null
		}
	},
	setup(props) {
		const colorClass = computed(() => `stat-card-${props.color}`);
		
		const formattedValue = computed(() => {
			if (props.format === 'currency') {
				return formatCurrency(props.value);
			} else if (props.format === 'number') {
				return formatNumber(props.value, 0);
			}
			return props.value;
		});
		
		const changeClass = computed(() => {
			if (!props.change) return '';
			return props.change > 0 ? 'stat-increase' : 'stat-decrease';
		});
		
		const changeIcon = computed(() => {
			if (!props.change) return '';
			return props.change > 0 ? '↑' : '↓';
		});
		
		return {
			colorClass,
			formattedValue,
			changeClass,
			changeIcon
		};
	}
};
</script>

<style scoped>
.stat-card {
	background: white;
	border-radius: 8px;
	padding: 20px;
	display: flex;
	align-items: center;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	transition: transform 0.2s ease;
}

.stat-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stat-icon {
	width: 56px;
	height: 56px;
	border-radius: 12px;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 28px;
	margin-right: 16px;
}

.stat-card-blue .stat-icon {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card-green .stat-icon {
	background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-card-orange .stat-icon {
	background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-card-red .stat-icon {
	background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.stat-card-purple .stat-icon {
	background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.stat-content {
	flex: 1;
}

.stat-label {
	font-size: 14px;
	color: #6c757d;
	margin-bottom: 4px;
}

.stat-value {
	font-size: 28px;
	font-weight: bold;
	color: #2c3e50;
	margin-bottom: 4px;
}

.stat-change {
	font-size: 12px;
	display: flex;
	align-items: center;
	gap: 4px;
}

.stat-increase {
	color: #10b981;
}

.stat-decrease {
	color: #ef4444;
}
</style>
