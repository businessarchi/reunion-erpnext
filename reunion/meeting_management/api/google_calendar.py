# Copyright (c) 2025, Business Architecte and contributors
# For license information, please see license.txt

"""
API pour la synchronisation avec Google Calendar
"""

import frappe
from frappe import _
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from reunion.meeting_management.api.google_auth import get_credentials


@frappe.whitelist()
def get_calendar_info():
	"""
	Récupère les informations du calendrier Google connecté

	Returns:
		dict: {"success": bool, "calendar": dict, "message": str}
	"""
	try:
		credentials = get_credentials()

		if not credentials:
			return {
				"success": False,
				"message": _("Non connecté à Google Calendar")
			}

		# Construire le service Google Calendar API
		service = build('calendar', 'v3', credentials=credentials)

		# Récupérer les infos du calendrier
		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")
		calendar_id = settings.calendar_id or "primary"

		# Obtenir les détails du calendrier
		calendar = service.calendars().get(calendarId=calendar_id).execute()

		return {
			"success": True,
			"calendar": {
				"id": calendar.get("id"),
				"summary": calendar.get("summary"),
				"description": calendar.get("description"),
				"timeZone": calendar.get("timeZone"),
				"is_primary": calendar_id == "primary"
			}
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google Calendar - Get Calendar Info Error")
		return {
			"success": False,
			"message": str(e)
		}


@frappe.whitelist()
def list_calendars():
	"""
	Liste tous les calendriers Google disponibles pour l'utilisateur

	Returns:
		dict: {"success": bool, "calendars": list, "message": str}
	"""
	try:
		credentials = get_credentials()

		if not credentials:
			return {
				"success": False,
				"message": _("Non connecté à Google Calendar")
			}

		# Construire le service Google Calendar API
		service = build('calendar', 'v3', credentials=credentials)

		# Lister tous les calendriers
		calendar_list = service.calendarList().list().execute()

		calendars = []
		for calendar in calendar_list.get('items', []):
			calendars.append({
				"id": calendar.get("id"),
				"summary": calendar.get("summary"),
				"description": calendar.get("description", ""),
				"primary": calendar.get("primary", False),
				"access_role": calendar.get("accessRole"),
				"backgroundColor": calendar.get("backgroundColor")
			})

		return {
			"success": True,
			"calendars": calendars,
			"count": len(calendars)
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google Calendar - List Calendars Error")
		return {
			"success": False,
			"message": str(e)
		}


@frappe.whitelist()
def sync_from_google():
	"""
	Importe les événements de Google Calendar vers ERPNext

	Returns:
		dict: {"success": bool, "events_synced": int, "message": str}
	"""
	try:
		credentials = get_credentials()

		if not credentials:
			return {
				"success": False,
				"message": _("Non connecté à Google Calendar")
			}

		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")

		if not settings.sync_from_google:
			return {
				"success": False,
				"message": _("La synchronisation depuis Google est désactivée")
			}

		# Construire le service Google Calendar API
		service = build('calendar', 'v3', credentials=credentials)

		# Récupérer les événements des 30 derniers jours
		now = datetime.utcnow()
		time_min = (now - timedelta(days=30)).isoformat() + 'Z'
		time_max = (now + timedelta(days=90)).isoformat() + 'Z'

		calendar_id = settings.calendar_id or "primary"

		events_result = service.events().list(
			calendarId=calendar_id,
			timeMin=time_min,
			timeMax=time_max,
			maxResults=100,
			singleEvents=True,
			orderBy='startTime'
		).execute()

		events = events_result.get('items', [])
		events_synced = 0

		# TODO: Créer les événements dans ERPNext
		# Cela nécessitera le doctype Meeting/Réunion
		for event in events:
			# Pour l'instant, on compte juste les événements
			events_synced += 1

		# Mettre à jour la date de dernière synchronisation
		settings.last_sync = datetime.now()
		settings.sync_status = "Connecté"
		settings.save(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"events_synced": events_synced,
			"message": _("{0} événements trouvés dans Google Calendar").format(events_synced)
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google Calendar - Sync From Google Error")

		# Marquer comme erreur
		try:
			settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")
			settings.sync_status = "Erreur"
			settings.save(ignore_permissions=True)
			frappe.db.commit()
		except:
			pass

		return {
			"success": False,
			"message": str(e)
		}


@frappe.whitelist()
def sync_to_google(meeting_name):
	"""
	Exporte une réunion ERPNext vers Google Calendar

	Args:
		meeting_name: Nom du document Meeting

	Returns:
		dict: {"success": bool, "event_id": str, "message": str}
	"""
	try:
		credentials = get_credentials()

		if not credentials:
			return {
				"success": False,
				"message": _("Non connecté à Google Calendar")
			}

		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")

		if not settings.sync_to_google:
			return {
				"success": False,
				"message": _("La synchronisation vers Google est désactivée")
			}

		# TODO: Récupérer le document Meeting et créer l'événement dans Google Calendar
		# Cela nécessitera le doctype Meeting/Réunion

		return {
			"success": False,
			"message": _("Fonction non encore implémentée - En attente du doctype Meeting")
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google Calendar - Sync To Google Error")
		return {
			"success": False,
			"message": str(e)
		}
