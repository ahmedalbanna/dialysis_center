# Docker Compose Setup for Frappe Framework

This setup provides containerized MariaDB and Redis services for Frappe Framework development.

## 📦 Services Included

### MariaDB 10.11.14
- **Container Name:** `frappe-mariadb`
- **Port:** `3306`
- **Root Password:** `frappe@123`
- **Database:** `_b2165c2f32b36e51`
- **User:** `_b2165c2f32b36e51`
- **Password:** `I4AuTAt1FS2TIsge`
- **Features:**
  - UTF8MB4 character set
  - Optimized InnoDB settings
  - 1GB buffer pool
  - Slow query logging
  - Health checks
  - Persistent volumes

### Redis Cache
- **Container Name:** `frappe-redis-cache`
- **Port:** `13000`
- **Type:** LRU cache (512MB max memory)
- **Persistence:** Disabled (in-memory only)

### Redis Queue
- **Container Name:** `frappe-redis-queue`
- **Port:** `11000`
- **Type:** Persistent queue
- **Persistence:** AOF (Append-Only File)

### Redis SocketIO
- **Container Name:** `frappe-redis-socketio`
- **Port:** `12000`
- **Type:** Real-time messaging
- **Persistence:** Disabled

## 🚀 Quick Start

### Using Helper Script (Recommended)

```bash
# Start all services
./docker-commands.sh start

# Check service status
./docker-commands.sh status

# Check service health
./docker-commands.sh health

# View logs
./docker-commands.sh logs

# View logs for specific service
./docker-commands.sh logs mariadb
```

### Using Docker Compose Directly

```bash
# Start all services in background
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🔧 Management Commands

### Start Services
```bash
./docker-commands.sh start
# or
docker-compose up -d
```

### Stop Services
```bash
./docker-commands.sh stop
# or
docker-compose down
```

### Restart Services
```bash
./docker-commands.sh restart
# or
docker-compose restart
```

### Check Status
```bash
./docker-commands.sh status
# or
docker-compose ps
```

### Check Health
```bash
./docker-commands.sh health
```

### View Logs
```bash
# All services
./docker-commands.sh logs

# Specific service
./docker-commands.sh logs mariadb
./docker-commands.sh logs redis-cache
./docker-commands.sh logs redis-queue
./docker-commands.sh logs redis-socketio
```

## 🗄️ Database Management

### Access MariaDB Shell
```bash
./docker-commands.sh mariadb
# or
docker exec -it frappe-mariadb mysql -u root -pfrappe@123
```

### Create Database Backup
```bash
./docker-commands.sh backup
# Backup saved to: ./backups/mariadb_backup_YYYYMMDD_HHMMSS.sql
```

### Restore Database Backup
```bash
./docker-commands.sh restore ./backups/mariadb_backup_20260218_123456.sql
```

### Import SQL File
```bash
docker exec -i frappe-mariadb mysql -u root -pfrappe@123 < your_backup.sql
```

### Export Specific Database
```bash
docker exec frappe-mariadb mysqldump -u root -pfrappe@123 _b2165c2f32b36e51 > database_backup.sql
```

## 🔴 Redis Management

### Access Redis Cache Shell
```bash
./docker-commands.sh redis
# or
docker exec -it frappe-redis-cache redis-cli
```

### Access Other Redis Instances
```bash
# Redis Queue
docker exec -it frappe-redis-queue redis-cli

