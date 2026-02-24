import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, time_diff_in_seconds, getdate, flt
from frappe import _

class DialysisSession(Document):
	def validate(self):
		self.validate_patient_and_machine()
		self.validate_session_date()
		self.validate_duration_constraints()
		self.validate_weights()
		self.validate_vital_signs()
		self.calculate_weight_loss()
		self.calculate_uf_rate()
		self.validate_treatment_metrics()
		self.set_status()
	
	def validate_patient_and_machine(self):
		"""Validate patient exists and is active"""
		if self.patient:
			patient = frappe.get_doc("Patient", self.patient)
			if patient.status != "Active":
				frappe.throw(_("Cannot create session for inactive patient: {0}").format(self.patient))
		
		"""Validate machine availability"""
		if self.dialysis_machine and self.session_date:
			# Check if machine is already scheduled for overlapping time
			overlapping = frappe.db.exists("Dialysis Session", {
				"dialysis_machine": self.dialysis_machine,
				"session_date": self.session_date,
				"name": ["!=", self.name],
				"docstatus": ["<", 2]  # Not cancelled
			})
			if overlapping:
				frappe.throw(_("Machine {0} is already scheduled for {1}").format(
					self.dialysis_machine, self.session_date))
	
	def validate_session_date(self):
		"""Validate session date is not in future"""
		if self.session_date:
			if getdate(self.session_date) > getdate():
				frappe.throw(_("Session date cannot be in the future"))
	
	def validate_duration_constraints(self):
		"""Validate treatment duration is within acceptable range"""
		if self.treatment_duration:
			# Standard dialysis duration is 3-5 hours (180-300 minutes)
			if flt(self.treatment_duration) < 120:
				frappe.msgprint(_("Warning: Treatment duration less than 2 hours"), 
					indicator="orange", alert=True)
			if flt(self.treatment_duration) > 360:
				frappe.msgprint(_("Warning: Treatment duration exceeds 6 hours"), 
					indicator="orange", alert=True)
	
	def validate_treatment_metrics(self):
		"""Validate treatment adequacy metrics if available"""
		# Kt/V should ideally be >= 1.2 for adequate dialysis
		if self.ktv and flt(self.ktv) < 1.2:
			frappe.msgprint(_("Warning: Kt/V value {0} is below recommended level of 1.2").format(self.ktv),
				indicator="orange", alert=True)
		
		# URR (Urea Reduction Ratio) should ideally be >= 65%
		if self.urr and flt(self.urr) < 65:
			frappe.msgprint(_("Warning: URR value {0}% is below recommended level of 65%").format(self.urr),
				indicator="orange", alert=True)
	
	def validate_weights(self):
		"""Validate weight measurements"""
		if self.pre_dialysis_weight and self.pre_dialysis_weight <= 0:
			frappe.throw(_("Pre-dialysis weight must be greater than 0"))
		
		if self.post_dialysis_weight and self.post_dialysis_weight <= 0:
			frappe.throw(_("Post-dialysis weight must be greater than 0"))
		
		if self.pre_dialysis_weight and self.post_dialysis_weight:
			if self.post_dialysis_weight > self.pre_dialysis_weight:
				frappe.msgprint(_("Warning: Post-dialysis weight is greater than pre-dialysis weight"), 
					indicator="orange", alert=True)
			
			# Check for excessive weight loss (>5% body weight)
			weight_loss = self.pre_dialysis_weight - self.post_dialysis_weight
			weight_loss_pct = (weight_loss / self.pre_dialysis_weight) * 100
			if weight_loss_pct > 5:
				frappe.msgprint(_("Warning: Weight loss exceeds 5% of body weight ({0}%)").format(
					round(weight_loss_pct, 2)), indicator="red", alert=True)
	
	def validate_vital_signs(self):
		"""Validate vital signs are within acceptable ranges"""
		# Pre-dialysis BP validation
		if self.pre_systolic_bp and self.pre_diastolic_bp:
			if self.pre_systolic_bp < self.pre_diastolic_bp:
				frappe.throw(_("Pre-dialysis systolic BP cannot be less than diastolic BP"))
			
			# Check for hypertension crisis (BP > 180/120)
			if self.pre_systolic_bp > 180 or self.pre_diastolic_bp > 120:
				frappe.msgprint(_("Critical: Pre-dialysis BP indicates hypertensive crisis"), 
					indicator="red", alert=True)
		
		# Post-dialysis BP validation
		if self.post_systolic_bp and self.post_diastolic_bp:
			if self.post_systolic_bp < self.post_diastolic_bp:
				frappe.throw(_("Post-dialysis systolic BP cannot be less than diastolic BP"))
			
			# Check for hypotension (BP < 90/60)
			if self.post_systolic_bp < 90 or self.post_diastolic_bp < 60:
				frappe.msgprint(_("Warning: Post-dialysis BP indicates hypotension"), 
					indicator="orange", alert=True)
	
	def calculate_weight_loss(self):
		"""Calculate actual weight loss"""
		if self.pre_dialysis_weight and self.post_dialysis_weight:
			self.weight_loss = flt(self.pre_dialysis_weight - self.post_dialysis_weight, 2)
	
	def calculate_uf_rate(self):
		"""Calculate ultrafiltration rate"""
		if self.weight_loss and self.actual_duration and self.actual_duration > 0:
			# UF rate in ml/hour (1 kg = 1000 ml)
			self.uf_rate = flt((self.weight_loss * 1000) / (self.actual_duration / 60.0), 2)
	
	def set_status(self):
		"""Auto-set status based on fields"""
		if not self.status:
			if self.started_at and not self.completed_at:
				self.status = "In Progress"
			elif self.completed_at:
				self.status = "Completed"
			else:
				self.status = "Scheduled"
	
	def before_save(self):
		"""Data preparation before saving"""
		# Trim whitespace from notes
		if self.notes:
			self.notes = self.notes.strip()
		
		# Calculate weight loss if not already set
		if self.pre_dialysis_weight and self.post_dialysis_weight and not self.weight_loss:
			self.calculate_weight_loss()
		
		# Calculate UF rate if not already set
		if self.weight_loss and self.actual_duration and not self.uf_rate:
			self.calculate_uf_rate()
	
	def before_submit(self):
		"""Validate completion before submit"""
		if not self.completed_at:
			self.completed_at = now_datetime()
		
		if self.started_at and self.completed_at:
			duration_seconds = time_diff_in_seconds(self.completed_at, self.started_at)
			self.actual_duration = int(duration_seconds / 60)
		
		# Ensure critical fields are filled
		if not self.post_dialysis_weight:
			frappe.throw(_("Post-dialysis weight is required before submitting session"))
		
		if not self.post_systolic_bp or not self.post_diastolic_bp:
			frappe.throw(_("Post-dialysis vital signs are required before submitting session"))
		
		# Recalculate final values
		self.calculate_weight_loss()
		self.calculate_uf_rate()
		self.status = "Completed"
	
	def on_submit(self):
		"""Update machine utilization and create vital signs log"""
		self.update_machine_utilization()
		self.create_vital_signs_log()
		self.recalculate_treatment_metrics()
	
	def recalculate_treatment_metrics(self):
		"""Recalculate Kt/V and URR values on submission"""
		# These would typically be calculated based on pre/post lab values
		# Placeholder for future integration with lab results
		try:
			# Kt/V = (pre_urea - post_urea) / pre_urea * 100 (simplified)
			# URR = (pre_urea - post_urea) / pre_urea * 100
			# These would use actual lab values from related lab tests
			pass
		except Exception as e:
			frappe.log_error(message=str(e), title="Treatment Metrics Calculation Failed")
	
	def update_machine_utilization(self):
		"""Update machine statistics"""
		if self.dialysis_machine:
			machine = frappe.get_doc("Dialysis Machine", self.dialysis_machine)
			machine.total_sessions = (machine.total_sessions or 0) + 1
			if self.actual_duration:
				machine.total_hours_used = (machine.total_hours_used or 0) + (self.actual_duration / 60.0)
			machine.last_used_date = self.session_date
			machine.save(ignore_permissions=True)
	
	def create_vital_signs_log(self):
		"""Create vital signs log entry"""
		if self.post_systolic_bp and self.post_diastolic_bp:
			vital_log = frappe.get_doc({
				"doctype": "Vital Signs Log",
				"patient": self.patient,
				"recorded_at": self.completed_at or now_datetime(),
				"systolic_bp": self.post_systolic_bp,
				"diastolic_bp": self.post_diastolic_bp,
				"pulse_rate": self.post_pulse_rate,
				"temperature": self.post_temperature,
				"weight": self.post_dialysis_weight,
				"source_doctype": "Dialysis Session",
				"source_name": self.name
			})
			vital_log.insert(ignore_permissions=True)
	
	def on_update(self):
		"""Called after saving - update related records"""
		# Clear caches for performance
		frappe.cache.delete_value(f"session_{self.name}")
		frappe.cache.delete_value(f"patient_{self.patient}_latest_session")
		
		# Update patient's last session date if submitted
		if self.docstatus == 1 and self.patient:
			frappe.db.set_value("Patient", self.patient, "last_session_date", self.session_date)
	
	def on_cancel(self):
		"""Reverse machine utilization on cancel"""
		if self.dialysis_machine:
			machine = frappe.get_doc("Dialysis Machine", self.dialysis_machine)
			machine.total_sessions = max((machine.total_sessions or 0) - 1, 0)
			if self.actual_duration:
				machine.total_hours_used = max((machine.total_hours_used or 0) - (self.actual_duration / 60.0), 0)
			machine.save(ignore_permissions=True)
		
		# Clear related caches
		frappe.cache.delete_value(f"session_{self.name}")
		frappe.cache.delete_value(f"patient_{self.patient}_latest_session")
