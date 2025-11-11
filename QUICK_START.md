# Guide de Démarrage Rapide

## 🎯 Créer Votre App à partir de ce Template

### Étape 1 : Cloner et Renommer

```bash
# Cloner le template
git clone https://github.com/votre-repo/modele-frappe.git ma-nouvelle-app
cd ma-nouvelle-app

# Renommer le module principal
mv frappe_app mon_app

# Supprimer l'historique git
rm -rf .git
git init
```

### Étape 2 : Personnaliser les Métadonnées

#### Fichier `pyproject.toml`

```toml
[project]
name = "mon_app"
authors = [
    {name = "Votre Nom", email = "votre.email@example.com"}
]
description = "Description de votre application"
```

#### Fichier `setup.py`

```python
from mon_app import __version__ as version

setup(
	name="mon_app",
	version=version,
	description="Description de votre application",
	author="Votre Nom",
	author_email="votre.email@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
```

#### Fichier `mon_app/__init__.py`

```python
"""
Mon App
"""

__version__ = "0.0.1"
```

#### Fichier `mon_app/hooks.py`

```python
app_name = "mon_app"
app_title = "Mon App"
app_publisher = "Votre Société"
app_description = "Description de votre application"
app_email = "contact@votresociete.com"
app_license = "MIT"
```

### Étape 3 : Installer sur votre site Frappe

```bash
# Se placer dans le répertoire bench
cd /path/to/frappe-bench

# Ajouter l'app
bench get-app /path/to/ma-nouvelle-app

# Installer sur un site
bench --site monsite.local install-app mon_app

# Démarrer le serveur
bench start
```

### Étape 4 : Créer votre Premier Module

#### Éditer `mon_app/modules.txt`

```
Mon Module
```

#### Créer le dossier du module

```bash
mkdir -p mon_app/mon_module
touch mon_app/mon_module/__init__.py
```

### Étape 5 : Créer votre Premier DocType

```bash
# Méthode 1 : Via Bench CLI
bench new-doctype

# Méthode 2 : Via l'interface Frappe
# 1. Ouvrir http://monsite.local
# 2. Aller dans "DocType List"
# 3. Cliquer sur "New"
# 4. Remplir les informations :
#    - Module: Mon Module
#    - Name: Mon DocType
#    - etc.
```

#### Structure manuelle d'un DocType

```bash
mkdir -p mon_app/mon_module/doctype/mon_doctype
cd mon_app/mon_module/doctype/mon_doctype

# Créer les fichiers
touch __init__.py
touch mon_doctype.json
touch mon_doctype.py
touch mon_doctype.js
touch test_mon_doctype.py
```

**Fichier `mon_doctype.py`** :

```python
import frappe
from frappe.model.document import Document

class MonDoctype(Document):
	def validate(self):
		# Logique de validation
		pass

	def before_save(self):
		# Avant sauvegarde
		pass

	def after_insert(self):
		# Après création
		pass
```

### Étape 6 : Ajouter des Hooks

Dans `mon_app/hooks.py`, décommentez et configurez :

```python
# Document Events
doc_events = {
	"Customer": {
		"before_save": "mon_app.utils.before_customer_save",
		"after_insert": "mon_app.utils.after_customer_insert",
	}
}

# Scheduled Tasks
scheduler_events = {
	"daily": [
		"mon_app.tasks.daily"
	],
	"hourly": [
		"mon_app.tasks.hourly"
	]
}

# Include JS/CSS
app_include_js = "/assets/mon_app/js/mon_app.bundle.js"
app_include_css = "/assets/mon_app/css/mon_app.css"

# DocType-specific JS
doctype_js = {
	"Customer": "public/js/customer.js"
}
```

### Étape 7 : Créer une API

Dans `mon_app/utils.py` :

```python
import frappe

@frappe.whitelist()
def get_customers(filters=None):
	"""
	API pour récupérer les clients
	Usage: frappe.call('mon_app.utils.get_customers')
	"""
	return frappe.get_all("Customer",
		filters=filters or {},
		fields=["name", "customer_name", "email"]
	)

@frappe.whitelist(allow_guest=True)
def public_endpoint():
	"""API accessible sans authentification"""
	return {"status": "ok", "message": "Hello World"}
```

