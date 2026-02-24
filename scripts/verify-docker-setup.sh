#!/bin/bash

echo "========================================"
echo "Docker Setup Verification"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Docker
echo -n "Docker: "
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Installed$(docker --version)${NC}"
else
    echo -e "${RED}✗ Not installed${NC}"
fi

# Check Docker Compose
echo -n "Docker Compose: "
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓ Installed$(docker-compose --version)${NC}"
else
    echo -e "${RED}✗ Not installed${NC}"
fi

echo ""
echo "========================================"
echo "Service Status"
echo "========================================"
docker-compose ps

echo ""
echo "========================================"
echo "Service Health Checks"
echo "========================================"
~/scripts/docker-commands.sh health

echo ""
echo "========================================"
echo "Database Information"
echo "========================================"
echo -n "Tables in database: "
docker exec frappe-mariadb mysql -u root -pfrappe@123 -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '_b2165c2f32b36e51';" 2>/dev/null | tail -1

echo ""
echo "========================================"
echo "Port Bindings"
echo "========================================"
echo "MariaDB:        localhost:3306"
echo "Redis Cache:    localhost:13000"
echo "Redis Queue:    localhost:11000"
echo "Redis SocketIO: localhost:12000"

echo ""
echo "========================================"
echo "Frappe Site Configuration"
echo "========================================"
cat ~/frappe-bench/sites/frappe.local/site_config.json

echo ""
echo "========================================"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. cd ~/frappe-bench"
echo "  2. bench start"
echo "  3. Access: http://localhost:8000"
echo ""
