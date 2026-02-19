# Dialysis Center Management System - Development Environment Setup

**Version:** 1.0  
**Last Updated:** 2026-02-19  
**Frappe Version:** v15.x  
**Target Framework:** Frappe Framework

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Create New App](#create-new-app)
4. [Project Structure](#project-structure)
5. [Build Tool Configuration](#build-tool-configuration)
6. [Development Workflow](#development-workflow)
7. [Code Quality Tools](#code-quality-tools)
8. [Testing Setup](#testing-setup)
9. [Database Configuration](#database-configuration)
10. [Common Issues & Solutions](#common-issues--solutions)

---

## 1. Prerequisites

### System Requirements

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.10+ | Backend framework |
| Node.js | 18+ or 20+ | Frontend build tools |
| MariaDB | 10.6+ | Database |
| Redis | 6+ or 7+ | Cache & queue |
| Git | 2.30+ | Version control |
| wkhtmltopdf | 0.12.6+ | PDF generation |

### Operating System

- **Recommended:** Ubuntu 22.04 LTS, Debian 11+, macOS 12+
- **Supported:** CentOS 8+, Fedora 35+, Windows (WSL2)

### Install Prerequisites (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3.10 python3.10-dev python3.10-venv python3-pip

# Install MariaDB
sudo apt install -y mariadb-server mariadb-client

# Install Redis
sudo apt install -y redis-server

# Install Node.js (using NodeSource)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install wkhtmltopdf
sudo apt install -y wkhtmltopdf

# Install other dependencies
sudo apt install -y git build-essential libssl-dev libffi-dev \
    libmariadb-dev libpq-dev libjpeg-dev zlib1g-dev libwebp-dev \
    libsasl2-dev libldap2-dev libcups2-dev pv
```

### Configure MariaDB

```bash
# Secure MariaDB installation
sudo mysql_secure_installation

# Configure MariaDB for Frappe
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Add these settings:

```ini
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```

Restart MariaDB:

```bash
sudo systemctl restart mariadb
```

---

## 2. Initial Setup

### Install Frappe Bench

```bash
# Install bench CLI
sudo pip3 install frappe-bench

# Verify installation
bench --version
```

### Initialize Bench (if not already done)

```bash
# Create bench directory (skip if already exists)
cd ~
bench init frappe-bench --frappe-branch version-15

# Navigate to bench
cd frappe-bench
```

### Create New Site (if needed)

```bash
# Create site for dialysis center
bench new-site dialysis.local --admin-password admin123 --db-name dialysis_db

# Set as current site
bench use dialysis.local
```

---

## 3. Create New App

### Generate App Structure

```bash
# Navigate to bench directory
cd ~/frappe-bench

# Create new app
bench new-app dialysis_center

# Follow prompts:
# - App Title: Dialysis Center Management
# - App Description: Complete dialysis center management system
# - App Publisher: Your Organization Name
# - App Email: dev@yourorg.com
# - App License: MIT
# - App Icon: 💉
```

### Install App to Site

```bash
# Install the app
bench --site dialysis.local install-app dialysis_center

# Verify installation
bench --site dialysis.local list-apps
```

---

## 4. Project Structure

### App Directory Layout

```
frappe-bench/apps/dialysis_center/
├── dialysis_center/                 # Main Python package
│   ├── __init__.py
│   ├── hooks.py                     # App configuration & hooks
│   ├── modules.txt                  # List of modules
│   ├── patches.txt                  # Database patches
│   │
│   ├── config/                      # App configuration
│   │   ├── __init__.py
│   │   ├── desktop.py              # Desktop icons
│   │   └── docs.py                 # Documentation config
│   │
│   ├── public/                      # Static assets
│   │   ├── css/                    # Stylesheets
│   │   ├── js/                     # JavaScript files
│   │   ├── images/                 # Images
│   │   └── icons/                  # SVG icons
│   │
│   ├── templates/                   # Jinja templates
│   │   ├── pages/                  # Web pages
│   │   └── includes/               # Reusable includes
│   │
│   ├── www/                        # Portal/website pages
│   │
│   ├── patient_management/          # Module: Patient Management
│   │   ├── doctype/
│   │   │   ├── patient/
│   │   │   │   ├── patient.json
│   │   │   │   ├── patient.py
│   │   │   │   ├── patient.js
│   │   │   │   └── test_patient.py
│   │   │   └── patient_document/
│   │   ├── page/
│   │   └── report/
│   │
│   ├── appointment_scheduling/      # Module: Appointments
│   ├── clinical_operations/         # Module: Clinical
│   ├── inventory/                   # Module: Inventory
│   ├── billing/                     # Module: Billing
│   └── reporting/                   # Module: Reports
│
├── package.json                     # Node.js dependencies
├── pyproject.toml                   # Python dependencies
├── requirements.txt                 # Python requirements
├── setup.py                         # App installation script
├── README.md
└── license.txt
```

### Create Modules

```bash
# Navigate to app directory
cd ~/frappe-bench/apps/dialysis_center

# Create modules.txt file
cat > dialysis_center/modules.txt << 'MODULES'
Patient Management
Appointment Scheduling
Clinical Operations
Inventory Management
Equipment Management
Billing
Staff Management
Reporting
MODULES

# Create module directories
mkdir -p dialysis_center/patient_management/doctype
mkdir -p dialysis_center/appointment_scheduling/doctype
mkdir -p dialysis_center/clinical_operations/doctype
mkdir -p dialysis_center/inventory_management/doctype
mkdir -p dialysis_center/equipment_management/doctype
mkdir -p dialysis_center/billing/doctype
mkdir -p dialysis_center/staff_management/doctype
mkdir -p dialysis_center/reporting/{report,page}

# Create __init__.py files
find dialysis_center -type d -exec touch {}/__init__.py \;
```

---

## 5. Build Tool Configuration

### 5.1 esbuild Configuration

Frappe uses esbuild for bundling JavaScript and CSS. Configuration is done in `hooks.py`.

#### Edit hooks.py

```python
# dialysis_center/hooks.py

from __future__ import unicode_literals
from frappe import __version__ as frappe_version

app_name = "dialysis_center"
app_title = "Dialysis Center Management"
app_publisher = "Your Organization"
app_description = "Complete dialysis center management system"
app_email = "dev@yourorg.com"
app_license = "MIT"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "/assets/dialysis_center/css/dialysis_center.bundle.css"
]

app_include_js = [
    "/assets/dialysis_center/js/dialysis_center.bundle.js"
]

# include js, css files in header of web template
web_include_css = [
    "/assets/dialysis_center/css/dialysis_web.bundle.css"
]

web_include_js = [
    "/assets/dialysis_center/js/dialysis_web.bundle.js"
]

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dialysis_center/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Patient": "public/js/patient.js",
    "Appointment": "public/js/appointment.js",
    "Dialysis Session": "public/js/dialysis_session.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# -----

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dialysis_center.utils.jinja_methods",
# 	"filters": "dialysis_center.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dialysis_center.install.before_install"
# after_install = "dialysis_center.install.after_install"

# Uninstallation
# --------------

# before_uninstall = "dialysis_center.uninstall.before_uninstall"
# after_uninstall = "dialysis_center.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dialysis_center.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Patient": {
        "validate": "dialysis_center.patient_management.doctype.patient.patient.validate_patient",
        "on_update": "dialysis_center.patient_management.doctype.patient.patient.on_patient_update",
    },
    "Dialysis Session": {
        "on_submit": "dialysis_center.clinical_operations.doctype.dialysis_session.dialysis_session.on_session_submit",
        "on_cancel": "dialysis_center.clinical_operations.doctype.dialysis_session.dialysis_session.on_session_cancel",
    },
    "*": {
        "on_trash": "dialysis_center.utils.audit.log_deletion"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "all": [
        "dialysis_center.tasks.all"
    ],
    "daily": [
        "dialysis_center.tasks.daily_cleanup",
        "dialysis_center.tasks.send_daily_reports"
    ],
    "hourly": [
        "dialysis_center.tasks.check_appointments",
        "dialysis_center.tasks.update_machine_status"
    ],
    "weekly": [
        "dialysis_center.tasks.weekly_summary"
    ],
    "monthly": [
        "dialysis_center.tasks.monthly_reports"
    ],
    # Cron format: minute hour day month day_of_week
    "cron": {
        "0 8 * * *": [  # Every day at 8 AM
            "dialysis_center.tasks.morning_checklist"
        ],
        "0 */4 * * *": [  # Every 4 hours
            "dialysis_center.tasks.sync_lab_results"
        ]
    }
}

# Testing
# -------

# before_tests = "dialysis_center.install.before_tests"

# Overriding Methods
# ------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dialysis_center.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dialysis_center.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dialysis_center.auth.validate"
# ]

# Translation
# -----------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []

# Fixtures
# --------
# Fixtures are used to export/import configuration data

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Dialysis Center Management"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Dialysis Center Management"]]},
    {"dt": "Role", "filters": [["name", "in", [
        "Dialysis Nurse",
        "Dialysis Doctor", 
        "Dialysis Technician",
        "Dialysis Administrator"
    ]]]},
]
```

### 5.2 package.json Configuration

Create/edit the `package.json` file:

```json
{
  "name": "dialysis_center",
  "version": "0.0.1",
  "description": "Dialysis Center Management System",
  "main": "index.js",
  "scripts": {
    "watch": "yarn run build --watch",
    "build": "frappe build --app dialysis_center",
    "lint": "eslint public/js/**/*.js --fix",
    "format": "prettier --write 'public/**/*.{js,vue,scss,css}'",
    "test": "jest"
  },
  "keywords": [
    "frappe",
    "dialysis",
    "healthcare"
  ],
  "author": "Your Organization",
  "license": "MIT",
  "dependencies": {
    "@vue/compiler-sfc": "^3.3.0",
    "chart.js": "^4.4.0",
    "vue": "^3.3.0",
    "vue-router": "^4.2.0"
  },
  "devDependencies": {
    "@babel/core": "^7.23.0",
    "@babel/preset-env": "^7.23.0",
    "eslint": "^8.50.0",
    "eslint-plugin-vue": "^9.17.0",
    "jest": "^29.7.0",
    "prettier": "^3.0.3",
    "sass": "^1.69.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

Install Node dependencies:

```bash
cd ~/frappe-bench/apps/dialysis_center
yarn install
# or
npm install
```

### 5.3 Python Dependencies (pyproject.toml)

Create/edit `pyproject.toml`:

```toml
[project]
name = "dialysis_center"
version = "0.0.1"
description = "Dialysis Center Management System"
authors = [
    { name = "Your Organization", email = "dev@yourorg.com" }
]
dependencies = [
    "frappe>=15.0.0",
    "pandas>=2.0.0",
    "python-dateutil>=2.8.2",
    "pillow>=10.0.0",
]
requires-python = ">=3.10"
readme = "README.md"
license = { text = "MIT" }

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]

[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[tool.ruff]
line-length = 110
target-version = "py310"

[tool.ruff.lint]
select = ["F", "E", "W", "I", "UP", "B", "RUF"]
ignore = ["B008", "B904"]

[tool.ruff.format]
quote-style = "double"
indent-style = "tab"
docstring-code-format = true

[tool.black]
line-length = 110
target-version = ['py310', 'py311', 'py312']
skip-string-normalization = false

[tool.pytest.ini_options]
testpaths = ["dialysis_center"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
```

Install Python dependencies:

```bash
cd ~/frappe-bench/apps/dialysis_center
pip install -e .
pip install -e ".[dev]"  # For development dependencies
```

---

## 6. Development Workflow

### 6.1 Building Assets

```bash
# Build all apps
bench build

# Build specific app
bench build --app dialysis_center

# Watch mode (auto-rebuild on changes)
cd ~/frappe-bench/apps/dialysis_center
yarn watch

# Or from bench directory
bench watch
```

### 6.2 Clear Cache

```bash
# Clear all cache
bench --site dialysis.local clear-cache

# Clear website cache only
bench --site dialysis.local clear-website-cache

# Rebuild and clear
bench build && bench --site dialysis.local clear-cache
```

### 6.3 Running the Development Server

```bash
# Start development server
cd ~/frappe-bench
bench start

# Start in production mode
bench start --production

# Start specific services
bench serve         # Web server only
bench watch         # Asset building only
bench worker        # Background jobs only
bench schedule      # Scheduler only
```

Access the application:
- **URL:** http://localhost:8000
- **Site:** dialysis.local
- **Username:** Administrator
- **Password:** admin123

### 6.4 Database Migrations

```bash
# Run migrations
bench --site dialysis.local migrate

# Run specific app migrations
bench --site dialysis.local migrate --app dialysis_center

# Reload a specific doctype
bench --site dialysis.local console
>>> frappe.reload_doc('patient_management', 'doctype', 'patient')
```

### 6.5 Console Access

```bash
# Python console (IPython)
bench --site dialysis.local console

# Examples in console:
>>> import frappe
>>> frappe.db.sql("SELECT count(*) FROM `tabPatient`")
>>> doc = frappe.get_doc("Patient", "PT-2026-00001")
>>> doc.patient_name
```

### 6.6 MariaDB Access

```bash
# Access database directly
bench --site dialysis.local mariadb

# Or with full MySQL command
mysql -u root -p dialysis_db
```

---

## 7. Code Quality Tools

### 7.1 Pre-commit Hooks Setup

```bash
cd ~/frappe-bench/apps/dialysis_center

# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'PRECOMMIT'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
        exclude: '.*\.(txt|csv)$'
      - id: end-of-file-fixer
        exclude: '.*\.(txt|csv)$'
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=5000']
      - id: check-json
      - id: check-merge-conflict
      - id: mixed-line-ending

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.8
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, vue, scss, css, json, yaml]
        args: [--tab-width=4, --use-tabs, --write]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: \.(js|vue)$
        args: [--fix]
        additional_dependencies:
          - eslint@8.56.0
          - eslint-plugin-vue@9.19.2

  - repo: local
    hooks:
      - id: commitlint
        name: commitlint
        entry: bash -c 'npx commitlint --edit "$1"'
        language: system
        stages: [commit-msg]
PRECOMMIT

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Run pre-commit on all files (initial check)
pre-commit run --all-files
```

### 7.2 ESLint Configuration

Create `.eslintrc.json`:

```json
{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:vue/vue3-recommended"
  ],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "plugins": ["vue"],
  "rules": {
    "indent": ["error", "tab"],
    "quotes": ["error", "double"],
    "semi": ["error", "always"],
    "no-unused-vars": "warn",
    "no-console": "off",
    "vue/multi-word-component-names": "off",
    "vue/html-indent": ["error", "tab"]
  },
  "globals": {
    "frappe": "readonly",
    "cur_frm": "readonly",
    "cur_list": "readonly",
    "__": "readonly",
    "moment": "readonly"
  }
}
```

### 7.3 Prettier Configuration

Create `.prettierrc`:

```json
{
  "useTabs": true,
  "tabWidth": 4,
  "semi": true,
  "singleQuote": false,
  "trailingComma": "es5",
  "printWidth": 110,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

Create `.prettierignore`:

```
node_modules/
*.min.js
*.bundle.js
*.bundle.css
public/dist/
.git/
```

### 7.4 EditorConfig

Create `.editorconfig`:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{py,js,vue,scss,css,html}]
indent_style = tab
indent_size = 4

[*.json]
indent_style = space
indent_size = 2

[*.{yml,yaml}]
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

### 7.5 Ruff Configuration

Already in `pyproject.toml` (see section 5.3), but you can also use `ruff.toml`:

```toml
# ruff.toml
line-length = 110
target-version = "py310"

[lint]
select = ["F", "E", "W", "I", "UP", "B", "RUF"]
ignore = ["B008", "B904"]

[format]
quote-style = "double"
indent-style = "tab"
docstring-code-format = true
```

### 7.6 Running Code Quality Checks

```bash
# Ruff (Python linting)
ruff check dialysis_center/
ruff check dialysis_center/ --fix

# Ruff formatting
ruff format dialysis_center/

# ESLint (JavaScript)
npm run lint
# or
eslint public/js/**/*.js --fix

# Prettier
npm run format
# or
prettier --write 'public/**/*.{js,vue,scss,css}'

# Run all pre-commit hooks manually
pre-commit run --all-files
```

---

## 8. Testing Setup

### 8.1 Python Unit Tests

Create test file structure:

```bash
# Tests are created alongside doctypes
# Example: dialysis_center/patient_management/doctype/patient/test_patient.py
```

Example test file:

```python
# dialysis_center/patient_management/doctype/patient/test_patient.py

import frappe
from frappe.tests import IntegrationTestCase
from dialysis_center.patient_management.doctype.patient.patient import Patient


class TestPatient(IntegrationTestCase):
	"""Test Patient DocType"""

	def setUp(self):
		"""Create test patient"""
		self.test_patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": "Test Patient",
			"date_of_birth": "1980-01-01",
			"gender": "Male",
			"blood_group": "O+",
			"mobile": "+1234567890",
			"email": "test.patient@example.com",
			"status": "Active"
		})
		self.test_patient.insert()

	def tearDown(self):
		"""Clean up test data"""
		if frappe.db.exists("Patient", self.test_patient.name):
			frappe.delete_doc("Patient", self.test_patient.name, force=True)

	def test_patient_creation(self):
		"""Test patient can be created"""
		self.assertTrue(frappe.db.exists("Patient", self.test_patient.name))
		self.assertEqual(self.test_patient.patient_name, "Test Patient")

	def test_patient_id_generation(self):
		"""Test patient ID is auto-generated"""
		self.assertTrue(self.test_patient.name.startswith("PT-"))

	def test_age_calculation(self):
		"""Test age is calculated correctly from DOB"""
		# Assuming Patient has get_age() method
		age = self.test_patient.get_age()
		self.assertGreater(age, 40)  # Born in 1980

	def test_duplicate_email_validation(self):
		"""Test duplicate email is not allowed"""
		duplicate_patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": "Another Patient",
			"date_of_birth": "1990-01-01",
			"gender": "Female",
			"email": "test.patient@example.com"  # Same email
		})
		with self.assertRaises(frappe.ValidationError):
			duplicate_patient.insert()

	def test_required_fields(self):
		"""Test required fields validation"""
		invalid_patient = frappe.get_doc({
			"doctype": "Patient",
			"patient_name": "Invalid Patient"
			# Missing required fields
		})
		with self.assertRaises(frappe.MandatoryError):
			invalid_patient.insert()
```

### 8.2 Running Tests

```bash
# Run all tests for the app
bench --site dialysis.local run-tests --app dialysis_center

# Run tests for specific module
bench --site dialysis.local run-tests --module dialysis_center.patient_management

# Run tests for specific doctype
bench --site dialysis.local run-tests --doctype "Patient"

# Run specific test class
bench --site dialysis.local run-tests \
  --test dialysis_center.patient_management.doctype.patient.test_patient.TestPatient

# Run specific test method
bench --site dialysis.local run-tests \
  --test dialysis_center.patient_management.doctype.patient.test_patient.TestPatient.test_patient_creation

# Run with coverage
bench --site dialysis.local run-tests --app dialysis_center --coverage

# Parallel testing (faster)
bench --site dialysis.local run-tests --app dialysis_center --parallel
```

### 8.3 pytest Configuration

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["dialysis_center"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests"
]
```

### 8.4 Cypress UI Tests (Optional)

Install Cypress:

```bash
cd ~/frappe-bench/apps/dialysis_center
npm install --save-dev cypress

# Add to package.json scripts:
# "cypress:open": "cypress open",
# "cypress:run": "cypress run"
```

Create test structure:

```bash
mkdir -p cypress/integration
mkdir -p cypress/fixtures
mkdir -p cypress/support
```

Example Cypress test:

```javascript
// cypress/integration/patient.spec.js

describe('Patient Management', () => {
	before(() => {
		cy.login('Administrator', 'admin123');
	});

	it('creates a new patient', () => {
		cy.visit('/app/patient/new');
		
		cy.fill_field('patient_name', 'Cypress Test Patient');
		cy.fill_field('date_of_birth', '1985-05-15');
		cy.fill_field('gender', 'Male');
		cy.fill_field('blood_group', 'A+');
		cy.fill_field('mobile', '+1987654321');
		cy.fill_field('email', 'cypress.test@example.com');
		
		cy.get('.btn-primary[data-label="Save"]').click();
		cy.get('.msgprint').should('contain', 'Saved');
	});

	it('searches for patients', () => {
		cy.visit('/app/patient');
		cy.get('.list-row').should('have.length.greaterThan', 0);
		
		cy.get('input[data-element="search"]').type('Cypress Test');
		cy.get('.list-row').should('contain', 'Cypress Test Patient');
	});
});
```

---

## 9. Database Configuration

### 9.1 Database Backup

```bash
# Manual backup
bench --site dialysis.local backup

# Backup with files
bench --site dialysis.local backup --with-files

# Backup to specific location
bench --site dialysis.local backup --backup-path ~/backups/

# List backups
ls -lh ~/frappe-bench/sites/dialysis.local/private/backups/
```

### 9.2 Database Restore

```bash
# Restore from latest backup
bench --site dialysis.local restore

# Restore specific backup
bench --site dialysis.local restore \
  ~/frappe-bench/sites/dialysis.local/private/backups/20260219_120000-dialysis_db-database.sql.gz

# Restore with files
bench --site dialysis.local restore \
  --with-private-files ~/path/to/private-files.tar \
  --with-public-files ~/path/to/public-files.tar \
  ~/path/to/database.sql.gz
```

### 9.3 Database Indexing

Add indexes in DocType JSON or via migration:

```python
# dialysis_center/patches/v1_0/add_patient_indexes.py

import frappe

def execute():
	"""Add database indexes for better performance"""
	
	# Add index on frequently queried fields
	frappe.db.add_index("Patient", ["status", "date_of_birth"])
	frappe.db.add_index("Appointment", ["appointment_date", "status"])
	frappe.db.add_index("Dialysis Session", ["session_date", "patient"])
	
	frappe.db.commit()
```

Add to `patches.txt`:

```
dialysis_center.patches.v1_0.add_patient_indexes
```

### 9.4 Database Optimization

```bash
# Access MariaDB
bench --site dialysis.local mariadb

# Run optimization commands
OPTIMIZE TABLE `tabPatient`;
OPTIMIZE TABLE `tabAppointment`;
OPTIMIZE TABLE `tabDialysis Session`;

# Analyze tables for query optimization
ANALYZE TABLE `tabPatient`;
ANALYZE TABLE `tabAppointment`;

# Check table status
SHOW TABLE STATUS LIKE 'tabPatient';

# Check indexes
SHOW INDEX FROM `tabPatient`;
```

---

## 10. Common Issues & Solutions

### Issue 1: Assets Not Loading

**Symptoms:** JavaScript/CSS not loading, 404 errors

**Solutions:**

```bash
# Rebuild assets
bench build --app dialysis_center

# Clear cache
bench --site dialysis.local clear-cache

# Hard reload browser (Ctrl+Shift+R)

# Check if files exist
ls -la ~/frappe-bench/sites/assets/dialysis_center/

# Restart bench
bench restart
```

### Issue 2: Database Connection Errors

**Symptoms:** "Can't connect to database" errors

**Solutions:**

```bash
# Check MariaDB status
sudo systemctl status mariadb

# Restart MariaDB
sudo systemctl restart mariadb

# Check site_config.json
cat ~/frappe-bench/sites/dialysis.local/site_config.json

# Test database connection
bench --site dialysis.local mariadb
```

### Issue 3: Permission Errors

**Symptoms:** "You don't have permission" errors

**Solutions:**

```bash
# Check user roles
bench --site dialysis.local console
>>> frappe.get_doc("User", "user@example.com").get_roles()

# Add role to user
>>> user = frappe.get_doc("User", "user@example.com")
>>> user.add_roles("Dialysis Nurse")

# Check DocType permissions
>>> frappe.get_all("DocPerm", filters={"parent": "Patient"})

# Reset permissions
bench --site dialysis.local set-admin-password admin123
```

### Issue 4: Migration Failures

**Symptoms:** Errors during `bench migrate`

**Solutions:**

```bash
# Run with skip-failing flag
bench --site dialysis.local migrate --skip-failing

# Check migration log
cat ~/frappe-bench/logs/bench.log

# Manually reload doctype
bench --site dialysis.local console
>>> frappe.reload_doc('patient_management', 'doctype', 'patient')
>>> frappe.db.commit()

# Reset DocType (use with caution - loses data)
bench --site dialysis.local console
>>> frappe.delete_doc("DocType", "Patient", force=True)
>>> frappe.db.commit()
# Then re-import the DocType
```

### Issue 5: Redis Connection Errors

**Symptoms:** "Redis connection failed" errors

**Solutions:**

```bash
# Check Redis status
sudo systemctl status redis

# Restart Redis
sudo systemctl restart redis

# Check Redis configuration in site_config.json
cat ~/frappe-bench/sites/dialysis.local/site_config.json

# Test Redis connection
redis-cli ping
# Should return: PONG
```

### Issue 6: Port Already in Use

**Symptoms:** "Address already in use" when starting bench

**Solutions:**

```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
bench serve --port 8001
```

### Issue 7: Import/Export Issues

**Symptoms:** Errors importing data files

**Solutions:**

```bash
# Check file permissions
chmod 644 ~/path/to/import.csv

# Import with bench console
bench --site dialysis.local console
>>> from frappe.core.doctype.data_import.data_import import import_file
>>> import_file("Patient", "/path/to/patients.csv")

# Export data
bench --site dialysis.local console
>>> frappe.get_list("Patient", fields=["name", "patient_name"])
```

### Issue 8: Slow Performance

**Solutions:**

```bash
# Enable query logging
bench --site dialysis.local set-config enable_query_comments 1

# Check slow queries
bench --site dialysis.local mariadb
> SHOW FULL PROCESSLIST;

# Optimize database
bench --site dialysis.local mariadb
> OPTIMIZE TABLE `tabPatient`;

# Clear cache regularly
bench --site dialysis.local clear-cache

# Use Redis for caching
# Ensure Redis is properly configured in site_config.json
```

---

## Development Best Practices

### 1. Git Workflow

```bash
# Create feature branch
git checkout -b feature/patient-management

# Make changes and commit with conventional commits
git add .
git commit -m "feat: add patient registration form"

# Push to remote
git push origin feature/patient-management

# Create pull request on GitHub/GitLab
```

### 2. Code Organization

- Keep controller logic in `.py` files
- Keep UI logic in `.js` files
- Use modules to organize related functionality
- Follow Frappe naming conventions (`snake_case`)

### 3. Documentation

- Document all custom functions
- Add docstrings to Python methods
- Comment complex business logic
- Keep README.md updated

### 4. Performance

- Use database indexes on frequently queried fields
- Minimize frappe.db.get_all() calls in loops
- Cache expensive computations
- Use background jobs for long-running tasks

### 5. Security

- Never expose sensitive data in logs
- Use frappe.whitelist() carefully
- Validate all user inputs
- Implement proper permission checks

---

## Quick Reference Commands

```bash
# Development
bench start                                    # Start development server
bench build --app dialysis_center             # Build assets
bench watch                                    # Watch and rebuild assets
bench --site dialysis.local clear-cache        # Clear cache

# Database
bench --site dialysis.local migrate            # Run migrations
bench --site dialysis.local backup             # Backup database
bench --site dialysis.local mariadb            # Access database
bench --site dialysis.local console            # Python console

# Testing
bench --site dialysis.local run-tests --app dialysis_center  # Run tests
pre-commit run --all-files                     # Run code quality checks

# Deployment
bench restart                                  # Restart services
bench update                                   # Update all apps
bench migrate-to version-15                    # Upgrade Frappe version

# Maintenance
bench doctor                                   # Check system health
bench setup requirements                       # Update dependencies
bench pip install package_name                 # Install Python package
```

---

## Additional Resources

- **Frappe Docs:** https://frappeframework.com/docs
- **Frappe Forum:** https://discuss.erpnext.com/
- **GitHub:** https://github.com/frappe/frappe
- **YouTube:** Frappe Framework Tutorial Series

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-19  
**Maintained By:** Development Team

