"""
API endpoint pour vérifier les événements synchronisés
Accessible via: /api/method/reunion.meeting_management.api.check_events.check
"""

import frappe


@frappe.whitelist()
def check():
	"""
	Vérifie combien d'événements Google Calendar ont été synchronisés
	"""
	try:
		# Compter les événements avec google_event_id
		events_with_google = frappe.db.count('Event', {
			'google_event_id': ['!=', '']
		})

		# Compter tous les événements
		total_events = frappe.db.count('Event')

		# Obtenir quelques exemples
		sample_events = frappe.db.get_all('Event',
			filters={'google_event_id': ['!=', '']},
			fields=['name', 'subject', 'starts_on', 'google_event_id', 'google_calendar_id'],
			limit=5
		)

		# Compter les tâches avec google_event_id
		tasks_with_google = frappe.db.count('Task', {
			'google_event_id': ['!=', '']
		})

		# Obtenir quelques exemples de tâches
		sample_tasks = frappe.db.get_all('Task',
			filters={'google_event_id': ['!=', '']},
			fields=['name', 'subject', 'exp_start_date', 'google_event_id', 'google_calendar_id'],
			limit=5
		)

		return {
			"success": True,
			"total_events": total_events,
			"events_with_google": events_with_google,
			"sample_events": sample_events,
			"total_tasks": frappe.db.count('Task'),
			"tasks_with_google": tasks_with_google,
			"sample_tasks": sample_tasks
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Check Events Error")
		return {
			"success": False,
			"message": str(e)
		}
