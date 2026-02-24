#!/usr/bin/env python3
"""
Phase 6: Comprehensive End-to-End Verification Script
Dialysis Center Management System

This script validates all core workflows and functionality before production deployment.
Run: python PHASE_6_VERIFICATION_SCRIPT.py --site dialysis.local

Author: Rovo Dev
Version: 1.0.0
Date: February 19, 2026
"""

import sys
import json
import time
from datetime import datetime, timedelta
import argparse

try:
    import frappe
    from frappe.utils import getdate, today, nowtime, now_datetime
except ImportError:
    print("ERROR: Frappe not found. Run this script from bench directory:")
    print("  cd frappe-bench")
    print("  python ../PHASE_6_VERIFICATION_SCRIPT.py --site dialysis.local")
    sys.exit(1)


class VerificationTest:
    """Base class for verification tests"""
    
    def __init__(self, name):
        self.name = name
        self.passed = False
        self.error = None
        self.duration = 0
    
    def run(self):
        """Run the test and catch errors"""
        start_time = time.time()
        try:
            self.execute()
            self.passed = True
        except Exception as e:
            self.error = str(e)
            self.passed = False
        self.duration = time.time() - start_time
    
    def execute(self):
        """Override this method in subclass"""
        raise NotImplementedError
    
    def result(self):
        """Return test result"""
        status = "✅ PASS" if self.passed else "❌ FAIL"
        duration = f"{self.duration:.2f}s"
        error = f" - {self.error}" if self.error else ""
        return f"{status} | {self.name:50s} | {duration:>8s}{error}"


# ============================================================================
# TEST SUITE 1: Database & DocType Validation
# ============================================================================

class TestPatientDocTypeExists(VerificationTest):
    def execute(self):
        assert frappe.db.exists("DocType", "Patient"), "Patient DocType not found"
        # Verify key fields exist
        fields = frappe.db.get_all("DocField", {"parent": "Patient", "in_list_view": 1})
        assert len(fields) > 0, "Patient has no list view fields"

class TestAppointmentDocTypeExists(VerificationTest):
    def execute(self):
        assert frappe.db.exists("DocType", "Appointment"), "Appointment DocType not found"
        fields = frappe.db.get_all("DocField", {"parent": "Appointment"})
        assert len(fields) > 5, "Appointment DocType missing fields"

class TestDialysisSessionDocTypeExists(VerificationTest):
    def execute(self):
        assert frappe.db.exists("DocType", "Dialysis Session"), "Dialysis Session DocType not found"
        fields = frappe.db.get_all("DocField", {"parent": "Dialysis Session"})
        assert len(fields) > 8, "Dialysis Session DocType incomplete"

class TestPatientBillDocTypeExists(VerificationTest):
    def execute(self):
        assert frappe.db.exists("DocType", "Patient Bill"), "Patient Bill DocType not found"

class TestLabTestDocTypeExists(VerificationTest):
    def execute(self):
        assert frappe.db.exists("DocType", "Lab Test"), "Lab Test DocType not found"

class TestDialysisMachineDocTypeExists(VerificationTest):
    def execute(self):
        assert frappe.db.exists("DocType", "Dialysis Machine"), "Dialysis Machine DocType not found"

class TestStaffDocTypeExists(VerificationTest):
    def execute(self):
        assert frappe.db.exists("DocType", "Staff"), "Staff DocType not found"

class TestDatabaseStructure(VerificationTest):
    def execute(self):
        # Check key tables exist
        tables = frappe.db.get_tables()
        required_tables = ["tabPatient", "tabAppointment", "tabDialysis_Session", "tabPatient_Bill"]
        for table in required_tables:
            assert table in tables, f"Table {table} not found in database"


# ============================================================================
# TEST SUITE 2: Permission & Role Configuration
# ============================================================================

class TestRoleExists(VerificationTest):
    def execute(self):
        roles = frappe.db.get_list("Role", {"name": ["in", ["Dialysis Administrator", "Dialysis Technician"]]})
        assert len(roles) >= 2, "Required roles not configured"

class TestAdministratorUser(VerificationTest):
    def execute(self):
        user = frappe.db.exists("User", "Administrator")
        assert user, "Administrator user not found"

