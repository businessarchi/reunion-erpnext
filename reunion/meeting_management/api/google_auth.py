# Copyright (c) 2025, Business Architecte and contributors
# For license information, please see license.txt

"""
API pour l'authentification Google OAuth2
"""

import frappe
from frappe import _
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json
from datetime import datetime, timedelta


# Scopes requis pour Google Calendar
# Note: calendar inclut déjà calendar.events, pas besoin des deux
SCOPES = ['https://www.googleapis.com/auth/calendar']


@frappe.whitelist()
def get_authorization_url():
	"""
	Génère l'URL d'autorisation OAuth2 pour Google Calendar

	Returns:
		dict: {"success": bool, "authorization_url": str}
	"""
	try:
		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")

		if not settings.client_id or not settings.client_secret:
			return {
				"success": False,
				"message": _("Client ID et Client Secret non configurés")
			}

		# URL de callback après autorisation
		redirect_uri = get_redirect_uri()

		# Configuration OAuth flow
		flow = Flow.from_client_config(
			{
				"web": {
					"client_id": settings.client_id,
					"client_secret": settings.get_password("client_secret"),
					"auth_uri": "https://accounts.google.com/o/oauth2/auth",
					"token_uri": "https://oauth2.googleapis.com/token",
					"redirect_uris": [redirect_uri]
				}
			},
			scopes=SCOPES,
			redirect_uri=redirect_uri
		)

		# Paramètres OAuth
		# access_type='offline' est CRUCIAL pour obtenir un refresh_token
		# prompt='consent' force Google à redemander le consentement et retourner un refresh_token
		authorization_url, state = flow.authorization_url(
			access_type='offline',
			prompt='consent'  # Force consent pour obtenir refresh_token
		)

		# Stocker le state pour validation
		frappe.cache().set_value(f"google_oauth_state_{frappe.session.user}", state, expires_in_sec=600)

		return {
			"success": True,
			"authorization_url": authorization_url
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google OAuth - Get Authorization URL Error")
		return {
			"success": False,
			"message": str(e)
		}


@frappe.whitelist(allow_guest=True)
def handle_oauth_callback(code=None, state=None, error=None):
	"""
	Gère le callback OAuth2 de Google

	Args:
		code: Code d'autorisation Google
		state: State pour validation CSRF
		error: Erreur éventuelle

	Returns:
		Redirect vers Google Calendar Settings
	"""
	try:
		# Log pour debug
		frappe.logger().info(f"OAuth Callback received - code: {'present' if code else 'missing'}, error: {error}")

		if error:
			frappe.log_error(f"OAuth error from Google: {error}", "Google OAuth - Error from Google")
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = f"/app/google-calendar-settings?error={error}"
			return

		if not code:
			frappe.log_error("No authorization code received", "Google OAuth - Missing Code")
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = "/app/google-calendar-settings?error=no_code"
			return

		# Valider le state (protection CSRF)
		# Note: En production, valider le state stocké

		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")
		redirect_uri = get_redirect_uri()

		# Échanger le code contre des tokens
		flow = Flow.from_client_config(
			{
				"web": {
					"client_id": settings.client_id,
					"client_secret": settings.get_password("client_secret"),
					"auth_uri": "https://accounts.google.com/o/oauth2/auth",
					"token_uri": "https://oauth2.googleapis.com/token",
					"redirect_uris": [redirect_uri]
				}
			},
			scopes=SCOPES,
			redirect_uri=redirect_uri
		)

		# Désactiver la vérification stricte des scopes
		# Google peut retourner plus de scopes que demandés si le Client ID a été utilisé
		# avec OAuth Playground ou d'autres applications
		import os
		os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

		flow.fetch_token(code=code)
		credentials = flow.credentials

		# Récupérer à nouveau le doc pour être sûr d'avoir la dernière version
		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")

		# Sauvegarder les tokens et le statut
		if credentials.expiry:
			settings.token_expiry = credentials.expiry
		else:
			# Par défaut, les tokens expirent après 1 heure
			settings.token_expiry = datetime.now() + timedelta(hours=1)

		settings.sync_status = "Connecté"

		# Pour les champs Password, on doit utiliser set_value AVANT le save
		settings.access_token = credentials.token
		settings.refresh_token = credentials.refresh_token

		settings.save(ignore_permissions=True)
		frappe.db.commit()

		# Log success
		frappe.logger().info(f"OAuth tokens saved successfully for user")

		# Rediriger vers la page de settings
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = "/app/google-calendar-settings?success=1"

	except Exception as e:
		error_msg = str(e)
		frappe.log_error(frappe.get_traceback(), "Google OAuth - Handle Callback Error")
		frappe.logger().error(f"OAuth callback failed: {error_msg}")
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = f"/app/google-calendar-settings?error={error_msg}"


@frappe.whitelist()
def disconnect():
	"""
	Déconnecte Google Calendar en supprimant les tokens

	Returns:
		dict: {"success": bool, "message": str}
	"""
	try:
		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")

		settings.access_token = None
		settings.refresh_token = None
		settings.token_expiry = None
		settings.sync_status = "Non connecté"
		settings.last_sync = None
		settings.save(ignore_permissions=True)

		frappe.db.commit()

		return {
			"success": True,
			"message": _("Déconnecté de Google Calendar avec succès")
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google OAuth - Disconnect Error")
		return {
			"success": False,
			"message": str(e)
		}


def get_credentials():
	"""
	Récupère les credentials OAuth2 valides pour Google Calendar
	Rafraîchit automatiquement le token si expiré

	Returns:
		Credentials: Google OAuth2 credentials ou None
	"""
	try:
		settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")

		frappe.logger().info(f"get_credentials - enabled: {settings.enabled}")
		frappe.logger().info(f"get_credentials - has access_token: {bool(settings.access_token)}")
		frappe.logger().info(f"get_credentials - has refresh_token: {bool(settings.refresh_token)}")

		if not settings.enabled:
			frappe.logger().warning("Google Calendar not enabled")
			return None

		if not settings.access_token or not settings.refresh_token:
			frappe.logger().warning(f"Missing tokens - access: {bool(settings.access_token)}, refresh: {bool(settings.refresh_token)}")
			return None

		# Récupérer les tokens déchiffrés
		access_token = settings.get_password("access_token")
		refresh_token = settings.get_password("refresh_token")

		frappe.logger().info(f"get_credentials - decrypted access_token: {bool(access_token)}")
		frappe.logger().info(f"get_credentials - decrypted refresh_token: {bool(refresh_token)}")

		if not access_token or not refresh_token:
			frappe.logger().error("Failed to decrypt tokens")
			return None

		# Créer les credentials
		credentials = Credentials(
			token=access_token,
			refresh_token=refresh_token,
			token_uri="https://oauth2.googleapis.com/token",
			client_id=settings.client_id,
			client_secret=settings.get_password("client_secret"),
			scopes=SCOPES
		)

		# Vérifier si le token est expiré et le rafraîchir si nécessaire
		if credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())

			# Sauvegarder le nouveau token
			settings.access_token = credentials.token
			if credentials.expiry:
				settings.token_expiry = credentials.expiry
			settings.save(ignore_permissions=True)
			frappe.db.commit()

		return credentials

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google OAuth - Get Credentials Error")

		# Marquer comme erreur
		try:
			settings = frappe.get_doc("Google Calendar Settings", "Google Calendar Settings")
			settings.sync_status = "Erreur"
			settings.save(ignore_permissions=True)
			frappe.db.commit()
		except:
			pass

		return None


def get_redirect_uri():
	"""
	Génère l'URI de redirection OAuth

	Returns:
		str: URL de callback
	"""
	site_url = frappe.utils.get_url()
	return f"{site_url}/api/method/reunion.meeting_management.api.google_auth.handle_oauth_callback"
