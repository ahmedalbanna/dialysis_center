<template>
	<div v-if="visible" class="alert-banner" :class="typeClass">
		<div class="alert-icon">{{ icon }}</div>
		<div class="alert-content">
			<div class="alert-title" v-if="title">{{ title }}</div>
			<div class="alert-message">{{ message }}</div>
		</div>
		<button v-if="dismissible" class="alert-close" @click="handleClose">×</button>
	</div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
	name: 'AlertBanner',
	props: {
		type: {
			type: String,
			default: 'info',
			validator: (value) => ['info', 'success', 'warning', 'error'].includes(value)
		},
		title: {
			type: String,
			default: ''
		},
		message: {
			type: String,
			required: true
		},
		dismissible: {
			type: Boolean,
			default: true
		}
	},
	emits: ['close'],
	setup(props, { emit }) {
		const visible = ref(true);
		
		const typeClass = computed(() => `alert-${props.type}`);
		
		const icon = computed(() => {
			const icons = {
				info: 'ℹ️',
				success: '✅',
				warning: '⚠️',
				error: '❌'
			};
			return icons[props.type] || icons.info;
		});
		
		const handleClose = () => {
			visible.value = false;
			emit('close');
		};
		
		return {
			visible,
			typeClass,
			icon,
			handleClose
		};
	}
};
</script>

<style scoped>
.alert-banner {
	display: flex;
	align-items: flex-start;
	padding: 16px;
	border-radius: 8px;
	margin-bottom: 16px;
	border-left: 4px solid;
}

.alert-info {
	background: #eff6ff;
	border-color: #3b82f6;
	color: #1e40af;
}

.alert-success {
	background: #f0fdf4;
	border-color: #10b981;
	color: #065f46;
}

.alert-warning {
	background: #fffbeb;
	border-color: #f59e0b;
	color: #92400e;
}

.alert-error {
	background: #fef2f2;
	border-color: #ef4444;
	color: #991b1b;
}

.alert-icon {
	font-size: 20px;
	margin-right: 12px;
}

.alert-content {
	flex: 1;
}

.alert-title {
	font-weight: 600;
	margin-bottom: 4px;
}

.alert-message {
	font-size: 14px;
}

.alert-close {
	background: none;
	border: none;
	font-size: 24px;
	cursor: pointer;
	padding: 0;
	width: 24px;
	height: 24px;
	display: flex;
	align-items: center;
	justify-content: center;
	opacity: 0.6;
	transition: opacity 0.2s;
}

.alert-close:hover {
	opacity: 1;
}
</style>
