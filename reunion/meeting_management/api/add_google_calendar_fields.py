"""
Script pour ajouter les custom fields Google Calendar aux DocTypes Event et Task
À exécuter via: bench execute reunion.meeting_management.api.add_google_calendar_fields.add_custom_fields
"""

import frappe


def add_custom_fields():
	"""Ajoute les custom fields pour la synchronisation Google Calendar"""

	# Custom fields pour Event
	event_fields = [
		{
			'doctype': 'Event',
			'fieldname': 'google_event_id',
			'label': 'Google Event ID',
			'fieldtype': 'Data',
			'insert_after': 'event_type',
			'read_only': 1,
			'hidden': 1
		},
		{
			'doctype': 'Event',
			'fieldname': 'google_calendar_id',
			'label': 'Google Calendar ID',
			'fieldtype': 'Data',
			'insert_after': 'google_event_id',
			'read_only': 1,
			'hidden': 1
		}
	]

	# Custom fields pour Task
	task_fields = [
		{
			'doctype': 'Task',
			'fieldname': 'google_event_id',
			'label': 'Google Event ID',
			'fieldtype': 'Data',
			'insert_after': 'status',
			'read_only': 1,
			'hidden': 1
		},
		{
			'doctype': 'Task',
			'fieldname': 'google_calendar_id',
			'label': 'Google Calendar ID',
			'fieldtype': 'Data',
			'insert_after': 'google_event_id',
			'read_only': 1,
			'hidden': 1
		}
	]

	all_fields = event_fields + task_fields

	for field in all_fields:
		# Vérifier si le field existe déjà
		if not frappe.db.exists('Custom Field', {
			'dt': field['doctype'],
			'fieldname': field['fieldname']
		}):
			custom_field = frappe.get_doc({
				'doctype': 'Custom Field',
				'dt': field['doctype'],
				'fieldname': field['fieldname'],
				'label': field['label'],
				'fieldtype': field['fieldtype'],
				'insert_after': field['insert_after'],
				'read_only': field['read_only'],
				'hidden': field['hidden']
			})
			custom_field.insert(ignore_permissions=True)
			print(f"✓ Created custom field: {field['doctype']}.{field['fieldname']}")
		else:
			print(f"- Custom field already exists: {field['doctype']}.{field['fieldname']}")

	frappe.db.commit()
	print("\n✅ All custom fields have been created successfully!")


if __name__ == '__main__':
	add_custom_fields()
