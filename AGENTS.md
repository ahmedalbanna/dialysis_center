# Frappe Framework Development Guide

## Using Specialized Subagents for Efficient Development

**Rovo Dev** has access to 15 specialized subagents, each with deep expertise in specific domains. To maximize efficiency, delegate tasks using the appropriate subagent with its dedicated memory file:

### Quick Subagent Reference

| Task Type | Subagent | Memory File | Best For |
|-----------|----------|-------------|----------|
| **DocType Design** | DocType-Architect | `.rovodev/subagents/memory/DocType-Architect.memory.md` | Creating/modifying DocTypes, field definitions, validations |
| **API Development** | API-Whitelister | `.rovodev/subagents/memory/API-Whitelister.memory.md` | Whitelisted methods, REST APIs, authentication |
| **Database Operations** | Database-Navigator | `.rovodev/subagents/memory/Database-Navigator.memory.md` | ORM queries, optimization, migrations, indices |
| **Hooks & Events** | Hooks-Orchestrator | `.rovodev/subagents/memory/Hooks-Orchestrator.memory.md` | Document lifecycle, scheduled tasks, event handlers |
| **Frontend Development** | Frontend-Forge | `.rovodev/subagents/memory/Frontend-Forge.memory.md` | Vue components, forms, custom scripts, assets |
| **Permissions** | Permission-Guardian | `.rovodev/subagents/memory/Permission-Guardian.memory.md` | Role-based access, document sharing, security |
| **Workflows** | Workflow-Wizard | `.rovodev/subagents/memory/Workflow-Wizard.memory.md` | State machines, approvals, transitions |
| **Testing** | Test-Engineer | `.rovodev/subagents/memory/Test-Engineer.memory.md` | Unit tests, integration tests, fixtures |
| **Bench Operations** | Bench-Master | `.rovodev/subagents/memory/Bench-Master.memory.md` | Site management, migrations, deployments |
| **Debugging** | Debug-Detective | `.rovodev/subagents/memory/Debug-Detective.memory.md` | Error diagnosis, logs, troubleshooting |
| **Module Structure** | Module-Designer | `.rovodev/subagents/memory/Module-Designer.memory.md` | App layout, workspaces, navigation |
| **Third-party APIs** | Integration-Specialist | `.rovodev/subagents/memory/Integration-Specialist.memory.md` | Webhooks, payment gateways, external sync |
| **Code Quality** | Ruff-Formatter | `.rovodev/subagents/memory/Ruff-Formatter.memory.md` | Code style, linting, pre-commit |
| **Mobile Apps** | PWA-Builder | `.rovodev/subagents/memory/PWA-Builder.memory.md` | Service workers, offline mode, mobile UI |
| **Frappe Setup** | frappe-installer | `.rovodev/subagents/memory/frappe-installer.memory.md` | Environment setup, Docker, production |

### How to Use Subagents

**Pattern 1: Delegate a Single Task**
```python
# Example: Create a DocType
invoke_subagents(
    subagent_names=["DocType-Architect"],
    task_descriptions=["Create a Patient DocType with fields: patient_id, name, date_of_birth, blood_type, medical_history"],
    task_names=["Create Patient DocType"],
    additional_memory_file=".rovodev/subagents/memory/DocType-Architect.memory.md"
)
```

**Pattern 2: Delegate Multiple Independent Tasks**
```python
# Example: Parallel development
invoke_subagents(
    subagent_names=["DocType-Architect", "API-Whitelister", "Test-Engineer"],
    task_descriptions=[
        "Create Appointment DocType with date, time, doctor, patient fields",
        "Create API endpoints for appointment booking and retrieval",
        "Write unit tests for appointment validation and permissions"
    ],
    task_names=["Appointment DocType", "Appointment APIs", "Appointment Tests"],
    additional_memory_file=[
        ".rovodev/subagents/memory/DocType-Architect.memory.md",
        ".rovodev/subagents/memory/API-Whitelister.memory.md",
        ".rovodev/subagents/memory/Test-Engineer.memory.md"
    ]
)
```

**Pattern 3: Sequential Task Chain**
```python
# Step 1: Create the data model
invoke_subagents(
    subagent_names=["DocType-Architect"],
    task_descriptions=["Create Session DocType..."],
    task_names=["Session DocType"],
    additional_memory_file=".rovodev/subagents/memory/DocType-Architect.memory.md"
)

# Step 2: Create APIs (after DocType is ready)
invoke_subagents(
    subagent_names=["API-Whitelister"],
    task_descriptions=["Create REST APIs for Session management..."],
    task_names=["Session APIs"],
    additional_memory_file=".rovodev/subagents/memory/API-Whitelister.memory.md"
)

# Step 3: Write tests (after APIs are defined)
invoke_subagents(
    subagent_names=["Test-Engineer"],
    task_descriptions=["Write comprehensive tests for Session APIs..."],
    task_names=["Session Tests"],
    additional_memory_file=".rovodev/subagents/memory/Test-Engineer.memory.md"
)
```

### When to Use Each Subagent

**DocType-Architect**
- Creating new DocTypes or modifying existing ones
- Designing field structures and relationships
- Implementing custom validations
- Creating child tables and linked documents
- Use when: Data model design is needed

**API-Whitelister**
- Creating new whitelisted methods
- Designing REST API endpoints
- Implementing authentication/authorization
- Creating API documentation
- Use when: Backend API functionality is needed

**Database-Navigator**
- Writing complex queries
- Optimizing slow queries
- Creating database indices
- Running migrations
- Data transformation scripts
- Use when: Database operations or optimization needed

**Hooks-Orchestrator**
- Implementing document lifecycle hooks
- Creating scheduled background tasks
- Setting up event handlers
- Configuring system hooks
- Use when: Document events or automation needed

**Frontend-Forge**
- Creating custom Vue components
- Building form customizations
- Implementing dashboards
- Managing static assets
- Use when: Frontend/UI development needed

**Permission-Guardian**
- Setting up role-based access control
- Implementing document-level permissions
- Creating user permission rules
- Auditing security configurations
- Use when: Security/access control needed

**Workflow-Wizard**
- Designing workflow states and transitions
- Creating approval chains
- Implementing conditional routing
- Setting up workflow notifications
- Use when: Business process automation needed

**Test-Engineer**
- Writing unit tests
- Creating integration tests
- Setting up test fixtures
- Implementing test data factories
- Use when: Testing and quality assurance needed

**Bench-Master**
- Managing Frappe sites
- Running migrations
- Deploying applications
- Configuring production environments
- Use when: Deployment or site management needed

**Debug-Detective**
- Diagnosing errors and issues
- Reading error logs
- Troubleshooting permission errors
- Fixing migration issues
- Use when: Debugging or troubleshooting needed

**Module-Designer**
- Creating complete modules
- Designing module structure
- Setting up workspaces
- Configuring navigation
- Use when: Large-scale module creation needed

**Integration-Specialist**
- Connecting to third-party APIs
- Implementing webhooks
- Setting up payment gateway integration
- Synchronizing external data
- Use when: Third-party integration needed

**Ruff-Formatter**
- Enforcing code style
- Running linters
- Pre-commit hook setup
- Code quality checks
- Use when: Code formatting/quality assurance needed

**PWA-Builder**
- Building mobile-first interfaces
- Implementing offline functionality
- Creating service workers
- Mobile app optimization
- Use when: Mobile/PWA development needed

**frappe-installer**
- Setting up Frappe environments
- Installing dependencies
- Configuring Docker/production
- Running installation scripts
- Use when: Initial Frappe setup needed

### Decision Tree: Which Subagent to Use?

```
START: I need to develop a feature
│
├─ Is it DATA MODEL related?
│  ├─ YES → Use: DocType-Architect
│  │        (Create/modify DocTypes, fields, validations)
│  └─ NO → Continue...
│
├─ Is it BACKEND/API related?
│  ├─ YES → Use: API-Whitelister
│  │        (Create whitelisted methods, REST APIs, auth)
│  └─ NO → Continue...
│
├─ Is it DATABASE related?
│  ├─ YES → Use: Database-Navigator
│  │        (Queries, optimization, migrations)
│  └─ NO → Continue...
│
├─ Is it FRONTEND/UI related?
│  ├─ YES → Use: Frontend-Forge
│  │        (Vue components, forms, dashboards)
│  └─ NO → Continue...
│
├─ Is it DOCUMENT AUTOMATION related?
│  ├─ YES, lifecycle hooks? → Use: Hooks-Orchestrator
│  ├─ YES, workflows? → Use: Workflow-Wizard
│  └─ NO → Continue...
│
├─ Is it SECURITY/ACCESS related?
│  ├─ YES → Use: Permission-Guardian
│  │        (Roles, permissions, sharing)
│  └─ NO → Continue...
│
├─ Is it TESTING related?
│  ├─ YES → Use: Test-Engineer
│  │        (Unit tests, integration tests)
│  └─ NO → Continue...
│
├─ Is it DEPLOYMENT/INFRASTRUCTURE related?
│  ├─ YES, setup? → Use: frappe-installer
│  ├─ YES, site management? → Use: Bench-Master
│  └─ NO → Continue...
│
├─ Is it INTEGRATION with external systems?
│  ├─ YES → Use: Integration-Specialist
│  │        (APIs, webhooks, payments)
│  └─ NO → Continue...
│
├─ Is it MOBILE/PWA related?
│  ├─ YES → Use: PWA-Builder
│  │        (Service workers, offline, mobile UI)
│  └─ NO → Continue...
│
├─ Is it MODULE STRUCTURE related?
│  ├─ YES → Use: Module-Designer
│  │        (Module layout, workspaces)
│  └─ NO → Continue...
│
├─ Is it CODE QUALITY/FORMATTING?
│  ├─ YES → Use: Ruff-Formatter
│  │        (Linting, style enforcement)
│  └─ NO → Continue...
│
└─ Is it DEBUGGING/TROUBLESHOOTING?
   ├─ YES → Use: Debug-Detective
   │        (Error diagnosis, logs)
   └─ NO → Ask clarifying questions
```

### Best Practices for Subagent Usage

1. **Always Provide Memory File**
   - Every subagent call should include `additional_memory_file` parameter
   - Memory files contain domain-specific patterns and best practices
   - Example: `additional_memory_file=".rovodev/subagents/memory/DocType-Architect.memory.md"`

2. **Be Specific with Task Descriptions**
   - Include requirements, constraints, and expected outcomes
   - Example: ✅ "Create Patient DocType with mandatory fields: patient_id, name, email, phone. Include validation for email format and unique patient_id"
   - Example: ❌ "Create a DocType for patients" (too vague)

3. **Use Parallel Execution for Independent Tasks**
   - When tasks don't depend on each other, invoke multiple subagents simultaneously
   - Maximum 4 concurrent subagents per invocation
   - Saves time and reduces overall execution time

4. **Chain Tasks for Dependent Work**
   - When Task B depends on Task A being complete, invoke sequentially
   - Task A → Wait for completion → Task B
   - Example: DocType → API → Tests

5. **Validate Subagent Output**
   - Review generated code for correctness
   - Ensure it follows Frappe conventions
   - Test before deploying to production

6. **Reuse Memory Files Across Projects**
   - Memory files are generic and apply to any Frappe application
   - No need to recreate for each project
   - Ensures consistency across all projects

7. **Document Custom Requirements**
   - If a task has special requirements beyond standard patterns
   - Include them explicitly in the task description
   - This helps subagents provide more targeted solutions

### Example Workflows: Real-World Development Scenarios

#### Scenario 1: Build a Complete Patient Management Module

**Step 1: Create Data Models (Parallel)**
```python
invoke_subagents(
    subagent_names=["DocType-Architect", "DocType-Architect"],
    task_descriptions=[
        "Create Patient DocType with fields: patient_id (Link, unique), name (Data), email (Data), phone (Data), date_of_birth (Date), blood_type (Select: O+, O-, A+, A-, B+, B-, AB+, AB-), medical_history (Text). Add validations: email format, unique patient_id, date_of_birth cannot be in future",
        "Create Medical Record DocType with fields: patient (Link to Patient), visit_date (Date), diagnosis (Text), treatment (Text), notes (TextEditor). Make it submittable. Add child table 'prescriptions' with fields: medicine_name, dosage, frequency, duration_days"
    ],
    task_names=["Patient DocType", "Medical Record DocType"],
    additional_memory_file=".rovodev/subagents/memory/DocType-Architect.memory.md"
)
```

**Step 2: Create Backend APIs (After Step 1)**
```python
invoke_subagents(
    subagent_names=["API-Whitelister"],
    task_descriptions=[
        "Create whitelisted API methods for Patient management: get_patient_list (returns all patients with filters for name, blood_type, created_date), get_patient_details (returns complete patient info with recent medical records), create_patient (creates new patient with validation), update_patient (updates patient fields with audit trail). Include proper error handling and permission checks"
    ],
    task_names=["Patient APIs"],
    additional_memory_file=".rovodev/subagents/memory/API-Whitelister.memory.md"
)
```

**Step 3: Create Frontend UI (After Step 1)**
```python
invoke_subagents(
    subagent_names=["Frontend-Forge"],
    task_descriptions=[
        "Create Patient List page with Vue 3: display all patients in table with columns (patient_id, name, blood_type, last_visit). Add filters for blood_type and date range. Add button to create new patient. Add search by name. Include pagination. Style with SCSS following Frappe conventions"
    ],
    task_names=["Patient List UI"],
    additional_memory_file=".rovodev/subagents/memory/Frontend-Forge.memory.md"
)
```

