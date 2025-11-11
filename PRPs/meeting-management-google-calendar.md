# Plan d'implémentation : Application de gestion de réunions avec intégration Google Calendar

## Vue d'ensemble

Création d'une application ERPNext complète pour gérer les réunions avec synchronisation bidirectionnelle vers Google Calendar. L'application permettra aux utilisateurs de se connecter à leur compte Google, synchroniser leur agenda principal, et gérer les réunions directement depuis ERPNext.

## Résumé des exigences

- **Authentification Google OAuth2** : Permettre aux utilisateurs de se connecter à leur compte Google
- **Synchronisation Google Calendar** : Connexion à l'agenda principal de l'utilisateur
- **Gestion des réunions** : Créer, modifier, supprimer des réunions
- **Synchronisation bidirectionnelle** : Les modifications dans ERPNext se reflètent dans Google Calendar et vice versa
- **Participants** : Gérer les participants aux réunions
- **Interface utilisateur** : Vue calendrier et liste des réunions

## Résultats de la recherche

### Bonnes pratiques Frappe/ERPNext

D'après l'analyse du codebase et la documentation Frappe :

1. **Structure modulaire** : Utiliser le module `meeting_management` avec des doctypes séparés
2. **Document Events** : Utiliser les hooks `doc_events` pour déclencher la synchronisation automatique
3. **Scheduled Tasks** : Implémenter des tâches planifiées pour la synchronisation périodique
4. **Whitelisted API Methods** : Exposer les méthodes OAuth et sync via `@frappe.whitelist()`
5. **Settings Doctype** : Créer un doctype unique pour stocker les paramètres Google Calendar
6. **Child Tables** : Utiliser une table enfant pour les participants
7. **Track Changes** : Activer le suivi des modifications pour audit

### Implémentations de référence

- **Google Calendar API Python** : Utiliser `google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2`
- **OAuth2 Flow** : Flux OAuth2 standard avec `credentials.json` et `token.json`
- **Frappe DocType Patterns** : Suivre le pattern de `sample_doctype` existant
- **API Methods Location** : Créer un module `api/google_calendar.py` dédié
- **Calendar View** : Utiliser `doctype_calendar_js` hook pour la vue calendrier ERPNext

### Décisions technologiques

1. **Google Calendar API v3** : API officielle Google pour l'intégration calendrier
   - Justification : API mature, bien documentée, support Python officiel

2. **OAuth2 avec refresh tokens** : Authentification utilisateur avec tokens persistants
   - Justification : Permet une synchronisation automatique sans redemander l'autorisation

3. **Scheduled Sync (hourly)** : Synchronisation automatique toutes les heures
   - Justification : Balance entre fraîcheur des données et charge API

4. **Webhook optionnel** : Push notifications de Google Calendar (Phase 2)
   - Justification : Synchronisation temps réel, mais nécessite configuration avancée

5. **Stockage sécurisé des tokens** : Tokens OAuth stockés chiffrés dans la base de données
   - Justification : Sécurité des credentials utilisateur

## Tâches d'implémentation

### Phase 1 : Configuration et authentification Google (Fondations)

#### 1. Configuration du projet Google Cloud
- **Description** : Créer un projet Google Cloud, activer l'API Calendar, configurer l'écran de consentement OAuth
- **Fichiers à créer** : Documentation `docs/google-cloud-setup.md`
- **Dépendances** : Aucune
- **Effort estimé** : 30 minutes
- **Livrables** :
  - Projet Google Cloud créé
  - API Google Calendar activée
  - Credentials OAuth2 (client_id, client_secret) générés
  - Fichier `credentials.json` téléchargé

#### 2. Installation des dépendances Python
- **Description** : Ajouter les bibliothèques Google Calendar API au projet
- **Fichiers à modifier** :
  - [requirements.txt](requirements.txt) - Ajouter les dépendances
- **Dépendances** : Tâche 1
- **Effort estimé** : 15 minutes
- **Packages à ajouter** :
  ```
  google-api-python-client>=2.0.0
  google-auth-httplib2>=0.1.0
  google-auth-oauthlib>=1.0.0
  ```

#### 3. Créer le module meeting_management
- **Description** : Créer la structure de répertoires pour le nouveau module
- **Fichiers à créer** :
  - `frappe_app/meeting_management/__init__.py`
  - `frappe_app/meeting_management/doctype/__init__.py`
- **Fichiers à modifier** :
  - [frappe_app/modules.txt](frappe_app/modules.txt) - Ajouter "Meeting Management"
- **Dépendances** : Aucune
- **Effort estimé** : 10 minutes

#### 4. Créer le doctype Google Calendar Settings
- **Description** : Doctype unique (Single) pour stocker les paramètres et credentials OAuth
- **Fichiers à créer** :
  - `frappe_app/meeting_management/doctype/google_calendar_settings/__init__.py`
  - `frappe_app/meeting_management/doctype/google_calendar_settings/google_calendar_settings.json`
  - `frappe_app/meeting_management/doctype/google_calendar_settings/google_calendar_settings.py`
  - `frappe_app/meeting_management/doctype/google_calendar_settings/google_calendar_settings.js`
