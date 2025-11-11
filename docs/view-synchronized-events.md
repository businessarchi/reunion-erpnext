# Comment voir les éléments synchronisés entre ERPNext et Google Calendar

## 📋 Méthode 1 : Via le doctype Event (Recommandé)

### Accéder aux événements synchronisés

1. **Dans ERPNext, aller à :**
   ```
   Home → CRM → Event
   ```
   OU utiliser la barre de recherche (Ctrl/Cmd + K) et taper `Event`

2. **Vous verrez la liste de tous les événements**

### Identifier les événements synchronisés

Les événements synchronisés avec Google Calendar ont des **champs spéciaux** :

| Champ | Description | Comment le voir |
|-------|-------------|-----------------|
| **Push to Google Calendar** | Si coché ✅, l'événement est envoyé vers Google | Visible dans le formulaire Event |
| **Pull from Google Calendar** | Si coché ✅, l'événement provient de Google | Visible dans le formulaire Event |
| **Google Calendar ID** | L'ID unique de l'événement dans Google Calendar | Visible dans le formulaire Event (section Google Calendar) |
| **Google Calendar** | Le calendrier Google associé | Visible dans le formulaire Event |

### Voir les détails d'un événement synchronisé

1. **Cliquer sur un événement** dans la liste
2. **Descendre jusqu'à la section "Google Calendar"**
3. Vous verrez :
   - ✅ Push to Google Calendar (envoyé vers Google)
   - ✅ Pull from Google Calendar (provient de Google)
   - Google Calendar ID : `abc123xyz...`
   - Google Calendar : `primary` ou nom du calendrier

---

## 📅 Méthode 2 : Vue Calendrier

### Affichage visuel des événements

1. **Dans la liste des Events, cliquer sur l'icône Calendrier** (en haut à droite)

2. **Vous verrez tous les événements dans une vue calendrier**
   - Les événements ERPNext
   - Les événements synchronisés de Google Calendar

3. **Cliquer sur un événement** pour voir ses détails

### Astuce : Filtrer les événements synchronisés

Dans la vue liste Event, vous pouvez ajouter des **filtres** :

```
Filtrer par :
- "Push to Google Calendar" = Oui  → Voir uniquement les événements envoyés vers Google
- "Pull from Google Calendar" = Oui  → Voir uniquement les événements provenant de Google
- "Google Calendar ID" is set  → Voir tous les événements synchronisés
```

---

## 🔍 Méthode 3 : Vérifier la synchronisation en temps réel

### Forcer une synchronisation

1. **Aller dans : Setup → Integrations → Google Settings**

2. **Vérifier les paramètres :**
   - Enable Google Calendar : ✅
   - Push to Google Calendar : ✅ (si vous voulez envoyer vers Google)
   - Pull from Google Calendar : ✅ (si vous voulez recevoir de Google)

3. **Pour synchroniser maintenant :**
   - ERPNext synchronise automatiquement via un job planifié
   - Vous pouvez aussi créer un nouvel Event pour tester

### Tester la synchronisation bidirectionnelle

#### Test 1 : ERPNext → Google Calendar

1. **Créer un nouvel Event dans ERPNext** :
   - Home → CRM → Event → New
   - Remplir : Subject, Starts On, Ends On
   - **Cocher "Push to Google Calendar"** ✅
   - Save