**Step 4: Create Tests (After Steps 2 & 3)**
```python
invoke_subagents(
    subagent_names=["Test-Engineer"],
    task_descriptions=[
        "Write comprehensive tests for Patient module: test patient creation with valid/invalid data, test email validation, test unique patient_id constraint, test permission checks, test API endpoints with various filters. Create test fixtures for patient data. Include both unit and integration tests"
    ],
    task_names=["Patient Tests"],
    additional_memory_file=".rovodev/subagents/memory/Test-Engineer.memory.md"
)
```

**Step 5: Setup Module Structure (After Steps 1-4)**
```python
invoke_subagents(
    subagent_names=["Module-Designer"],
    task_descriptions=[
        "Create patient_management module with proper workspace, navigation, and dashboard. Include quick create shortcuts for Patient and Medical Record. Add dashboard showing total patients, recent visits, and patients by blood type. Configure menu items and module permissions"
    ],
    task_names=["Patient Module"],
    additional_memory_file=".rovodev/subagents/memory/Module-Designer.memory.md"
)
```

#### Scenario 2: Add Document Automation and Workflows

**Step 1: Create Automation (Independent)**
```python
invoke_subagents(
    subagent_names=["Hooks-Orchestrator"],
    task_descriptions=[
        "Implement document lifecycle hooks for Medical Record DocType: before_insert - assign next visit date automatically (30 days from visit_date), on_submit - send notification to patient, after_submit - create automatic follow-up task, before_cancel - check if any related prescriptions are pending"
    ],
    task_names=["Medical Record Automation"],
    additional_memory_file=".rovodev/subagents/memory/Hooks-Orchestrator.memory.md"
)
```

**Step 2: Create Approval Workflow (Independent)**
```python
invoke_subagents(
    subagent_names=["Workflow-Wizard"],
    task_descriptions=[
        "Create approval workflow for Medical Record: states (Draft, Pending Approval, Approved, Rejected). Draft → Pending Approval (auto on submit). Pending Approval → Approved (by Doctor role) or Rejected (by Doctor role). Add conditional routing: if treatment cost > 5000, require Hospital Manager approval. Setup email notifications for state transitions"
    ],
    task_names=["Medical Record Workflow"],
    additional_memory_file=".rovodev/subagents/memory/Workflow-Wizard.memory.md"
)
```

#### Scenario 3: Database Optimization

**Step 1: Analyze and Optimize**
```python
invoke_subagents(
    subagent_names=["Database-Navigator"],
    task_descriptions=[
        "Analyze Patient and Medical Record tables for query optimization: identify missing indices on frequently queried fields (patient in Medical Record, visit_date, created date), write optimized query for getting patient medical history with pagination, create migration script to add indices: (patient, visit_date) on Medical Record, (name, created) on Patient. Check for N+1 query problems in patient list views"
    ],
    task_names=["Database Optimization"],
    additional_memory_file=".rovodev/subagents/memory/Database-Navigator.memory.md"
)
```

#### Scenario 4: Integration with External System

**Step 1: Setup Integration**
```python
invoke_subagents(
    subagent_names=["Integration-Specialist"],
    task_descriptions=[
        "Create integration with external EMR (Electronic Medical Records) system: setup webhook handler to receive patient updates from EMR, create API method to push Medical Record to EMR on submission, implement sync mechanism to check for updates periodically, handle errors with retry logic, add audit logging for all integration calls"
    ],
    task_names=["EMR Integration"],
    additional_memory_file=".rovodev/subagents/memory/Integration-Specialist.memory.md"
)
```

#### Scenario 5: Complete Deployment

**Step 1: Setup Environment (First Time)**
```python
invoke_subagents(
    subagent_names=["frappe-installer"],
    task_descriptions=[
        "Setup Frappe development environment on Linux: install MariaDB 10.11, Redis 7.0, Python 3.10+, Node.js 22, install wkhtmltopdf, create bench directory, initialize Frappe bench, create frappe.local site, setup auto-backup, configure development settings"
    ],
    task_names=["Frappe Setup"],
    additional_memory_file=".rovodev/subagents/memory/frappe-installer.memory.md"
)
```

**Step 2: Deploy Application**
```python
invoke_subagents(
    subagent_names=["Bench-Master"],
    task_descriptions=[
        "Deploy patient_management app to production: create production site, run migrations, install app, setup supervisor for process management, configure Nginx reverse proxy, setup SSL certificates, enable auto-backups with daily scheduling, verify all services running"
    ],
    task_names=["Patient App Deployment"],
    additional_memory_file=".rovodev/subagents/memory/Bench-Master.memory.md"
)
```

### Common Task Combinations

| Feature | Subagents to Use | Sequence |
|---------|------------------|----------|
| **New DocType** | DocType-Architect | Sequential: DocType → API → Test |
| **API Endpoint** | API-Whitelister, Test-Engineer | Parallel: API + Tests |
| **Frontend Form** | DocType-Architect, Frontend-Forge, Test-Engineer | Sequential: DocType → Frontend → Tests |
| **Full Module** | All 15 subagents | Planned parallelization with dependencies |
| **Bug Fix** | Debug-Detective, relevant subagent | Sequential: Debug → Fix |
| **Performance** | Database-Navigator, Bench-Master | Parallel: Analyze + Optimize |
| **Security Audit** | Permission-Guardian, Debug-Detective | Parallel: Audit + Test |
| **Code Quality** | Ruff-Formatter, Test-Engineer | Parallel: Format + Test |

---

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

## Advanced DocType System

### Complete Field Type Reference

**Standard Field Types with Properties:**

| Field Type | Storage | Searchable | Use Case | Properties |
|-----------|---------|-----------|----------|-----------|
| `Link` | Foreign key | Yes | References to other DocTypes | `options` (target DocType), `ignore_user_permissions` |
| `Select` | Enum | Yes | Predefined options | `options` (newline-separated values) |
| `MultiSelect` | JSON array | Yes | Multiple selections | `options` (newline-separated values) |
| `Data` | VARCHAR(255) | Yes | General text | `length`, `unique`, `read_only` |
| `Text` | TEXT | Limited | Long text | `in_list_view`, `in_standard_filter` |
| `Text Editor` | LONGTEXT | No | Rich HTML content | Uses TinyMCE editor |
| `Integer` | INT | Yes | Whole numbers | `default` |
| `Float` | DECIMAL(19,6) | Yes | Decimal numbers | `precision` |
| `Currency` | DECIMAL(19,6) | Yes | Monetary values | `precision`, `fieldtype` |
| `Percent` | DECIMAL(5,2) | Yes | Percentages | Default 0-100 range |
| `Checkbox` | BOOLEAN | Yes | True/false toggle | No special properties |
| `Date` | DATE | Yes | Calendar dates | `default` (e.g., "today") |
| `Datetime` | DATETIME | Yes | Timestamp | `default` (e.g., "now") |
| `Time` | TIME | Yes | Time values | No special properties |
| `Duration` | INT | Yes | Time duration (seconds) | Stores as seconds |
| `Table` | Child table | Limited | Row-based data | `options` (child DocType name) |
| `Attach` | VARCHAR(255) | Limited | File upload | Stores file path |
| `Attach Image` | VARCHAR(255) | Limited | Image upload | Validates image MIME type |
| `Rating` | SMALLINT | Yes | Star rating | `options` (1-10) |
| `Barcode` | VARCHAR(255) | Yes | Barcode data | `barcode_type` |
| `Color` | VARCHAR(7) | Yes | Hex color | Default #000000 |
| `JSON` | LONGTEXT | No | Structured data | No validation |
| `Read Only` | VARCHAR(255) | No | Display only | Computed/formula fields |
| `GeoData` | LONGTEXT | No | Geographic data | GIS support |

### Lifecycle Hooks: Complete Execution Order

```python
# frappe/model/document.py - Actual lifecycle execution
class Document:
	def insert(self, ignore_permissions=False, ignore_links=False, ignore_validate=False, ignore_mandatory=False, ignore_children=False, ignore_on_submit=False, ignore_if_duplicate=False):
		# 1. before_insert hook (custom apps)
		self.run_doc_method("before_insert")
		
		# 2. validate hook
		self.validate()
		
		# 3. before_save hook
		self.run_doc_method("before_save")
		
		# 4. Insert into database
		self.db_insert()
		
		# 5. after_insert hook
		self.run_doc_method("after_insert")
		
		# 6. Async: Run doc_events hooks
		frappe.publish_realtime("doctype_insert", {"doctype": self.doctype, "name": self.name})

	def save(self, ignore_permissions=False, ...):
		# For updates:
		# 1. validate hook
		self.validate()
		
		# 2. before_save hook
		self.run_doc_method("before_save")
		
		# 3. db_update() to database
		self.db_update()
		
		# 4. on_update hook
		self.run_doc_method("on_update")
		
		# 5. async realtime events

	def submit(self, ignore_permissions=False, ...):
		# Submittable documents only
		# 1. before_submit hook
		# 2. on_submit hook
		# 3. Update status to Submitted
		# 4. Log change in changelog

	def cancel(self):
		# For submitted documents
		# 1. before_cancel hook
		# 2. on_cancel hook
		# 3. Update status to Cancelled

	def delete(self, ignore_permissions=False, ...):
		# 1. before_trash hook
		# 2. Check if_delete_after_days
		# 3. Physical delete or mark as deleted
		# 4. on_trash hook
		# 5. after_delete hook
```

**Hook Execution Guarantee:**
- `validate`, `before_save`, `on_update`: ALWAYS executed on document save
- `before_insert`, `after_insert`: Only on new document insert
- `on_submit`, `on_cancel`: Only on submittable DocTypes
- Child table `validate()` runs BEFORE parent validate
- All doc_event hooks defined in hooks.py run AFTER database operations

### Advanced Field Validation Patterns

```python
class MyDocType(Document):
	def validate(self):
		"""Comprehensive validation example"""
		# 1. Required field checking (automatic with mandatory flag)
		
		# 2. Cross-field validation
		if self.start_date and self.end_date:
			if self.start_date > self.end_date:
				frappe.throw(_("Start date must be before end date"))
		
		# 3. Conditional validation
		if self.status == "Active" and not self.valid_till:
			frappe.throw(_("Valid till date required for active records"))
		
		# 4. Database lookups
		if frappe.db.exists("DocType", {"name": self.reference_name, "docstatus": 1}):
			# Reference is submitted
			pass
		
		# 5. Child table validation
		if not self.child_table:
			frappe.throw(_("At least one row required"))
		
		# 6. Duplicate checking
		duplicate = frappe.db.exists("MyDocType", {
			"field1": self.field1,
			"field2": self.field2,
			"name": ["!=", self.name]  # Exclude current doc
		})
		if duplicate:
			frappe.throw(_("Duplicate record found"))
	
	def before_save(self):
		"""Pre-save data transformation"""
		# 1. Trim whitespace
		self.name_field = self.name_field.strip() if self.name_field else ""
		
		# 2. Normalize data
		self.email = self.email.lower()
		
		# 3. Calculate computed fields
		self.total = sum(d.amount for d in self.items)
		
		# 4. Set defaults
		if not self.created_date:
			self.created_date = frappe.utils.today()
	
	def on_update(self):
		"""Post-save business logic"""
		# Update related records
		frappe.db.set_value("LinkedDoc", self.linked_doc_name, "status", self.status)
		
		# Clear caches
		frappe.cache.delete_value(f"myapp_{self.name}")
		
		# Trigger workflows
		if self.status_changed():
			self.trigger_workflow()
```

### Child Table Operations & Relationships

```python
class ParentDocType(Document):
	def validate(self):
		"""Child table validation patterns"""
		# Validate child rows
		for i, row in enumerate(self.child_table, 1):
			if row.quantity <= 0:
				frappe.throw(_("Row {0}: Quantity must be positive").format(i))
			
			# Cross-reference validation
			item_doc = frappe.get_doc("Item", row.item_code)
			if item_doc.disabled:
				frappe.throw(_("Row {0}: Item {1} is disabled").format(i, row.item_code))
			
			# Update child row computed fields
			row.total = row.quantity * row.rate
	
	def before_save(self):
		"""Calculate parent totals from child rows"""
		self.total_quantity = sum(d.quantity for d in self.child_table)
		self.grand_total = sum(d.total for d in self.child_table)

# Accessing child tables
doc = frappe.get_doc("Parent", "doc_name")
print(doc.child_table)  # List of child row objects
print(doc.child_table[0].field_name)  # Access child field

# Adding child rows programmatically
doc.append("child_table", {
	"field1": "value1",
	"field2": "value2"
})
doc.save()

# Working with child table as list
items = [d.as_dict() for d in doc.items]
```

### Custom Field Creation & Management

```python
# Programmatically create custom fields
def create_custom_field():
	# Custom Field DocType definition
	frappe.get_doc({
		"doctype": "Custom Field",
		"dt": "MyDocType",  # Target DocType
		"fieldname": "custom_field_name",
		"fieldtype": "Data",
		"label": "Custom Field Label",
		"insert_after": "existing_field_name",
		"is_mandatory": False,
		"read_only": False,
		"in_list_view": True,
		"in_standard_filter": True,
		"default": "default_value",
		"options": None,  # For Link/Select types
		"unique": False,
		"hidden": False,
		"allow_on_submit": False,
		"depends_on": "eval: doc.status == 'Draft'",  # Conditional show
	}).insert(ignore_permissions=True)

# Get custom fields for a DocType
custom_fields = frappe.get_all("Custom Field", filters={"dt": "MyDocType"})

# Modify custom field
frappe.db.set_value("Custom Field", 
	{"dt": "MyDocType", "fieldname": "custom_field_name"},
	"is_mandatory", 1
)
```

### DocType Permissions & Sharing