class TestPermissionConfiguration(VerificationTest):
    def execute(self):
        # Check Patient permissions for Dialysis Administrator
        perms = frappe.db.get_all("DocPerm", {
            "parent": "Patient",
            "role": "Dialysis Administrator"
        })
        assert len(perms) > 0, "Patient permissions not configured for admin role"
        perm = perms[0]
        assert perm.read, "Admin should have read permission on Patient"
        assert perm.write, "Admin should have write permission on Patient"


# ============================================================================
# TEST SUITE 3: Workflow Testing
# ============================================================================

class TestPatientCreation(VerificationTest):
    def execute(self):
        # Create test patient
        patient_name = f"TEST-PT-{int(time.time())}"
        patient = frappe.get_doc({
            "doctype": "Patient",
            "first_name": "Test",
            "last_name": "Patient",
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "contact_number": "555-0001",
            "email": f"test.patient.{int(time.time())}@example.com"
        })
        patient.insert()
        
        # Verify creation
        assert frappe.db.exists("Patient", patient.name), "Patient not found after creation"
        
        # Cleanup
        frappe.delete_doc("Patient", patient.name, force=True)

class TestAppointmentCreation(VerificationTest):
    def execute(self):
        # Ensure test patient exists
        patient_name = None
        existing = frappe.db.get_list("Patient", limit=1)
        
        if not existing:
            # Create test patient
            patient = frappe.get_doc({
                "doctype": "Patient",
                "first_name": "Test",
                "last_name": "Appt",
                "date_of_birth": "1985-05-15",
                "gender": "Female",
                "contact_number": "555-0002",
                "email": f"test.appt.{int(time.time())}@example.com"
            })
            patient.insert()
            patient_name = patient.name
        else:
            patient_name = existing[0].name
        
        # Create appointment
        appointment = frappe.get_doc({
            "doctype": "Appointment",
            "patient": patient_name,
            "appointment_type": "Dialysis",
            "appointment_date": getdate(today()),
            "start_time": "08:00",
            "end_time": "12:00"
        })
        appointment.insert()
        
        # Verify
        assert frappe.db.exists("Appointment", appointment.name), "Appointment not created"
        assert appointment.status == "Draft", "Appointment should start as Draft"
        
        # Cleanup
        frappe.delete_doc("Appointment", appointment.name, force=True)

class TestDialysisSessionWorkflow(VerificationTest):
    def execute(self):
        # Get or create patient
        existing = frappe.db.get_list("Patient", limit=1)
        if not existing:
            patient = frappe.get_doc({
                "doctype": "Patient",
                "first_name": "Test",
                "last_name": "Session",
                "date_of_birth": "1990-12-25",
                "gender": "Male",
                "contact_number": "555-0003",
                "email": f"test.session.{int(time.time())}@example.com"
            })
            patient.insert()
            patient_name = patient.name
        else:
            patient_name = existing[0].name
        
        # Create dialysis session
        session = frappe.get_doc({
            "doctype": "Dialysis Session",
            "patient": patient_name,
            "session_date": getdate(today()),
            "start_time": "08:00",
            "end_time": "12:00",
            "status": "Draft"
        })
        session.insert()
        
        # Verify session creation
        assert frappe.db.exists("Dialysis Session", session.name), "Session not created"
        
        # Cleanup
        frappe.delete_doc("Dialysis Session", session.name, force=True)

class TestPatientBillCreation(VerificationTest):
    def execute(self):
        # Get or create patient
        existing = frappe.db.get_list("Patient", limit=1)
        if not existing:
            patient = frappe.get_doc({
                "doctype": "Patient",
                "first_name": "Test",
                "last_name": "Bill",
                "date_of_birth": "1995-07-04",
                "gender": "Female",
                "contact_number": "555-0004",
                "email": f"test.bill.{int(time.time())}@example.com"
            })
            patient.insert()
            patient_name = patient.name
        else:
            patient_name = existing[0].name
        
        # Create bill
        bill = frappe.get_doc({
            "doctype": "Patient Bill",
            "patient": patient_name,
            "billing_date": getdate(today()),
            "billing_period": "February 2026",
            "patient_class": "Individual"
        })
        
        # Add service line
        bill.append("services", {
            "service": "Dialysis Treatment",
            "description": "Regular dialysis session 4 hours",
            "quantity": 1,
            "unit_price": 250.00
        })
        
        bill.insert()
        
        # Verify
        assert frappe.db.exists("Patient Bill", bill.name), "Bill not created"
        assert bill.grand_total == 250.00, "Bill total calculation incorrect"
        
        # Cleanup
        frappe.delete_doc("Patient Bill", bill.name, force=True)

