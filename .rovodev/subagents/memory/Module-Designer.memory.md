# Module Designer Memory File

## Quick Facts
- **Specialty**: Creating complete Frappe modules with DocTypes, workspaces, dashboards, reports, navigation setup, module-level permissions
- **Primary Tools**: File creation, JSON editing, workspace configuration, dashboard design
- **Common Tasks**: Module structure setup, workspace creation, dashboard charts, module organization, sidebar navigation
- **Estimated Task Time**: 60-120 minutes per module

---

## Module Structure

### Standard Module Layout
```
apps/myapp/myapp/
├── module_name/
│   ├── doctype/
│   │   ├── doctype1/
│   │   │   ├── doctype1.json
│   │   │   ├── doctype1.py
│   │   │   └── doctype1.js
│   │   └── doctype2/
│   ├── workspace/
│   │   ├── module_workspace.json
│   │   └── doctype_workspace.json
│   ├── dashboard/
│   │   └── module_dashboard.json
│   ├── page/
│   │   └── custom_page.py
│   ├── report/
│   │   └── custom_report.py
│   └── __init__.py
└── modules.txt  # Lists all modules
```

### modules.txt Structure
```
Patient Management
Appointment Scheduling
Clinical Operations
Laboratory
Inventory Management
Equipment Management
Billing
Staff Management
Reporting
```

---

## Core Module Components

### Component 1: Module Configuration

**File**: `apps/myapp/myapp/module_name/__init__.py`

```python
# Module initialization (often empty or with module metadata)
from __future__ import unicode_literals
```

### Component 2: Workspace (Main Entry Point)

**File**: `apps/myapp/myapp/module_name/workspace/module_workspace.json`

```json
{
	"doctype": "Workspace",
	"name": "Patient Management",
	"module": "Patient Management",
	"label": "Patient Management",
	"sidebar": 1,
	"cards": [
		{
			"name": "Patient Master",
			"label": "Patient Master",
			"icon": "icon-square",
			"link": "List/Patient",
			"links": [
				{
					"label": "Patient",
					"name": "Patient",
					"type": "Link",
					"icon": "icon-link"
				},
				{
					"label": "New Patient",
					"name": "Patient",
					"type": "Link New",
					"icon": "icon-plus"
				}
			]
		},
		{
			"name": "Reports",
			"label": "Reports",
			"icon": "icon-list",
			"links": [
				{
					"label": "Patient Analysis",
					"name": "Patient Analysis",
					"type": "Report",
					"icon": "icon-bar-chart"
				}
			]
		},
		{
			"name": "Settings",
			"label": "Settings",
			"icon": "icon-cog",
			"links": [
				{
					"label": "Patient Category",
					"name": "Patient Category",
					"type": "DocType",
					"icon": "icon-link"
				}
			]
		}
	],
	"charts": [
		{
			"chart_name": "Patient Growth",
			"label": "Patient Growth"
		}
	],
	"category": "Healthcare"
}
```

### Component 3: Dashboard

**File**: `apps/myapp/myapp/module_name/dashboard/module_dashboard.json`

```json
{
	"doctype": "Dashboard",
	"name": "Patient Management Dashboard",
	"dashboard_name": "Patient Management Dashboard",
	"charts": [
		{
			"chart_name": "Total Patients",
			"chart": "Total Patients",
			"width": 0.5
		},
		{
			"chart_name": "Patient Registration Trend",
			"chart": "Patient Registration Trend",
			"width": 0.5
		},
		{
			"chart_name": "Appointments by Status",
			"chart": "Appointments by Status",
			"width": 0.33
		}
	],
	"refresh_interval": 60
}
```

### Component 4: Dashboard Chart

**File**: `apps/myapp/myapp/module_name/dashboard/patient_count.json`

```json
{
	"doctype": "Dashboard Chart",
	"name": "Total Patients",
	"chart_name": "Total Patients",
	"chart_type": "Number",
	"document_type": "Patient",
	"based_on": "",
	"aggregate_function": "Count",
	"group_by": "",
	"filters": [
		{
			"filter_field": "docstatus",
			"filter_type": "=",
			"filter_value": "0"
		}
	],
	"is_public": 1
}
```

### Component 5: Report

**File**: `apps/myapp/myapp/module_name/report/patient_report.py`

```python
import frappe
from frappe import _

def execute(filters=None):
	columns = [
		{"label": _("Name"), "fieldname": "name", "width": 150},
		{"label": _("Patient Name"), "fieldname": "patient_name", "width": 150},
		{"label": _("Age"), "fieldname": "age", "width": 80},
		{"label": _("Category"), "fieldname": "category", "width": 100},
		{"label": _("Contact"), "fieldname": "contact_number", "width": 120},
	]
	
	data = frappe.get_all("Patient",
		fields=["name", "patient_name", "age", "category", "contact_number"],
		filters=get_filters(filters),
		order_by="creation desc"
	)
	
	return columns, data

def get_filters(filters):
	"""Build query filters"""
	filter_dict = {}
	
	if filters and filters.get("category"):
		filter_dict["category"] = filters["category"]
	
	if filters and filters.get("patient_name"):
		filter_dict["patient_name"] = ["like", f"%{filters['patient_name']}%"]
	
	return filter_dict
```

