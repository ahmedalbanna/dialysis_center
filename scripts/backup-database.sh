#!/bin/bash
#
# Automated Database Backup Script for Frappe
# This script creates timestamped backups of MariaDB database
#

set -e

# Configuration
BACKUP_DIR="./backups/auto"
BACKUP_RETENTION_DAYS=7
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-frappe@123}"
DB_NAME="${MYSQL_DATABASE:-_b2165c2f32b36e51}"
CONTAINER_NAME="frappe-mariadb"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

echo_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

echo_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate backup filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/frappe_db_${TIMESTAMP}.sql.gz"
BACKUP_INFO="$BACKUP_DIR/frappe_db_${TIMESTAMP}.info"

echo_info "Starting database backup..."

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo_error "MariaDB container is not running!"
fi

# Create backup
echo_info "Backing up database: $DB_NAME"
docker exec "$CONTAINER_NAME" mysqldump \
    -u root \
    -p"$MYSQL_ROOT_PASSWORD" \
    --single-transaction \
    --quick \
    --lock-tables=false \
    --routines \
    --triggers \
    --events \
    "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    # Get backup size
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    
    # Create backup info file
    cat > "$BACKUP_INFO" << EOF
Backup Information
==================
Date: $(date)
Database: $DB_NAME
Backup File: $BACKUP_FILE
Backup Size: $BACKUP_SIZE
Container: $CONTAINER_NAME
Host: $(hostname)
EOF

    echo_success "Backup completed successfully!"
    echo_info "Backup file: $BACKUP_FILE"
    echo_info "Backup size: $BACKUP_SIZE"
    
    # Count tables in backup
    TABLES=$(zcat "$BACKUP_FILE" | grep "CREATE TABLE" | wc -l)
    echo_info "Tables backed up: $TABLES"
else
    echo_error "Backup failed!"
fi

# Clean up old backups
echo_info "Cleaning up old backups (keeping last $BACKUP_RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "frappe_db_*.sql.gz" -type f -mtime +$BACKUP_RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "frappe_db_*.info" -type f -mtime +$BACKUP_RETENTION_DAYS -delete

# List recent backups
echo ""
echo_info "Recent backups:"
ls -lht "$BACKUP_DIR"/frappe_db_*.sql.gz 2>/dev/null | head -5 | awk '{print "  " $9 " (" $5 ")"}'

echo ""
echo_success "Backup process completed!"
