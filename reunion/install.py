"""
Installation and setup functions for Frappe App
"""

import frappe


def before_install():
	"""
	Run before app installation
	"""
	pass


def after_install():
	"""
	Run after app installation
	- Create default records
	- Set up initial configuration
	- Import fixtures
	"""
	frappe.db.commit()


def before_uninstall():
	"""
	Run before app uninstallation
	"""
	pass


def after_uninstall():
	"""
	Run after app uninstallation
	- Clean up custom fields
	- Remove app data
	"""
	pass