# Redis SocketIO
docker exec -it frappe-redis-socketio redis-cli
```

### Redis Common Commands
```bash
# Inside redis-cli:
PING                    # Test connection
INFO                    # Server info
DBSIZE                  # Number of keys
KEYS *                  # List all keys (use carefully in production)
FLUSHALL                # Clear all data (WARNING: destructive)
MONITOR                 # Monitor all commands in real-time
```

## 📊 Monitoring

### Check Container Stats
```bash
docker stats frappe-mariadb frappe-redis-cache frappe-redis-queue frappe-redis-socketio
```

### View Service Health
```bash
docker-compose ps
```

### MariaDB Health Check
```bash
docker exec frappe-mariadb mysqladmin ping -h localhost -u root -pfrappe@123
```

### Redis Health Check
```bash
docker exec frappe-redis-cache redis-cli ping
docker exec frappe-redis-queue redis-cli ping
docker exec frappe-redis-socketio redis-cli ping
```

## 🔧 Frappe Configuration

Update your Frappe site configuration to use Docker services:

### Update `frappe-bench/sites/common_site_config.json`:
```json
{
  "db_host": "localhost",
  "db_port": 3306,
  "redis_cache": "redis://localhost:13000",
  "redis_queue": "redis://localhost:11000",
  "redis_socketio": "redis://localhost:12000"
}
```

### Update `frappe-bench/sites/frappe.local/site_config.json`:
```json
{
  "db_name": "_b2165c2f32b36e51",
  "db_password": "I4AuTAt1FS2TIsge",
  "db_user": "_b2165c2f32b36e51",
  "db_host": "localhost",
  "db_port": 3306
}
```

### Restart Frappe Bench
```bash
cd ~/frappe-bench
bench restart
```

## 📁 Data Persistence

All data is stored in Docker volumes:

- **mariadb_data:** MariaDB database files
- **redis_cache_data:** Redis cache data (volatile)
- **redis_queue_data:** Redis queue data (persistent)
- **redis_socketio_data:** Redis SocketIO data

### List Volumes
```bash
docker volume ls | grep frappe
```

### Inspect Volume
```bash
docker volume inspect frappe_mariadb_data
```

### Backup Volumes
```bash
# MariaDB
docker run --rm -v frappe_mariadb_data:/data -v $(pwd)/backups:/backup ubuntu tar czf /backup/mariadb_volume_backup.tar.gz -C /data .

# Redis Queue
docker run --rm -v frappe_redis_queue_data:/data -v $(pwd)/backups:/backup ubuntu tar czf /backup/redis_queue_volume_backup.tar.gz -C /data .
```

## 🧹 Cleanup

### Remove All Containers and Volumes
```bash
./docker-commands.sh cleanup
# or
docker-compose down -v
```

### Remove Only Containers (Keep Data)
```bash
docker-compose down
```

### Remove Unused Docker Resources
```bash
docker system prune -a --volumes
```

## 🔒 Security Considerations

### Production Deployment

1. **Change Default Passwords:**
   - Update `.env` file with strong passwords
   - Never commit `.env` to version control

2. **Network Security:**
   - Don't expose database ports publicly
   - Use Docker networks for inter-container communication
   - Consider using `127.0.0.1:3306` instead of `0.0.0.0:3306`

3. **Firewall Rules:**
   ```bash
   # Allow only localhost
   sudo ufw allow from 127.0.0.1 to any port 3306
   sudo ufw allow from 127.0.0.1 to any port 13000
   ```

4. **SSL/TLS:**
   - Configure MariaDB SSL certificates
   - Use encrypted Redis connections in production

## 🐛 Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs mariadb

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart mariadb
```

### Cannot Connect to MariaDB
```bash
# Check if MariaDB is running
docker exec frappe-mariadb mysqladmin ping -u root -pfrappe@123

# Check network connectivity
docker exec frappe-mariadb netstat -tlnp | grep 3306

# Check MariaDB error log
docker-compose logs mariadb
```

### Redis Connection Issues
```bash
# Test Redis connection
docker exec frappe-redis-cache redis-cli ping

# Check Redis info
docker exec frappe-redis-cache redis-cli info
```

### Permission Denied Errors
```bash
# Fix file permissions
chmod 644 .env
chmod 755 docker-commands.sh
```

### Port Already in Use
```bash
# Find what's using the port
sudo lsof -i :3306
sudo lsof -i :13000

# Kill the process or change port in docker-compose.yml
```

## 📝 Environment Variables

Edit `.env` file to customize:

```env
# MariaDB
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password

# Redis Ports
REDIS_CACHE_PORT=13000
REDIS_QUEUE_PORT=11000
REDIS_SOCKETIO_PORT=12000
```

## 🔄 Updating Services

### Update to Latest Images
```bash
docker-compose pull
docker-compose up -d
```

### Update Specific Service
```bash
docker-compose pull mariadb
docker-compose up -d mariadb
```

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MariaDB Docker Hub](https://hub.docker.com/_/mariadb)
- [Redis Docker Hub](https://hub.docker.com/_/redis)
- [Frappe Framework Documentation](https://frappeframework.com/docs)

## 🆘 Support

For issues and questions:
- Check container logs: `./docker-commands.sh logs`
- Verify health: `./docker-commands.sh health`
- Review MariaDB configuration: `mariadb-config/frappe.cnf`
- Check Frappe bench logs: `~/frappe-bench/logs/`

---

**Created:** 2026-02-18
**Docker Compose Version:** 3.8
**Services:** MariaDB 10.11.14, Redis 7.0.15