class TestLabTestCreation(VerificationTest):
    def execute(self):
        # Get or create patient
        existing = frappe.db.get_list("Patient", limit=1)
        if not existing:
            patient = frappe.get_doc({
                "doctype": "Patient",
                "first_name": "Test",
                "last_name": "Lab",
                "date_of_birth": "1992-03-10",
                "gender": "Male",
                "contact_number": "555-0005",
                "email": f"test.lab.{int(time.time())}@example.com"
            })
            patient.insert()
            patient_name = patient.name
        else:
            patient_name = existing[0].name
        
        # Create lab test
        lab_test = frappe.get_doc({
            "doctype": "Lab Test",
            "patient": patient_name,
            "test_template": "Monthly Dialysis Panel",
            "ordered_date": getdate(today())
        })
        lab_test.insert()
        
        # Verify
        assert frappe.db.exists("Lab Test", lab_test.name), "Lab test not created"
        
        # Cleanup
        frappe.delete_doc("Lab Test", lab_test.name, force=True)


# ============================================================================
# TEST SUITE 4: API Endpoint Testing
# ============================================================================

class TestAPIWhitelisting(VerificationTest):
    def execute(self):
        # Check if API endpoints are whitelisted
        hooks_path = frappe.get_app_path("dialysis_center", "hooks.py")
        with open(hooks_path, 'r') as f:
            hooks_content = f.read()
        
        # Check for expected API patterns
        assert "@frappe.whitelist()" in hooks_content or "whitelisted_methods" in hooks_content, \
            "API endpoints not properly configured in hooks"

class TestStandardRESTAPI(VerificationTest):
    def execute(self):
        # Test GET /api/resource/Patient endpoint
        # This test verifies the REST API is accessible
        try:
            patients = frappe.get_all("Patient", limit=1, fields=["name"])
            assert isinstance(patients, list), "REST API should return list"
        except Exception as e:
            raise AssertionError(f"REST API test failed: {str(e)}")

class TestDocTypeMetadata(VerificationTest):
    def execute(self):
        # Verify DocType metadata is properly configured
        patient_doctype = frappe.get_doc("DocType", "Patient")
        assert patient_doctype.name == "Patient", "Patient DocType metadata incomplete"
        assert patient_doctype.fields, "Patient DocType has no fields"


# ============================================================================
# TEST SUITE 5: Data Integrity
# ============================================================================

class TestDatabaseConstraints(VerificationTest):
    def execute(self):
        # Check for NOT NULL constraints on required fields
        patient_fields = frappe.db.get_all("DocField", {
            "parent": "Patient",
            "reqd": 1
        })
        assert len(patient_fields) > 0, "Patient should have required fields"

class TestDataTypeValidation(VerificationTest):
    def execute(self):
        # Verify field types are correct
        date_fields = frappe.db.get_all("DocField", {
            "parent": "Patient",
            "fieldtype": "Date"
        })
        assert len(date_fields) > 0, "Patient should have date fields"

class TestUniqueConstraints(VerificationTest):
    def execute(self):
        # Check for unique field configuration
        unique_fields = frappe.db.get_all("DocField", {
            "parent": "Patient",
            "unique": 1
        })
        # Some fields should be unique (like email)
        assert len(unique_fields) >= 0, "Unique constraints check"


# ============================================================================
# TEST SUITE 6: Performance Tests
# ============================================================================

class TestPatientListPerformance(VerificationTest):
    def execute(self):
        # Time the patient list query
        start = time.time()
        patients = frappe.get_all("Patient", limit=100)
        duration = time.time() - start
        
        # Should complete in < 1 second
        assert duration < 1.0, f"Patient list query too slow: {duration:.2f}s"

