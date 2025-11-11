"""
Desktop configuration for Frappe App
"""

from frappe import _


def get_data():
	"""
	Return desktop icons configuration
	"""
	return [
		{
			"module_name": "Frappe App",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Frappe App")
		}
	]
