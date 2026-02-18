# Nginx & Automated Backup Guide for Frappe

## 🚀 Complete Docker Setup

This setup includes:
- ✅ **Nginx** - Reverse proxy and load balancer
- ✅ **MariaDB 10.11.14** - Database server
- ✅ **Redis Cache, Queue, SocketIO** - Caching and messaging
- ✅ **Automated Backups** - Scheduled database backups
- ✅ **Automated Restore** - Easy database restoration

---

## 📦 Services Overview

### Nginx (Port 80, 443)
- **Container:** `frappe-nginx`
- **Image:** nginx:1.24-alpine
- **Network Mode:** host (for easy localhost communication)
- **Features:**
  - Reverse proxy to Frappe (port 8000)
  - Socket.IO proxy (port 9000)
  - Static file serving
  - Rate limiting (10 req/s)
  - Gzip compression
  - Security headers

### MariaDB (Port 3306)
- **Container:** `frappe-mariadb`
- **Credentials:** root / frappe@123
- **Optimizations:** 1GB buffer pool, UTF8MB4

### Redis Services
- **Cache (Port 13000):** LRU cache, 512MB
- **Queue (Port 11000):** Persistent queue with AOF
- **SocketIO (Port 12000):** Real-time messaging

---

## 🎯 Quick Start

### 1. Start All Services
```bash
./docker-commands.sh start
```

### 2. Start Frappe
```bash
cd ~/frappe-bench
bench start
```

### 3. Access Application
- **Via Nginx:** http://localhost or http://10.128.0.37
- **Direct:** http://localhost:8000
- **Credentials:** Administrator / admin@123

---

## 🔧 Nginx Management

### View Nginx Status
```bash
docker-compose ps
./docker-commands.sh status
```

### Check Nginx Configuration
```bash
docker exec frappe-nginx nginx -t
```

### Reload Nginx (after config changes)
```bash
./docker-commands.sh nginx-reload
```

### View Nginx Logs
```bash
# Access logs
./docker-commands.sh nginx-logs

# Error logs
docker logs frappe-nginx

# All logs
docker-compose logs -f nginx
```

### Access Nginx Shell
```bash
./docker-commands.sh nginx
```

### Edit Nginx Configuration
```bash
# Edit main config
nano nginx-config/nginx.conf

# Edit Frappe site config
nano nginx-config/frappe.conf

# Reload after changes
./docker-commands.sh nginx-reload
```

---

## 💾 Backup & Restore

### Manual Backup

#### Create Backup
```bash
./backup-database.sh
```

**Output:**
- Backup file: `./backups/auto/frappe_db_YYYYMMDD_HHMMSS.sql.gz`
- Backup info: `./backups/auto/frappe_db_YYYYMMDD_HHMMSS.info`
- Compressed SQL dump with all tables

#### Backup Features
- ✅ Timestamped backups
- ✅ Gzip compression
- ✅ Single transaction (consistent snapshot)
- ✅ Includes routines, triggers, events
- ✅ Auto cleanup (keeps 7 days)
- ✅ Backup info file with metadata

### Manual Restore

#### Interactive Restore
```bash
./restore-database.sh
```

This will:
1. List all available backups
2. Let you choose which backup to restore
3. Create a pre-restore backup
4. Restore the selected backup
5. Verify the restoration

#### Command Line Restore
```bash
# Restore specific backup
./restore-database.sh ./backups/auto/frappe_db_20260218_232633.sql.gz

# Or just the filename
./restore-database.sh frappe_db_20260218_232633.sql.gz
```

#### Restore Features
- ✅ Interactive backup selection
- ✅ Pre-restore backup (safety)
- ✅ Database drop and recreate
- ✅ Verification of restored tables
- ✅ Warning prompts

---

## ⏰ Automated Backups

### Setup Automated Backups
```bash
./setup-auto-backup.sh
```

**Interactive Setup Options:**
1. Every hour
2. Every 6 hours
3. Daily at midnight
4. Daily at specific time
5. Custom cron expression

**What it does:**
- Creates cron job for scheduled backups
- Optional: Creates systemd timer
- Runs test backup
- Logs to `./backups/auto/backup.log`

### View Scheduled Backups
```bash
# View cron jobs
crontab -l

# View systemd timers (if configured)
systemctl --user list-timers
sudo systemctl list-timers | grep frappe
```

