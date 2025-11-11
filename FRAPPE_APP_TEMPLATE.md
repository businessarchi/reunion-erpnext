# Frappe App Template - Structure et Utilisation

Ce projet est un modèle (template) pour créer des applications Frappe personnalisées. Il contient tous les fichiers et dossiers nécessaires pour démarrer rapidement le développement d'une nouvelle app Frappe.

## 📁 Structure du Projet

```
modele-frappe/
├── frappe_app/                    # Module principal de l'application
│   ├── __init__.py               # Version de l'app
│   ├── hooks.py                  # Configuration des hooks Frappe
│   ├── modules.txt               # Liste des modules de l'app
│   ├── patches.txt               # Liste des patches de migration
│   ├── install.py                # Scripts d'installation/désinstallation
│   ├── tasks.py                  # Tâches planifiées (scheduler)
│   ├── utils.py                  # Fonctions utilitaires
│   │
│   ├── config/                   # Configuration de l'app
│   │   ├── desktop.py           # Configuration du bureau (icônes)
│   │   └── docs.py              # Configuration de la documentation
│   │
│   ├── frappe_app/              # Module "Frappe App"
│   │   ├── __init__.py
│   │   └── doctype/             # Tous les DocTypes du module
│   │       └── sample_doctype/  # Exemple de DocType
│   │           ├── __init__.py
│   │           ├── sample_doctype.json
│   │           ├── sample_doctype.py
│   │           └── test_sample_doctype.py
│   │
│   ├── public/                   # Assets statiques
│   │   ├── js/
│   │   │   └── frappe_app.bundle.js
│   │   └── css/
│   │       └── frappe_app.css
│   │
│   ├── templates/                # Templates Jinja2
│   │   ├── pages/               # Pages web custom
│   │   └── includes/            # Includes réutilisables
│   │
│   ├── www/                      # Pages web publiques
│   ├── fixtures/                 # Données initiales (JSON)
│   └── patches/                  # Patches de migration de base de données
│
├── setup.py                      # Configuration Python (legacy)
├── pyproject.toml               # Configuration Python moderne
├── requirements.txt             # Dépendances Python
├── README.md                    # Documentation principale
├── LICENSE                      # Licence du projet
└── CLAUDE.md                    # Instructions pour Claude Code

```

## 🚀 Comment Utiliser ce Template

### 1. Personnaliser l'Application

Modifiez les fichiers suivants pour adapter le template à votre projet :

#### **pyproject.toml**
```toml
[project]
name = "votre_app"  # Changez le nom
authors = [
    {name = "Votre Nom", email = "votre@email.com"}
]
description = "Description de votre app"
```

#### **setup.py**
```python
from votre_app import __version__ as version  # Changez l'import

setup(
	name="votre_app",
	description="Description de votre app",
	author="Votre Nom",
	author_email="votre@email.com",
	...
)
```

#### **frappe_app/hooks.py**
```python
app_name = "votre_app"
app_title = "Votre App"
app_publisher = "Votre Société"
app_description = "Description de votre app"
app_email = "contact@votresociete.com"
```

### 2. Renommer le Module

Renommez le dossier `frappe_app` avec le nom de votre application :

```bash
mv frappe_app votre_app
```

Puis mettez à jour toutes les références dans :
- `setup.py`
- `pyproject.toml`
- `hooks.py`
- `__init__.py`

### 3. Créer vos Modules

Éditez `frappe_app/modules.txt` pour définir vos modules :

```
Module 1
Module 2
Module 3
```

Créez ensuite les dossiers correspondants dans `frappe_app/` :

```bash
mkdir -p frappe_app/module_1
mkdir -p frappe_app/module_2
```

### 4. Créer des DocTypes

Utilisez Bench CLI pour créer de nouveaux DocTypes :

```bash
bench new-doctype
# Ou manuellement, créez la structure comme dans sample_doctype/
```

## 📝 Fichiers Clés

### **hooks.py** - Configuration Centrale

Le fichier `hooks.py` est le cœur de votre application. Il configure :

- **Métadonnées de l'app** : nom, titre, auteur
- **Assets** : JS/CSS à inclure
- **Events** : hooks sur les documents (before_save, on_submit, etc.)
- **Scheduled Tasks** : tâches planifiées
- **Permissions** : logique de permissions custom
- **Overrides** : surcharges de DocTypes Frappe standard

### **install.py** - Installation

Scripts exécutés lors de l'installation/désinstallation :

```python
def after_install():
    # Créer des enregistrements par défaut
    # Configurer des paramètres
    frappe.db.commit()
```

### **tasks.py** - Tâches Planifiées

Définissez des tâches qui s'exécutent automatiquement :

```python
def daily():
    # Exécuté tous les jours à minuit
    pass

def hourly():
    # Exécuté toutes les heures
    pass
```

Activez-les dans `hooks.py` :

```python
scheduler_events = {
    "daily": ["votre_app.tasks.daily"],
    "hourly": ["votre_app.tasks.hourly"]
}
```

### **utils.py** - Fonctions Utilitaires

Fonctions réutilisables et API endpoints :

```python
@frappe.whitelist()
def mon_api():
    """API accessible depuis le client"""
    return {"status": "success"}
```

## 🏗️ Créer un DocType

Structure complète d'un DocType :

```
frappe_app/mon_module/doctype/mon_doctype/
├── __init__.py
├── mon_doctype.json          # Définition du DocType (champs, permissions)
├── mon_doctype.py            # Controller Python (logique métier)
├── mon_doctype.js            # Client-side script (optionnel)
├── mon_doctype_list.js       # Script pour la vue liste (optionnel)
├── mon_doctype.html          # Template d'impression (optionnel)
└── test_mon_doctype.py       # Tests unitaires
```

