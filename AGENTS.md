# Frappe Framework Development Guide

## Project Overview

**Frappe Framework** is a full-stack, metadata-driven, low-code web framework built for creating business applications like ERPNext.

- **Language**: Python 3.10+ (currently 3.12.12), JavaScript (Node.js 22+)
- **Framework Version**: v15.100.1
- **Database**: MariaDB 10.11.14
- **Cache**: Redis 7.0.15
- **Frontend**: Vue.js, Vanilla JS, SCSS
- **Backend**: Python with Werkzeug WSGI, Jinja2 templating
- **Build Tool**: esbuild
- **License**: MIT

### Key Technologies
- **Python**: Werkzeug, Jinja2, PyMySQL, PyPika, RestrictedPython, WeasyPrint, Babel
- **JavaScript**: Vue.js, @editorjs/editorjs, Socket.IO, esbuild
- **Database ORM**: Custom ORM with PyPika query builder
- **Task Queue**: RQ (Redis Queue)
- **Testing**: Python unittest, Cypress for UI tests

## Project Structure

### Core Directories

```
frappe-bench/
├── apps/frappe/                    # Main Frappe framework application
│   ├── frappe/                     # Python package
│   │   ├── core/                   # Core doctypes (User, Role, etc.)
│   │   ├── desk/                   # Desk/UI backend logic
│   │   ├── public/                 # Static assets (JS, CSS, images)
│   │   ├── website/                # Website rendering engine
│   │   ├── model/                  # Document model & ORM
│   │   ├── database/               # Database abstraction layer
│   │   ├── email/                  # Email handling
│   │   ├── integrations/           # Third-party integrations
│   │   ├── printing/               # Print format engine
│   │   ├── workflow/               # Workflow system
│   │   ├── utils/                  # Utility functions
│   │   └── hooks.py                # App hooks configuration
│   ├── esbuild/                    # Build configuration
│   ├── cypress/                    # UI tests
│   └── package.json                # Node.js dependencies
├── sites/                          # Site-specific data
│   ├── frappe.local/               # Example site
│   │   ├── private/                # Private files & backups
│   │   ├── public/                 # Public files
│   │   └── site_config.json        # Site configuration
│   └── apps.txt                    # Installed apps list
└── config/                         # Redis & scheduler config
```

### Important Files

- `frappe/__init__.py` - Core framework API, global functions
- `frappe/app.py` - WSGI application entry point
- `frappe/hooks.py` - Hook definitions and lifecycle events
- `frappe/model/document.py` - Base Document class
- `frappe/database/database.py` - Database abstraction
- `pyproject.toml` - Python dependencies and tooling config
- `package.json` - JavaScript dependencies
- `.editorconfig` - Editor configuration
- `.pre-commit-config.yaml` - Pre-commit hooks

## Development Setup

### Starting the Development Server

```bash
cd ~/frappe-bench
bench start
```

Access at: http://127.0.0.1:8000 (Login: Administrator / admin@123)

### Common Bench Commands

```bash
# Create a new site
bench new-site mysite.local --admin-password=PASSWORD

# Install an app to a site
bench --site frappe.local install-app app_name

# Run migrations
bench --site frappe.local migrate

# Clear cache
bench --site frappe.local clear-cache

# Run tests
bench --site frappe.local run-tests

# Build assets
bench build

# Console access
bench --site frappe.local console

# Database access
bench --site frappe.local mariadb
```

## Coding Standards & Conventions

### Python Code Style

- **Formatter**: Ruff (replaces Black + isort)
- **Linter**: Ruff (replaces flake8, pylint)
- **Line Length**: 110 characters
- **Indentation**: TABS (not spaces) - 4 spaces width
- **Quotes**: Double quotes (`"`)
- **Python Version**: 3.10+ compatible

