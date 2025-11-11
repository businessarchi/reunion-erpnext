# Guide de Contribution

Merci de votre intérêt pour contribuer au Template Frappe ! 🎉

Ce document fournit des lignes directrices pour contribuer au projet.

## 🌟 Comment Contribuer

### Signaler des Bugs

Si vous trouvez un bug, veuillez créer une issue avec :

- **Description claire** du problème
- **Étapes pour reproduire** le bug
- **Comportement attendu** vs comportement observé
- **Version** de Frappe/ERPNext utilisée
- **Captures d'écran** si applicable

### Proposer des Améliorations

Pour proposer une nouvelle fonctionnalité :

1. **Vérifier** qu'elle n'existe pas déjà dans les issues
2. **Créer une issue** décrivant :
   - Le problème que ça résout
   - La solution proposée
   - Des exemples d'utilisation
3. **Attendre la discussion** avant de commencer le développement

### Soumettre des Pull Requests

1. **Fork** le projet
2. **Créer une branche** depuis `main` :
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
3. **Faire vos modifications** en suivant les standards de code
4. **Tester** vos changements
5. **Commit** avec des messages clairs :
   ```bash
   git commit -m "Ajout: Description de la fonctionnalité"
   ```
6. **Push** vers votre fork :
   ```bash
   git push origin feature/ma-fonctionnalite
   ```
7. **Ouvrir une Pull Request** vers `main`

## 📋 Standards de Code

### Python

- Suivre **PEP 8**
- Utiliser des **docstrings** pour les fonctions
- **Type hints** encouragés pour Python 3.10+
- Indentation : **tabs** (comme Frappe)

```python
def ma_fonction(arg1: str, arg2: int) -> dict:
	"""
	Description de la fonction

	Args:
		arg1: Description du paramètre 1
		arg2: Description du paramètre 2

	Returns:
		dict: Description du retour
	"""
	pass
```

### JavaScript

- Suivre les conventions **Frappe**
- Utiliser **ES6+** si possible
- Indentation : **tabs**
- Commentaires en anglais pour le code, français pour la doc

```javascript
frappe.ui.form.on('DocType', {
	refresh: function(frm) {
		// Code here
	}
});
```

### Documentation

- Documentation en **français**
- Utiliser **Markdown** pour le formatage
- Ajouter des **exemples** quand c'est pertinent
- Mettre à jour **CHANGELOG.md** pour les changements

## 🧪 Tests

Avant de soumettre une PR :

```bash
# Tester l'app
bench run-tests --app frappe_app

# Tester un DocType spécifique
bench run-tests --doctype "Sample Doctype"

# Vérifier la syntaxe Python
flake8 frappe_app/

# Vérifier les types (si applicable)
mypy frappe_app/
```

## 📝 Messages de Commit

Format recommandé :

```
Type: Description courte (max 50 caractères)

Description détaillée si nécessaire (max 72 caractères par ligne).

Fixes #123
```

**Types** :
- `Ajout` : Nouvelle fonctionnalité
- `Fix` : Correction de bug
- `Docs` : Documentation uniquement
- `Style` : Formatage, points-virgules manquants, etc.
- `Refactor` : Refactorisation du code
- `Test` : Ajout/modification de tests
- `Chore` : Maintenance, configuration

**Exemples** :
```
Ajout: Script de renommage automatique de l'app

Ajout d'un script Python pour renommer automatiquement
l'application template avec les paramètres fournis.

Fixes #42
```

```
Fix: Correction du hook permission_query_conditions

Le hook n'était pas correctement référencé dans hooks.py
```

## 🎯 Domaines de Contribution

### Priorité Haute
- 📚 Amélioration de la documentation
- 🐛 Correction de bugs
- ✅ Ajout de tests
- 🔧 Amélioration du script de renommage

### Priorité Moyenne
- 📊 Exemples de rapports
- 🔄 Exemples de workflows
- 🎨 Exemples de print formats
- 📱 Amélioration du responsive

### Priorité Basse
- 🌍 Traductions (anglais, etc.)
- 🎨 Thèmes visuels
- 📦 Intégrations tierces

## 🔍 Processus de Review

Toutes les PR sont reviewées par les mainteneurs :

1. ✅ **Code review** : Qualité, standards
2. ✅ **Tests** : Tous les tests passent
3. ✅ **Documentation** : À jour et complète
4. ✅ **CHANGELOG** : Mis à jour si nécessaire

Les reviews peuvent prendre quelques jours. Soyez patient ! 🙏

## 📦 Structure pour Nouvelles Fonctionnalités

Quand vous ajoutez une nouvelle fonctionnalité :

```
1. Code dans frappe_app/
2. Tests dans frappe_app/tests/
3. Documentation dans FRAPPE_APP_TEMPLATE.md
4. Exemple dans le code si applicable
5. Mise à jour de CHANGELOG.md
```

## ❓ Questions

Pour toute question :

- 💬 Ouvrir une **Discussion** sur GitHub
- 📧 Envoyer un email aux mainteneurs
- 🌐 Poster sur le [Forum Frappe](https://discuss.frappe.io)

## 📜 Licence

En contribuant, vous acceptez que vos contributions soient sous licence **MIT**.

## 🙏 Remerciements

Merci à tous les contributeurs qui aident à améliorer ce template !

Votre contribution, quelle que soit sa taille, est appréciée. 💙

---

**Ensemble, construisons le meilleur template Frappe !** 🚀