```python
# DocType-level permissions (who can do what)
# Set in DocType UI or programmatically:
frappe.permissions.add_permission("MyDocType", "Role Name", 0)  # 0 = DocType level

# Document-level sharing (access to specific documents)
frappe.share.add(
	doctype="MyDocType",
	name="document_name",
	user="user@example.com",
	perm_type="write",  # read, write, submit
	notify=True
)

# Check document access
if frappe.has_permission("MyDocType", "write", doc=doc):
	# User has write permission
	pass
```

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

## Server-Side Development Patterns

### Document Lifecycle Hooks - Practical Patterns

```python
# frappe/core/doctype/document_lifecycle.py - Complete example

class Order(Document):
	"""Example showing all lifecycle hooks in action"""
	
	def before_insert(self):
		"""Called before new document is inserted - useful for initialization"""
		# Set defaults only for new documents
		if not self.order_date:
			self.order_date = frappe.utils.today()
		if not self.status:
			self.status = "Draft"
		# Generate unique identifiers
		self.reference_number = self.generate_reference()
	
	def before_save(self):
		"""Called before ANY save (insert or update) - data preparation"""
		# Normalize data
		self.customer_name = self.customer_name.strip().title() if self.customer_name else ""
		
		# Calculate computed fields
		self.total_amount = self.calculate_total()
		self.tax_amount = self.calculate_tax()
		self.grand_total = self.total_amount + self.tax_amount
		
		# Data transformation
		self.normalized_phone = self.normalize_phone(self.phone)
	
	def validate(self):
		"""Called before save - business logic validation"""
		# Check mandatory relationships
		if not frappe.db.exists("Customer", self.customer):
			frappe.throw(_("Customer {0} does not exist").format(self.customer))
		
		# Cross-field validation
		if self.delivery_date and self.order_date:
			if self.delivery_date < self.order_date:
				frappe.throw(_("Delivery date must be after order date"))
		
		# Validate child table
		if not self.items:
			frappe.throw(_("At least one item is required"))
		
		total_qty = 0
		for i, item in enumerate(self.items, 1):
			if item.qty <= 0:
				frappe.throw(_("Row {0}: Quantity must be positive").format(i))
			
			# Check item validity
			if not frappe.db.exists("Item", item.item_code):
				frappe.throw(_("Row {0}: Item {1} not found").format(i, item.item_code))
			
			# Update row total
			item.line_total = item.qty * item.rate
			total_qty += item.qty
		
		# Check business rules
		if total_qty > 1000 and self.customer_type == "New":
			frappe.msgprint(_("Warning: Large order from new customer"))
	
	def after_insert(self):
		"""Called after new document is inserted - post-creation tasks"""
		# Log the creation
		frappe.log("Order created: {0}".format(self.name))
		
		# Send notification email
		self.send_confirmation_email()
		
		# Create related documents
		self.create_auto_invoice() if self.auto_invoice else None
	
	def on_update(self):
		"""Called after document is saved (insert or update) - update related records"""
		# Update customer's last order date
		frappe.db.set_value("Customer", self.customer, "last_order_date", self.order_date)
		
		# Sync to external system
		self.sync_to_erp()
		
		# Clear related caches
		frappe.cache.delete_value(f"customer_orders_{self.customer}")
		
		# Trigger workflow
		if self.status_changed():
			self.trigger_approval_workflow()
	
	def on_submit(self):
		"""Called when document is submitted - finalize and lock"""
		# Create warehouse entries
		self.create_warehouse_entries()
		
		# Generate invoice if needed
		if self.create_invoice_on_submit:
			self.create_invoice()
		
		# Send to customer
		self.send_to_customer()
		
		# Update ledger
		self.post_to_general_ledger()
	
	def on_cancel(self):
		"""Called when submitted document is cancelled - reverse operations"""
		# Reverse warehouse entries
		self.reverse_warehouse_entries()
		
		# Cancel related invoices
		self.cancel_related_invoices()
		
		# Reverse ledger entries
		self.reverse_ledger_entries()
		
		# Notify customer
		self.send_cancellation_notice()
	
	def before_trash(self):
		"""Called before document deletion - final checks"""
		# Prevent deletion of submitted documents
		if self.docstatus == 1:
			frappe.throw(_("Cannot delete submitted orders. Cancel instead."))
		
		# Check for linked records
		linked = frappe.get_all("Invoice", filters={"order_id": self.name})
		if linked:
			frappe.throw(_("Cannot delete order with linked invoices"))
	
	def after_delete(self):
		"""Called after document is deleted - cleanup"""
		# Log deletion
		frappe.log("Order deleted: {0}".format(self.name))
		
		# Clear any temporary data
		frappe.cache.delete_value(f"order_temp_{self.name}")
	
	# Helper methods
	def calculate_total(self):
		return sum(item.line_total for item in self.items) if self.items else 0
	
	def calculate_tax(self):
		return self.calculate_total() * (self.tax_rate / 100) if self.tax_rate else 0
	
	def status_changed(self):
		"""Check if status field changed"""
		return self.get_doc_before_save() and self.status != self.get_doc_before_save().status
	
	def get_doc_before_save(self):
		"""Get the document's previous state"""
		return frappe.get_cached_value("Order", self.name, "*")
```

### Background Job Processing Patterns

```python
# Background jobs using Redis Queue (RQ)

# Simple background job
@frappe.whitelist()
def process_order(order_id):
	"""Whitelisted method that can be called from frontend"""
	# Enqueue long-running task
	frappe.enqueue(
		"myapp.orders.tasks.heavy_processing",
		queue="default",  # or "short", "long"
		timeout=300,
		order_id=order_id,
		is_async=True,
		job_id=f"process_{order_id}"  # Unique job ID prevents duplicates
	)
	return {"status": "queued"}

# Task definition
def heavy_processing(order_id):
	"""Background job - runs in worker process"""
	order = frappe.get_doc("Order", order_id)
	
	# Long-running operations
	order.process_items()
	order.calculate_shipping()
	order.update_inventory()
	
	# Update status
	frappe.db.set_value("Order", order_id, "status", "Processing")
	
	# Send notification
	frappe.publish_realtime("order_processed", {"order_id": order_id})

# Job with progress tracking
def long_running_task(job_id, data):
	"""Track progress of long-running job"""
	try:
		total_items = len(data['items'])
		for i, item in enumerate(data['items']):
			process_item(item)
			# Update progress every 10%
			if i % max(1, total_items // 10) == 0:
				frappe.publish_realtime(
					"job_progress",
					{"job_id": job_id, "progress": (i / total_items) * 100}
				)
	except Exception as e:
		frappe.log_error(f"Job {job_id} failed: {str(e)}")
		raise

# Check job status
def get_job_status(job_id):
	"""Check if background job is complete"""
	job = frappe.get_cached_value("Job Queue", job_id)
	return {
		"status": job.status if job else "not_found",  # queued, started, finished, failed
		"exc": job.exc_msg if job and job.status == "failed" else None
	}

# Scheduled background jobs in hooks.py
# scheduler_events = {
# 	"daily": [
# 		"myapp.tasks.daily_cleanup",
# 		"myapp.tasks.send_daily_digest"
# 	],
# 	"hourly": [
# 		"myapp.tasks.sync_external_data"
# 	],
# 	"cron": {
# 		"0 0 * * *": ["myapp.tasks.midnight_task"],  # Daily at midnight
# 		"0 */6 * * *": ["myapp.tasks.six_hourly_task"],  # Every 6 hours
# 	}
# }

def daily_cleanup():
	"""Scheduled task - runs daily at configured time"""
	# Delete old temporary records
	frappe.db.delete("Temp Data", filters={"created": ("<", frappe.utils.add_days(frappe.utils.today(), -30))})
	
	# Archive old logs
	frappe.db.sql("ARCHIVE TABLE log_entries WHERE created < DATE_SUB(NOW(), INTERVAL 90 DAY)")
```

### Email Notification Patterns

```python
# Sending emails from document lifecycle

class Invoice(Document):
	def on_submit(self):
		"""Send invoice to customer on submission"""
		self.send_invoice_email()
	
	def send_invoice_email(self):
		"""Send invoice via email"""
		# Get template with variables
		template = frappe.db.get_value("Email Template", "Invoice Notification", "response_html")
		
		# Prepare email context
		email_context = {
			"customer_name": self.customer_name,
			"invoice_number": self.name,
			"total_amount": self.grand_total,
			"due_date": self.due_date,
			"subject": f"Invoice {self.name}"
		}
		
		# Render template
		message = frappe.render_template(template, email_context)
		
		# Send email with attachment
		frappe.sendmail(
			recipients=[self.customer_email],
			subject=f"Invoice {self.name} for {self.total_amount}",
			message=message,
			attachments=[{
				"fname": f"invoice_{self.name}.pdf",
				"fcontent": self.get_pdf_content()
			}],
			reference_doctype="Invoice",
			reference_name=self.name
		)
		
		# Log email sent
		frappe.log(f"Invoice email sent to {self.customer_email}")

# Queue email sending as background job
def send_bulk_emails(doctype, filters):
	"""Send emails to multiple recipients in background"""
	frappe.enqueue(
		"myapp.email_utils.bulk_email_job",
		queue="long",
		timeout=1800,
		doctype=doctype,
		filters=filters
	)

def bulk_email_job(doctype, filters):
	"""Background job for bulk emails"""
	docs = frappe.get_all(doctype, filters=filters, fields=["name"])
	
	for doc_name in docs:
		doc = frappe.get_doc(doctype, doc_name['name'])
		try:
			doc.send_email()
		except Exception as e:
			frappe.log_error(f"Email failed for {doc_name['name']}: {str(e)}")
```

### Exception Handling & Error Patterns

```python
class DataImport(Document):
	def validate(self):
		"""Error handling and custom exceptions"""
		try:
			# Validation with specific error types
			self.validate_file_format()
			self.validate_required_columns()
			self.validate_data_integrity()
		except frappe.ValidationError as e:
			# Re-throw validation errors
			frappe.throw(str(e))
		except Exception as e:
			# Log unexpected errors
			frappe.log_error(f"Unexpected error: {str(e)}")
			frappe.throw(_("An unexpected error occurred during validation"))
	
	def validate_file_format(self):
		"""Custom validation method"""
		if not self.file_path.endswith(('.csv', '.xlsx')):
			frappe.throw(_("Only CSV and Excel files are supported"))
	
	def validate_required_columns(self):
		"""Check required columns exist"""
		required = ['name', 'email', 'amount']
		existing = self.get_file_columns()
		
		missing = set(required) - set(existing)
		if missing:
			frappe.throw(_("Missing required columns: {0}").format(", ".join(missing)))
	
	def validate_data_integrity(self):
		"""Check data quality"""
		for i, row in enumerate(self.data_rows, 1):
			if not row.get('email') or '@' not in row['email']:
				frappe.throw(_("Row {0}: Invalid email format").format(i))
			
			if row.get('amount') and not self.is_valid_number(row['amount']):
				frappe.throw(_("Row {0}: Amount must be a number").format(i))
```

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

## Advanced API Patterns

### Authentication & Authorization

```python
# API authentication patterns

@frappe.whitelist()
def public_method():
	"""Accessible without authentication"""
	return {"status": "public"}

@frappe.whitelist(allow_guest=False)
def authenticated_method():
	"""Requires logged-in user"""
	return {"user": frappe.session.user}

@frappe.whitelist()
def admin_only_method():
	"""Check roles at runtime"""
	if "Administrator" not in frappe.get_roles():
		frappe.throw(_("Only administrators can access this"))
	return {"status": "admin"}

@frappe.whitelist()
def check_doc_permission(doctype, doc_name):
	"""Verify document-level permissions"""
	if not frappe.has_permission(doctype, "read", doc=doc_name):
		frappe.throw(_("You do not have permission to access this document"))
	
	doc = frappe.get_doc(doctype, doc_name)
	return doc.as_dict()

# Token-based API authentication
def create_api_token(user):
	"""Generate API token for third-party access"""
	token = frappe.generate_hash(length=32)
	frappe.db.set_value("User", user, "api_key", token)
	return token

def verify_api_token(token):
	"""Verify token and return user"""
	user = frappe.db.get_value("User", filters={"api_key": token}, fieldname="name")
	return user

# Use in API request header: Authorization: token {api_key}:{api_secret}
```

### Webhook Implementation

```python
# Webhook patterns - called when documents are created/updated

def trigger_webhook_on_update():
	"""Define in hooks.py under doc_events"""
	# hooks.py: doc_events = {
	#	"Order": {
	#		"on_submit": "myapp.webhooks.order_submitted"
	#	}
	# }

def order_submitted(doc, method):
	"""Executed when Order is submitted"""
	# Send to external system
	response = requests.post(
		"https://external-api.com/orders",
		json={
			"order_id": doc.name,
			"customer": doc.customer,
			"total": doc.grand_total,
			"items": [{"item_code": item.item_code, "qty": item.qty} for item in doc.items]
		},
		headers={"Authorization": f"Bearer {get_api_token()}"},
		timeout=10
	)
	
	# Log webhook call
	if response.status_code == 200:
		frappe.db.set_value("Order", doc.name, "external_order_id", response.json()["id"])
	else:
		frappe.log_error(f"Webhook failed: {response.text}")

# Retry logic for failed webhooks
def retry_failed_webhooks():
	"""Scheduled task to retry failed webhooks"""
	failed = frappe.get_all("Integration Request", 
		filters={"status": "Failed"},
		limit=100
	)
	
	for req in failed:
		integration_req = frappe.get_doc("Integration Request", req.name)
		try:
			response = requests.request(
				method=integration_req.request_method,
				url=integration_req.url,
				data=integration_req.request_body,
				timeout=10
			)
			
			if response.status_code < 400:
				integration_req.status = "Completed"
				integration_req.response_body = response.text
			else:
				integration_req.status = "Failed"
		except Exception as e:
			frappe.log_error(f"Webhook retry failed: {str(e)}")
		
		integration_req.save(ignore_permissions=True)
```

