# 🚀 Frappe App Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Un template complet et prêt à l'emploi pour créer des applications Frappe Framework.**

Ce projet fournit une structure de base complète pour développer des applications Frappe personnalisées, avec des exemples de code, des fichiers de configuration et une documentation détaillée.

## 📦 Contenu du Template

- ✅ Structure complète d'une app Frappe
- ✅ Fichiers de configuration (hooks.py, setup.py, pyproject.toml)
- ✅ Exemple de DocType avec controller Python
- ✅ Scripts client (JS) pour formulaires et listes
- ✅ Exemples de pages web (www/)
- ✅ Système de permissions personnalisées
- ✅ Tâches planifiées (scheduler)
- ✅ Tests unitaires
- ✅ Fixtures et patches de migration
- ✅ Documentation complète en français

## 🎯 Pour Qui ?

Ce template est idéal pour :

- Développeurs débutant avec Frappe Framework
- Équipes voulant standardiser leur structure d'apps
- Projets nécessitant un démarrage rapide
- Développeurs cherchant des exemples de code Frappe

## 🚦 Démarrage Rapide

### 1. Cloner le Template

```bash
git clone https://github.com/votre-repo/modele-frappe.git mon_app
cd mon_app
```

### 2. Renommer l'Application

```bash
# Renommer le module principal
mv frappe_app mon_app

# Mettre à jour les fichiers de configuration
# Voir QUICK_START.md pour les détails
```

### 3. Installer sur Frappe

```bash
# Dans votre répertoire frappe-bench
bench get-app /path/to/mon_app
bench --site monsite.local install-app mon_app
bench start
```

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Guide pas-à-pas pour démarrer
- **[FRAPPE_APP_TEMPLATE.md](FRAPPE_APP_TEMPLATE.md)** - Documentation complète de la structure
- **[CLAUDE.md](CLAUDE.md)** - Instructions pour Claude Code

## 📁 Structure du Projet

```
frappe_app/
├── __init__.py                  # Version de l'app
├── hooks.py                     # Configuration centrale
├── modules.txt                  # Liste des modules
├── patches.txt                  # Patches de migration
├── install.py                   # Scripts d'installation
├── tasks.py                     # Tâches planifiées
├── utils.py                     # Fonctions utilitaires
├── permissions.py               # Logique de permissions
├── config/                      # Configuration
│   ├── desktop.py              # Icônes du bureau
│   └── docs.py                 # Configuration docs
├── frappe_app/                 # Module principal
│   └── doctype/                # DocTypes
│       └── sample_doctype/     # Exemple de DocType
├── public/                     # Assets statiques
│   ├── js/                     # Scripts JavaScript
│   └── css/                    # Feuilles de style
├── templates/                  # Templates Jinja2
├── www/                        # Pages web publiques
├── fixtures/                   # Données initiales
├── patches/                    # Patches de migration
└── tests/                      # Tests unitaires
```

## 🔧 Fonctionnalités Incluses

### DocType d'Exemple

Un DocType complet "Sample Doctype" avec :
- Controller Python avec hooks (validate, before_save, etc.)
- Fichier JSON de définition
- Script client JavaScript
- Script pour la vue liste
- Tests unitaires

### Exemples de Code

- **API Endpoints** : Fonctions whitelisted dans `utils.py`
- **Tâches Planifiées** : Exemples daily/hourly dans `tasks.py`
- **Permissions** : Logique custom dans `permissions.py`
- **Pages Web** : Exemple complet dans `www/example-page.py`
- **Scripts Client** : Formulaires et listes dans `public/js/`

### Configuration

- **hooks.py** : Tous les hooks Frappe commentés et expliqués
- **Permissions** : Système de permissions personnalisé
- **Desktop** : Configuration des icônes du bureau
- **Fixtures** : Exemple de custom field

### Tests

- Tests unitaires pour les utils
- Tests pour le DocType exemple
- Configuration pour pytest

## 🛠️ Commandes Utiles

```bash
# Développement
bench start                      # Démarrer le serveur
bench migrate                    # Migrer la base de données
bench clear-cache                # Vider le cache
bench build                      # Compiler les assets

# Tests
bench run-tests --app mon_app
bench run-tests --doctype "Sample Doctype"

# Console
bench console                    # Console Python interactive
```

## 📖 Ressources Frappe

- [Documentation Officielle](https://frappeframework.com/docs)
- [API Reference](https://frappeframework.com/docs/user/en/api)
- [Forum Frappe](https://discuss.frappe.io)
- [GitHub Frappe](https://github.com/frappe/frappe)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📝 Licence

MIT License - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## ✨ Fonctionnalités à Venir

- [ ] Exemples de rapports personnalisés
- [ ] Exemples d'intégration avec d'autres apps
- [ ] Exemples de workflows
- [ ] Exemples de print formats
- [ ] Exemples de dashboards
- [ ] Guide de déploiement en production

## 💡 Support

Pour toute question ou problème :

- Ouvrir une [issue](https://github.com/votre-repo/modele-frappe/issues)
- Consulter la [documentation](FRAPPE_APP_TEMPLATE.md)
- Visiter le [forum Frappe](https://discuss.frappe.io)

---

**Développé avec ❤️ pour la communauté Frappe**