#### Key Ruff Rules
```toml
# From pyproject.toml
[tool.ruff.format]
quote-style = "double"
indent-style = "tab"
docstring-code-format = true

[tool.ruff.lint]
select = ["F", "E", "W", "I", "UP", "B", "RUF"]
```

#### Python Conventions
- Use tabs for indentation in `.py`, `.js`, `.vue`, `.css`, `.scss`, `.html`
- Use 2 spaces for `.json` files
- Files end with newline (`insert_final_newline = true`)
- No trailing whitespace
- UTF-8 encoding
- LF line endings

### JavaScript Code Style

- **Formatter**: Prettier
- **Linter**: ESLint
- **Indentation**: Tabs
- **Build System**: esbuild (configured in `esbuild/` directory)

### File Naming

- Python: `snake_case.py`
- JavaScript: `snake_case.js`
- DocTypes: `Title Case` (generates `title_case` folder names)
- CSS/SCSS: `snake_case.scss` or `kebab-case.scss`

## DocType Development

### DocType Structure

DocTypes are the core data model in Frappe. They are metadata-driven.

```
frappe/core/doctype/user/
├── user.json                    # DocType schema (auto-generated)
├── user.py                      # Controller class
├── user.js                      # Client-side controller
├── test_user.py                 # Unit tests
└── user_dashboard.py            # Dashboard configuration (optional)
```

### Creating a DocType Controller

```python
# frappe/core/doctype/user/user.py
import frappe
from frappe.model.document import Document

class User(Document):
	"""Controller for User DocType"""
	
	def validate(self):
		"""Called before saving"""
		self.validate_email()
	
	def on_update(self):
		"""Called after saving"""
		self.update_user_permissions()
	
	def on_trash(self):
		"""Called before deleting"""
		if self.name == "Administrator":
			frappe.throw("Cannot delete Administrator")
```

### Document Lifecycle Hooks

Available hooks (in order):
1. `before_insert` - Before creating new document
2. `after_insert` - After creating new document
3. `validate` - Before saving (insert or update)
4. `before_save` - Before saving to database
5. `on_update` - After saving to database
6. `on_submit` - When document is submitted (if submittable)
7. `on_cancel` - When document is cancelled
8. `on_trash` - Before deleting
9. `after_delete` - After deleting

## API Development

### Whitelisting Functions

Use `@frappe.whitelist()` to expose functions to client-side or REST API:

```python
import frappe

@frappe.whitelist()
def my_api_method(arg1, arg2):
	"""Accessible via /api/method/myapp.mymodule.my_api_method"""
	return {"result": arg1 + arg2}

@frappe.whitelist(allow_guest=True)
def public_method():
	"""Accessible without authentication"""
	return {"status": "ok"}

@frappe.whitelist(methods=["POST", "PUT"])
def update_only():
	"""Only allow POST/PUT requests"""
	pass
```

### Client-Side API Calls

```javascript
// From client-side JavaScript
frappe.call({
	method: 'myapp.mymodule.my_api_method',
	args: {
		arg1: 'value1',
		arg2: 'value2'
	},
	callback: function(r) {
		console.log(r.message);
	}
});
```

### REST API

```bash
# GET request
curl http://localhost:8000/api/method/myapp.mymodule.my_api_method?arg1=value1

# POST request
curl -X POST http://localhost:8000/api/method/myapp.mymodule.my_api_method \
  -H "Content-Type: application/json" \
  -d '{"arg1": "value1", "arg2": "value2"}'
```

## Database Operations

### Using Frappe ORM

```python
# Get a document
doc = frappe.get_doc("User", "john@example.com")

# Create a new document
doc = frappe.get_doc({
	"doctype": "User",
	"email": "jane@example.com",
	"first_name": "Jane"
})
doc.insert()

# Update a document
doc = frappe.get_doc("User", "john@example.com")
doc.first_name = "Johnny"
doc.save()

# Delete a document
frappe.delete_doc("User", "john@example.com")

# Get list of documents
users = frappe.get_all("User", 
	filters={"enabled": 1},
	fields=["name", "email", "first_name"],
	order_by="creation desc",
	limit=10
)

# Get single value
email = frappe.db.get_value("User", "john@example.com", "email")

# Set value without loading document
frappe.db.set_value("User", "john@example.com", "first_name", "Johnny")

# Raw SQL (use sparingly)
frappe.db.sql("""
	SELECT name, email FROM `tabUser` 
	WHERE enabled = 1
""", as_dict=True)
```

