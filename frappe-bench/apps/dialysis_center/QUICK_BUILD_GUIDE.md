# Dialysis Center Frontend - Quick Build Guide

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (1 minute)

```bash
cd frappe-bench/apps/dialysis_center
npm install
```

Expected output:
```
added 15 packages in 30s
```

---

### Step 2: Build Assets (2 minutes)

```bash
npm run build
```

OR using bench:

```bash
cd frappe-bench
bench build --app dialysis_center
```

Expected output:
```
🔨 Building Dialysis Center frontend...
✅ Build complete!
```

---

### Step 3: Verify (1 minute)

```bash
# Clear cache
bench clear-cache

# Restart server (if running)
bench restart
```

Open browser: http://localhost:8000

Check console for:
```
✅ Dialysis Center Vue components loaded
✅ Dialysis Center utilities loaded
✅ Dialysis Center dashboards loaded
✅ Dialysis Center real-time system loaded
```

---

### Step 4: Test (1 minute)

1. **Open Patient Form:**
   - Create/view any patient
   - See stats cards below patient name
   
2. **Open Appointment Form:**
   - Create new appointment
   - See available time slots
   
3. **Open Dialysis Session Form:**
   - View any session
   - See vitals chart (if vitals exist)

---

## 🔄 Development Workflow

### Watch Mode (Auto-rebuild)

```bash
cd frappe-bench/apps/dialysis_center
npm run watch
```

Now any changes to `.vue`, `.js`, or `.scss` files will auto-rebuild!

---

## 🐛 Troubleshooting

### Issue: npm install fails

**Solution:**
```bash
# Use Node 18+
nvm use 18
npm install
```

### Issue: Build fails with "Cannot find module 'vue'"

**Solution:**
```bash
npm install vue chart.js --save
npm install esbuild esbuild-vue sass --save-dev
```

### Issue: Bundles not loading in browser

**Solution:**
```bash
bench build --app dialysis_center
bench clear-cache
# Hard refresh browser: Ctrl+Shift+R
```

### Issue: Vue components not rendering

**Solution:**
1. Check browser console for errors
2. Verify bundle files exist:
   ```bash
   ls dialysis_center/public/dist/js/
   ```
3. Rebuild:
   ```bash
   npm run build
   bench clear-cache
   ```

---

## 📋 Quick Checklist

- [ ] Node.js 18+ installed
- [ ] `npm install` completed successfully
- [ ] `npm run build` completed successfully
- [ ] Browser console shows 4 "✅ loaded" messages
- [ ] Patient form shows stats cards
- [ ] Appointment form shows time slots
- [ ] Session form shows vitals chart

---

## 🚀 Next Steps

1. **Customize Components:**
   - Edit `.vue` files in `public/src/components/`
   - Rebuild: `npm run build`

2. **Add New Features:**
   - Create utilities in `public/src/utils/`
   - Create dashboards in `public/src/pages/`
   - Register in respective bundle files

3. **Deploy to Production:**
   ```bash
   npm run build
   bench build --app dialysis_center --production
   ```

---

## 📖 Full Documentation

See `FRONTEND_IMPLEMENTATION_SUMMARY.md` for complete details.

---

**Status:** ✅ **READY TO BUILD!**

**Build Time:** ~5 minutes  
**Complexity:** Low  
**Support:** Vue 3, Chart.js, esbuild, SCSS
