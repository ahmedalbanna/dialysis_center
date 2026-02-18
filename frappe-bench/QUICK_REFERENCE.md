# Frappe Framework v15.100.1 - Quick Reference Guide

## Installation Summary
- **OS:** Ubuntu 24.04.4 LTS
- **Frappe Version:** 15.100.1
- **Installation Date:** February 18, 2026
- **Location:** `~/frappe-bench`

## Credentials

### Database (MariaDB)
- **Root User:** root
- **Root Password:** frappe@123
- **Port:** 3306
- **Default Host:** localhost

### Frappe Administrator
- **Email:** Administrator
- **Password:** admin@123
- **Access URL:** http://127.0.0.1:8000

### Database for Site 'frappe.local'
- **Database Name:** _b2165c2f32b36e51
- **Database User Password:** I4AuTAt1FS2TIsge (auto-generated)

## Running Services

### Start Development Server
```bash
cd ~/frappe-bench
bench start
```

### Service Ports
- **Web Server:** 8000 (http://127.0.0.1:8000)
- **WebSocket/SocketIO:** 9000 (ws://127.0.0.1:9000)
- **Redis Cache:** 13000
- **Redis Queue:** 11000
- **MariaDB:** 3306
- **File Watcher:** 6787

## Common Commands

### Site Management
```bash
# Create new site
bench new-site mysite.local --admin-password=PASSWORD

# List sites
ls ~/frappe-bench/sites/

# View site configuration
cat ~/frappe-bench/sites/frappe.local/site_config.json

# Access site database
bench --site frappe.local execute frappe.client.get list:User
```

### Application Management
```bash
# List installed apps
bench --site frappe.local list-apps

# Install app on site
bench --site frappe.local install-app app_name

# Get app
bench get-app app_name https://github.com/username/repo.git
```

### Development
```bash
# Run tests
bench --site frappe.local run-tests

# Run migrations
bench migrate

# Clear cache
bench clear-cache

# Build assets
bench build

# Watch and rebuild assets
bench watch
```

### Database Operations
```bash
# Access MariaDB directly
sudo mysql -u root -pfrappe@123

# Backup database
bench --site frappe.local backup

# Restore database
bench --site frappe.local restore backup_file.sql.gz
```

### Logs and Debugging
```bash
# View logs
bench logs

# Follow logs
bench logs -f

# Show running processes
ps aux | grep frappe

# Check bench version
bench version
```

## System Services

### MariaDB
```bash
# Status
sudo systemctl status mariadb

# Restart
sudo systemctl restart mariadb

# Stop
sudo systemctl stop mariadb

# Start
sudo systemctl start mariadb
```

### Redis
```bash
# Status
sudo systemctl status redis-server

# Restart
sudo systemctl restart redis-server

# Test connection
redis-cli ping
```

## Directory Structure

```
~/frappe-bench/
├── apps/                    # Installed applications
│   └── frappe/             # Core framework
├── env/                    # Python virtual environment
├── sites/                  # Site data
│   ├── frappe.local/       # Your site directory
│   ├── assets/             # Compiled assets
│   └── common_site_config.json
├── config/                 # Configuration files
│   ├── nginx.conf
│   └── supervisor.conf
├── logs/                   # Log files
├── Procfile               # Process definitions
└── patches.txt            # Applied patches
```

## Configuration Files

### Site Configuration
`~/frappe-bench/sites/frappe.local/site_config.json`

### Common Configuration
`~/frappe-bench/sites/common_site_config.json`

### Current Settings
- Redis Cache: redis://127.0.0.1:13000
- Redis Queue: redis://127.0.0.1:11000
- Redis SocketIO: redis://127.0.0.1:13000
- Gunicorn Workers: 9
- Background Workers: 1
- Webserver Port: 8000
- SocketIO Port: 9000
- Live Reload: Enabled

## Troubleshooting

### Server Won't Start
```bash
# Check if ports are in use
sudo lsof -i :8000
sudo lsof -i :3306
sudo lsof -i :6379

# View detailed logs
bench logs -f

# Kill existing processes and restart
pkill -f "bench start"
bench start
```

### Database Connection Error
```bash
# Verify MariaDB is running
sudo systemctl status mariadb

# Test connection
mysql -u root -pfrappe@123 -e "SELECT 1"

# Restart database
sudo systemctl restart mariadb
```

### Missing Dependencies
```bash
# Install missing Python packages
bench pip install -r apps/frappe/requirements.txt

# Install missing Node packages
cd ~/frappe-bench && yarn install

# Rebuild assets
bench build
```

### Redis Issues
```bash
# Check Redis connection
redis-cli ping

# View Redis info
redis-cli info

# Clear Redis cache
redis-cli FLUSHALL
```

## Performance Optimization (Development)

### Disable Hot Reload (if experiencing issues)
Edit `~/frappe-bench/sites/common_site_config.json`:
```json
"live_reload": false
```

### Increase Gunicorn Workers
Edit `~/frappe-bench/sites/common_site_config.json`:
```json
"gunicorn_workers": 4
```

## Security Notes

### Before Production Deployment
1. Change default admin password immediately
2. Configure firewall (allow only needed ports)
3. Set up SSL/TLS certificates
4. Disable live reload
5. Configure Nginx reverse proxy
6. Set up proper logging and monitoring
7. Configure regular backups
8. Harden database access (change root password)
9. Set up fail2ban or similar protection
10. Enable HTTPS only

### Change Admin Password
```bash
cd ~/frappe-bench
bench --site frappe.local set-admin-password
```

## Useful Links

- **Frappe Documentation:** https://frappeframework.com/docs/
- **GitHub Repository:** https://github.com/frappe/frappe
- **Community Forum:** https://discuss.erpnext.com/
- **Issue Tracker:** https://github.com/frappe/frappe/issues

## Next Steps

1. **Access the Application**
   - Open http://127.0.0.1:8000
   - Login with Administrator / admin@123

2. **Explore the Interface**
   - Check out the desk
   - Explore available modules
   - Create your first document

3. **Development**
   - Create a custom app: `bench new-app myapp`
   - Learn the architecture
   - Start building features

4. **Production Deployment**
   - Set up domain name
   - Configure SSL certificates
   - Set up Nginx
   - Configure supervisor/systemd
   - Set up automated backups

## Support

For issues and questions:
- Check logs: `bench logs -f`
- Visit forum: https://discuss.erpnext.com/
- Check documentation: https://frappeframework.com/docs/
- GitHub issues: https://github.com/frappe/frappe/issues

---
**Setup completed successfully! Happy developing! 🚀**
