#!/bin/bash
# Docker Compose Helper Commands for Frappe

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

echo_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

echo_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo_error "docker-compose is not installed!"
    exit 1
fi

# Function to start all services
start_services() {
    echo_info "Starting all services..."
    docker-compose up -d
    echo_success "All services started!"
}

# Function to stop all services
stop_services() {
    echo_info "Stopping all services..."
    docker-compose down
    echo_success "All services stopped!"
}

# Function to restart all services
restart_services() {
    echo_info "Restarting all services..."
    docker-compose restart
    echo_success "All services restarted!"
}

# Function to view logs
view_logs() {
    if [ -z "$1" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$1"
    fi
}

# Function to check service status
check_status() {
    echo_info "Checking service status..."
    docker-compose ps
}

# Function to check service health
check_health() {
    echo_info "Checking service health..."
    echo ""
    
    # Check MariaDB
    echo "MariaDB:"
    docker exec frappe-mariadb mysqladmin ping -h localhost -u root -pfrappe@123 2>/dev/null && echo_success "MariaDB is healthy" || echo_error "MariaDB is not responding"
    
    # Check Redis Cache
    echo "Redis Cache:"
    docker exec frappe-redis-cache redis-cli ping 2>/dev/null && echo_success "Redis Cache is healthy" || echo_error "Redis Cache is not responding"
    
    # Check Redis Queue
    echo "Redis Queue:"
    docker exec frappe-redis-queue redis-cli ping 2>/dev/null && echo_success "Redis Queue is healthy" || echo_error "Redis Queue is not responding"
    
    # Check Redis SocketIO
    echo "Redis SocketIO:"
    docker exec frappe-redis-socketio redis-cli ping 2>/dev/null && echo_success "Redis SocketIO is healthy" || echo_error "Redis SocketIO is not responding"
    
    # Check Nginx
    echo "Nginx:"
    docker exec frappe-nginx nginx -t 2>/dev/null && echo_success "Nginx is healthy" || echo_error "Nginx configuration error"
}

# Function to access MariaDB shell
mariadb_shell() {
    echo_info "Accessing MariaDB shell..."
    docker exec -it frappe-mariadb mysql -u root -pfrappe@123
}

# Function to access Redis Cache shell
redis_cache_shell() {
    echo_info "Accessing Redis Cache shell..."
    docker exec -it frappe-redis-cache redis-cli
}

# Function to access Nginx shell
nginx_shell() {
    echo_info "Accessing Nginx shell..."
    docker exec -it frappe-nginx sh
}

# Function to reload Nginx configuration
nginx_reload() {
    echo_info "Reloading Nginx configuration..."
    docker exec frappe-nginx nginx -t && docker exec frappe-nginx nginx -s reload
    echo_success "Nginx configuration reloaded!"
}

# Function to view Nginx logs
nginx_logs() {
    echo_info "Viewing Nginx logs..."
    docker exec frappe-nginx tail -f /var/log/nginx/frappe.access.log
}

# Function to backup MariaDB
backup_mariadb() {
    BACKUP_DIR="./backups"
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/mariadb_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    echo_info "Creating MariaDB backup..."
    docker exec frappe-mariadb mysqldump -u root -pfrappe@123 --all-databases > "$BACKUP_FILE"
    echo_success "Backup created: $BACKUP_FILE"
}

# Function to restore MariaDB backup
restore_mariadb() {
    if [ -z "$1" ]; then
        echo_error "Please provide backup file path"
        exit 1
    fi
    
    echo_info "Restoring MariaDB from $1..."
    docker exec -i frappe-mariadb mysql -u root -pfrappe@123 < "$1"
    echo_success "Database restored successfully!"
}

# Function to clean up (remove containers and volumes)
cleanup() {
    read -p "This will remove all containers and volumes. Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo_info "Cleaning up..."
        docker-compose down -v
        echo_success "Cleanup complete!"
    else
        echo_info "Cleanup cancelled"
    fi
}

# Main command handler
case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        view_logs "$2"
        ;;
    status)
        check_status
        ;;
    health)
        check_health
        ;;
    mariadb)
        mariadb_shell
        ;;
    redis)
        redis_cache_shell
        ;;
    backup)
        backup_mariadb
        ;;
    restore)
        restore_mariadb "$2"
        ;;
    nginx)
        nginx_shell
        ;;
    nginx-reload)
        nginx_reload
        ;;
    nginx-logs)
        nginx_logs
        ;;
    cleanup)
        cleanup
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs [service]|status|health|mariadb|redis|nginx|nginx-reload|nginx-logs|backup|restore <file>|cleanup}"
        echo ""
        echo "Commands:"
        echo "  start           - Start all services"
        echo "  stop            - Stop all services"
        echo "  restart         - Restart all services"
        echo "  logs [service]  - View logs (optionally for specific service)"
        echo "  status          - Check service status"
        echo "  health          - Check service health"
        echo "  mariadb         - Access MariaDB shell"
        echo "  redis           - Access Redis Cache shell"
        echo "  nginx           - Access Nginx shell"
        echo "  nginx-reload    - Reload Nginx configuration"
        echo "  nginx-logs      - View Nginx access logs"
        echo "  backup          - Create MariaDB backup"
        echo "  restore <file>  - Restore MariaDB from backup"
        echo "  cleanup         - Remove containers and volumes"
        exit 1
        ;;
esac