### File Upload & Download APIs

```python
# File handling patterns

@frappe.whitelist()
def upload_document(doctype, docname):
	"""Handle file upload to document"""
	from frappe.utils.file_manager import upload_file
	
	# Get file from request
	file = frappe.request.files.get('file')
	
	# Validate file
	if not file or not file.filename:
		frappe.throw(_("No file uploaded"))
	
	# Check document exists and user has permission
	if not frappe.db.exists(doctype, docname):
		frappe.throw(_(f"{doctype} {docname} not found"))
	
	# Upload file
	try:
		file_doc = upload_file(
			fname=file.filename,
			content=file.read(),
			doctype=doctype,
			docname=docname
		)
		return {"file_url": file_doc.file_url, "file_name": file_doc.file_name}
	except Exception as e:
		frappe.log_error(f"File upload error: {str(e)}")
		frappe.throw(_("File upload failed"))

@frappe.whitelist()
def download_document(file_path):
	"""Secure file download"""
	# Validate file path to prevent directory traversal
	if ".." in file_path or file_path.startswith("/"):
		frappe.throw(_("Invalid file path"))
	
	# Check if file exists
	from frappe.utils.file_manager import get_file_path
	try:
		file_path = get_file_path(file_path)
		with open(file_path, "rb") as f:
			return f.read()
	except FileNotFoundError:
		frappe.throw(_("File not found"))

# Bulk file upload
@frappe.whitelist()
def bulk_import_documents(doctype):
	"""Import multiple documents from file"""
	import csv
	
	file = frappe.request.files.get('file')
	if not file:
		frappe.throw(_("No file provided"))
	
	# Parse CSV
	stream = file.read().decode('utf-8').splitlines()
	reader = csv.DictReader(stream)
	
	created_docs = []
	errors = []
	
	for i, row in enumerate(reader, 1):
		try:
			doc = frappe.get_doc({
				"doctype": doctype,
				**row  # Unpack row data as fields
			})
			doc.insert()
			created_docs.append(doc.name)
		except Exception as e:
			errors.append({"row": i, "error": str(e)})
	
	return {
		"created": len(created_docs),
		"failed": len(errors),
		"docs": created_docs,
		"errors": errors
	}
```

### Data Import Patterns

```python
# Data import/sync from external systems

@frappe.whitelist()
def sync_customers_from_external_api():
	"""Sync customer data from external API"""
	import requests
	
	external_api_url = frappe.db.get_single_value("Settings", "external_api_url")
	api_key = frappe.db.get_single_value("Settings", "api_key")
	
	try:
		# Fetch data from external API
		response = requests.get(
			f"{external_api_url}/customers",
			headers={"Authorization": f"Bearer {api_key}"},
			timeout=30
		)
		response.raise_for_status()
		
		customers = response.json()
		created = 0
		updated = 0
		
		for customer_data in customers:
			# Check if customer exists
			existing = frappe.db.exists("Customer", {"external_id": customer_data["id"]})
			
			if existing:
				# Update existing customer
				doc = frappe.get_doc("Customer", existing)
				doc.customer_name = customer_data["name"]
				doc.phone = customer_data.get("phone")
				doc.email_id = customer_data.get("email")
				doc.save()
				updated += 1
			else:
				# Create new customer
				doc = frappe.get_doc({
					"doctype": "Customer",
					"customer_name": customer_data["name"],
					"customer_type": "Individual",
					"external_id": customer_data["id"],
					"phone": customer_data.get("phone"),
					"email_id": customer_data.get("email")
				})
				doc.insert()
				created += 1
		
		frappe.msgprint(f"Sync completed: {created} created, {updated} updated")
		return {"created": created, "updated": updated}
		
	except requests.RequestException as e:
		frappe.log_error(f"Sync failed: {str(e)}")
		frappe.throw(_("Failed to sync data from external API"))

# Incremental sync using timestamps
def sync_incremental_updates():
	"""Sync only changed records since last sync"""
	last_sync = frappe.db.get_single_value("Settings", "last_customer_sync")
	
	external_api_url = frappe.db.get_single_value("Settings", "external_api_url")
	
	response = requests.get(
		f"{external_api_url}/customers/changed",
		params={"since": last_sync},
		timeout=30
	)
	
	for customer_data in response.json():
		# Process only changed records
		doc = frappe.get_doc("Customer", {"external_id": customer_data["id"]})
		doc.update(customer_data)
		doc.save()
	
	# Update last sync time
	frappe.db.set_single_value("Settings", "last_customer_sync", frappe.utils.now())
```

### Custom API Endpoints

```python
# Create custom API routes (alternative to whitelisted methods)

# In app's __init__.py or api.py
from frappe import api

@api.validate_auth()
def api_get_orders(filters=None):
	"""GET /api/method/myapp.api.get_orders"""
	return frappe.get_all("Order", filters=filters or {})

@api.validate_auth()
def api_create_order(customer, items):
	"""POST /api/method/myapp.api.create_order"""
	order = frappe.get_doc({
		"doctype": "Order",
		"customer": customer,
		"items": [{"item_code": item["code"], "qty": item["qty"]} for item in items]
	})
	order.insert()
	return order.as_dict()

# RESTful resource endpoints
@frappe.whitelist(methods=["GET"])
def get_order(order_id):
	"""GET /api/resource/Order/{order_id}"""
	return frappe.get_doc("Order", order_id).as_dict()

@frappe.whitelist(methods=["PUT"])
def update_order(order_id, **kwargs):
	"""PUT /api/resource/Order/{order_id}"""
	order = frappe.get_doc("Order", order_id)
	order.update(kwargs)
	order.save()
	return order.as_dict()

@frappe.whitelist(methods=["DELETE"])
def delete_order(order_id):
	"""DELETE /api/resource/Order/{order_id}"""
	frappe.delete_doc("Order", order_id)
	return {"status": "deleted"}
```

### API Error Handling & Responses

```python
# Standardized error handling

@frappe.whitelist()
def safe_api_operation(param1, param2):
	"""API with comprehensive error handling"""
	try:
		# Validate inputs
		if not param1 or not param2:
			frappe.throw(_("Both parameters are required"))
		
		# Business logic
		result = process_operation(param1, param2)
		
		# Return standardized response
		return {
			"status": "success",
			"data": result,
			"message": _("Operation completed successfully")
		}
		
	except frappe.ValidationError as e:
		# Validation errors (user input issues)
		return {
			"status": "error",
			"type": "validation",
			"message": str(e),
			"code": 400
		}
	except frappe.PermissionError as e:
		# Permission errors
		return {
			"status": "error",
			"type": "permission",
			"message": _("You do not have permission for this operation"),
			"code": 403
		}
	except Exception as e:
		# Unexpected errors
		frappe.log_error(f"Unexpected error: {str(e)}")
		return {
			"status": "error",
			"type": "internal",
			"message": _("An unexpected error occurred"),
			"code": 500
		}

# Custom exception classes
class CustomValidationError(frappe.ValidationError):
	"""Custom validation error for specific business logic"""
	pass

class APIQuotaExceeded(Exception):
	"""API rate limiting"""
	pass
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

## Client-Side Development Patterns

### Form Event Scripts - Complete Patterns

Form scripts are JavaScript files that customize DocType behavior on the client side. They are loaded automatically when forms are rendered.

```javascript
// frappe/public/js/form_scripts.js - Complete example

// File: apps/myapp/myapp/public/js/myapp_form.js
// Auto-loaded for "MyDocType" form

frappe.ui.form.on("MyDocType", {
	// Document-level events
	onload: function(frm) {
		// Called when form is first loaded
		frm.set_intro("Welcome! Complete all required fields.");
		
		// Set up dynamic form state
		frm.page.add_menu_item(__("Export"), function() {
			frm.call({
				method: "export_document",
				args: {name: frm.doc.name},
				callback: function(r) {
					frappe.msgprint("Exported successfully");
				}
			});
		});
	},
	
	refresh: function(frm) {
		// Called every time form is redrawn (save, field change, etc.)
		// Set field properties dynamically
		frm.set_df_property("sensitive_field", "read_only", 1);
		
		// Show/hide sections based on conditions
		frm.set_df_property("pricing_section", "hidden", frm.doc.customer_type !== "Wholesale");
		
		// Update button visibility
		if (frm.doc.docstatus === 0) {
			// Draft - show draft actions
			frm.add_custom_button(__("Process"), function() {
				frm.call({
					method: "process",
					args: {doctype: frm.doctype, name: frm.doc.name},
					callback: function(r) {
						frm.reload_doc();
					}
				});
			}, __("Actions"));
		} else if (frm.doc.docstatus === 1) {
			// Submitted - show submit actions
			frm.add_custom_button(__("Amend"), function() {
				frm.amend_doc();
			}, __("Actions"));
		}
		
		// Apply conditional CSS classes
		frm.wrapper.classList.toggle("high-priority", frm.doc.priority === "High");
	},
	
	validate: function(frm) {
		// Client-side validation before save
		if (frm.doc.end_date < frm.doc.start_date) {
			frappe.throw(__("End date must be after start date"));
		}
		
		// Validate child table
		if (!frm.doc.items || frm.doc.items.length === 0) {
			frappe.throw(__("At least one item is required"));
		}
		
		// Check for unsaved changes in child tables
		let unsaved = frm.doc.items.filter(d => d.__islocal);
		if (unsaved.length > 0) {
			frappe.msgprint(__("Please save all items before submitting"));
			throw new Error("Unsaved items");
		}
	},
	
	before_save: function(frm) {
		// Preparation before document is saved
		// Trim whitespace from fields
		frm.doc.name_field = frm.doc.name_field.trim();
		
		// Calculate dependent fields
		frm.doc.total = frm.doc.items.reduce((sum, item) => sum + item.amount, 0);
		
		// Set timestamps
		if (!frm.doc.last_modified) {
			frm.doc.last_modified = frappe.datetime.now_datetime();
		}
	},
	
	after_save: function(frm) {
		// Called after successful save
		frappe.msgprint(__("Document saved successfully"));
		
		// Refresh related list views
		frappe.listview_settings['MyDocType'].refresh();
		
		// Update local cache
		frappe.cache.set_value(`doc_${frm.doctype}_${frm.doc.name}`, frm.doc);
	},
	
	// Field-level events
	status: function(frm) {
		// Called when "status" field changes
		if (frm.doc.status === "Approved") {
			frm.set_value("approved_date", frappe.datetime.now_date());
			frm.set_df_property("approval_notes", "read_only", 1);
		} else if (frm.doc.status === "Draft") {
			frm.set_value("approved_date", "");
			frm.set_df_property("approval_notes", "read_only", 0);
		}
	},
	
	customer: function(frm) {
		// When customer field changes, fetch customer details
		if (frm.doc.customer) {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Customer",
					filters: {name: frm.doc.customer},
					fieldname: ["customer_name", "credit_limit", "default_currency"]
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value("customer_name", r.message.customer_name);
						frm.set_value("credit_limit", r.message.credit_limit);
					}
				}
			});
		}
	},
	
	// Child table events
	items_add: function(frm, cdt, cdn) {
		// When a new row is added to items table
		let row = frappe.get_model(cdt, cdn);
		row.quantity = 1;
		row.rate = 0;
	},
	
	items_remove: function(frm, cdt, cdn) {
		// When a row is deleted from items table
		// Recalculate totals
		frm.doc.total = frm.doc.items.reduce((sum, item) => sum + (item.quantity * item.rate), 0);
		frm.refresh_field("total");
	},
	
	items_quantity: function(frm, cdt, cdn) {
		// When quantity field in items table changes
		let row = frappe.get_model(cdt, cdn);
		row.line_total = row.quantity * row.rate;
		
		// Refresh just this field
		frappe.model.set_value(cdt, cdn, "line_total", row.line_total);
		
		// Recalculate parent total
		frm.doc.total = frm.doc.items.reduce((sum, item) => sum + (item.line_total || 0), 0);
		frm.refresh_field("total");
	},
	
	// Grid/Table-level events
	items: function(frm) {
		// When entire items table changes
		frm.refresh_field("items");
	}
});

// Conditional field visibility
frappe.ui.form.on("MyDocType", {
	customer_type: function(frm) {
		// Show/hide fields based on customer type
		let is_b2b = frm.doc.customer_type === "B2B";
		
		frm.set_df_property("company_name", "hidden", !is_b2b);
		frm.set_df_property("tax_id", "hidden", !is_b2b);
		frm.set_df_property("invoice_type", "hidden", !is_b2b);
		
		// Update field labels
		frm.set_df_property("address", "label", is_b2b ? __("Company Address") : __("Home Address"));
	}
});
```

### List View & Report Customization

```javascript
// List view customization - loaded automatically for MyDocType

