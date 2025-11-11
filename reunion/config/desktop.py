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
			"module_name": "Gestion Réunions",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Gestion Réunions")
		}
	]
