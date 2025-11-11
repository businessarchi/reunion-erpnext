"""
Custom Permission Logic for Frappe App

This module contains permission query conditions and permission checks
that can be hooked into DocTypes via hooks.py
"""

import frappe


def get_permission_query_conditions(user):
	"""
	Returns SQL conditions to filter documents based on user permissions.

	This function is used in hooks.py like this:
	permission_query_conditions = {
		"Sample Doctype": "reunion.permissions.get_permission_query_conditions"
	}

	Args:
		user (str): The user for whom to generate conditions

	Returns:
		str: SQL WHERE clause conditions
	"""
	if not user:
		user = frappe.session.user

	# System Manager can see everything
	if "System Manager" in frappe.get_roles(user):
		return None

	# Regular users can only see Active documents
	return """(`tabSample Doctype`.status = 'Active')"""


def has_permission(doc, ptype, user):
	"""
	Custom permission check for individual documents.

	This function is used in hooks.py like this:
	has_permission = {
		"Sample Doctype": "reunion.permissions.has_permission"
	}

	Args:
		doc: The document to check permissions for
		ptype (str): Permission type ('read', 'write', 'submit', etc.)
		user (str): The user to check permissions for

	Returns:
		bool: True if user has permission, False otherwise
	"""
	if not user:
		user = frappe.session.user

	# System Manager has all permissions
	if "System Manager" in frappe.get_roles(user):
		return True

	# Owner always has permission
	if doc.owner == user:
		return True

	# Read permission for all users if status is Active
	if ptype == "read" and doc.status == "Active":
		return True

	# Write permission only for specific roles
	if ptype == "write":
		user_roles = frappe.get_roles(user)
		if "Sample Role" in user_roles:
			return True

	# Default: no permission
	return False


def can_create_sample_doctype(user=None):
	"""
	Check if a user can create a Sample Doctype.

	Usage:
		if reunion.permissions.can_create_sample_doctype():
			# Allow creation
	"""
	if not user:
		user = frappe.session.user

	# Check role
	user_roles = frappe.get_roles(user)
	allowed_roles = ["System Manager", "Sample Creator"]

	return any(role in user_roles for role in allowed_roles)


def filter_allowed_documents(doctype, user=None):
	"""
	Get list of documents a user has access to.

	Args:
		doctype (str): The DocType name
		user (str): User to check (defaults to current user)

	Returns:
		list: List of document names the user can access
	"""
	if not user:
		user = frappe.session.user

	# System Manager sees all
	if "System Manager" in frappe.get_roles(user):
		return frappe.get_all(doctype, pluck="name")

	# Regular users see only their own or Active ones
	filters = [
		["owner", "=", user],
		["status", "=", "Active"]
	]

	return frappe.get_all(
		doctype,
		filters=filters,
		or_filters=True,
		pluck="name"
	)
