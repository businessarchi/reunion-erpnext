# 📂 Structure Complète du Template Frappe

Ce document présente l'arborescence complète du template avec la description de chaque fichier.

## 🌳 Arborescence Complète

```
modele-frappe/
│
├── 📄 README.md                              # Documentation principale du projet
├── 📄 LICENSE                                # Licence MIT
├── 📄 QUICK_START.md                        # Guide de démarrage rapide
├── 📄 FRAPPE_APP_TEMPLATE.md               # Documentation détaillée
├── 📄 STRUCTURE.md                          # Ce fichier - structure du projet
├── 📄 CLAUDE.md                             # Instructions pour Claude Code
│
├── 📄 setup.py                              # Configuration Python (legacy)
├── 📄 pyproject.toml                        # Configuration Python moderne
├── 📄 requirements.txt                      # Dépendances Python
├── 📄 MANIFEST.in                           # Fichiers à inclure dans le package
├── 📄 .gitignore                            # Fichiers à ignorer par Git
├── 📄 .editorconfig                         # Configuration de l'éditeur
│
└── 📁 frappe_app/                           # MODULE PRINCIPAL
    │
    ├── 📄 __init__.py                       # Version de l'application
    ├── 📄 hooks.py                          # Configuration centrale Frappe
    ├── 📄 modules.txt                       # Liste des modules
    ├── 📄 patches.txt                       # Liste des patches de migration
    ├── 📄 install.py                        # Scripts installation/désinstallation
    ├── 📄 tasks.py                          # Tâches planifiées (scheduler)
    ├── 📄 utils.py                          # Fonctions utilitaires et API
    ├── 📄 permissions.py                    # Logique de permissions custom
    │
    ├── 📁 config/                           # CONFIGURATION
    │   ├── 📄 desktop.py                   # Configuration des icônes du bureau
    │   └── 📄 docs.py                      # Configuration de la documentation
    │
    ├── 📁 frappe_app/                       # MODULE "Frappe App"
    │   ├── 📄 __init__.py
    │   └── 📁 doctype/                     # DOCTYPES DU MODULE
    │       ├── 📄 __init__.py
    │       └── 📁 sample_doctype/          # EXEMPLE DE DOCTYPE
    │           ├── 📄 __init__.py
    │           ├── 📄 sample_doctype.json  # Définition du DocType
    │           ├── 📄 sample_doctype.py    # Controller Python
    │           └── 📄 test_sample_doctype.py # Tests unitaires
    │
    ├── 📁 public/                           # ASSETS STATIQUES
    │   ├── 📁 js/                          # JavaScript
    │   │   ├── 📄 frappe_app.bundle.js    # Bundle JS principal
    │   │   ├── 📄 doctype_example.js      # Exemple script DocType
    │   │   └── 📄 list_view_example.js    # Exemple script List View
    │   └── 📁 css/                         # Styles CSS
    │       └── 📄 frappe_app.css          # CSS principal
    │
    ├── 📁 templates/                        # TEMPLATES JINJA2
    │   ├── 📄 .gitkeep
    │   ├── 📁 pages/                       # Templates de pages
    │   │   └── 📄 .gitkeep
    │   └── 📁 includes/                    # Includes réutilisables
    │       └── 📄 .gitkeep
    │
    ├── 📁 www/                              # PAGES WEB PUBLIQUES
    │   ├── 📄 .gitkeep
    │   ├── 📄 example-page.py             # Controller de page
    │   └── 📄 example-page.html           # Template de page
    │
    ├── 📁 fixtures/                         # DONNÉES INITIALES
    │   ├── 📄 .gitkeep
    │   └── 📄 custom_field.json           # Exemple de fixture
    │
    ├── 📁 patches/                          # PATCHES DE MIGRATION
    │   ├── 📄 .gitkeep
    │   └── 📁 v0_1/                        # Patches version 0.1
    │       ├── 📄 __init__.py
    │       └── 📄 example_patch.py        # Exemple de patch
    │
    └── 📁 tests/                            # TESTS UNITAIRES
        ├── 📄 __init__.py
        └── 📄 test_utils.py               # Tests pour utils.py
```

## 📝 Description des Fichiers

### 📁 Racine du Projet

| Fichier | Description |
|---------|-------------|
| `README.md` | Documentation principale avec présentation du template |
| `LICENSE` | Licence MIT du projet |
| `QUICK_START.md` | Guide de démarrage rapide pas-à-pas |
| `FRAPPE_APP_TEMPLATE.md` | Documentation complète et détaillée |
| `STRUCTURE.md` | Ce fichier - arborescence du projet |
| `CLAUDE.md` | Instructions pour Claude Code |
| `setup.py` | Configuration setuptools (legacy) |
| `pyproject.toml` | Configuration Python moderne (PEP 621) |
| `requirements.txt` | Dépendances Python |
| `MANIFEST.in` | Fichiers à inclure dans le package distribué |
| `.gitignore` | Fichiers à exclure du contrôle de version |
| `.editorconfig` | Configuration de style de code |

### 📁 frappe_app/ (Module Principal)

