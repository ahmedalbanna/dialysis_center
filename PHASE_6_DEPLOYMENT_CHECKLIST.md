# Phase 6: Deployment Checklist & Production Readiness
## Dialysis Center Management System

**Date**: February 19, 2026  
**Version**: 1.0.0  
**Audience**: System Administrators, DevOps Engineers

---

## Part 1: Pre-Deployment Verification (30 items)

### Environment Checks
- [ ] **Python 3.10+** installed: `python3 --version`
- [ ] **Node.js 18+** installed: `node --version`
- [ ] **MariaDB 10.11+** running: `mysql --version`
- [ ] **Redis 7.0+** running: `redis-cli ping` (should return PONG)
- [ ] **Git** available: `git --version`
- [ ] **wkhtmltopdf** installed (for PDF generation): `wkhtmltopdf --version`

### Frappe Bench Setup
- [ ] Bench installed: `bench --version`
- [ ] Bench directory exists: `/path/to/frappe-bench`
- [ ] Virtual environment active: `which python` shows bench venv
- [ ] Frappe app installed: Check `apps/frappe` directory
- [ ] Apps properly configured: `bench version`

### Database Verification
- [ ] MariaDB service running: `systemctl status mariadb`
- [ ] Database user created: `mysql -u frappe_user -p frappe_password`
- [ ] Database exists: `SHOW DATABASES;` shows frappe database
- [ ] Connection pool configured correctly
- [ ] Character set is utf8mb4: `SHOW VARIABLES LIKE 'character_set%';`

### Dialysis Center App Installation
- [ ] App cloned/installed: Check `apps/dialysis_center` directory
- [ ] App listed in installed apps: `bench list-apps` includes dialysis_center
- [ ] App migrated: `bench --site dialysis.local migrate`
- [ ] Fixtures loaded: Check patient, staff, machines in database
- [ ] Permissions configured: Verify Role and DocPerm entries

### DocType & Module Validation
- [ ] All DocTypes present in database
  - [ ] Patient
  - [ ] Appointment
  - [ ] Dialysis Session
  - [ ] Patient Bill
  - [ ] Lab Test
  - [ ] Dialysis Machine
  - [ ] Staff
- [ ] All modules enabled in modules.txt
- [ ] Workspaces created for each module
- [ ] Dashboards configured and accessible

### Permission & Security
- [ ] Role "Dialysis Administrator" created
- [ ] Role "Dialysis Technician" created
- [ ] Role "Clinic Manager" created
- [ ] Role "Accounts Manager" created
- [ ] Default permissions assigned to roles
- [ ] Document sharing configured for multi-user scenarios
- [ ] Password policies enforced

### API & Webhooks
- [ ] API endpoints whitelisted in hooks.py
- [ ] CORS configured for external integrations
- [ ] API authentication methods tested (Session, API Key, Bearer)
- [ ] Rate limiting configured (if applicable)
- [ ] Webhook handlers registered

### Asset Compilation
- [ ] Static assets compiled: `bench build`
- [ ] CSS bundles present in public/dist
- [ ] JavaScript bundles present in public/dist
- [ ] Images and fonts accessible
- [ ] Asset manifest (assets.json) generated

### Cache & Redis
- [ ] Redis running and accessible
- [ ] Cache backend configured (Redis)
- [ ] Session backend configured
- [ ] Job queue backend configured
- [ ] Cache keys accessible: `redis-cli KEYS "*"`

### Testing & Validation
- [ ] Run all tests: `bench --site dialysis.local run-tests --module dialysis_center`
- [ ] All tests passing: ✅ Verification script (below)
- [ ] No schema mismatches: Check error logs
- [ ] Data integrity verified: Database constraints intact

### Logs & Monitoring
- [ ] Log files directory exists and writable
- [ ] Error log accessible: `tail -f logs/error.log`
- [ ] Access log configured
- [ ] Bench worker logs accessible
- [ ] Scheduler logs accessible