- **Dépendances** : Tâche 3
- **Effort estimé** : 1 heure
- **Structure JSON** :
  ```json
  {
    "issingle": 1,
    "fields": [
      {"fieldname": "enabled", "fieldtype": "Check", "label": "Enable Google Calendar Sync"},
      {"fieldname": "client_id", "fieldtype": "Data", "label": "Client ID"},
      {"fieldname": "client_secret", "fieldtype": "Password", "label": "Client Secret"},
      {"fieldname": "redirect_uri", "fieldtype": "Data", "label": "Redirect URI", "read_only": 1},
      {"fieldname": "access_token", "fieldtype": "Password", "label": "Access Token", "read_only": 1},
      {"fieldname": "refresh_token", "fieldtype": "Password", "label": "Refresh Token", "read_only": 1},
      {"fieldname": "token_expiry", "fieldtype": "Datetime", "label": "Token Expiry", "read_only": 1},
      {"fieldname": "calendar_id", "fieldtype": "Data", "label": "Calendar ID", "default": "primary"},
      {"fieldname": "last_sync", "fieldtype": "Datetime", "label": "Last Sync", "read_only": 1},
      {"fieldname": "sync_status", "fieldtype": "Select", "label": "Sync Status", "options": "Not Connected\nConnected\nError", "read_only": 1}
    ]
  }
  ```

#### 5. Implémenter le flux OAuth2
- **Description** : Créer les méthodes pour l'authentification Google OAuth2
- **Fichiers à créer** :
  - `frappe_app/meeting_management/api/__init__.py`
  - `frappe_app/meeting_management/api/google_auth.py`
- **Dépendances** : Tâche 2, 4
- **Effort estimé** : 2 heures
- **Méthodes à implémenter** :
  - `@frappe.whitelist()` `get_authorization_url()` : Générer l'URL OAuth2
  - `@frappe.whitelist()` `handle_oauth_callback(code)` : Échanger le code contre des tokens
  - `refresh_access_token()` : Rafraîchir le token expiré
  - `get_credentials()` : Récupérer les credentials valides

#### 6. Créer la page web de callback OAuth
- **Description** : Page pour gérer le retour de Google après authentification
- **Fichiers à créer** :
  - `frappe_app/meeting_management/www/google-callback.py`
  - `frappe_app/meeting_management/www/google-callback.html`
- **Dépendances** : Tâche 5
- **Effort estimé** : 1 heure

#### 7. Ajouter un bouton "Connect Google Calendar" dans Settings
- **Description** : Interface utilisateur pour déclencher le flux OAuth
- **Fichiers à modifier** :
  - `frappe_app/meeting_management/doctype/google_calendar_settings/google_calendar_settings.js`
- **Dépendances** : Tâche 5, 6
- **Effort estimé** : 45 minutes
- **Fonctionnalités** :
  - Bouton "Connect to Google Calendar"
  - Affichage du statut de connexion
  - Bouton "Disconnect" si connecté

### Phase 2 : Doctypes de gestion des réunions

#### 8. Créer le doctype Meeting
- **Description** : Doctype principal pour les réunions
- **Fichiers à créer** :
  - `frappe_app/meeting_management/doctype/meeting/__init__.py`
  - `frappe_app/meeting_management/doctype/meeting/meeting.json`
  - `frappe_app/meeting_management/doctype/meeting/meeting.py`
  - `frappe_app/meeting_management/doctype/meeting/meeting.js`
  - `frappe_app/meeting_management/doctype/meeting/test_meeting.py`
- **Dépendances** : Tâche 3
- **Effort estimé** : 2 heures
- **Structure JSON** :
  ```json
  {
    "autoname": "naming_series:",
    "naming_series": "MTG-.YYYY.-.#####",
    "fields": [
      {"fieldname": "title", "fieldtype": "Data", "label": "Title", "reqd": 1, "in_list_view": 1},
      {"fieldname": "description", "fieldtype": "Text Editor", "label": "Description"},
      {"fieldname": "start_datetime", "fieldtype": "Datetime", "label": "Start Date & Time", "reqd": 1},
      {"fieldname": "end_datetime", "fieldtype": "Datetime", "label": "End Date & Time", "reqd": 1},
      {"fieldname": "location", "fieldtype": "Data", "label": "Location"},
      {"fieldname": "meeting_link", "fieldtype": "Data", "label": "Meeting Link (Google Meet, Zoom, etc.)"},
      {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Scheduled\nIn Progress\nCompleted\nCancelled", "default": "Scheduled"},
      {"fieldname": "participants", "fieldtype": "Table", "label": "Participants", "options": "Meeting Participant"},
      {"fieldname": "google_event_id", "fieldtype": "Data", "label": "Google Event ID", "read_only": 1, "hidden": 1},
      {"fieldname": "google_calendar_link", "fieldtype": "Data", "label": "Google Calendar Link", "read_only": 1},
      {"fieldname": "synced_with_google", "fieldtype": "Check", "label": "Synced with Google", "read_only": 1, "default": 0},
      {"fieldname": "last_synced", "fieldtype": "Datetime", "label": "Last Synced", "read_only": 1}
    ],
    "track_changes": 1
  }
  ```

#### 9. Créer le doctype Meeting Participant (Child Table)
- **Description** : Table enfant pour gérer les participants aux réunions
- **Fichiers à créer** :
  - `frappe_app/meeting_management/doctype/meeting_participant/__init__.py`
  - `frappe_app/meeting_management/doctype/meeting_participant/meeting_participant.json`
  - `frappe_app/meeting_management/doctype/meeting_participant/meeting_participant.py`
