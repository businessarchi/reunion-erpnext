# Copyright (c) 2025, Business Architecte and contributors
# For license information, please see license.txt

"""
API pour la synchronisation avec Google Calendar
"""

import frappe
from frappe import _
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser
from reunion.meeting_management.api.google_auth import get_credentials


@frappe.whitelist()
def get_calendar_info():
	"""
	Récupère les informations du calendrier Google connecté

	Returns:
		dict: {"success": bool, "calendar": dict, "message": str}
	"""
	try:
		frappe.logger().info("get_calendar_info called")
		credentials = get_credentials()

		frappe.logger().info(f"get_calendar_info - credentials: {credentials is not None}")

		if not credentials:
			frappe.log_error("No credentials returned from get_credentials()", "Google Calendar - No Credentials")
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
		frappe.logger().info("list_calendars called")
		credentials = get_credentials()

		frappe.logger().info(f"list_calendars - credentials: {credentials is not None}")

		if not credentials:
			frappe.log_error("No credentials returned from get_credentials()", "Google Calendar - No Credentials List")
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
	Synchronise tous les calendriers configurés vers leurs DocTypes respectifs (Event ou Task)

	Returns:
		dict: {"success": bool, "events_synced": int, "tasks_synced": int, "message": str}
	"""
	try:
		credentials = get_credentials()

		if not credentials:
			return {
				"success": False,
				"message": _("Non connecté à Google Calendar")
			}

		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")

		# Vérifier qu'il y a des calendriers configurés
		if not settings.calendars_to_sync:
			return {
				"success": False,
				"message": _("Aucun calendrier configuré. Cliquez sur 'Charger les calendriers' d'abord.")
			}

		# Construire le service Google Calendar API
		service = build('calendar', 'v3', credentials=credentials)

		# Récupérer les événements des 30 derniers jours et 90 jours à venir
		now = datetime.utcnow()
		time_min = (now - timedelta(days=30)).isoformat() + 'Z'
		time_max = (now + timedelta(days=90)).isoformat() + 'Z'

		total_events_synced = 0
		total_tasks_synced = 0
		calendars_processed = 0

		# Parcourir chaque calendrier configuré
		for cal_config in settings.calendars_to_sync:
			if not cal_config.enabled:
				continue

			try:
				# Récupérer les événements de ce calendrier
				events_result = service.events().list(
					calendarId=cal_config.calendar_id,
					timeMin=time_min,
					timeMax=time_max,
					maxResults=100,
					singleEvents=True,
					orderBy='startTime'
				).execute()

				events = events_result.get('items', [])

				# Synchroniser chaque événement vers le DocType configuré
				for event in events:
					try:
						if cal_config.sync_to_doctype == "Event":
							sync_event_to_erpnext(event, cal_config.calendar_id)
							total_events_synced += 1
						elif cal_config.sync_to_doctype == "Task":
							sync_event_to_task(event, cal_config.calendar_id)
							total_tasks_synced += 1
					except Exception as e:
						# Log mais ne pas arrêter la synchronisation
						frappe.log_error(
							f"Error syncing event {event.get('id', 'unknown')}: {str(e)}\n{frappe.get_traceback()}",
							f"Google Calendar - Sync Single Event Error"
						)

				calendars_processed += 1

			except Exception as e:
				frappe.log_error(
					frappe.get_traceback(),
					f"Google Calendar - Sync Error for {cal_config.calendar_id}"
				)
				# Continue avec les autres calendriers même si un échoue
				continue

		# Mettre à jour la date de dernière synchronisation
		settings.last_sync = datetime.now()
		settings.sync_status = "Connecté"
		settings.save(ignore_permissions=True)
		frappe.db.commit()

		message_parts = []
		if total_events_synced > 0:
			message_parts.append(f"{total_events_synced} événement(s)")
		if total_tasks_synced > 0:
			message_parts.append(f"{total_tasks_synced} tâche(s)")

		message = _("Synchronisation réussie: {0} depuis {1} calendrier(s)").format(
			" et ".join(message_parts) if message_parts else "0 éléments",
			calendars_processed
		)

		return {
			"success": True,
			"events_synced": total_events_synced,
			"tasks_synced": total_tasks_synced,
			"calendars_processed": calendars_processed,
			"message": message
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


def sync_event_to_erpnext(google_event, calendar_id):
	"""
	Synchronise un événement Google Calendar vers le DocType Event d'ERPNext

	Args:
		google_event: Événement Google Calendar (dict)
		calendar_id: ID du calendrier source
	"""
	# Extraire les données de l'événement Google
	google_event_id = google_event.get('id')
	summary = google_event.get('summary', 'Sans titre')[:140]  # Limiter à 140 caractères
	description = google_event.get('description', '')[:5000]  # Limiter à 5000 caractères
	location = google_event.get('location', '')[:140]

	# Gérer les dates (événements all-day vs avec heure)
	start = google_event.get('start', {})
	end = google_event.get('end', {})

	if 'dateTime' in start:
		# Parser les dates ISO 8601 avec timezone et convertir en format MySQL
		start_dt = dateutil_parser.parse(start['dateTime'])
		end_dt = dateutil_parser.parse(end['dateTime'])

		# Convertir au format MySQL (YYYY-MM-DD HH:MM:SS)
		starts_on = start_dt.strftime('%Y-%m-%d %H:%M:%S')
		ends_on = end_dt.strftime('%Y-%m-%d %H:%M:%S')
		all_day = 0
	else:
		# Événements all-day (date uniquement)
		starts_on = start['date'] + ' 00:00:00'
		ends_on = end['date'] + ' 23:59:59'
		all_day = 1

	# Vérifier si l'événement existe déjà (par google_event_id)
	existing = frappe.db.exists('Event', {
		'google_event_id': google_event_id,
		'google_calendar_id': calendar_id
	})

	if existing:
		# Mettre à jour l'événement existant
		event_doc = frappe.get_doc('Event', existing)
		event_doc.subject = summary
		event_doc.description = description
		event_doc.location = location
		event_doc.starts_on = starts_on
		event_doc.ends_on = ends_on
		event_doc.all_day = all_day
		event_doc.save(ignore_permissions=True)
	else:
		# Créer un nouvel événement
		event_doc = frappe.get_doc({
			'doctype': 'Event',
			'subject': summary,
			'description': description,
			'location': location,
			'starts_on': starts_on,
			'ends_on': ends_on,
			'all_day': all_day,
			'google_event_id': google_event_id,
			'google_calendar_id': calendar_id,
			'event_type': 'Public',  # Par défaut
			'status': 'Open'
		})
		event_doc.insert(ignore_permissions=True)

	frappe.db.commit()


def sync_event_to_task(google_event, calendar_id):
	"""
	Synchronise un événement Google Calendar vers le DocType Task d'ERPNext

	Args:
		google_event: Événement Google Calendar (dict)
		calendar_id: ID du calendrier source
	"""
	# Extraire les données de l'événement Google
	google_event_id = google_event.get('id')
	summary = google_event.get('summary', 'Sans titre')[:140]  # Limiter à 140 caractères
	description = google_event.get('description', '')[:5000]  # Limiter à 5000 caractères

	# Gérer les dates
	start = google_event.get('start', {})
	end = google_event.get('end', {})

	if 'dateTime' in start:
		exp_start_date = start['dateTime'].split('T')[0]
		exp_end_date = end['dateTime'].split('T')[0]
	else:
		exp_start_date = start['date']
		exp_end_date = end['date']

	# Vérifier si la tâche existe déjà
	existing = frappe.db.exists('Task', {
		'google_event_id': google_event_id,
		'google_calendar_id': calendar_id
	})

	if existing:
		# Mettre à jour la tâche existante
		task_doc = frappe.get_doc('Task', existing)
		task_doc.subject = summary
		task_doc.description = description
		task_doc.exp_start_date = exp_start_date
		task_doc.exp_end_date = exp_end_date
		task_doc.save(ignore_permissions=True)
	else:
		# Créer une nouvelle tâche
		task_doc = frappe.get_doc({
			'doctype': 'Task',
			'subject': summary,
			'description': description,
			'exp_start_date': exp_start_date,
			'exp_end_date': exp_end_date,
			'google_event_id': google_event_id,
			'google_calendar_id': calendar_id,
			'status': 'Open'
		})
		task_doc.insert(ignore_permissions=True)

	frappe.db.commit()


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
