import frappe
from frappe import _
import json

def get_context(context):
    """Page de diagnostic pour trouver l'intégration Google Calendar"""
    context.no_cache = 1
    context.show_sidebar = False

    # Vérifier les permissions
    if not frappe.has_permission("Event", "read"):
        context.error = "Permissions insuffisantes"
        return context

    results = {}

    # 1. Chercher les doctypes liés à Google Calendar
    try:
        # Vérifier si Google Calendar doctype existe
        if frappe.db.exists("DocType", "Google Calendar"):
            google_cal_doc = frappe.get_doc("Google Calendar", "Google Calendar")
            results["google_calendar_doctype"] = {
                "exists": True,
                "fields": [f.fieldname for f in google_cal_doc.fields]
            }
        else:
            results["google_calendar_doctype"] = {"exists": False}
    except:
        results["google_calendar_doctype"] = {"exists": False, "error": True}

    # 2. Vérifier les paramètres dans Google Settings
    try:
        google_settings = frappe.get_doc("Google Settings", "Google Settings")
        results["google_settings"] = {
            "enable": google_settings.enable,
            "has_credentials": bool(google_settings.client_id and google_settings.client_secret),
            "fields": list(google_settings.as_dict().keys())
        }
    except Exception as e:
        results["google_settings"] = {"error": str(e)}

    # 3. Chercher les Events avec des infos Google
    try:
        events_with_google = frappe.db.sql("""
            SELECT name, subject, creation
            FROM `tabEvent`
            ORDER BY creation DESC
            LIMIT 10
        """, as_dict=True)

        results["recent_events"] = events_with_google

        # Vérifier les champs d'un Event
        if events_with_google:
            event_doc = frappe.get_doc("Event", events_with_google[0].name)
            event_fields = event_doc.as_dict()

            # Chercher les champs liés à Google
            google_fields = {k: v for k, v in event_fields.items()
                           if k and ('google' in str(k).lower() or 'calendar' in str(k).lower())}

            results["event_google_fields"] = google_fields
    except Exception as e:
        results["recent_events"] = {"error": str(e)}

    # 4. Chercher les méthodes whitelisted liées à calendar
    try:
        # Utiliser l'API Google directement
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        # Essayer de récupérer les credentials
        google_settings = frappe.get_doc("Google Settings", "Google Settings")

        if google_settings.get("access_token"):
            results["google_oauth"] = {
                "status": "Tokens présents",
                "has_access_token": True,
                "has_refresh_token": bool(google_settings.get("refresh_token"))
            }

            # Essayer de lister les calendriers
            try:
                creds = Credentials(
                    token=google_settings.get("access_token"),
                    refresh_token=google_settings.get("refresh_token"),
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=google_settings.client_id,
                    client_secret=google_settings.get_password("client_secret")
                )

                service = build('calendar', 'v3', credentials=creds)
                calendar_list = service.calendarList().list().execute()

                results["google_calendars"] = {
                    "success": True,
                    "calendars": [
                        {
                            "id": cal.get("id"),
                            "summary": cal.get("summary"),
                            "primary": cal.get("primary", False),
                            "accessRole": cal.get("accessRole")
                        }
                        for cal in calendar_list.get("items", [])
                    ]
                }
            except Exception as e:
                results["google_calendars"] = {
                    "success": False,
                    "error": str(e)
                }
        else:
            results["google_oauth"] = {
                "status": "Pas de tokens OAuth",
                "has_access_token": False
            }
    except Exception as e:
        results["google_oauth"] = {"error": str(e)}

    # 5. Chercher les hooks liés à Event
    try:
        from frappe import get_hooks
        hooks = get_hooks()

        doc_events = hooks.get("doc_events", {})
        event_hooks = doc_events.get("Event", {})

        results["event_hooks"] = event_hooks if event_hooks else "Aucun hook Event trouvé"
    except Exception as e:
        results["event_hooks"] = {"error": str(e)}

    context.results = results
    context.results_json = json.dumps(results, indent=2, default=str)
    context.success = True

    return context
