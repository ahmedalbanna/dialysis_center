/**
 * Dialysis Center - Validators Utility
 * Client-side validation functions for forms
 */

export const validators = {
	/**
	 * Validate email format
	 */
	email: (value) => {
		if (!value) return { valid: true };
		const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		return {
			valid: emailPattern.test(value),
			message: 'Please enter a valid email address'
		};
	},

	/**
	 * Validate phone number
	 */
	phone: (value) => {
		if (!value) return { valid: true };
		const phonePattern = /^[\d\s\-\+\(\)]+$/;
		const isValid = phonePattern.test(value) && value.replace(/\D/g, '').length >= 10;
		return {
			valid: isValid,
			message: 'Please enter a valid phone number (min 10 digits)'
		};
	},

	/**
	 * Validate required field
	 */
	required: (value, fieldName = 'This field') => {
		const isValid = value !== null && value !== undefined && value !== '';
		return {
			valid: isValid,
			message: `${fieldName} is required`
		};
	},

	/**
	 * Validate date is not in future
	 */
	notFutureDate: (value) => {
		if (!value) return { valid: true };
		const inputDate = new Date(value);
		const today = new Date();
		today.setHours(0, 0, 0, 0);
		return {
			valid: inputDate <= today,
			message: 'Date cannot be in the future'
		};
	},

	/**
	 * Validate date is in future
	 */
	futureDate: (value) => {
		if (!value) return { valid: true };
		const inputDate = new Date(value);
		const today = new Date();
		today.setHours(0, 0, 0, 0);
		return {
			valid: inputDate >= today,
			message: 'Date must be in the future'
		};
	},

	/**
	 * Validate age range
	 */
	ageRange: (dob, minAge = 18, maxAge = 100) => {
		if (!dob) return { valid: true };
		const birthDate = new Date(dob);
		const today = new Date();
		let age = today.getFullYear() - birthDate.getFullYear();
		const monthDiff = today.getMonth() - birthDate.getMonth();
		if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
			age--;
		}
		const isValid = age >= minAge && age <= maxAge;
		return {
			valid: isValid,
			message: `Age must be between ${minAge} and ${maxAge} years`
		};
	},

	/**
	 * Validate number range
	 */
	numberRange: (value, min, max, fieldName = 'Value') => {
		if (value === null || value === undefined) return { valid: true };
		const num = parseFloat(value);
		const isValid = !isNaN(num) && num >= min && num <= max;
		return {
			valid: isValid,
			message: `${fieldName} must be between ${min} and ${max}`
		};
	},

	/**
	 * Validate blood pressure
	 */
	bloodPressure: (systolic, diastolic) => {
		const sysValid = validators.numberRange(systolic, 70, 200, 'Systolic BP');
		const diaValid = validators.numberRange(diastolic, 40, 130, 'Diastolic BP');
		
		if (!sysValid.valid) return sysValid;
		if (!diaValid.valid) return diaValid;
		
		if (systolic && diastolic && parseInt(systolic) <= parseInt(diastolic)) {
			return {
				valid: false,
				message: 'Systolic BP must be greater than Diastolic BP'
			};
		}
		
		return { valid: true };
	},

	/**
	 * Validate vital signs are within normal ranges
	 */
	vitals: (vitalName, value) => {
		const ranges = {
			systolic_bp: { min: 90, max: 140 },
			diastolic_bp: { min: 60, max: 90 },
			heart_rate: { min: 60, max: 100 },
			temperature: { min: 36.1, max: 37.2 },
			weight: { min: 30, max: 250 }
		};
		
		const range = ranges[vitalName];
		if (!range || !value) return { valid: true };
		
		const num = parseFloat(value);
		if (num < range.min || num > range.max) {
			return {
				valid: false,
				message: `Warning: Value outside normal range (${range.min}-${range.max})`,
				warning: true
			};
		}
		
		return { valid: true };
	}
};

/**
 * Validate multiple fields at once
 */
export function validateForm(fields) {
	const errors = {};
	let isValid = true;
	
	for (const [fieldName, config] of Object.entries(fields)) {
		const { value, rules } = config;
		
		for (const rule of rules) {
			const result = rule(value);
			if (!result.valid) {
				errors[fieldName] = result.message;
				isValid = false;
				break;
			}
		}
	}
	
	return { isValid, errors };
}
