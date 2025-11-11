"""
Example Web Page Controller
URL: http://yoursite.local/example-page
"""

import frappe

def get_context(context):
	"""
	This function is called when the page is rendered.
	It should return a context dictionary with data for the template.
	"""
	context.no_cache = 1  # Don't cache this page
	context.show_sidebar = True

	# Page metadata
	context.title = "Example Page"
	context.description = "This is an example web page"

	# Fetch data from database
	context.items = frappe.get_all(
		"Sample Doctype",
		filters={"status": "Active"},
		fields=["name", "title", "description"],
		limit=10
	)

	# Add custom data
	context.custom_data = {
		"total_count": len(context.items),
		"page_info": "This page demonstrates how to create web pages in Frappe"
	}

	# You can also check permissions
	if frappe.session.user != "Guest":
		context.user_email = frappe.session.user

	return context
