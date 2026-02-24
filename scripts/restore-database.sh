#!/bin/bash
#
# Automated Database Restore Script for Frappe
# This script restores database from backup files
#

set -e

# Configuration
BACKUP_DIR="./backups/auto"
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-frappe@123}"
DB_NAME="${MYSQL_DATABASE:-_b2165c2f32b36e51}"
CONTAINER_NAME="frappe-mariadb"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

echo_warning() {
    echo -e "${RED}⚠ $1${NC}"
}

# Function to list available backups
list_backups() {
    echo_info "Available backups:"
    echo ""
    
    if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A $BACKUP_DIR/frappe_db_*.sql.gz 2>/dev/null)" ]; then
        echo_warning "No backups found in $BACKUP_DIR"
        exit 1
    fi
    
    local count=1
    for backup in $(ls -t "$BACKUP_DIR"/frappe_db_*.sql.gz 2>/dev/null); do
        local size=$(du -h "$backup" | cut -f1)
        local date=$(stat -c %y "$backup" | cut -d'.' -f1)
        local filename=$(basename "$backup")
        
        echo -e "${BLUE}[$count]${NC} $filename"
        echo "    Date: $date"
        echo "    Size: $size"
        
        # Show info file if exists
        local info_file="${backup%.sql.gz}.info"
        if [ -f "$info_file" ]; then
            local tables=$(grep "Tables" "$info_file" 2>/dev/null || echo "")
            [ -n "$tables" ] && echo "    $tables"
        fi
        echo ""
        
        count=$((count + 1))
    done
}

# Function to restore from backup
restore_backup() {
    local backup_file="$1"
    
    if [ ! -f "$backup_file" ]; then
        echo_error "Backup file not found: $backup_file"
    fi
    
    echo_warning "WARNING: This will replace the current database!"
    echo_info "Database: $DB_NAME"
    echo_info "Backup: $(basename $backup_file)"
    echo ""
    
    read -p "Are you sure you want to continue? (yes/no): " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo_info "Restore cancelled"
        exit 0
    fi
    
    # Check if container is running
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        echo_error "MariaDB container is not running!"
    fi
    
    # Create a pre-restore backup
    echo_info "Creating pre-restore backup..."
    PRE_RESTORE_BACKUP="$BACKUP_DIR/pre_restore_$(date +%Y%m%d_%H%M%S).sql.gz"
    docker exec "$CONTAINER_NAME" mysqldump \
        -u root \
        -p"$MYSQL_ROOT_PASSWORD" \
        --single-transaction \
        --quick \
        "$DB_NAME" | gzip > "$PRE_RESTORE_BACKUP"
    echo_success "Pre-restore backup saved: $PRE_RESTORE_BACKUP"
    
    # Drop and recreate database
    echo_info "Dropping and recreating database..."
    docker exec "$CONTAINER_NAME" mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "DROP DATABASE IF EXISTS \`$DB_NAME\`;"
    docker exec "$CONTAINER_NAME" mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo_success "Database recreated"
    
    # Restore from backup
    echo_info "Restoring database from backup..."
    docker exec -i "$CONTAINER_NAME" mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME" < <(zcat "$backup_file")
    
    if [ $? -eq 0 ]; then
        echo_success "Database restored successfully!"
        
        # Verify restoration
        echo_info "Verifying restoration..."
        TABLES=$(docker exec "$CONTAINER_NAME" mysql -u root -p"$MYSQL_ROOT_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '$DB_NAME';" 2>/dev/null)
        ROWS=$(docker exec "$CONTAINER_NAME" mysql -u root -p"$MYSQL_ROOT_PASSWORD" -N -e "SELECT SUM(TABLE_ROWS) FROM information_schema.tables WHERE table_schema = '$DB_NAME';" 2>/dev/null)
        
        echo_success "Database restored successfully!"
        echo_success "Tables: $TABLES"
        echo_success "Total Rows: $ROWS"
    else
        echo_error "Restore failed!"
    fi
}

# Main script
echo "========================================"
echo "Frappe Database Restore Utility"
echo "========================================"
echo ""

# Parse arguments
if [ $# -eq 0 ]; then
    # Interactive mode - list backups
    list_backups
    
    echo ""
    read -p "Enter backup number to restore (or 'q' to quit): " choice
    
    if [ "$choice" == "q" ] || [ "$choice" == "Q" ]; then
        echo_info "Restore cancelled"
        exit 0
    fi
    
    # Get the selected backup
    BACKUP_FILE=$(ls -t "$BACKUP_DIR"/frappe_db_*.sql.gz 2>/dev/null | sed -n "${choice}p")
    
    if [ -z "$BACKUP_FILE" ]; then
        echo_error "Invalid selection"
    fi
    
    restore_backup "$BACKUP_FILE"
else
    # Command line mode - restore specific file
    BACKUP_FILE="$1"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        # Try to find in backup directory
        BACKUP_FILE="$BACKUP_DIR/$1"
    fi
    
    restore_backup "$BACKUP_FILE"
fi

echo ""
echo_success "Restore process completed!"