- **Dépendances** : Tâche 3
- **Effort estimé** : 45 minutes
- **Structure JSON** :
  ```json
  {
    "istable": 1,
    "fields": [
      {"fieldname": "email", "fieldtype": "Data", "label": "Email", "reqd": 1, "in_list_view": 1},
      {"fieldname": "full_name", "fieldtype": "Data", "label": "Full Name", "in_list_view": 1},
      {"fieldname": "response_status", "fieldtype": "Select", "label": "Response Status", "options": "Pending\nAccepted\nDeclined\nTentative", "default": "Pending"},
      {"fieldname": "is_organizer", "fieldtype": "Check", "label": "Is Organizer", "default": 0}
    ]
  }
  ```

#### 10. Ajouter les validations du doctype Meeting
- **Description** : Valider les données du meeting (dates cohérentes, etc.)
- **Fichiers à modifier** :
  - `frappe_app/meeting_management/doctype/meeting/meeting.py`
- **Dépendances** : Tâche 8, 9
- **Effort estimé** : 45 minutes
- **Validations** :
  - `end_datetime` doit être après `start_datetime`
  - Au moins un participant requis
  - Vérifier les conflits de réunions (optionnel)

### Phase 3 : Synchronisation Google Calendar

#### 11. Implémenter les méthodes de synchronisation Google Calendar
- **Description** : Méthodes pour créer, modifier, supprimer des événements dans Google Calendar
- **Fichiers à créer** :
  - `frappe_app/meeting_management/api/google_calendar.py`
- **Dépendances** : Tâche 5, 8
- **Effort estimé** : 3 heures
- **Méthodes à implémenter** :
  - `create_google_event(meeting_doc)` : Créer un événement Google Calendar
  - `update_google_event(meeting_doc)` : Mettre à jour un événement existant
  - `delete_google_event(google_event_id)` : Supprimer un événement
  - `get_google_event(google_event_id)` : Récupérer un événement
  - `list_google_events(time_min, time_max)` : Lister les événements d'une période
  - `sync_from_google()` : Importer les événements de Google Calendar vers ERPNext
  - `build_calendar_service()` : Créer le client API Google Calendar

#### 12. Connecter les hooks de document Meeting
- **Description** : Déclencher automatiquement la synchronisation lors des opérations CRUD
- **Fichiers à modifier** :
  - [frappe_app/hooks.py](frappe_app/hooks.py) - Ajouter les `doc_events`
  - `frappe_app/meeting_management/doctype/meeting/meeting.py` - Implémenter les hooks
- **Dépendances** : Tâche 11
- **Effort estimé** : 1 heure
- **Hooks à ajouter** :
  ```python
  doc_events = {
      "Meeting": {
          "after_insert": "frappe_app.meeting_management.doctype.meeting.meeting.sync_to_google_after_insert",
          "on_update": "frappe_app.meeting_management.doctype.meeting.meeting.sync_to_google_on_update",
          "on_trash": "frappe_app.meeting_management.doctype.meeting.meeting.delete_from_google"
      }
  }
  ```

#### 13. Implémenter la synchronisation planifiée (Scheduled Sync)
- **Description** : Tâche planifiée pour importer les événements de Google Calendar
- **Fichiers à modifier** :
  - [frappe_app/tasks.py](frappe_app/tasks.py) - Ajouter la tâche
  - [frappe_app/hooks.py](frappe_app/hooks.py) - Configurer `scheduler_events`
- **Dépendances** : Tâche 11
- **Effort estimé** : 1.5 heures
- **Configuration** :
  ```python
  scheduler_events = {
      "hourly": [
          "frappe_app.tasks.sync_google_calendar_hourly"
      ]
  }
  ```
- **Logique** :
  - Récupérer les événements Google Calendar depuis la dernière synchro
  - Créer/mettre à jour les Meetings dans ERPNext
  - Gérer les conflits (priorité à la dernière modification)

#### 14. Ajouter un bouton "Sync Now" dans le doctype Meeting
- **Description** : Permettre une synchronisation manuelle d'un meeting spécifique
- **Fichiers à modifier** :
  - `frappe_app/meeting_management/doctype/meeting/meeting.js`
- **Dépendances** : Tâche 11
- **Effort estimé** : 30 minutes

### Phase 4 : Interface utilisateur et expérience

#### 15. Configurer la vue calendrier pour Meeting
- **Description** : Activer et configurer la vue calendrier native de Frappe
- **Fichiers à créer** :
  - `frappe_app/meeting_management/doctype/meeting/meeting_calendar.js`
- **Fichiers à modifier** :
  - [frappe_app/hooks.py](frappe_app/hooks.py) - Ajouter `doctype_calendar_js`
- **Dépendances** : Tâche 8
- **Effort estimé** : 1 heure
- **Configuration** :
  ```javascript
  frappe.views.calendar['Meeting'] = {
      field_map: {
          "start": "start_datetime",
          "end": "end_datetime",
          "id": "name",
          "title": "title",
          "allDay": false
      },
      get_events_method: "frappe_app.meeting_management.doctype.meeting.meeting.get_events"
  }
  ```

#### 16. Personnaliser la vue liste du doctype Meeting
- **Description** : Ajouter des indicateurs de statut et des actions rapides
- **Fichiers à créer** :
  - `frappe_app/meeting_management/doctype/meeting/meeting_list.js`
- **Fichiers à modifier** :
  - [frappe_app/hooks.py](frappe_app/hooks.py) - Ajouter `doctype_list_js`
