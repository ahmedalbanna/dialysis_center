# Frontend Forge Memory File

## Quick Facts
- **Specialty**: Client-side JavaScript development, form customization, Vue.js components, custom UI/UX, list views, reports, and real-time interactions
- **Primary Tools**: File creation/editing, bash for testing
- **Common Tasks**: Form event scripts, list view customization, report development, custom dialogs, real-time updates
- **Estimated Task Time**: 25-40 minutes per feature

---

## Most Common Patterns (80% of work)

### Pattern 1: Complete Form Event Script

**Scenario**: Create a custom form with field dependencies, validations, and dynamic calculations.

```javascript
// File: apps/myapp/myapp/public/js/order_form.js
// Auto-loaded for Order form

frappe.ui.form.on("Order", {
	// Form-level events
	onload: function(frm) {
		// Called when form first loads
		frm.set_intro("Create a new order for your customer");
		
		// Customize form layout
		frm.layout.main.wrapper.classList.add("custom-order-form");
		
		// Add custom buttons
		frm.add_custom_button(__("Print Order"), function() {
			frappe.call({
				method: "myapp.api.print_order",
				args: {order_id: frm.doc.name},
				callback: function(r) {
					frappe.msgprint(__("Order printed"));
				}
			});
		}, __("Actions"));
	},
	
	refresh: function(frm) {
		// Called every time form redraws
		// Control field visibility based on document state
		frm.set_df_property("notes", "hidden", frm.doc.docstatus !== 0);
		
		// Show/hide sections
		frm.set_df_property("items_section", "hidden", !frm.doc.customer);
		
		// Set field requirements dynamically
		if (frm.doc.order_type === "Bulk") {
			frm.set_df_property("min_quantity", "reqd", 1);
		} else {
			frm.set_df_property("min_quantity", "reqd", 0);
		}
		
		// Update button visibility based on docstatus
		frm.page.clear_primary_action();
		if (frm.doc.docstatus === 0) {
			frm.page.set_primary_action(__("Save"), () => frm.save());
		} else if (frm.doc.docstatus === 1) {
			frm.page.set_primary_action(__("Amend"), () => frm.amend_doc());
		}
	},
	
	validate: function(frm) {
		// Client-side validation before save
		if (!frm.doc.customer) {
			frappe.throw(__("Customer is required"));
		}
		
		if (frm.doc.items.length === 0) {
			frappe.throw(__("Order must have at least one item"));
		}
		
		// Validate each item
		for (let i = 0; i < frm.doc.items.length; i++) {
			const item = frm.doc.items[i];
			if (!item.item_code) {
				frappe.throw(__("Row {0}: Item code is required").format(i + 1));
			}
			if (item.qty <= 0) {
				frappe.throw(__("Row {0}: Quantity must be positive").format(i + 1));
			}
		}
	},
	
	before_save: function(frm) {
		// Data preparation before saving
		// Trim whitespace
		frm.doc.customer_name = frm.doc.customer_name?.trim() || "";
		
		// Calculate totals
		frm.doc.total_qty = frm.doc.items.reduce((sum, item) => sum + item.qty, 0);
		frm.doc.total_amount = frm.doc.items.reduce((sum, item) => sum + (item.qty * item.rate), 0);
	},
	
	after_save: function(frm) {
		// Post-save actions
		frappe.msgprint(__("Order saved successfully"));
		
		// Clear any temporary data
		frappe.cache.delete_value(`temp_order_${frm.doc.name}`);
	},
	
	// Field-level events
	customer: function(frm) {
		// When customer field changes
		if (!frm.doc.customer) return;
		
		// Fetch customer details
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
					frm.set_value("currency", r.message.default_currency);
				}
			}
		});
	},
	
	order_type: function(frm) {
		// Handle order type change
		if (frm.doc.order_type === "Bulk") {
			frm.set_df_property("min_quantity", "reqd", 1);
			frm.set_value("discount_percent", 10);
		} else {
			frm.set_df_property("min_quantity", "reqd", 0);
			frm.set_value("discount_percent", 0);
		}
		frm.refresh_field("min_quantity");
		frm.refresh_field("discount_percent");
	},
	
	// Child table events
	items_add: function(frm, cdt, cdn) {
		// When new row added to items table
		let row = frappe.get_model(cdt, cdn);
		row.qty = 1;
		row.rate = 0;
	},
	
	items_remove: function(frm, cdt, cdn) {
		// When row removed from items table
		// Recalculate total
		frm.doc.total_amount = frm.doc.items.reduce((sum, item) => sum + (item.qty * item.rate), 0);
		frm.refresh_field("total_amount");
	},
	
	items_qty: function(frm, cdt, cdn) {
		// When quantity changes in items table
		let row = frappe.get_model(cdt, cdn);
		row.line_total = row.qty * row.rate;
		frappe.model.set_value(cdt, cdn, "line_total", row.line_total);
		
		// Recalculate parent total
		frm.doc.total_amount = frm.doc.items.reduce((sum, item) => sum + (item.line_total || 0), 0);
		frm.refresh_field("total_amount");
	}
});

// Conditional field visibility
frappe.ui.form.on("Order", {
	order_date: function(frm) {
		// Show warning if order is old
		const days_old = frappe.datetime.get_day_diff(frappe.datetime.now_date(), frm.doc.order_date);
		if (days_old > 30) {
			frappe.msgprint(__("Warning: This order is {0} days old").format(days_old));
		}
	}
});
```

