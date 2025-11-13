// Copyright (c) 2025, Business Architecte and contributors
// For license information, please see license.txt

frappe.ui.form.on('Google Calendar Settings', {
	refresh: function(frm) {
		// Bouton Setup (toujours visible pour debug)
		frm.add_custom_button(__('🔧 Setup Custom Fields'), function() {
			setup_custom_fields(frm);
		}, __('Admin'));

		// Ajouter le bouton de connexion Google
		if (frm.doc.enabled && frm.doc.client_id && frm.doc.client_secret) {
			if (frm.doc.sync_status === 'Non connecté' || frm.doc.sync_status === 'Erreur') {
				frm.add_custom_button(__('Se connecter à Google Calendar'), function() {
					connect_to_google(frm);
				}, __('Actions'));
			}

			if (frm.doc.sync_status === 'Connecté') {
				frm.add_custom_button(__('Charger les calendriers'), function() {
					load_calendars_into_table(frm);
				}, __('Actions'));

				frm.add_custom_button(__('Synchroniser maintenant'), function() {
					sync_now(frm);
				}, __('Actions'));

				frm.add_custom_button(__('Déconnecter'), function() {
					disconnect_google(frm);
				}, __('Actions'));
			}
		}

		// Ajouter un message d'aide
		if (!frm.doc.client_id || !frm.doc.client_secret) {
			frm.dashboard.add_comment(
				__('Pour configurer Google Calendar : <br>1. Créer un projet sur Google Cloud Console<br>2. Activer l\'API Google Calendar<br>3. Créer des credentials OAuth 2.0<br>4. Copier le Client ID et Client Secret ici'),
				'blue',
				true
			);
		}
	},

	enabled: function(frm) {
		// Placeholder pour futures validations
	}
});

function connect_to_google(frm) {
	frappe.call({
		method: 'reunion.meeting_management.api.google_auth.get_authorization_url',
		callback: function(r) {
			if (r.message && r.message.authorization_url) {
				// Ouvrir l'URL d'autorisation dans une nouvelle fenêtre
				window.open(r.message.authorization_url, '_blank');

				frappe.msgprint({
					title: __('Autorisation Google'),
					indicator: 'blue',
					message: __('Une fenêtre s\'est ouverte pour autoriser l\'accès à Google Calendar. Après autorisation, revenez ici et actualisez la page.')
				});
			} else {
				frappe.msgprint({
					title: __('Erreur'),
					indicator: 'red',
					message: __('Impossible de générer l\'URL d\'autorisation')
				});
			}
		}
	});
}

function sync_now(frm) {
	frappe.call({
		method: 'reunion.meeting_management.api.google_calendar.sync_from_google',
		freeze: true,
		freeze_message: __('Synchronisation en cours...'),
		callback: function(r) {
			if (r.message && r.message.success) {
				frappe.show_alert({
					message: __('Synchronisation réussie ! {0} événements importés', [r.message.events_synced || 0]),
					indicator: 'green'
				});
				frm.reload_doc();
			} else {
				frappe.msgprint({
					title: __('Erreur'),
					indicator: 'red',
					message: r.message.message || __('Erreur lors de la synchronisation')
				});
			}
		}
	});
}

function disconnect_google(frm) {
	frappe.confirm(
		__('Êtes-vous sûr de vouloir déconnecter Google Calendar ?'),
		function() {
			frappe.call({
				method: 'reunion.meeting_management.api.google_auth.disconnect',
				callback: function(r) {
					if (r.message && r.message.success) {
						frappe.show_alert({
							message: __('Déconnecté de Google Calendar'),
							indicator: 'green'
						});
						frm.reload_doc();
					}
				}
			});
		}
	);
}

function load_calendars_into_table(frm) {
	frappe.call({
		method: 'reunion.meeting_management.api.google_calendar.list_calendars',
		freeze: true,
		freeze_message: __('Récupération de la liste des calendriers...'),
		callback: function(r) {
			if (r.message && r.message.success) {
				let calendars = r.message.calendars;

				// Vider la table actuelle
				frm.clear_table('calendars_to_sync');

				// Ajouter chaque calendrier
				calendars.forEach(cal => {
					let row = frm.add_child('calendars_to_sync');
					row.calendar_id = cal.id;
					row.calendar_name = cal.summary;
					row.description = cal.description || '';
					row.enabled = cal.primary ? 1 : 0; // Activer automatiquement le calendrier principal
					row.sync_to_doctype = 'Event'; // Par défaut synchroniser vers Event
				});

				frm.refresh_field('calendars_to_sync');

				frappe.show_alert({
					message: __('${calendars.length} calendrier(s) chargé(s). Configurez-les et enregistrez.'),
					indicator: 'green'
				});
			} else {
				frappe.msgprint({
					title: __('Erreur'),
					indicator: 'red',
					message: r.message.message || __('Impossible de récupérer la liste')
				});
			}
		}
	});
}

function setup_custom_fields(frm) {
	frappe.call({
		method: 'reunion.meeting_management.api.setup_custom_fields.setup',
		freeze: true,
		freeze_message: __('Création des custom fields...'),
		callback: function(r) {
			if (r.message && r.message.success) {
				frappe.show_alert({
					message: __('Custom fields créés avec succès !'),
					indicator: 'green'
				});
			} else {
				frappe.msgprint({
					title: __('Erreur'),
					indicator: 'red',
					message: r.message.message || __('Erreur lors de la création des custom fields')
				});
			}
		}
	});
}