frappe.listview_settings['MyDocType'] = {
	// Add custom columns
	add_fields: ["customer_name", "status", "total_amount"],
	
	// Custom column rendering
	formatters: {
		status: function(value, df, options) {
			// Render status with color coding
			let color = {
				"Draft": "gray",
				"Submitted": "blue",
				"Completed": "green",
				"Cancelled": "red"
			}[value];
			
			return `<span class="indicator ${color}">${value}</span>`;
		},
		total_amount: function(value, df, options) {
			// Render amount with currency formatting
			return frappe.format(value, {fieldtype: "Currency"});
		}
	},
	
	// Custom filters
	filters: [
		["docstatus", "=", 1],  // Only submitted
		["status", "!=", "Cancelled"]
	],
	
	// Custom button on list
	onload: function(listview) {
		listview.page.add_menu_item(__("Bulk Export"), function() {
			let selected = listview.get_checked_items();
			if (selected.length === 0) {
				frappe.msgprint(__("Please select items to export"));
				return;
			}
			
			frappe.call({
				method: "myapp.api.bulk_export",
				args: {names: selected.map(d => d.name)},
				callback: function(r) {
					frappe.msgprint(__("Export completed"));
				}
			});
		});
	},
	
	// Custom action on checkbox
	refresh: function(listview) {
		// Add custom button to toolbar
		listview.page.add_action_item(__("Process Selected"), function() {
			let selected = listview.get_checked_items();
			frappe.call({
				method: "myapp.api.process_bulk",
				args: {names: selected.map(d => d.name)},
				callback: function(r) {
					listview.refresh();
				}
			});
		});
	}
};

// Report customization
frappe.listview_settings['Report'] = {
	onload: function(report) {
		// Add custom report actions
		report.page.add_menu_item(__("Email Report"), function() {
			new frappe.ui.Dialog({
				title: __("Email Report"),
				fields: [
					{fieldtype: "Data", fieldname: "recipients", label: __("Recipients"), reqd: 1},
					{fieldtype: "Text", fieldname: "message", label: __("Message")}
				],
				primary_action_label: __("Send"),
				primary_action(values) {
					frappe.call({
						method: "myapp.api.email_report",
						args: {
							report_name: report.report_name,
							filters: report.filter_area.get(),
							recipients: values.recipients.split(","),
							message: values.message
						},
						callback: function(r) {
							frappe.msgprint(__("Report sent"));
						}
					});
					this.hide();
				}
			}).show();
		});
	}
};
```

### Advanced Client-Server Communication

```javascript
// frappe.call patterns for client-server interaction

// 1. Simple method call with async/await
async function fetch_customer_details(customer_id) {
	try {
		const result = await frappe.db.get_value("Customer", customer_id, 
			["customer_name", "credit_limit", "payment_terms"]
		);
		return result.message;
	} catch (error) {
		frappe.msgprint(__("Error fetching customer details"));
		console.error(error);
	}
}

// 2. Batch operations
async function bulk_update_status(doc_ids, new_status) {
	const promises = doc_ids.map(id => 
		frappe.call({
			method: "frappe.client.set_value",
			args: {
				doctype: "MyDocType",
				name: id,
				fieldname: {status: new_status}
			}
		})
	);
	
	return Promise.all(promises);
}

// 3. With progress tracking
function process_with_progress(items, process_fn) {
	let processed = 0;
	const total = items.length;
	
	const progressDialog = new frappe.ui.Dialog({
		title: __("Processing..."),
		static: true,
		fields: [
			{
				fieldtype: "HTML",
				fieldname: "progress_html",
				html: `<div class="progress"><div class="progress-bar" style="width: 0%"></div></div>
				       <p id="progress-text">0/${total}</p>`
			}
		]
	});
	progressDialog.show();
	
	items.forEach(item => {
		process_fn(item).then(() => {
			processed++;
			const percent = (processed / total) * 100;
			progressDialog.$wrapper.find(".progress-bar").css("width", percent + "%");
			progressDialog.$wrapper.find("#progress-text").text(`${processed}/${total}`);
			
			if (processed === total) {
				progressDialog.hide();
				frappe.msgprint(__("Processing complete"));
			}
		});
	});
}

// 4. Real-time updates via Socket.IO
frappe.realtime.on("document_updated", function(data) {
	if (data.doctype === cur_frm.doctype && data.name === cur_frm.doc.name) {
		// Refresh current form if it's the updated document
		cur_frm.reload_doc();
	}
});

// Publish event from backend
frappe.call({
	method: "myapp.api.trigger_update",
	args: {doctype: "MyDocType", name: "doc-name"},
	callback: function(r) {
		// Backend will publish via frappe.publish_realtime()
	}
});
```

### Custom Dialogs & UI Components

```javascript
// Custom dialog patterns

function show_custom_dialog() {
	// Create reusable dialog
	const dialog = new frappe.ui.Dialog({
		title: __("Create Invoice"),
		fields: [
			{
				fieldtype: "Link",
				fieldname: "customer",
				label: __("Customer"),
				options: "Customer",
				reqd: 1
			},
			{
				fieldtype: "Date",
				fieldname: "invoice_date",
				label: __("Invoice Date"),
				default: frappe.datetime.now_date()
			},
			{
				fieldtype: "Currency",
				fieldname: "amount",
				label: __("Amount"),
				reqd: 1
			},
			{
				fieldtype: "Select",
				fieldname: "status",
				label: __("Status"),
				options: "\nDraft\nSubmitted\nPaid",
				default: "Draft"
			}
		],
		primary_action_label: __("Create"),
		primary_action(values) {
			// Handle form submission
			frappe.call({
				method: "myapp.api.create_invoice",
				args: values,
				callback: function(r) {
					frappe.msgprint(__("Invoice created"));
					dialog.hide();
					
					// Refresh current list or form
					if (cur_list) {
						cur_list.refresh();
					}
				}
			});
		},
		secondary_action_label: __("Cancel"),
		secondary_action() {
			dialog.hide();
		}
	});
	
	// Add computed field logic
	dialog.fields_dict.customer.df.onchange = function() {
		// When customer changes, fetch default values
		let customer = dialog.get_value("customer");
		frappe.db.get_value("Customer", customer, "default_currency", function(r) {
			if (r.message) {
				dialog.set_value("currency", r.message.default_currency);
			}
		});
	};
	
	dialog.show();
}

// Quick entry (inline creation)
frappe.ui.form.on("ParentDocType", {
	items_add: function(frm, cdt, cdn) {
		// When new row added, open quick entry for child table
		let row = frappe.get_model(cdt, cdn);
		
		frappe.quick_entry.open("Item", {
			doctype: "Item",
			after_insert(item_doc) {
				row.item_code = item_doc.name;
				frm.refresh_field("items");
			}
		});
	}
});
```

## Database Operations & Optimization

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

### Advanced Query Patterns

```python
# Query builder with complex conditions

from frappe.query_builder import DocType, Field

def complex_order_query():
	"""Advanced query with joins and aggregations"""
	Order = DocType("Order")
	Item = DocType("Order Item")
	Customer = DocType("Customer")
	
	# Complex query with joins
	query = (
		frappe.qb.from_(Order)
		.join(Customer).on(Order.customer == Customer.name)
		.select(
			Order.name,
			Order.customer,
			Customer.customer_name,
			Field("COUNT(*)").as_("item_count"),
			Field("SUM(amount)").as_("total_amount")
		)
		.where((Order.docstatus == 1) & (Order.order_date >= "2026-01-01"))
		.groupby(Order.name, Order.customer)
		.having(Field("SUM(amount)") > 1000)
		.orderby(Field("SUM(amount)"), order="DESC")
		.limit(20)
	)
	
	return query.run(as_dict=True)

def batch_query_processing():
	"""Process large datasets in batches to avoid memory issues"""
	batch_size = 1000
	start = 0
	
	while True:
		orders = frappe.get_all("Order",
			filters={"docstatus": 1},
			fields=["name", "customer", "total"],
			start=start,
			page_length=batch_size
		)
		
		if not orders:
			break
		
		# Process batch
		for order in orders:
			process_order(order)
			frappe.db.commit()  # Commit after processing
		
		start += batch_size

def get_related_documents(doctype, name):
	"""Efficiently get all related documents"""
	# Get document with all child tables
	doc = frappe.get_doc(doctype, name)
	
	# Get linked documents
	links = frappe.get_all(doctype, 
		filters={"parent_document": name},
		fields=["name", "docstatus"]
	)
	
	# Get comments and activity
	comments = frappe.get_all("Comment",
		filters={"doc_type": doctype, "doc_name": name},
		order_by="creation desc"
	)
	
	return {
		"document": doc,
		"links": links,
		"comments": comments
	}
```

### Transaction Management

```python
# Database transactions and rollback handling

def atomic_operation():
	"""Atomically create multiple related documents"""
	try:
		with frappe.db.transaction():
			# Create order
			order = frappe.get_doc({
				"doctype": "Order",
				"customer": "CUST-001",
				"order_date": frappe.utils.today()
			})
			order.insert()
			
			# Create related invoice
			invoice = frappe.get_doc({
				"doctype": "Invoice",
				"order_id": order.name,
				"customer": order.customer
			})
			invoice.insert()
			
			# Update customer ledger
			frappe.db.set_value("Customer", order.customer, "last_order_id", order.name)
			
			# If all succeeds, commit automatically
	except Exception as e:
		# On error, entire transaction rolls back
		frappe.log_error(f"Transaction failed: {str(e)}")
		raise

def savepoint_example():
	"""Use savepoints for partial rollback"""
	try:
		with frappe.db.transaction():
			order = frappe.get_doc({"doctype": "Order", "customer": "CUST-001"})
			order.insert()
			
			# Create savepoint
			frappe.db.savepoint("before_items")
			
			try:
				# Add items (might fail)
				for item_data in items_list:
					item = frappe.get_doc({
						"doctype": "Order Item",
						"order": order.name,
						**item_data
					})
					item.insert()
			except Exception as e:
				# Rollback to savepoint, but keep order
				frappe.db.rollback_to_savepoint("before_items")
				frappe.log_error(f"Item insertion failed: {str(e)}")
	except Exception as e:
		frappe.log_error(f"Order creation failed: {str(e)}")
		raise
```

### Query Optimization

```python
# Common optimization patterns

def avoid_n_plus_one():
	"""WRONG: N+1 query problem"""
	orders = frappe.get_all("Order", filters={"docstatus": 1}, fields=["name"])
	
	for order in orders:
		# This runs a query for EACH order - N+1 problem!
		doc = frappe.get_doc("Order", order.name)
		customer = frappe.db.get_value("Customer", doc.customer, "customer_name")
		print(f"{order.name}: {customer}")

def optimize_with_single_query():
	"""CORRECT: Fetch all data in single query"""
	orders = frappe.get_all("Order",
		filters={"docstatus": 1},
		fields=["name", "customer"],  # Include related field
		# Use 'with' to fetch linked document details
	)
	
	for order in orders:
		# Customer name is already in order
		print(f"{order.name}: {order.customer}")

def use_cached_get():
	"""Use cached retrieval for frequently accessed documents"""
	# First access - fetches from DB
	customer = frappe.get_cached_doc("Customer", "CUST-001")
	
	# Second access - returns from cache
	customer_again = frappe.get_cached_doc("Customer", "CUST-001")
	
	# Clear cache if needed
	frappe.cache.clear()

def batch_fetch_optimization():
	"""Fetch multiple documents efficiently"""
	order_ids = ["ORD-001", "ORD-002", "ORD-003"]
	
	# WRONG: Multiple individual fetches
	# orders = [frappe.get_doc("Order", name) for name in order_ids]
	
	# CORRECT: Single query with filter
	orders = frappe.get_all("Order",
		filters={"name": ["in", order_ids]},
		fields=["*"]
	)
```

### Index Management

```python
# Create and manage database indexes

def create_custom_index():
	"""Create custom index for frequent queries"""
	# Check if index exists
	frappe.db.add_index("Order", ["customer", "order_date"])
	
	# Now queries filtering on customer+date are fast
	fast_orders = frappe.get_all("Order",
		filters={"customer": "CUST-001", "order_date": "2026-02-19"}
	)

def list_indexes():
	"""View all indexes on a table"""
	indexes = frappe.db.sql("""
		SELECT INDEX_NAME, COLUMN_NAME 
		FROM INFORMATION_SCHEMA.STATISTICS 
		WHERE TABLE_NAME = %s
	""", ("tabOrder",), as_dict=True)
	
	return indexes

def analyze_slow_queries():
	"""Enable query logging to identify slow queries"""
	# In site_config.json or during development:
	# frappe.db.print_sql(True)
	
	# Or use MySQL slow query log
	# Enable in MariaDB: long_query_time = 2, log_slow_queries
	
	# Analyze execution
	frappe.db.sql("EXPLAIN SELECT * FROM `tabOrder` WHERE customer = %s", ("CUST-001",))
```

### Schema Migrations

```python
# Alter table structure

def add_custom_field_migration():
	"""Add new field to DocType (migration)"""
	# Usually done through UI, but programmatic way:
	
	frappe.get_doc({
		"doctype": "Custom Field",
		"dt": "Order",
		"fieldname": "new_field",
		"fieldtype": "Data",
		"label": "New Field",
		"insert_after": "existing_field"
	}).insert()
	
	# Migrate database
	frappe.db.commit()

def rename_field_migration():
	"""Rename database column"""
	# Use migrations instead of direct SQL
	frappe.db.sql("""
		ALTER TABLE `tabOrder` 
		CHANGE `old_fieldname` `new_fieldname` VARCHAR(255)
	""")
	
	# Update DocType definition
	frappe.db.sql("""
		UPDATE `tabDocField` 
		SET `fieldname` = 'new_fieldname' 
		WHERE `parent` = 'Order' AND `fieldname` = 'old_fieldname'
	""")

def create_index_migration():
	"""Create database index for performance"""
	frappe.db.sql("""
		ALTER TABLE `tabOrder` 
		ADD INDEX `idx_customer_date` (`customer`, `order_date`)
	""")

