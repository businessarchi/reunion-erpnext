"""
Utility functions for Frappe App
"""

import frappe


def get_app_version():
	"""Get the current app version"""
	from reunion import __version__
	return __version__


# Example whitelisted API method
@frappe.whitelist()
def ping():
	"""
	Test API endpoint
	Usage: frappe.call('frappe_app.utils.ping')
	"""
	return "pong"


# Example Jinja filter
def currency_in_words(amount):
	"""
	Convert currency amount to words
	Usage in Jinja: {{ amount | currency_in_words }}
	"""
	# Implementation here
	return str(amount)
