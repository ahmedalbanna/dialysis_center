# Frappe Installer Memory File

## Quick Facts
- **Specialty**: Frappe framework setup on Linux, system dependency installation, virtual environment config, Bench initialization, site creation, service configuration, verification
- **Primary Tools**: Bash/shell scripts, apt-get, systemctl, Bench CLI
- **Common Tasks**: Fresh Frappe install, dependency setup, site creation, MariaDB/Redis setup, production configuration
- **Estimated Task Time**: 30-90 minutes depending on environment

---

## System Requirements

### Operating System
- Ubuntu 20.04+ (recommended)
- Debian 10+
- Other Linux distributions (CentOS, AlmaLinux, etc.)

### Hardware Minimum
- CPU: 2 cores
- RAM: 4 GB (8 GB recommended)
- Disk: 20 GB free space
- Network: Internet connection for package downloads

### System Dependencies
```
- Python 3.10+ (3.12.x current)
- Node.js 18+ (22.x current)
- MariaDB 10.6+ (10.11.x current)
- Redis 6.0+ (7.0+ recommended)
- wkhtmltopdf (for PDF generation)
- Git
- Build tools (gcc, make, etc.)
```

---

## Installation Steps

### Step 1: System Preparation

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install system dependencies
sudo apt-get install -y \
	curl \
	wget \
	git \
	python3 \
	python3-dev \
	python3-pip \
	python3-venv \
	build-essential \
	libssl-dev \
	libffi-dev \
	redis-server \
	mariadb-server \
	mariadb-client \
	wkhtmltopdf \
	xvfb \
	fontconfig \
	libfreetype6 \
	libjpeg62-turbo \
	libpng16-16 \
	libx11-6 \
	libxcb1 \
	libxext6 \
	libxrender1

# Install Node.js (via NodeSource)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installations
python3 --version
node --version
mysql --version
redis-cli --version
```

### Step 2: MariaDB Configuration

```bash
# Secure MariaDB installation
sudo mysql_secure_installation

# Or manually configure
sudo mysql -u root -p << EOF
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