### Query Builder (PyPika)

```python
from frappe.query_builder import DocType

User = DocType("User")
users = (
	frappe.qb.from_(User)
	.select(User.name, User.email)
	.where(User.enabled == 1)
	.orderby(User.creation, order="desc")
	.limit(10)
).run(as_dict=True)
```

## Hooks System

Hooks are defined in `hooks.py` and allow apps to extend Frappe functionality.

### Common Hooks

```python
# frappe/hooks.py

# Document lifecycle hooks
doc_events = {
	"User": {
		"before_insert": "myapp.user.before_user_insert",
		"on_update": "myapp.user.on_user_update",
	},
	"*": {
		"on_trash": "myapp.utils.log_deletion"
	}
}

# Scheduled tasks
scheduler_events = {
	"daily": [
		"myapp.tasks.daily_cleanup"
	],
	"hourly": [
		"myapp.tasks.send_notifications"
	],
	"cron": {
		"0 0 * * *": [  # Daily at midnight
			"myapp.tasks.midnight_task"
		]
	}
}

# Website routing
website_route_rules = [
	{"from_route": "/old-page", "to_route": "/new-page"},
]

# Request lifecycle hooks
before_request = ["myapp.utils.before_request"]
after_request = ["myapp.utils.after_request"]

# Override standard methods
override_whitelisted_methods = {
	"frappe.desk.form.load.getdoc": "myapp.overrides.custom_getdoc"
}

# Custom fixtures
fixtures = [
	{"dt": "Custom Field", "filters": {"module": "My App"}},
	"Role",
]
```

## Testing

### Python Unit Tests

```python
# frappe/core/doctype/user/test_user.py
import frappe
from frappe.tests import IntegrationTestCase

class TestUser(IntegrationTestCase):
	def setUp(self):
		"""Run before each test"""
		self.test_user = frappe.get_doc({
			"doctype": "User",
			"email": "test@example.com",
			"first_name": "Test"
		}).insert()
	
	def tearDown(self):
		"""Run after each test"""
		frappe.delete_doc("User", "test@example.com", force=True)
	
	def test_user_creation(self):
		"""Test user can be created"""
		self.assertEqual(self.test_user.email, "test@example.com")
	
	def test_validation(self):
		"""Test validation logic"""
		with self.assertRaises(frappe.ValidationError):
			bad_user = frappe.get_doc({
				"doctype": "User",
				"email": "invalid-email"
			})
			bad_user.insert()
```

### Running Tests

```bash
# Run all tests for a site
bench --site frappe.local run-tests

# Run tests for specific app
bench --site frappe.local run-tests --app frappe

# Run tests for specific module
bench --site frappe.local run-tests --module frappe.core.doctype.user

# Run specific test
bench --site frappe.local run-tests --test frappe.core.doctype.user.test_user.TestUser.test_user_creation
```

### Cypress UI Tests

```javascript
// cypress/integration/user.js
describe('User Form', () => {
	before(() => {
		cy.login('Administrator');
	});
	
	it('creates a new user', () => {
		cy.visit('/app/user/new');
		cy.fill_field('email', 'test@example.com');
		cy.fill_field('first_name', 'Test');
		cy.click_button('Save');
		cy.url().should('include', '/app/user/test@example.com');
	});
});
```

## Pre-commit Hooks

Pre-commit hooks enforce code quality. They run automatically on `git commit`.

### Setup Pre-commit

