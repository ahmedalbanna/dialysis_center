#!/bin/bash

# Hot-Reload Verification Script
# Checks if hot-reload is properly configured and working

set -e

echo "🔍 Verifying Hot-Reload Configuration..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_item() {
	local name=$1
	local condition=$2
	
	if eval "$condition"; then
		echo -e "${GREEN}✓${NC} $name"
		return 0
	else
		echo -e "${RED}✗${NC} $name"
		return 1
	fi
}

all_passed=true

echo "📋 Checking Configuration Files..."
check_item "Procfile has --live-reload flag" "grep -q '\-\-live-reload' Procfile" || all_passed=false
check_item "Frappe hooks includes hot-reload.bundle.js" "grep -q 'hot-reload.bundle.js' apps/frappe/frappe/hooks.py" || all_passed=false
check_item "Dialysis Center hooks includes hot-reload.bundle.js" "grep -q 'hot-reload.bundle.js' apps/dialysis_center/dialysis_center/hooks.py" || all_passed=false

echo ""
echo "📦 Checking Compiled Assets..."
check_item "Frappe hot-reload bundle compiled" "ls sites/assets/frappe/dist/js/hot-reload.bundle.*.js 2>/dev/null | grep -q ." || all_passed=false
check_item "Dialysis Center hot-reload bundle compiled" "ls sites/assets/dialysis_center/dist/js/hot-reload.bundle.*.js 2>/dev/null | grep -q ." || all_passed=false

echo ""
echo "🔗 Checking Asset Registration..."
check_item "Hot-reload bundle in assets.json" "grep -q 'hot-reload.bundle.js' sites/assets/assets.json" || all_passed=false

echo ""
echo "📁 Checking Source Files..."
check_item "hot-reload.js exists" "test -f apps/frappe/frappe/public/js/hot-reload.js" || all_passed=false
check_item "hot-reload.bundle.js exists (Frappe)" "test -f apps/frappe/frappe/public/js/hot-reload.bundle.js" || all_passed=false
check_item "hot-reload.bundle.js exists (Dialysis Center)" "test -f apps/dialysis_center/dialysis_center/public/js/hot-reload.bundle.js" || all_passed=false

echo ""
echo "🚀 Services Check..."
check_item "Redis queue running" "redis-cli -p 11000 ping 2>/dev/null | grep -q PONG" || true
check_item "Redis cache running" "redis-cli -p 13000 ping 2>/dev/null | grep -q PONG" || true

echo ""
if [ "$all_passed" = true ]; then
	echo -e "${GREEN}✅ Hot-Reload Configuration Verified!${NC}"
	echo ""
	echo "Next steps:"
	echo "1. Run: cd frappe-bench && bench start"
	echo "2. Open: http://127.0.0.1:8000"
	echo "3. Open browser console (F12)"
	echo "4. Edit a file in apps/dialysis_center/dialysis_center/public/"
	echo "5. Watch for hot-reload messages in console"
	exit 0
else
	echo -e "${RED}⚠️  Some checks failed. See above for details.${NC}"
	echo ""
	echo "Troubleshooting:"
	echo "1. Run: cd frappe-bench && bench build"
	echo "2. Verify Redis is running: bench status"
	echo "3. Check logs: tail -f logs/*.log"
	exit 1
fi
