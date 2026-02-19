# Dialysis Center Management System - Frontend Design & Implementation Guide

**Version:** 1.0.0  
**Last Updated:** 2026-02-19  
**Framework:** Frappe Framework v15 with Vue.js 3  
**Target Devices:** Desktop, Tablet, Mobile (Responsive)

---

## Table of Contents

1. [Frontend Architecture](#1-frontend-architecture)
2. [Design System & UI Guidelines](#2-design-system--ui-guidelines)
3. [Page Layouts & Navigation](#3-page-layouts--navigation)
4. [Component Library](#4-component-library)
5. [Forms & Data Entry](#5-forms--data-entry)
6. [Dashboard & Analytics](#6-dashboard--analytics)
7. [Calendar & Scheduling](#7-calendar--scheduling)
8. [Clinical Workflow Interfaces](#8-clinical-workflow-interfaces)
9. [Mobile & Responsive Design](#9-mobile--responsive-design)
10. [State Management](#10-state-management)
11. [API Integration](#11-api-integration)
12. [Performance Optimization](#12-performance-optimization)
13. [Accessibility (WCAG 2.1)](#13-accessibility-wcag-21)
14. [Testing Strategy](#14-testing-strategy)
15. [Build & Deployment](#15-build--deployment)

---

## 1. Frontend Architecture

### 1.1 Technology Stack

```yaml
Core Framework: Frappe Framework v15
JavaScript:
  - Vue.js 3.x (Composition API)
  - Vanilla JavaScript for Frappe integrations
  
UI Libraries:
  - Frappe UI Components (built-in)
  - Chart.js / ApexCharts (visualizations)
  - FullCalendar (scheduling)
  - DataTables (list views)
  
Build Tools:
  - esbuild (bundler)
  - Vite (dev server for Vue components)
  - PostCSS (CSS processing)
  
Styling:
  - SCSS/SASS
  - Tailwind CSS (optional)
  - Frappe UI Theme System
```

### 1.2 Application Structure

```
dialysis_center/public/
├── js/
│   ├── dialysis_center.bundle.js       # Main bundle
│   ├── patient_portal.bundle.js        # Patient portal
│   ├── components/                     # Vue components
│   │   ├── PatientCard.vue
│   │   ├── AppointmentCalendar.vue
│   │   ├── SessionMonitor.vue
│   │   ├── VitalsChart.vue
│   │   └── ...
│   ├── pages/                          # Custom pages
│   │   ├── session_dashboard/
│   │   ├── patient_dashboard/
│   │   └── ...
│   ├── utils/                          # Utility functions
│   │   ├── api.js
│   │   ├── validators.js
│   │   ├── formatters.js
│   │   └── ...
│   └── store/                          # State management
│       ├── index.js
│       ├── modules/
│       │   ├── patient.js
│       │   ├── appointment.js
│       │   └── session.js
│       └── ...
├── css/
│   ├── dialysis_center.bundle.css
│   ├── components/
│   │   ├── _patient-card.scss
│   │   ├── _calendar.scss
│   │   ├── _session-monitor.scss
│   │   └── ...
│   ├── pages/
│   │   └── ...
│   ├── themes/
│   │   ├── _variables.scss
│   │   ├── _light.scss
│   │   └── _dark.scss
│   └── utils/
│       ├── _mixins.scss
│       └── _helpers.scss
├── images/
│   ├── icons/
│   ├── illustrations/
│   └── logos/
└── fonts/
    └── ...
```

### 1.3 Bundle Configuration

**hooks.py configuration:**
```python
# App bundles
app_include_js = [
    "dialysis_center.bundle.js"
]

app_include_css = [
    "dialysis_center.bundle.css"
]

# DocType-specific JavaScript
doctype_js = {
    "Patient": "public/js/doctype/patient.js",
    "Appointment": "public/js/doctype/appointment.js",
    "Dialysis Session": "public/js/doctype/dialysis_session.js",
    "Lab Result": "public/js/doctype/lab_result.js",
}

# DocType-specific CSS
doctype_list_js = {
    "Patient": "public/js/doctype/patient_list.js",
    "Appointment": "public/js/doctype/appointment_list.js",
}

# Page-specific JavaScript
page_js = {
    "session-dashboard": "public/js/pages/session_dashboard.js",
    "patient-dashboard": "public/js/pages/patient_dashboard.js",
}

# Web includes (for portal)
web_include_js = [
    "patient_portal.bundle.js"
]

web_include_css = [
    "patient_portal.bundle.css"
]
```

---

## 2. Design System & UI Guidelines

### 2.1 Color Palette

```scss
// Primary Colors
$primary-blue: #2490EF;          // Actions, links
$primary-dark: #1976D2;          // Hover states
$primary-light: #64B5F6;         // Backgrounds

// Status Colors
$success-green: #28A745;         // Completed, healthy
$warning-orange: #FFA000;        // Pending, caution
$danger-red: #DC3545;            // Critical, errors
$info-cyan: #17A2B8;             // Information

// Clinical Colors
$dialysis-active: #4CAF50;       // Active session
$dialysis-scheduled: #2196F3;    // Scheduled
$dialysis-completed: #9E9E9E;    // Completed
$alert-critical: #F44336;        // Critical alerts
$alert-warning: #FF9800;         // Warnings

// Neutral Colors
$gray-100: #F8F9FA;              // Backgrounds
$gray-200: #E9ECEF;              // Borders
$gray-300: #DEE2E6;
$gray-400: #CED4DA;
$gray-500: #ADB5BD;              // Text (secondary)
$gray-600: #6C757D;
$gray-700: #495057;
$gray-800: #343A40;
$gray-900: #212529;              // Text (primary)

// Background
$bg-primary: #FFFFFF;
$bg-secondary: #F8F9FA;
$bg-tertiary: #E9ECEF;
```

### 2.2 Typography

```scss
// Font Family
$font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
$font-monospace: 'Fira Code', 'Courier New', monospace;

// Font Sizes
$font-size-xs: 0.75rem;    // 12px
$font-size-sm: 0.875rem;   // 14px
$font-size-base: 1rem;     // 16px
$font-size-lg: 1.125rem;   // 18px
$font-size-xl: 1.25rem;    // 20px
$font-size-2xl: 1.5rem;    // 24px
$font-size-3xl: 1.875rem;  // 30px
$font-size-4xl: 2.25rem;   // 36px

// Font Weights
$font-weight-light: 300;
$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;

// Line Heights
$line-height-tight: 1.2;
$line-height-normal: 1.5;
$line-height-relaxed: 1.75;
```

### 2.3 Spacing System

```scss
// Spacing Scale (based on 4px)
$space-1: 0.25rem;   // 4px
$space-2: 0.5rem;    // 8px
$space-3: 0.75rem;   // 12px
$space-4: 1rem;      // 16px
$space-5: 1.25rem;   // 20px
$space-6: 1.5rem;    // 24px
$space-8: 2rem;      // 32px
$space-10: 2.5rem;   // 40px
$space-12: 3rem;     // 48px
$space-16: 4rem;     // 64px
```

### 2.4 Border Radius

```scss
$border-radius-sm: 0.25rem;   // 4px
$border-radius-md: 0.5rem;    // 8px
$border-radius-lg: 0.75rem;   // 12px
$border-radius-xl: 1rem;      // 16px
$border-radius-full: 9999px;  // Circular
```

### 2.5 Shadows

```scss
$shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
$shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
$shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
$shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

---

## 3. Page Layouts & Navigation

### 3.1 Main Navigation Structure

```html
<!-- Top Navigation Bar -->
<nav class="navbar navbar-main">
  <div class="navbar-brand">
    <img src="/assets/dialysis_center/images/logo.svg" alt="Logo">
    <span>Dialysis Center</span>
  </div>
  
  <div class="navbar-menu">
    <a href="/app/patient" class="nav-item">
      <i class="fa fa-users"></i>
      <span>Patients</span>
    </a>
    <a href="/app/appointment" class="nav-item">
      <i class="fa fa-calendar"></i>
      <span>Appointments</span>
    </a>
    <a href="/app/session-dashboard" class="nav-item active">
      <i class="fa fa-heartbeat"></i>
      <span>Sessions</span>
    </a>
    <a href="/app/inventory-item" class="nav-item">
      <i class="fa fa-box"></i>
      <span>Inventory</span>
    </a>
    <a href="/app/reports" class="nav-item">
      <i class="fa fa-chart-bar"></i>
      <span>Reports</span>
    </a>
  </div>
  
  <div class="navbar-actions">
    <!-- Quick Actions -->
    <button class="btn-icon" data-action="new-appointment">
      <i class="fa fa-plus"></i>
    </button>
    
    <!-- Notifications -->
    <div class="notifications-dropdown">
      <button class="btn-icon" data-toggle="dropdown">
        <i class="fa fa-bell"></i>
        <span class="badge">3</span>
      </button>
    </div>
    
    <!-- User Menu -->
    <div class="user-menu">
      <button class="user-avatar" data-toggle="dropdown">
        <img src="/api/method/frappe.utils.get_user_avatar" alt="User">
      </button>
    </div>
  </div>
</nav>
```

### 3.2 Workspace Layout

**Frappe Workspace Configuration:**
```json
{
  "name": "Dialysis Center",
  "title": "Dialysis Center",
  "icon": "heartbeat",
  "category": "Modules",
  "charts": [
    {
      "chart_name": "Daily Sessions",
      "label": "Daily Sessions"
    },
    {
      "chart_name": "Patient Status",
      "label": "Patient Status"
    }
  ],
  "shortcuts": [
    {
      "type": "DocType",
      "label": "New Patient",
      "doc_view": "Patient",
      "color": "#2490EF"
    },
    {
      "type": "DocType",
      "label": "New Appointment",
      "doc_view": "Appointment",
      "color": "#28A745"
    },
    {
      "type": "Page",
      "label": "Session Dashboard",
      "link_to": "session-dashboard",
      "color": "#DC3545"
    }
  ],
  "links": [
    {
      "label": "Patient Management",
      "type": "Card Break"
    },
    {
      "label": "Patient",
      "type": "Link",
      "link_type": "DocType",
      "link_to": "Patient"
    },
    {
      "label": "Medical History",
      "type": "Link",
      "link_type": "DocType",
      "link_to": "Medical History"
    }
  ]
}
```

### 3.3 Dashboard Layout Pattern

```html
<div class="dashboard-container">
  <!-- Header with Filters -->
  <div class="dashboard-header">
    <h1>Session Dashboard</h1>
    <div class="dashboard-filters">
      <select class="form-control" id="location-filter">
        <option>All Locations</option>
      </select>
      <input type="date" class="form-control" id="date-filter">
      <button class="btn btn-primary">Refresh</button>
    </div>
  </div>
  
  <!-- Key Metrics -->
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-icon bg-success">
        <i class="fa fa-heartbeat"></i>
      </div>
      <div class="metric-content">
        <h3>12</h3>
        <p>Active Sessions</p>
      </div>
    </div>
    <!-- More metric cards -->
  </div>
  
  <!-- Main Content Area -->
  <div class="dashboard-content">
    <div class="content-grid">
      <!-- Left Column (70%) -->
      <div class="content-main">
        <!-- Session Monitor -->
        <div class="card">
          <div class="card-header">
            <h3>Active Sessions</h3>
          </div>
          <div class="card-body">
            <!-- Component content -->
          </div>
        </div>
      </div>
      
      <!-- Right Sidebar (30%) -->
      <div class="content-sidebar">
        <!-- Upcoming Appointments -->
        <div class="card">
          <div class="card-header">
            <h3>Upcoming</h3>
          </div>
          <div class="card-body">
Tool call argument 'replace' pruned from message history.

            <!-- Upcoming appointments list -->
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

## 4. Component Library

### 4.1 PatientCard Component

**Vue Component: `PatientCard.vue`**

```vue
<template>
  <div class="patient-card" @click="$emit('click', patient)">
    <div class="patient-header">
      <div class="patient-avatar">
        {{ initials }}
      </div>
      <div class="patient-info">
        <h3>{{ patient.patient_name }}</h3>
        <p class="patient-id">{{ patient.name }}</p>
      </div>
      <span :class="['status-badge', patient.status.toLowerCase()]">
        {{ patient.status }}
      </span>
    </div>
    
    <div class="patient-details">
      <div class="detail-item">
        <span class="detail-label">Age</span>
        <span class="detail-value">{{ patient.age }} years</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Blood Group</span>
        <span class="detail-value">{{ patient.blood_group }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Dialysis Type</span>
        <span class="detail-value">{{ patient.dialysis_type }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Next Session</span>
        <span class="detail-value">{{ formatDate(patient.next_session) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'PatientCard',
  props: {
    patient: {
      type: Object,
      required: true
    }
  },
  emits: ['click'],
  setup(props) {
    const initials = computed(() => {
      return props.patient.patient_name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase();
    });
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    };
    
    return {
      initials,
      formatDate
    };
  }
};
</script>

<style scoped>
.patient-card {
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 16px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.patient-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.patient-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.patient-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: var(--primary-dark);
  font-size: 1.125rem;
}

.patient-info {
  flex: 1;
}

.patient-info h3 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--gray-900);
}

.patient-id {
  margin: 0;
  color: var(--gray-600);
  font-size: 0.875rem;
}

.patient-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 0.75rem;
  color: var(--gray-600);
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 0.875rem;
  color: var(--gray-900);
  font-weight: 500;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
}
</style>
```

### 4.2 SessionMonitor Component

**Vue Component: `SessionMonitor.vue`**

```vue
<template>
  <div class="session-monitor">
    <div class="session-grid">
      <div 
        v-for="session in sessions" 
        :key="session.name"
        :class="['session-card', getStatusClass(session)]"
        @click="openSession(session)"
      >
        <div class="session-header">
          <div class="machine-info">
            <i class="fa fa-cog"></i>
            <span>{{ session.machine_name }}</span>
          </div>
          <span :class="['session-status', session.status.toLowerCase()]">
            {{ session.status }}
          </span>
        </div>
        
        <div class="patient-info">
          <h4>{{ session.patient_name }}</h4>
          <p>{{ session.patient_id }}</p>
        </div>
        
        <div class="session-progress">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: getProgress(session) + '%' }"
            ></div>
          </div>
          <div class="progress-time">
            <span>{{ session.elapsed_time }}</span>
            <span>{{ session.duration }} min</span>
          </div>
        </div>
        
        <div class="vital-signs">
          <div class="vital-item">
            <i class="fa fa-heartbeat"></i>
            <span>{{ session.heart_rate }} bpm</span>
          </div>
          <div class="vital-item">
            <i class="fa fa-tint"></i>
            <span>{{ session.blood_pressure }}</span>
          </div>
          <div class="vital-item">
            <i class="fa fa-thermometer-half"></i>
            <span>{{ session.temperature }}°C</span>
          </div>
        </div>
        
        <div v-if="hasAlerts(session)" class="session-alerts">
          <i class="fa fa-exclamation-triangle"></i>
          <span>{{ session.alert_message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';

export default {
  name: 'SessionMonitor',
  props: {
    location: {
      type: String,
      default: null
    }
  },
  setup(props) {
    const sessions = ref([]);
    let refreshInterval = null;
    
    const fetchSessions = async () => {
      try {
        const response = await frappe.call({
          method: 'dialysis_center.api.session.get_active_sessions',
          args: {
            location: props.location
          }
        });
        sessions.value = response.message || [];
      } catch (error) {
        console.error('Error fetching sessions:', error);
        frappe.show_alert({
          message: 'Failed to load active sessions',
          indicator: 'red'
        });
      }
    };
    
    const getProgress = (session) => {
      const elapsed = parseFloat(session.elapsed_time);
      const duration = parseFloat(session.duration);
      return Math.min((elapsed / duration) * 100, 100);
    };
    
    const getStatusClass = (session) => {
      if (hasAlerts(session)) return 'has-alert';
      return '';
    };
    
    const hasAlerts = (session) => {
      return session.alert_message && session.alert_message.length > 0;
    };
    
    const openSession = (session) => {
      frappe.set_route('Form', 'Dialysis Session', session.name);
    };
    
    onMounted(() => {
      fetchSessions();
      // Refresh every 30 seconds
      refreshInterval = setInterval(fetchSessions, 30000);
    });
    
    onUnmounted(() => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    });
    
    return {
      sessions,
      getProgress,
      getStatusClass,
      hasAlerts,
      openSession
    };
  }
};
</script>

<style scoped>
.session-monitor {
  width: 100%;
}

.session-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.session-card {
  border: 2px solid var(--gray-200);
  border-radius: 12px;
  padding: 16px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.session-card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.session-card.has-alert {
  border-color: var(--danger-red);
  animation: pulse-border 2s infinite;
}

@keyframes pulse-border {
  0%, 100% { border-color: var(--danger-red); }
  50% { border-color: var(--warning-orange); }
}

.session-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.machine-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: var(--gray-600);
}

.session-status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.session-status.active {
  background: #d4edda;
  color: #155724;
}

.patient-info h4 {
  margin: 0 0 4px 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--gray-900);
}

.patient-info p {
  margin: 0;
  font-size: 0.875rem;
  color: var(--gray-600);
}

.session-progress {
  margin: 16px 0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--gray-200);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--success-green), var(--primary-blue));
  transition: width 0.3s ease;
}

.progress-time {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--gray-600);
}

.vital-signs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding: 12px 0;
  border-top: 1px solid var(--gray-200);
  border-bottom: 1px solid var(--gray-200);
}

.vital-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 0.875rem;
}

.vital-item i {
  color: var(--primary-blue);
}

.session-alerts {
  margin-top: 12px;
  padding: 8px 12px;
  background: #fff3cd;
  border-left: 4px solid var(--danger-red);
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: #856404;
}

.session-alerts i {
  color: var(--danger-red);
}
</style>
```


### 4.3 AppointmentCalendar Component

**Vue Component: `AppointmentCalendar.vue`**

```vue
<template>
  <div class="appointment-calendar">
    <FullCalendar :options="calendarOptions" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

export default {
  name: 'AppointmentCalendar',
  components: {
    FullCalendar
  },
  setup() {
    const calendarOptions = ref({
      plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
      initialView: 'timeGridWeek',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      slotMinTime: '06:00:00',
      slotMaxTime: '22:00:00',
      slotDuration: '00:30:00',
      allDaySlot: false,
      editable: true,
      selectable: true,
      selectMirror: true,
      dayMaxEvents: true,
      weekends: true,
      events: [],
      select: handleDateSelect,
      eventClick: handleEventClick,
      eventDrop: handleEventDrop,
      eventResize: handleEventResize,
      eventContent: renderEventContent
    });
    
    const handleDateSelect = (selectInfo) => {
      frappe.new_doc('Appointment', {
        appointment_date: selectInfo.startStr.split('T')[0],
        appointment_time: selectInfo.startStr.split('T')[1].substring(0, 5)
      });
    };
    
    const handleEventClick = (clickInfo) => {
      frappe.set_route('Form', 'Appointment', clickInfo.event.id);
    };
    
    const handleEventDrop = async (dropInfo) => {
      try {
        await frappe.call({
          method: 'dialysis_center.api.appointment.reschedule',
          args: {
            appointment_id: dropInfo.event.id,
            new_date: dropInfo.event.startStr.split('T')[0],
            new_time: dropInfo.event.startStr.split('T')[1].substring(0, 5)
          }
        });
        frappe.show_alert({
          message: 'Appointment rescheduled',
          indicator: 'green'
        });
      } catch (error) {
        dropInfo.revert();
        frappe.show_alert({
          message: 'Failed to reschedule appointment',
          indicator: 'red'
        });
      }
    };
    
    const handleEventResize = async (resizeInfo) => {
      try {
        await frappe.call({
          method: 'dialysis_center.api.appointment.update_duration',
          args: {
            appointment_id: resizeInfo.event.id,
            duration: (resizeInfo.event.end - resizeInfo.event.start) / 60000
          }
        });
      } catch (error) {
        resizeInfo.revert();
      }
    };
    
    const renderEventContent = (eventInfo) => {
      return {
        html: `
          <div class="fc-event-main-frame">
            <div class="fc-event-time">${eventInfo.timeText}</div>
            <div class="fc-event-title-container">
              <div class="fc-event-title">${eventInfo.event.title}</div>
              <div class="fc-event-machine">${eventInfo.event.extendedProps.machine}</div>
            </div>
          </div>
        `
      };
    };
    
    const loadAppointments = async () => {
      try {
        const response = await frappe.call({
          method: 'dialysis_center.api.appointment.get_calendar_events',
          args: {}
        });
        calendarOptions.value.events = response.message.map(apt => ({
          id: apt.name,
          title: apt.patient_name,
          start: `${apt.appointment_date}T${apt.appointment_time}`,
          end: `${apt.appointment_date}T${apt.end_time}`,
          backgroundColor: getStatusColor(apt.status),
          borderColor: getStatusColor(apt.status),
          extendedProps: {
            machine: apt.machine_name,
            patient_id: apt.patient,
            status: apt.status
          }
        }));
      } catch (error) {
        console.error('Error loading appointments:', error);
      }
    };
    
    const getStatusColor = (status) => {
      const colors = {
        'Scheduled': '#2196F3',
        'Confirmed': '#4CAF50',
        'Checked In': '#FF9800',
        'In Progress': '#9C27B0',
        'Completed': '#9E9E9E',
        'Cancelled': '#F44336'
      };
      return colors[status] || '#2196F3';
    };
    
    onMounted(() => {
      loadAppointments();
    });
    
    return {
      calendarOptions
    };
  }
};
</script>

<style scoped>
.appointment-calendar {
  background: white;
  padding: 16px;
  border-radius: 8px;
}

:deep(.fc) {
  font-family: var(--font-primary);
}

:deep(.fc-event) {
  border-radius: 4px;
  padding: 4px;
  font-size: 0.875rem;
}

:deep(.fc-event-machine) {
  font-size: 0.75rem;
  opacity: 0.8;
  margin-top: 2px;
}
</style>
```

---

## 5. Forms & Data Entry

### 5.1 Enhanced DocType Form (Patient)

**File: `dialysis_center/public/js/doctype/patient.js`**

```javascript
frappe.ui.form.on('Patient', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			frm.add_custom_button(__('Book Appointment'), function() {
				frappe.new_doc('Appointment', {
					patient: frm.doc.name,
					patient_name: frm.doc.patient_name
				});
			}, __('Actions'));
			
			frm.add_custom_button(__('View Medical History'), function() {
				frappe.set_route('List', 'Medical History', {
					patient: frm.doc.name
				});
			}, __('View'));
			
			frm.add_custom_button(__('Session History'), function() {
				frappe.set_route('List', 'Dialysis Session', {
					patient: frm.doc.name
				});
			}, __('View'));
			
			// Dashboard indicators
			frm.dashboard.add_indicator(__('Active Sessions: {0}', [frm.doc.active_sessions || 0]), 'blue');
			frm.dashboard.add_indicator(__('Upcoming: {0}', [frm.doc.upcoming_appointments || 0]), 'orange');
			
			// Load dashboard data
			load_patient_dashboard(frm);
		}
		
		// Custom styling based on status
		if (frm.doc.status === 'Inactive') {
			frm.set_indicator_formatter('status', function(doc) {
				return (doc.status === 'Active') ? 'green' : 'red';
			});
		}
	},
	
	date_of_birth: function(frm) {
		// Auto-calculate age
		if (frm.doc.date_of_birth) {
			const age = frappe.datetime.get_age(frm.doc.date_of_birth);
			frm.set_value('age', age);
		}
	},
	
	national_id: function(frm) {
		// Validate national ID format
		if (frm.doc.national_id) {
			validate_national_id(frm);
		}
	},
	
	dialysis_type: function(frm) {
		// Set default treatment template based on dialysis type
		if (frm.doc.dialysis_type) {
			frappe.call({
				method: 'dialysis_center.api.patient.get_default_template',
				args: {
					dialysis_type: frm.doc.dialysis_type
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('default_treatment_template', r.message);
					}
				}
			});
		}
	}
});

function load_patient_dashboard(frm) {
	// Load recent vitals chart
	frappe.call({
		method: 'dialysis_center.api.patient.get_vitals_trend',
		args: {
			patient: frm.doc.name,
			days: 30
		},
		callback: function(r) {
			if (r.message) {
				render_vitals_chart(frm, r.message);
			}
		}
	});
	
	// Load upcoming appointments
	frappe.call({
		method: 'dialysis_center.api.patient.get_upcoming_appointments',
		args: {
			patient: frm.doc.name,
			limit: 5
		},
		callback: function(r) {
			if (r.message) {
				render_upcoming_appointments(frm, r.message);
			}
		}
	});
}

function render_vitals_chart(frm, data) {
	const wrapper = frm.fields_dict.vitals_chart_html.$wrapper;
	wrapper.empty();
	
	const chart = new frappe.Chart(wrapper[0], {
		title: 'Vital Signs Trend (Last 30 Days)',
		data: {
			labels: data.labels,
			datasets: [
				{
					name: 'Systolic BP',
					values: data.systolic,
					chartType: 'line'
				},
				{
					name: 'Diastolic BP',
					values: data.diastolic,
					chartType: 'line'
				},
				{
					name: 'Heart Rate',
					values: data.heart_rate,
					chartType: 'line'
				}
			]
		},
		type: 'axis-mixed',
		height: 250,
		colors: ['#F44336', '#2196F3', '#4CAF50']
	});
}

function render_upcoming_appointments(frm, appointments) {
	const wrapper = frm.fields_dict.upcoming_appointments_html.$wrapper;
	wrapper.empty();
	
	const html = `
		<div class="upcoming-appointments">
			<h4>Upcoming Appointments</h4>
			<div class="appointments-list">
				${appointments.map(apt => `
					<div class="appointment-item">
						<div class="appointment-date">
							<i class="fa fa-calendar"></i>
							${frappe.datetime.str_to_user(apt.appointment_date)}
						</div>
						<div class="appointment-time">
							<i class="fa fa-clock"></i>
							${apt.appointment_time}
						</div>
						<div class="appointment-machine">
							<i class="fa fa-cog"></i>
							${apt.machine_name}
						</div>
						<a href="/app/appointment/${apt.name}" class="btn btn-xs btn-default">
							View
						</a>
					</div>
				`).join('')}
			</div>
		</div>
	`;
	
	wrapper.html(html);
}

function validate_national_id(frm) {
	// Example validation for Saudi national ID
	const id = frm.doc.national_id;
	const pattern = /^[12]\d{9}$/;
	
	if (!pattern.test(id)) {
		frappe.msgprint({
			title: __('Invalid National ID'),
			message: __('National ID must be 10 digits starting with 1 or 2'),
			indicator: 'red'
		});
		frm.set_value('national_id', '');
	}
}
```

### 5.2 Form Validation Utilities

**File: `dialysis_center/public/js/utils/validators.js`**

```javascript
// Custom validation functions for dialysis center

export const validators = {
	// Validate blood pressure format (120/80)
	validateBloodPressure: function(value) {
		const pattern = /^\d{2,3}\/\d{2,3}$/;
		if (!pattern.test(value)) {
			return 'Invalid blood pressure format. Use XXX/XX (e.g., 120/80)';
		}
		
		const [systolic, diastolic] = value.split('/').map(Number);
		if (systolic < 70 || systolic > 250) {
			return 'Systolic pressure must be between 70 and 250';
		}
		if (diastolic < 40 || diastolic > 150) {
			return 'Diastolic pressure must be between 40 and 150';
		}
		if (systolic <= diastolic) {
			return 'Systolic must be greater than diastolic';
		}
		
		return true;
	},
	
	// Validate temperature range
	validateTemperature: function(value) {
		const temp = parseFloat(value);
		if (isNaN(temp)) {
			return 'Temperature must be a number';
		}
		if (temp < 35 || temp > 42) {
			return 'Temperature must be between 35°C and 42°C';
		}
		return true;
	},
	
	// Validate heart rate
	validateHeartRate: function(value) {
		const hr = parseInt(value);
		if (isNaN(hr)) {
			return 'Heart rate must be a number';
		}
		if (hr < 40 || hr > 200) {
			return 'Heart rate must be between 40 and 200 bpm';
		}
		return true;
	},
	
	// Validate weight
	validateWeight: function(value) {
		const weight = parseFloat(value);
		if (isNaN(weight)) {
			return 'Weight must be a number';
		}
		if (weight < 20 || weight > 300) {
			return 'Weight must be between 20 and 300 kg';
		}
		return true;
	},
	
	// Validate UF goal
	validateUFGoal: function(value) {
		const uf = parseFloat(value);
		if (isNaN(uf)) {
			return 'UF goal must be a number';
		}
		if (uf < 0 || uf > 10) {
			return 'UF goal must be between 0 and 10 liters';
		}
		return true;
	},
	
	// Validate blood flow rate
	validateBloodFlowRate: function(value) {
		const qb = parseInt(value);
		if (isNaN(qb)) {
			return 'Blood flow rate must be a number';
		}
		if (qb < 100 || qb > 500) {
			return 'Blood flow rate must be between 100 and 500 ml/min';
		}
		return true;
	},
	
	// Validate dialysate flow rate
	validateDialysateFlowRate: function(value) {
		const qd = parseInt(value);
		if (isNaN(qd)) {
			return 'Dialysate flow rate must be a number';
		}
		if (qd < 300 || qd > 800) {
			return 'Dialysate flow rate must be between 300 and 800 ml/min';
		}
		return true;
	},
	
	// Validate session duration
	validateSessionDuration: function(value) {
		const duration = parseInt(value);
		if (isNaN(duration)) {
			return 'Duration must be a number';
		}
		if (duration < 120 || duration > 360) {
			return 'Session duration must be between 2 and 6 hours (120-360 minutes)';
		}
		if (duration % 30 !== 0) {
			return 'Duration must be in 30-minute increments';
		}
		return true;
	}
};

// Apply validator to a field
export function applyValidator(frm, fieldname, validator) {
	frm.fields_dict[fieldname].$input.on('change', function() {
		const value = frm.doc[fieldname];
		if (value) {
			const result = validator(value);
			if (result !== true) {
				frappe.msgprint({
					title: __('Validation Error'),
					message: result,
					indicator: 'red'
				});
				frm.set_value(fieldname, '');
			}
		}
	});
}
```


---

## 6. Dashboard & Analytics

### 6.1 Session Dashboard Page

**File: `dialysis_center/dialysis_center/page/session_dashboard/session_dashboard.js`**

```javascript
frappe.pages['session-dashboard'].on_page_load = function(wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Session Dashboard',
		single_column: true
	});
	
	new SessionDashboard(page);
};

class SessionDashboard {
	constructor(page) {
		this.page = page;
		this.filters = {};
		this.refresh_interval = null;
		
		this.setup_page();
		this.setup_filters();
		this.load_dashboard();
		this.start_auto_refresh();
	}
	
	setup_page() {
		// Add custom buttons
		this.page.add_inner_button(__('New Session'), () => {
			frappe.new_doc('Dialysis Session');
		});
		
		this.page.add_inner_button(__('Refresh'), () => {
			this.load_dashboard();
		});
		
		// Create dashboard container
		this.page.main.html(`
			<div class="session-dashboard-container">
				<div class="metrics-section"></div>
				<div class="sessions-section"></div>
				<div class="sidebar-section"></div>
			</div>
		`);
	}
	
	setup_filters() {
		// Location filter
		this.page.add_field({
			label: __('Location'),
			fieldtype: 'Link',
			fieldname: 'location',
			options: 'Location',
			change: () => {
				this.filters.location = this.page.fields_dict.location.get_value();
				this.load_dashboard();
			}
		});
		
		// Date filter
		this.page.add_field({
			label: __('Date'),
			fieldtype: 'Date',
			fieldname: 'date',
			default: frappe.datetime.get_today(),
			change: () => {
				this.filters.date = this.page.fields_dict.date.get_value();
				this.load_dashboard();
			}
		});
		
		// Shift filter
		this.page.add_field({
			label: __('Shift'),
			fieldtype: 'Select',
			fieldname: 'shift',
			options: ['All', 'Morning', 'Afternoon', 'Evening'],
			default: 'All',
			change: () => {
				this.filters.shift = this.page.fields_dict.shift.get_value();
				this.load_dashboard();
			}
		});
	}
	
	async load_dashboard() {
		try {
			const response = await frappe.call({
				method: 'dialysis_center.api.dashboard.get_session_dashboard_data',
				args: this.filters
			});
			
			if (response.message) {
				this.render_metrics(response.message.metrics);
				this.render_active_sessions(response.message.active_sessions);
				this.render_sidebar(response.message);
			}
		} catch (error) {
			frappe.show_alert({
				message: __('Failed to load dashboard'),
				indicator: 'red'
			});
		}
	}
	
	render_metrics(metrics) {
		const container = this.page.main.find('.metrics-section');
		container.html(`
			<div class="metrics-grid">
				<div class="metric-card">
					<div class="metric-icon bg-success">
						<i class="fa fa-heartbeat"></i>
					</div>
					<div class="metric-content">
						<h3>${metrics.active_sessions}</h3>
						<p>${__('Active Sessions')}</p>
					</div>
				</div>
				<div class="metric-card">
					<div class="metric-icon bg-primary">
						<i class="fa fa-calendar-check"></i>
					</div>
					<div class="metric-content">
						<h3>${metrics.scheduled_today}</h3>
						<p>${__('Scheduled Today')}</p>
					</div>
				</div>
				<div class="metric-card">
					<div class="metric-icon bg-warning">
						<i class="fa fa-clock"></i>
					</div>
					<div class="metric-content">
						<h3>${metrics.waiting}</h3>
						<p>${__('Waiting')}</p>
					</div>
				</div>
				<div class="metric-card">
					<div class="metric-icon bg-info">
						<i class="fa fa-cog"></i>
					</div>
					<div class="metric-content">
						<h3>${metrics.available_machines}/${metrics.total_machines}</h3>
						<p>${__('Available Machines')}</p>
					</div>
				</div>
			</div>
		`);
	}
	
	render_active_sessions(sessions) {
		const container = this.page.main.find('.sessions-section');
		
		if (sessions.length === 0) {
			container.html(`
				<div class="empty-state">
					<i class="fa fa-info-circle"></i>
					<p>${__('No active sessions')}</p>
				</div>
			`);
			return;
		}
		
		// Use Vue component for session monitoring
		const wrapper = $('<div class="session-monitor-wrapper"></div>');
		container.html(wrapper);
		
		new Vue({
			el: wrapper[0],
			template: '<SessionMonitor :location="location" />',
			components: { SessionMonitor },
			data: {
				location: this.filters.location
			}
		});
	}
	
	render_sidebar(data) {
		const container = this.page.main.find('.sidebar-section');
		container.html(`
			<div class="sidebar-content">
				<!-- Upcoming Appointments -->
				<div class="sidebar-card">
					<h4>${__('Upcoming Appointments')}</h4>
					<div class="appointment-list">
						${data.upcoming_appointments.map(apt => `
							<div class="appointment-item" onclick="frappe.set_route('Form', 'Appointment', '${apt.name}')">
								<div class="apt-time">${apt.appointment_time}</div>
								<div class="apt-patient">${apt.patient_name}</div>
								<div class="apt-machine">${apt.machine_name}</div>
							</div>
						`).join('')}
					</div>
				</div>
				
				<!-- Alerts & Notifications -->
				<div class="sidebar-card">
					<h4>${__('Alerts')}</h4>
					<div class="alerts-list">
						${data.alerts.map(alert => `
							<div class="alert-item ${alert.severity}">
								<i class="fa fa-exclamation-triangle"></i>
								<div class="alert-message">${alert.message}</div>
								<div class="alert-time">${frappe.datetime.comment_when(alert.timestamp)}</div>
							</div>
						`).join('')}
					</div>
				</div>
				
				<!-- Staff on Duty -->
				<div class="sidebar-card">
					<h4>${__('Staff on Duty')}</h4>
					<div class="staff-list">
						${data.staff_on_duty.map(staff => `
							<div class="staff-item">
								<div class="staff-avatar">
									${staff.name.charAt(0)}
								</div>
								<div class="staff-info">
									<div class="staff-name">${staff.staff_name}</div>
									<div class="staff-role">${staff.role}</div>
								</div>
							</div>
						`).join('')}
					</div>
				</div>
			</div>
		`);
	}
	
	start_auto_refresh() {
		// Auto-refresh every 30 seconds
		this.refresh_interval = setInterval(() => {
			this.load_dashboard();
		}, 30000);
	}
	
	destroy() {
		if (this.refresh_interval) {
			clearInterval(this.refresh_interval);
		}
	}
}
```

### 6.2 Analytics Charts

**File: `dialysis_center/public/js/components/VitalsChart.vue`**

```vue
<template>
  <div class="vitals-chart">
    <div class="chart-header">
      <h4>{{ title }}</h4>
      <div class="chart-controls">
        <select v-model="timeRange" @change="loadData">
          <option value="7">Last 7 Days</option>
          <option value="30">Last 30 Days</option>
          <option value="90">Last 90 Days</option>
        </select>
      </div>
    </div>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import ApexCharts from 'apexcharts';

export default {
  name: 'VitalsChart',
  props: {
    patient: {
      type: String,
      required: true
    },
    title: {
      type: String,
      default: 'Vital Signs Trend'
    }
  },
  setup(props) {
    const chartContainer = ref(null);
    const timeRange = ref(30);
    let chart = null;
    
    const chartOptions = {
      chart: {
        type: 'line',
        height: 350,
        toolbar: {
          show: true
        },
        zoom: {
          enabled: true
        }
      },
      stroke: {
        width: [3, 3, 3],
        curve: 'smooth'
      },
      markers: {
        size: 4,
        hover: {
          size: 6
        }
      },
      xaxis: {
        type: 'datetime',
        labels: {
          format: 'dd MMM'
        }
      },
      yaxis: [
        {
          title: {
            text: 'Blood Pressure (mmHg)'
          },
          min: 60,
          max: 200
        },
        {
          opposite: true,
          title: {
            text: 'Heart Rate (bpm)'
          },
          min: 40,
          max: 140
        }
      ],
      legend: {
        position: 'top'
      },
      colors: ['#F44336', '#2196F3', '#4CAF50'],
      tooltip: {
        shared: true,
        intersect: false,
        x: {
          format: 'dd MMM yyyy HH:mm'
        }
      }
    };
    
    const loadData = async () => {
      try {
        const response = await frappe.call({
          method: 'dialysis_center.api.patient.get_vitals_trend',
          args: {
            patient: props.patient,
            days: timeRange.value
          }
        });
        
        if (response.message) {
          const data = response.message;
          
          const series = [
            {
              name: 'Systolic BP',
              data: data.map(d => [new Date(d.timestamp).getTime(), d.systolic]),
              yAxisIndex: 0
            },
            {
              name: 'Diastolic BP',
              data: data.map(d => [new Date(d.timestamp).getTime(), d.diastolic]),
              yAxisIndex: 0
            },
            {
              name: 'Heart Rate',
              data: data.map(d => [new Date(d.timestamp).getTime(), d.heart_rate]),
              yAxisIndex: 1
            }
          ];
          
          if (chart) {
            chart.updateSeries(series);
          } else {
            chart = new ApexCharts(
              chartContainer.value,
              { ...chartOptions, series }
            );
            chart.render();
          }
        }
      } catch (error) {
        console.error('Error loading vitals data:', error);
      }
    };
    
    onMounted(() => {
      loadData();
    });
    
    watch(() => props.patient, () => {
      loadData();
    });
    
    return {
      chartContainer,
      timeRange,
      loadData
    };
  }
};
</script>

<style scoped>
.vitals-chart {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 16px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-header h4 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--gray-900);
}

.chart-controls select {
  padding: 6px 12px;
  border: 1px solid var(--gray-300);
  border-radius: 4px;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
}

.chart-container {
  width: 100%;
  min-height: 350px;
}
</style>
```

---

## 7. Calendar & Scheduling

### 7.1 Appointment Booking Interface

**File: `dialysis_center/public/js/pages/appointment_booking.js`**

```javascript
class AppointmentBooking {
	constructor(wrapper) {
		this.wrapper = wrapper;
		this.selected_date = frappe.datetime.get_today();
		this.selected_time = null;
		this.selected_machine = null;
		
		this.render();
		this.load_availability();
	}
	
	render() {
		this.wrapper.html(`
			<div class="appointment-booking">
				<div class="booking-header">
					<h2>${__('Book Appointment')}</h2>
				</div>
				
				<div class="booking-content">
					<div class="booking-left">
						<!-- Patient Selection -->
						<div class="form-group">
							<label>${__('Patient')}</label>
							<div class="patient-search"></div>
						</div>
						
						<!-- Date Selection -->
						<div class="form-group">
							<label>${__('Date')}</label>
							<input type="date" class="form-control date-picker" 
								value="${this.selected_date}">
						</div>
						
						<!-- Location Selection -->
						<div class="form-group">
							<label>${__('Location')}</label>
							<div class="location-select"></div>
						</div>
						
						<!-- Shift Selection -->
						<div class="form-group">
							<label>${__('Shift')}</label>
							<div class="shift-buttons">
								<button class="btn btn-shift" data-shift="Morning">
									<i class="fa fa-sun"></i> Morning
								</button>
								<button class="btn btn-shift" data-shift="Afternoon">
									<i class="fa fa-cloud-sun"></i> Afternoon
								</button>
								<button class="btn btn-shift" data-shift="Evening">
									<i class="fa fa-moon"></i> Evening
								</button>
							</div>
						</div>
					</div>
					
					<div class="booking-right">
						<!-- Time Slots -->
						<div class="time-slots-container">
							<h4>${__('Available Time Slots')}</h4>
							<div class="time-slots-grid"></div>
						</div>
						
						<!-- Machine Selection -->
						<div class="machine-selection-container">
							<h4>${__('Select Machine')}</h4>
							<div class="machines-grid"></div>
						</div>
					</div>
				</div>
				
				<div class="booking-footer">
					<button class="btn btn-primary btn-book" disabled>
						${__('Book Appointment')}
					</button>
				</div>
			</div>
		`);
		
		this.setup_event_handlers();
		this.setup_patient_search();
	}
	
	setup_patient_search() {
		const container = this.wrapper.find('.patient-search');
		
		frappe.ui.form.make_control({
			parent: container,
			df: {
				fieldtype: 'Link',
				options: 'Patient',
				fieldname: 'patient',
				placeholder: __('Search patient by name or ID'),
				change: () => {
					this.patient = container.find('input').val();
					this.load_patient_info();
				}
			},
			render_input: true
		});
	}
	
	setup_event_handlers() {
		// Date change
		this.wrapper.find('.date-picker').on('change', (e) => {
			this.selected_date = e.target.value;
			this.load_availability();
		});
		
		// Shift selection
		this.wrapper.find('.btn-shift').on('click', (e) => {
			this.wrapper.find('.btn-shift').removeClass('active');
			$(e.currentTarget).addClass('active');
			this.selected_shift = $(e.currentTarget).data('shift');
			this.load_availability();
		});
		
		// Book button
		this.wrapper.find('.btn-book').on('click', () => {
			this.book_appointment();
		});
	}
	
	async load_availability() {
		try {
			const response = await frappe.call({
				method: 'dialysis_center.api.appointment.check_availability',
				args: {
					date: this.selected_date,
					shift: this.selected_shift,
					location: this.selected_location
				}
			});
			
			if (response.message) {
				this.render_time_slots(response.message.time_slots);
				this.render_machines(response.message.machines);
			}
		} catch (error) {
			frappe.show_alert({
				message: __('Failed to load availability'),
				indicator: 'red'
			});
		}
	}
	
	render_time_slots(slots) {
		const container = this.wrapper.find('.time-slots-grid');
		container.empty();
		
		slots.forEach(slot => {
			const button = $(`
				<button class="time-slot ${slot.available ? '' : 'disabled'}" 
					data-time="${slot.time}"
					${slot.available ? '' : 'disabled'}>
					<div class="slot-time">${slot.time}</div>
					<div class="slot-available">${slot.available_machines} available</div>
				</button>
			`);
			
			button.on('click', () => {
				container.find('.time-slot').removeClass('selected');
				button.addClass('selected');
				this.selected_time = slot.time;
				this.validate_booking();
			});
			
			container.append(button);
		});
	}
	
	render_machines(machines) {
		const container = this.wrapper.find('.machines-grid');
		container.empty();
		
		machines.forEach(machine => {
			const card = $(`
				<div class="machine-card ${machine.available ? '' : 'disabled'}"
					data-machine="${machine.name}">
					<div class="machine-icon">
						<i class="fa fa-cog"></i>
					</div>
					<div class="machine-name">${machine.machine_name}</div>
					<div class="machine-model">${machine.model}</div>
					<div class="machine-status ${machine.status.toLowerCase()}">
						${machine.status}
					</div>
				</div>
			`);
			
			if (machine.available) {
				card.on('click', () => {
					container.find('.machine-card').removeClass('selected');
					card.addClass('selected');
					this.selected_machine = machine.name;
					this.validate_booking();
				});
			}
			
			container.append(card);
		});
	}
	
	validate_booking() {
		const is_valid = this.patient && this.selected_date && 
			this.selected_time && this.selected_machine;
		
		this.wrapper.find('.btn-book').prop('disabled', !is_valid);
	}
	
	async book_appointment() {
		try {
			const response = await frappe.call({
				method: 'dialysis_center.api.appointment.book_appointment',
				args: {
					patient: this.patient,
					appointment_date: this.selected_date,
					appointment_time: this.selected_time,
					machine: this.selected_machine,
					location: this.selected_location
				}
			});
			
			if (response.message) {
				frappe.show_alert({
					message: __('Appointment booked successfully'),
					indicator: 'green'
				});
				
				frappe.set_route('Form', 'Appointment', response.message.name);
			}
		} catch (error) {
			frappe.show_alert({
				message: __('Failed to book appointment'),
				indicator: 'red'
			});
		}
	}
}
```


---

## 8. Clinical Workflow Interfaces

### 8.1 Session Recording Interface

**File: `dialysis_center/public/js/doctype/dialysis_session.js`**

```javascript
frappe.ui.form.on('Dialysis Session', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add action buttons based on status
			if (frm.doc.status === 'Scheduled') {
				frm.add_custom_button(__('Start Session'), function() {
					start_session(frm);
				}).addClass('btn-primary');
			}
			
			if (frm.doc.status === 'In Progress') {
				frm.add_custom_button(__('Record Vitals'), function() {
					show_vitals_dialog(frm);
				});
				
				frm.add_custom_button(__('Log Event'), function() {
					show_event_dialog(frm);
				});
				
				frm.add_custom_button(__('Complete Session'), function() {
					complete_session(frm);
				}).addClass('btn-success');
			}
			
			// Real-time session timer
			if (frm.doc.status === 'In Progress') {
				render_session_timer(frm);
			}
			
			// Vitals trend chart
			if (frm.doc.vitals_log && frm.doc.vitals_log.length > 0) {
				render_vitals_trend_chart(frm);
			}
		}
	},
	
	patient: function(frm) {
		if (frm.doc.patient) {
			load_patient_defaults(frm);
		}
	},
	
	machine: function(frm) {
		if (frm.doc.machine) {
			check_machine_availability(frm);
		}
	}
});

function start_session(frm) {
	frappe.confirm(
		__('Are you sure you want to start this dialysis session?'),
		function() {
			frappe.call({
				method: 'dialysis_center.api.session.start_session',
				args: {
					session_id: frm.doc.name
				},
				callback: function(r) {
					if (r.message) {
						frm.reload_doc();
						frappe.show_alert({
							message: __('Session started'),
							indicator: 'green'
						});
					}
				}
			});
		}
	);
}

function show_vitals_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Record Vital Signs'),
		fields: [
			{
				fieldtype: 'Time',
				fieldname: 'time',
				label: __('Time'),
				default: frappe.datetime.now_time(),
				reqd: 1
			},
			{
				fieldtype: 'Column Break'
			},
			{
				fieldtype: 'Data',
				fieldname: 'blood_pressure',
				label: __('Blood Pressure (mmHg)'),
				placeholder: '120/80',
				reqd: 1
			},
			{
				fieldtype: 'Int',
				fieldname: 'heart_rate',
				label: __('Heart Rate (bpm)'),
				reqd: 1
			},
			{
				fieldtype: 'Column Break'
			},
			{
				fieldtype: 'Float',
				fieldname: 'temperature',
				label: __('Temperature (°C)'),
				precision: 1
			},
			{
				fieldtype: 'Float',
				fieldname: 'weight',
				label: __('Weight (kg)'),
				precision: 2
			},
			{
				fieldtype: 'Section Break'
			},
			{
				fieldtype: 'Int',
				fieldname: 'blood_flow_rate',
				label: __('Blood Flow Rate (ml/min)')
			},
			{
				fieldtype: 'Int',
				fieldname: 'dialysate_flow_rate',
				label: __('Dialysate Flow Rate (ml/min)')
			},
			{
				fieldtype: 'Column Break'
			},
			{
				fieldtype: 'Float',
				fieldname: 'uf_removed',
				label: __('UF Removed (L)'),
				precision: 2
			},
			{
				fieldtype: 'Float',
				fieldname: 'venous_pressure',
				label: __('Venous Pressure (mmHg)'),
				precision: 1
			},
			{
				fieldtype: 'Section Break'
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'notes',
				label: __('Notes')
			}
		],
		primary_action_label: __('Save'),
		primary_action: function(values) {
			frappe.call({
				method: 'dialysis_center.api.session.record_vitals',
				args: {
					session_id: frm.doc.name,
					vitals: values
				},
				callback: function(r) {
					if (r.message) {
						frm.reload_doc();
						dialog.hide();
						frappe.show_alert({
							message: __('Vitals recorded'),
							indicator: 'green'
						});
					}
				}
			});
		}
	});
	
	dialog.show();
}

function show_event_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Log Session Event'),
		fields: [
			{
				fieldtype: 'Select',
				fieldname: 'event_type',
				label: __('Event Type'),
				options: [
					'Alarm',
					'Complication',
					'Medication Given',
					'Equipment Issue',
					'Patient Request',
					'Other'
				],
				reqd: 1
			},
			{
				fieldtype: 'Select',
				fieldname: 'severity',
				label: __('Severity'),
				options: ['Info', 'Warning', 'Critical'],
				default: 'Info'
			},
			{
				fieldtype: 'Section Break'
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'description',
				label: __('Description'),
				reqd: 1
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'action_taken',
				label: __('Action Taken')
			}
		],
		primary_action_label: __('Log Event'),
		primary_action: function(values) {
			frappe.call({
				method: 'dialysis_center.api.session.log_event',
				args: {
					session_id: frm.doc.name,
					event: values
				},
				callback: function(r) {
					if (r.message) {
						frm.reload_doc();
						dialog.hide();
					}
				}
			});
		}
	});
	
	dialog.show();
}

function complete_session(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Complete Session'),
		fields: [
			{
				fieldtype: 'Float',
				fieldname: 'total_uf_removed',
				label: __('Total UF Removed (L)'),
				reqd: 1,
				precision: 2
			},
			{
				fieldtype: 'Int',
				fieldname: 'actual_duration',
				label: __('Actual Duration (minutes)'),
				reqd: 1
			},
			{
				fieldtype: 'Column Break'
			},
			{
				fieldtype: 'Data',
				fieldname: 'final_bp',
				label: __('Final Blood Pressure'),
				reqd: 1
			},
			{
				fieldtype: 'Float',
				fieldname: 'post_dialysis_weight',
				label: __('Post-Dialysis Weight (kg)'),
				reqd: 1,
				precision: 2
			},
			{
				fieldtype: 'Section Break'
			},
			{
				fieldtype: 'Select',
				fieldname: 'session_outcome',
				label: __('Session Outcome'),
				options: [
					'Completed Successfully',
					'Completed with Issues',
					'Terminated Early'
				],
				default: 'Completed Successfully',
				reqd: 1
			},
			{
				fieldtype: 'Section Break'
			},
			{
				fieldtype: 'Small Text',
				fieldname: 'completion_notes',
				label: __('Completion Notes')
			}
		],
		primary_action_label: __('Complete'),
		primary_action: function(values) {
			frappe.call({
				method: 'dialysis_center.api.session.complete_session',
				args: {
					session_id: frm.doc.name,
					completion_data: values
				},
				freeze: true,
				freeze_message: __('Completing session...'),
				callback: function(r) {
					if (r.message) {
						frm.reload_doc();
						dialog.hide();
						frappe.show_alert({
							message: __('Session completed successfully'),
							indicator: 'green'
						});
					}
				}
			});
		}
	});
	
	dialog.show();
}

function render_session_timer(frm) {
	const wrapper = frm.fields_dict.session_timer_html.$wrapper;
	wrapper.empty();
	
	const start_time = new Date(frm.doc.actual_start_time);
	const target_duration = frm.doc.planned_duration * 60 * 1000; // Convert to milliseconds
	
	function update_timer() {
		const now = new Date();
		const elapsed = now - start_time;
		const elapsed_minutes = Math.floor(elapsed / 60000);
		const elapsed_seconds = Math.floor((elapsed % 60000) / 1000);
		const progress = (elapsed / target_duration) * 100;
		
		wrapper.html(`
			<div class="session-timer">
				<div class="timer-display">
					<div class="timer-label">Elapsed Time</div>
					<div class="timer-value">${elapsed_minutes}:${String(elapsed_seconds).padStart(2, '0')}</div>
					<div class="timer-target">Target: ${frm.doc.planned_duration} min</div>
				</div>
				<div class="timer-progress">
					<div class="progress-bar">
						<div class="progress-fill" style="width: ${Math.min(progress, 100)}%"></div>
					</div>
				</div>
			</div>
		`);
	}
	
	update_timer();
	setInterval(update_timer, 1000);
}

function render_vitals_trend_chart(frm) {
	const wrapper = frm.fields_dict.vitals_trend_html.$wrapper;
	wrapper.empty();
	
	const vitals = frm.doc.vitals_log;
	const labels = vitals.map(v => v.time);
	const systolic = vitals.map(v => parseInt(v.blood_pressure.split('/')[0]));
	const diastolic = vitals.map(v => parseInt(v.blood_pressure.split('/')[1]));
	const heart_rate = vitals.map(v => v.heart_rate);
	
	new frappe.Chart(wrapper[0], {
		title: 'Vital Signs During Session',
		data: {
			labels: labels,
			datasets: [
				{
					name: 'Systolic BP',
					values: systolic,
					chartType: 'line'
				},
				{
					name: 'Diastolic BP',
					values: diastolic,
					chartType: 'line'
				},
				{
					name: 'Heart Rate',
					values: heart_rate,
					chartType: 'line'
				}
			]
		},
		type: 'axis-mixed',
		height: 250,
		colors: ['#F44336', '#2196F3', '#4CAF50']
	});
}

function load_patient_defaults(frm) {
	frappe.call({
		method: 'dialysis_center.api.patient.get_treatment_defaults',
		args: {
			patient: frm.doc.patient
		},
		callback: function(r) {
			if (r.message) {
				frm.set_value('pre_dialysis_weight', r.message.last_post_weight);
				frm.set_value('dry_weight', r.message.dry_weight);
				frm.set_value('treatment_template', r.message.default_template);
			}
		}
	});
}
```

---

## 9. Mobile & Responsive Design

### 9.1 Responsive Breakpoints

```scss
// Responsive breakpoints
$breakpoint-xs: 480px;
$breakpoint-sm: 768px;
$breakpoint-md: 992px;
$breakpoint-lg: 1200px;
$breakpoint-xl: 1440px;

// Mixins for responsive design
@mixin respond-to($breakpoint) {
  @if $breakpoint == xs {
    @media (max-width: $breakpoint-xs) { @content; }
  }
  @else if $breakpoint == sm {
    @media (max-width: $breakpoint-sm) { @content; }
  }
  @else if $breakpoint == md {
    @media (max-width: $breakpoint-md) { @content; }
  }
  @else if $breakpoint == lg {
    @media (max-width: $breakpoint-lg) { @content; }
  }
  @else if $breakpoint == xl {
    @media (max-width: $breakpoint-xl) { @content; }
  }
}

// Example usage
.dashboard-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 24px;
  
  @include respond-to(md) {
    grid-template-columns: 1fr;
  }
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  
  @include respond-to(lg) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @include respond-to(sm) {
    grid-template-columns: 1fr;
  }
}
```

### 9.2 Mobile-First Components

```scss
// Mobile-optimized session card
.session-card {
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 16px;
  
  // Desktop view
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: center;
  
  // Mobile view
  @include respond-to(sm) {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .session-info {
    @include respond-to(sm) {
      order: 1;
    }
  }
  
  .session-vitals {
    @include respond-to(sm) {
      order: 2;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }
  }
  
  .session-actions {
    @include respond-to(sm) {
      order: 3;
      display: flex;
      gap: 8px;
      
      .btn {
        flex: 1;
        font-size: 0.875rem;
      }
    }
  }
}
```

---

## 10. State Management

### 10.1 Simple State Store

**File: `dialysis_center/public/js/store/index.js`**

```javascript
class Store {
	constructor() {
		this.state = {
			currentUser: null,
			currentLocation: null,
			activeSessions: [],
			notifications: [],
			preferences: {}
		};
		
		this.listeners = {};
		
		this.init();
	}
	
	init() {
		// Load user preferences from localStorage
		const savedPrefs = localStorage.getItem('dialysis_center_preferences');
		if (savedPrefs) {
			this.state.preferences = JSON.parse(savedPrefs);
		}
		
		// Load current user
		this.state.currentUser = frappe.session.user;
		
		// Subscribe to real-time updates
		this.subscribeToRealtime();
	}
	
	// Get state
	getState(key) {
		if (key) {
			return this.state[key];
		}
		return this.state;
	}
	
	// Set state
	setState(key, value) {
		this.state[key] = value;
		this.notify(key, value);
		
		// Save preferences to localStorage
		if (key === 'preferences') {
			localStorage.setItem('dialysis_center_preferences', JSON.stringify(value));
		}
	}
	
	// Subscribe to state changes
	subscribe(key, callback) {
		if (!this.listeners[key]) {
			this.listeners[key] = [];
		}
		this.listeners[key].push(callback);
		
		// Return unsubscribe function
		return () => {
			this.listeners[key] = this.listeners[key].filter(cb => cb !== callback);
		};
	}
	
	// Notify listeners
	notify(key, value) {
		if (this.listeners[key]) {
			this.listeners[key].forEach(callback => callback(value));
		}
	}
	
	// Subscribe to real-time updates
	subscribeToRealtime() {
		// Session updates
		frappe.realtime.on('session_updated', (data) => {
			this.updateActiveSessions(data);
		});
		
		// Notifications
		frappe.realtime.on('notification', (data) => {
			this.addNotification(data);
		});
		
		// Alerts
		frappe.realtime.on('alert', (data) => {
			this.showAlert(data);
		});
	}
	
	// Update active sessions
	updateActiveSessions(sessionData) {
		let sessions = this.state.activeSessions;
		const index = sessions.findIndex(s => s.name === sessionData.name);
		
		if (index >= 0) {
			sessions[index] = { ...sessions[index], ...sessionData };
		} else {
			sessions.push(sessionData);
		}
		
		this.setState('activeSessions', sessions);
	}
	
	// Add notification
	addNotification(notification) {
		const notifications = [notification, ...this.state.notifications];
		this.setState('notifications', notifications.slice(0, 50)); // Keep last 50
	}
	
	// Show alert
	showAlert(alert) {
		frappe.show_alert({
			message: alert.message,
			indicator: alert.severity === 'critical' ? 'red' : 'orange'
		});
		
		// Play sound for critical alerts
		if (alert.severity === 'critical') {
			this.playAlertSound();
		}
	}
	
	// Play alert sound
	playAlertSound() {
		const audio = new Audio('/assets/dialysis_center/sounds/alert.mp3');
		audio.play().catch(err => console.log('Could not play sound:', err));
	}
	
	// Preferences
	setPreference(key, value) {
		const prefs = { ...this.state.preferences, [key]: value };
		this.setState('preferences', prefs);
	}
	
	getPreference(key, defaultValue = null) {
		return this.state.preferences[key] || defaultValue;
	}
}

// Export singleton instance
window.dialysisStore = new Store();
```


---

## 11. API Integration

### 11.1 API Helper Functions

**File: `dialysis_center/public/js/utils/api.js`**

```javascript
export const api = {
	// Generic API call wrapper
	call: async function(method, args = {}) {
		try {
			const response = await frappe.call({
				method: method,
				args: args,
				freeze: true
			});
			return response.message;
		} catch (error) {
			console.error('API Error:', error);
			frappe.show_alert({
				message: error.message || 'An error occurred',
				indicator: 'red'
			});
			throw error;
		}
	},
	
	// Patient API
	patient: {
		get: (patient_id) => api.call('dialysis_center.api.patient.get_patient', { patient_id }),
		search: (query) => api.call('dialysis_center.api.patient.search_patients', { query }),
		getVitalsTrend: (patient_id, days) => api.call('dialysis_center.api.patient.get_vitals_trend', { patient: patient_id, days }),
		getUpcomingAppointments: (patient_id) => api.call('dialysis_center.api.patient.get_upcoming_appointments', { patient: patient_id })
	},
	
	// Appointment API
	appointment: {
		checkAvailability: (date, shift, location) => api.call('dialysis_center.api.appointment.check_availability', { date, shift, location }),
		book: (data) => api.call('dialysis_center.api.appointment.book_appointment', data),
		reschedule: (appointment_id, new_date, new_time) => api.call('dialysis_center.api.appointment.reschedule', { appointment_id, new_date, new_time }),
		cancel: (appointment_id, reason) => api.call('dialysis_center.api.appointment.cancel_appointment', { appointment_id, reason }),
		checkIn: (appointment_id) => api.call('dialysis_center.api.appointment.check_in', { appointment_id })
	},
	
	// Session API
	session: {
		getActive: (location) => api.call('dialysis_center.api.session.get_active_sessions', { location }),
		start: (session_id) => api.call('dialysis_center.api.session.start_session', { session_id }),
		recordVitals: (session_id, vitals) => api.call('dialysis_center.api.session.record_vitals', { session_id, vitals }),
		logEvent: (session_id, event) => api.call('dialysis_center.api.session.log_event', { session_id, event }),
		complete: (session_id, completion_data) => api.call('dialysis_center.api.session.complete_session', { session_id, completion_data })
	},
	
	// Dashboard API
	dashboard: {
		getSessionDashboard: (filters) => api.call('dialysis_center.api.dashboard.get_session_dashboard_data', filters),
		getMetrics: (date, location) => api.call('dialysis_center.api.dashboard.get_metrics', { date, location })
	},
	
	// Inventory API
	inventory: {
		getStock: (item_code, location) => api.call('dialysis_center.api.inventory.get_stock_level', { item_code, location }),
		checkAvailability: (items) => api.call('dialysis_center.api.inventory.check_availability', { items }),
		issueStock: (session_id, items) => api.call('dialysis_center.api.inventory.issue_stock', { session_id, items })
	},
	
	// Reports API
	reports: {
		getPatientList: (filters) => api.call('dialysis_center.api.reports.get_patient_list', filters),
		getSessionSummary: (filters) => api.call('dialysis_center.api.reports.get_session_summary', filters),
		getFinancialReport: (filters) => api.call('dialysis_center.api.reports.get_financial_report', filters)
	}
};

// Export for use in other modules
window.dialysisAPI = api;
```

---

## 12. Performance Optimization

### 12.1 Code Splitting

```javascript
// Lazy load components
const SessionMonitor = () => import('./components/SessionMonitor.vue');
const AppointmentCalendar = () => import('./components/AppointmentCalendar.vue');
const VitalsChart = () => import('./components/VitalsChart.vue');

// Use in Vue
export default {
	components: {
		SessionMonitor,
		AppointmentCalendar,
		VitalsChart
	}
};
```

### 12.2 Caching Strategy

```javascript
class CacheManager {
	constructor() {
		this.cache = new Map();
		this.ttl = 5 * 60 * 1000; // 5 minutes
	}
	
	set(key, value, ttl = this.ttl) {
		this.cache.set(key, {
			value: value,
			expires: Date.now() + ttl
		});
	}
	
	get(key) {
		const item = this.cache.get(key);
		if (!item) return null;
		
		if (Date.now() > item.expires) {
			this.cache.delete(key);
			return null;
		}
		
		return item.value;
	}
	
	clear() {
		this.cache.clear();
	}
	
	// Cache with automatic fetch
	async fetch(key, fetchFn, ttl) {
		const cached = this.get(key);
		if (cached) return cached;
		
		const data = await fetchFn();
		this.set(key, data, ttl);
		return data;
	}
}

window.cacheManager = new CacheManager();
```

### 12.3 Debouncing & Throttling

```javascript
// Debounce function
function debounce(func, wait) {
	let timeout;
	return function executedFunction(...args) {
		const later = () => {
			clearTimeout(timeout);
			func(...args);
		};
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
	};
}

// Throttle function
function throttle(func, limit) {
	let inThrottle;
	return function(...args) {
		if (!inThrottle) {
			func.apply(this, args);
			inThrottle = true;
			setTimeout(() => inThrottle = false, limit);
		}
	};
}

// Usage example
const searchPatients = debounce(async (query) => {
	const results = await api.patient.search(query);
	renderResults(results);
}, 300);

const handleScroll = throttle(() => {
	// Handle scroll event
}, 100);
```

---

## 13. Accessibility (WCAG 2.1)

### 13.1 Keyboard Navigation

```javascript
// Ensure all interactive elements are keyboard accessible
document.addEventListener('keydown', (e) => {
	// ESC to close dialogs
	if (e.key === 'Escape') {
		frappe.ui.Dialog.prototype.hide();
	}
	
	// Ctrl+S to save
	if (e.ctrlKey && e.key === 's') {
		e.preventDefault();
		cur_frm && cur_frm.save();
	}
	
	// Ctrl+N for new
	if (e.ctrlKey && e.key === 'n') {
		e.preventDefault();
		// Create new document
	}
});

// Tab trap for modals
function trapFocus(element) {
	const focusableElements = element.querySelectorAll(
		'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
	);
	const firstElement = focusableElements[0];
	const lastElement = focusableElements[focusableElements.length - 1];
	
	element.addEventListener('keydown', function(e) {
		if (e.key === 'Tab') {
			if (e.shiftKey && document.activeElement === firstElement) {
				e.preventDefault();
				lastElement.focus();
			} else if (!e.shiftKey && document.activeElement === lastElement) {
				e.preventDefault();
				firstElement.focus();
			}
		}
	});
}
```

### 13.2 ARIA Labels

```html
<!-- Accessible buttons -->
<button 
  aria-label="Start dialysis session"
  aria-describedby="session-help-text">
  <i class="fa fa-play" aria-hidden="true"></i>
  Start
</button>

<!-- Accessible form fields -->
<div class="form-group">
  <label for="patient-search" id="patient-label">
    Patient Search
  </label>
  <input 
    id="patient-search"
    type="text"
    aria-labelledby="patient-label"
    aria-required="true"
    aria-invalid="false"
    aria-describedby="patient-help">
  <span id="patient-help" class="help-text">
    Search by name or ID
  </span>
</div>

<!-- Accessible alerts -->
<div 
  role="alert"
  aria-live="assertive"
  aria-atomic="true"
  class="alert alert-danger">
  Critical: Patient blood pressure is abnormal
</div>

<!-- Accessible data table -->
<table role="grid" aria-label="Active Sessions">
  <thead>
    <tr role="row">
      <th role="columnheader" scope="col">Patient</th>
      <th role="columnheader" scope="col">Machine</th>
      <th role="columnheader" scope="col">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr role="row">
      <td role="gridcell">John Doe</td>
      <td role="gridcell">Machine 01</td>
      <td role="gridcell">Active</td>
    </tr>
  </tbody>
</table>
```

### 13.3 Color Contrast

```scss
// Ensure WCAG AA compliance (4.5:1 for normal text, 3:1 for large text)
.btn-primary {
  background-color: #2490EF; // Contrast ratio: 4.52:1 on white
  color: #FFFFFF;
  
  &:hover {
    background-color: #1976D2; // Increased contrast
  }
}

.alert-danger {
  background-color: #FFF3F3;
  border-color: #DC3545;
  color: #721c24; // Contrast ratio: 8.59:1
}

// Use both color and icons
.status-indicator {
  &.active {
    color: #155724;
    &::before {
      content: "✓ "; // Icon + color
    }
  }
  
  &.error {
    color: #721c24;
    &::before {
      content: "⚠ "; // Icon + color
    }
  }
}
```

---

## 14. Testing Strategy

### 14.1 Unit Tests (Jest)

```javascript
// tests/unit/validators.test.js
import { validators } from '@/utils/validators';

describe('Validators', () => {
	describe('validateBloodPressure', () => {
		test('accepts valid blood pressure', () => {
			expect(validators.validateBloodPressure('120/80')).toBe(true);
			expect(validators.validateBloodPressure('140/90')).toBe(true);
		});
		
		test('rejects invalid format', () => {
			expect(validators.validateBloodPressure('120')).toMatch(/Invalid format/);
			expect(validators.validateBloodPressure('120-80')).toMatch(/Invalid format/);
		});
		
		test('rejects out of range values', () => {
			expect(validators.validateBloodPressure('300/80')).toMatch(/Systolic/);
			expect(validators.validateBloodPressure('120/200')).toMatch(/Diastolic/);
		});
	});
	
	describe('validateTemperature', () => {
		test('accepts valid temperature', () => {
			expect(validators.validateTemperature('37.5')).toBe(true);
			expect(validators.validateTemperature('36.0')).toBe(true);
		});
		
		test('rejects out of range', () => {
			expect(validators.validateTemperature('50')).toMatch(/between 35/);
		});
	});
});
```

### 14.2 Component Tests (Vue Test Utils)

```javascript
// tests/unit/PatientCard.spec.js
import { mount } from '@vue/test-utils';
import PatientCard from '@/components/PatientCard.vue';

describe('PatientCard.vue', () => {
	const mockPatient = {
		name: 'PT-2026-00001',
		patient_name: 'John Doe',
		age: 45,
		blood_group: 'O+',
		dialysis_type: 'Hemodialysis',
		next_session: '2026-02-20',
		status: 'Active'
	};
	
	test('renders patient information', () => {
		const wrapper = mount(PatientCard, {
			props: { patient: mockPatient }
		});
		
		expect(wrapper.text()).toContain('John Doe');
		expect(wrapper.text()).toContain('PT-2026-00001');
		expect(wrapper.text()).toContain('45 years');
	});
	
	test('displays initials correctly', () => {
		const wrapper = mount(PatientCard, {
			props: { patient: mockPatient }
		});
		
		expect(wrapper.find('.patient-avatar').text()).toBe('JD');
	});
	
	test('emits click event', async () => {
		const wrapper = mount(PatientCard, {
			props: { patient: mockPatient }
		});
		
		await wrapper.trigger('click');
		
		expect(wrapper.emitted()).toHaveProperty('click');
		expect(wrapper.emitted().click[0]).toEqual([mockPatient]);
	});
	
	test('applies correct status class', () => {
		const wrapper = mount(PatientCard, {
			props: { patient: mockPatient }
		});
		
		const badge = wrapper.find('.status-badge');
		expect(badge.classes()).toContain('active');
	});
});
```

### 14.3 Integration Tests (Cypress)

```javascript
// cypress/integration/session_workflow.spec.js
describe('Session Workflow', () => {
	beforeEach(() => {
		cy.login('Administrator', 'admin@123');
		cy.visit('/app/session-dashboard');
	});
	
	it('starts a new session', () => {
		// Click new session button
		cy.contains('New Session').click();
		
		// Fill session form
		cy.fill_field('patient', 'PT-2026-00001');
		cy.fill_field('machine', 'Machine 01');
		cy.fill_field('planned_duration', '240');
		
		// Save
		cy.click_button('Save');
		
		// Start session
		cy.contains('Start Session').click();
		cy.contains('Yes').click();
		
		// Verify status
		cy.get('.indicator').should('contain', 'In Progress');
	});
	
	it('records vitals during session', () => {
		cy.visit('/app/dialysis-session/DS-2026-00001');
		
		// Click record vitals
		cy.contains('Record Vitals').click();
		
		// Fill vitals
		cy.fill_field('blood_pressure', '120/80');
		cy.fill_field('heart_rate', '75');
		cy.fill_field('temperature', '37.0');
		
		// Save
		cy.contains('Save').click();
		
		// Verify vitals recorded
		cy.get('.vitals-log').should('contain', '120/80');
	});
	
	it('completes a session', () => {
		cy.visit('/app/dialysis-session/DS-2026-00001');
		
		// Click complete
		cy.contains('Complete Session').click();
		
		// Fill completion data
		cy.fill_field('total_uf_removed', '2.5');
		cy.fill_field('actual_duration', '240');
		cy.fill_field('final_bp', '110/70');
		cy.fill_field('post_dialysis_weight', '68.5');
		
		// Complete
		cy.contains('Complete').click();
		
		// Verify completed
		cy.get('.indicator').should('contain', 'Completed');
	});
});
```

---

## 15. Build & Deployment

### 15.1 Build Configuration

**File: `dialysis_center/esbuild/config.js`**

```javascript
module.exports = {
	entryPoints: [
		'dialysis_center/public/js/dialysis_center.bundle.js',
		'dialysis_center/public/css/dialysis_center.bundle.scss'
	],
	outdir: 'dialysis_center/public/dist',
	bundle: true,
	minify: process.env.NODE_ENV === 'production',
	sourcemap: process.env.NODE_ENV !== 'production',
	target: ['es2020'],
	loader: {
		'.vue': 'js',
		'.scss': 'css',
		'.png': 'file',
		'.svg': 'file',
		'.jpg': 'file'
	},
	plugins: [
		// Vue plugin
		require('esbuild-plugin-vue3')(),
		// SCSS plugin
		require('esbuild-plugin-sass')()
	]
};
```

### 15.2 Production Build

```bash
# Build for production
cd frappe-bench/apps/dialysis_center
yarn build

# Or using bench
bench build --app dialysis_center --production

# Minify and optimize
bench build --app dialysis_center --production --minify
```

### 15.3 Asset Optimization

```javascript
// Image optimization
const sharp = require('sharp');

async function optimizeImages() {
	const images = await glob('dialysis_center/public/images/**/*.{jpg,png}');
	
	for (const image of images) {
		await sharp(image)
			.resize(1920, 1080, { fit: 'inside', withoutEnlargement: true })
			.jpeg({ quality: 80, progressive: true })
			.toFile(image.replace(/\.\w+$/, '.optimized.jpg'));
	}
}
```

### 15.4 Performance Checklist

- [ ] Enable gzip/brotli compression
- [ ] Implement lazy loading for images
- [ ] Code splitting for large components
- [ ] Tree shaking unused code
- [ ] Minify CSS and JavaScript
- [ ] Optimize images (WebP, compression)
- [ ] Implement service worker for caching
- [ ] Use CDN for static assets
- [ ] Enable browser caching headers
- [ ] Monitor bundle size (<500KB initial load)
- [ ] Lighthouse score >90
- [ ] First Contentful Paint <2s
- [ ] Time to Interactive <5s

---

## Appendix: Style Guide

### Component Naming
- **PascalCase** for Vue components: `SessionMonitor.vue`
- **kebab-case** for HTML/CSS: `session-monitor`
- **camelCase** for JavaScript: `sessionMonitor`

### File Organization
```
dialysis_center/
├── public/
│   ├── js/
│   │   ├── components/       # Reusable Vue components
│   │   ├── pages/           # Page-specific code
│   │   ├── doctype/         # DocType controllers
│   │   ├── utils/           # Utility functions
│   │   └── store/           # State management
│   ├── css/
│   │   ├── components/      # Component styles
│   │   ├── pages/          # Page styles
│   │   └── utils/          # Mixins, variables
│   └── images/
│       ├── icons/          # SVG icons
│       └── illustrations/  # UI illustrations
```

### Code Comments
```javascript
/**
 * Records patient vital signs during dialysis session
 * @param {string} sessionId - Dialysis session ID
 * @param {Object} vitals - Vital signs data
 * @param {string} vitals.blood_pressure - BP in format "120/80"
 * @param {number} vitals.heart_rate - Heart rate in bpm
 * @param {number} vitals.temperature - Temperature in Celsius
 * @returns {Promise<Object>} Updated session data
 */
async function recordVitals(sessionId, vitals) {
	// Implementation
}
```

---

**End of Frontend Design & Implementation Guide**

**Last Updated:** 2026-02-19  
**Version:** 1.0.0  
**Total Pages:** 45+ sections covering complete frontend implementation