Appeler depuis le client :

```javascript
frappe.call({
	method: 'mon_app.utils.get_customers',
	args: {
		filters: {status: 'Active'}
	},
	callback: function(r) {
		console.log(r.message);
	}
});
```

### Étape 8 : Ajouter des Tâches Planifiées

Dans `mon_app/tasks.py` :

```python
import frappe

def daily():
	"""Exécuté tous les jours à minuit"""
	# Exemple : Envoyer un rapport quotidien
	customers = frappe.get_all("Customer", filters={"status": "Active"})
	frappe.sendmail(
		recipients=["admin@example.com"],
		subject="Rapport quotidien",
		message=f"Nombre de clients actifs : {len(customers)}"
	)

def hourly():
	"""Exécuté toutes les heures"""
	# Exemple : Synchroniser des données
	pass
```

Activer dans `hooks.py` :

```python
scheduler_events = {
	"daily": ["mon_app.tasks.daily"],
	"hourly": ["mon_app.tasks.hourly"]
}
```

### Étape 9 : Créer une Page Web

Créer `mon_app/www/ma-page.py` :

```python
import frappe

def get_context(context):
	context.title = "Ma Page"
	context.items = frappe.get_all("Mon DocType",
		fields=["name", "title", "description"]
	)
	return context
```

Créer `mon_app/www/ma-page.html` :

```html
{% extends "templates/web.html" %}

{% block page_content %}
<div class="container">
	<h1>{{ title }}</h1>
	<div class="row">
		{% for item in items %}
		<div class="col-md-4">
			<div class="card">
				<h3>{{ item.title }}</h3>
				<p>{{ item.description }}</p>
			</div>
		</div>
		{% endfor %}
	</div>
</div>
{% endblock %}
```

Accessible sur : `http://monsite.local/ma-page`

### Étape 10 : Tester votre App

```bash
# Migrer la base de données
bench --site monsite.local migrate

# Vider le cache
bench --site monsite.local clear-cache

# Compiler les assets
bench build --app mon_app

# Lancer les tests
bench --site monsite.local run-tests --app mon_app

# Tester un DocType spécifique
bench --site monsite.local run-tests --doctype "Mon Doctype"
```

## 📋 Commandes Utiles

```bash
# Développement
bench start                          # Démarrer le serveur de développement
bench console                        # Console Python interactive
bench clear-cache                    # Vider le cache
bench build                          # Compiler les assets

# Base de données
bench migrate                        # Appliquer les migrations
bench backup                         # Sauvegarder
bench restore                        # Restaurer

# App
bench get-app [url/path]            # Télécharger une app
bench install-app [app]             # Installer une app
bench uninstall-app [app]           # Désinstaller une app
bench remove-app [app]              # Supprimer une app

# Site
bench new-site [site]               # Créer un nouveau site
bench drop-site [site]              # Supprimer un site
bench use [site]                    # Définir le site par défaut

# Fixtures
bench export-fixtures               # Exporter les fixtures
```

## 🔍 Debugging

### Activer le mode Debug

Dans `site_config.json` :

```json
{
	"developer_mode": 1,
	"allow_tests": 1
}
```

### Logs

```bash
# Voir les logs en temps réel
tail -f sites/monsite.local/logs/web.error.log

# Logs de la base de données
tail -f sites/monsite.local/logs/db.log
```

### Console Python

```bash
bench console

# Dans la console :
>>> frappe.get_all("Mon Doctype")
>>> doc = frappe.get_doc("Mon Doctype", "DOC-0001")
>>> doc.save()
```

## 📚 Prochaines Étapes

1. ✅ Créer vos DocTypes
2. ✅ Implémenter votre logique métier
3. ✅ Ajouter des tests unitaires
4. ✅ Créer des pages web si nécessaire
5. ✅ Configurer les permissions
6. ✅ Ajouter des fixtures pour les données initiales
7. ✅ Documenter votre code
8. ✅ Tester en production

## 🆘 Besoin d'Aide ?

- [Documentation Frappe](https://frappeframework.com/docs)
- [Forum Frappe](https://discuss.frappe.io)
- [GitHub Issues](https://github.com/frappe/frappe/issues)

Bon développement ! 🚀