- **Dépendances** : Tâche 8
- **Effort estimé** : 45 minutes
- **Fonctionnalités** :
  - Indicateurs colorés par statut (Scheduled: blue, Completed: green, Cancelled: red)
  - Badge "Synced" pour les meetings synchronisés avec Google
  - Action rapide "Sync to Google"

#### 17. Améliorer le formulaire Meeting avec UX
- **Description** : Ajouter des fonctionnalités interactives au formulaire
- **Fichiers à modifier** :
  - `frappe_app/meeting_management/doctype/meeting/meeting.js`
- **Dépendances** : Tâche 8
- **Effort estimé** : 1 heure
- **Fonctionnalités** :
  - Auto-complétion des emails de participants
  - Validation temps réel des dates
  - Affichage du lien Google Calendar si synchronisé
  - Bouton "Open in Google Calendar"
  - Indicateur de statut de synchronisation

#### 18. Créer une page web "My Meetings"
- **Description** : Page publique pour voir ses réunions à venir
- **Fichiers à créer** :
  - `frappe_app/meeting_management/www/my-meetings.py`
  - `frappe_app/meeting_management/www/my-meetings.html`
- **Dépendances** : Tâche 8
- **Effort estimé** : 1.5 heures
- **Fonctionnalités** :
  - Liste des réunions à venir de l'utilisateur
  - Filtres par date et statut
  - Liens vers le détail des réunions

### Phase 5 : Permissions et sécurité

#### 19. Configurer les permissions du doctype Meeting
- **Description** : Définir les rôles et permissions pour le doctype Meeting
- **Fichiers à modifier** :
  - `frappe_app/meeting_management/doctype/meeting/meeting.json` - Section permissions
- **Dépendances** : Tâche 8
- **Effort estimé** : 30 minutes
- **Rôles** :
  - **System Manager** : Tous les droits
  - **Meeting Manager** : Créer, lire, écrire, supprimer tous les meetings
  - **Meeting User** : Créer, lire, écrire ses propres meetings
  - **Meeting Guest** : Lire uniquement les meetings où il est participant

#### 20. Implémenter les permission query conditions
- **Description** : Filtrer les meetings visibles selon l'utilisateur
- **Fichiers à créer** :
  - `frappe_app/meeting_management/permissions.py`
- **Fichiers à modifier** :
  - [frappe_app/hooks.py](frappe_app/hooks.py) - Ajouter `permission_query_conditions` et `has_permission`
- **Dépendances** : Tâche 19
- **Effort estimé** : 1 heure
- **Logique** :
  - Les utilisateurs voient leurs propres meetings (owner = user)
  - Les utilisateurs voient les meetings où ils sont participants
  - System Manager et Meeting Manager voient tous les meetings

#### 21. Sécuriser le stockage des tokens OAuth
- **Description** : Chiffrer les tokens dans la base de données
- **Fichiers à modifier** :
  - `frappe_app/meeting_management/doctype/google_calendar_settings/google_calendar_settings.py`
- **Dépendances** : Tâche 4
- **Effort estimé** : 45 minutes
- **Approche** :
  - Utiliser les champs `Password` de Frappe (chiffrement automatique)
  - Valider que les tokens ne sont jamais exposés dans les API responses
  - Logs sans tokens sensibles

### Phase 6 : Tests et documentation

#### 22. Écrire les tests unitaires pour Google Calendar API
- **Description** : Tester les méthodes de synchronisation avec des mocks
- **Fichiers à créer** :
  - `frappe_app/meeting_management/api/test_google_calendar.py`
- **Dépendances** : Tâche 11
- **Effort estimé** : 2 heures
- **Tests à couvrir** :
  - Création d'événement Google
  - Mise à jour d'événement
  - Suppression d'événement
  - Gestion des erreurs API
  - Refresh token

#### 23. Écrire les tests unitaires pour Meeting doctype
- **Description** : Tester le comportement du doctype Meeting
- **Fichiers à modifier** :
  - `frappe_app/meeting_management/doctype/meeting/test_meeting.py`
- **Dépendances** : Tâche 8
- **Effort estimé** : 1.5 heures
- **Tests à couvrir** :
  - Création de meeting
  - Validation des dates
  - Ajout/suppression de participants
  - Hooks de synchronisation (mockés)

#### 24. Écrire les tests d'intégration OAuth
- **Description** : Tester le flux OAuth complet (avec mocks)
- **Fichiers à créer** :
  - `frappe_app/meeting_management/api/test_google_auth.py`
- **Dépendances** : Tâche 5
- **Effort estimé** : 1.5 heures

#### 25. Créer la documentation utilisateur
- **Description** : Guide d'utilisation de l'application
- **Fichiers à créer** :
  - `docs/user-guide.md`
  - `docs/google-calendar-setup.md`
  - `docs/troubleshooting.md`
- **Dépendances** : Toutes les tâches précédentes
- **Effort estimé** : 2 heures
- **Contenu** :
  - Comment configurer Google Cloud
  - Comment se connecter à Google Calendar
  - Comment créer et gérer des réunions
  - Comment fonctionne la synchronisation
  - FAQ et dépannage

#### 26. Créer la documentation développeur
- **Description** : Documentation technique pour les développeurs
- **Fichiers à créer** :
  - `docs/developer-guide.md`
  - `docs/api-reference.md`
- **Dépendances** : Toutes les tâches précédentes
- **Effort estimé** : 1.5 heures
- **Contenu** :
  - Architecture de l'application
  - Structure des doctypes
  - API methods disponibles
  - Hooks et événements
  - Extension et personnalisation