**Key Patterns**:
- ✅ Use `onload` for initialization (one-time setup)
- ✅ Use `refresh` for state-dependent UI (called multiple times)
- ✅ Field events for specific field changes
- ✅ Child table events for row operations
- ✅ Always check conditions before operations
- ✅ Use `frappe.msgprint()` for success messages
- ✅ Use `frappe.throw()` for errors

---

### Pattern 2: List View Customization

**Scenario**: Customize the Order list with custom columns, formatters, and bulk actions.

```javascript
// File: apps/myapp/myapp/public/js/order_list.js

frappe.listview_settings['Order'] = {
	// Add custom fields to display
	add_fields: ["customer_name", "grand_total", "status", "creation"],
	
	// Custom column formatting
	formatters: {
		status: function(value, df, options) {
			// Format status with color indicator
			const colors = {
				"Draft": "lightgray",
				"Submitted": "lightblue",
				"Completed": "lightgreen",
				"Cancelled": "lightcoral"
			};
			
			return `<span style="background-color: ${colors[value] || 'white'}; padding: 4px 8px; border-radius: 3px;">${value}</span>`;
		},
		
		grand_total: function(value, df, options) {
			// Format currency
			return frappe.format(value, {fieldtype: "Currency"});
		},
		
		creation: function(value, df, options) {
			// Format date relative to today
			return frappe.datetime.str_to_user(value);
		}
	},
	
	// Filter orders by default
	filters: [
		["docstatus", "!=", 2],  // Exclude cancelled
		["creation", ">", frappe.datetime.add_days("today", -90)]  // Last 90 days
	],
	
	// Custom actions on list
	onload: function(listview) {
		// Add custom button to toolbar
		listview.page.add_menu_item(__("Export Orders"), function() {
			const selected = listview.get_checked_items();
			if (selected.length === 0) {
				frappe.msgprint(__("Please select orders to export"));
				return;
			}
			
			frappe.call({
				method: "myapp.api.export_orders",
				args: {order_ids: selected.map(d => d.name)},
				callback: function(r) {
					frappe.msgprint(__("Orders exported successfully"));
				}
			});
		});
		
		// Add filter button
		listview.page.add_action_item(__("Today's Orders"), function() {
			listview.filter_area.add([
				["Order", "creation", ">=", frappe.datetime.now_date()]
			]);
			listview.refresh();
		});
	},
	
	refresh: function(listview) {
		// Update list after changes
		const selected_count = listview.get_checked_items().length;
		
		if (selected_count > 0) {
			// Show bulk action button
			listview.page.add_action_item(__("Process Selected"), function() {
				const selected = listview.get_checked_items();
				frappe.call({
					method: "myapp.api.bulk_process_orders",
					args: {order_ids: selected.map(d => d.name)},
					callback: function(r) {
						listview.refresh();
					}
				});
			});
		}
	}
};
```

