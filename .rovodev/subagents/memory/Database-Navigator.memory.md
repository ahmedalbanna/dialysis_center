# Database Navigator Memory File

## Quick Facts
- **Specialty**: Frappe ORM operations, query optimization, database schema management, raw SQL, migrations, and performance tuning
- **Primary Tools**: File creation/editing, bash for testing queries
- **Common Tasks**: Query optimization, N+1 detection/fixing, migration creation, index management, transaction handling
- **Estimated Task Time**: 15-30 minutes per query/optimization

---

## Most Common Patterns (80% of work)

### Pattern 1: Optimized Query with Frappe ORM

**Scenario**: Fetch orders with related customer data efficiently.

```python
# File: apps/myapp/myapp/api/order_queries.py

# WRONG - N+1 problem (1 query per order)
def get_orders_slow():
	"""This will run hundreds of queries!"""
	orders = frappe.get_all("Order", filters={"docstatus": 1}, fields=["name"])
	
	result = []
	for order in orders:
		doc = frappe.get_doc("Order", order.name)  # Query for each order!
		customer_name = frappe.db.get_value("Customer", doc.customer, "customer_name")
		result.append({
			"order_id": order.name,
			"customer": customer_name
		})
	return result

# CORRECT - Single query with all needed fields
def get_orders_optimized():
	"""Efficient query - includes customer field directly"""
	orders = frappe.get_all(
		"Order",
		filters={"docstatus": 1},
		fields=["name", "customer", "customer_name", "order_date", "grand_total"],
		order_by="creation desc",
		limit=100
	)
	return orders

# EVEN BETTER - If you need customer_name, fetch it separately once
def get_orders_best():
	"""Most efficient for complex data"""
	# Get orders
	orders = frappe.get_all(
		"Order",
		filters={"docstatus": 1},
		fields=["name", "customer", "order_date", "grand_total"],
		order_by="creation desc",
		limit=100
	)
	
	# Get unique customers (batch operation)
	customer_ids = set(o["customer"] for o in orders)
	customers = frappe.get_all(
		"Customer",
		filters={"name": ["in", list(customer_ids)]},
		fields=["name", "customer_name"]
	)
	
	# Create lookup dict (memory efficient)
	customer_map = {c["name"]: c["customer_name"] for c in customers}
	
	# Enrich orders with customer names
	for order in orders:
		order["customer_name"] = customer_map.get(order["customer"], "")
	
	return orders
```

