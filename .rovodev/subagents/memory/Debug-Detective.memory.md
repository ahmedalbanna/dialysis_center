# Debug Detective Memory File

## Quick Facts
- **Specialty**: Troubleshooting Frappe issues: permission errors, missing assets, Redis failures, migrations, CSS/JS not loading, session issues, database errors
- **Primary Tools**: Bash for logs, error inspection, file checking, database queries
- **Common Tasks**: Error diagnosis, log analysis, permission debugging, asset troubleshooting, database fixes
- **Estimated Task Time**: 10-30 minutes per issue

---

## Systematic Debugging Workflow

### Step 1: Identify Error Category
```bash
# Check logs for error type
tail -100 frappe-bench/logs/frappe.log | grep -i "error\|exception\|traceback"

# Database errors: Check MariaDB logs
tail -50 /var/log/mysql/error.log

# Redis errors: Check Redis connectivity
redis-cli ping

# Asset errors: Check browser console (F12 → Console tab)
```

### Step 2: Reproduce the Issue
- Identify exact steps to reproduce
- Note environment (dev/production)
- Check if issue is site-specific or global
- Try in different browser/incognito mode

### Step 3: Gather Context
```bash
# Framework version
grep "^__version__" frappe-bench/apps/frappe/frappe/__init__.py

# Python version
python --version

# Database health
bench --site mysite.local sql "SHOW GLOBAL STATUS LIKE 'Threads%';"

# Redis status
redis-cli INFO server | grep redis_version
```

---

## Common Error Categories & Solutions

### Category 1: Permission Errors

**Error Message**: `User does not have permission` or `PermissionError`

**Diagnosis**:
```python
# In console or custom script
frappe.console()
> user = "test@example.com"
> frappe.has_permission("Order", "write", user=user)
> # Returns True/False

# Check user roles
> frappe.get_roles(user)

# Check DocType permissions
> frappe.get_all("DocPerm", filters={"parent": "Order"}, 
    fields=["role", "read", "write", "create", "delete", "submit", "cancel"])
```

**Solutions**:
```bash
# 1. Check if user exists
bench --site mysite.local sql "SELECT name FROM tabUser WHERE name='test@example.com';"

# 2. Grant permission via console
bench --site mysite.local console
> frappe.permissions.add_permission("Order", "Sales User", 0)  # 0 = DocType level
> frappe.db.commit()

# 3. For document-level sharing
> frappe.share.add("Order", "ORDER-001", "test@example.com", "read")
```

### Category 2: Missing/Not Loading Assets

**Symptoms**: CSS/JS files not loading, styles missing, JavaScript errors in console

**Diagnosis**:
```bash
# Check if assets are built
ls -la frappe-bench/apps/frappe/frappe/public/dist/

# Check assets.json manifest
cat frappe-bench/apps/frappe/frappe/public/dist/assets.json | head -20

# Check browser developer tools (F12 → Network)
# Look for 404 errors on JS/CSS files
```

**Solutions**:
```bash
# 1. Rebuild assets
bench build

# 2. Clear browser cache (Ctrl+Shift+Del or Cmd+Shift+Del)

# 3. Hard refresh browser (Ctrl+Shift+R)

# 4. Clear server cache
bench --site mysite.local clear-cache

# 5. Check if esbuild completed successfully
bench build --verbose | tail -50

# 6. Verify static files are served
curl http://localhost:8000/app/frappe/desk.bundle.js | head -5
```

### Category 3: Database Connection Errors

**Error Message**: `MySQL server has gone away` or `Can't connect to MySQL server`

**Diagnosis**:
```bash
# Check if MariaDB is running
sudo systemctl status mariadb
# or
ps aux | grep -i mysql

# Test connection
bench --site mysite.local sql "SELECT 1;" 

# Check MariaDB logs
sudo tail -50 /var/log/mysql/error.log

# Check database config
cat frappe-bench/sites/mysite.local/site_config.json | grep -i "db_"
```

**Solutions**:
```bash
# 1. Restart MariaDB
sudo systemctl restart mariadb

# 2. Check disk space
df -h | grep -E "/$|/var"

# 3. Increase max_connections if too many connections
# Edit /etc/mysql/mariadb.conf.d/50-server.cnf
# max_connections = 200

# 4. Verify database exists
bench --site mysite.local sql "SHOW DATABASES LIKE 'frappe%';"

# 5. If corrupted, repair tables
bench --site mysite.local sql "REPAIR TABLE tabUser;"
```

### Category 4: Redis/Cache Errors

**Error Message**: `Redis connection refused` or `Cache connection failed`

**Diagnosis**:
```bash
# Check Redis status
redis-cli ping  # Should return PONG

# Check Redis connectivity
redis-cli -p 6379 PING

# Check Redis memory
redis-cli INFO memory | head -10

# Check configured Redis in Frappe
cat frappe-bench/common_site_config.json | grep redis

# Test from Python
bench --site mysite.local console
> frappe.cache.get_value("test_key")
```

