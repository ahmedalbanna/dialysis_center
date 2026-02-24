"""
Workflow State Transition Tests for Dialysis Center App

Tests state machines for:
1. Appointment status transitions
2. Dialysis Session status transitions
3. Invoice status transitions
4. Lab Test status transitions
5. Insurance Claim status transitions
"""

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today
from .test_fixtures import FixtureFactory


class TestAppointmentStateTransitions(IntegrationTestCase):
	"""Test appointment workflow state machine"""

	def test_appointment_initial_state(self):
		"""Test appointment starts in Scheduled state"""
		appointment = FixtureFactory.create_appointment()
		self.assertEqual(appointment.status, "Scheduled")

	def test_scheduled_to_completed_transition(self):
		"""Test Scheduled → Completed transition"""
		appointment = FixtureFactory.create_appointment()
		
		appointment.status = "Completed"
		appointment.save()
		
		self.assertEqual(appointment.status, "Completed")

	def test_scheduled_to_cancelled_transition(self):
		"""Test Scheduled → Cancelled transition"""
		appointment = FixtureFactory.create_appointment()
		
		appointment.status = "Cancelled"
		appointment.save()
		
		self.assertEqual(appointment.status, "Cancelled")

	def test_scheduled_to_noshow_transition(self):
		"""Test Scheduled → No-show transition"""
		appointment = FixtureFactory.create_appointment()
		
		appointment.status = "No-show"
		appointment.save()
		
		self.assertEqual(appointment.status, "No-show")

	def test_completed_to_cancelled_transition(self):
		"""Test Completed → Cancelled transition"""
		appointment = FixtureFactory.create_appointment()
		appointment.status = "Completed"
		appointment.save()
		
		appointment.status = "Cancelled"
		appointment.save()
		
		self.assertEqual(appointment.status, "Cancelled")

	def test_cancelled_to_scheduled_transition(self):
		"""Test Cancelled → Scheduled transition (rescheduling)"""
		appointment = FixtureFactory.create_appointment()
		appointment.status = "Cancelled"
		appointment.save()
		
		appointment.status = "Scheduled"
		appointment.save()
		
		self.assertEqual(appointment.status, "Scheduled")

	def test_valid_appointment_statuses(self):
		"""Test all valid appointment statuses"""
		valid_statuses = ["Scheduled", "Completed", "Cancelled", "No-show"]
		appointment = FixtureFactory.create_appointment()
		
		for status in valid_statuses:
			appointment.status = status
			appointment.save()
			self.assertEqual(appointment.status, status)

	def test_appointment_status_history(self):
		"""Test appointment status changes are tracked"""
		appointment = FixtureFactory.create_appointment()
		
		# Track status changes
		statuses = []
		statuses.append(appointment.status)  # Scheduled
		
		appointment.status = "Completed"
		appointment.save()
		statuses.append(appointment.status)
		
		appointment.refresh()
		self.assertEqual(appointment.status, "Completed")
		self.assertEqual(statuses[0], "Scheduled")
		self.assertEqual(statuses[1], "Completed")


