/**
 * Dialysis Center - Utils Bundle
 * Exports all utility functions globally for use in form scripts
 */

import * as constants from './utils/constants.js';
import * as formatters from './utils/formatters.js';
import * as validators from './utils/validators.js';
import * as apiHelpers from './utils/api-helpers.js';

// Make utilities available globally
window.DialysisCenter = {
	constants,
	formatters,
	validators,
	api: apiHelpers
};

console.log('✅ Dialysis Center utilities loaded');
