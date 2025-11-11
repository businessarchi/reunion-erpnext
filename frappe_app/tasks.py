"""
Scheduled tasks for Frappe App
"""

import frappe


def all():
	"""
	Runs on every scheduler tick (default: every 5 minutes)
	"""
	pass


def hourly():
	"""
	Runs every hour
	"""
	pass


def daily():
	"""
	Runs daily at midnight
	"""
	pass


def weekly():
	"""
	Runs every Sunday at midnight
	"""
	pass


def monthly():
	"""
	Runs on the 1st of every month at midnight
	"""
	pass
