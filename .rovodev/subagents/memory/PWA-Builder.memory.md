# PWA Builder Memory File

## Quick Facts
- **Specialty**: Progressive Web Apps on Frappe, service workers, offline functionality, mobile-first UI, app manifests, mobile portal patterns, tab-based navigation, localStorage management, responsive design
- **Primary Tools**: JavaScript service workers, manifest.json, offline storage, responsive CSS
- **Common Tasks**: Service worker setup, offline caching, mobile UI design, push notifications, app installation
- **Estimated Task Time**: 60-180 minutes per PWA feature

---

## PWA Core Components

### 1. Web App Manifest

**File**: `apps/myapp/myapp/public/manifest.json`

```json
{
	"name": "Healthcare Clinic App",
	"short_name": "Clinic",
	"description": "Healthcare clinic management app",
	"start_url": "/app/clinic-portal",
	"display": "standalone",
	"background_color": "#ffffff",
	"theme_color": "#1f2937",
	"orientation": "portrait",
	"scope": "/",
	"icons": [
		{
			"src": "/assets/icon-192.png",
			"sizes": "192x192",
			"type": "image/png",
			"purpose": "any"
		},
		{
			"src": "/assets/icon-512.png",
			"sizes": "512x512",
			"type": "image/png",
			"purpose": "maskable"
		}
	],
	"screenshots": [
		{
			"src": "/assets/screenshot1.png",
			"sizes": "540x720",
			"type": "image/png",
			"form_factor": "narrow"
		}
	],
	"shortcuts": [
		{
			"name": "New Appointment",
			"short_name": "Appointment",
			"url": "/app/appointment/new",
			"icons": [{"src": "/assets/new-appointment.png", "sizes": "192x192"}]
		},
		{
			"name": "My Schedule",
			"short_name": "Schedule",
			"url": "/app/my-appointments",
			"icons": [{"src": "/assets/schedule.png", "sizes": "192x192"}]
		}
	]
}
```

### 2. Service Worker

**File**: `apps/myapp/myapp/public/js/service-worker.js`

```javascript
// Service Worker for offline functionality and caching

const CACHE_NAME = "clinic-app-v1";
const STATIC_ASSETS = [
	"/app/clinic-portal",
	"/assets/offline.html",
	"/app/frappe/desk.bundle.js",
	"/app/frappe/desk.bundle.css"
];

// Install event - cache static assets
self.addEventListener("install", (event) => {
	event.waitUntil(
		caches.open(CACHE_NAME).then((cache) => {
			return cache.addAll(STATIC_ASSETS);
		})
	);
	self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener("activate", (event) => {
	event.waitUntil(
		caches.keys().then((cacheNames) => {
			return Promise.all(
				cacheNames.map((cacheName) => {
					if (cacheName !== CACHE_NAME) {
						return caches.delete(cacheName);
					}
				})
			);
		})
	);
	self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener("fetch", (event) => {
	const { request } = event;
	const url = new URL(request.url);

	// Skip non-GET requests
	if (request.method !== "GET") {
		return;
	}

	// API requests - network first, cache as fallback
	if (url.pathname.startsWith("/api/")) {
		event.respondWith(
			fetch(request)
				.then((response) => {
					// Cache successful API responses
					if (response.ok) {
						const cache = caches.open(CACHE_NAME);
						cache.then((c) => c.put(request, response.clone()));
					}
					return response;
				})
				.catch(() => {
					// Return cached response if network fails
					return caches.match(request);
				})
		);
		return;
	}

	// Static assets - cache first
	event.respondWith(
		caches.match(request).then((response) => {
			return response || fetch(request).then((response) => {
				if (!response || response.status !== 200 || response.type === "error") {
					return response;
				}
				const cache = caches.open(CACHE_NAME);
				cache.then((c) => c.put(request, response.clone()));
				return response;
			});
		})
	);
});

// Message event - handle updates from client
self.addEventListener("message", (event) => {
	if (event.data && event.data.type === "SKIP_WAITING") {
		self.skipWaiting();
	}
});
```

### 3. PWA Registration

**File**: `apps/myapp/myapp/public/js/pwa-register.js`

