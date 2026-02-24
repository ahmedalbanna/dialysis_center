# Administrator Guide
## Dialysis Center Management System

**Version**: 1.0.0  
**Last Updated**: February 19, 2026  
**Audience**: System Administrators, IT Staff, Clinic Managers

---

## Part 1: System Configuration

### 1.1 Initial Setup After Deployment

**First Login**:
1. Access application: `https://your-domain.com`
2. Login with Administrator credentials
3. You'll see Setup Wizard (or skip it)
4. Configure basic settings

**Set Organization Name**:
1. Go to Setup > System Settings
2. Set:
   - **Company Name**: Your clinic name
   - **Company Address**: Full address
   - **Company Email**: Main contact email
   - **Company Phone**: Main phone number
   - **Website**: Optional clinic website
3. Save

**Configure Localization**:
1. Go to Setup > Locale
2. Set:
   - **Language**: English (or other)
   - **Timezone**: Your timezone (UTC, EST, PST, etc.)
   - **Date Format**: DD-MM-YYYY or MM-DD-YYYY
   - **Currency**: USD, EUR, etc.
3. Save

### 1.2 User Account Setup

**Create Administrator Accounts**:
1. Go to Setup > User
2. Click "New User"
3. Enter:
   - **Email**: User email (acts as username)
   - **First Name**: Administrator name
   - **Last Name**: Surname
   - **Password**: Initial password (user changes on first login)
4. Click "Save"
5. User can now login

**Assign Roles**:
1. Click "Edit" on user
2. Click "Roles" section
3. Click "Add Row"
4. Select role:
   - **Dialysis Administrator**: Full system access
   - **Clinic Manager**: Clinic operations
   - **Accounts Manager**: Billing and finance
   - **Dialysis Technician**: Clinical staff
   - **Nurse**: Clinical support
5. Save
6. User immediately has role permissions

**Disable User Account**:
1. Open user
2. Check "Disabled"
3. Save
4. User cannot login
5. Useful when staff leaves

### 1.3 Role & Permission Configuration

**View Default Roles**:
1. Go to Setup > Role
2. System includes pre-configured roles:
   - Dialysis Administrator
   - Clinic Manager
   - Accounts Manager
   - Dialysis Technician
   - Nurse
   - Patient (limited access)

**Create Custom Role**:
1. Click "New Role"
2. Enter **Role Name**: e.g., "Lab Supervisor"
3. Save
4. Configure permissions (see next section)

**Configure Role Permissions**:
1. Open role
2. Click "Permissions" section
3. For each DocType:
   - Check: Read / Write / Create / Delete / Submit / Cancel / Amend
   - Set **Permission Level**: 0 (standard) or 1 (owner level)
4. Save
5. Role now has these permissions

**Permission Levels Explained**:
- **Level 0**: Standard permissions (visible to all users with role)
- **Level 1**: Owner level (only creator can modify)
- **Level 2**: Specific fields (if custom permission logic)

### 1.4 DocType Customization

**Add Custom Field to DocType**:
1. Go to DocType (e.g., Patient)
2. Click "Customize Form"
3. Click "Add Row" in Fields section
4. Enter:
   - **Label**: User-friendly name
   - **Fieldname**: System name (snake_case)
   - **Fieldtype**: Data/Link/Select/Date/etc.
   - **Required**: Check if mandatory
   - **Options**: For Select fields (e.g., "Yes\nNo")
   - **Default Value**: Pre-fill value
5. Arrange with drag-and-drop
6. Click "Save Customization"

**Hide/Show Fields**:
1. Open DocType Customization
2. For each field:
   - Check "Hidden" to hide
   - Set "Read Only" to display-only
   - Set "Mandatory" for required fields
3. Save

**Conditional Field Display**:
1. Set "Depends On" field
2. Add "Conditional Display" expression: `eval: doc.field_name == 'value'`
3. Example: Show vascular access location only if access type is selected
4. Save

### 1.5 Email Configuration