### Configuration Files
- [ ] site_config.json exists and valid JSON
- [ ] Database credentials correct in site_config.json
- [ ] Redis URL configured
- [ ] Email configuration set
- [ ] File upload paths configured
- [ ] Session timeout configured (recommended: 7200 seconds)

### DNS & Network
- [ ] Domain name resolves (if using custom domain)
- [ ] Firewall allows ports 80/443/3306/6379
- [ ] Network connectivity to database verified
- [ ] Network connectivity to Redis verified
- [ ] Reverse proxy/load balancer configured (if applicable)

### Backup Systems
- [ ] Backup directory exists and writable
- [ ] Backup retention policy defined
- [ ] Initial backup created and verified
- [ ] Backup restoration tested

---

## Part 2: Production Readiness Checklist (35 items)

### SSL/TLS Certificate Setup
- [ ] SSL certificate obtained (Let's Encrypt or commercial)
- [ ] Private key secured and backed up
- [ ] Certificate chain valid
- [ ] Certificate not expired
- [ ] HSTS header configured
- [ ] Automatic certificate renewal configured

### Nginx/Reverse Proxy
- [ ] Nginx installed and running
- [ ] Nginx configuration file created for site
- [ ] SSL certificate configured in Nginx
- [ ] Gzip compression enabled
- [ ] Cache headers configured
- [ ] Security headers configured (X-Frame-Options, CSP, etc.)
- [ ] Rate limiting configured in Nginx

### Firewall Configuration
- [ ] Firewall enabled and running
- [ ] Port 22 (SSH) restricted to admin IPs only
- [ ] Port 80 (HTTP) open and redirects to HTTPS
- [ ] Port 443 (HTTPS) open to all
- [ ] Port 3306 (MySQL) open only to internal network
- [ ] Port 6379 (Redis) open only to internal network
- [ ] Port 8000 (Frappe) not directly accessible from internet

### Database Production Setup
- [ ] Database backup scheduled (daily, automated)
- [ ] Backup location: separate disk/storage
- [ ] Database user password strong (20+ characters, mixed)
- [ ] Root user password changed from default
- [ ] Unnecessary database users removed
- [ ] Query logging enabled for debugging
- [ ] Binary logging enabled for recovery
- [ ] Database replication configured (if applicable)

### Process Management (Supervisor)
- [ ] Supervisor installed: `supervisorctl --version`
- [ ] Supervisor configuration files created
- [ ] Web worker processes configured (2-4 processes)
- [ ] Worker processes configured for async jobs
- [ ] Scheduler process configured
- [ ] All processes monitored and auto-restart enabled
- [ ] Process logs configured and monitored

### Email Configuration
- [ ] Email SMTP server configured
- [ ] Sender email address set (e.g., noreply@clinicname.com)
- [ ] Test email sent successfully
- [ ] Email templates configured
- [ ] Notification recipients configured
- [ ] Email queue monitoring enabled
- [ ] Bounce handling configured (if applicable)

### Monitoring & Alerting
- [ ] Monitoring tool installed (Sentry, DataDog, New Relic, etc.)
- [ ] Application error tracking configured
- [ ] Performance metrics monitored (CPU, Memory, Disk)
- [ ] Database performance monitored
- [ ] Alert thresholds configured
- [ ] Notification channels set up (email, Slack, PagerDuty)
- [ ] Uptime monitoring configured

### Logging & Log Rotation
- [ ] Application logs configured
- [ ] Access logs configured
- [ ] Error logs configured
- [ ] Log rotation configured (logrotate)
- [ ] Log retention policy defined (30+ days)
- [ ] Central log collection configured (optional)
- [ ] Log shipping to external service (optional)

### Performance Optimization
- [ ] Database indexes verified: `SHOW INDEX FROM tab*;`
- [ ] Query cache configured (if using older MariaDB)
- [ ] Redis memory limit configured
- [ ] JavaScript/CSS assets minified
- [ ] Image optimization completed
- [ ] CDN configured for static assets (optional)
- [ ] HTTP/2 enabled in Nginx

### User Access Provisioning
- [ ] Administrator account created
- [ ] Department leads assigned
- [ ] Staff users created with appropriate roles
- [ ] Patient initial data loaded
- [ ] Test users created for UAT
- [ ] Multi-factor authentication enabled (optional)
- [ ] Single sign-on (LDAP/Active Directory) configured (optional)

### Data Migration (if from legacy system)
- [ ] Patient data migration script validated
- [ ] Staff data migration completed
- [ ] Historical appointment data migrated
- [ ] Historical billing data validated
- [ ] Data integrity checks passed
- [ ] Duplicate detection and resolution completed
- [ ] User acceptance testing on migrated data completed

### Documentation & Runbooks
- [ ] Deployment runbook documented
- [ ] Emergency procedures documented
- [ ] Password recovery procedures documented
- [ ] Rollback procedures documented
- [ ] On-call runbooks created
- [ ] Admin contact list maintained
- [ ] Incident response plan in place

### Legal & Compliance
- [ ] HIPAA compliance verified (if applicable)
- [ ] Data privacy policy implemented
- [ ] Audit logging enabled
- [ ] Audit log retention configured (90+ days)
- [ ] Compliance checklist completed
- [ ] Legal review completed
- [ ] User agreements/terms configured

### Security Hardening
- [ ] SSH key-based authentication configured
- [ ] Password policy enforced (minimum complexity)
- [ ] API key rotation scheduled
- [ ] API rate limiting enabled
- [ ] DDoS protection configured (if using external CDN)
- [ ] Security headers configured in Nginx
- [ ] OWASP top 10 protections implemented

### Load Testing & Performance
- [ ] Load testing completed (100+ concurrent users)
- [ ] Response time < 2 seconds for 95th percentile
- [ ] Database query optimization completed
- [ ] Memory usage stable under load
- [ ] CPU usage acceptable (< 80%)
- [ ] Scaling strategy documented
- [ ] Results documented and approved

### Disaster Recovery
- [ ] Disaster recovery plan documented
- [ ] Recovery time objective (RTO) defined (e.g., 4 hours)
- [ ] Recovery point objective (RPO) defined (e.g., 1 hour)
- [ ] Backup restoration tested in sandbox environment
- [ ] Failover procedures documented and tested
- [ ] Data retention and archival policy defined
- [ ] Off-site backup location verified

### Go-Live Readiness
- [ ] All checklist items completed: ✅
- [ ] All tests passing: ✅
- [ ] Load testing passed: ✅
- [ ] Backup verified: ✅
- [ ] Runbooks reviewed: ✅
- [ ] Team trained: ✅
- [ ] Business stakeholders approved: ✅
- [ ] Maintenance window scheduled: ✅

---

## Part 3: Troubleshooting Guide (30+ scenarios)

### Database Connection Issues

**Symptom**: "Lost connection to MySQL server during query"
**Solution**:
1. Check MariaDB status: `systemctl status mariadb`
2. Check connection pool: `SHOW PROCESSLIST;`
3. Increase max_connections in MariaDB config
4. Restart MariaDB: `systemctl restart mariadb`
5. Check logs: `/var/log/mysql/error.log`

**Symptom**: "Access denied for user 'frappe_user'@'localhost'"
**Solution**:
1. Verify credentials in site_config.json
2. Test connection: `mysql -u frappe_user -p -h localhost`
3. Reset password: `ALTER USER 'frappe_user'@'localhost' IDENTIFIED BY 'new_password';`
4. Flush privileges: `FLUSH PRIVILEGES;`
5. Update site_config.json with new password

### Asset Loading Problems

**Symptom**: CSS/JS files return 404, styling broken
**Solution**:
1. Rebuild assets: `bench build`
2. Clear browser cache: Ctrl+Shift+Del (hard refresh)
3. Check assets.json generated: `ls public/dist/`
4. Verify Nginx serving static files correctly
5. Check file permissions: `chmod 755 public/dist`

**Symptom**: "Failed to load resource: the server responded with a status of 500"
**Solution**:
1. Check error logs: `tail -f logs/error.log`
2. Check browser console for exact error
3. Verify file exists: `find public -name "*.bundle.js"`
4. Rebuild if missing: `bench build`
5. Check Nginx configuration for static paths

### Permission Errors

**Symptom**: "User does not have permission to read [DocType]"
**Solution**:
1. Check user roles: `frappe.db.get_value("User", "user@example.com", "roles")`
2. Check DocType permissions: Role-based permissions in DocType setup
3. Add permission: "Dialysis Administrator" role needs read/write on DocTypes
4. Check document sharing: User may need document-level access
5. Clear browser cache and re-login

**Symptom**: "Insufficient permissions to create Patient"
**Solution**:
1. Verify user has "Dialysis Administrator" or equivalent role
2. Check "Create" permission on Patient DocType
3. Verify document sharing if document-level permissions enabled
4. Check if DocType has custom permission query
5. User must have permission at DocType level (permlevel 0)

### API Endpoint Failures

**Symptom**: "POST /api/resource/Patient returns 403 Forbidden"
**Solution**:
1. Verify user authenticated: Check Authorization header
2. Check API whitelist in hooks.py
3. Verify CORS configured correctly
4. Test with cURL: `curl -X POST http://localhost:8000/api/resource/Patient -H "Authorization: token key:secret"`
5. Check rate limiting not exceeded

**Symptom**: "GET /api/resource/Patient returns 404 Not Found"
**Solution**:
1. Verify Patient DocType exists: `frappe.db.exists("DocType", "Patient")`
2. Check API endpoint name matches DocType name exactly
3. Verify Frappe recognizes the custom app
4. Check if API endpoint is whitelisted (custom endpoints need @frappe.whitelist())
5. Rebuild and restart: `bench build && bench start`

### Performance Bottlenecks

**Symptom**: Page load time > 5 seconds
**Solution**:
1. Check database query performance: Enable query logs
2. Verify indexes present: `EXPLAIN SELECT * FROM tabPatient WHERE name='PT-001';`
3. Check for N+1 queries in browser DevTools Network tab
4. Verify Redis running: `redis-cli ping`
5. Clear Redis cache: `redis-cli FLUSHDB`
6. Optimize heavy reports: Add WHERE clause limits

**Symptom**: "OperationalError: Lost connection to MySQL server"
**Solution**:
1. Check MariaDB memory: `free -h`
2. Check max_connections: `SHOW VARIABLES LIKE 'max_connections';`
3. Kill idle connections: `SHOW PROCESSLIST;` then `KILL connection_id;`
4. Restart MariaDB: `systemctl restart mariadb`
5. Review slow query log: `SHOW VARIABLES LIKE 'slow_query_log';`

### Session Management Issues

**Symptom**: User logged out after 30 minutes of inactivity
**Solution**:
1. Check session timeout: `frappe.session_defaults["session_expiry_time"]`
2. Modify in site_config.json: `"session_expiry_time": 7200` (2 hours)
3. Restart Frappe: `bench restart`
4. Clear Redis sessions: `redis-cli DEL "*"`
5. User re-login required

**Symptom**: "Session cookie not secure" warning in production
**Solution**:
1. Enable HTTPS only
2. Set in site_config.json: `"ssl_certificate": "/path/to/cert.pem"`
3. Configure Nginx to redirect HTTP to HTTPS
4. Set Secure flag: Session cookies automatically marked Secure over HTTPS
5. Set SameSite: Configured in Frappe automatically

### Backup/Restore Problems

**Symptom**: "Backup failed: Permission denied writing to /path/to/backup"
**Solution**:
1. Check directory exists: `mkdir -p /path/to/backup`
2. Fix permissions: `chmod 755 /path/to/backup`
3. Fix ownership: `chown frappe:frappe /path/to/backup`
4. Check disk space: `df -h` (need 2x database size)
5. Try manual backup: `bench --site dialysis.local backup`

**Symptom**: "Restore failed: Duplicate key error on table 'tabPatient'"
**Solution**:
1. Restore to clean database: Create new empty site first
2. Check backup file integrity: `gzip -t backup.sql.gz`
3. Extract and inspect: `gunzip -c backup.sql.gz | head -100`
4. Verify source and target schema compatibility
5. Contact Frappe support if corruption suspected

### Workflow & Approval Issues

**Symptom**: "Workflow state not transitioning on approval"
**Solution**:
1. Check workflow created: DocType -> Workflow tab
2. Verify current user has approval role
3. Check workflow transitions: Open Workflow DocType
4. Verify user assigned to Approver field
5. Clear browser cache and refresh

**Symptom**: "Approval email not sent to approver"
**Solution**:
1. Check email configuration: Setup -> Email Account
2. Verify SMTP server accessible
3. Check Email Queue: Queue item shows pending/sent
4. Review email template: Setup -> Email Template
5. Check logs: `grep "Email" logs/error.log`

### Data Integrity Issues

**Symptom**: "Patient record shows duplicate entries in list"
**Solution**:
1. Check database: `SELECT COUNT(*) as count FROM tabPatient WHERE name='PT-001';`
2. If > 1, investigate custom import script or data migration
3. Restore from backup if corruption suspected
4. Run data validation: `bench --site dialysis.local run-tests --module dialysis_center`

**Symptom**: "Referential integrity: Patient Bill references non-existent Patient"
**Solution**:
1. Identify orphaned bills: `SELECT * FROM tabPatient_Bill WHERE patient NOT IN (SELECT name FROM tabPatient);`
2. Option A: Delete orphaned records: `DELETE FROM tabPatient_Bill WHERE patient NOT IN (SELECT name FROM tabPatient);`
3. Option B: Restore from backup (if recent)
4. Implement foreign key constraints to prevent future issues

### Authentication & API Key Problems

**Symptom**: "Invalid API key" when calling private endpoint
**Solution**:
1. Generate new API key: User -> API Key section
2. Store key and secret securely
3. Test: `curl -H "Authorization: token {key}:{secret}" http://localhost:8000/api/method/frappe.client.get_list`
4. Verify key not expired or revoked
5. Check rate limiting not triggered

**Symptom**: "CORS error when calling API from external domain"
**Solution**:
1. Check CORS configuration in hooks.py
2. Add domain to allowed origins: `"allow_cors": ["https://example.com"]`
3. Verify preflight request succeeds (OPTIONS request)
4. For development: Use `"allow_cors": "*"` (NOT for production)
5. Restart Frappe: `bench restart`

---

## Pre-Deployment Verification Script

```bash
#!/bin/bash
# Quick verification before deployment

echo "=== Pre-Deployment Verification ==="

# Check Python
python3 --version || { echo "Python 3 not found"; exit 1; }

# Check MariaDB
mysql --version || { echo "MariaDB not found"; exit 1; }

# Check Redis
redis-cli ping || { echo "Redis not running"; exit 1; }

# Check Frappe
bench --version || { echo "Bench not found"; exit 1; }

# Check app
bench list-apps | grep dialysis_center || { echo "App not installed"; exit 1; }

# Run tests
bench --site dialysis.local run-tests --module dialysis_center || { echo "Tests failed"; exit 1; }

echo "✅ All pre-deployment checks passed!"
```

Save as `pre_deploy_check.sh` and run: `bash pre_deploy_check.sh`

---

## Sign-Off & Approval

- [ ] System Administrator reviewed and approved
- [ ] Infrastructure/DevOps team reviewed
- [ ] Security team reviewed and approved
- [ ] Business stakeholders approved
- [ ] Deployment date/time scheduled
- [ ] Rollback plan tested and documented
- [ ] Support team trained

**Approved By**: ___________________  
**Date**: ___________________  
**Time**: ___________________  

---

**Next Step**: Run PHASE_6_VERIFICATION_SCRIPT.py to validate all workflows before going live.