```javascript
// Register service worker and handle updates

if ("serviceWorker" in navigator) {
	window.addEventListener("load", () => {
		navigator.serviceWorker
			.register("/assets/service-worker.js")
			.then((registration) => {
				console.log("Service Worker registered:", registration);

				// Check for updates periodically
				setInterval(() => {
					registration.update();
				}, 60000); // Check every minute

				// Listen for updates
				registration.addEventListener("updatefound", () => {
					const newWorker = registration.installing;
					newWorker.addEventListener("statechange", () => {
						if (newWorker.state === "activated") {
							// New version available
							show_update_notification();
						}
					});
				});
			})
			.catch((error) => {
				console.error("Service Worker registration failed:", error);
			});
	});

	// Handle skip waiting message
	let refreshing = false;
	navigator.serviceWorker.addEventListener("controllerchange", () => {
		if (refreshing) return;
		refreshing = true;
		window.location.reload();
	});
}

function show_update_notification() {
	frappe.msgprint({
		title: __("Update Available"),
		indicator: "blue",
		message: __("A new version is available. Refresh to update."),
		primary_action: {
			label: __("Refresh"),
			action: () => {
				navigator.serviceWorker.controller.postMessage({
					type: "SKIP_WAITING"
				});
			}
		}
	});
}
```

### 4. Offline Data Storage

**File**: `apps/myapp/myapp/public/js/offline-storage.js`

```javascript
// Manage offline data with localStorage and IndexedDB

class OfflineStorage {
	constructor(dbName = "clinic-app", version = 1) {
		this.dbName = dbName;
		this.version = version;
		this.db = null;
		this.initDB();
	}

	initDB() {
		return new Promise((resolve, reject) => {
			const request = indexedDB.open(this.dbName, this.version);

			request.onerror = () => reject(request.error);
			request.onsuccess = () => {
				this.db = request.result;
				resolve(this.db);
			};

			request.onupgradeneeded = (event) => {
				const db = event.target.result;

				// Create object stores
				if (!db.objectStoreNames.contains("appointments")) {
					db.createObjectStore("appointments", { keyPath: "id" });
				}
				if (!db.objectStoreNames.contains("patients")) {
					db.createObjectStore("patients", { keyPath: "id" });
				}
				if (!db.objectStoreNames.contains("pending_changes")) {
					db.createObjectStore("pending_changes", { keyPath: "id", autoIncrement: true });
				}
			};
		});
	}

	// Save data offline
	saveOffline(storeName, data) {
		return new Promise((resolve, reject) => {
			const transaction = this.db.transaction(storeName, "readwrite");
			const store = transaction.objectStore(storeName);
			const request = store.put(data);

			request.onerror = () => reject(request.error);
			request.onsuccess = () => resolve(request.result);
		});
	}

	// Get data offline
	getOffline(storeName, id) {
		return new Promise((resolve, reject) => {
			const transaction = this.db.transaction(storeName, "readonly");
			const store = transaction.objectStore(storeName);
			const request = store.get(id);

			request.onerror = () => reject(request.error);
			request.onsuccess = () => resolve(request.result);
		});
	}

	// Get all data offline
	getAllOffline(storeName) {
		return new Promise((resolve, reject) => {
			const transaction = this.db.transaction(storeName, "readonly");
			const store = transaction.objectStore(storeName);
			const request = store.getAll();

			request.onerror = () => reject(request.error);
			request.onsuccess = () => resolve(request.result);
		});
	}

	// Queue change for sync when online
	queueChange(action, doctype, docname, data) {
		return this.saveOffline("pending_changes", {
			action,
			doctype,
			docname,
			data,
			timestamp: Date.now(),
			synced: false
		});
	}

	// Sync pending changes
	async syncPendingChanges() {
		const changes = await this.getAllOffline("pending_changes");

		for (const change of changes) {
			if (change.synced) continue;

			try {
				if (change.action === "create") {
					await frappe.call({
						method: "frappe.client.insert",
						args: { doc: change.data }
					});
				} else if (change.action === "update") {
					await frappe.call({
						method: "frappe.client.set_value",
						args: {
							doctype: change.doctype,
							name: change.docname,
							fieldname: change.data
						}
					});
				}

				// Mark as synced
				change.synced = true;
				await this.saveOffline("pending_changes", change);
			} catch (error) {
				console.error("Sync failed for", change.docname, error);
			}
		}
	}
}

// Initialize global instance
const offlineStorage = new OfflineStorage();

// Listen for online/offline events
window.addEventListener("online", () => {
	console.log("Back online - syncing changes");
	offlineStorage.syncPendingChanges();
});
```