```bash
cd frappe-bench/apps/frappe
pre-commit install
pre-commit install --hook-type commit-msg
```

### Configured Hooks

1. **Ruff** - Python linting and formatting
2. **Prettier** - JavaScript/Vue/SCSS formatting
3. **ESLint** - JavaScript linting
4. **Trailing whitespace** - Remove trailing whitespace
5. **Commitlint** - Enforce conventional commit messages

### Manual Run

```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
```

## Asset Building

### Build Process

Frappe uses esbuild for bundling JavaScript and CSS.

```bash
# Build production assets
bench build

# Build specific app
bench build --app frappe

# Watch mode (auto-rebuild on changes)
yarn watch
# or
cd apps/frappe && yarn watch
```

### Asset Inclusion

Define in `hooks.py`:

```python
# JavaScript bundles to include
app_include_js = [
	"libs.bundle.js",
	"desk.bundle.js",
]

# CSS bundles to include
app_include_css = [
	"desk.bundle.css",
]

# Per-DocType JavaScript
doctype_js = {
	"User": "public/js/user.js",
}

# Website JavaScript
web_include_js = ["website_script.js"]
```

## Permissions System

### Role-Based Permissions

Permissions are defined per DocType and Role:

```python
# Programmatically add permissions
frappe.permissions.add_permission("User", "HR Manager", 0)

# Check permissions
if frappe.has_permission("User", "write", user="john@example.com"):
	# User has write access
	pass

# Get documents with permission check
users = frappe.get_all("User", 
	filters={"enabled": 1},
	ignore_permissions=False  # Default
)
```

### Permission Levels

- **Read** - View document
- **Write** - Edit document
- **Create** - Create new document
- **Delete** - Delete document
- **Submit** - Submit document (if submittable)
- **Cancel** - Cancel submitted document
- **Amend** - Amend cancelled document

## Performance Best Practices

### Database Queries

- Use `frappe.get_all()` instead of `frappe.get_list()` for better performance (no permission checks by default)
- Specify `fields` parameter to avoid SELECT *
- Use `frappe.get_cached_doc()` for frequently accessed documents
- Avoid N+1 queries - use `frappe.get_all()` with filters instead of loops
- Use database indexes for frequently filtered fields

### Caching

```python
# Cache a value
frappe.cache.set_value("my_key", "my_value", expires_in_sec=3600)

# Get cached value
value = frappe.cache.get_value("my_key")

# Clear cache
frappe.cache.delete_value("my_key")

# Cache entire document
doc = frappe.get_cached_doc("User", "john@example.com")
```

### Background Jobs

Use RQ for long-running tasks:

```python
# Enqueue a job
frappe.enqueue(
	"myapp.tasks.long_running_task",
	queue="default",  # or "short", "long"
	timeout=300,
	arg1="value1",
	arg2="value2"
)

# Enqueue a method on the current document
doc.enqueue_method("send_email", queue="default")
```

## Translation & Internationalization

### Translating Strings

```python
# Python
from frappe import _

message = _("Hello {0}").format(user.name)
message = _("Welcome", context="greeting")

# JavaScript
let message = __("Hello {0}", [user.name]);
let message = __("Welcome");
```

### Translation Files

- Translations stored in `frappe/translations/*.csv`
- Generate POT file: `bench --site frappe.local build-message-files`
- Translate on Crowdin or manually edit CSV files

## Debugging

### Enable Debug Mode

```bash
# In site_config.json
{
	"developer_mode": 1,
	"allow_error_traceback": 1
}
```

### Logging

```python
# Simple logging
frappe.log("Debug message")
frappe.errprint("Error message")

# Structured logging
frappe.logger().info("Info message")
frappe.logger().error("Error message")
frappe.logger().debug("Debug message")

# Print SQL queries
frappe.print_sql(True)
```

### Console Debugging

```bash
# IPython console
bench --site frappe.local console

# In console:
>>> doc = frappe.get_doc("User", "Administrator")
>>> doc.email
>>> frappe.db.sql("SELECT name FROM tabUser LIMIT 5")
```