def migration_example():
	"""Complete migration example"""
	# File: frappe-bench/apps/myapp/myapp/migrations/add_status_field.py
	
	def execute():
		frappe.get_doc({
			"doctype": "Custom Field",
			"dt": "Order",
			"fieldname": "process_status",
			"fieldtype": "Select",
			"label": "Process Status",
			"options": "\nPending\nProcessing\nCompleted\nFailed",
			"default": "Pending"
		}).insert()
		
		frappe.db.commit()
```

### Data Integrity

```python
# Maintain data consistency

def check_referential_integrity():
	"""Verify foreign key relationships are valid"""
	# Check for orphaned records
	orphaned_orders = frappe.db.sql("""
		SELECT o.name FROM `tabOrder` o
		LEFT JOIN `tabCustomer` c ON o.customer = c.name
		WHERE c.name IS NULL AND o.customer IS NOT NULL
	""", as_dict=True)
	
	if orphaned_orders:
		frappe.msgprint(f"Found {len(orphaned_orders)} orphaned orders")
		for order in orphaned_orders:
			frappe.log_error(f"Orphaned order: {order.name}")

def fix_data_consistency():
	"""Fix data integrity issues"""
	# Example: Recalculate totals
	orders = frappe.get_all("Order", filters={"docstatus": 1})
	
	for order_name in orders:
		order = frappe.get_doc("Order", order_name)
		
		# Recalculate
		order.grand_total = sum(item.amount for item in order.items)
		order.save(ignore_permissions=True)

def validate_data_before_import():
	"""Validate data before inserting"""
	def import_customers(csv_file):
		import csv
		
		with open(csv_file) as f:
			reader = csv.DictReader(f)
			
			for row in reader:
				# Validate required fields
				if not row.get("customer_name"):
					frappe.throw(_("customer_name is required"))
				
				# Validate data types
				if not is_valid_email(row.get("email")):
					frappe.throw(_("Invalid email format"))
				
				# Check uniqueness
				if frappe.db.exists("Customer", row["customer_name"]):
					frappe.throw(_("Duplicate customer"))
				
				# Create document
				customer = frappe.get_doc({
					"doctype": "Customer",
					**row
				})
				customer.insert()
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

## Testing & Quality Assurance

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

## Advanced Testing Frameworks

### Comprehensive Unit Test Patterns

```python
# Complete testing patterns with fixtures and mocking

import frappe
from frappe.tests import IntegrationTestCase, FrappeTestCase
from unittest.mock import patch, MagicMock
import json

class TestOrderWorkflow(IntegrationTestCase):
	"""Test complete order lifecycle"""
	
	@classmethod
	def setUpClass(cls):
		"""Setup test data once for all tests"""
		# Create test customer
		if not frappe.db.exists("Customer", "TEST-CUSTOMER"):
			frappe.get_doc({
				"doctype": "Customer",
				"name": "TEST-CUSTOMER",
				"customer_name": "Test Customer",
				"customer_type": "Individual"
			}).insert()
		
		# Create test items
		for i in range(1, 4):
			if not frappe.db.exists("Item", f"TEST-ITEM-{i}"):
				frappe.get_doc({
					"doctype": "Item",
					"name": f"TEST-ITEM-{i}",
					"item_name": f"Test Item {i}",
					"item_group": "All Item Groups",
					"stock_uom": "Nos"
				}).insert()
	
	def setUp(self):
		"""Setup before each test"""
		# Create fresh order for each test
		self.order = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUSTOMER",
			"order_date": frappe.utils.today()
		})
		
		# Add order items
		for i in range(1, 3):
			self.order.append("items", {
				"item_code": f"TEST-ITEM-{i}",
				"qty": 5,
				"rate": 100
			})
	
	def test_order_creation(self):
		"""Test order can be created"""
		self.order.insert()
		self.assertTrue(frappe.db.exists("Order", self.order.name))
	
	def test_order_validation(self):
		"""Test order validation rules"""
		self.order.items = []  # Empty items
		
		with self.assertRaises(frappe.ValidationError):
			self.order.insert()
	
	def test_order_total_calculation(self):
		"""Test order total is calculated correctly"""
		self.order.insert()
		
		expected_total = sum(item.qty * item.rate for item in self.order.items)
		self.assertEqual(self.order.grand_total, expected_total)
	
	def test_order_submission(self):
		"""Test order submission workflow"""
		self.order.insert()
		self.order.submit()
		
		self.assertEqual(self.order.docstatus, 1)
		
		# Verify submitted record cannot be modified
		with self.assertRaises(frappe.ValidationError):
			self.order.order_date = frappe.utils.today()
			self.order.save()
	
	def test_order_cancellation(self):
		"""Test order cancellation"""
		self.order.insert()
		self.order.submit()
		self.order.cancel()
		
		self.assertEqual(self.order.docstatus, 2)
	
	def test_permission_checks(self):
		"""Test permission-based operations"""
		self.order.insert()
		
		# Check if current user has permission
		has_access = frappe.has_permission("Order", "write", doc=self.order.name)
		self.assertTrue(has_access)
	
	def test_with_mock_external_api(self):
		"""Test with mocked external API calls"""
		with patch("myapp.external_api.fetch_shipping_cost") as mock_api:
			mock_api.return_value = 50.0
			
			self.order.insert()
			shipping_cost = self.order.calculate_shipping()
			
			self.assertEqual(shipping_cost, 50.0)
			mock_api.assert_called_once()
	
	def test_child_table_operations(self):
		"""Test child table manipulation"""
		self.order.insert()
		
		# Add new item
		self.order.append("items", {
			"item_code": "TEST-ITEM-3",
			"qty": 10,
			"rate": 200
		})
		self.order.save()
		
		# Verify item was added
		self.assertEqual(len(self.order.items), 3)
		
		# Remove item
		self.order.items.pop()
		self.order.save()
		
		self.assertEqual(len(self.order.items), 2)
	
	def tearDown(self):
		"""Cleanup after each test"""
		if self.order.name and frappe.db.exists("Order", self.order.name):
			frappe.delete_doc("Order", self.order.name, force=True)
```

### Test Fixtures & Test Data

```python
# Test data management

class TestWithFixtures(IntegrationTestCase):
	"""Test using fixture data"""
	
	fixtures = ["Customer", "Item", "Order"]  # Auto-loaded from fixtures/
	
	def test_with_fixture_data(self):
		"""Test using pre-created fixture data"""
		# Fixtures are auto-loaded in setUpClass
		customer = frappe.get_doc("Customer", "TEST-CUSTOMER")
		self.assertEqual(customer.customer_type, "Individual")

# Create test data factory
class TestDataFactory:
	"""Factory for creating test documents"""
	
	@staticmethod
	def create_customer(name=None, **kwargs):
		"""Create test customer"""
		doc = frappe.get_doc({
			"doctype": "Customer",
			"name": name or frappe.utils.generate_hash(),
			"customer_name": kwargs.get("customer_name", "Test Customer"),
			"customer_type": kwargs.get("customer_type", "Individual"),
			**kwargs
		})
		doc.insert()
		return doc
	
	@staticmethod
	def create_order(customer=None, items=None):
		"""Create test order with items"""
		doc = frappe.get_doc({
			"doctype": "Order",
			"customer": customer or "TEST-CUSTOMER",
			"order_date": frappe.utils.today()
		})
		
		for item_data in items or []:
			doc.append("items", item_data)
		
		doc.insert()
		return doc

class TestWithFactory(IntegrationTestCase):
	"""Use test factory"""
	
	def setUp(self):
		"""Create test data using factory"""
		self.customer = TestDataFactory.create_customer()
		self.order = TestDataFactory.create_order(
			customer=self.customer.name,
			items=[
				{"item_code": "TEST-ITEM-1", "qty": 5, "rate": 100},
				{"item_code": "TEST-ITEM-2", "qty": 3, "rate": 150}
			]
		)
	
	def tearDown(self):
		"""Cleanup"""
		frappe.delete_doc("Order", self.order.name, force=True)
		frappe.delete_doc("Customer", self.customer.name, force=True)
```

### Permission & Security Testing

```python
# Test permission and security features

class TestPermissions(IntegrationTestCase):
	"""Test permission system"""
	
	def setUp(self):
		"""Create test users with different roles"""
		# Admin user
		if not frappe.db.exists("User", "admin@test.com"):
			frappe.get_doc({
				"doctype": "User",
				"email": "admin@test.com",
				"first_name": "Admin",
				"roles": [{"role": "Administrator"}]
			}).insert()
		
		# Sales user
		if not frappe.db.exists("User", "sales@test.com"):
			frappe.get_doc({
				"doctype": "User",
				"email": "sales@test.com",
				"first_name": "Sales",
				"roles": [{"role": "Sales User"}]
			}).insert()
	
	def test_admin_permission(self):
		"""Test admin has full permission"""
		self.assertTrue(frappe.has_permission("Order", "write", user="admin@test.com"))
	
	def test_role_based_access(self):
		"""Test role-based access control"""
		# Create document
		order = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUSTOMER"
		})
		order.insert()
		
		# Sales user should have permission
		has_perm = frappe.has_permission("Order", "read", doc=order.name, user="sales@test.com")
		self.assertTrue(has_perm or not has_perm)  # Depends on DocType permissions
	
	def test_document_sharing(self):
		"""Test document-level sharing"""
		order = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUSTOMER"
		})
		order.insert()
		
		# Share with specific user
		frappe.share.add("Order", order.name, "sales@test.com", "read")
		
		# Verify sharing
		shared = frappe.db.get_all("Document Share", 
			filters={"doc_type": "Order", "doc_name": order.name}
		)
		self.assertTrue(len(shared) > 0)

class TestSQLInjection(IntegrationTestCase):
	"""Test SQL injection prevention"""
	
	def test_safe_query_with_escape(self):
		"""Test parameterized queries"""
		# This should not throw error but safely handle input
		result = frappe.db.sql(
			"SELECT name FROM `tabOrder` WHERE customer = %s",
			("O'Reilly'; DROP TABLE Orders; --",)
		)
		self.assertIsInstance(result, list)
	
	def test_orm_prevents_injection(self):
		"""Test ORM prevents injection"""
		# ORM handles escaping automatically
		orders = frappe.get_all("Order", 
			filters={"customer": "O'Reilly'; DROP TABLE Orders; --"}
		)
		self.assertIsInstance(orders, list)
```

### API & Integration Testing

```python
# Test API endpoints and integrations

class TestAPIEndpoints(IntegrationTestCase):
	"""Test whitelisted API methods"""
	
	def test_api_method_call(self):
		"""Test calling whitelisted method"""
		result = frappe.call(
			"myapp.api.get_orders",
			kwargs={"customer": "TEST-CUSTOMER"}
		)
		self.assertIsInstance(result.message, list)
	
	def test_api_with_permissions(self):
		"""Test API respects permissions"""
		with self.assertRaises(frappe.PermissionError):
			frappe.call(
				"myapp.api.delete_order",
				kwargs={"order_id": "ORDER-001"}
			)
	
	def test_webhook_call(self):
		"""Test webhook execution"""
		order = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUSTOMER"
		})
		order.insert()
		
		with patch("myapp.webhooks.send_to_external_api") as mock_webhook:
			mock_webhook.return_value = {"status": "success"}
			
			order.submit()
			
			# Verify webhook was called
			mock_webhook.assert_called()
	
	def test_file_upload(self):
		"""Test file upload functionality"""
		from io import BytesIO
		
		# Mock file upload
		file_content = b"test file content"
		
		# This would typically be called from frontend
		# Simulating it here
		result = frappe.call(
			"myapp.api.upload_document",
			kwargs={"doctype": "Order", "docname": "ORDER-001"},
			files={"file": ("test.txt", BytesIO(file_content))}
		)
		
		self.assertIn("file_url", result.message or {})
```

### Database & Query Testing

```python
# Test database operations

class TestDatabaseOperations(IntegrationTestCase):
	"""Test database queries and optimization"""
	
	def test_query_performance(self):
		"""Test query doesn't have N+1 problem"""
		# Create multiple orders
		for i in range(10):
			frappe.get_doc({
				"doctype": "Order",
				"customer": "TEST-CUSTOMER"
			}).insert()
		
		# This should use single query, not N+1
		orders = frappe.get_all("Order", 
			fields=["name", "customer", "grand_total"],
			limit=10
		)
		
		self.assertEqual(len(orders), 10)
	
	def test_transaction_rollback(self):
		"""Test transaction rollback on error"""
		try:
			with frappe.db.transaction():
				order = frappe.get_doc({
					"doctype": "Order",
					"customer": "TEST-CUSTOMER"
				})
				order.insert()
				
				# Force error
				raise Exception("Test error")
		except Exception:
			pass
		
		# Order should not be created (rollback)
		# This depends on whether explicit transaction was used
	
	def test_cache_invalidation(self):
		"""Test cache is properly invalidated"""
		# Create and cache document
		doc = frappe.get_doc({
			"doctype": "Order",
			"customer": "TEST-CUSTOMER"
		})
		doc.insert()
		
		# Modify document
		doc.notes = "Modified"
		doc.save()
		
		# Fetch should get updated version, not cached
		reloaded = frappe.get_doc("Order", doc.name)
		self.assertEqual(reloaded.notes, "Modified")
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

## Permissions System & Security

### Role-Based Permissions (RBAC)

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

## Advanced Permissions & Security Implementation

### Document-Level Permissions (DLP)

```python
# Restrict documents based on owner or conditions

# 1. Owner-based access (if_owner condition)
# Set in DocType Permissions UI or programmatically:
# Permission: User role can only read/write their own documents