**Key Optimization Rules**:
- ✅ **Always specify `fields`** (don't use `*`)
- ✅ **Batch fetch related data** (one query per relation type)
- ✅ **Use cache for lookups** (customer names, item details)
- ✅ **Paginate large result sets** (use `limit` or `page_length`)
- ✅ **Create lookup dictionaries** (avoid nested loops)

---

### Pattern 2: Advanced Query with Filters & Aggregation

**Scenario**: Get monthly sales summary with totals and counts.

```python
from frappe.query_builder import DocType, Field

def get_sales_summary(year=None, month=None):
	"""
	Get monthly sales summary with aggregations
	"""
	if not year:
		year = frappe.utils.getdate().year
	
	Order = DocType("Order")
	
	# Build base query
	query = (
		frappe.qb.from_(Order)
		.select(
			Field("MONTH(order_date)").as_("month"),
			Field("COUNT(*)").as_("order_count"),
			Field("SUM(grand_total)").as_("total_amount"),
			Field("AVG(grand_total)").as_("avg_amount")
		)
		.where((Order.docstatus == 1) & (Field("YEAR(order_date)") == year))
		.groupby(Field("MONTH(order_date)"))
		.orderby(Field("MONTH(order_date)"))
	)
	
	# Add optional month filter
	if month:
		query = query.where(Field("MONTH(order_date)") == month)
	
	# Execute and return
	return query.run(as_dict=True)

# Usage
summary = get_sales_summary(year=2026, month=2)
# Returns: [
#   {"month": 1, "order_count": 45, "total_amount": 50000, "avg_amount": 1111.11},
#   ...
# ]
```

**Key Query Builder Features**:
- Use `Field()` for SQL functions (COUNT, SUM, AVG, MONTH, YEAR)
- Chain `.where()` for multiple conditions with `&` (AND) or `|` (OR)
- Use `.groupby()` and `.having()` for aggregations
- Always use `.run(as_dict=True)` for readability

---

### Pattern 3: Complex Join Query

**Scenario**: Get orders with customer details and total items.

```python
from frappe.query_builder import DocType, Field

def get_orders_with_details():
	"""
	Join Order with Customer and count items
	"""
	Order = DocType("Order")
	Customer = DocType("Customer")
	OrderItem = DocType("Order Item")
	
	# Complex query with joins
	query = (
		frappe.qb.from_(Order)
		.join(Customer).on(Order.customer == Customer.name)
		.left_join(OrderItem).on(Order.name == OrderItem.parent)
		.select(
			Order.name,
			Order.order_date,
			Customer.customer_name,
			Customer.email,
			Field("COUNT(DISTINCT").concat(OrderItem.name).concat(")").as_("item_count"),
			Field("SUM(DISTINCT").concat(OrderItem.line_total).concat(")").as_("total_amount")
		)
		.where(Order.docstatus == 1)
		.groupby(Order.name, Order.customer, Customer.name)
		.having(Field("COUNT(DISTINCT").concat(OrderItem.name).concat(")") > 0)
		.orderby(Order.creation, order="DESC")
	)
	
	return query.run(as_dict=True)
```

**Key Join Patterns**:
- `.join()` for INNER JOIN (required match)
- `.left_join()` for LEFT JOIN (all from left table)
- Always specify `.on()` condition
- Use `.groupby()` with all non-aggregate fields
- Use `.having()` for filtering aggregated results

---

### Pattern 4: Batch Processing Large Datasets

**Scenario**: Process 100,000 orders without memory overflow.

```python
def process_all_orders_efficiently():
	"""
	Batch process large dataset without loading everything into memory
	"""
	batch_size = 1000
	start = 0
	total_processed = 0
	
	while True:
		# Fetch one batch
		orders = frappe.get_all(
			"Order",
			filters={"docstatus": 1},
			fields=["name", "customer", "grand_total"],
			start=start,
			page_length=batch_size
		)
		
		# Exit if no more data
		if not orders:
			break
		
		# Process this batch
		for order_data in orders:
			process_single_order(order_data)
			total_processed += 1
			
			# Log progress every 10%
			if total_processed % (batch_size * 10) == 0:
				frappe.logger().info(f"Processed {total_processed} orders")
		
		# Commit after each batch
		frappe.db.commit()
		
		# Move to next batch
		start += batch_size
		
		# Optional: Memory cleanup
		import gc
		gc.collect()
	
	return {"total_processed": total_processed}

def process_single_order(order_data):
	"""Process one order"""
	# Calculate commissions, update balances, etc.
	pass
```

**Batch Processing Best Practices**:
- ✅ Fetch in batches (1000-5000 per batch)
- ✅ Commit after each batch (frees locks)
- ✅ Log progress for monitoring
- ✅ Call gc.collect() for long-running jobs
- ✅ Use for data migrations and bulk updates

---

### Pattern 5: Transaction Management with Rollback

**Scenario**: Create linked documents atomically (Order → Invoice → Payment).

```python
def create_order_with_invoice_and_payment(order_data, invoice_data, payment_data):
	"""
	Create order and related docs in one transaction.
	If ANY step fails, rollback EVERYTHING.
	"""
	try:
		# Start transaction
		with frappe.db.transaction():
			# Step 1: Create order
			order = frappe.get_doc({
				"doctype": "Order",
				**order_data
			})
			order.insert()
			frappe.logger().info(f"Created order: {order.name}")
			
			# Step 2: Create invoice from order
			invoice = frappe.get_doc({
				"doctype": "Invoice",
				"order_id": order.name,
				**invoice_data
			})
			invoice.insert()
			frappe.logger().info(f"Created invoice: {invoice.name}")
			
			# Step 3: Create payment
			payment = frappe.get_doc({
				"doctype": "Payment",
				"order_id": order.name,
				"invoice_id": invoice.name,
				**payment_data
			})
			payment.insert()
			frappe.logger().info(f"Created payment: {payment.name}")
			
			# If we get here, transaction will auto-commit
			return {
				"order": order.name,
				"invoice": invoice.name,
				"payment": payment.name
			}
	
	except Exception as e:
		# Transaction auto-rolls back on exception
		frappe.logger().error(f"Transaction failed, rolling back: {str(e)}")
		frappe.log_error(f"Order creation failed: {str(e)}")
		raise

# Usage
result = create_order_with_invoice_and_payment(
	order_data={"customer": "CUST-001", ...},
	invoice_data={"amount": 10000, ...},
	payment_data={"status": "Pending", ...}
)
```

**Transaction Guarantees**:
- ✅ ALL operations succeed or ALL rollback
- ✅ No partial states possible
- ✅ Database locks held only during transaction
- ✅ Automatic commit on success, rollback on exception

---

### Pattern 6: Index Management for Performance

**Scenario**: Optimize slow queries by adding appropriate indexes.

```python
def analyze_and_optimize():
	"""
	Analyze slow queries and create indexes
	"""
	# 1. Enable query logging
	frappe.db.print_sql(True)
	
	# 2. Run slow query
	orders = frappe.get_all(
		"Order",
		filters={"customer": "CUST-001", "order_date": [">=", "2026-01-01"]},
		fields=["name", "grand_total"]
	)
	
	# 3. Check execution plan (look for full table scans)
	frappe.db.sql("""
		EXPLAIN SELECT * FROM `tabOrder` 
		WHERE `customer` = 'CUST-001' 
		AND `order_date` >= '2026-01-01'
	""")
	
	# 4. Add indexes for frequent filters
	frappe.db.add_index("Order", ["customer"])
	frappe.db.add_index("Order", ["order_date"])
	frappe.db.add_index("Order", ["customer", "order_date"])  # Composite index
	
	# 5. Verify index is used
	frappe.db.sql("""
		EXPLAIN SELECT * FROM `tabOrder` 
		WHERE `customer` = 'CUST-001' 
		AND `order_date` >= '2026-01-01'
	""")
	# Look for "Using index" in output

def list_all_indexes():
	"""List all indexes for a table"""
	indexes = frappe.db.sql("""
		SELECT INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
		FROM INFORMATION_SCHEMA.STATISTICS
		WHERE TABLE_NAME = 'tabOrder'
		ORDER BY INDEX_NAME, SEQ_IN_INDEX
	""", as_dict=True)
	
	return indexes
```

**Index Best Practices**:
- ✅ Index frequently filtered columns
- ✅ Composite indexes for multi-column filters
- ✅ Don't over-index (slows down writes)
- ✅ Regular ANALYZE TABLE to update statistics
- ✅ Use EXPLAIN to verify index usage

---

## Advanced Patterns (20% of work)

### Pattern 7: Caching Query Results

```python
def get_customer_orders_cached(customer_id, cache_minutes=60):
	"""
	Cache expensive query results in Redis
	"""
	cache_key = f"customer_orders_{customer_id}"
	
	# Try to get from cache first
	cached_orders = frappe.cache.get_value(cache_key)
	if cached_orders is not None:
		frappe.logger().debug(f"Cache hit for {cache_key}")
		return cached_orders
	
	# Not in cache, fetch from database
	frappe.logger().debug(f"Cache miss for {cache_key}, fetching from DB")
	orders = frappe.get_all(
		"Order",
		filters={"customer": customer_id},
		fields=["name", "order_date", "grand_total"],
		order_by="order_date desc"
	)
	
	# Store in cache with expiry
	frappe.cache.set_value(cache_key, orders, expires_in_sec=cache_minutes * 60)
	
	return orders

def invalidate_customer_cache(customer_id):
	"""Clear cache when customer data changes"""
	frappe.cache.delete_value(f"customer_orders_{customer_id}")
```

### Pattern 8: Data Migration Pattern

```python
def migrate_customer_types():
	"""
	Migrate data safely with validation and rollback
	"""
	total = 0
	errors = []
	
	try:
		with frappe.db.transaction():
			# Get all customers
			customers = frappe.get_all("Customer", fields=["name", "old_type"])
			
			for customer in customers:
				try:
					# Map old type to new type
					mapping = {
						"corp": "Business",
						"indv": "Individual",
						"retail": "Business"
					}
					
					new_type = mapping.get(customer["old_type"])
					if new_type:
						frappe.db.set_value("Customer", customer["name"], "customer_type", new_type)
						total += 1
				except Exception as e:
					errors.append({"customer": customer["name"], "error": str(e)})
			
			# Validate migration
			invalid = frappe.db.sql("""
				SELECT COUNT(*) as count FROM `tabCustomer` 
				WHERE `customer_type` NOT IN ('Business', 'Individual')
			""")[0][0]
			
			if invalid > 0:
				frappe.throw(frappe._("Migration incomplete, rolling back"))
			
			frappe.logger().info(f"Migrated {total} customers")
	
	except Exception as e:
		frappe.logger().error(f"Migration failed: {str(e)}")
		raise
	
	return {"total_migrated": total, "errors": errors}
```

---

## Common Mistakes & Solutions

### Mistake 1: N+1 Query Problem
```python
# WRONG - 101 queries!
orders = frappe.get_all("Order", limit=100)
for order in orders:
	customer = frappe.db.get_value("Customer", order.customer, "customer_name")

# CORRECT - 2 queries
orders = frappe.get_all("Order", fields=["name", "customer"], limit=100)
customers = frappe.get_all("Customer", fields=["name", "customer_name"])
cust_map = {c["name"]: c["customer_name"] for c in customers}
```

### Mistake 2: Loading All Fields Unnecessarily
```python
# WRONG - loads 50 fields you don't need
orders = frappe.get_all("Order", fields=["*"])

# CORRECT - load only needed fields
orders = frappe.get_all("Order", fields=["name", "customer", "grand_total"])
```

### Mistake 3: Forgetting to Commit
```python
# WRONG - changes might be lost
def update_orders():
	for order in orders:
		frappe.db.set_value("Order", order.name, "status", "Processed")

# CORRECT - commit after batch
def update_orders():
	for order in orders:
		frappe.db.set_value("Order", order.name, "status", "Processed")
	frappe.db.commit()
```

### Mistake 4: Not Handling NULL Values
```python
# WRONG - comparison fails for NULL
orders = frappe.get_all("Order", filters={"notes": ""})

# CORRECT - explicitly check for NULL
orders = frappe.get_all("Order", filters={"notes": ["is", "not set"]})
```

### Mistake 5: Over-using Raw SQL
```python
# WRONG - SQL injection risk
customer = request.args.get("name")
result = frappe.db.sql(f"SELECT * FROM `tabCustomer` WHERE name = '{customer}'")

# CORRECT - parameterized query
customer = request.args.get("name")
result = frappe.db.sql("SELECT * FROM `tabCustomer` WHERE name = %s", (customer,))

# EVEN BETTER - use ORM
customer = frappe.get_doc("Customer", customer)
```

---

## Testing Database Queries

```python
def test_query_performance():
	"""Test query execution and performance"""
	import time
	
	# Create test data
	for i in range(1000):
		frappe.get_doc({
			"doctype": "Order",
			"customer": f"CUST-{i % 100}",
			"grand_total": i * 100
		}).insert()
	frappe.db.commit()
	
	# Test slow query
	start = time.time()
	orders = frappe.get_all("Order", fields=["*"])  # Slow!
	slow_time = time.time() - start
	
	# Test optimized query
	start = time.time()
	orders = frappe.get_all("Order", fields=["name", "customer", "grand_total"])  # Fast!
	fast_time = time.time() - start
	
	print(f"Slow: {slow_time:.3f}s, Fast: {fast_time:.3f}s")
	assert fast_time < slow_time * 0.5  # Should be much faster
```

---

## Performance Checklist

- [ ] Specify `fields` (don't use `*`)
- [ ] Batch fetch related data
- [ ] Use cache for lookups
- [ ] Paginate large result sets
- [ ] Create indexes for filters
- [ ] Use EXPLAIN to verify
- [ ] Batch process large updates
- [ ] Commit after batches
- [ ] Profile with `frappe.db.print_sql()`
- [ ] Cache expensive queries

---

## Integration with Other Subagents

- **Works with**: API-Whitelister (for APIs), DocType-Architect (for schema)
- **Hands off to**: Bench-Master for DB configuration
- **Context to pass**: Table structure, filter conditions, expected output

---

## Quick Database Command Reference

```python
# Get one document
doc = frappe.get_doc("Order", "ORD-2026-001")

# Get multiple documents
orders = frappe.get_all("Order", filters={"docstatus": 1}, limit=100)

# Get single value
customer_name = frappe.db.get_value("Customer", "CUST-001", "customer_name")

# Set single value
frappe.db.set_value("Order", "ORD-2026-001", "status", "Completed")

# Check existence
exists = frappe.db.exists("Order", "ORD-2026-001")

# Delete
frappe.delete_doc("Order", "ORD-2026-001")

# Raw SQL
result = frappe.db.sql("SELECT * FROM `tabOrder` LIMIT 10", as_dict=True)

# Count
count = frappe.db.count("Order", filters={"docstatus": 1})

# Save transaction
with frappe.db.transaction():
	# Multiple operations here
	pass
```