**Set SMTP Server**:
1. Go to Setup > Email Account
2. Click "New Email Account"
3. Enter:
   - **Email Address**: noreply@clinic.com
   - **Password**: SMTP password (not user password)
   - **SMTP Server**: smtp.gmail.com (or your provider)
   - **SMTP Port**: 587 (or 465 for SSL)
   - **Use TLS**: Check if using TLS
4. Click "Save"
5. Test: Click "Test Email" button

**Default Email Address**:
1. Open Email Account
2. Check "Default Outgoing Account"
3. Save
4. System uses this for all outgoing emails

**Email Signature**:
1. Go to Email Account
2. Set "Signature" field
3. HTML supported
4. Added to all outgoing emails from system

**Email Templates**:
1. Go to Setup > Email Template
2. Pre-configured templates for:
   - Appointment confirmations
   - Billing notifications
   - Test result notifications
3. Click to edit template
4. Customize subject and body
5. Save

### 1.6 Backup & Restore Configuration

**Configure Automatic Backups**:
1. Go to Setup > Backup Settings
2. Set:
   - **Backup Frequency**: Daily (recommended)
   - **Backup Time**: Off-peak time (e.g., 2 AM)
   - **Backup Location**: `/path/to/backups` or cloud storage
   - **Retention Days**: Keep 30 days of backups
3. Save
4. System auto-backs up at configured time

**Manual Backup**:
1. Go to Backups
2. Click "Backup" button
3. Wait for completion
4. Download backup file if needed
5. Backup stored in backup directory

**Restore from Backup**:
1. **WARNING**: This overwrites current data
2. Go to Backups
3. Click "Restore" on backup file
4. Confirm you want to restore
5. System restores database
6. Verify data restored correctly
7. Test key workflows

**Backup Verification**:
1. Periodically restore to test environment
2. Verify data integrity
3. Test restore time (for RTO planning)
4. Document restore procedures

### 1.7 Security Configuration

**Password Policy**:
1. Go to Setup > System Settings
2. Set:
   - **Minimum Password Length**: 12 characters (recommended)
   - **Require Password Change**: Every 90 days
   - **Password Strength Check**: Enabled
3. Save
4. Applied to new and changed passwords

**Enable Two-Factor Authentication** (Optional):
1. Go to Setup > System Settings
2. Check "Enable Two Factor Authentication"
3. Users can set up 2FA in their profile
4. OTP via email or authenticator app

**API Key Management**:
1. User goes to their profile (top right)
2. Click "Settings"
3. Scroll to "API Keys & Secrets"
4. Click "Generate"
5. Store securely (shown only once)
6. Share key:secret with integrations
7. User can revoke key if compromised

**Session Timeout**:
1. Go to Setup > System Settings
2. Set "Session Timeout (in seconds)": 7200 (2 hours)
3. Save
4. Users logged out after inactivity
5. Can adjust per role if needed

---

## Part 2: User Management

### 2.1 Creating User Accounts

**Bulk User Creation**:
1. Go to Setup > User > Import
2. Prepare CSV with columns:
   - Email
   - First Name
   - Last Name
   - Send Welcome Email (Yes/No)
3. Upload CSV
4. System creates users
5. Sends welcome emails with temporary password

**Individual User Creation**:
1. Go to Setup > User
2. Click "New User"
3. Fill form (see Initial Setup section above)
4. Check "Send Welcome Email"
5. Save
6. User receives email with login link

### 2.2 Managing User Profiles

**Update User Profile**:
1. User clicks profile icon (top right)
2. Click "User Settings"
3. Can update:
   - Phone number
   - Contact email
   - Timezone
   - Desktop customization
4. Click "Save"

**Admin View of User**:
1. Go to Setup > User
2. Click on user name
3. View:
   - All assigned roles
   - Last login time
   - Account creation date
   - Password change history
   - Login attempts
4. Can modify roles, disable, reset password

### 2.3 Role Assignment

**Assign Single Role**:
1. Open user
2. Click "Roles" section
3. Click "Add Row"
4. Select role from dropdown
5. Save
6. Takes effect immediately

**Assign Multiple Roles**:
1. Open user
2. Click "Roles"
3. Add multiple rows with different roles
4. Save
5. User has combined permissions of all roles