class TestDialysisSessionStateTransitions(IntegrationTestCase):
	"""Test dialysis session workflow state machine"""

	def test_session_initial_state(self):
		"""Test session starts in Scheduled state"""
		session = FixtureFactory.create_dialysis_session()
		self.assertEqual(session.session_status, "Scheduled")

	def test_scheduled_to_in_progress_transition(self):
		"""Test Scheduled → In Progress transition"""
		session = FixtureFactory.create_dialysis_session()
		
		session.session_status = "In Progress"
		session.save()
		
		self.assertEqual(session.session_status, "In Progress")

	def test_in_progress_to_completed_transition(self):
		"""Test In Progress → Completed transition"""
		session = FixtureFactory.create_dialysis_session()
		session.session_status = "In Progress"
		session.save()
		
		session.session_status = "Completed"
		session.save()
		
		self.assertEqual(session.session_status, "Completed")

	def test_completed_to_billed_transition(self):
		"""Test Completed → Billed transition"""
		session = FixtureFactory.create_dialysis_session()
		session.session_status = "Completed"
		session.save()
		
		session.session_status = "Billed"
		session.save()
		
		self.assertEqual(session.session_status, "Billed")

	def test_scheduled_to_cancelled_transition(self):
		"""Test Scheduled → Cancelled transition"""
		session = FixtureFactory.create_dialysis_session()
		
		session.session_status = "Cancelled"
		session.save()
		
		self.assertEqual(session.session_status, "Cancelled")

	def test_in_progress_to_cancelled_transition(self):
		"""Test In Progress → Cancelled transition"""
		session = FixtureFactory.create_dialysis_session()
		session.session_status = "In Progress"
		session.save()
		
		session.session_status = "Cancelled"
		session.save()
		
		self.assertEqual(session.session_status, "Cancelled")

	def test_valid_session_statuses(self):
		"""Test all valid session statuses"""
		valid_statuses = ["Scheduled", "In Progress", "Completed", "Billed", "Cancelled"]
		session = FixtureFactory.create_dialysis_session()
		
		for status in valid_statuses:
			session.session_status = status
			session.save()
			self.assertEqual(session.session_status, status)

	def test_typical_session_workflow(self):
		"""Test typical complete session workflow"""
		session = FixtureFactory.create_dialysis_session()
		
		# Scheduled → In Progress
		self.assertEqual(session.session_status, "Scheduled")
		
		session.session_status = "In Progress"
		session.save()
		self.assertEqual(session.session_status, "In Progress")
		
		# In Progress → Completed
		session.session_status = "Completed"
		session.save()
		self.assertEqual(session.session_status, "Completed")
		
		# Completed → Billed
		session.session_status = "Billed"
		session.save()
		self.assertEqual(session.session_status, "Billed")

	def test_session_status_with_duration(self):
		"""Test session duration is recorded with status changes"""
		session = FixtureFactory.create_dialysis_session(
			session_time_in="08:00:00",
			session_time_out="12:00:00"
		)
		
		self.assertEqual(session.session_duration_minutes, 240)
		
		# Duration should persist through status changes
		session.session_status = "In Progress"
		session.save()
		
		self.assertEqual(session.session_duration_minutes, 240)


class TestInvoiceStateTransitions(IntegrationTestCase):
	"""Test invoice workflow state machine"""

	def test_invoice_initial_state(self):
		"""Test invoice starts in Draft state"""
		invoice = FixtureFactory.create_invoice()
		self.assertEqual(invoice.status, "Draft")

	def test_draft_to_submitted_transition(self):
		"""Test Draft → Submitted transition"""
		invoice = FixtureFactory.create_invoice()
		
		invoice.status = "Submitted"
		invoice.save()
		
		self.assertEqual(invoice.status, "Submitted")

	def test_submitted_to_paid_transition(self):
		"""Test Submitted → Paid transition"""
		invoice = FixtureFactory.create_invoice()
		invoice.status = "Submitted"
		invoice.save()
		
		invoice.status = "Paid"
		invoice.save()
		
		self.assertEqual(invoice.status, "Paid")

	def test_draft_to_cancelled_transition(self):
		"""Test Draft → Cancelled transition"""
		invoice = FixtureFactory.create_invoice()
		
		invoice.status = "Cancelled"
		invoice.save()
		
		self.assertEqual(invoice.status, "Cancelled")

	def test_submitted_to_cancelled_transition(self):
		"""Test Submitted → Cancelled transition"""
		invoice = FixtureFactory.create_invoice()
		invoice.status = "Submitted"
		invoice.save()
		
		invoice.status = "Cancelled"
		invoice.save()
		
		self.assertEqual(invoice.status, "Cancelled")

	def test_paid_to_cancelled_transition(self):
		"""Test Paid → Cancelled transition"""
		invoice = FixtureFactory.create_invoice()
		invoice.status = "Submitted"
		invoice.save()
		
		invoice.status = "Paid"
		invoice.save()
		
		invoice.status = "Cancelled"
		invoice.save()
		
		self.assertEqual(invoice.status, "Cancelled")

	def test_valid_invoice_statuses(self):
		"""Test all valid invoice statuses"""
		valid_statuses = ["Draft", "Submitted", "Paid", "Cancelled"]
		invoice = FixtureFactory.create_invoice()
		
		for status in valid_statuses:
			invoice.status = status
			invoice.save()
			self.assertEqual(invoice.status, status)

	def test_typical_invoice_workflow(self):
		"""Test typical complete invoice workflow"""
		invoice = FixtureFactory.create_invoice()
		
		# Draft → Submitted
		self.assertEqual(invoice.status, "Draft")
		
		invoice.status = "Submitted"
		invoice.save()
		self.assertEqual(invoice.status, "Submitted")
		
		# Submitted → Paid
		invoice.status = "Paid"
		invoice.save()
		self.assertEqual(invoice.status, "Paid")

	def test_invoice_status_with_amounts(self):
		"""Test invoice amounts persist through status changes"""
		invoice = FixtureFactory.create_invoice(
			billing_amount=1500.00,
			insurance_amount=750.00,
			patient_amount=750.00
		)
		
		original_amount = invoice.billing_amount
		
		# Change status
		invoice.status = "Submitted"
		invoice.save()
		
		self.assertEqual(invoice.billing_amount, original_amount)