### Component 6: Module Permissions

**Setup in hooks.py**:
```python
default_roles = [
	{
		"role": "Patient Manager",
		"doctype": "Patient",
		"permlevel": 0,
		"permissions": ["read", "write", "create"]
	},
	{
		"role": "Clinic Staff",
		"doctype": "Patient",
		"permlevel": 0,
		"permissions": ["read"]
	}
]
```

---

## Common Module Patterns

### Pattern 1: Multi-Level DocType Organization

**Master Data Module**:
```json
{
	"cards": [
		{
			"name": "Masters",
			"links": [
				{"label": "Patient", "type": "Link"},
				{"label": "Doctor", "type": "Link"},
				{"label": "Department", "type": "Link"}
			]
		},
		{
			"name": "Categories",
			"links": [
				{"label": "Patient Category", "type": "Link"},
				{"label": "Disease Type", "type": "Link"}
			]
		},
		{
			"name": "Settings",
			"links": [
				{"label": "Clinic Settings", "type": "Link"}
			]
		}
	]
}
```

### Pattern 2: Transaction Processing Module

**Appointment Module**:
```json
{
	"cards": [
		{
			"name": "Appointments",
			"links": [
				{"label": "New Appointment", "type": "Link New"},
				{"label": "All Appointments", "type": "Link"},
				{"label": "My Appointments", "filter": "created by current user"}
			]
		},
		{
			"name": "Analytics",
			"links": [
				{"label": "Appointment Report", "type": "Report"},
				{"label": "Doctor Workload", "type": "Report"}
			]
		}
	]
}
```

### Pattern 3: Dashboard with Real-Time Data

**Billing Module Dashboard**:
```json
{
	"doctype": "Dashboard",
	"charts": [
		{
			"chart_name": "Daily Revenue",
			"label": "Daily Revenue",
			"chart_type": "Line",
			"width": 0.5
		},
		{
			"chart_name": "Outstanding Amount",
			"label": "Outstanding Amount",
			"chart_type": "Gauge",
			"width": 0.5
		},
		{
			"chart_name": "Payment Methods",
			"label": "Payment Methods",
			"chart_type": "Pie",
			"width": 0.33
		}
	],
	"refresh_interval": 300
}
```

---

## Workspace Configuration Best Practices

### Navigation Best Practices
- **Top Level**: Main business functions (Patient, Appointment, Billing)
- **Secondary**: Supporting functions (Reports, Analytics, Settings)
- **Grouping**: Logical grouping by workflow phase
- **Icons**: Consistent, recognizable icons for each card
- **Naming**: Clear, user-friendly names (not technical)

### Card Organization
```json
{
	"cards": [
		{"position": 0, "label": "Daily Tasks"},
		{"position": 1, "label": "Master Data"},
		{"position": 2, "label": "Transactions"},
		{"position": 3, "label": "Reports"},
		{"position": 4, "label": "Settings"}
	]
}
```

### Link Types
- **Link**: Go to DocType list view
- **Link New**: Create new document shortcut
- **Report**: Direct to report
- **Page**: Custom page
- **DocType**: Configuration/settings

---

## Decision Tree: When to Call Module-Designer

**Use Module-Designer when:**
- ✅ Setting up new module structure
- ✅ Creating workspaces and navigation
- ✅ Designing dashboards and charts
- ✅ Organizing module-level permissions
- ✅ Setting up module documentation
- ✅ Creating module-specific reports
- ✅ Organizing multi-DocType workflows

**Don't use for:**
- ❌ Individual DocType design (use DocType-Architect)
- ❌ API development (use API-Whitelister)
- ❌ Permission setup (use Permission-Guardian)
- ❌ Frontend components (use Frontend-Forge)

---

## Integration Points

**Works with:**
- DocType-Architect: Designs DocTypes in the module
- Frontend-Forge: Customizes workspace/dashboard UI
- Permission-Guardian: Sets module-level permissions
- All other subagents: Organize their deliverables into module

**Key files:**
- `modules.txt` - Module listing
- `workspace/*.json` - Navigation and entry points
- `dashboard/*.json` - Dashboard definitions
- `report/*.py` - Module-specific reports
- `hooks.py` - Module-level configuration

---

**Last Updated**: 2026-02-19
**Frappe Version**: v15.100.1
**Module Organization Pattern**: Hierarchical, permission-aware
