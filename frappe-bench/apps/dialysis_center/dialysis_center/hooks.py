from . import __version__ as app_version

app_name = "dialysis_center"
app_title = "Dialysis Center"
app_publisher = "Ahmed Albanna"
app_description = "Dialysis Center Management System"
app_email = "ahmed@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
	"/assets/dialysis_center/css/dialysis_center.css",
	"/assets/dialysis_center/css/responsive_design.css",
]
app_include_js = [
	"hot-reload.bundle.js",
	"/assets/dialysis_center/dist/js/utils.bundle.js",
	"/assets/dialysis_center/dist/js/components.bundle.js",
	"/assets/dialysis_center/dist/js/dashboard.bundle.js",
	"/assets/dialysis_center/dist/js/realtime.bundle.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/dialysis_center/css/dialysis_center.css"
# web_include_js = "/assets/dialysis_center/js/dialysis_center.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dialysis_center/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Patient": "public/js/patient_enhanced.js",
	"Dialysis Session": "public/js/session_realtime.js",
	"Appointment": "public/js/appointment_enhanced.js",
	"Invoice": "public/js/invoice.js",
	"Lab Test": "public/js/lab_test.js",
	"Staff": "public/js/staff.js",
	"Dialysis Machine": "public/js/dialysis_machine.js",
	"Medication": "public/js/medication.js",
}
