"""
Example Database Migration Patch

This patch is executed once when migrating the database.
Add this to patches.txt:
reunion.patches.v0_1.example_patch
"""

import frappe


def execute():
	"""
	Execute the patch.
	This function is called when 'bench migrate' is run.
	"""
	frappe.reload_doc("frappe_app", "doctype", "sample_doctype")

	# Example: Update existing documents
	docs = frappe.get_all("Sample Doctype", filters={"status": ""})

	for doc in docs:
		sample_doc = frappe.get_doc("Sample Doctype", doc.name)
		sample_doc.status = "Draft"
		sample_doc.save()

	frappe.db.commit()

	print(f"Updated {len(docs)} Sample Doctype documents")
