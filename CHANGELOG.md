# Changelog

Toutes les modifications notables de ce template seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### À venir
- Exemples de rapports personnalisés
- Exemples d'intégration avec d'autres apps
- Exemples de workflows
- Exemples de print formats
- Exemples de dashboards
- Guide de déploiement en production

## [1.0.0] - 2024-10-05

### Ajouté
- Structure complète d'une application Frappe
- Fichier `hooks.py` avec tous les hooks commentés
- Exemple de DocType complet (Sample Doctype)
- Controller Python avec tous les événements du document
- Tests unitaires pour le DocType
- Scripts client JavaScript (formulaire et liste)
- Exemple de page web (`www/example-page`)
- Système de permissions personnalisées
- Tâches planifiées (scheduler tasks)
- Fonctions utilitaires et API endpoints
- Scripts d'installation/désinstallation
- Configuration du bureau (desktop icons)
- Exemple de fixture (custom field)
- Exemple de patch de migration
- Tests unitaires pour les utils
- Documentation complète en français :
  - README.md principal
  - QUICK_START.md pour démarrer rapidement
  - FRAPPE_APP_TEMPLATE.md documentation détaillée
  - STRUCTURE.md arborescence du projet
  - CLAUDE.md instructions pour Claude Code
- Script de renommage automatique (`rename_app.py`)
- Fichiers de configuration :
  - `.gitignore`
  - `.editorconfig`
  - `MANIFEST.in`
  - `pyproject.toml`
  - `setup.py`
  - `requirements.txt`

### Caractéristiques

#### Fichiers Python (15)
- `frappe_app/__init__.py` - Version de l'app
- `frappe_app/hooks.py` - Configuration centrale
- `frappe_app/install.py` - Installation
- `frappe_app/tasks.py` - Tâches planifiées
- `frappe_app/utils.py` - Utilitaires et API
- `frappe_app/permissions.py` - Permissions custom
- `frappe_app/config/desktop.py` - Configuration bureau
- `frappe_app/config/docs.py` - Configuration docs
- `frappe_app/frappe_app/doctype/sample_doctype/sample_doctype.py` - Controller
- `frappe_app/frappe_app/doctype/sample_doctype/test_sample_doctype.py` - Tests
- `frappe_app/patches/v0_1/example_patch.py` - Patch exemple
- `frappe_app/tests/test_utils.py` - Tests utils
- `frappe_app/www/example-page.py` - Page web
- `setup.py` - Configuration setup
- `rename_app.py` - Script de renommage

#### Fichiers JavaScript (3)
- `frappe_app/public/js/frappe_app.bundle.js` - Bundle principal
- `frappe_app/public/js/doctype_example.js` - Exemple DocType
- `frappe_app/public/js/list_view_example.js` - Exemple List View

#### Fichiers JSON (2)
- `frappe_app/frappe_app/doctype/sample_doctype/sample_doctype.json` - Définition DocType
- `frappe_app/fixtures/custom_field.json` - Fixture exemple

#### Fichiers HTML (1)
- `frappe_app/www/example-page.html` - Template page web

#### Fichiers CSS (1)
- `frappe_app/public/css/frappe_app.css` - Styles globaux

#### Documentation (5)
- `README.md` - Documentation principale
- `QUICK_START.md` - Guide démarrage rapide
- `FRAPPE_APP_TEMPLATE.md` - Documentation détaillée
- `STRUCTURE.md` - Arborescence
- `CLAUDE.md` - Instructions Claude Code
- `CHANGELOG.md` - Ce fichier

#### Configuration (6)
- `pyproject.toml` - Config Python moderne
- `setup.py` - Config Python legacy
- `requirements.txt` - Dépendances
- `.gitignore` - Exclusions Git
- `.editorconfig` - Config éditeur
- `MANIFEST.in` - Inclusion package

### Total
**~35 fichiers** prêts à l'emploi pour démarrer votre projet Frappe !

## Notes de Version

### v1.0.0 - Template Initial
Cette première version fournit une base solide pour créer des applications Frappe :
- Tous les fichiers essentiels sont inclus
- Exemples de code pour chaque fonctionnalité
- Documentation complète en français
- Script de renommage pour faciliter la personnalisation

Le template suit les meilleures pratiques Frappe et inclut des exemples pour :
- DocTypes et controllers
- Permissions personnalisées
- Tâches planifiées
- Pages web publiques
- API endpoints
- Tests unitaires
- Migrations de base de données

---

**Note** : Ce template est maintenu activement. N'hésitez pas à signaler des bugs ou suggérer des améliorations via les Issues GitHub.