**Key Patterns**:
- ✅ Use `formatters` for custom column display
- ✅ Use `filters` for default list filtering
- ✅ Use `onload` for toolbar customization
- ✅ Use `get_checked_items()` for bulk operations
- ✅ Always check if items are selected before action
- ✅ Refresh list after bulk operations

---

### Pattern 3: Custom Dialog for Data Collection

**Scenario**: Create a modal dialog for order quick entry.

```javascript
function show_quick_order_dialog() {
	const dialog = new frappe.ui.Dialog({
		title: __("Quick Order"),
		size: "large",
		static: true,  // Prevent closing on background click
		fields: [
			{
				fieldtype: "Link",
				fieldname: "customer",
				label: __("Customer"),
				options: "Customer",
				reqd: 1,
				change: function() {
					// When customer changes, fetch their default currency
					const customer = dialog.get_value("customer");
					if (customer) {
						frappe.db.get_value("Customer", customer, "default_currency", function(r) {
							if (r.message) {
								dialog.set_value("currency", r.message.default_currency);
							}
						});
					}
				}
			},
			{
				fieldtype: "Date",
				fieldname: "order_date",
				label: __("Order Date"),
				default: frappe.datetime.now_date(),
				reqd: 1
			},
			{
				fieldtype: "Select",
				fieldname: "currency",
				label: __("Currency"),
				options: "\nUSD\nEUR\nGBP\nAED"
			},
			{
				fieldtype: "Section Break",
				label: __("Items")
			},
			{
				fieldtype: "Table",
				fieldname: "items",
				label: __("Order Items"),
				data: []
			}
		],
		primary_action_label: __("Create Order"),
		primary_action(values) {
			// Validate before creating
			if (!values.customer) {
				frappe.msgprint(__("Customer is required"));
				return;
			}
			
			if (!values.items || values.items.length === 0) {
				frappe.msgprint(__("At least one item is required"));
				return;
			}
			
			// Create order via API
			frappe.call({
				method: "myapp.api.create_order_from_dialog",
				args: {
					customer: values.customer,
					order_date: values.order_date,
					currency: values.currency,
					items: values.items
				},
				callback: function(r) {
					if (r.message) {
						frappe.msgprint(__("Order created: {0}").format(r.message.order_id));
						dialog.hide();
						
						// Refresh list if open
						if (cur_list) {
							cur_list.refresh();
						}
					}
				}
			});
		},
		secondary_action_label: __("Cancel"),
		secondary_action() {
			dialog.hide();
		}
	});
	
	dialog.show();
}
```

**Key Patterns**:
- ✅ Use `Dialog` for modal forms
- ✅ Validate before submitting
- ✅ Use `change` callback for dependent fields
- ✅ Call API to create documents
- ✅ Refresh related list/form after success
- ✅ Clear dialog after success

---

## Advanced Patterns (20% of work)

### Pattern 4: Real-Time Updates via Socket.IO

```javascript
// Listen for real-time document updates
frappe.realtime.on("doctype:Order:update", function(data) {
	if (data.doctype === cur_frm.doctype && data.name === cur_frm.doc.name) {
		// Current form was updated by another user
		frappe.msgprint(__("This document was updated by another user"));
		cur_frm.reload_doc();
	}
});

// Publish event from backend when document changes
frappe.call({
	method: "myapp.api.update_order",
	args: {order_id: "ORD-001", status: "Completed"},
	callback: function(r) {
		// Backend will publish: frappe.publish_realtime("doctype:Order:update", {...})
	}
});
```