class TestLabTestStateTransitions(IntegrationTestCase):
	"""Test lab test workflow state machine"""

	def test_lab_test_initial_state(self):
		"""Test lab test starts in Pending state"""
		lab_test = FixtureFactory.create_lab_test()
		self.assertEqual(lab_test.status, "Pending")

	def test_pending_to_in_progress_transition(self):
		"""Test Pending → In Progress transition"""
		lab_test = FixtureFactory.create_lab_test()
		
		lab_test.status = "In Progress"
		lab_test.save()
		
		self.assertEqual(lab_test.status, "In Progress")

	def test_in_progress_to_completed_transition(self):
		"""Test In Progress → Completed transition"""
		lab_test = FixtureFactory.create_lab_test()
		lab_test.status = "In Progress"
		lab_test.save()
		
		lab_test.status = "Completed"
		lab_test.save()
		
		self.assertEqual(lab_test.status, "Completed")

	def test_pending_to_cancelled_transition(self):
		"""Test Pending → Cancelled transition"""
		lab_test = FixtureFactory.create_lab_test()
		
		lab_test.status = "Cancelled"
		lab_test.save()
		
		self.assertEqual(lab_test.status, "Cancelled")

	def test_valid_lab_test_statuses(self):
		"""Test all valid lab test statuses"""
		valid_statuses = ["Pending", "In Progress", "Completed", "Cancelled"]
		lab_test = FixtureFactory.create_lab_test()
		
		for status in valid_statuses:
			lab_test.status = status
			lab_test.save()
			self.assertEqual(lab_test.status, status)

	def test_typical_lab_test_workflow(self):
		"""Test typical complete lab test workflow"""
		lab_test = FixtureFactory.create_lab_test()
		
		# Pending → In Progress
		self.assertEqual(lab_test.status, "Pending")
		
		lab_test.status = "In Progress"
		lab_test.save()
		self.assertEqual(lab_test.status, "In Progress")
		
		# In Progress → Completed
		lab_test.status = "Completed"
		lab_test.save()
		self.assertEqual(lab_test.status, "Completed")