### View Backup Logs
```bash
# Real-time log
tail -f ./backups/auto/backup.log

# Last 50 lines
tail -50 ./backups/auto/backup.log

# Search for errors
grep -i error ./backups/auto/backup.log
```

### Manage Automated Backups
```bash
# Edit cron schedule
crontab -e

# Remove automated backups
crontab -l | grep -v "backup-database.sh" | crontab -

# Stop systemd timer
sudo systemctl stop frappe-backup.timer
sudo systemctl disable frappe-backup.timer
```

---

## 📊 Backup Management

### List All Backups
```bash
ls -lht ./backups/auto/*.sql.gz
```

### Check Backup Size
```bash
du -sh ./backups/auto/
```

### View Backup Info
```bash
cat ./backups/auto/frappe_db_20260218_232633.info
```

### Cleanup Old Backups
```bash
# Remove backups older than 7 days (automatic in backup script)
find ./backups/auto -name "frappe_db_*.sql.gz" -mtime +7 -delete

# Remove backups older than 30 days
find ./backups/auto -name "frappe_db_*.sql.gz" -mtime +30 -delete

# Keep only last 10 backups
ls -t ./backups/auto/frappe_db_*.sql.gz | tail -n +11 | xargs rm -f
```

### Copy Backup to Remote Server
```bash
# Using scp
scp ./backups/auto/frappe_db_20260218_232633.sql.gz user@remote:/path/to/backups/

# Using rsync
rsync -avz ./backups/auto/ user@remote:/path/to/backups/
```

---

## 🔒 Nginx Configuration Details

### Rate Limiting
- **Zone:** frappe (10MB memory)
- **Rate:** 10 requests/second
- **Burst:** 20 requests
- **Connections:** Max 10 per IP

### Security Headers
```nginx
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

### Proxy Settings
- **Timeouts:** 300 seconds (5 minutes)
- **Buffering:** Disabled for real-time responses
- **HTTP Version:** 1.1
- **WebSocket:** Enabled for Socket.IO

### Static File Caching
- **Assets:** 1 year cache
- **Files:** 1 hour cache
- **Gzip:** Enabled for text/json/css/js

---

## 🛠️ Troubleshooting

### Nginx Won't Start
```bash
# Check logs
docker logs frappe-nginx

# Verify configuration
docker exec frappe-nginx nginx -t

# Check if port 80 is in use
sudo lsof -i :80

# Stop system nginx if running
sudo systemctl stop nginx
```

### 502 Bad Gateway
```bash
# Check if Frappe is running
curl http://localhost:8000

# Start Frappe if needed
cd ~/frappe-bench
bench start

# Check logs
./docker-commands.sh logs nginx
```

### Backup Fails
```bash
# Check if MariaDB is running
docker ps | grep mariadb

# Check disk space
df -h

# Test connection
docker exec frappe-mariadb mysql -u root -pfrappe@123 -e "SELECT 1;"

# Check permissions
ls -la ./backups/auto/
```

### Restore Fails
```bash
# Check backup file integrity
gunzip -t ./backups/auto/frappe_db_20260218_232633.sql.gz

# View backup contents
zcat ./backups/auto/frappe_db_20260218_232633.sql.gz | head -50

# Check MariaDB connection
docker exec frappe-mariadb mysql -u root -pfrappe@123 -e "SHOW DATABASES;"
```

### Can't Access Frappe via Nginx
```bash
# Test Nginx
curl -I http://localhost

# Test Frappe directly
curl -I http://localhost:8000

# Check if default.conf is removed
docker exec frappe-nginx ls -la /etc/nginx/conf.d/

# Remove if exists
docker exec frappe-nginx rm -f /etc/nginx/conf.d/default.conf
docker exec frappe-nginx nginx -s reload
```

---

## 📈 Monitoring

### Check All Services Health
```bash
./docker-commands.sh health
```

### Monitor Resource Usage
```bash
# All containers
docker stats

# Specific containers
docker stats frappe-nginx frappe-mariadb frappe-redis-cache
```

### View Real-time Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f nginx
docker-compose logs -f mariadb
```

### Check Backup Success Rate
```bash
# Count successful backups
grep "Backup completed successfully" ./backups/auto/backup.log | wc -l

# Check for failures
grep -i "error\|failed" ./backups/auto/backup.log
```

---

## 🔄 Common Tasks

### Update Nginx Configuration
```bash
# 1. Edit config
nano nginx-config/frappe.conf

# 2. Test config
docker exec frappe-nginx nginx -t

# 3. Reload nginx
./docker-commands.sh nginx-reload
```

