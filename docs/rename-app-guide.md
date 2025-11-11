# Guide : Renommer l'app en "Gestion Réunions"

## 📛 Problème actuel

L'app s'appelle `frappe_app` (nom générique de template) au lieu d'un nom significatif pour ton application de gestion de réunions.

## ✅ Solution : Renommer proprement

### Option 1 : Utiliser le script de renommage inclus

Le template inclut un script `rename_app.py` pour renommer facilement :

```bash
cd /Users/melodie/Documents/GitHub/ERPnext/reunion-erpnext

# Renommer en "reunion" (nom technique)
python3 rename_app.py reunion "Gestion Réunions"
```

Ce script va :
- ✅ Renommer tous les fichiers et dossiers
- ✅ Mettre à jour les imports Python
- ✅ Modifier hooks.py avec le nouveau nom
- ✅ Mettre à jour setup.py

### Option 2 : Recommencer avec un nouveau nom

Si tu préfères repartir proprement :

```bash
cd ~/frappe-bench/apps

# Créer une nouvelle app avec le bon nom
bench new-app reunion

# Copier les fichiers que tu veux garder
cp reunion-erpnext/frappe_app/public/js/google_calendar_fix.js reunion/reunion/public/js/
cp -r reunion-erpnext/docs reunion/docs
cp -r reunion-erpnext/PRPs reunion/PRPs

# Installer la nouvelle app
bench --site architecte.business install-app reunion
```

### Option 3 : Garder frappe_app et créer le module meeting_management

Le plus simple pour l'instant : garder `frappe_app` comme nom d'app, mais créer un **module bien nommé** dedans :

```bash
cd /Users/melodie/Documents/GitHub/ERPnext/reunion-erpnext

# Créer le module de gestion de réunions
mkdir -p frappe_app/meeting_management
mkdir -p frappe_app/meeting_management/doctype
mkdir -p frappe_app/meeting_management/api
touch frappe_app/meeting_management/__init__.py
touch frappe_app/meeting_management/api/__init__.py
```

Puis mettre à jour `modules.txt` :

```
Meeting Management
```

## 📝 Mon recommandation

**Option 3** (garder frappe_app, créer le module meeting_management) parce que :

- ✅ Pas besoin de réinstaller l'app sur Frappe Cloud
- ✅ Le nom de l'app n'est pas visible par les utilisateurs
- ✅ Le nom du **module** (Meeting Management) est ce que les utilisateurs verront
- ✅ Plus rapide à mettre en place

## 🚀 Prochaines étapes

Une fois le module créé, on peut commencer à implémenter :

1. **Doctype "Meeting"** - Pour gérer les réunions
2. **Doctype "Google Calendar Settings"** - Pour la config OAuth
3. **API Google Calendar** - Pour la synchronisation
4. **Interface de gestion** - Calendrier, liste, etc.

Veux-tu que je commence l'implémentation en gardant `frappe_app` comme nom d'app et en créant le module `meeting_management` ?