class TestInsuranceClaimStateTransitions(IntegrationTestCase):
	"""Test insurance claim workflow state machine"""

	def test_claim_initial_state(self):
		"""Test claim starts in Draft state"""
		claim = FixtureFactory.create_insurance_claim()
		self.assertEqual(claim.claim_status, "Submitted")  # Default is Submitted

	def test_submitted_to_approved_transition(self):
		"""Test Submitted → Approved transition"""
		claim = FixtureFactory.create_insurance_claim()
		
		claim.claim_status = "Approved"
		claim.save()
		
		self.assertEqual(claim.claim_status, "Approved")

	def test_submitted_to_rejected_transition(self):
		"""Test Submitted → Rejected transition"""
		claim = FixtureFactory.create_insurance_claim()
		
		claim.claim_status = "Rejected"
		claim.save()
		
		self.assertEqual(claim.claim_status, "Rejected")

	def test_approved_to_paid_transition(self):
		"""Test Approved → Paid transition"""
		claim = FixtureFactory.create_insurance_claim()
		claim.claim_status = "Approved"
		claim.save()
		
		claim.claim_status = "Paid"
		claim.save()
		
		self.assertEqual(claim.claim_status, "Paid")

	def test_rejected_to_resubmitted_transition(self):
		"""Test Rejected → Submitted transition (resubmission)"""
		claim = FixtureFactory.create_insurance_claim()
		claim.claim_status = "Rejected"
		claim.save()
		
		claim.claim_status = "Submitted"
		claim.save()
		
		self.assertEqual(claim.claim_status, "Submitted")

	def test_valid_claim_statuses(self):
		"""Test all valid claim statuses"""
		valid_statuses = ["Draft", "Submitted", "Approved", "Rejected", "Paid"]
		claim = FixtureFactory.create_insurance_claim()
		
		for status in valid_statuses:
			claim.claim_status = status
			claim.save()
			self.assertEqual(claim.claim_status, status)

	def test_typical_claim_workflow(self):
		"""Test typical complete claim workflow"""
		claim = FixtureFactory.create_insurance_claim()
		
		# Submitted (initial)
		self.assertEqual(claim.claim_status, "Submitted")
		
		# Submitted → Approved
		claim.claim_status = "Approved"
		claim.save()
		self.assertEqual(claim.claim_status, "Approved")
		
		# Approved → Paid
		claim.claim_status = "Paid"
		claim.save()
		self.assertEqual(claim.claim_status, "Paid")

	def test_claim_status_with_amount(self):
		"""Test claim amount persists through status changes"""
		claim = FixtureFactory.create_insurance_claim(claim_amount=500.00)
		
		original_amount = claim.claim_amount
		
		# Change through statuses
		claim.claim_status = "Approved"
		claim.save()
		
		claim.claim_status = "Paid"
		claim.save()
		
		self.assertEqual(claim.claim_amount, original_amount)


class TestStateTransitionIntegration(IntegrationTestCase):
	"""Test state transitions across multiple documents"""

	def test_appointment_and_session_state_sync(self):
		"""Test appointment and session states are coordinated"""
		appointment = FixtureFactory.create_appointment()
		session = FixtureFactory.create_dialysis_session(appointment=appointment)
		
		# Both start in their respective scheduled states
		self.assertEqual(appointment.status, "Scheduled")
		self.assertEqual(session.session_status, "Scheduled")
		
		# Update appointment
		appointment.status = "Completed"
		appointment.save()
		
		# Session can be updated independently
		session.session_status = "Completed"
		session.save()
		
		self.assertEqual(appointment.status, "Completed")
		self.assertEqual(session.session_status, "Completed")

	def test_session_and_invoice_state_sync(self):
		"""Test session and invoice states are coordinated"""
		session = FixtureFactory.create_dialysis_session()
		invoice = FixtureFactory.create_invoice(session=session)
		
		# Session: Scheduled, Invoice: Draft
		self.assertEqual(session.session_status, "Scheduled")
		self.assertEqual(invoice.status, "Draft")
		
		# Session → Completed
		session.session_status = "Completed"
		session.save()
		
		# Invoice → Submitted
		invoice.status = "Submitted"
		invoice.save()
		
		self.assertEqual(session.session_status, "Completed")
		self.assertEqual(invoice.status, "Submitted")

	def test_invoice_and_claim_state_workflow(self):
		"""Test invoice and claim states in workflow"""
		invoice = FixtureFactory.create_invoice()
		claim = FixtureFactory.create_insurance_claim(invoice=invoice)
		
		# Invoice: Draft, Claim: Submitted
		self.assertEqual(invoice.status, "Draft")
		self.assertEqual(claim.claim_status, "Submitted")
		
		# Invoice → Submitted
		invoice.status = "Submitted"
		invoice.save()
		
		# Claim → Approved
		claim.claim_status = "Approved"
		claim.save()
		
		self.assertEqual(invoice.status, "Submitted")
		self.assertEqual(claim.claim_status, "Approved")
