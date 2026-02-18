# Frappe Framework v15.100.1 Installation Summary
## Ubuntu 24.04 LTS - Complete Setup

---

## 🎉 Installation Status: SUCCESS ✓

**Date:** February 18, 2026  
**System:** Ubuntu 24.04.4 LTS (Kernel 6.8.0-1007-gcp)  
**Installation Location:** `~/frappe-bench`  
**Total Setup Time:** ~15 minutes

---

## 📦 What Was Installed

### Core Components
| Component | Version | Status |
|-----------|---------|--------|
| Frappe Framework | 15.100.1 | ✓ Running |
| Frappe Bench | 5.29.1 | ✓ Active |
| MariaDB Server | 10.11.14 | ✓ Running |
| Redis Server | 7.0.15 | ✓ Running |
| Python | 3.12.12 | ✓ Virtual Env |
| Node.js | v22.14.0 | ✓ Pre-existing |
| npm | 10.9.2 | ✓ Pre-existing |
| Yarn | 1.22.22 | ✓ Installed |
| Git | 2.42.0 | ✓ Pre-existing |

### Supporting Tools
- **wkhtmltopdf** - PDF generation
- **Supervisor** - Process management
- **Cron daemon** - Scheduled tasks
- **Build tools** - Compilation support
- **Development libraries** - libssl-dev, libffi-dev, libmariadb-dev

---

## 🚀 Quick Start

### Start the Development Server
```bash
cd ~/frappe-bench
bench start
```

### Access the Application
- **URL:** http://127.0.0.1:8000 or http://10.128.0.37:8000
- **Username:** Administrator
- **Password:** admin@123

### Create Additional Sites
```bash
bench new-site mysite.local --admin-password=PASSWORD
```

---

## 🔑 Important Credentials

### MariaDB Database
```
Host: localhost
Port: 3306
Root User: root
Root Password: frappe@123
```

### Frappe Site (frappe.local)
```
Database Name: _b2165c2f32b36e51
Database Password: I4AuTAt1FS2TIsge (auto-generated)
Admin User: Administrator
Admin Password: admin@123
```

---

## 🔌 Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| Web Server | 8000 | Frappe web interface |
| WebSocket | 9000 | Real-time updates |
| MariaDB | 3306 | Database server |
| Redis (main) | 6379 | Main cache server |
| Redis Cache | 13000 | Asset caching |
| Redis Queue | 11000 | Background jobs |
| File Watcher | 6787 | Asset changes |

---

## 📁 Directory Structure

```
~/frappe-bench/
├── apps/
│   └── frappe/              # Frappe framework source
├── env/                     # Python virtual environment
├── sites/
│   ├── frappe.local/        # Your site
│   ├── assets/              # Compiled assets
│   └── common_site_config.json
├── config/                  # Server configurations
├── logs/                    # Application logs
├── Procfile                 # Process definitions
└── patches.txt              # Applied patches

Documentation Files:
├── QUICK_REFERENCE.md       # Common commands
├── INSTALLATION_VERIFICATION.md  # Verification report
└── INSTALLATION_COMPLETE.txt     # Setup summary
```

---

## 🛠️ Common Commands Reference

### Site Management
```bash
# Create new site
bench new-site sitename.local --admin-password=PASSWORD

# List sites
ls ~/frappe-bench/sites/

# View site configuration
cat ~/frappe-bench/sites/frappe.local/site_config.json
```

### Application Management
```bash
# Install an app on site
bench --site frappe.local install-app app_name

# Get (clone) an application
bench get-app app_name https://github.com/user/repo.git

# List apps on site
bench --site frappe.local list-apps
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

# Watch for changes
bench watch
```

### Database
```bash
# Backup site
bench --site frappe.local backup

# Access MariaDB
sudo mysql -u root -pfrappe@123

# Execute SQL
bench --site frappe.local execute "SELECT COUNT(*) FROM `tabUser`"
```

### Logs
```bash
# View logs (follow mode)
bench logs -f

# View specific logs
tail -f ~/frappe-bench/logs/web.log
```

---

## ⚙️ Service Management

### MariaDB
```bash
# Status
sudo systemctl status mariadb

# Start/Stop
sudo systemctl start mariadb
sudo systemctl stop mariadb

# Restart
sudo systemctl restart mariadb

# Enable on boot
sudo systemctl enable mariadb
```

### Redis
```bash
# Status
sudo systemctl status redis-server

# Start/Stop
sudo systemctl start redis-server
sudo systemctl stop redis-server

# Restart
sudo systemctl restart redis-server

# Test connection
redis-cli ping
```

### Cron
```bash
# Start the cron daemon
sudo systemctl start cron

# Check status
sudo systemctl status cron
```

---

## 🔒 Security Configuration

### Current Status
- **Mode:** Development
- **Live Reload:** Enabled
- **Debug Mode:** Enabled
- **Default Credentials:** Active
- **⚠️ Not production-ready without hardening**

### Before Production Deployment

1. **Change Passwords**
   ```bash
   # Change MariaDB root password
   sudo mysql -u root -pfrappe@123
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_strong_password';
   
   # Change Frappe admin password
   bench --site frappe.local set-admin-password
   ```

2. **Configure SSL/TLS**
   ```bash
   # Install Certbot
   sudo apt-get install certbot python3-certbot-nginx
   
   # Get certificate
   sudo certbot certonly --standalone -d yourdomain.com
   ```

3. **Set Up Nginx Reverse Proxy**
   ```bash
   bench setup nginx
   sudo systemctl restart nginx
   ```

