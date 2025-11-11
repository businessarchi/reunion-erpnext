"""
Sample DocType Controller
"""

import frappe
from frappe.model.document import Document


class SampleDoctype(Document):
	"""
	Custom controller for Sample Doctype
	"""

	def validate(self):
		"""
		Validate the document before saving
		"""
		pass

	def before_save(self):
		"""
		Called before the document is saved
		"""
		pass

	def after_insert(self):
		"""
		Called after the document is inserted
		"""
		pass

	def on_submit(self):
		"""
		Called when the document is submitted
		"""
		pass

	def on_cancel(self):
		"""
		Called when the document is cancelled
		"""
		pass

	def on_trash(self):
		"""
		Called when the document is deleted
		"""
		pass
