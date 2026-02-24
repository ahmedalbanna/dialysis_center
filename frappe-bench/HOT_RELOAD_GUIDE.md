# Hot-Reload Development Guide

## Overview

The Dialysis Center application now supports **instant hot-reload** during development. Changes to your code are automatically compiled and reflected in the browser without manual page reloads, significantly speeding up the development workflow.

### What is Hot-Reload?

Hot-reload enables you to:
- **See changes instantly** - No need to manually refresh the page
- **Preserve application state** - Form data and navigation state are maintained (for CSS changes)
- **Get immediate feedback** - Build errors appear in the browser console
- **Iterate faster** - 10x faster development cycle

---

## Quick Start

### 1. Start the Development Server

```bash
cd frappe-bench
bench start
```

This will start all necessary services including:
- **web** - Frappe web server (port 8000)
- **watch** - Asset watcher with live-reload enabled (monitoring for file changes)
- **socketio** - Real-time communication via Socket.IO
- **redis_cache** - Cache layer
- **redis_queue** - Job queue
- **scheduler** - Background task scheduler
- **worker** - Background job worker

### 2. Open Your Browser

Navigate to your development site:
```
http://127.0.0.1:8000
```

Login with your default credentials:
- **Username**: Administrator
- **Password**: admin@123

### 3. Make Changes and Watch Them Appear

Edit any of these files and see changes instantly:

**JavaScript/Vue Components:**
```javascript
// apps/dialysis_center/dialysis_center/public/js/patient.js
// Page reloads automatically when changed
```

**CSS/SCSS Files:**
```scss
// apps/dialysis_center/dialysis_center/public/css/dialysis_center.css
// CSS updates dynamically without page reload (state preserved!)
```

**Python Backend:**
```python
# dialysis_center/api/patient.py
# Changes require page reload, but hot-reload detects and reloads
```

---

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Browser                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  hot-reload.js - Listens for build events       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────┬───────────────────────────────────────────────┘
          │ Socket.IO connection
          ▼
┌─────────────────────────────────────────────────────────┐
│                  Frappe Backend                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Socket.IO Server - Broadcasts build events     │  │
│  └──────────────────────────────────────────────────┘  │
          ▲ publishes to
          │
┌─────────┴───────────────────────────────────────────────┐
│                  Redis Queue                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Receives build events from esbuild             │  │
│  └──────────────────────────────────────────────────┘  │
          ▲ publishes to
          │
┌─────────┴───────────────────────────────────────────────┐
│                  esbuild Watch                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Detects file changes & compiles assets         │  │
│  │  Command: bench watch --live-reload             │  │
│  └──────────────────────────────────────────────────┘  │
          ▲ watches
          │
          ▼
     Your Source Files
```

### Flow

1. **You edit a file** (JS, CSS, Python)
2. **esbuild watch detects change** and recompiles
3. **esbuild publishes build event** to Redis
4. **Socket.IO broadcasts event** to all connected browsers
5. **hot-reload.js receives event** in your browser
6. **Smart reload strategy**:
   - **CSS files only**: Update stylesheets dynamically (no page reload)
   - **JS files**: Full page reload (safest approach)
   - **Python files**: Full page reload

---

## Features

### ✅ CSS Hot-Update

When you modify CSS/SCSS files, the stylesheets are updated dynamically without a page reload:

```scss
/* Change this... */
.patient-card {
  background-color: white;
}

/* And see it instantly, form data preserved! */
.patient-card {
  background-color: #f5f5f5;
}
```

**Benefits:**
- ⚡ Instant visual feedback
- 💾 Form data preserved
- 🚀 No navigation state loss

### ⚡ Smart JavaScript Reload

When you modify JavaScript files, the entire page reloads to pick up the changes safely:

```javascript
// Modify this...
frappe.ui.form.on('Patient', {
  refresh(frm) {
    console.log("Patient loaded");
  }
});

// Page automatically reloads to apply changes
```

### 🐛 Error Handling

Build errors are displayed in your browser console with formatted error messages:

```javascript
// Syntax error example
const obj = {
  name: "Patient"  // Missing comma
  age: 30
};

// Output in console:
// [Hot-Reload] Build Error: Unexpected token
// Check console for details
```

### 📝 Unsaved Changes Protection

If you have unsaved form data, hot-reload will **skip the reload** to protect your changes:

```
⚠️  [Hot-Reload] Unsaved changes detected in: Patient
    Save changes to reload