4. **Configure Supervisor**
   ```bash
   bench setup supervisor
   sudo systemctl enable supervisor
   sudo systemctl start supervisor
   ```

5. **Harden Security**
   - Configure firewall rules
   - Disable live reload
   - Set up fail2ban
   - Enable HTTPS only
   - Configure backups

---

## 📊 System Information

### OS
- **Distribution:** Ubuntu 24.04.4 LTS
- **Kernel:** 6.8.0-1007-gcp
- **Architecture:** x86_64

### Python Environment
- **Python:** 3.12.12 (in virtual environment)
- **Location:** `~/frappe-bench/env/bin/python`
- **Package Manager:** pip 26.0.1

### Node.js Environment
- **Node.js:** v22.14.0
- **npm:** 10.9.2
- **Yarn:** 1.22.22

### Database
- **MariaDB:** 10.11.14-MariaDB
- **Character Set:** utf8mb4
- **Collation:** utf8mb4_unicode_ci

### Cache & Queue
- **Redis:** 7.0.15
- **Cache Port:** 13000
- **Queue Port:** 11000

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is in use
sudo lsof -i :8000

# View detailed logs
bench logs -f

# Kill existing processes and restart
pkill -f "bench start"
bench start
```

### Database Connection Error
```bash
# Check MariaDB status
sudo systemctl status mariadb

# Test database connection
mysql -u root -pfrappe@123 -e "SELECT 1"

# Restart MariaDB
sudo systemctl restart mariadb
```

### Redis Connection Issues
```bash
# Check Redis status
sudo systemctl status redis-server

# Test connection
redis-cli ping

# View Redis info
redis-cli info

# Clear Redis cache
redis-cli FLUSHALL
```

### Missing Dependencies
```bash
# Install Python dependencies
bench pip install -r apps/frappe/requirements.txt

# Install Node dependencies
cd ~/frappe-bench && yarn install

# Rebuild assets
bench build
```

### File Permissions
```bash
# Fix ownership
sudo chown -R $USER:$USER ~/frappe-bench

# Fix directory permissions
find ~/frappe-bench -type d -exec chmod 755 {} \;
```

---

## 📚 Documentation Files

The following documentation files have been created in `~/frappe-bench/`:

1. **QUICK_REFERENCE.md** (6.2 KB)
   - Common commands
   - Configuration details
   - Service management
   - Troubleshooting tips

2. **INSTALLATION_VERIFICATION.md** (6.8 KB)
   - Component verification checklist
   - Configuration summary
   - Service health checks
   - Feature verification

3. **INSTALLATION_COMPLETE.txt** (8.8 KB)
   - Installation summary
   - Next steps
   - Security recommendations
   - Support resources

4. **This file:** FRAPPE_SETUP_SUMMARY.md (in home directory)
   - Complete overview
   - Installation details
   - Credentials and ports
   - Commands and troubleshooting

---

## 🌐 Useful Resources

### Official Documentation
- **Frappe Framework:** https://frappeframework.com/docs/
- **API Documentation:** https://frappeframework.com/api/
- **GitHub Repository:** https://github.com/frappe/frappe

### Community Support
- **Discussion Forum:** https://discuss.erpnext.com/
- **GitHub Issues:** https://github.com/frappe/frappe/issues
- **Discord Community:** https://discord.gg/frappe

### Local Resources
- **Quick Reference:** `~/frappe-bench/QUICK_REFERENCE.md`
- **Verification Report:** `~/frappe-bench/INSTALLATION_VERIFICATION.md`
- **Completion Summary:** `~/frappe-bench/INSTALLATION_COMPLETE.txt`

---

## ✅ Installation Checklist

- [x] System requirements verified
- [x] Dependencies installed
- [x] MariaDB installed and running
- [x] Redis installed and running
- [x] Frappe Framework installed
- [x] Bench utility installed
- [x] Python virtual environment created
- [x] Node modules installed
- [x] Assets compiled
- [x] Translations compiled
- [x] Site 'frappe.local' created
- [x] Admin user configured
- [x] Development server verified
- [x] Documentation created
- [x] Services enabled for auto-start

---

## 🎯 Next Steps

### Immediate (Development)
1. Start the server: `bench start`
2. Access http://127.0.0.1:8000
3. Login with Administrator credentials
4. Explore the interface
5. Create test documents

### Short Term (Learning)
1. Study Frappe architecture
2. Create custom apps: `bench new-app myapp`
3. Design DocTypes
4. Implement business logic
5. Write unit tests

### Before Production
1. Change all default passwords
2. Set up SSL/TLS certificates
3. Configure Nginx reverse proxy
4. Set up automated backups
5. Configure monitoring and logging
6. Harden system security
7. Test disaster recovery procedures
8. Document custom configurations

---

## 📝 Notes

- The development server includes a debugger (PIN: 106-127-527)
- Live reload is enabled for faster development
- All services are configured to auto-start on system reboot
- Redis memory overcommit warning is non-critical for development
- Supervisor is installed but uses Honcho for development
- Create additional sites as needed for testing

---

## 🚀 You're All Set!

Your Frappe Framework installation is complete and ready for development.

**To start coding:**
```bash
cd ~/frappe-bench
bench start
```

Then open your browser to: **http://127.0.0.1:8000**

For detailed documentation, see the files in `~/frappe-bench/`

**Happy coding!** 🎉

---

*Last Updated: February 18, 2026*  
*Installation Version: Frappe 15.100.1 on Ubuntu 24.04 LTS*