**Department-Based Access**:
1. Some DocTypes have "Department" field
2. Can restrict by department
3. Example: Accounts Manager only sees their department's bills
4. Configure in Permission Query Conditions

### 2.4 Password Management

**Reset User Password** (Admin):
1. Open user
2. Click "Reset Password"
3. System generates temporary password
4. Send to user via email
5. User must change on first login

**Require Password Change**:
1. If user hasn't changed password recently
2. Go to user record
3. Check "Force Password Change on Login"
4. Save
5. User must change password at next login

**Password History**:
1. Open user
2. View "Password Change History"
3. System tracks all password changes
4. Security audit trail

---

## Part 3: Data Management

### 3.1 Data Backup Procedures

**Daily Backup Checklist**:
- [ ] Backup completed without errors
- [ ] Backup file size reasonable (within 10% of previous)
- [ ] Backup accessible from backup location
- [ ] Email notification received (if configured)
- [ ] Monthly full backup on separate storage

**Backup Verification**:
1. Monthly: Restore backup to test environment
2. Verify data integrity
3. Check row counts match production
4. Test key workflows
5. Document results

**Long-term Archival**:
1. Weekly/monthly backups moved to archive storage
2. Archive location: Separate server/cloud
3. Keep 1-3 months of backups
4. Older backups retained per policy (e.g., 7 years for healthcare)
5. Document retention policy

### 3.2 Data Restoration

**Restore Process**:
1. **BEFORE RESTORING**: Notify all users system will be down
2. Shutdown web server: `bench stop`
3. Shutdown worker: `supervisorctl stop all`
4. Go to Backups
5. Click "Restore" on chosen backup
6. System restores database (can take 10-30 minutes for large DB)
7. Verify restoration succeeded
8. Restart services: `bench start`
9. Test login and key workflows
10. Notify users system is back online

**Restore to Different Database** (for testing):
1. Create new site: `bench new-site test.local`
2. Restore: `bench --site test.local restore /path/to/backup.sql.gz`
3. Use test site without affecting production
4. Test changes or migrations
5. Delete when done: `bench drop-site test.local`

**Incremental Recovery**:
1. If only recent transactions corrupted
2. Restore to point just before corruption
3. Re-enter recent transactions
4. Verify patient data integrity
5. Document incident

### 3.3 Data Cleanup & Archiving

**Delete Old Test Records**:
1. Go to DocType list
2. Filter by creation date (older than date needed)
3. Select records to delete
4. Click "Delete"
5. **WARNING**: Cannot be undone without restore

**Archive Old Sessions**:
1. Dialysis sessions older than 2 years can be archived
2. Go to Dialysis Session list
3. Filter by date
4. Select sessions
5. Click "Archive"
6. Moved to archive table (searchable but not in main views)

**Clean Up Test Data**:
1. Before going live, remove test patients/appointments
2. Go to Patient list
3. Filter by: Created during testing period
4. Select all
5. Delete
6. Verify no test data remains

**GDPR Data Deletion** (if required):
1. Patient requests data deletion
2. Go to Patient record
3. Click "Delete All Personal Data"
4. Patient name/contact info deleted
5. Sessions/bills kept for legal/financial records
6. Generate deletion confirmation

### 3.4 Data Validation

**Check Data Integrity**:
1. Go to Tools > Database Doctor
2. Run checks for:
   - Missing required fields
   - Orphaned records (bills with no patient)
   - Duplicate patient records
   - Invalid foreign keys
3. Review findings
4. Fix issues or delete orphaned records

**Patient Data Validation**:
1. Go to Patient list
2. Filter for incomplete records (missing email, phone)
3. Contact patients for missing info
4. Update records
5. Verify all required fields populated

**Financial Data Validation**:
1. Go to Billing Report
2. Verify: Total bills = Total payments + Outstanding
3. Reconcile with accounting system
4. Resolve discrepancies
5. Document reconciliation

---

## Part 4: System Maintenance

### 4.1 Monitoring System Health

