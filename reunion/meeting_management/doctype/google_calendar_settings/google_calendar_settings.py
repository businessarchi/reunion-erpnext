# Copyright (c) 2025, Business Architecte and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GoogleCalendarSettings(Document):
	"""Doctype pour gérer la configuration Google Calendar OAuth"""

	def validate(self):
		"""Validation avant sauvegarde"""
		if self.enabled and not (self.client_id and self.client_secret):
			frappe.throw("Client ID et Client Secret sont requis pour activer Google Calendar")
