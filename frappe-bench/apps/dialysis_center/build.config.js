#!/usr/bin/env node

/**
 * Dialysis Center - esbuild Configuration
 * Builds Vue 3 components and bundles for Frappe integration
 */

const esbuild = require('esbuild');
const vue = require('esbuild-vue');
const path = require('path');
const fs = require('fs');

const isWatch = process.argv.includes('--watch');
const isProduction = process.argv.includes('--production');

const publicPath = path.resolve(__dirname, 'dialysis_center/public');
const srcPath = path.join(publicPath, 'src');
const distPath = path.join(publicPath, 'dist');

// Ensure dist directories exist
if (!fs.existsSync(distPath)) {
	fs.mkdirSync(distPath, { recursive: true });
}
if (!fs.existsSync(path.join(distPath, 'js'))) {
	fs.mkdirSync(path.join(distPath, 'js'), { recursive: true });
}
if (!fs.existsSync(path.join(distPath, 'css'))) {
	fs.mkdirSync(path.join(distPath, 'css'), { recursive: true });
}

// Build configuration
const buildOptions = {
	entryPoints: [
		path.join(srcPath, 'components.bundle.js'),
		path.join(srcPath, 'dashboard.bundle.js'),
		path.join(srcPath, 'utils.bundle.js'),
	],
	bundle: true,
	outdir: path.join(distPath, 'js'),
	format: 'iife',
	target: 'es2020',
	minify: isProduction,
	sourcemap: !isProduction,
	plugins: [vue()],
	loader: {
		'.vue': 'js',
		'.scss': 'css',
		'.css': 'css',
	},
	external: ['frappe', 'frappe.ui', 'frappe.call'],
	define: {
		'process.env.NODE_ENV': isProduction ? '"production"' : '"development"',
	},
};

async function build() {
	try {
		if (isWatch) {
			console.log('👀 Watching for changes...');
			const ctx = await esbuild.context(buildOptions);
			await ctx.watch();
		} else {
			console.log('🔨 Building Dialysis Center frontend...');
			await esbuild.build(buildOptions);
			console.log('✅ Build complete!');
		}
	} catch (error) {
		console.error('❌ Build failed:', error);
		process.exit(1);
	}
}

build();
