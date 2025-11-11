# 📑 Index de la Documentation

Bienvenue dans le Template Frappe ! Ce fichier vous guide vers toutes les ressources disponibles.

## 🚀 Pour Démarrer

### Nouveaux Utilisateurs

1. **[README.md](README.md)** ⭐ COMMENCER ICI
   - Vue d'ensemble du template
   - Fonctionnalités principales
   - Installation rapide
   - Liens vers les autres ressources

2. **[QUICK_START.md](QUICK_START.md)** 📖 GUIDE PAS-À-PAS
   - Instructions détaillées étape par étape
   - Personnalisation de l'application
   - Création de DocTypes
   - Exemples de code
   - Commandes utiles

### Développeurs Expérimentés

3. **[FRAPPE_APP_TEMPLATE.md](FRAPPE_APP_TEMPLATE.md)** 📚 RÉFÉRENCE COMPLÈTE
   - Structure détaillée du projet
   - Explication de chaque fichier
   - Tous les hooks Frappe disponibles
   - Bonnes pratiques
   - Guide complet des fonctionnalités

## 📁 Documentation Technique

### Architecture & Structure

4. **[STRUCTURE.md](STRUCTURE.md)** 🗂️ ARBORESCENCE
   - Arborescence complète du projet
   - Description de chaque fichier et dossier
   - Tableaux récapitulatifs
   - Statistiques du template

5. **[ARCHITECTURE.md](ARCHITECTURE.md)** 🏗️ ARCHITECTURE
   - Diagrammes de l'architecture
   - Flux de données et requêtes
   - Cycle de vie des documents
   - Système de permissions
   - Tâches planifiées
   - Pages web et API

### Utilisation Pratique

6. **[SUMMARY.txt](SUMMARY.txt)** 📊 RÉSUMÉ VISUEL
   - Vue d'ensemble en un coup d'œil
   - Statistiques du template
   - Checklist de démarrage
   - Commandes essentielles

7. **Script [rename_app.py](rename_app.py)** 🔧 RENOMMAGE AUTO
   - Script Python pour renommer l'app
   - Usage : `python rename_app.py mon_app "Mon App" "Société" "email"`
   - Met à jour tous les fichiers automatiquement

## 🤝 Contribution & Maintenance

8. **[CONTRIBUTING.md](CONTRIBUTING.md)** 💡 GUIDE DE CONTRIBUTION
   - Comment contribuer au projet
   - Standards de code
   - Processus de Pull Request
   - Messages de commit
   - Tests

9. **[CHANGELOG.md](CHANGELOG.md)** 📝 HISTORIQUE
   - Journal des versions
   - Liste des fonctionnalités ajoutées
   - Corrections de bugs
   - Améliorations

## 🛠️ Configuration & Développement

10. **[CLAUDE.md](CLAUDE.md)** 🤖 INSTRUCTIONS CLAUDE CODE
    - Instructions pour Claude Code
    - Objectifs du projet
    - Architecture de l'application
    - DocTypes à implémenter
    - Commandes de développement

## 📦 Fichiers de Code Essentiels

### Configuration Racine

| Fichier | Description | Lien |
|---------|-------------|------|
| `setup.py` | Configuration setuptools | [setup.py](setup.py) |
| `pyproject.toml` | Config Python moderne | [pyproject.toml](pyproject.toml) |
| `requirements.txt` | Dépendances Python | [requirements.txt](requirements.txt) |
| `MANIFEST.in` | Inclusion package | [MANIFEST.in](MANIFEST.in) |
| `.gitignore` | Exclusions Git | [.gitignore](.gitignore) |
| `.editorconfig` | Config éditeur | [.editorconfig](.editorconfig) |

### Module Principal (frappe_app/)

| Fichier | Description | Lien |
|---------|-------------|------|
| `hooks.py` | ⭐ Configuration centrale | [frappe_app/hooks.py](frappe_app/hooks.py) |
| `__init__.py` | Version de l'app | [frappe_app/__init__.py](frappe_app/__init__.py) |
| `modules.txt` | Liste des modules | [frappe_app/modules.txt](frappe_app/modules.txt) |
| `patches.txt` | Liste des patches | [frappe_app/patches.txt](frappe_app/patches.txt) |
| `install.py` | Installation/Désinstallation | [frappe_app/install.py](frappe_app/install.py) |
| `tasks.py` | Tâches planifiées | [frappe_app/tasks.py](frappe_app/tasks.py) |
| `utils.py` | Utilitaires & API | [frappe_app/utils.py](frappe_app/utils.py) |
| `permissions.py` | Permissions custom | [frappe_app/permissions.py](frappe_app/permissions.py) |

### Configuration

| Fichier | Description | Lien |
|---------|-------------|------|
| `config/desktop.py` | Icônes du bureau | [frappe_app/config/desktop.py](frappe_app/config/desktop.py) |
| `config/docs.py` | Config documentation | [frappe_app/config/docs.py](frappe_app/config/docs.py) |

### Exemple de DocType

