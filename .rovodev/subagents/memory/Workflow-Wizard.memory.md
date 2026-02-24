# Workflow Wizard Memory File

## Quick Facts
- **Specialty**: Frappe workflow system, state transitions, approval flows, role-based routing, email notifications, workflow actions, complex multi-step workflows
- **Primary Tools**: Workflow DocType creation, automation setup, state management
- **Common Tasks**: Order approval workflows, document submission states, conditional routing, automated actions
- **Estimated Task Time**: 40-80 minutes per workflow

---

## Workflow Architecture

### Core Components
1. **Workflow Document** - Defines states and transitions
2. **Workflow State** - Represents a document state (Draft, Pending Review, Approved, etc.)
3. **Workflow Action** - Represents a transition between states
4. **Workflow Assignment** - Assigns documents to users for approval
5. **Workflow Rules** - Conditions for transitioning between states

### State Machine Pattern
```
Initial State → Condition Check → Route to Reviewer
                   ↓ (Approved)     ↓
             Final State ← Reviewer Action
```

---

## Workflow Setup Pattern

### Step 1: Create Workflow DocType

**File**: Create via UI or use:
```python
frappe.get_doc({
	"doctype": "Workflow",
	"name": "Order Approval",
	"document_type": "Order",
	"is_active": 1,
	"states": [
		{
			"state": "Draft",
			"is_initial": 1,
			"allow_self_approval": 1
		},
		{
			"state": "Pending Review",
			"allow_self_approval": 0
		},
		{
			"state": "Approved",
			"is_end": 1,
			"allow_self_approval": 0
		},
		{
			"state": "Rejected",
			"is_end": 1,
			"allow_self_approval": 0
		}
	],
	"transitions": [
		{
			"state": "Draft",
			"next_state": "Pending Review",
			"action": "Submit for Review",
			"allowed_roles": ["Order Creator"]
		},
		{
			"state": "Pending Review",
			"next_state": "Approved",
			"action": "Approve",
			"allowed_roles": ["Approver"],
			"conditions": "doc.grand_total <= 10000"
		},
		{
			"state": "Pending Review",
			"next_state": "Rejected",
			"action": "Reject",
			"allowed_roles": ["Approver"]
		}
	]
}).insert()
```

### Step 2: Set Workflow on DocType

Edit DocType properties:
- Set `Workflow State Field` to `workflow_state` (field must exist in DocType)
- Enable workflow: Check `Has Auto Repeat` if needed

### Step 3: Add Workflow State Field to DocType

```json
{
	"fieldname": "workflow_state",
	"fieldtype": "Link",
	"label": "Workflow State",
	"options": "Workflow State",
	"read_only": 1,
	"hidden": 1
}
```

---

## Common Workflow Patterns

### Pattern 1: Simple Approval Workflow

**Use Case**: Order needs manager approval before proceeding

```python
def setup_order_approval_workflow():
	"""Setup simple 2-level approval"""
	workflow = frappe.get_doc({
		"doctype": "Workflow",
		"name": "Order Approval",
		"document_type": "Order",
		"is_active": 1,
		"states": [
			{"state": "Draft", "is_initial": 1},
			{"state": "Awaiting Approval", "allow_self_approval": 0},
			{"state": "Approved", "is_end": 1}
		],
		"transitions": [
			{
				"state": "Draft",
				"next_state": "Awaiting Approval",
				"action": "Submit",
				"allowed_roles": ["Order User"]
			},
			{
				"state": "Awaiting Approval",
				"next_state": "Approved",
				"action": "Approve",
				"allowed_roles": ["Manager"]
			}
		]
	})
	workflow.insert()
```

### Pattern 2: Conditional Approval (Amount-Based)

**Use Case**: Large orders need director approval, small orders need manager approval

```python
states = [
	{"state": "Draft", "is_initial": 1},
	{"state": "Manager Review", "allow_self_approval": 0},
	{"state": "Director Review", "allow_self_approval": 0},
	{"state": "Approved", "is_end": 1}
]

transitions = [
	{
		"state": "Draft",
		"next_state": "Manager Review",
		"action": "Submit",
		"allowed_roles": ["Sales User"],
		"trigger_message": "Order submitted for review"
	},
	{
		"state": "Manager Review",
		"next_state": "Approved",
		"action": "Approve",
		"allowed_roles": ["Manager"],
		"conditions": "doc.grand_total <= 50000",
		"trigger_message": "Order approved (under 50k)"
	},
	{
		"state": "Manager Review",
		"next_state": "Director Review",
		"action": "Escalate",
		"allowed_roles": ["Manager"],
		"conditions": "doc.grand_total > 50000",
		"trigger_message": "Order escalated to director"
	},
	{
		"state": "Director Review",
		"next_state": "Approved",
		"action": "Approve",
		"allowed_roles": ["Director"],
		"trigger_message": "Order approved by director"
	}
]
```

### Pattern 3: Multi-Step Workflow with Rejection

**Use Case**: Document review with feedback loop

```python
states = [
	{"state": "Draft", "is_initial": 1},
	{"state": "Review", "allow_self_approval": 0},
	{"state": "Revision Required"},
	{"state": "Final Review"},
	{"state": "Published", "is_end": 1}
]

transitions = [
	{
		"state": "Draft",
		"next_state": "Review",
		"action": "Submit",
		"allowed_roles": ["Editor"]
	},
	{
		"state": "Review",
		"next_state": "Revision Required",
		"action": "Request Changes",
		"allowed_roles": ["Reviewer"],
		"trigger_message": "Changes requested"
	},
	{
		"state": "Revision Required",
		"next_state": "Review",
		"action": "Resubmit",
		"allowed_roles": ["Editor"],
		"trigger_message": "Resubmitted for review"
	},
	{
		"state": "Review",
		"next_state": "Final Review",
		"action": "Approve",
		"allowed_roles": ["Reviewer"]
	},
	{
		"state": "Final Review",
		"next_state": "Published",
		"action": "Publish",
		"allowed_roles": ["Publisher"]
	}
]
```