### Migrate to New Server
```bash
# On old server
./backup-database.sh

# Copy backup to new server
scp ./backups/auto/frappe_db_*.sql.gz newserver:/path/

# On new server
./restore-database.sh /path/frappe_db_*.sql.gz
```

### Restore from Specific Point in Time
```bash
# List backups by date
ls -lt ./backups/auto/frappe_db_*.sql.gz

# Restore specific backup
./restore-database.sh frappe_db_20260218_120000.sql.gz
```

### Test Backup Integrity
```bash
# Test gzip file
gunzip -t ./backups/auto/frappe_db_20260218_232633.sql.gz

# Count tables in backup
zcat ./backups/auto/frappe_db_20260218_232633.sql.gz | grep "CREATE TABLE" | wc -l

# View database structure
zcat ./backups/auto/frappe_db_20260218_232633.sql.gz | grep "CREATE TABLE" | head -20
```

---

## 🎛️ Advanced Configuration

### Custom Backup Retention
Edit `backup-database.sh`:
```bash
BACKUP_RETENTION_DAYS=30  # Keep 30 days instead of 7
```

### Backup to External Storage
```bash
# Add to backup-database.sh
# After backup creation, sync to S3
aws s3 sync ./backups/auto/ s3://your-bucket/frappe-backups/

# Or sync to remote server
rsync -avz ./backups/auto/ user@backup-server:/backups/frappe/
```

### Enable Nginx SSL
```bash
# 1. Create SSL directory
mkdir -p nginx-config/ssl

# 2. Generate self-signed certificate (for testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx-config/ssl/frappe.key \
  -out nginx-config/ssl/frappe.crt

# 3. Edit nginx-config/frappe.conf to add SSL server block
# 4. Reload nginx
./docker-commands.sh nginx-reload
```

### Custom Nginx Logs Location
Edit `docker-compose.yml`:
```yaml
volumes:
  - /var/log/frappe-nginx:/var/log/nginx
```

---

## 📋 File Structure

```
.
├── docker-compose.yml              # Docker services configuration
├── .env                            # Environment variables
├── docker-commands.sh              # Service management script
├── backup-database.sh              # Manual backup script
├── restore-database.sh             # Manual restore script
├── setup-auto-backup.sh            # Automated backup setup
├── nginx-config/
│   ├── nginx.conf                  # Main Nginx config
│   ├── frappe.conf                 # Frappe site config
│   └── ssl/                        # SSL certificates (optional)
├── mariadb-config/
│   └── frappe.cnf                  # MariaDB optimizations
└── backups/
    └── auto/                       # Automatic backups
        ├── frappe_db_*.sql.gz      # Backup files
        ├── frappe_db_*.info        # Backup metadata
        └── backup.log              # Backup logs
```

---

## 🔐 Security Best Practices

### 1. Change Default Passwords
```bash
# Edit .env file
nano .env

# Update:
MYSQL_ROOT_PASSWORD=your_strong_password
MYSQL_PASSWORD=your_strong_password
```

### 2. Restrict Backup Access
```bash
chmod 700 ./backups
chmod 600 ./backups/auto/*.sql.gz
```

### 3. Encrypt Backups
```bash
# Encrypt backup
gpg -c ./backups/auto/frappe_db_20260218_232633.sql.gz

# Decrypt backup
gpg -d frappe_db_20260218_232633.sql.gz.gpg | gunzip | docker exec -i frappe-mariadb mysql ...
```

### 4. Use Firewall
```bash
# Allow only localhost for database
sudo ufw allow from 127.0.0.1 to any port 3306
```

### 5. Regular Security Updates
```bash
# Update Docker images
docker-compose pull
docker-compose up -d
```

---

## 📞 Support & Documentation

### Quick Reference
- **Start services:** `./docker-commands.sh start`
- **Backup database:** `./backup-database.sh`
- **Restore database:** `./restore-database.sh`
- **Check health:** `./docker-commands.sh health`
- **View logs:** `./docker-commands.sh logs`

### Full Documentation
- Main setup: `DOCKER_SETUP.md`
- Quick start: `DOCKER_QUICK_START.md`
- This guide: `NGINX_BACKUP_GUIDE.md`

### Verify Installation
```bash
./verify-docker-setup.sh
```

---

**Last Updated:** 2026-02-18  
**Version:** 1.0  
**Services:** Nginx 1.24, MariaDB 10.11.14, Redis 7.0.15
