"""
Unit tests for Sample Doctype
"""

import frappe
import unittest


class TestSampleDoctype(unittest.TestCase):
	"""
	Test cases for Sample Doctype
	"""

	def setUp(self):
		"""
		Set up test fixtures
		"""
		pass

	def tearDown(self):
		"""
		Clean up after tests
		"""
		pass

	def test_creation(self):
		"""
		Test document creation
		"""
		doc = frappe.get_doc({
			"doctype": "Sample Doctype",
			"title": "Test Sample",
			"description": "This is a test",
			"status": "Draft"
		})
		doc.insert()

		self.assertEqual(doc.title, "Test Sample")
		self.assertEqual(doc.status, "Draft")

		doc.delete()
