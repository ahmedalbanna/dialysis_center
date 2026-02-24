# Hot-Reload Quick Reference Card

## 🚀 Getting Started (30 seconds)

```bash
cd frappe-bench
bench start
# → Open http://127.0.0.1:8000
# → Press F12 to open console
# → Edit a file and watch it change!
```

---

## ⚡ What You Can Edit (and what happens)

| File Type | Location | Result | State |
|-----------|----------|--------|-------|
| **CSS/SCSS** | `public/css/*.css` | 🔄 Hot-update (no reload) | ✅ Preserved |
| **JavaScript** | `public/js/*.js` | 🔁 Page reloads | ✅ Mostly preserved |
| **Vue** | `public/components/*.vue` | 🔁 Page reloads | ✅ Mostly preserved |
| **Python** | `api/*.py` | 🔁 Page reloads | ✅ Mostly preserved |
| **HTML** | `templates/*.html` | 🔁 Page reloads | ✅ Mostly preserved |

---

## 📊 Expected Times

```
CSS change    : 500-1000ms to see in browser
JS change     : 1-2 seconds for reload
Python change : 100-200ms rebuild + page reload
```

---

## 🔍 Console Messages

```javascript
// ✅ SUCCESS
[Hot-Reload 14:32:45] CSS updated (1 file)
[Hot-Reload 14:32:45] Reloading...

// ⚠️ WARNING
[Hot-Reload] Unsaved changes detected in: Patient
Save changes to reload

// ❌ ERROR
[Hot-Reload] Build Error: Unexpected token
// Check console for details
```

---

## 🛠️ Troubleshooting (5 minutes)

### Not seeing changes?
```bash
# 1. Hard refresh browser
Ctrl+Shift+R  (Windows)
Cmd+Shift+R   (Mac)

# 2. Check watch is running
ps aux | grep "bench watch"

# 3. Verify configuration
cd frappe-bench && ./VERIFY_HOT_RELOAD.sh
```

### Errors appearing?
```bash
# Check browser console (F12)
# Fix the syntax error
# Save file again
# esbuild will retry automatically
```

### Page keeps reloading?
```bash
# Check for infinite loops in your code
# Restart services
bench restart
```

---

## 🎯 Best Practices

✅ **DO:**
- Use hot-reload for rapid iteration
- Check console for build messages
- Save often to trigger rebuilds
- Use browser DevTools (F12)

❌ **DON'T:**
- Make changes without saving
- Ignore build error messages
- Change multiple file types simultaneously
- Close the watch process

---

## 📝 File Locations

```
frappe-bench/
├── apps/frappe/frappe/public/
│   ├── js/          ← Edit JavaScript here
│   └── css/         ← Edit CSS/SCSS here
│
└── apps/dialysis_center/dialysis_center/public/
    ├── js/          ← Edit app JavaScript
    └── css/         ← Edit app CSS/SCSS
```

---

## 🔗 Console Commands

```javascript
// Check hot-reload status
window.__frappe_hot_reload__

// View if socket connected
frappe.realtime

// Manual page reload
location.reload()

// Clear browser cache
// Ctrl+Shift+Delete → Clear browsing data
```

---

## 📖 Full Documentation

- **Complete Guide**: `HOT_RELOAD_GUIDE.md`
- **Implementation Details**: `HOT_RELOAD_IMPLEMENTATION_SUMMARY.md`
- **Verification Script**: `./VERIFY_HOT_RELOAD.sh`

---

## ❓ Quick FAQ

**Q: Why did my page reload?**
A: You edited JavaScript or Python. CSS edits don't reload.

**Q: Form data disappeared?**
A: Page reloaded. Save your form before major edits.

**Q: No changes showing?**
A: Save your file, check console for errors, hard refresh browser.

**Q: How do I disable hot-reload?**
A: Remove `--live-reload` from `Procfile` or set `disable_hot_reload: 1` in site config.

**Q: Does it work in production?**
A: No, hot-reload is disabled in production automatically.

---

## 🆘 Need Help?

1. **Check console**: F12 → Console tab
2. **Run verification**: `./VERIFY_HOT_RELOAD.sh`
3. **Read guide**: `HOT_RELOAD_GUIDE.md`
4. **Restart**: `bench restart`
5. **Build**: `bench build`

---

## ✨ Key Features

🔄 **Instant Updates** - See changes in milliseconds  
💾 **State Preserved** - CSS updates don't lose form data  
🛡️ **Safe Reloads** - Unsaved changes are protected  
📱 **Multi-Browser** - Works across all modern browsers  
⚡ **Production Ready** - Auto-disabled in production  

---

**Last Updated**: 2026-02-19  
**Status**: ✅ Ready for Development