### Pattern 5: Client-Side Caching

```javascript
function get_customer_cached(customer_id) {
	// Try localStorage first (persists across sessions)
	let cached = localStorage.getItem(`customer_${customer_id}`);
	if (cached) {
		return JSON.parse(cached);
	}
	
	// Fetch from server
	frappe.db.get_value("Customer", customer_id, 
		["name", "customer_name", "credit_limit"], 
		function(r) {
			if (r.message) {
				// Cache locally
				localStorage.setItem(`customer_${customer_id}`, JSON.stringify(r.message));
				
				// Also cache in frappe cache (session only)
				frappe.cache.set_value(`customer_${customer_id}`, r.message);
			}
		}
	);
}
```

---

## Common Mistakes & Solutions

### Mistake 1: Not Checking for Form Existence
```javascript
// WRONG - crashes if form not open
cur_frm.set_value("status", "Active");

// CORRECT - check if form exists
if (cur_frm && cur_frm.doctype === "Order") {
	cur_frm.set_value("status", "Active");
}
```

### Mistake 2: Modifying Child Table Wrong Way
```javascript
// WRONG - direct modification doesn't update UI
frm.doc.items[0].qty = 10;

// CORRECT - use frappe methods
frappe.model.set_value(frm.doc.items[0].doctype, frm.doc.items[0].name, "qty", 10);
frm.refresh_field("items");
```

### Mistake 3: Not Handling Async Operations
```javascript
// WRONG - assumes data is available immediately
frappe.db.get_value("Customer", customer, "credit_limit");
console.log(credit_limit);  // Undefined!

// CORRECT - use callback
frappe.db.get_value("Customer", customer, "credit_limit", function(r) {
	if (r.message) {
		console.log(r.message.credit_limit);  // Now available
	}
});
```

### Mistake 4: Memory Leaks in Event Listeners
```javascript
// WRONG - listener never removed
$(document).on("click", ".my-button", function() { ... });

// CORRECT - use jQuery off() or event namespacing
$(document).on("click.myapp", ".my-button", function() { ... });
$(document).off("click.myapp");
```

### Mistake 5: Not Refreshing Fields After Change
```javascript
// WRONG - field value changes but UI doesn't update
frm.doc.total = 100;

// CORRECT - refresh the field
frm.set_value("total", 100);
// Or for read-only fields:
frm.doc.total = 100;
frm.refresh_field("total");
```

---

## Testing Frontend Code

```javascript
// Manual test in browser console
// 1. Set field value
cur_frm.set_value("customer", "CUST-001");

// 2. Trigger field change event
cur_frm.fields_dict.customer.refresh();

// 3. Check calculated field
console.log(cur_frm.doc.total);

// 4. Test list view filtering
cur_list.filter_area.add([["Order", "status", "=", "Draft"]]);
cur_list.refresh();
```

---

## Performance Considerations

- Cache frequently accessed data (localStorage, frappe.cache)
- Debounce field change handlers (avoid too many API calls)
- Use `frappe.timeout` for delayed operations
- Minimize DOM manipulation in loops
- Use `frappe.after_ajax()` for operations after requests

---

## Integration with Other Subagents

- **Works with**: API-Whitelister (API calls), Database-Navigator (data loading)
- **Hands off to**: API-Whitelister when building backend APIs
- **Context to pass**: UI requirements, form structure, user interactions

---

## Quick Frontend Checklist

- [ ] Form events (onload, refresh, validate, before_save, after_save)
- [ ] Field-level change handlers
- [ ] Child table add/remove/change handlers
- [ ] Async API calls with callbacks
- [ ] Error handling with frappe.throw/msgprint
- [ ] Cache management (localStorage, frappe.cache)
- [ ] UI state management (hidden, reqd, read_only)
- [ ] List view customization
- [ ] Custom dialogs for data entry
- [ ] Real-time updates via Socket.IO
