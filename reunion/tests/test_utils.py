"""
Unit tests for utility functions
"""

import frappe
import unittest
from reunion.utils import ping


class TestUtils(unittest.TestCase):
	"""
	Test utility functions
	"""

	def test_ping(self):
		"""
		Test the ping API endpoint
		"""
		result = ping()
		self.assertEqual(result, "pong")

	def test_app_version(self):
		"""
		Test that app version is accessible
		"""
		from frappe_app import __version__
		self.assertIsNotNone(__version__)
		self.assertIsInstance(__version__, str)