### Exemple de Controller

```python
from frappe.model.document import Document

class MonDoctype(Document):
    def validate(self):
        # Validation avant sauvegarde
        if not self.title:
            frappe.throw("Le titre est requis")

    def before_save(self):
        # Traitement avant sauvegarde
        self.title = self.title.upper()

    def after_insert(self):
        # Après création
        frappe.sendmail(...)
```

## 🔧 Commandes Bench Utiles

```bash
# Installation
bench get-app /path/to/modele-frappe
bench --site site1.local install-app votre_app

# Développement
bench start                    # Démarrer le serveur
bench migrate                  # Appliquer les migrations
bench clear-cache              # Vider le cache
bench build                    # Compiler les assets

# DocTypes
bench new-doctype             # Créer un nouveau DocType
bench console                 # Console Python interactive

# Tests
bench run-tests --app votre_app
bench run-tests --doctype "Mon Doctype"

# Base de données
bench backup                  # Sauvegarder la base
bench restore                 # Restaurer une sauvegarde
```

## 📚 Hooks Disponibles

### Document Events

```python
doc_events = {
    "Doctype Name": {
        "before_insert": "method",
        "after_insert": "method",
        "before_save": "method",
        "after_save": "method",
        "on_update": "method",
        "on_submit": "method",
        "on_cancel": "method",
        "on_trash": "method",
        "before_submit": "method",
        "before_cancel": "method",
    }
}
```

### Permissions

```python
permission_query_conditions = {
    "Doctype Name": "votre_app.permissions.get_permission_query_conditions"
}

has_permission = {
    "Doctype Name": "votre_app.permissions.has_permission"
}
```

### Override DocTypes

```python
override_doctype_class = {
    "Customer": "votre_app.overrides.CustomCustomer"
}
```

## 🎨 Assets (JS/CSS)

### Inclure des fichiers globaux

Dans `hooks.py` :

```python
# Pour le bureau (desk)
app_include_js = "/assets/votre_app/js/votre_app.bundle.js"
app_include_css = "/assets/votre_app/css/votre_app.css"

# Pour le site web
web_include_js = "/assets/votre_app/js/web.bundle.js"
web_include_css = "/assets/votre_app/css/web.css"
```

### Fichiers spécifiques aux DocTypes

```python
doctype_js = {
    "Customer": "public/js/customer.js"
}

doctype_list_js = {
    "Customer": "public/js/customer_list.js"
}
```

## 🧪 Tests

Créez des tests dans `test_*.py` :

```python
import frappe
import unittest

class TestMonDoctype(unittest.TestCase):
    def setUp(self):
        # Préparation avant chaque test
        pass

    def test_creation(self):
        doc = frappe.get_doc({
            "doctype": "Mon Doctype",
            "title": "Test"
        })
        doc.insert()
        self.assertEqual(doc.title, "Test")
        doc.delete()
```

Exécutez avec :
```bash
bench run-tests --app votre_app
```

## 📦 Fixtures

Pour exporter/importer des données initiales :

1. Ajoutez dans `hooks.py` :
```python
fixtures = [
    "Custom Field",
    {"dt": "Votre DocType", "filters": [["name", "in", ["Record1", "Record2"]]]}
]
```

2. Exportez :
```bash
bench export-fixtures
```

Les fichiers JSON seront créés dans `frappe_app/fixtures/`

## 🌐 Pages Web

### Pages dans www/

Créez `www/ma-page.html` et `www/ma-page.py` :

```python
# www/ma-page.py
def get_context(context):
    context.title = "Ma Page"
    context.data = frappe.get_all("Mon Doctype")
```

```html
<!-- www/ma-page.html -->
{% extends "templates/web.html" %}

{% block page_content %}
<h1>{{ title }}</h1>
<ul>
{% for item in data %}
    <li>{{ item.name }}</li>
{% endfor %}
</ul>
{% endblock %}
```

Accessible sur : `http://yoursite.local/ma-page`

## 🔑 API Endpoints

Créez des endpoints whitelisted :

```python
# Dans utils.py ou n'importe quel fichier Python
import frappe

@frappe.whitelist()
def get_data(filters=None):
    """
    API endpoint accessible via :
    frappe.call('votre_app.utils.get_data', {filters: {...}})
    """
    return frappe.get_all("Mon Doctype", filters=filters)

@frappe.whitelist(allow_guest=True)
def public_api():
    """Accessible sans authentification"""
    return {"message": "Hello World"}
```

## 📖 Ressources

- [Documentation Frappe Framework](https://frappeframework.com/docs)
- [API Reference](https://frappeframework.com/docs/user/en/api)
- [Forum Frappe](https://discuss.frappe.io)
- [GitHub Frappe](https://github.com/frappe/frappe)

## ✅ Checklist pour Démarrer

- [ ] Renommer `frappe_app` avec le nom de votre app
- [ ] Mettre à jour `setup.py` et `pyproject.toml`
- [ ] Personnaliser `hooks.py`
- [ ] Définir vos modules dans `modules.txt`
- [ ] Créer vos DocTypes
- [ ] Configurer les hooks nécessaires
- [ ] Ajouter vos assets JS/CSS
- [ ] Écrire des tests
- [ ] Créer vos fixtures si nécessaire
- [ ] Documenter votre app

## 📄 Licence

MIT
