# Docker Quick Start Guide - Frappe Framework

## 🚀 Quick Commands

### Start All Services
```bash
./docker-commands.sh start
```

### Stop All Services
```bash
./docker-commands.sh stop
```

### Check Service Health
```bash
./docker-commands.sh health
```

### View Logs
```bash
./docker-commands.sh logs
./docker-commands.sh logs mariadb
```

## 📊 Service Status

```bash
docker-compose ps
```

## 🗄️ Database Access

### MariaDB Shell
```bash
./docker-commands.sh mariadb
```

### Quick Query
```bash
docker exec frappe-mariadb mysql -u root -pfrappe@123 -e "SHOW DATABASES;"
```

## 🔴 Redis Access

### Redis Cache
```bash
docker exec -it frappe-redis-cache redis-cli
```

### Redis Queue
```bash
docker exec -it frappe-redis-queue redis-cli
```

## 🔧 Start Frappe with Docker Services

```bash
cd ~/frappe-bench
bench start
```

## 📦 Current Configuration

- **MariaDB:** localhost:3306
- **Redis Cache:** localhost:13000
- **Redis Queue:** localhost:11000
- **Redis SocketIO:** localhost:12000

## 🔑 Credentials

- **MariaDB Root:** frappe@123
- **Database Name:** _b2165c2f32b36e51
- **Database User:** _b2165c2f32b36e51
- **Database Password:** I4AuTAt1FS2TIsge
- **Administrator:** admin@123

---
For full documentation, see: `DOCKER_SETUP.md`
