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

	def before_save(self):
		"""Actions avant sauvegarde"""
		# S'assurer que calendar_id a une valeur par défaut
		if not self.calendar_id:
			self.calendar_id = "primary"

	def on_update(self):
		"""Actions après mise à jour"""
		pass