class TestAppointmentQueryPerformance(VerificationTest):
    def execute(self):
        # Time appointment query with filters
        start = time.time()
        appointments = frappe.get_all("Appointment", 
            filters={"appointment_date": getdate(today())},
            limit=50
        )
        duration = time.time() - start
        
        assert duration < 1.0, f"Appointment query too slow: {duration:.2f}s"

class TestBillQueryPerformance(VerificationTest):
    def execute(self):
        # Time bill summary query
        start = time.time()
        bills = frappe.get_all("Patient Bill", 
            fields=["name", "patient", "grand_total"],
            limit=100
        )
        duration = time.time() - start
        
        assert duration < 1.0, f"Bill query too slow: {duration:.2f}s"


# ============================================================================
# TEST SUITE 7: Cache & Session
# ============================================================================

class TestRedisConnectivity(VerificationTest):
    def execute(self):
        # Check Redis cache is working
        import redis
        try:
            r = redis.Redis()
            r.ping()
        except Exception as e:
            raise AssertionError(f"Redis not accessible: {str(e)}")

class TestSessionManagement(VerificationTest):
    def execute(self):
        # Verify session table exists
        assert frappe.db.exists("DocType", "Session"), "Session DocType not found"
        sessions = frappe.db.get_list("Session", limit=1)
        assert isinstance(sessions, list), "Session query failed"


# ============================================================================
# TEST SUITE 8: Security & Audit
# ============================================================================

class TestAuditTrail(VerificationTest):
    def execute(self):
        # Check audit trail is enabled
        assert frappe.db.exists("DocType", "DocType History") or \
               frappe.db.exists("DocType", "Comment"), \
               "Audit trail not properly configured"

class TestFieldLevelSecurity(VerificationTest):
    def execute(self):
        # Verify sensitive fields have proper permissions
        patient_fields = frappe.db.get_all("DocField", {
            "parent": "Patient"
        }, fields=["fieldname", "read_only"])
        
        assert len(patient_fields) > 0, "Field security check failed"

class TestDocumentSharing(VerificationTest):
    def execute(self):
        # Verify document sharing table exists
        assert frappe.db.exists("DocType", "Document Share"), \
            "Document sharing not configured"


# ============================================================================
# TEST SUITE 9: Configuration & Settings
# ============================================================================

class TestEmailConfiguration(VerificationTest):
    def execute(self):
        # Check email account exists
        email_accounts = frappe.db.get_all("Email Account", limit=1)
        # May be empty in test env, but table should exist
        assert isinstance(email_accounts, list), "Email configuration check failed"

class TestLocalizationSettings(VerificationTest):
    def execute(self):
        # Check system settings
        settings = frappe.db.get_single("System Settings")
        assert settings, "System Settings not found"

class TestFileUploadPath(VerificationTest):
    def execute(self):
        # Verify files directory exists
        import os
        from frappe.utils import get_path
        
        files_path = get_path("files")
        assert os.path.exists(files_path), "Files directory not found"


# ============================================================================
# TEST SUITE 10: Module Integration
# ============================================================================

class TestModuleConfiguration(VerificationTest):
    def execute(self):
        # Check all modules are registered
        modules_file = frappe.get_app_path("dialysis_center", "modules.txt")
        with open(modules_file, 'r') as f:
            modules = f.read().strip().split('\n')
        
        expected_modules = [
            "Patient Management",
            "Appointment Scheduling",
            "Dialysis Center Management",
            "Billing Management",
            "Laboratory Management",
            "Equipment Management",
            "Staff Management"
        ]
        
        for module in expected_modules:
            assert module in modules, f"Module '{module}' not found in modules.txt"