### 5. Mobile-First Responsive UI

**File**: `apps/myapp/myapp/public/css/mobile-first.scss`

```scss
// Mobile-first responsive design

// Variables
$color-primary: #2563eb;
$color-secondary: #1f2937;
$spacing-unit: 0.25rem;
$breakpoint-sm: 640px;
$breakpoint-md: 768px;
$breakpoint-lg: 1024px;

// Base mobile styles
body {
	font-size: 16px;
	line-height: 1.5;
	margin: 0;
	padding: 0;
}

.container {
	padding: $spacing-unit * 4;
	max-width: 100%;
}

// Tab-based navigation (mobile friendly)
.tab-navigation {
	display: flex;
	flex-direction: column;
	gap: $spacing-unit * 2;
	overflow-x: auto;
	-webkit-overflow-scrolling: touch;

	.tab-button {
		padding: $spacing-unit * 3;
		border: none;
		background: $color-secondary;
		color: white;
		border-radius: 4px;
		cursor: pointer;
		font-size: 14px;
		white-space: nowrap;

		&.active {
			background: $color-primary;
		}
	}
}

// Responsive grid
.grid {
	display: grid;
	grid-template-columns: 1fr;
	gap: $spacing-unit * 4;

	@media (min-width: $breakpoint-md) {
		grid-template-columns: repeat(2, 1fr);
	}

	@media (min-width: $breakpoint-lg) {
		grid-template-columns: repeat(3, 1fr);
	}
}

// Card layout (touch-friendly)
.card {
	padding: $spacing-unit * 4;
	border: 1px solid #e5e7eb;
	border-radius: 8px;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	min-height: 100px; // Touch-friendly minimum height

	&:active {
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}
}

// Touch-friendly buttons
button,
.btn {
	min-height: 44px; // iOS recommended touch target
	min-width: 44px;
	padding: $spacing-unit * 2 $spacing-unit * 4;
	font-size: 16px;
	border-radius: 4px;
	border: none;
	cursor: pointer;
	transition: all 0.2s ease;

	&:active {
		opacity: 0.8;
		transform: scale(0.98);
	}
}

// Safe area for notches
@supports (padding: max(0px)) {
	.safe-area {
		padding-top: max(1rem, env(safe-area-inset-top));
		padding-bottom: max(1rem, env(safe-area-inset-bottom));
		padding-left: max(1rem, env(safe-area-inset-left));
		padding-right: max(1rem, env(safe-area-inset-right));
	}
}
```

---

## PWA Registration in Hooks

**File**: `apps/myapp/myapp/hooks.py`

```python
app_include_js = [
	"libs.bundle.js",
	"desk.bundle.js",
	"pwa-register.js",  # Register service worker
	"offline-storage.js",  # Offline data management
]

app_include_css = [
	"desk.bundle.css",
	"mobile-first.css",  # Responsive design
]

# Add manifest link
web_include_head = [
	'<link rel="manifest" href="/assets/manifest.json">'
]
```

---

## Decision Tree: When to Call PWA-Builder

**Use PWA-Builder when:**
- ✅ Creating mobile app experience
- ✅ Adding offline functionality
- ✅ Building service workers
- ✅ Mobile-first responsive design
- ✅ Push notifications setup
- ✅ App manifest creation
- ✅ Tab-based mobile navigation

**Don't use for:**
- ❌ Regular form customization (use Frontend-Forge)
- ❌ API development (use API-Whitelister)
- ❌ Permission setup (use Permission-Guardian)
- ❌ Database operations (use Database-Navigator)

---

**Last Updated**: 2026-02-19
**Frappe Version**: v15.100.1
**PWA Standards**: W3C-compliant