2. **Vérifier dans Google Calendar** :
   - Aller sur [calendar.google.com](https://calendar.google.com)
   - Chercher votre événement par son titre
   - Il devrait apparaître !

#### Test 2 : Google Calendar → ERPNext

1. **Créer un événement dans Google Calendar** :
   - Aller sur [calendar.google.com](https://calendar.google.com)
   - Créer un nouvel événement
   - Sauvegarder

2. **Attendre la synchronisation** (ou forcer via bench) :
   - ERPNext synchronise périodiquement
   - Ou en console : `bench execute frappe.integrations.doctype.google_calendar.google_calendar.sync`

3. **Vérifier dans ERPNext** :
   - Home → CRM → Event
   - Chercher votre événement par son titre
   - Il devrait avoir "Pull from Google Calendar" ✅

---

## 🛠️ Méthode 4 : Via la console Bench (Technique)

### Lister tous les événements synchronisés

```bash
bench console
```

Puis dans la console Python :

```python
import frappe

# Récupérer tous les événements avec Google Calendar ID
events = frappe.get_all("Event",
    filters={"google_calendar_id": ["!=", ""]},
    fields=["name", "subject", "starts_on", "ends_on", "google_calendar_id", "push_to_google_calendar", "pull_from_google_calendar"]
)

print(f"Nombre d'événements synchronisés : {len(events)}\n")

for event in events:
    print(f"Titre : {event.subject}")
    print(f"  Date : {event.starts_on}")
    print(f"  Google ID : {event.google_calendar_id}")
    print(f"  Push to Google : {event.push_to_google_calendar}")
    print(f"  Pull from Google : {event.pull_from_google_calendar}")
    print()
```

### Vérifier un événement spécifique

```python
event_name = "EVT-00001"  # Remplacer par le nom de votre événement
event = frappe.get_doc("Event", event_name)

print(f"Subject: {event.subject}")
print(f"Google Calendar ID: {event.google_calendar_id}")
print(f"Push to Google: {event.push_to_google_calendar}")
print(f"Pull from Google: {event.pull_from_google_calendar}")
print(f"Google Calendar: {event.google_calendar}")
```

### Voir tous les calendriers Google accessibles

```python
from frappe.integrations.doctype.google_calendar.google_calendar import get_google_calendar_object

# Récupérer le service Google Calendar
calendar_service = get_google_calendar_object()

# Lister tous les calendriers
calendar_list = calendar_service.calendarList().list().execute()

print("Calendriers accessibles depuis ERPNext :\n")
for calendar in calendar_list.get('items', []):
    print(f"ID : {calendar['id']}")
    print(f"  Nom : {calendar['summary']}")
    print(f"  Primary : {calendar.get('primary', False)}")
    print(f"  Couleur : {calendar.get('backgroundColor', 'N/A')}")
    print()
```

### Lister les événements d'un calendrier Google

```python
from frappe.integrations.doctype.google_calendar.google_calendar import get_google_calendar_object
from datetime import datetime, timedelta

calendar_service = get_google_calendar_object()

# Paramètres de recherche
calendar_id = 'primary'  # Ou un autre calendar ID
time_min = datetime.utcnow().isoformat() + 'Z'  # Maintenant
time_max = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'  # 30 jours

# Récupérer les événements
events_result = calendar_service.events().list(
    calendarId=calendar_id,
    timeMin=time_min,
    timeMax=time_max,
    maxResults=50,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])

print(f"Événements dans Google Calendar '{calendar_id}' :\n")
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(f"{start} - {event['summary']}")
    print(f"  ID: {event['id']}")
    print()
```

---

## 📊 Méthode 5 : Créer un rapport personnalisé

### Rapport SQL pour voir les événements synchronisés

1. **Aller dans : Home → Reports → Report Builder**

2. **Créer un nouveau rapport :**
   - DocType : Event
   - Report Type : Report Builder

3. **Ajouter les colonnes :**
   - Name
   - Subject
   - Starts On
   - Ends On
   - Google Calendar ID
   - Push to Google Calendar
   - Pull from Google Calendar
   - Google Calendar

4. **Ajouter un filtre :**
   - Google Calendar ID : is set

5. **Sauvegarder le rapport : "Google Calendar Synced Events"**

### Script Report avancé (optionnel)

Créer un fichier Python pour un rapport custom :

```python
# frappe_app/frappe_app/report/google_calendar_sync_status/google_calendar_sync_status.py

import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "name", "label": "Event ID", "fieldtype": "Link", "options": "Event", "width": 120},
        {"fieldname": "subject", "label": "Subject", "fieldtype": "Data", "width": 200},
        {"fieldname": "starts_on", "label": "Start", "fieldtype": "Datetime", "width": 150},
        {"fieldname": "sync_status", "label": "Sync Status", "fieldtype": "Data", "width": 150},
        {"fieldname": "google_calendar_id", "label": "Google ID", "fieldtype": "Data", "width": 200}
    ]

    events = frappe.get_all("Event",
        fields=["name", "subject", "starts_on", "push_to_google_calendar",
                "pull_from_google_calendar", "google_calendar_id"],
        order_by="starts_on desc"
    )

    data = []
    for event in events:
        sync_status = "Not Synced"
        if event.google_calendar_id:
            if event.push_to_google_calendar and event.pull_from_google_calendar:
                sync_status = "Bidirectional Sync"
            elif event.push_to_google_calendar:
                sync_status = "Pushed to Google"
            elif event.pull_from_google_calendar:
                sync_status = "Pulled from Google"

        data.append({
            "name": event.name,
            "subject": event.subject,
            "starts_on": event.starts_on,
            "sync_status": sync_status,
            "google_calendar_id": event.google_calendar_id or "-"
        })

    return columns, data
```

---

## 🔔 Méthode 6 : Vérifier les logs de synchronisation

### Voir les erreurs de synchronisation

1. **Aller dans : Setup → Error Log**

2. **Filtrer par :**
   - Method : contient "google_calendar"
   - OU chercher "Google Calendar" dans le champ de recherche

3. **Analyser les erreurs** pour comprendre les problèmes de synchronisation

### Voir l'historique des modifications

1. **Ouvrir un Event synchronisé**

2. **Cliquer sur "View" → "Version History"**

3. **Voir toutes les modifications** :
   - Qui a créé/modifié l'événement
   - Quand
   - Quelles valeurs ont changé
   - Si ça vient d'une synchro Google

---

## ✅ Checklist : Vérifier que la synchronisation fonctionne

### Tests à faire

- [ ] **Créer un Event dans ERPNext avec "Push to Google Calendar" ✅**
  - ✅ Vérifier qu'il apparaît dans Google Calendar dans les 5 minutes
  - ✅ Vérifier que le champ "Google Calendar ID" est rempli dans ERPNext

- [ ] **Créer un événement dans Google Calendar**
  - ✅ Attendre la synchronisation (ou forcer via bench)
  - ✅ Vérifier qu'il apparaît dans ERPNext Event List
  - ✅ Vérifier que "Pull from Google Calendar" est coché

- [ ] **Modifier un Event dans ERPNext**
  - ✅ Changer le titre ou la date
  - ✅ Vérifier que la modification apparaît dans Google Calendar

- [ ] **Modifier un événement dans Google Calendar**
  - ✅ Changer le titre ou la date
  - ✅ Attendre la synchro
  - ✅ Vérifier que la modification apparaît dans ERPNext

- [ ] **Supprimer un Event dans ERPNext**
  - ✅ Vérifier qu'il est supprimé dans Google Calendar

- [ ] **Supprimer un événement dans Google Calendar**
  - ✅ Attendre la synchro
  - ✅ Vérifier qu'il est supprimé dans ERPNext

---

## 🐛 Problèmes courants

### "Je ne vois aucun événement synchronisé"

**Causes possibles :**

1. **Les checkboxes ne sont pas cochées**
   - Solution : Vérifier Google Settings → Enable Google Calendar, Push, Pull

2. **Le calendrier par défaut n'est pas configuré**
   - Solution : Mettre "primary" dans Calendar Name

3. **La synchronisation n'a pas encore eu lieu**
   - Solution : Attendre ou forcer via `bench execute frappe.integrations.doctype.google_calendar.google_calendar.sync`

4. **Problème d'authentification**
   - Solution : Réautoriser l'accès dans Google Settings

### "Les événements apparaissent en double"

**Cause :** Synchronisation bidirectionnelle mal configurée

**Solution :**
- Ne pas cocher Push ET Pull sur le même événement créé manuellement
- Laisser ERPNext gérer automatiquement

### "Les modifications ne se synchronisent pas"

**Cause :** La synchronisation est désactivée ou l'événement n'est pas lié

**Solution :**
- Vérifier que le Google Calendar ID existe
- Vérifier que Push to Google Calendar est coché
- Forcer une synchronisation manuelle

---

## 📚 Ressources supplémentaires

- **Documentation ERPNext** : [Google Calendar Integration](https://docs.erpnext.com/docs/user/manual/en/google_calendar)
- **Guide de dépannage** : [docs/fix-google-calendar-default.md](fix-google-calendar-default.md)
- **Plan d'implémentation custom** : [PRPs/meeting-management-google-calendar.md](../PRPs/meeting-management-google-calendar.md)

---

## 💡 Astuces avancées

### Créer un dashboard pour voir les stats de synchronisation

```javascript
// Dashboard custom pour voir les métriques de sync
frappe.pages['google-sync-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Google Calendar Sync Dashboard',
        single_column: true
    });

    // Charger les statistiques
    frappe.call({
        method: 'frappe.client.get_count',
        args: {
            doctype: 'Event',
            filters: {google_calendar_id: ['!=', '']}
        },
        callback: function(r) {
            page.add_inner_message('Events synchronisés : ' + r.message);
        }
    });
}
```

### Automatiser la vérification de synchronisation

Créer un script qui vérifie périodiquement :

```python
# frappe_app/tasks.py
def check_google_calendar_sync():
    """Vérifier que la synchronisation Google Calendar fonctionne"""
    import frappe
    from datetime import datetime, timedelta

    # Vérifier les événements créés dans les dernières 24h
    yesterday = datetime.now() - timedelta(days=1)

    events = frappe.get_all("Event",
        filters={
            "creation": [">=", yesterday],
            "push_to_google_calendar": 1,
            "google_calendar_id": ""
        },
        fields=["name", "subject"]
    )

    if events:
        # Envoyer une notification
        frappe.log_error(
            f"{len(events)} événements ne sont pas synchronisés avec Google Calendar",
            "Google Calendar Sync Warning"
        )
```

Ajouter dans [hooks.py](../frappe_app/hooks.py) :

```python
scheduler_events = {
    "daily": [
        "frappe_app.tasks.check_google_calendar_sync"
    ]
}
```

---

## 🎯 Résumé rapide

| Besoin | Méthode |
|--------|---------|
| Voir la liste des événements | Home → CRM → Event |
| Voir le calendrier visuel | Event List → Icône Calendrier |
| Filtrer les événements synchro | Ajouter filtre "Google Calendar ID is set" |
| Voir les détails de synchro | Ouvrir un Event → Section "Google Calendar" |
| Déboguer la synchro | bench console + code Python |
| Voir les erreurs | Setup → Error Log |

Commence par la **Méthode 1** (via Event doctype) - c'est la plus simple et la plus visuelle !
