# Bench Master Memory File

## Quick Facts
- **Specialty**: Frappe Bench CLI operations, site management, app installation, database operations, environment configuration, and deployment
- **Primary Tools**: Bash commands, bench CLI, file editing
- **Common Tasks**: Site creation, app management, migrations, cache clearing, database backups, production setup
- **Estimated Task Time**: 15-45 minutes per task

---

## Core Bench Commands (Reference)

### Site Management
```bash
# Create new site
bench new-site mysite.local --admin-password=admin@123

# List all sites
bench list-sites

# Switch current site
bench --site mysite.local console

# Backup site
bench --site mysite.local backup

# Restore from backup
bench --site mysite.local restore /path/to/backup.sql.gz

# Reset site (removes all data)
bench --site mysite.local reset-database
```

### App Management
```bash
# Install app to site
bench --site mysite.local install-app myapp

# Uninstall app
bench --site mysite.local uninstall-app myapp

# Get app list
bench --site mysite.local list-apps

# Create new app
bench new-app myapp

# Remove app
rm -rf apps/myapp
```

### Database & Cache
```bash
# Run migrations
bench --site mysite.local migrate

# Clear cache
bench --site mysite.local clear-cache

# Clear all caches
bench clear-cache --all-sites

# Database console
bench --site mysite.local mariadb

# SQL query
bench --site mysite.local sql "SELECT * FROM tabUser LIMIT 5"
```

### Development Server
```bash
# Start development server
bench start

# Start with specific port
bench start --port 8001

# Build assets
bench build

# Watch for changes (with rebuild)
bench watch

# Run tests
bench --site mysite.local run-tests

# Run specific test
bench --site mysite.local run-tests --module myapp.doctype.mydoc.test_mydoc
```

---

## Common Patterns

### Pattern 1: Setup New Development Site
```bash
# 1. Create site
bench new-site dev.local --admin-password=admin@123

# 2. Install your app
bench --site dev.local install-app myapp

# 3. Run migrations
bench --site dev.local migrate

# 4. Verify
bench --site dev.local console
> frappe.get_all("DocType", limit=5)
```

### Pattern 2: Backup & Restore Workflow
```bash
# Backup before major changes
bench --site mysite.local backup

# Make changes...

# Restore if needed
bench --site mysite.local restore /path/to/backup
```

### Pattern 3: Production Deployment Checklist
```bash
# 1. Build assets for production
bench build

# 2. Run all migrations
bench --site prod.local migrate

# 3. Reload doctypes
bench --site prod.local reload-doc

# 4. Clear all caches
bench --site prod.local clear-cache

# 5. Enable production mode
# Edit site_config.json: "developer_mode": 0

# 6. Start with supervisor (not bench start)
# Use systemctl or supervisor config
```

---

## Critical Decision Points

**When to use bench new-site vs reset-database:**
- **new-site**: Creating a completely fresh environment (development/testing)
- **reset-database**: Clearing data while keeping schema (fresh state in same site)

**When to rebuild vs restart:**
- **rebuild (bench build)**: After asset changes, hooks changes
- **restart (bench start)**: After code changes, database changes
- **both**: Safe approach when unsure

**Backup frequency:**
- Before any major changes
- Before app updates/migrations
- Daily in production (automated)
- Before deployment to production

---

## Common Issues & Solutions

**Issue**: Site not starting after migration
```bash
# Solution: Clear cache and run migrate again
bench --site mysite.local clear-cache
bench --site mysite.local migrate
bench start
```

**Issue**: "Site mysite.local not found"
```bash
# Solution: Check site name
bench list-sites
# Ensure site_config.json exists in frappe-bench/sites/mysite.local/
```

**Issue**: Assets not loading after changes
```bash
# Solution: Rebuild and clear cache
bench build
bench --site mysite.local clear-cache
```

**Issue**: Port already in use
```bash
# Solution: Use different port
bench start --port 8001
# Or kill process on port 8000
lsof -ti :8000 | xargs kill -9
```

---

## Performance Tuning

### Enable Production Mode (for performance testing)
Edit `frappe-bench/sites/mysite.local/site_config.json`:
```json
{
  "developer_mode": 0,
  "compress": 1,
  "db_query_timeout": 40000
}
```

### Increase Worker Processes
Edit `frappe-bench/Procfile`:
```procfile
web: gunicorn --workers 4 --bind 0.0.0.0:8000 frappe.app:application
```

### Enable Redis Caching
Verify Redis is running and configured in `common_site_config.json`:
```json
{
  "redis_cache": "redis://127.0.0.1:6379/1",
  "redis_queue": "redis://127.0.0.1:6379/2"
}
```

---

## Decision Tree: When to Call Bench-Master Subagent

**Use Bench-Master when:**
- ✅ Setting up new development/production environments
- ✅ Managing site lifecycle (create, backup, restore, reset)
- ✅ Installing/uninstalling apps
- ✅ Running migrations and database operations
- ✅ Troubleshooting deployment issues
- ✅ Performance tuning and optimization
- ✅ Automating deployment pipelines

**Don't use Bench-Master for:**
- ❌ DocType/field design (use DocType-Architect)
- ❌ API development (use API-Whitelister)
- ❌ Frontend customization (use Frontend-Forge)
- ❌ Code quality (use Ruff-Formatter)

---

## Integration Points

**Works with:**
- frappe-installer: Initial setup
- Debug-Detective: Troubleshooting deployment issues
- Test-Engineer: Running test suites
- All subagents: As prerequisite environment setup

**Key files touched:**
- `frappe-bench/Procfile` - Process configuration
- `frappe-bench/sites/mysite.local/site_config.json` - Site settings
- `frappe-bench/common_site_config.json` - Global settings

---

**Last Updated**: 2026-02-19
**Frappe Version**: v15.100.1
**Bench Version**: 5.x+