**Solutions**:
```bash
# 1. Restart Redis
sudo systemctl restart redis-server

# 2. Check if Redis is listening
netstat -tlnp | grep 6379

# 3. Clear Redis cache
redis-cli FLUSHDB

# 4. Check Redis logs
sudo tail -50 /var/log/redis/redis-server.log

# 5. Reinstall Redis if corrupted
sudo apt-get remove redis-server
sudo apt-get install redis-server
```

### Category 5: Migration Errors

**Error Message**: `Migration failed` or `Column doesn't exist`

**Diagnosis**:
```bash
# Check pending migrations
bench --site mysite.local migrate --dry-run

# Check what migrations exist
ls frappe-bench/apps/*/patches.txt

# Check database schema
bench --site mysite.local sql "DESCRIBE tabOrder;"

# Check custom fields
frappe.get_all("Custom Field", filters={"dt": "Order"})
```

**Solutions**:
```bash
# 1. Run migrate with verbose output
bench --site mysite.local migrate --verbose

# 2. Run specific failing migration
bench --site mysite.local migrate --skip-failing

# 3. Reload DocType definition
bench --site mysite.local console
> frappe.reload_doc('module_name', 'doctype', 'doctype_name')
> frappe.db.commit()

# 4. If stuck, force reset (CAREFUL - data loss)
bench --site mysite.local reset-database --mariadb-root-password=root
```

### Category 6: Session/Login Issues

**Error Message**: `Session expired` or `You are not logged in`

**Diagnosis**:
```bash
# Check if session cookie is set
# Browser DevTools → Application → Cookies → sid

# Check session in database
bench --site mysite.local sql "SELECT * FROM tabSession WHERE user='test@example.com' LIMIT 1;"

# Check if session storage works
frappe.cache.get_value(session_id)
```

**Solutions**:
```bash
# 1. Clear browser cookies (Ctrl+Shift+Del)

# 2. Logout and login again

# 3. Check session timeout in site_config
cat frappe-bench/sites/mysite.local/site_config.json | grep session

# 4. Clear expired sessions
bench --site mysite.local sql "DELETE FROM tabSession WHERE expires_on < NOW();"

# 5. Restart development server
# Stop: Ctrl+C
# Start: bench start
```

### Category 7: JavaScript Errors

**Symptoms**: JS errors in console, form not responding, buttons not working

**Diagnosis**:
```bash
# Open browser console (F12)
# Look for red error messages

# Common errors:
# - Uncaught TypeError: Cannot read property 'x' of undefined
# - Uncaught ReferenceError: frappe is not defined
# - Mixed Content: blocked by HTTPS

# Check if frappe is loaded
# In console: typeof frappe → should return "object"

# Check custom scripts
curl http://localhost:8000/custom-script.js
```

**Solutions**:
```bash
# 1. Check for syntax errors in custom scripts
node -c apps/myapp/myapp/public/js/custom.js

# 2. Rebuild assets
bench build

# 3. Check browser console for full error stack

# 4. Check custom script hooks in hooks.py
grep -r "app_include_js" apps/myapp/myapp/hooks.py

# 5. Verify script is in correct path
ls apps/myapp/myapp/public/js/
```

---

## Essential Debug Commands

```bash
# Tail live logs
tail -f frappe-bench/logs/frappe.log

# Search logs for error
grep "ERROR" frappe-bench/logs/frappe.log | tail -20

# Check system resources
top  # CPU and memory usage

# Check disk space
df -h

# Monitor network connections
netstat -tlnp | grep python

# Check file permissions
ls -la frappe-bench/sites/mysite.local/

# Database health check
bench --site mysite.local sql "SELECT COUNT(*) FROM tabUser;"

# Clear all caches
bench --site mysite.local clear-cache
bench clear-cache

# Check app logs
cat frappe-bench/logs/bench.log
```

---

## Decision Tree: When to Call Debug-Detective

**Use Debug-Detective when:**
- ✅ Users report errors or system is broken
- ✅ Feature stops working after deploy
- ✅ Slow queries or performance issues
- ✅ Permission issues blocking users
- ✅ Assets not loading correctly
- ✅ Database connection problems
- ✅ Session/authentication issues

**Don't use for:**
- ❌ Feature development (use appropriate architect)
- ❌ Permission setup (use Permission-Guardian)
- ❌ Database schema changes (use Database-Navigator)
- ❌ Code quality issues (use Ruff-Formatter)

---

## Pro Tips

1. **Always start with logs**: Most issues leave a trail in logs
2. **Reproduce consistently**: If you can't reproduce, hard to fix
3. **Check resource limits**: Disk space, RAM, connections often cause subtle errors
4. **Isolate the change**: What changed recently? Rollback to test
5. **Clear caches**: Many "mysterious" issues are actually cached data
6. **Check permissions**: Permission errors are most common issue
7. **Test in fresh browser**: Incognito mode avoids cache issues

---

**Last Updated**: 2026-02-19
**Frappe Version**: v15.100.1
**Common Patterns Covered**: 7 major categories