# 2. User Permissions (restrict by field)
def setup_user_permissions():
	"""Grant user access to specific records"""
	# User can only see orders for specific branches
	frappe.share.add(
		doctype="Order",
		name="ORD-001",
		user="sales@example.com",
		perm_type="read",
		notify=False
	)
	
	# Or use User Permission DocType for bulk assignments
	frappe.get_doc({
		"doctype": "User Permission",
		"user": "sales@example.com",
		"allow": "Branch",
		"for_value": "North Branch"
	}).insert()

# 3. Permission queries (custom SQL conditions)
class Order(Document):
	def get_permission_query_conditions(self, user):
		"""Filter orders visible to user"""
		# Manager sees all orders
		if "Manager" in frappe.get_roles():
			return ""
		
		# Sales person sees only their own orders
		if "Sales User" in frappe.get_roles():
			return f"`tabOrder`.`owner` = {frappe.db.escape(user)}"
		
		# Customer sees their orders
		if "Customer" in frappe.get_roles():
			return f"`tabOrder`.`customer_email` = {frappe.db.escape(user)}"
		
		return "`tabOrder`.`name` = NULL"  # No access

def get_permission_query_conditions(user):
	"""Module-level permission query (hook)"""
	if user == "Administrator":
		return ""
	
	# Restrict to user's region
	user_region = frappe.db.get_value("User", user, "region")
	return f"`tabOrder`.`region` = {frappe.db.escape(user_region)}"

# Set in hooks.py:
# permission_query_conditions = {
#	"Order": "myapp.permissions.get_permission_query_conditions"
# }
```

### Row-Level Security (RLS)

```python
# Control field-level access

def setup_field_permissions():
	"""Hide sensitive fields from certain roles"""
	# Create custom field with permission conditions
	frappe.get_doc({
		"doctype": "Custom Field",
		"dt": "Invoice",
		"fieldname": "profit_margin",
		"fieldtype": "Percent",
		"label": "Profit Margin",
		"read_only": 0,
		"permlevel": 1,  # Only visible to higher permission levels
		"roles": "Accounts Manager"
	}).insert()

class Invoice(Document):
	def get_access_fields(self, user):
		"""Dynamically hide fields based on role"""
		access_fields = ["name", "customer", "date", "total"]
		
		if "Accounts" in frappe.get_roles():
			access_fields.extend(["cost", "profit_margin", "tax"])
		
		if "Administrator" in frappe.get_roles():
			# Full access
			return None
		
		return access_fields
```

### SQL Injection Prevention

```python
# Secure database operations - prevent SQL injection

# WRONG - vulnerable to SQL injection
def get_orders_bad(customer_name):
	"""INSECURE: Don't do this!"""
	return frappe.db.sql(f"SELECT * FROM `tabOrder` WHERE customer = '{customer_name}'")

# CORRECT - parameterized queries
def get_orders_safe(customer_name):
	"""SECURE: Use parameter binding"""
	# Method 1: Using placeholder %s
	return frappe.db.sql(
		"SELECT * FROM `tabOrder` WHERE customer = %s",
		(customer_name,)
	)
	
	# Method 2: Using escape function
	safe_name = frappe.db.escape(customer_name)
	return frappe.db.sql(f"SELECT * FROM `tabOrder` WHERE customer = {safe_name}")
	
	# Method 3: Using ORM (preferred)
	return frappe.get_all("Order", filters={"customer": customer_name})
	
	# Method 4: Using Query Builder
	Order = frappe.qb.DocType("Order")
	return frappe.qb.from_(Order).select("*").where(Order.customer == customer_name).run()

# CORRECT - validate user input
@frappe.whitelist()
def search_documents(doctype, search_term):
	"""Sanitize user input"""
	# Validate doctype
	if not frappe.db.exists("DocType", doctype):
		frappe.throw(_("Invalid DocType"))
	
	# Escape search term
	safe_term = f"%{frappe.db.escape(search_term)}%"
	
	# Query with validation
	return frappe.db.sql(
		f"SELECT name, title FROM `tab{doctype}` WHERE title LIKE {safe_term} LIMIT 10",
		as_dict=True
	)

# CORRECT - use allow_on_submit wisely
class Invoice(Document):
	def validate(self):
		# Don't allow modification of submitted document fields
		if self.docstatus == 1:
			frappe.throw(_("Document is submitted. Cannot modify."))
```

### Authentication & Session Management

```python
# User authentication patterns

def verify_user_credentials(email, password):
	"""Verify login credentials"""
	from frappe.utils import cstr, get_password_hash
	
	user = frappe.db.get_value("User", email, ["name", "password"])
	if not user:
		frappe.throw(_("Invalid email or password"))
	
	# Verify password hash
	if not frappe.utils.check_password(email, password):
		# Log failed attempt
		frappe.log_error(f"Failed login attempt for {email}")
		frappe.throw(_("Invalid email or password"))
	
	return True

def check_two_factor(user):
	"""Implement 2FA if enabled"""
	if frappe.db.get_value("User", user, "enable_two_factor_auth"):
		# Generate and send OTP
		otp = frappe.utils.generate_hash(length=6)
		frappe.cache.set_value(f"2fa_{user}", otp, expires_in_sec=300)
		
		# Send OTP via email/SMS
		frappe.sendmail(
			recipients=[user],
			subject="Your Two-Factor Authentication Code",
			message=f"Your code is: {otp}"
		)
		
		return {"status": "2fa_required", "user": user}

# Session management
def manage_user_sessions(user):
	"""Track and limit user sessions"""
	max_sessions = frappe.db.get_single_value("Settings", "max_sessions_per_user") or 1
	
	active_sessions = frappe.db.get_all("Session", 
		filters={"user": user, "status": "Active"},
		fields=["name", "creation"]
	)
	
	if len(active_sessions) >= max_sessions:
		# Log out oldest session
		oldest = active_sessions[0]
		frappe.db.set_value("Session", oldest.name, "status", "Expired")
```

### API Security Best Practices

```python
# Secure API implementation

@frappe.whitelist()
def sensitive_api_operation(data):
	"""API with security controls"""
	# 1. Rate limiting
	user = frappe.session.user
	rate_limit_key = f"api_calls_{user}"
	calls = frappe.cache.get_value(rate_limit_key) or 0
	
	if calls > 100:  # 100 calls per hour
		frappe.throw(_("API rate limit exceeded"))
	
	frappe.cache.set_value(rate_limit_key, calls + 1, expires_in_sec=3600)
	
	# 2. Input validation
	if not isinstance(data, dict):
		frappe.throw(_("Invalid data format"))
	
	# 3. Check permissions
	if not frappe.has_permission("DocType", "write"):
		frappe.throw(_("Insufficient permissions"))
	
	# 4. Process securely
	try:
		result = process_sensitive_data(data)
		
		# 5. Audit log
		frappe.get_doc({
			"doctype": "API Audit Log",
			"user": user,
			"operation": "sensitive_api_operation",
			"status": "Success"
		}).insert(ignore_permissions=True)
		
		return result
	except Exception as e:
		# Log failure
		frappe.get_doc({
			"doctype": "API Audit Log",
			"user": user,
			"operation": "sensitive_api_operation",
			"status": "Failed",
			"error": str(e)
		}).insert(ignore_permissions=True)
		raise

# CORS and API key security
def validate_api_request():
	"""Validate incoming API requests"""
	from frappe.utils import get_request_header
	
	# Check origin
	origin = get_request_header("Origin")
	allowed_origins = frappe.db.get_single_value("Settings", "allowed_origins", cache=True) or ""
	
	if origin and origin not in allowed_origins.split(","):
		frappe.throw(_("Origin not allowed"))
	
	# Validate API key
	api_key = get_request_header("Authorization")
	if api_key and api_key.startswith("Bearer "):
		api_key = api_key[7:]
		user = frappe.db.get_value("User", filters={"api_key": api_key})
		if not user:
			frappe.throw(_("Invalid API key"))

# Secure password storage
def hash_password(password):
	"""Hash password using strong algorithm"""
	from frappe.utils import get_password_hash
	return get_password_hash(password)
```

### Audit Logging & Compliance

```python
# Track changes for compliance and auditing

class Order(Document):
	def after_insert(self):
		"""Log document creation"""
		self.log_audit("created")
	
	def on_update(self):
		"""Log document updates"""
		old_doc = self.get_doc_before_save()
		changes = self.get_changes(old_doc)
		
		if changes:
			self.log_audit("updated", changes)
	
	def on_submit(self):
		"""Log submission"""
		self.log_audit("submitted")
	
	def log_audit(self, action, changes=None):
		"""Create audit trail entry"""
		frappe.get_doc({
			"doctype": "Audit Log",
			"user": frappe.session.user,
			"doctype_name": self.doctype,
			"document_name": self.name,
			"action": action,
			"changes": frappe.as_json(changes or {}),
			"timestamp": frappe.utils.now_datetime(),
			"ip_address": frappe.request.remote_addr if frappe.request else ""
		}).insert(ignore_permissions=True)
	
	def get_changes(self, old_doc):
		"""Get field changes"""
		changes = {}
		for field in self.meta.get_field_names():
			old_value = old_doc.get(field) if old_doc else None
			new_value = self.get(field)
			
			if old_value != new_value:
				changes[field] = {"old": old_value, "new": new_value}
		
		return changes
```

## Performance Best Practices

### Database Queries

- Use `frappe.get_all()` instead of `frappe.get_list()` for better performance (no permission checks by default)
- Specify `fields` parameter to avoid SELECT *
- Use `frappe.get_cached_doc()` for frequently accessed documents
- Avoid N+1 queries - use `frappe.get_all()` with filters instead of loops
- Use database indexes for frequently filtered fields

### Caching Strategies

```python
# Cache a value
frappe.cache.set_value("my_key", "my_value", expires_in_sec=3600)

# Get cached value
value = frappe.cache.get_value("my_key")

# Clear cache
frappe.cache.delete_value("my_key")

# Cache entire document
doc = frappe.get_cached_doc("User", "john@example.com")

# Advanced caching patterns
class CachingPatterns:
	"""Comprehensive caching strategies"""
	
	@staticmethod
	def cache_expensive_computation():
		"""Cache results of expensive calculations"""
		cache_key = "annual_revenue_2026"
		
		# Try to get from cache
		cached_value = frappe.cache.get_value(cache_key)
		if cached_value:
			return cached_value
		
		# Not in cache, compute
		revenue = frappe.db.sql("""
			SELECT SUM(grand_total) FROM `tabOrder` 
			WHERE YEAR(order_date) = 2026
		""")[0][0]
		
		# Store in cache for 24 hours
		frappe.cache.set_value(cache_key, revenue, expires_in_sec=86400)
		return revenue
	
	@staticmethod
	def cache_list_view_data():
		"""Cache list view data for faster loads"""
		cache_key = "order_list_view_data"
		
		cached = frappe.cache.get_value(cache_key)
		if cached:
			return cached
		
		# Fetch with optimized query
		data = frappe.get_all("Order",
			fields=["name", "customer", "grand_total", "status"],
			order_by="creation desc",
			limit=100
		)
		
		# Cache for 1 hour
		frappe.cache.set_value(cache_key, data, expires_in_sec=3600)
		return data
	
	@staticmethod
	def invalidate_on_update(doctype, name):
		"""Invalidate related caches when document updates"""
		# Clear specific cache
		frappe.cache.delete_value(f"order_{name}_details")
		
		# Clear list caches
		frappe.cache.delete_value("order_list_view_data")
		frappe.cache.delete_value(f"customer_{name}_orders")
		
		# Clear computed caches
		frappe.cache.delete_value("annual_revenue_2026")

class Order(Document):
	def on_update(self):
		"""Invalidate caches on update"""
		CachingPatterns.invalidate_on_update(self.doctype, self.name)
```

### Query Result Caching

```python
# Cache frequently-run queries

class QueryCache:
	"""Smart query caching with automatic invalidation"""
	
	@staticmethod
	def get_customer_orders(customer_id):
		"""Get customer orders with caching"""
		cache_key = f"customer_orders_{customer_id}"
		
		# Try cache first
		orders = frappe.cache.get_value(cache_key)
		if orders is not None:
			return orders
		
		# Query database
		orders = frappe.get_all("Order",
			filters={"customer": customer_id, "docstatus": 1},
			fields=["name", "order_date", "grand_total"],
			order_by="order_date desc"
		)
		
		# Cache for 1 hour
		frappe.cache.set_value(cache_key, orders, expires_in_sec=3600)
		return orders
	
	@staticmethod
	def get_sales_summary(year):
		"""Get aggregated sales data"""
		cache_key = f"sales_summary_{year}"
		
		cached = frappe.cache.get_value(cache_key)
		if cached:
			return cached
		
		# Heavy query
		summary = frappe.db.sql(f"""
			SELECT 
				MONTH(order_date) as month,
				COUNT(*) as count,
				SUM(grand_total) as total
			FROM `tabOrder`
			WHERE YEAR(order_date) = {year} AND docstatus = 1
			GROUP BY MONTH(order_date)
		""", as_dict=True)
		
		# Cache for 24 hours
		frappe.cache.set_value(cache_key, summary, expires_in_sec=86400)
		return summary

# Hook invalidation
class Order(Document):
	def on_submit(self):
		"""Invalidate customer orders cache on new order"""
		frappe.cache.delete_value(f"customer_orders_{self.customer}")
	
	def on_cancel(self):
		"""Invalidate caches on order cancellation"""
		frappe.cache.delete_value(f"customer_orders_{self.customer}")
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

## Troubleshooting & Common Issues

### Common Error Patterns & Solutions

