"""
Script pour ajouter les custom fields Google Calendar aux DocTypes Event et Task
À exécuter via: bench execute reunion.meeting_management.api.add_google_calendar_fields.add_custom_fields
"""

import frappe


def add_custom_fields():
	"""Ajoute les custom fields pour la synchronisation Google Calendar"""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
	from frappe.model.meta import get_meta

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

	# Vider le cache complet
	frappe.clear_cache()

	# Forcer la suppression du cache de métadonnées pour Event et Task
	for doctype in doctypes:
		cache_key = f"doctype_meta:{doctype}"
		frappe.cache().delete_value(cache_key)
		print(f"✓ Cleared meta cache for {doctype}")

	print("✓ Cache cleared and meta refreshed")

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

	# Vérifier si les colonnes existent et les ajouter manuellement si nécessaire
	for doctype, table_name in [('Event', 'tabEvent'), ('Task', 'tabTask')]:
		for fieldname in ['google_event_id', 'google_calendar_id']:
			try:
				# Vérifier si la colonne existe
				result = frappe.db.sql(f"""
					SELECT COLUMN_NAME
					FROM INFORMATION_SCHEMA.COLUMNS
					WHERE TABLE_SCHEMA = %s
					AND TABLE_NAME = %s
					AND COLUMN_NAME = %s
				""", (frappe.conf.db_name, table_name, fieldname))

				if not result:
					# La colonne n'existe pas, l'ajouter
					print(f"⚠ Column {table_name}.{fieldname} does not exist, adding it...")
					frappe.db.sql(f"""
						ALTER TABLE `{table_name}`
						ADD COLUMN `{fieldname}` VARCHAR(140)
					""")
					print(f"✓ Added column {table_name}.{fieldname}")
				else:
					print(f"✓ Column {table_name}.{fieldname} already exists")
			except Exception as e:
				print(f"⚠ Error checking/adding column {table_name}.{fieldname}: {str(e)}")

	frappe.db.commit()

	# Maintenant créer les Custom Field docs
	create_custom_fields(custom_fields, update=True)

	frappe.db.commit()
	print("\n✅ All custom fields have been created successfully!")


if __name__ == '__main__':
	add_custom_fields()