| Fichier | Description | Lien |
|---------|-------------|------|
| `sample_doctype.json` | Définition du DocType | [frappe_app/frappe_app/doctype/sample_doctype/sample_doctype.json](frappe_app/frappe_app/doctype/sample_doctype/sample_doctype.json) |
| `sample_doctype.py` | Controller Python | [frappe_app/frappe_app/doctype/sample_doctype/sample_doctype.py](frappe_app/frappe_app/doctype/sample_doctype/sample_doctype.py) |
| `test_sample_doctype.py` | Tests unitaires | [frappe_app/frappe_app/doctype/sample_doctype/test_sample_doctype.py](frappe_app/frappe_app/doctype/sample_doctype/test_sample_doctype.py) |

### Assets Frontend

| Fichier | Description | Lien |
|---------|-------------|------|
| `frappe_app.bundle.js` | Bundle JS principal | [frappe_app/public/js/frappe_app.bundle.js](frappe_app/public/js/frappe_app.bundle.js) |
| `doctype_example.js` | Script formulaire | [frappe_app/public/js/doctype_example.js](frappe_app/public/js/doctype_example.js) |
| `list_view_example.js` | Script liste | [frappe_app/public/js/list_view_example.js](frappe_app/public/js/list_view_example.js) |
| `frappe_app.css` | CSS global | [frappe_app/public/css/frappe_app.css](frappe_app/public/css/frappe_app.css) |

### Page Web Exemple

| Fichier | Description | Lien |
|---------|-------------|------|
| `example-page.py` | Controller Python | [frappe_app/www/example-page.py](frappe_app/www/example-page.py) |
| `example-page.html` | Template HTML | [frappe_app/www/example-page.html](frappe_app/www/example-page.html) |

### Fixtures & Patches

| Fichier | Description | Lien |
|---------|-------------|------|
| `custom_field.json` | Fixture exemple | [frappe_app/fixtures/custom_field.json](frappe_app/fixtures/custom_field.json) |
| `example_patch.py` | Patch migration | [frappe_app/patches/v0_1/example_patch.py](frappe_app/patches/v0_1/example_patch.py) |

### Tests

| Fichier | Description | Lien |
|---------|-------------|------|
| `test_utils.py` | Tests utilitaires | [frappe_app/tests/test_utils.py](frappe_app/tests/test_utils.py) |

## 🎯 Parcours d'Apprentissage Recommandé

### Niveau Débutant

```
1. README.md
   ↓
2. QUICK_START.md
   ↓
3. SUMMARY.txt
   ↓
4. Utiliser rename_app.py
   ↓
5. Installer et tester
```

### Niveau Intermédiaire

```
1. STRUCTURE.md
   ↓
2. FRAPPE_APP_TEMPLATE.md
   ↓
3. Examiner sample_doctype
   ↓
4. Créer vos propres DocTypes
   ↓
5. Ajouter des hooks personnalisés
```

### Niveau Avancé

```
1. ARCHITECTURE.md
   ↓
2. permissions.py (permissions custom)
   ↓
3. tasks.py (scheduler)
   ↓
4. Intégrations & API
   ↓
5. CONTRIBUTING.md (contribuer)
```

## 🔍 Recherche Rapide

### Par Sujet

- **Installation** → README.md, QUICK_START.md
- **Configuration** → FRAPPE_APP_TEMPLATE.md, hooks.py
- **DocTypes** → QUICK_START.md, sample_doctype/
- **Permissions** → ARCHITECTURE.md, permissions.py
- **API** → FRAPPE_APP_TEMPLATE.md, utils.py
- **Pages Web** → ARCHITECTURE.md, www/
- **Tests** → CONTRIBUTING.md, tests/
- **Migration** → patches.txt, patches/
- **Frontend** → public/js/, public/css/

### Par Type de Fichier

- **📚 Documentation** → README.md, QUICK_START.md, etc.
- **🐍 Python** → *.py
- **📜 JavaScript** → public/js/*.js
- **🎨 CSS** → public/css/*.css
- **📋 JSON** → *.json
- **⚙️ Config** → setup.py, pyproject.toml, hooks.py

## 📞 Support & Ressources

### Ressources Officielles Frappe

- **Documentation** : https://frappeframework.com/docs
- **API Reference** : https://frappeframework.com/docs/user/en/api
- **Forum** : https://discuss.frappe.io
- **GitHub** : https://github.com/frappe/frappe

### Ce Template

- **Issues** : Signaler des bugs ou demander des fonctionnalités
- **Discussions** : Poser des questions
- **Pull Requests** : Contribuer au projet

## 📊 Statistiques du Template

- **Total de fichiers** : ~51
- **Fichiers Python** : 20
- **Fichiers JavaScript** : 3
- **Documentation** : 8 fichiers
- **Exemples de code** : Complets et commentés
- **Tests** : Inclus et fonctionnels

## ✅ Checklist de Démarrage

- [ ] Lire README.md
- [ ] Suivre QUICK_START.md
- [ ] Renommer l'app avec rename_app.py
- [ ] Installer sur Frappe bench
- [ ] Tester l'app de base
- [ ] Créer vos modules
- [ ] Créer vos DocTypes
- [ ] Ajouter vos hooks
- [ ] Écrire des tests
- [ ] Consulter CONTRIBUTING.md

## 🎉 Vous Êtes Prêt !

Avec toutes ces ressources, vous avez tout ce qu'il faut pour créer une application Frappe professionnelle.

**Bon développement !** 🚀

---

*Dernière mise à jour : 2024-10-05*

*Template maintenu avec ❤️ pour la communauté Frappe*