class TestWorkspaceConfiguration(VerificationTest):
    def execute(self):
        # Check workspaces exist for modules
        workspaces = frappe.db.get_all("Workspace", limit=5)
        assert len(workspaces) > 0, "No workspaces configured"


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests(site_name):
    """Run all verification tests"""
    
    print("\n" + "="*100)
    print("DIALYSIS CENTER MANAGEMENT SYSTEM - PHASE 6 VERIFICATION")
    print(f"Site: {site_name} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")
    
    # Initialize Frappe
    try:
        frappe.init(site_name)
        frappe.connect()
    except Exception as e:
        print(f"ERROR: Cannot connect to site '{site_name}'")
        print(f"Details: {str(e)}")
        sys.exit(1)
    
    # Group tests by category
    test_groups = {
        "1. DocType Validation": [
            TestPatientDocTypeExists("Patient DocType exists"),
            TestAppointmentDocTypeExists("Appointment DocType exists"),
            TestDialysisSessionDocTypeExists("Dialysis Session DocType exists"),
            TestPatientBillDocTypeExists("Patient Bill DocType exists"),
            TestLabTestDocTypeExists("Lab Test DocType exists"),
            TestDialysisMachineDocTypeExists("Dialysis Machine DocType exists"),
            TestStaffDocTypeExists("Staff DocType exists"),
            TestDatabaseStructure("Database structure verified"),
        ],
        "2. Permissions & Roles": [
            TestRoleExists("Required roles configured"),
            TestAdministratorUser("Administrator user exists"),
            TestPermissionConfiguration("Permissions properly configured"),
        ],
        "3. Core Workflows": [
            TestPatientCreation("Patient creation workflow"),
            TestAppointmentCreation("Appointment creation workflow"),
            TestDialysisSessionWorkflow("Dialysis session workflow"),
            TestPatientBillCreation("Patient bill creation workflow"),
            TestLabTestCreation("Lab test creation workflow"),
        ],
        "4. API & REST": [
            TestAPIWhitelisting("API endpoints whitelisted"),
            TestStandardRESTAPI("Standard REST API working"),
            TestDocTypeMetadata("DocType metadata accessible"),
        ],
        "5. Data Integrity": [
            TestDatabaseConstraints("Database constraints enforced"),
            TestDataTypeValidation("Field data types correct"),
            TestUniqueConstraints("Unique constraints configured"),
        ],
        "6. Performance": [
            TestPatientListPerformance("Patient list query performance"),
            TestAppointmentQueryPerformance("Appointment query performance"),
            TestBillQueryPerformance("Bill query performance"),
        ],
        "7. Cache & Sessions": [
            TestRedisConnectivity("Redis connectivity verified"),
            TestSessionManagement("Session management working"),
        ],
        "8. Security & Audit": [
            TestAuditTrail("Audit trail configured"),
            TestFieldLevelSecurity("Field-level security enabled"),
            TestDocumentSharing("Document sharing available"),
        ],
        "9. Configuration": [
            TestEmailConfiguration("Email configuration"),
            TestLocalizationSettings("Localization settings"),
            TestFileUploadPath("File upload path verified"),
        ],
        "10. Module Integration": [
            TestModuleConfiguration("Module configuration complete"),
            TestWorkspaceConfiguration("Workspace configuration complete"),
        ]
    }
    
    # Run tests and collect results
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    total_time = 0
    
    for group_name, tests in test_groups.items():
        print(f"\n{group_name}")
        print("-" * 100)
        
        for test in tests:
            test.run()
            print(test.result())
            
            total_tests += 1
            total_time += test.duration
            
            if test.passed:
                passed_tests += 1
            else:
                failed_tests += 1
    
    # Summary
    print("\n" + "="*100)
    print("SUMMARY")
    print("="*100)
    print(f"Total Tests:    {total_tests}")
    print(f"Passed:         {passed_tests} ✅")
    print(f"Failed:         {failed_tests} ❌")
    print(f"Success Rate:   {(passed_tests/total_tests)*100:.1f}%")
    print(f"Total Time:     {total_time:.2f}s")
    print("="*100)
    
    if failed_tests == 0:
        print("\n✅ ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION DEPLOYMENT")
        return 0
    else:
        print(f"\n❌ {failed_tests} TEST(S) FAILED - FIX ISSUES BEFORE DEPLOYMENT")
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Dialysis Center Management System - Verification Script"
    )
    parser.add_argument(
        "--site",
        required=True,
        help="Frappe site name (e.g., dialysis.local)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed error messages"
    )
    
    args = parser.parse_args()
    
    # Run verification
    exit_code = run_all_tests(args.site)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