## Common Patterns

### Creating Custom Apps

```bash
# Create new app
cd frappe-bench/apps
bench new-app myapp

# Install app to site
bench --site frappe.local install-app myapp
```

### Virtual DocTypes

For read-only data from external sources:

```python
class MyVirtualDocType(Document):
	@staticmethod
	def get_list(filters=None, page_length=20, **kwargs):
		"""Return list of documents"""
		# Fetch from external API
		return external_data
	
	@staticmethod
	def get_count(filters=None, **kwargs):
		"""Return total count"""
		return len(external_data)
	
	@staticmethod
	def get_stats(filters=None):
		"""Return stats for list view"""
		return {}
```

### Custom Print Formats

```python
# In DocType controller
def get_print_formats(self):
	return ["Standard", "Detailed", "Compact"]
```

### Email Notifications

```python
frappe.sendmail(
	recipients=["user@example.com"],
	subject="Subject Line",
	message="Email body",
	attachments=[{
		"fname": "file.pdf",
		"fcontent": pdf_content
	}]
)
```

## Deployment

### Production Checklist

- Change all default passwords
- Set up SSL/TLS certificates
- Configure Nginx reverse proxy
- Set up automated backups (`bench backup`)
- Enable Supervisor for process management
- Configure firewall rules
- Set up monitoring (Sentry integration available)
- Disable developer mode
- Set up log rotation

### Backup & Restore

```bash
# Create backup
bench --site frappe.local backup

# Restore backup
bench --site frappe.local restore /path/to/backup.sql.gz
```

## Resources

### Official Documentation
- Framework Docs: https://frappeframework.com/docs
- API Reference: https://frappeframework.com/docs/user/en/api
- Forum: https://discuss.erpnext.com/
- GitHub: https://github.com/frappe/frappe

### Key Concepts
- **DocType**: Metadata-driven data model (like a table + business logic)
- **Document**: Instance of a DocType (like a row)
- **Site**: Multi-tenant instance with its own database
- **Bench**: Development and deployment tool for Frappe apps
- **Hooks**: Extension points for customizing framework behavior
- **Whitelist**: Marking functions as callable from client-side

### File Locations
- Python modules: `frappe-bench/apps/frappe/frappe/`
- Static assets: `frappe-bench/apps/frappe/frappe/public/`
- Site files: `frappe-bench/sites/frappe.local/`
- Logs: `frappe-bench/logs/`
- Backups: `frappe-bench/sites/frappe.local/private/backups/`

## Troubleshooting

### Common Issues

**Assets not loading**
```bash
bench build --app frappe
bench clear-cache
```

**Database connection errors**
```bash
# Check MariaDB is running
sudo systemctl status mariadb

# Check Redis is running
sudo systemctl status redis
```

**Permission errors**
```bash
# Fix file permissions
cd frappe-bench
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
chmod +x env/bin/*
```

**Migration errors**
```bash
# Run migrate with debug
bench --site frappe.local migrate --skip-failing

# Reset specific DocType
bench --site frappe.local console
>>> frappe.reload_doc('module_name', 'doctype', 'doctype_name')
```

### Getting Help

1. Check error logs: `frappe-bench/logs/`
2. Enable developer mode for detailed tracebacks
3. Search the forum: https://discuss.erpnext.com/
4. Check GitHub issues: https://github.com/frappe/frappe/issues
5. Read the source code - it's well-commented!

## Development Workflow

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, commit with conventional commits
git commit -m "feat: add new user field"

# Pre-commit hooks run automatically

