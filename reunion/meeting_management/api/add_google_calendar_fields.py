"""
Script pour ajouter les custom fields Google Calendar aux DocTypes Event et Task
À exécuter via: bench execute reunion.meeting_management.api.add_google_calendar_fields.add_custom_fields
"""

import frappe


def add_custom_fields():
	"""Ajoute les custom fields pour la synchronisation Google Calendar"""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	# D'abord, supprimer les custom fields existants en utilisant SQL direct
	doctypes = ['Event', 'Task']
	fieldnames = ['google_event_id', 'google_calendar_id']

	for doctype in doctypes:
		for fieldname in fieldnames:
			try:
				# Supprimer directement de la base de données
				frappe.db.sql("""
					DELETE FROM `tabCustom Field`
					WHERE dt = %s AND fieldname = %s
				""", (doctype, fieldname))
				print(f"✓ Deleted existing custom field: {doctype}.{fieldname}")
			except Exception as e:
				print(f"⚠ Could not delete {doctype}.{fieldname}: {str(e)}")

	frappe.db.commit()

	# Vider le cache pour forcer le rechargement des métadonnées
	frappe.clear_cache(doctype='Event')
	frappe.clear_cache(doctype='Task')

	# Custom fields pour Event et Task
	custom_fields = {
		'Event': [
			{
				'fieldname': 'google_event_id',
				'label': 'Google Event ID',
				'fieldtype': 'Data',
				'insert_after': 'event_type',
				'read_only': 1,
				'hidden': 1,
				'no_copy': 1
			},
			{
				'fieldname': 'google_calendar_id',
				'label': 'Google Calendar ID',
				'fieldtype': 'Data',
				'insert_after': 'google_event_id',
				'read_only': 1,
				'hidden': 1,
				'no_copy': 1
			}
		],
		'Task': [
			{
				'fieldname': 'google_event_id',
				'label': 'Google Event ID',
				'fieldtype': 'Data',
				'insert_after': 'status',
				'read_only': 1,
				'hidden': 1,
				'no_copy': 1
			},
			{
				'fieldname': 'google_calendar_id',
				'label': 'Google Calendar ID',
				'fieldtype': 'Data',
				'insert_after': 'google_event_id',
				'read_only': 1,
				'hidden': 1,
				'no_copy': 1
			}
		]
	}

	# Utiliser la fonction create_custom_fields qui gère automatiquement la migration
	create_custom_fields(custom_fields, update=True)

	frappe.db.commit()
	print("\n✅ All custom fields have been created successfully!")


if __name__ == '__main__':
	add_custom_fields()