| Fichier | Description | Hook dans hooks.py |
|---------|-------------|--------------------|
| `__init__.py` | Définit la version de l'app (`__version__`) | - |
| `hooks.py` | **Fichier central** de configuration Frappe | - |
| `modules.txt` | Liste des modules de l'app | - |
| `patches.txt` | Liste ordonnée des patches à exécuter | - |
| `install.py` | Scripts avant/après installation | `after_install`, `before_install` |
| `tasks.py` | Tâches planifiées (cron) | `scheduler_events` |
| `utils.py` | Fonctions utilitaires et API endpoints | `jinja.methods`, etc. |
| `permissions.py` | Logique de permissions personnalisée | `permission_query_conditions`, `has_permission` |

### 📁 config/

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| `desktop.py` | Configuration des icônes du bureau ERPNext | Définir l'icône de votre module |
| `docs.py` | Configuration de la documentation | Lier vers votre documentation GitHub |

### 📁 frappe_app/frappe_app/doctype/

Structure standard d'un DocType Frappe :

| Fichier | Description | Requis |
|---------|-------------|--------|
| `__init__.py` | Fichier Python vide | ✅ Oui |
| `[doctype].json` | Définition du DocType (champs, permissions) | ✅ Oui |
| `[doctype].py` | Controller Python (logique métier) | ✅ Oui |
| `[doctype].js` | Script client pour le formulaire | ❌ Optionnel |
| `[doctype]_list.js` | Script client pour la vue liste | ❌ Optionnel |
| `[doctype]_calendar.js` | Configuration vue calendrier | ❌ Optionnel |
| `[doctype]_tree.js` | Configuration vue arbre | ❌ Optionnel |
| `test_[doctype].py` | Tests unitaires | ✅ Recommandé |
| `[doctype].html` | Template d'impression | ❌ Optionnel |

### 📁 public/

| Dossier/Fichier | Description | Inclusion |
|-----------------|-------------|-----------|
| `js/frappe_app.bundle.js` | JavaScript global de l'app | `app_include_js` |
| `js/doctype_example.js` | Script spécifique à un DocType | `doctype_js` |
| `js/list_view_example.js` | Script pour vue liste | `doctype_list_js` |
| `css/frappe_app.css` | Styles CSS globaux | `app_include_css` |

### 📁 templates/

| Dossier | Description | Usage |
|---------|-------------|-------|
| `pages/` | Templates de pages web | Utilisé par `www/` |
| `includes/` | Fragments réutilisables | Inclus dans d'autres templates |

### 📁 www/

Pages web accessibles publiquement :

| Type de fichier | Description | URL |
|----------------|-------------|-----|
| `example-page.py` | Controller Python | - |
| `example-page.html` | Template Jinja2 | `/example-page` |

**Structure** : Pour une page `/ma-page`, créez :
- `www/ma-page.py` (controller)
- `www/ma-page.html` (template)

### 📁 fixtures/

| Fichier | Description | Format |
|---------|-------------|--------|
| `custom_field.json` | Champs personnalisés | JSON |
| `*.json` | Autres fixtures | JSON |

**Export** : `bench export-fixtures`

### 📁 patches/

| Structure | Description | Référence |
|-----------|-------------|-----------|
| `v0_1/example_patch.py` | Patch de migration version 0.1 | Ajouté dans `patches.txt` |

**Format** : `frappe_app.patches.v0_1.example_patch`

### 📁 tests/

| Fichier | Description | Exécution |
|---------|-------------|-----------|
| `test_utils.py` | Tests des fonctions utilitaires | `bench run-tests` |
| `test_*.py` | Autres tests | `bench run-tests` |

## 🔑 Fichiers Clés à Personnaliser

Lors de la création de votre app à partir de ce template, modifiez en priorité :

1. ✅ **pyproject.toml** - Nom, auteur, description
2. ✅ **setup.py** - Nom, auteur, version
3. ✅ **hooks.py** - `app_name`, `app_title`, etc.
4. ✅ **frappe_app/__init__.py** - Version
5. ✅ **modules.txt** - Noms de vos modules
6. ✅ **README.md** - Documentation de votre app

## 📊 Statistiques du Template

- **Fichiers Python** : 15
- **Fichiers JavaScript** : 3
- **Fichiers JSON** : 2
- **Fichiers HTML** : 1
- **Fichiers CSS** : 1
- **Fichiers Markdown** : 4
- **Fichiers de configuration** : 5

**Total** : ~31 fichiers prêts à l'emploi

## 🎯 Prochaines Étapes

1. Cloner ce template
2. Renommer `frappe_app` avec le nom de votre app
3. Personnaliser les fichiers de configuration
4. Créer vos modules et DocTypes
5. Implémenter votre logique métier
6. Tester et déployer

## 📚 Ressources

- [QUICK_START.md](QUICK_START.md) - Démarrer rapidement
- [FRAPPE_APP_TEMPLATE.md](FRAPPE_APP_TEMPLATE.md) - Documentation détaillée
- [Documentation Frappe](https://frappeframework.com/docs)

---

**Template créé avec ❤️ pour faciliter le développement d'apps Frappe**