# Push and create PR
git push origin feature/my-feature
```

### Conventional Commits

Follow conventional commit format (enforced by commitlint):

- `feat: description` - New feature
- `fix: description` - Bug fix
- `docs: description` - Documentation changes
- `style: description` - Code style changes
- `refactor: description` - Code refactoring
- `test: description` - Test changes
- `chore: description` - Build/tooling changes

---

**Last Updated**: 2026-02-19
**Framework Version**: v15.100.1

---

## Notes: Documentation & Requirements Engineering Best Practices

### Large Document Creation Strategy
When creating comprehensive documentation (requirements, user stories, technical designs):

**Approach:**
- Create initial file with header and structure overview
- Build incrementally using `find_and_replace_code` in manageable chunks (300-500 lines per update)
- Each iteration should add one complete section or subsection
- Always include clear section markers (##, ###) for easy navigation

**Avoid:**
- Attempting to create entire large documents (1000+ lines) in a single `create_file` call
- This can lead to JSON parsing errors and incomplete file creation

### Requirements Documentation Workflow
**Successful Pattern Demonstrated:**
1. Start with **Functional Requirements** document
   - Executive summary and objectives
   - Detailed requirements by module (FR-XXX-XXX format)
   - Non-functional requirements (NFR-XXX-XXX format)
   - Include glossary, risks, and approval sections
   
2. Generate **User Stories** from requirements
   - Standard format: As a [role], I want [feature], So that [benefit]
   - Include: Story ID, Epic, Priority (MoSCoW), Story Points, Acceptance Criteria, Dependencies
   - Group by Epics for better organization
   - Add sprint planning guidance and story point summaries
   
3. Create **Technical Design** from user stories
   - Application architecture and module structure
   - Complete DocType specifications (fields, types, validations)
   - Database schema with indexes
   - API endpoint designs with code examples
   - Integration points and security design
   - Performance considerations and caching strategies
   - Implementation checklist with timeline

### DocType Design Best Practices
**Field Naming Conventions:**
- Use `snake_case` for field names: `patient_name`, `appointment_date`
- Prefix boolean fields: `is_active`, `has_batch_no`
- Use descriptive names for better readability

**DocType Types:**
- **Master DocTypes**: Reference data (Patient, Staff, Machine) - use field-based naming
- **Transaction DocTypes**: Operational records (Appointment, Session, Bill) - use auto-naming with year
- **Submittable DocTypes**: Documents requiring workflow (Session, Bill) - add submit/cancel states

**Naming Patterns:**
- `{PREFIX}-{YYYY}-{#####}` for transactions (e.g., `PT-2026-00001`)
- Field-based naming for masters
- Keep prefixes short (2-3 characters)

### API Design Pattern
**Whitelist Functions Properly:**
```python
@frappe.whitelist()
def api_function(param1, param2):
    # Always validate inputs
    # Return structured data
    # Handle errors gracefully
```

**Base URL Pattern:** `/api/method/{app}.api.{module}.{function}`

### Documentation Deliverables for Healthcare Systems
For complex domain applications (like healthcare), provide:
1. **Functional Requirements** (~1000 lines)
   - 80+ detailed requirements
   - Module-based organization
   - Acceptance criteria

2. **User Stories** (~1600 lines)
   - 50-60 stories grouped by 10-12 epics
   - 250-300 story points total
   - Sprint planning reference

3. **Technical Design** (~2100 lines)
   - 25+ DocType specifications
   - Complete database schema
   - API endpoints with code
   - Deployment architecture

**Estimated Delivery:** 6-8 months for team of 3-4 developers (based on story points)

### Module Organization for Large Apps
**Structure by Business Domain:**
```
app_name/
├── patient_management/
├── appointment_scheduling/
├── clinical_operations/
├── laboratory/
├── inventory/
├── equipment/
├── billing/
├── staff/
└── reporting/
```

Each module contains:
- `doctype/` - Data models
- `page/` - Custom pages
- `report/` - Reports specific to module

### API Documentation Best Practices
**OpenAPI/Swagger Specification Pattern:**
1. **Complete 4-Phase Documentation Stack:**
   - Phase 1: Functional Requirements (business logic, FR-XXX format)
   - Phase 2: User Stories (agile stories, epics, story points)
   - Phase 3: Technical Design (DocTypes, schemas, implementation)
   - Phase 4: API Specification (OpenAPI YAML, endpoints, schemas)

2. **OpenAPI File Structure:**
   - Start with metadata, servers, authentication schemes
   - Group endpoints by logical modules (Patient, Appointment, Session, etc.)
   - Define reusable schemas in `components/schemas`
   - Include request/response examples for clarity
   - Document security requirements per endpoint
   - Add rate limiting and error response patterns

3. **YAML Creation Strategy:**
   - Initial file: metadata + first few endpoints (~500 lines)
   - Incremental additions: 1-2 modules per update (~300-400 lines)
   - Ensures valid YAML structure throughout
   - Easier to validate and test incrementally

4. **Authentication Patterns for Frappe:**
   - API Key: `Authorization: token {api_key}:{api_secret}`
   - Session-based: Cookie authentication for web clients
   - Document both methods in security schemes

5. **Endpoint Naming Convention:**
   - List: `GET /api/resource/{doctype}`
   - Get: `GET /api/resource/{doctype}/{name}`
   - Create: `POST /api/resource/{doctype}`
   - Update: `PUT /api/resource/{doctype}/{name}`
   - Custom methods: `POST /api/method/{app}.api.{module}.{function}`

**Deliverables for Complete Project Documentation:**
- Functional Requirements: ~1000 lines
- User Stories: ~1600 lines
- Technical Design: ~2100 lines
- API Specification: ~2000 lines (40+ endpoints)
- Frontend Design: ~1500 lines
- Development Environment Setup: ~1400 lines
- **Total**: ~9700 lines of comprehensive documentation

### Frontend Documentation Best Practices
**5-Phase Complete Documentation Stack:**
1. Functional Requirements → Business logic and acceptance criteria
2. User Stories → Agile epics and story points
3. Technical Design → Backend, database, DocTypes
4. API Specification → OpenAPI/Swagger endpoints
5. Frontend Design → UI/UX, components, implementation

**Frontend Document Structure:**
- **Architecture** (~200 lines): Tech stack, file structure, bundle config
- **Design System** (~200 lines): Colors, typography, spacing, shadows
- **Layouts & Navigation** (~200 lines): Page structure, navigation patterns
- **Component Library** (~400 lines): Reusable Vue components with examples
- **Forms & Validation** (~200 lines): DocType forms, validation utilities
- **Dashboard & Analytics** (~200 lines): Real-time dashboards, charts
- **Workflows** (~200 lines): Clinical/business process interfaces
- **State Management** (~100 lines): Store pattern, real-time updates
- **API Integration** (~100 lines): Helper functions organized by module
- **Performance** (~100 lines): Caching, debouncing, optimization
- **Accessibility** (~100 lines): WCAG compliance, keyboard nav, ARIA
- **Testing** (~100 lines): Unit, component, E2E test examples
- **Build & Deploy** (~100 lines): esbuild config, optimization checklist

**Key Frontend Patterns:**
- Use `bash cat >> file.md << 'EOF'` for adding large code blocks (avoids JSON escaping issues)
- Vue 3 Composition API for all components
- Frappe UI integration patterns (frappe.call, frappe.ui.Dialog)
- Real-time updates via frappe.realtime.on()
- Mobile-first responsive design with SCSS mixins
- Component naming: PascalCase (Vue), kebab-case (CSS), camelCase (JS)

**Bash Append Strategy for Large Content:**
When adding substantial code examples or multi-section content:
- Use `cat >> filename << 'EOF'` instead of `find_and_replace_code`
- Avoids JSON parsing issues with special characters (backticks, quotes)
- Better for adding 500+ line blocks with mixed HTML/JS/CSS
- Check file end state with `tail` before appending

**Last Updated**: 2026-02-19
**Framework Version**: v15.100.1
