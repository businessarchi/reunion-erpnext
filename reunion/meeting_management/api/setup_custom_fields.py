"""
API endpoint pour ajouter les custom fields Google Calendar
Accessible via: /api/method/reunion.meeting_management.api.setup_custom_fields.setup
"""

import frappe


@frappe.whitelist()
def setup():
	"""
	Ajoute les custom fields pour Google Calendar sync
	Peut être appelé depuis l'interface ERPNext
	"""
	try:
		from reunion.meeting_management.api.add_google_calendar_fields import add_custom_fields
		add_custom_fields()

		return {
			"success": True,
			"message": "Custom fields créés avec succès ! Vous pouvez maintenant synchroniser vos calendriers."
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Setup Custom Fields Error")
		return {
			"success": False,
			"message": str(e)
		}