### Pattern 4: Workflow with Automatic Transitions

**Use Case**: Document auto-finalizes after payment is received

```python
# Setup hook to trigger workflow transition
doc_events = {
	"Order": {
		"on_update": "myapp.workflows.check_auto_finalize"
	}
}

def check_auto_finalize(doc, method):
	"""Auto-transition workflow when payment received"""
	if doc.payment_status == "Paid" and doc.workflow_state == "Awaiting Payment":
		# Transition to next state
		frappe.workflow.apply_workflow(
			doc,
			action="Finalize"  # Transition action name
		)
		doc.save(ignore_permissions=True)
```

---

## Workflow Features & Actions

### Workflow Assignment (Auto-assign to users)

```python
def auto_assign_to_reviewer(doc, method):
	"""Auto-assign workflow document to appropriate reviewer"""
	
	# Determine reviewer based on amount
	if doc.grand_total > 100000:
		reviewer = "director@company.com"
	elif doc.grand_total > 50000:
		reviewer = "manager@company.com"
	else:
		reviewer = "approver@company.com"
	
	# Create workflow assignment
	frappe.get_doc({
		"doctype": "Workflow Assignment",
		"doctype_name": doc.doctype,
		"document_name": doc.name,
		"workflow_state": "Pending Review",
		"assigned_to": reviewer
	}).insert(ignore_permissions=True)
	
	# Send email notification
	frappe.sendmail(
		recipients=[reviewer],
		subject=f"Approval needed: {doc.name}",
		message=f"Order {doc.name} for {doc.grand_total} needs your approval"
	)
```

### Email Notifications on State Change

```python
def notify_on_state_change(doc, method):
	"""Send notifications when workflow state changes"""
	
	state_messages = {
		"Approved": {
			"recipients": [doc.created_by],
			"subject": "Order Approved",
			"message": f"Your order {doc.name} has been approved"
		},
		"Rejected": {
			"recipients": [doc.created_by],
			"subject": "Order Rejected",
			"message": f"Your order {doc.name} was rejected. Please contact support."
		}
	}
	
	if doc.workflow_state in state_messages:
		msg_config = state_messages[doc.workflow_state]
		frappe.sendmail(
			recipients=msg_config["recipients"],
			subject=msg_config["subject"],
			message=msg_config["message"]
		)
```

### Custom Workflow Actions

```python
def get_custom_workflow_actions(doc, method):
	"""Add custom workflow actions to document"""
	
	actions = []
	
	if doc.workflow_state == "Draft":
		actions.append({
			"label": "Submit for Review",
			"name": "submit_review",
			"submit": False
		})
	
	elif doc.workflow_state == "Pending Review":
		actions.append({
			"label": "Approve",
			"name": "approve",
			"submit": True
		})
		actions.append({
			"label": "Reject",
			"name": "reject",
			"submit": False
		})
	
	return actions
```

---

## Workflow API

### Programmatic Workflow Transitions

```python
# Get current state
current_state = frappe.db.get_value("Order", "ORDER-001", "workflow_state")

# Apply workflow action
doc = frappe.get_doc("Order", "ORDER-001")
frappe.workflow.apply_workflow(doc, action="Approve")
doc.save(ignore_permissions=True)

# Get available actions
from frappe.workflow import get_transitions
available_actions = get_transitions(doc, "workflow_state")

# Check if user can perform action
can_approve = frappe.workflow.check_authority(doc, "Approve")
```

### Workflow Query

```python
# Get all orders in approval state
orders_pending = frappe.get_all("Order",
	filters={"workflow_state": "Awaiting Approval"},
	fields=["name", "customer", "grand_total"]
)

# Get workflow assignments for current user
my_assignments = frappe.get_all("Workflow Assignment",
	filters={"assigned_to": frappe.session.user},
	fields=["document_name", "doctype_name", "workflow_state"]
)
```

---

## Decision Tree: When to Call Workflow-Wizard

**Use Workflow-Wizard when:**
- ✅ Setting up approval workflows
- ✅ Implementing state-based document processing
- ✅ Creating role-based routing
- ✅ Building conditional approval rules
- ✅ Automating workflow transitions
- ✅ Implementing email notifications tied to states
- ✅ Creating complex multi-step processes

**Don't use for:**
- ❌ Simple state tracking (use field in DocType)
- ❌ Permission management (use Permission-Guardian)
- ❌ Basic validation (use DocType validate)
- ❌ Scheduled tasks (use Hooks-Orchestrator)

---

## Pro Tips

1. **Keep workflows simple**: Complex workflows become hard to maintain
2. **Always include rejection states**: Users need feedback loop
3. **Use auto-assignment**: Reduces manual notification
4. **Log transitions**: Track who approved/rejected and when
5. **Test role permissions**: Ensure only authorized users can approve
6. **Document states**: Make state names clear to business users
7. **Use conditions sparingly**: Complex conditions reduce transparency

---

**Last Updated**: 2026-02-19
**Frappe Version**: v15.100.1
**Common Patterns**: Approval, Conditional, Multi-step, Auto-transition