```

---

## Configuration

### Enabling/Disabling Hot-Reload

Hot-reload is **enabled by default** in development mode.

**In `site_config.json`:**
```json
{
  "developer_mode": 1,
  "disable_hot_reload": 0
}
```

To disable hot-reload:
```json
{
  "disable_hot_reload": 1
}
```

### Watch Command

The watch command is configured in `Procfile`:

```procfile
watch: bash -c "source ~/.nvm/nvm.sh && bench watch --live-reload"
```

The `--live-reload` flag enables the feature. Remove it to disable:

```procfile
watch: bash -c "source ~/.nvm/nvm.sh && bench watch"
```

---

## Troubleshooting

### Hot-Reload Not Working?

**Issue**: Changes are not appearing in the browser

**Solutions**:
1. **Check watch process is running**:
   ```bash
   ps aux | grep "bench watch"
   ```
   
2. **Verify Socket.IO connection**:
   - Open browser console (F12)
   - Check if `frappe.realtime` is available:
     ```javascript
     console.log(frappe.realtime);
     ```

3. **Restart services**:
   ```bash
   cd frappe-bench
   bench restart
   ```

4. **Clear browser cache**:
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

### Build Errors Appearing?

**Issue**: Changes caused a build error

**Solution**:
1. Check the console error message
2. Fix the syntax error in your code
3. Save the file
4. esbuild will automatically retry the build

### Page Keeps Reloading?

**Issue**: Page reloads repeatedly

**Solution**:
1. Check for infinite loops in your JavaScript
2. Look for circular imports
3. Check for files being modified by other processes
4. Restart the watch process:
   ```bash
   # Stop with Ctrl+C, then restart
   bench start
   ```

### Socket.IO Connection Failed?

**Issue**: Console shows "Cannot connect to redis_queue"

**Solution**:
1. Verify Redis is running:
   ```bash
   ps aux | grep redis
   ```

2. Check Redis configuration:
   ```bash
   cd frappe-bench
   redis-cli ping
   ```
   Should output: `PONG`

3. Restart Redis:
   ```bash
   bench restart
   ```

---

## Development Workflow Tips

### 1. Multiple File Types

When editing multiple types of files, hot-reload intelligently handles them:

```
Edit CSS              → Instant CSS update (state preserved)
Edit JS               → Page reloads
Edit Python + JS      → Page reloads (JS changes take precedence)
```

### 2. Working with Forms

When developing form controllers:

```javascript
// apps/dialysis_center/dialysis_center/public/js/patient.js
frappe.ui.form.on('Patient', {
  refresh(frm) {
    // Changes to this will trigger page reload
    this.setup_filters();
  },
  
  setup_filters() {
    // New methods are picked up on page reload
  }
});
```

**Workflow:**
1. Edit the JavaScript
2. Browser automatically reloads
3. Form refreshes with new logic
4. Test the change

### 3. CSS/Theme Development

When styling forms and pages:

```scss
// apps/dialysis_center/dialysis_center/public/css/dialysis_center.css
.patient-form {
  .form-section {
    background: white;
    border-radius: 4px;
  }
}
```

**Workflow:**
1. Edit the SCSS
2. See changes instantly (no reload)
3. Form data stays intact
4. Adjust styling in real-time

### 4. API Development

When modifying API endpoints:

```python
# dialysis_center/api/patient.py
@frappe.whitelist()
def get_patient_details(patient_id):
    # Changes here require page reload to take effect
    patient = frappe.get_doc("Patient", patient_id)
    return patient.as_dict()
```

**Workflow:**
1. Edit the Python code
2. Save the file
3. Browser reloads and picks up new endpoint
4. Test the updated API

---

## Console Debugging

### Check Hot-Reload Status

In your browser console:

```javascript
// View hot-reload status
console.log(window.__frappe_hot_reload__);

// Output example:
// {
//   enabled: true,
//   isReloading: false,
//   lastBuildTime: 1703001234567,
//   ...
// }
```

### View Build Events

Watch for build events in the console:

```javascript
// Log showing successful CSS compilation
[Hot-Reload 14:32:45] Updated stylesheet: /assets/dialysis_center/css/dialysis_center.css
[Hot-Reload 14:32:45] CSS updated (1 file)
```

### Check Socket.IO Connection

```javascript
// Verify Socket.IO is connected
frappe.realtime.on("connect", () => {
  console.log("Socket.IO connected for hot-reload");
});
```

---

## Performance Considerations

### Build Times

Typical rebuild times for different file types:

| File Type | Rebuild Time | Impact |
|-----------|-------------|--------|
| CSS/SCSS | 500-1000ms | Hot-update (no reload) |
| JavaScript | 1-2 sec | Full page reload |
| Python | 100-200ms | Watch detects, reload on next change |

### Debouncing

Hot-reload includes a 300ms debounce to prevent rapid consecutive reloads:

```javascript
// If you save a file multiple times quickly,
// only one reload happens
debounceDelay: 300; // ms
```

---

## Best Practices

### ✅ Do:
- Use hot-reload for rapid iteration on UI
- Develop CSS/styling with instant feedback
- Test form logic with hot-reload
- Check console for build errors before testing

### ❌ Don't:
- Rely on hot-reload for Python API changes (always verify in Postman/curl)
- Forget to save files (hot-reload only works on saved files)
- Make complex changes without testing (reload might lose state)
- Leave sensitive operations in refresh handlers

---

## Advanced Configuration

### Custom Reload Debounce

Edit `frappe/public/js/hot-reload.js` to adjust debounce:

```javascript
debounceDelay: 300, // Change this value (ms)
```

Lower = faster reloads, higher = prevents rapid reloads

### Disable for Specific Assets

To exclude certain files from hot-reload, edit esbuild configuration:

```bash
# In apps/frappe/esbuild/esbuild.js, add to ignore patterns
```

### Environment Variables

Control hot-reload via environment:

```bash
# Disable hot-reload globally
export FRAPPE_DISABLE_HOT_RELOAD=1
bench watch
```

---

## Summary

| Feature | Benefit |
|---------|---------|
| **Instant CSS updates** | See styling changes without page reload |
| **Automatic JS reload** | Pick up JavaScript changes immediately |
| **Smart refresh logic** | Only reload when necessary |
| **Error handling** | Build errors shown in console |
| **State preservation** | Form data preserved on CSS changes |
| **Production safe** | Disabled automatically in production |

---

## Getting Help

If you encounter issues:

1. **Check the browser console** (`F12` → Console tab)
2. **Review esbuild logs** in the terminal
3. **Verify all services running**: `bench status`
4. **Restart services**: `bench restart`
5. **Hard refresh browser**: `Ctrl+Shift+R`

---

## Next Steps

Now that hot-reload is configured:

1. ✅ **Start developing** - Edit files and see changes instantly
2. ✅ **Monitor console** - Watch for build messages
3. ✅ **Test thoroughly** - Use hot-reload to iterate quickly
4. ✅ **Optimize workflow** - Use keyboard shortcuts for faster editing

Happy developing! 🚀