### Phase 7 : Déploiement et configuration

#### 27. Créer le script d'installation
- **Description** : Hook after_install pour initialiser l'application
- **Fichiers à modifier** :
  - [frappe_app/install.py](frappe_app/install.py)
- **Fichiers à modifier (hooks)** :
  - [frappe_app/hooks.py](frappe_app/hooks.py) - Activer `after_install`
- **Dépendances** : Tâches 4, 8, 9
- **Effort estimé** : 1 heure
- **Actions** :
  - Créer le document Google Calendar Settings
  - Créer les rôles personnalisés (Meeting Manager, Meeting User)
  - Importer les fixtures si nécessaire

#### 28. Créer les fixtures pour les custom fields
- **Description** : Ajouter des custom fields si besoin (ex: sur User)
- **Fichiers à créer/modifier** :
  - `frappe_app/meeting_management/fixtures/custom_field.json`
- **Dépendances** : Tâche 8
- **Effort estimé** : 30 minutes
- **Exemple** : Ajouter un champ "Default Calendar" sur User

#### 29. Configurer les notifications
- **Description** : Notifications par email pour les réunions
- **Fichiers à créer** :
  - Configuration via l'UI Frappe (ou via fixtures)
- **Dépendances** : Tâche 8
- **Effort estimé** : 1 heure
- **Notifications** :
  - Notification de création de réunion aux participants
  - Rappel 1 heure avant la réunion
  - Notification de modification
  - Notification d'annulation

#### 30. Tester le déploiement complet
- **Description** : Installer l'app sur une nouvelle instance et valider
- **Dépendances** : Toutes les tâches précédentes
- **Effort estimé** : 2 heures
- **Checklist** :
  - Installation sans erreur
  - Configuration Google Calendar fonctionnelle
  - Synchronisation bidirectionnelle opérationnelle
  - Tests unitaires passent
  - Interface utilisateur responsive et fonctionnelle

## Points d'intégration dans le code

### Fichiers à modifier

- [frappe_app/hooks.py](frappe_app/hooks.py)
  - Ajouter le module "Meeting Management"
  - Configurer `doc_events` pour Meeting
  - Configurer `scheduler_events` pour la synchronisation
  - Configurer `doctype_js`, `doctype_list_js`, `doctype_calendar_js`
  - Configurer `permission_query_conditions` et `has_permission`
  - Activer `after_install`

- [frappe_app/modules.txt](frappe_app/modules.txt)
  - Ajouter "Meeting Management"

- [requirements.txt](requirements.txt)
  - Ajouter les dépendances Google Calendar API

- [frappe_app/install.py](frappe_app/install.py)
  - Implémenter `after_install()` pour l'initialisation

- [frappe_app/tasks.py](frappe_app/tasks.py)
  - Ajouter `sync_google_calendar_hourly()`

### Nouveaux fichiers à créer

#### Module Meeting Management
- `frappe_app/meeting_management/__init__.py`
- `frappe_app/meeting_management/permissions.py`

#### API Google Calendar
- `frappe_app/meeting_management/api/__init__.py`
- `frappe_app/meeting_management/api/google_auth.py`
- `frappe_app/meeting_management/api/google_calendar.py`
- `frappe_app/meeting_management/api/test_google_auth.py`
- `frappe_app/meeting_management/api/test_google_calendar.py`

#### Doctype: Google Calendar Settings
- `frappe_app/meeting_management/doctype/google_calendar_settings/__init__.py`
- `frappe_app/meeting_management/doctype/google_calendar_settings/google_calendar_settings.json`
- `frappe_app/meeting_management/doctype/google_calendar_settings/google_calendar_settings.py`
- `frappe_app/meeting_management/doctype/google_calendar_settings/google_calendar_settings.js`

#### Doctype: Meeting
- `frappe_app/meeting_management/doctype/meeting/__init__.py`
- `frappe_app/meeting_management/doctype/meeting/meeting.json`
- `frappe_app/meeting_management/doctype/meeting/meeting.py`
- `frappe_app/meeting_management/doctype/meeting/meeting.js`
- `frappe_app/meeting_management/doctype/meeting/meeting_list.js`
- `frappe_app/meeting_management/doctype/meeting/meeting_calendar.js`
- `frappe_app/meeting_management/doctype/meeting/test_meeting.py`

#### Doctype: Meeting Participant
- `frappe_app/meeting_management/doctype/meeting_participant/__init__.py`
- `frappe_app/meeting_management/doctype/meeting_participant/meeting_participant.json`
- `frappe_app/meeting_management/doctype/meeting_participant/meeting_participant.py`

#### Pages Web
- `frappe_app/meeting_management/www/google-callback.py`
- `frappe_app/meeting_management/www/google-callback.html`
- `frappe_app/meeting_management/www/my-meetings.py`
- `frappe_app/meeting_management/www/my-meetings.html`

#### Documentation
- `docs/user-guide.md`
- `docs/google-cloud-setup.md`
- `docs/developer-guide.md`
- `docs/api-reference.md`
- `docs/troubleshooting.md`

#### Fixtures
- `frappe_app/meeting_management/fixtures/custom_field.json`

### Patterns existants à suivre

1. **Doctype Structure** : Suivre le pattern de `sample_doctype`
   - Fichiers JSON, Python, JS dans le même répertoire
   - Tests unitaires avec `TestCase`