**Check System Status**:
1. Go to Setup > System Health
2. View:
   - Database size
   - Number of records by DocType
   - Last backup time
   - Cache status
   - Worker status
3. All green = healthy

**Monitor Disk Space**:
1. Login to server: `ssh admin@server.com`
2. Check disk: `df -h`
3. Ensure > 20% free space
4. If < 10% free: Delete old backups or files
5. Monitor daily

**Check Database Performance**:
1. Login to MariaDB: `mysql -u root -p`
2. View large tables: `SELECT table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size in MB' FROM information_schema.tables WHERE table_schema = 'frappe' ORDER BY (data_length + index_length) DESC;`
3. Check slow query log: `SHOW VARIABLES LIKE 'slow_query_log';`
4. If slow queries found: Add indexes

### 4.2 Database Optimization

**Add Index for Slow Query**:
1. Identify slow query from error logs
2. Example: `SELECT * FROM tabPatient WHERE name = 'PT-001'`
3. Add index: `CREATE INDEX idx_patient_name ON tabPatient(name);`
4. Verify improves performance

**Routine Maintenance**:
1. Weekly: Run `OPTIMIZE TABLE` on large tables
2. Monthly: Check fragmentation
3. Quarterly: Full database optimization
4. Yearly: Review table structures, consider partitioning

**Vacuum/Cleanup** (if using PostgreSQL):
1. `VACUUM ANALYZE;` (PostgreSQL)
2. Not needed for MariaDB (uses InnoDB)

### 4.3 Cache Management

**Clear Application Cache**:
1. Go to Tools > Cache Management
2. Click "Clear Cache"
3. Or from command line: `bench --site dialysis.local clear-cache`
4. Use if data seems stale
5. Performance may be slower immediately after (cache rebuilds)

**Clear Redis Cache**:
1. From server: `redis-cli FLUSHDB`
2. **WARNING**: Clears all cached data
3. Use only if cache corrupted
4. Better to clear specific keys: `redis-cli DEL "key_pattern*"`

**Monitor Cache Hit Rate**:
1. Go to Tools > Cache Monitor
2. View: Cache hits vs misses
3. If hit rate low (< 70%): May need more RAM
4. If hit rate high (> 90%): Good performance

### 4.4 Log Management

**Access Application Logs**:
1. Server: `/path/to/frappe-bench/logs/`
2. View recent errors: `tail -f logs/error.log`
3. View access logs: `tail -f logs/access.log`
4. Search logs: `grep "ERROR" logs/error.log`

**Log Retention**:
1. Configure log rotation in `/etc/logrotate.d/frappe`
2. Keep 30 days of logs
3. Compress old logs to save space
4. Archive critical logs separately

**Review Error Logs Daily**:
1. Check for patterns or recurring errors
2. Address issues causing repeated errors
3. Document unusual activity
4. Keep security audit trail

### 4.5 Bench Updates & Patches

**Check for Updates**:
1. Go to command line: `cd frappe-bench`
2. Check: `bench version`
3. Check available: `bench update-bench`

**Backup Before Update**:
1. **ALWAYS** backup before updating
2. `bench --site dialysis.local backup`
3. Verify backup created
4. Test restore on separate site

**Apply Updates**:
1. Notify users: System will be down 30-60 minutes
2. Stop services: `bench stop`
3. Update code: `cd apps/dialysis_center && git pull`
4. Install dependencies: `pip install -r requirements.txt`
5. Migrate database: `bench --site dialysis.local migrate`
6. Build assets: `bench build`
7. Start: `bench start`
8. Test key workflows
9. Notify users system is back online

### 4.6 Bench Housekeeping

**Clean Old Sessions** (monthly):
```bash
bench --site dialysis.local console
# In console:
frappe.db.sql("DELETE FROM tabSession WHERE creation < DATE_SUB(NOW(), INTERVAL 30 DAY)")
exit()
```

**Delete Old Files**:
1. Go to Tools > File Manager
2. View uploaded files
3. Delete unused files (saves disk space)

**Compress Old Backups**:
1. Server: `cd backups && gzip *.sql` (if not already gzipped)
2. Move old to archive: `mv *.sql.gz /backup/archive/`
3. Keep recent backups locally for quick restore