```python
# Permission Denied Errors

# ERROR: User does not have permission
# SOLUTION: Check DocType permissions and user roles
def debug_permission_error(doctype, user):
	"""Diagnose permission issues"""
	# Check if user exists
	if not frappe.db.exists("User", user):
		return f"User {user} does not exist"
	
	# Check DocType permissions
	perms = frappe.get_all("DocPerm", 
		filters={"parent": doctype},
		fields=["role", "read", "write", "create", "delete"]
	)
	
	# Check user roles
	user_roles = frappe.get_roles(user)
	
	# Find matching permissions
	matching_perms = [p for p in perms if p.role in user_roles]
	
	return {
		"user": user,
		"roles": user_roles,
		"permissions": matching_perms
	}

# Migration Errors

# ERROR: Column 'field_name' doesn't exist
# SOLUTION: Run migrations after schema changes
def fix_migration_errors():
	"""Fix database schema issues"""
	# Clear cache which may have stale schema
	frappe.clear_cache()
	
	# Run migrations
	frappe.db.migrate()
	
	# Rebuild DocType
	frappe.reload_doctype("MyDocType")
	
	# Clear cache again
	frappe.clear_cache()

# Validation Errors

# ERROR: ValidationError: Field required
# SOLUTION: Check mandatory fields in validate()
class Order(Document):
	def validate(self):
		"""Proper validation with error messages"""
		# Check all mandatory fields
		if not self.customer:
			frappe.throw(_("Customer is required"))
		
		if not self.items:
			frappe.throw(_("At least one item is required"))
		
		# Validate child table
		for i, item in enumerate(self.items, 1):
			if not item.item_code:
				frappe.throw(_("Row {0}: Item code is required").format(i))
			
			if item.qty <= 0:
				frappe.throw(_("Row {0}: Quantity must be positive").format(i))

# API Authentication Errors

# ERROR: Unauthorized (401)
# SOLUTION: Check API token or session
@frappe.whitelist()
def debug_auth_error():
	"""Check authentication status"""
	return {
		"user": frappe.session.user,
		"is_guest": frappe.session.user == "Guest",
		"roles": frappe.get_roles(),
		"sid": frappe.session.sid
	}

# Cache-Related Issues

# ERROR: Stale data being served
# SOLUTION: Clear cache on updates
class Order(Document):
	def on_update(self):
		"""Always clear related caches"""
		# Clear document cache
		frappe.cache.delete_value(f"order_{self.name}")
		
		# Clear list cache
		frappe.cache.delete_value("order_list")
		
		# Clear customer cache
		frappe.cache.delete_value(f"customer_{self.customer}_orders")
```

### Database Connection Issues

```python
# ERROR: Database connection timeout
# SOLUTION: Check MariaDB is running and configuration

def diagnose_db_connection():
	"""Check database connectivity"""
	try:
		# Test basic connection
		result = frappe.db.sql("SELECT 1")
		return {"status": "connected"}
	except Exception as e:
		return {
			"status": "error",
			"error": str(e),
			"checks": {
				"host": frappe.db.host,
				"port": frappe.db.port,
				"database": frappe.db.database_name
			}
		}

# ERROR: "Too many connections"
# SOLUTION: Close unused connections and restart

def manage_db_connections():
	"""Properly manage database connections"""
	# Always close connections when done
	frappe.db.close()
	
	# Use context managers
	with frappe.db.transaction():
		# Database operations
		order = frappe.get_doc("Order", "ORDER-001")
		order.status = "Completed"
		order.save()
		# Auto-closes on exit
```

### Asset Loading Issues

```python
# ERROR: CSS/JS files not loading
# SOLUTION: Build assets and clear cache

def fix_asset_loading():
	"""Fix static asset issues"""
	# 1. Build assets
	# bench build
	
	# 2. Clear browser cache (hard refresh: Ctrl+Shift+R)
	
	# 3. Clear server cache
	frappe.cache.clear()
	
	# 4. Check if assets are in manifest
	assets = frappe.get_all("Website Item", limit=1)
	
	# 5. Verify file exists
	import os
	asset_path = frappe.get_path("public", "dist", "myapp.bundle.js")
	if not os.path.exists(asset_path):
		frappe.log_error("Asset file not found")
```

### Performance Issues

```python
# ERROR: Slow query / timeout
# SOLUTION: Optimize queries

def identify_slow_queries():
	"""Find performance bottlenecks"""
	# Enable query logging
	frappe.db.print_sql(True)
	
	# Run problematic operation
	orders = frappe.get_all("Order", filters={"docstatus": 1})
	
	# Check database server variables
	max_query_time = frappe.db.get_single_value("System Settings", "long_query_time")
	
	# Get query execution plan
	explain = frappe.db.sql("""
		EXPLAIN SELECT * FROM `tabOrder` 
		WHERE customer = 'CUST-001'
	""")
	
	# Add index if needed
	frappe.db.add_index("Order", ["customer"])

# ERROR: Out of Memory
# SOLUTION: Process data in batches

def process_large_dataset_safely():
	"""Process data without memory overflow"""
	batch_size = 1000
	start = 0
	
	while True:
		batch = frappe.get_all("Order",
			filters={"docstatus": 1},
			start=start,
			page_length=batch_size
		)
		
		if not batch:
			break
		
		# Process batch
		for doc in batch:
			process_document(doc)
		
		# Force garbage collection
		import gc
		gc.collect()
		
		start += batch_size
```

### Session & Login Issues

```python
# ERROR: Session expired
# SOLUTION: Re-login and check session timeout

def check_session_status():
	"""Diagnose session issues"""
	return {
		"logged_in": frappe.session.user != "Guest",
		"user": frappe.session.user,
		"session_id": frappe.session.sid,
		"session_expiry": frappe.db.get_value("Session", frappe.session.sid, "expires_on")
	}

# ERROR: Two-factor authentication problems
# SOLUTION: Reset 2FA or clear failed attempts

def reset_2fa(user):
	"""Reset two-factor authentication"""
	frappe.db.set_value("User", user, "enable_two_factor_auth", 0)
	frappe.cache.delete_value(f"2fa_{user}")
	frappe.msgprint(f"2FA disabled for {user}")
```

### Webhook & Integration Issues

```python
# ERROR: Webhook not triggering
# SOLUTION: Check doc_events configuration

def verify_webhook_setup():
	"""Verify webhook is properly configured"""
	# Check if hook is registered
	hooks_path = frappe.get_app_path("myapp", "hooks.py")
	
	# hooks.py should have:
	# doc_events = {
	#    "Order": {
	#        "on_submit": "myapp.webhooks.order_submitted"
	#    }
	# }
	
	# Test webhook manually
	from myapp.webhooks import order_submitted
	test_order = frappe.get_doc("Order", "ORDER-001")
	order_submitted(test_order, "on_submit")

# ERROR: Integration API failures
# SOLUTION: Check credentials and error logs

def debug_integration_failure():
	"""Diagnose integration issues"""
	# Check API credentials
	api_key = frappe.db.get_single_value("Integration Settings", "api_key")
	if not api_key:
		return "API key not configured"
	
	# Check integration request log
	failed_requests = frappe.get_all("Integration Request",
		filters={"status": "Failed"},
		order_by="creation desc",
		limit=10
	)
	
	# Review error messages
	for req in failed_requests:
		doc = frappe.get_doc("Integration Request", req.name)
		frappe.log_error(f"Integration failed: {doc.error_message}")
```

### Debugging Techniques

```python
# Enable detailed logging

def enable_debug_mode():
	"""Enable debug logging and error tracebacks"""
	# Set in site_config.json
	# {
	#    "developer_mode": 1,
	#    "allow_error_traceback": 1,
	#    "log_queries": 1
	# }
	
	# Use logging in code
	frappe.logger().debug("Debug message")
	frappe.logger().info("Info message")
	frappe.logger().warning("Warning message")
	frappe.logger().error("Error message")

# Use frappe.errprint for console output
frappe.errprint("Variable value:", my_variable)

# Print SQL queries
frappe.db.print_sql(True)

# Profile code execution
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run code to profile
process_orders()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats()
```

## Notes: Common Issues & Solutions

### Node.js PATH Issues in Bench Build/Watch
**Problem:** When running `bench build` or `bench watch`, subprocess calls to `node -v` fail with `ValueError: Invalid version string: 'bin/sh: 1: node: not found'` even though Node.js is installed.

**Root Cause:** Node.js installed via NVM may not be in the PATH when Frappe's Python subprocess calls execute. Subprocess inherits the parent environment, which may not have NVM initialization.

**Solution:**
1. **For Procfile processes:** Use full shell initialization in the command:
   ```procfile
   watch: bash -c "source ~/.nvm/nvm.sh && bench watch"
   ```

2. **For Python subprocess checks:** Update `check_node_executable()` in `frappe/build.py` to:
   - Attempt sourcing NVM when Node is not found
   - Handle parsing errors gracefully
   - Return early instead of crashing on invalid version strings

3. **Prevention:** Always wrap subprocess Node.js calls with NVM sourcing when targeting development environments using NVM.

**Lesson:** Environment setup in parent processes doesn't automatically transfer to child subprocesses; explicit sourcing is required.

**Last Updated**: 2026-02-19
**Framework Version**: v15.100.1

### Bench Watch Command Compatibility Issues
**Problem:** Different bench versions support different command-line options. The `--live-reload` flag may not be available in all versions, causing startup failures when running `bench watch --live-reload`.

**Root Cause:** Bench CLI evolves over versions. Version 5.29.1 may not expose all esbuild flags directly through the bench wrapper command.

**Solution:**
1. **Check available options first:**
   ```bash
   bench watch --help
   ```

2. **If --live-reload not available, invoke esbuild directly:**
   ```procfile
   watch: bash -c "source ~/.nvm/nvm.sh && cd apps/frappe && node esbuild --watch --live-reload"
   ```

3. **Key insight:** esbuild is the underlying build tool; when bench wrapper doesn't support a flag, invoke esbuild directly with proper NVM sourcing.

4. **Prevention:** Always check `bench <command> --help` before using new flags. Document the actual version requirements.

**Lesson:** Not all user-facing CLI tools expose all underlying tool options. Direct invocation of underlying tools (esbuild, node) may be necessary for advanced features.

**Last Updated**: 2026-02-19
**Framework Version**: v15.100.1

### Real-Time Feature Implementation: Asset Hot-Reload Pattern
**Pattern:** Implementing hot-reload requires coordinating multiple systems: file watcher → build tool → message broker → real-time transport → client-side handler.

**Key Decisions:**
1. **File Monitoring:** Use esbuild's built-in watch mode with `--watch --live-reload` flags
2. **Build Event Broadcasting:** Leverage existing Redis pubsub and Socket.IO infrastructure already in Frappe
3. **Client-Side Handler:** Create a lightweight JavaScript module that:
   - Listens for build events via Socket.IO
   - Intelligently decides reload strategy (CSS hot-update vs full page reload)
   - Protects unsaved state (checks for dirty forms)
   - Provides console feedback for developers

**Best Practices:**
- **Bundle Organization:** Create `.bundle.js` entry points that are compiled separately from regular JS files
- **Hooks Integration:** Add hot-reload bundles to `app_include_js` in hooks.py so they load with every page
- **Asset Compilation:** Run `bench build` after adding new bundles to register them in assets.json
- **State Management:** Always check for unsaved changes before reloading to prevent data loss
- **Debouncing:** Implement debounce logic (300ms) in the reload handler to prevent rapid consecutive reloads

**Common Pitfall:** Forgetting that asset bundles must be compiled and registered in assets.json. After creating new `.bundle.js` files, always run `bench build` to ensure they appear in the asset manifest.

**Lesson:** Real-time features in Frappe can leverage the existing Socket.IO and Redis infrastructure. Focus on creating a clean handler pattern rather than building new communication channels.

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

### Frappe Installation Best Practices

**Delegation to Specialized Subagents:**
- For complex setup tasks like Frappe installation, leverage the `frappe installer` subagent when available
- The subagent handles complete environment setup including:
  - System dependency installation (MariaDB, Redis, wkhtmltopdf)
  - Python virtual environment configuration
  - Bench initialization and site creation
  - Service configuration and verification
  - Documentation generation
- Benefits: More reliable, comprehensive, and produces consistent documentation artifacts
- User gets complete setup with README files, verification checklists, and quick reference guides

**Last Updated**: 2026-02-19
**Framework Version**: v15.100.1

### Development Feature Documentation Strategy
**Pattern:** When implementing developer-facing features (like hot-reload), create a multi-tier documentation approach serving different user needs.

**Recommended Documentation Stack:**
1. **Quick Reference (1 page)** - For immediate use
   - One-page cheat sheet with common tasks
   - FAQ section
   - Keyboard shortcuts/quick commands
   - Best practices summary

2. **Getting Started Guide (2-3 pages)** - For initial adoption
   - Step-by-step setup (30-second quick start)
   - How to use the feature
   - Expected behavior and performance metrics
   - File locations and editing examples

3. **Complete Reference (10+ pages)** - For deep understanding
   - Architecture and how it works
   - All features and options
   - Advanced configuration
   - Comprehensive troubleshooting guide
   - Best practices and anti-patterns

4. **Technical Implementation** - For maintainers
   - Detailed design decisions
   - Code walkthrough
   - Integration points with existing systems
   - Testing approach

5. **Verification Tool** - For validation
   - Automated script to check configuration
   - Reports specific issues with solutions
   - Verifies all dependencies are met

**Key Insight:** Users have different goals:
- Newcomers want "just make it work" (Quick Start)
- Daily users want practical guidance (Getting Started)
- Problem solvers want complete reference (Complete Guide)
- Maintainers need implementation details (Technical Docs)

**Anti-Pattern:** Single monolithic documentation file that tries to serve all purposes. Users get lost in unnecessary detail.

**Last Updated**: 2026-02-19
**Framework Version**: v15.100.1