2. **API Methods** : Décorer avec `@frappe.whitelist()`
   - Placer dans un module `api/` séparé
   - Retourner des dictionnaires JSON-serializable

3. **Document Hooks** : Implémenter les méthodes dans le controller
   - `validate()`, `after_insert()`, `on_update()`, `on_trash()`

4. **Scheduled Tasks** : Déclarer dans `tasks.py` et référencer dans `hooks.py`

5. **Permissions** : Utiliser `permission_query_conditions` et `has_permission`

6. **Client-side Scripts** : Utiliser `frappe.ui.form.on()` pour les formulaires

7. **List View** : Utiliser `frappe.listview_settings` pour personnaliser

## Conception technique

### Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ERPNext Frontend                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Meeting Form │  │ Meeting List │  │  Calendar View       │  │
│  │  (meeting.js)│  │(meeting_list.│  │(meeting_calendar.js) │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │              │
└─────────┼─────────────────┼──────────────────────┼──────────────┘
          │                 │                      │
          └─────────────────┴──────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Frappe Backend (Python)                      │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Meeting Doctype                        │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  validate()  │ after_insert() │ on_update() │ ...   │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │                                         │
│  ┌─────────────────────▼─────────────────────────────────────┐  │
│  │            Google Calendar Sync Module                    │  │
│  │  ┌───────────────────────────────────────────────────┐    │  │
│  │  │  create_google_event() │ update_google_event()    │    │  │
│  │  │  delete_google_event() │ sync_from_google()       │    │  │
│  │  └───────────────────────────────────────────────────┘    │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │                                         │
│  ┌─────────────────────▼─────────────────────────────────────┐  │
│  │              Google OAuth Module                          │  │
│  │  ┌───────────────────────────────────────────────────┐    │  │
│  │  │  get_authorization_url() │ handle_oauth_callback()│    │  │
│  │  │  refresh_access_token()  │ get_credentials()      │    │  │
│  │  └───────────────────────────────────────────────────┘    │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │                                         │
│  ┌─────────────────────▼─────────────────────────────────────┐  │
│  │          Google Calendar Settings (Doctype)               │  │
│  │  - client_id, client_secret                               │  │
│  │  - access_token, refresh_token (encrypted)                │  │
│  │  - token_expiry, calendar_id                              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               │ OAuth 2.0 Flow
                               │ Calendar API v3
                               ▼
                    ┌──────────────────────┐
                    │  Google Calendar API │
                    │  (calendar.google.   │
                    │   com)                │
                    └──────────────────────┘
```

### Flux de données

#### 1. Authentification Google (Flux OAuth2)
```
User clicks "Connect Google"
  → get_authorization_url() generates OAuth URL
  → User redirects to Google consent screen
  → Google redirects to /google-callback with code
  → handle_oauth_callback(code) exchanges code for tokens
  → Tokens stored in Google Calendar Settings (encrypted)
  → Settings.sync_status = "Connected"
```

#### 2. Création d'une réunion (ERPNext → Google Calendar)
```
User creates Meeting in ERPNext
  → Meeting.validate() checks dates
  → Meeting.after_insert() triggered
  → sync_to_google_after_insert() called
  → create_google_event(meeting_doc) creates event in Google
  → Google returns event_id and link
  → Meeting.google_event_id and google_calendar_link updated
  → Meeting.synced_with_google = True
```

#### 3. Modification d'une réunion (ERPNext → Google Calendar)
```
User updates Meeting in ERPNext
  → Meeting.validate() checks dates
  → Meeting.on_update() triggered
  → sync_to_google_on_update() called
  → update_google_event(meeting_doc) updates event in Google
  → Meeting.last_synced updated
```

#### 4. Synchronisation depuis Google Calendar (Google → ERPNext)
```
Scheduled task runs hourly
  → sync_google_calendar_hourly() called
  → sync_from_google() fetches events since last_sync
  → For each Google event:
      - Check if Meeting exists (by google_event_id)
      - If exists: Update Meeting if Google event is newer
      - If not exists: Create new Meeting
  → Settings.last_sync updated
```

#### 5. Suppression d'une réunion (ERPNext → Google Calendar)
```
User deletes Meeting in ERPNext
  → Meeting.on_trash() triggered
  → delete_from_google() called
  → delete_google_event(google_event_id) deletes event in Google
  → Meeting deleted from ERPNext
```

### Points d'API

#### APIs publiques (whitelisted)

**Google OAuth**
- `POST frappe_app.meeting_management.api.google_auth.get_authorization_url`
  - Retourne l'URL d'autorisation OAuth Google
  - Paramètres : Aucun
  - Retour : `{"authorization_url": "https://accounts.google.com/..."}`

- `POST frappe_app.meeting_management.api.google_auth.handle_oauth_callback`
  - Traite le callback OAuth et stocke les tokens
  - Paramètres : `code` (string)
  - Retour : `{"success": true, "message": "Connected to Google Calendar"}`

- `POST frappe_app.meeting_management.api.google_auth.disconnect_google`
  - Déconnecte le compte Google
  - Paramètres : Aucun
  - Retour : `{"success": true, "message": "Disconnected"}`

**Google Calendar Sync**
- `POST frappe_app.meeting_management.api.google_calendar.sync_meeting_to_google`
  - Synchronise un meeting spécifique vers Google
  - Paramètres : `meeting_id` (string)
  - Retour : `{"success": true, "google_event_id": "...", "google_calendar_link": "..."}`

- `POST frappe_app.meeting_management.api.google_calendar.sync_from_google_now`
  - Déclenche une synchronisation immédiate depuis Google
  - Paramètres : Aucun
  - Retour : `{"success": true, "events_synced": 5, "meetings_created": 2, "meetings_updated": 3}`

**Meeting APIs**
- `GET frappe_app.meeting_management.doctype.meeting.meeting.get_events`
  - Récupère les événements pour la vue calendrier
  - Paramètres : `start` (datetime), `end` (datetime)
  - Retour : `[{"name": "MTG-001", "title": "...", "start": "...", "end": "..."}]`

#### APIs internes (non-whitelisted)

- `refresh_access_token()` : Rafraîchit le token d'accès expiré
- `get_credentials()` : Récupère les credentials OAuth valides
- `build_calendar_service()` : Construit le client API Google Calendar
- `create_google_event(meeting_doc)` : Crée un événement Google
- `update_google_event(meeting_doc)` : Met à jour un événement Google
- `delete_google_event(google_event_id)` : Supprime un événement Google
- `get_google_event(google_event_id)` : Récupère un événement Google
- `list_google_events(time_min, time_max)` : Liste les événements Google

## Dépendances et bibliothèques

### Python (à ajouter dans requirements.txt)
- **google-api-python-client>=2.0.0** : Client officiel Google API Python
- **google-auth-httplib2>=0.1.0** : Authentification Google avec httplib2
- **google-auth-oauthlib>=1.0.0** : Flux OAuth2 pour Google APIs

### Frappe Framework
- Déjà fourni par Frappe/ERPNext (pas besoin d'installer)

### JavaScript (Frontend)
- Déjà fourni par Frappe (jQuery, Vue.js selon version)

## Stratégie de test

### Tests unitaires

**Module google_auth** (`test_google_auth.py`)
- Tester `get_authorization_url()` génère une URL valide
- Tester `handle_oauth_callback()` avec un code valide (mocké)
- Tester `refresh_access_token()` renouvelle le token
- Tester la gestion des erreurs OAuth (token expiré, invalide)

**Module google_calendar** (`test_google_calendar.py`)
- Tester `create_google_event()` avec mocks de l'API Google
- Tester `update_google_event()` avec différents scénarios
- Tester `delete_google_event()` supprime l'événement
- Tester `sync_from_google()` crée/met à jour les meetings correctement
- Tester la gestion des erreurs API (rate limit, network error)

**Doctype Meeting** (`test_meeting.py`)
- Tester la création d'un meeting valide
- Tester la validation : end_datetime > start_datetime
- Tester l'ajout/suppression de participants
- Tester les hooks (mockés) : after_insert, on_update, on_trash
- Tester le calcul de la durée

**Doctype Meeting Participant** (`test_meeting_participant.py`)
- Tester la validation des emails
- Tester les statuts de réponse

### Tests d'intégration

**Flux OAuth complet**
- Tester le flux complet avec Google OAuth playground (manuel ou automatisé avec Selenium)

**Synchronisation bidirectionnelle**
- Créer un meeting dans ERPNext, vérifier qu'il apparaît dans Google Calendar
- Modifier un meeting dans ERPNext, vérifier la mise à jour dans Google
- Créer un événement dans Google Calendar, exécuter sync, vérifier qu'il apparaît dans ERPNext
- Supprimer un meeting dans ERPNext, vérifier la suppression dans Google

**Scheduled sync**
- Tester que la tâche planifiée s'exécute correctement
- Tester la réconciliation des conflits (modification simultanée)

### Tests de permissions

- Tester qu'un utilisateur voit uniquement ses meetings
- Tester qu'un utilisateur voit les meetings où il est participant
- Tester que System Manager voit tous les meetings

### Cas limites à couvrir

- **Token expiré** : Vérifier le refresh automatique
- **Pas de connexion internet** : Gérer gracieusement, mettre en queue
- **Rate limiting Google API** : Implémenter backoff exponentiel
- **Conflits de synchronisation** : Dernière modification gagne
- **Événements récurrents** : Gérer ou exclure (Phase 2)
- **Fuseaux horaires** : Gérer correctement les timezones
- **Participants invalides** : Validation des emails
- **Réunions très longues** : Validation de durée max (optionnel)

## Critères de succès

### Fonctionnels
- [ ] Un utilisateur peut se connecter à son compte Google via OAuth2
- [ ] Les tokens OAuth sont stockés de manière sécurisée et rafraîchis automatiquement
- [ ] Un utilisateur peut créer une réunion dans ERPNext
- [ ] La réunion créée apparaît automatiquement dans Google Calendar
- [ ] La modification d'une réunion dans ERPNext se reflète dans Google Calendar
- [ ] La suppression d'une réunion dans ERPNext supprime l'événement de Google Calendar
- [ ] La synchronisation planifiée importe les événements de Google Calendar toutes les heures
- [ ] Les événements créés dans Google Calendar apparaissent dans ERPNext après la synchro
- [ ] Un utilisateur peut ajouter plusieurs participants à une réunion
- [ ] La vue calendrier affiche correctement les réunions
- [ ] La vue liste affiche les indicateurs de statut et de synchronisation
- [ ] Les permissions limitent la visibilité des réunions aux utilisateurs autorisés

### Techniques
- [ ] Tous les tests unitaires passent (`bench run-tests --app frappe_app`)
- [ ] Les tests d'intégration OAuth fonctionnent
- [ ] Les tests de synchronisation bidirectionnelle fonctionnent
- [ ] Aucune erreur dans les logs en conditions normales
- [ ] La gestion des erreurs est gracieuse (messages clairs, pas de crash)
- [ ] Les performances sont acceptables (< 2s pour créer un meeting et sync)
- [ ] La synchronisation planifiée s'exécute sans erreur

### Sécurité
- [ ] Les tokens OAuth ne sont jamais exposés dans les logs ou API responses
- [ ] Les champs Password sont bien chiffrés en base de données
- [ ] Les permissions query conditions filtrent correctement les données
- [ ] L'API OAuth callback valide le state parameter (CSRF protection)

### Documentation
- [ ] La documentation utilisateur est complète et claire
- [ ] La documentation développeur explique l'architecture
- [ ] Le guide de configuration Google Cloud est détaillé
- [ ] La documentation de dépannage couvre les problèmes courants

### Déploiement
- [ ] L'installation sur une nouvelle instance fonctionne sans erreur
- [ ] Le hook `after_install` initialise correctement l'application
- [ ] Les migrations fonctionnent correctement
- [ ] L'application peut être désinstallée proprement

## Notes et considérations

### Défis potentiels

1. **Gestion des fuseaux horaires**
   - ERPNext et Google Calendar peuvent avoir des fuseaux horaires différents
   - Solution : Toujours stocker en UTC, convertir à l'affichage

2. **Conflits de synchronisation**
   - Modification simultanée dans ERPNext et Google Calendar
   - Solution : Dernière modification gagne (based on updated timestamp)

3. **Rate limiting Google API**
   - Google Calendar API a des limites de requêtes
   - Solution : Implémenter un backoff exponentiel, batching si possible

4. **Événements récurrents**
   - Google Calendar supporte les récurrences (RRULE)
   - Solution Phase 1 : Exclure les récurrences (ou les importer comme événements uniques)
   - Solution Phase 2 : Implémenter un doctype "Meeting Series"

5. **Multi-calendriers**
   - Un utilisateur peut avoir plusieurs calendriers Google
   - Solution Phase 1 : Synchroniser uniquement le calendrier principal
   - Solution Phase 2 : Permettre de choisir le calendrier

6. **Sécurité des tokens**
   - Les tokens OAuth doivent être stockés de manière ultra-sécurisée
   - Solution : Utiliser les champs Password de Frappe (chiffrement AES)

7. **Refresh token invalidé**
   - Si l'utilisateur révoque l'accès, le refresh token devient invalide
   - Solution : Détecter l'erreur, mettre sync_status = "Error", notifier l'utilisateur

### Améliorations futures (Phase 2+)

- **Webhook Google Calendar** : Recevoir des notifications push pour synchro temps réel
- **Événements récurrents** : Support complet des récurrences
- **Multi-calendriers** : Synchroniser plusieurs calendriers Google
- **Intégration vidéo** : Créer automatiquement des liens Google Meet
- **Gestion des pièces jointes** : Synchroniser les fichiers joints
- **Rappels personnalisés** : Configurer des rappels par email/SMS
- **Analytics** : Statistiques sur les réunions (durée, participants, taux d'acceptation)
- **Templates de réunions** : Créer des templates réutilisables
- **Conflict detection** : Détecter les conflits d'agenda avant création
- **Intégration Outlook/Office 365** : Support d'autres calendriers

### Considérations de performance

- **Batch sync** : Pour les utilisateurs avec beaucoup d'événements, paginer les requêtes
- **Caching** : Mettre en cache les credentials pour éviter les requêtes DB répétées
- **Async tasks** : Utiliser Frappe's background jobs pour les synchros longues
- **Indexing** : Ajouter des index sur google_event_id pour recherche rapide

### Considérations de conformité

- **RGPD** : Les tokens OAuth sont des données personnelles
  - Permettre aux utilisateurs de supprimer leurs données
  - Implémenter le droit à l'oubli
- **Scopes OAuth** : Demander uniquement les scopes nécessaires
  - `https://www.googleapis.com/auth/calendar.events` : Gérer les événements
  - Ne pas demander de scopes trop larges

---

## Prochaines étapes

### Commencer l'implémentation

Pour exécuter ce plan :

```bash
/execute-plan PRPs/meeting-management-google-calendar.md
```

### Priorisation suggérée

**Sprint 1 (Semaine 1)** : Phase 1 - Configuration et authentification Google
- Tâches 1-7 : OAuth fonctionnel

**Sprint 2 (Semaine 2)** : Phase 2 - Doctypes de base
- Tâches 8-10 : Doctypes Meeting et Meeting Participant

**Sprint 3 (Semaine 3)** : Phase 3 - Synchronisation
- Tâches 11-14 : Synchronisation bidirectionnelle

**Sprint 4 (Semaine 4)** : Phase 4 & 5 - UI et Permissions
- Tâches 15-21 : Interface et sécurité

**Sprint 5 (Semaine 5)** : Phase 6 & 7 - Tests et Déploiement
- Tâches 22-30 : Tests, documentation, déploiement

### Contact et support

Pour toute question ou problème durant l'implémentation, se référer à :
- Documentation Frappe : https://docs.frappe.io
- Documentation Google Calendar API : https://developers.google.com/calendar
- Forum Frappe : https://discuss.frappe.io

---

*Ce plan est prêt à être exécuté avec `/execute-plan PRPs/meeting-management-google-calendar.md`*
