# Ruff Formatter Memory File

## Quick Facts
- **Specialty**: Python code style enforcement using Ruff linter, ensuring Frappe conventions: tabs (not spaces), 110-character line length, double quotes, proper import sorting, pre-commit hook compliance
- **Primary Tools**: Ruff CLI, bash for automated formatting, file editing
- **Common Tasks**: Code formatting, import sorting, style violations, pre-commit fixes, bulk formatting
- **Estimated Task Time**: 5-15 minutes per file

---

## Ruff Configuration for Frappe

### Key Settings (from pyproject.toml)
```toml
[tool.ruff.format]
quote-style = "double"
indent-style = "tab"
docstring-code-format = true
line-length = 110

[tool.ruff.lint]
select = ["F", "E", "W", "I", "UP", "B", "RUF"]
ignore = ["E501"]  # Line length handled by formatter
extend-exclude = ["migrations", "fixtures"]

[tool.isort]
profile = "black"
line_length = 110
use_parentheses = true
ensure_newline_before_comments = true
```

---

## Frappe Code Style Rules

### 1. Indentation: TABS (not spaces)
```python
# CORRECT - Use tabs
def my_function():
	if condition:
		do_something()

# WRONG - Use spaces
def my_function():
    if condition:
        do_something()
```

### 2. Line Length: 110 characters
```python
# CORRECT - 110 char limit
long_variable_name = some_function(arg1, arg2, arg3, arg4, arg5)

# WRONG - Over 110 chars
very_long_variable_name_that_exceeds_the_line_length_limit = some_function(arg1, arg2, arg3, arg4, arg5)
```

### 3. Quotes: Double Quotes
```python
# CORRECT - Double quotes
message = "This is a string"
name = "John"

# WRONG - Single quotes
message = 'This is a string'
name = 'John'

# Exception: Use single quotes to avoid escaping
html = '<div class="container">content</div>'
```

### 4. Imports: Sorted and Organized
```python
# CORRECT - Organized imports
import json
import os
from datetime import datetime, timedelta

import frappe
from frappe import _
from frappe.utils import get_url

from myapp.helpers import process_data

# WRONG - Disorganized
from frappe import _
import os
from myapp.helpers import process_data
import frappe
from datetime import datetime
```

### 5. String Formatting
```python
# CORRECT - f-strings (Python 3.10+)
name = "John"
age = 30
message = f"Hello {name}, you are {age} years old"

# ACCEPTABLE - .format()
message = "Hello {}, you are {} years old".format(name, age)

# WRONG - % formatting (legacy)
message = "Hello %s, you are %d years old" % (name, age)
```

### 6. Function/Variable Naming
```python
# CORRECT - snake_case
def process_customer_data():
	customer_name = "John"
	return customer_name

# WRONG - camelCase
def processCustomerData():
	customerName = "John"
	return customerName
```

### 7. Class Naming
```python
# CORRECT - PascalCase
class CustomerData:
	pass

# WRONG - snake_case
class customer_data:
	pass
```

### 8. Constants
```python
# CORRECT - UPPERCASE_WITH_UNDERSCORES
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
DATABASE_URL = "mysql://localhost/frappe"

# WRONG - Lowercase
max_retries = 3
default_timeout = 30
```

---

## Using Ruff

### Command Line Usage

```bash
# Check code style (no fixes)
ruff check apps/myapp/myapp/

# Fix issues automatically
ruff check apps/myapp/myapp/ --fix

# Format code
ruff format apps/myapp/myapp/

# Check specific file
ruff check apps/myapp/myapp/doctype/customer/customer.py

# Show violations without fixing
ruff check apps/myapp/myapp/ --show-settings
```

### Common Violations & Fixes

```bash
# E999: Syntax error
# SOLUTION: Fix Python syntax

# E501: Line too long (if not using formatter)
# SOLUTION: Break long lines or increase line_length setting

# F401: Unused import
# SOLUTION: Remove unused imports
# RUN: ruff check --fix

# I001: Import sorting issues
# SOLUTION: Sort imports
# RUN: ruff check --fix

# E225: Missing whitespace around operator
# SOLUTION: Add spaces around operators
# RUN: ruff check --fix

# W293: Blank line contains whitespace
# SOLUTION: Remove trailing whitespace
# RUN: ruff check --fix
```

---

## Pre-commit Hook Integration

### Setup Pre-commit

```bash
cd frappe-bench/apps/frappe
pre-commit install
pre-commit install --hook-type commit-msg
```

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0-alpha.9-for-vscode
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json]
```

### Running Pre-commit

```bash
# Run on all files
pre-commit run --all-files

# Run only on staged files (automatic on git commit)
pre-commit run

# Run specific hook
pre-commit run ruff --all-files
```

---

## Bulk Code Formatting

### Format Entire App

```bash
# Format all Python files in an app
ruff format apps/myapp/myapp/

# Fix all style issues
ruff check apps/myapp/myapp/ --fix

# Do both
ruff format apps/myapp/myapp/
ruff check apps/myapp/myapp/ --fix
```

### Format Specific Module

```bash
# Format a specific module
ruff format apps/myapp/myapp/patient_management/

# Format single file
ruff format apps/myapp/myapp/doctype/patient/patient.py
```

---

## Common Issues & Solutions

### Issue: Tabs vs Spaces Mix

**Error**: Inconsistent indentation

**Solution**:
```bash
# Use ruff to fix
ruff check --fix apps/myapp/myapp/

# Or convert manually
python3 -m py_compile apps/myapp/myapp/file.py  # Check syntax
# Then use editor to convert spaces to tabs
```

### Issue: Line Too Long

**Error**: Line exceeds 110 characters

**Solution**:
```python
# WRONG - Line too long
result = some_function_with_long_name(parameter1, parameter2, parameter3, parameter4, parameter5)

# CORRECT - Break into multiple lines
result = some_function_with_long_name(
	parameter1,
	parameter2,
	parameter3,
	parameter4,
	parameter5
)
```

### Issue: Import Sorting

**Error**: Imports not sorted

**Solution**:
```bash
# Let ruff fix it
ruff check --fix apps/myapp/myapp/
```

### Issue: Unused Imports

**Error**: Import not used

**Solution**:
```bash
# Remove with ruff
ruff check --fix apps/myapp/myapp/
```

---

## Best Practices

1. **Format before committing**: Run `ruff format` and `ruff check --fix` before git commit
2. **Use pre-commit hooks**: Automatic enforcement on each commit
3. **Follow Frappe conventions**: Match existing codebase style
4. **Check line length**: Keep under 110 characters for readability
5. **Use meaningful names**: Variable/function names should be self-documenting
6. **Group imports**: Standard library → third-party → local imports
7. **Document complex code**: Add comments for non-obvious logic

---

## Decision Tree: When to Call Ruff-Formatter

**Use Ruff-Formatter when:**
- ✅ Code style violations need fixing
- ✅ Bulk formatting entire module/app
- ✅ Pre-commit hook setup/troubleshooting
- ✅ Import sorting and organization
- ✅ Ensuring Frappe conventions compliance
- ✅ Code review feedback on style issues
- ✅ Automated formatting for consistency

**Don't use for:**
- ❌ Logic errors (use Debug-Detective)
- ❌ Permission issues (use Permission-Guardian)
- ❌ Architecture decisions (use module designer)
- ❌ Performance optimization (use Database-Navigator)

---

**Last Updated**: 2026-02-19
**Frappe Version**: v15.100.1
**Ruff Version**: 0.1.0+