---

## Part 5: Troubleshooting & Support

### 5.1 Common Admin Issues

**"Service unavailable" error**:
1. Check if services running: `bench status`
2. If stopped: `bench start`
3. Check logs: `tail -f logs/error.log`
4. Resolve errors in logs
5. If persistent: Restart: `bench restart`

**Users cannot login**:
1. Check database: `bench console` → `frappe.db.count("User")`
2. Check session table: `SELECT COUNT(*) FROM tabSession WHERE `user` = 'user@email.com';`
3. Clear user sessions: `bench --site dialysis.local console` → `frappe.db.sql("DELETE FROM tabSession WHERE user = 'user@email.com'")`
4. User tries login again

**Page load very slow**:
1. Check database query performance (see 4.2 above)
2. Check server resources: `top` or `htop`
3. If memory full: Restart Frappe: `bench restart`
4. Check Redis: `redis-cli INFO`
5. If issues: Add more RAM or optimize queries

### 5.2 Getting Help

**Check Documentation**:
1. Dialysis Center app docs: Look in repo
2. Frappe docs: https://frappeframework.com/docs
3. Community forum: https://discuss.erpnext.com/

**Report Bug**:
1. Reproduce the issue
2. Gather information:
   - Frappe version
   - App version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error logs (relevant portion)
3. Create GitHub issue or contact support

**Contact Support**:
1. If critical system down
2. Gather: Description, logs, reproduction steps
3. Contact: support@dialysiscenter.app

---

## Part 6: Compliance & Auditing

### 6.1 HIPAA Compliance (if applicable in US)

**Access Controls**:
- Unique user IDs (email-based)
- Strong passwords (enforced)
- Multi-factor authentication (optional but recommended)
- Role-based permissions
- Session timeouts (30 min recommended for HIPAA)

**Audit Trails**:
- All document changes logged
- Access to patient records logged
- System tracks who viewed/modified what
- Retention: 6 years minimum

**Encryption**:
- HTTPS for web traffic (SSL/TLS)
- Database password encrypted
- API keys stored securely
- Backups encrypted at rest (recommended)

**Verify Compliance**:
1. Go to Setup > Audit Trail
2. View access log for patient records
3. Verify appropriate access only
4. Generate compliance report monthly

### 6.2 Audit Logging

**View Access Log**:
1. Go to Tools > Audit Trail
2. Filter by:
   - DocType (e.g., Patient)
   - User
   - Date range
   - Operation (Create/Update/Delete/Read)
3. View who accessed what when
4. Export for compliance review

**Export Audit Log**:
1. Go to Audit Trail
2. Click "Export"
3. Choose CSV/Excel
4. Download for records
5. Provide to auditors if requested

### 6.3 Data Privacy

**Privacy Settings**:
1. Configure what data is collected
2. Provide patient data download option
3. Implement data retention policy
4. Honor patient deletion requests
5. Document in Privacy Policy

**Consent Management**:
1. Obtain patient consent for:
   - Treatment data storage
   - Data sharing with insurance
   - Research use (if applicable)
2. Store consent records
3. Honor opt-out requests

---

## Quick Reference: Bench Commands

```bash
# General
bench --site dialysis.local console          # Python console
bench --site dialysis.local mariadb          # Database console
bench status                                  # Check service status
bench start                                   # Start all services
bench stop                                    # Stop all services
bench restart                                 # Restart all services

# Backups
bench --site dialysis.local backup            # Create backup
bench --site dialysis.local restore FILE.sql  # Restore backup

# Database
bench --site dialysis.local migrate           # Run migrations
bench --site dialysis.local reset-db          # Reset database (dangerous!)
bench --site dialysis.local clear-cache       # Clear cache

# Testing
bench --site dialysis.local run-tests         # Run all tests
bench --site dialysis.local run-tests --module dialysis_center  # Module tests

# Deployment
bench build                                   # Build assets
bench update-bench                            # Update Frappe
bench setup production                        # Setup for production
```

---

**End of Administrator Guide**

