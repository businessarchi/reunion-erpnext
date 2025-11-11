# Fix : ERPNext a créé un nouveau calendrier "primary" au lieu d'utiliser le vrai calendrier principal

## 🐛 Problème

ERPNext a créé un **nouveau calendrier Google** appelé "primary" au lieu d'utiliser ton **calendrier principal existant**. Résultat :
- ✅ La synchronisation fonctionne
- ❌ Mais sur le mauvais calendrier !
- ❌ Tes vrais rendez-vous ne sont pas synchronisés

## 🔍 Comprendre la différence

### Calendrier principal Google (le bon)
- **ID** : L'email de ton compte Google (ex: `ton.email@gmail.com`)
- **Alias** : `primary` (c'est un alias spécial)
- **C'est ton vrai calendrier** avec tous tes rendez-vous

### Calendrier créé par ERPNext (le mauvais)
- **Nom** : "primary" (juste le nom)
- **ID** : Un ID aléatoire généré par Google (ex: `abc123def456@group.calendar.google.com`)
- **Calendrier vide** créé par ERPNext

## ✅ Solution : Reconfigurer ERPNext

### Étape 1 : Identifier ton vrai calendrier principal

1. **Aller sur [calendar.google.com](https://calendar.google.com)**

2. **Cliquer sur les 3 points** à côté de ton calendrier principal (celui avec tous tes rdvs)

3. **Cliquer sur "Paramètres et partage"**

4. **Dans la section "Intégrer l'agenda"**, tu verras :
   - **ID de l'agenda** : C'est généralement ton email (ex: `melodie@gmail.com`)

5. **Copier cet ID**

### Étape 2 : Reconfigurer ERPNext

1. **Dans ERPNext, aller à :**
   ```
   Setup → Integrations → Google Settings
   ```

2. **Section "Google Calendar Settings"** :

3. **Trouver le champ "Calendar"** ou "Calendar ID" ou "Calendar Name"

4. **Option A - Si tu vois une liste déroulante :**
   - Cherche ton vrai calendrier dans la liste
   - Sélectionne celui qui correspond à ton email

5. **Option B - Si c'est un champ texte :**
   - Efface `primary`
   - Colle l'ID que tu as copié (ton email)
   - OU essaie simplement ton email Gmail complet

6. **Sauvegarder**

### Étape 3 : Forcer une synchronisation

1. **Toujours dans Google Settings**

2. **Cliquer sur "Synchronize"** ou **"Authorize API Access"** pour reconnecter

3. **Ou via la console Bench :**
   ```bash
   cd ~/frappe-bench
   bench console
   ```

   Puis dans la console Python :
   ```python
   from frappe.integrations.doctype.google_calendar.google_calendar import sync
   sync()
   ```

4. **Attendre quelques secondes**

5. **Vérifier dans Event** : Tes rendez-vous devraient maintenant apparaître !

## 🔧 Solution alternative : Script pour trouver le bon calendrier

Si tu n'es pas sûr de quel calendrier utiliser, lance ce script :

```bash
cd ~/frappe-bench
bench console
```

Puis :

```python
import frappe
from frappe.integrations.doctype.google_calendar.google_calendar import get_google_calendar_object

# Récupérer le service Google Calendar
calendar_service = get_google_calendar_object()

# Lister TOUS les calendriers accessibles
calendar_list = calendar_service.calendarList().list().execute()

print("=" * 60)
print("TOUS TES CALENDRIERS GOOGLE")
print("=" * 60)

for calendar in calendar_list.get('items', []):
    is_primary = calendar.get('primary', False)

    print(f"\n{'🌟 ' if is_primary else '📅 '}Calendrier: {calendar['summary']}")
    print(f"   ID: {calendar['id']}")
    print(f"   Primary: {is_primary}")
    print(f"   Access Role: {calendar.get('accessRole', 'N/A')}")

    # Compter les événements
    try:
        events = calendar_service.events().list(
            calendarId=calendar['id'],
            maxResults=10
        ).execute()
        event_count = len(events.get('items', []))
        print(f"   Événements (sample): {event_count}")
    except:
        print(f"   Événements: Erreur d'accès")

print("\n" + "=" * 60)
print("RECOMMANDATION:")
print("=" * 60)

# Trouver le calendrier principal
for calendar in calendar_list.get('items', []):
    if calendar.get('primary'):
        print(f"✅ Utilise cet ID dans ERPNext: {calendar['id']}")
        print(f"   (C'est ton calendrier principal)")
        break
```

Ce script te montrera :
- 🌟 Ton calendrier principal (le bon)
- 📅 Les autres calendriers (dont celui créé par ERPNext)
- Le nombre d'événements dans chaque calendrier

**Copie l'ID du calendrier avec 🌟** et utilise-le dans ERPNext !

## 🗑️ Optionnel : Supprimer le faux calendrier "primary"

Une fois que la synchro fonctionne avec le bon calendrier :

1. **Aller sur [calendar.google.com](https://calendar.google.com)**

2. **Dans la liste des calendriers à gauche**, trouve le calendrier nommé "primary" (celui qui est vide)

3. **Cliquer sur les 3 points → Paramètres et partage**

4. **Descendre tout en bas → "Supprimer l'agenda"**

5. **Confirmer**

Ça nettoiera ton Google Calendar.

## 📋 Checklist de vérification

Après avoir reconfiguré :

- [ ] Dans Google Settings, le Calendar ID est celui de ton vrai calendrier (ton email)
- [ ] Tu as cliqué sur "Synchronize" ou réautorisé
- [ ] Dans ERPNext Event List, tu vois maintenant tes rendez-vous
- [ ] Quand tu crées un Event dans ERPNext, il apparaît dans le BON calendrier Google
- [ ] Quand tu crées un rdv dans Google Calendar, il apparaît dans ERPNext

## 🎯 Pourquoi ça arrive ?

ERPNext utilise le terme `"primary"` de deux façons :

1. **`primary` comme ID spécial Google** : Un alias pour "le calendrier principal du user"
2. **`"primary"` comme nom** : Un nom de calendrier que tu pourrais créer

Quand tu mets `"primary"` dans le champ Calendar Name, ERPNext a peut-être :
- Cherché un calendrier avec le NOM "primary" (pas trouvé)
- Créé un nouveau calendrier avec ce nom

Au lieu de :
- Utiliser l'ID spécial `primary` qui pointe vers ton calendrier principal

## 🚀 Solution permanente : Créer ta propre intégration

Pour éviter ces problèmes à l'avenir, je te recommande de créer ton **propre intégration Google Calendar custom** où tu contrôles tout :

1. **Suivre le plan** : [PRPs/meeting-management-google-calendar.md](../PRPs/meeting-management-google-calendar.md)

2. **Dans ton code, utiliser explicitement :**
   ```python
   # Toujours utiliser le calendrier principal
   CALENDAR_ID = "primary"  # L'alias spécial Google

   # OU récupérer dynamiquement l'email du user
   calendar_id = frappe.db.get_value("User", frappe.session.user, "email")
   ```

3. **Avantages :**
   - ✅ Contrôle total sur quel calendrier est utilisé
   - ✅ Meilleure gestion des erreurs
   - ✅ Interface en français
   - ✅ Fonctionnalités personnalisées

## 💡 Astuce rapide pour tester

Pour vérifier quel calendrier ERPNext utilise actuellement :

```python
# Dans bench console
import frappe
from frappe.integrations.doctype.google_calendar.google_calendar import get_google_calendar_object

calendar_service = get_google_calendar_object()

# Récupérer le calendar_id configuré
calendar_id = frappe.db.get_single_value("Google Calendar", "google_calendar_id") or "primary"

print(f"Calendar ID configuré dans ERPNext: {calendar_id}")

# Tester l'accès
try:
    calendar_info = calendar_service.calendars().get(calendarId=calendar_id).execute()
    print(f"Nom du calendrier: {calendar_info['summary']}")
    print(f"Description: {calendar_info.get('description', 'N/A')}")
except Exception as e:
    print(f"Erreur: {e}")
```

## 📞 Résumé rapide

**Le problème :** ERPNext synchronise sur un calendrier "primary" qu'il a créé, pas ton vrai calendrier principal.

**La solution :**
1. Trouve l'ID de ton vrai calendrier (généralement ton email)
2. Va dans Google Settings → Calendar ID → Mets ton email
3. Sauvegarde et synchronise
4. Tes rdvs devraient apparaître !

**Test rapide :**
```bash
bench console
```
```python
from frappe.integrations.doctype.google_calendar.google_calendar import sync
sync()
```

Puis vérifie dans Event List !
