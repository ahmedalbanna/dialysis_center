#!/bin/bash
#
# Setup Automated Database Backups
# This script configures automatic backups using cron
#

set -e

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

echo_title() {
    echo -e "${BLUE}$1${NC}"
}

# Get absolute path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="$SCRIPT_DIR/backup-database.sh"

if [ ! -f "$BACKUP_SCRIPT" ]; then
    echo_error "Backup script not found: $BACKUP_SCRIPT"
fi

echo_title "========================================"
echo_title "Automated Backup Setup"
echo_title "========================================"
echo ""

# Ask user for backup frequency
echo_info "Select backup frequency:"
echo "  1) Every hour"
echo "  2) Every 6 hours"
echo "  3) Daily at midnight"
echo "  4) Daily at specific time"
echo "  5) Custom cron expression"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        CRON_SCHEDULE="0 * * * *"
        DESCRIPTION="hourly"
        ;;
    2)
        CRON_SCHEDULE="0 */6 * * *"
        DESCRIPTION="every 6 hours"
        ;;
    3)
        CRON_SCHEDULE="0 0 * * *"
        DESCRIPTION="daily at midnight"
        ;;
    4)
        read -p "Enter hour (0-23): " hour
        read -p "Enter minute (0-59): " minute
        CRON_SCHEDULE="$minute $hour * * *"
        DESCRIPTION="daily at $hour:$minute"
        ;;
    5)
        read -p "Enter cron expression (e.g., '0 */4 * * *'): " CRON_SCHEDULE
        DESCRIPTION="custom schedule"
        ;;
    *)
        echo_error "Invalid choice"
        ;;
esac

echo ""
echo_info "Backup will run: $DESCRIPTION"
echo_info "Cron schedule: $CRON_SCHEDULE"
echo ""

# Create cron job
CRON_JOB="$CRON_SCHEDULE cd $SCRIPT_DIR && $BACKUP_SCRIPT >> $SCRIPT_DIR/backups/auto/backup.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$BACKUP_SCRIPT"; then
    echo_info "Removing existing backup cron job..."
    crontab -l 2>/dev/null | grep -v "$BACKUP_SCRIPT" | crontab -
fi

# Add new cron job
echo_info "Adding cron job..."
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo_success "Cron job added successfully!"

# Verify cron job
echo ""
echo_info "Current backup cron jobs:"
crontab -l 2>/dev/null | grep "$BACKUP_SCRIPT" || echo "  None"

# Create systemd timer alternative (optional)
echo ""
read -p "Do you want to create a systemd timer as well? (y/n): " create_timer

if [[ $create_timer =~ ^[Yy]$ ]]; then
    echo_info "Creating systemd timer..."
    
    # Create service file
    cat > /tmp/frappe-backup.service << EOF
[Unit]
Description=Frappe Database Backup Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
User=$USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=$BACKUP_SCRIPT
StandardOutput=append:$SCRIPT_DIR/backups/auto/backup.log
StandardError=append:$SCRIPT_DIR/backups/auto/backup.log

[Install]
WantedBy=multi-user.target
EOF

    # Create timer file
    cat > /tmp/frappe-backup.timer << EOF
[Unit]
Description=Frappe Database Backup Timer
Requires=frappe-backup.service

[Timer]
OnCalendar=$description
Persistent=true

[Install]
WantedBy=timers.target
EOF

    # Install systemd files
    sudo cp /tmp/frappe-backup.service /etc/systemd/system/
    sudo cp /tmp/frappe-backup.timer /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable frappe-backup.timer
    sudo systemctl start frappe-backup.timer
    
    echo_success "Systemd timer created and started!"
    
    # Show timer status
    echo ""
    echo_info "Timer status:"
    sudo systemctl status frappe-backup.timer --no-pager | head -10
    
    rm /tmp/frappe-backup.service /tmp/frappe-backup.timer
fi

# Test backup
echo ""
read -p "Do you want to run a test backup now? (y/n): " run_test

if [[ $run_test =~ ^[Yy]$ ]]; then
    echo_info "Running test backup..."
    "$BACKUP_SCRIPT"
fi

echo ""
echo_success "Automated backup setup completed!"
echo ""
echo_info "Backup configuration:"
echo "  Schedule: $DESCRIPTION"
echo "  Script: $BACKUP_SCRIPT"
echo "  Backup directory: $SCRIPT_DIR/backups/auto"
echo "  Log file: $SCRIPT_DIR/backups/auto/backup.log"
echo ""
echo_info "To view cron jobs: crontab -l"
echo_info "To remove cron job: crontab -e"
echo_info "To view backup log: tail -f $SCRIPT_DIR/backups/auto/backup.log"
