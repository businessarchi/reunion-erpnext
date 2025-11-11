# Fix Google Calendar sur Frappe Cloud

## 🌐 Tu es sur Frappe Cloud

Sur Frappe Cloud, tu n'as pas accès à `bench console` directement. Voici les solutions adaptées.

## ✅ Solution 1 : Créer une page de diagnostic custom (Recommandé)

### Créer un fichier Python pour diagnostiquer

Crée ce fichier dans ton app :

**Fichier :** `frappe_app/www/google-calendar-debug.py`

```python
import frappe
from frappe import _

def get_context(context):
    """Page de diagnostic Google Calendar"""
    context.no_cache = 1
    context.show_sidebar = False

    # Vérifier si l'utilisateur est autorisé
    if not frappe.has_permission("Google Settings", "read"):
        context.error = "Vous n'avez pas les permissions nécessaires"
        return context

    try:
        from frappe.integrations.doctype.google_calendar.google_calendar import get_google_calendar_object

        # Récupérer le service Google Calendar
        calendar_service = get_google_calendar_object()

        if not calendar_service:
            context.error = "Service Google Calendar non disponible. Vérifiez l'autorisation OAuth."
            return context

        # Lister tous les calendriers
        calendar_list = calendar_service.calendarList().list().execute()
        calendars = []

        for calendar in calendar_list.get('items', []):
            # Compter les événements
            event_count = 0
            try:
                events = calendar_service.events().list(
                    calendarId=calendar['id'],
                    maxResults=50
                ).execute()
                event_count = len(events.get('items', []))
            except:
                event_count = "Erreur"

            calendars.append({
                'summary': calendar.get('summary', 'Sans nom'),
                'id': calendar['id'],
                'is_primary': calendar.get('primary', False),
                'access_role': calendar.get('accessRole', 'N/A'),
                'event_count': event_count
            })

        context.calendars = calendars
        context.success = True

    except Exception as e:
        context.error = str(e)
        frappe.log_error(frappe.get_traceback(), "Google Calendar Debug Error")

    return context
```

**Fichier :** `frappe_app/www/google-calendar-debug.html`

```html
{% extends "templates/web.html" %}

{% block title %}Google Calendar - Diagnostic{% endblock %}

{% block page_content %}
<div class="container mt-5">
    <h1>🔍 Diagnostic Google Calendar</h1>

    {% if error %}
    <div class="alert alert-danger">
        <strong>Erreur :</strong> {{ error }}
    </div>
    {% endif %}

    {% if success %}
    <div class="alert alert-success">
        ✅ Connexion Google Calendar réussie !
    </div>

    <h3>📅 Vos calendriers Google</h3>
    <p>Copiez l'ID du calendrier avec l'étoile 🌟 (votre calendrier principal)</p>

    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Nom</th>
                    <th>ID du calendrier</th>
                    <th>Accès</th>
                    <th>Événements</th>
                </tr>
            </thead>
            <tbody>
                {% for calendar in calendars %}
                <tr class="{% if calendar.is_primary %}table-success{% endif %}">
                    <td>
                        {% if calendar.is_primary %}
                        <span class="badge bg-warning">🌟 PRINCIPAL</span>
                        {% else %}
                        📅
                        {% endif %}
                    </td>
                    <td>{{ calendar.summary }}</td>
                    <td>
                        <code id="cal-{{ loop.index }}">{{ calendar.id }}</code>
                        <button class="btn btn-sm btn-primary"
                                onclick="copyToClipboard('{{ calendar.id }}', {{ loop.index }})">
                            Copier
                        </button>
                    </td>
                    <td>{{ calendar.access_role }}</td>
                    <td>
                        <span class="badge bg-info">{{ calendar.event_count }}</span>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="alert alert-info mt-4">
        <h5>📝 Instructions :</h5>
        <ol>
            <li>Copie l'<strong>ID du calendrier principal</strong> (celui avec 🌟)</li>
            <li>Va dans <strong>Setup → Integrations → Google Settings</strong></li>
            <li>Dans le champ "Calendar" ou "Calendar ID", colle cet ID</li>
            <li>Sauvegarde et synchronise</li>
        </ol>
    </div>

    <div class="mt-4">
        <a href="/app/google-settings" class="btn btn-primary">
            Aller dans Google Settings
        </a>
        <a href="/app/event" class="btn btn-success">
            Voir les Events
        </a>
    </div>

    {% endif %}
</div>

<script>
function copyToClipboard(text, index) {
    navigator.clipboard.writeText(text).then(function() {
        frappe.show_alert({
            message: 'ID copié dans le presse-papier !',
            indicator: 'green'
        });
    });
}
</script>
{% endblock %}
```

### Déployer sur Frappe Cloud

1. **Commit et push ton code :**
   ```bash
   cd /Users/melodie/Documents/GitHub/ERPnext/reunion-erpnext
   git add .
   git commit -m "Add Google Calendar diagnostic page"
   git push origin main
   ```

2. **Sur Frappe Cloud, déployer l'app :**
   - Va sur ton dashboard Frappe Cloud
   - Trouve ton site
   - Clique sur "Deploy" ou "Update Apps"

3. **Accéder à la page de diagnostic :**
   ```
   https://architecte.business/google-calendar-debug
   ```

4. **Copier l'ID du calendrier principal** (celui avec 🌟)

5. **Configurer dans ERPNext :**
   - Setup → Integrations → Google Settings
   - Coller l'ID dans le champ Calendar
   - Sauvegarder

---

## ✅ Solution 2 : Via l'interface ERPNext directement (Plus simple)

### Méthode manuelle sans code

1. **Aller sur [calendar.google.com](https://calendar.google.com)**

2. **Identifier ton calendrier principal** (celui avec tous tes rendez-vous)

3. **Cliquer sur les 3 points à côté → "Paramètres et partage"**

4. **Dans la section "Intégrer l'agenda"**, tu verras :
   - **ID de l'agenda** : C'est ton email (ex: `melodie@architecte.business`)

5. **Copier cet ID**

6. **Dans ERPNext :**
   ```
   Setup → Integrations → Google Settings
   ```

7. **Trouver le champ pour le Calendar ID**

8. **Remplacer par ton email**

9. **Sauvegarder et cliquer sur "Authorize API Access"**

---

## ✅ Solution 3 : Créer une API whitelisted

Si tu veux un script exécutable via l'interface ERPNext :

**Fichier :** `frappe_app/meeting_management/api/google_debug.py`

```python
import frappe
from frappe.integrations.doctype.google_calendar.google_calendar import get_google_calendar_object

@frappe.whitelist()
def list_google_calendars():
    """Liste tous les calendriers Google accessibles"""
    try:
        calendar_service = get_google_calendar_object()

        if not calendar_service:
            return {
                "success": False,
                "message": "Service Google Calendar non disponible"
            }

        calendar_list = calendar_service.calendarList().list().execute()
        calendars = []

        for calendar in calendar_list.get('items', []):
            # Compter les événements
            event_count = 0
            try:
                events = calendar_service.events().list(
                    calendarId=calendar['id'],
                    maxResults=50
                ).execute()
                event_count = len(events.get('items', []))
            except:
                event_count = 0

            calendars.append({
                'summary': calendar.get('summary', 'Sans nom'),
                'id': calendar['id'],
                'is_primary': calendar.get('primary', False),
                'access_role': calendar.get('accessRole', 'N/A'),
                'event_count': event_count,
                'description': calendar.get('description', '')
            })

        return {
            "success": True,
            "calendars": calendars
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "List Google Calendars Error")
        return {
            "success": False,
            "message": str(e)
        }

@frappe.whitelist()
def force_sync_google_calendar():
    """Force une synchronisation Google Calendar"""
    try:
        from frappe.integrations.doctype.google_calendar.google_calendar import sync
        sync()
        return {
            "success": True,
            "message": "Synchronisation lancée avec succès"
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Force Sync Error")
        return {
            "success": False,
            "message": str(e)
        }
```

**Ensuite, tu peux appeler cette méthode dans la console du navigateur :**

1. **Ouvre la console JavaScript** (F12) sur ton site ERPNext

2. **Exécute :**
   ```javascript
   frappe.call({
       method: 'frappe_app.meeting_management.api.google_debug.list_google_calendars',
       callback: function(r) {
           console.log('Calendriers disponibles:', r.message);

           if (r.message.success) {
               r.message.calendars.forEach(function(cal) {
                   console.log(
                       (cal.is_primary ? '🌟 PRINCIPAL:' : '📅'),
                       cal.summary,
                       '| ID:', cal.id,
                       '| Événements:', cal.event_count
                   );
               });
           }
       }
   });
   ```

3. **Regarde les résultats dans la console**

4. **Copie l'ID du calendrier principal** (celui avec 🌟)

---

## 🎯 Méthode la plus rapide (Sans code)

### Étape par étape

1. **Va sur [calendar.google.com](https://calendar.google.com)**

2. **Note le nom de ton calendrier principal** (celui avec tous tes rdvs)

3. **Dans ERPNext :**
   ```
   Setup → Integrations → Google Settings
   ```

4. **Dans le champ "Google Calendar" ou "Calendar"** :
   - Si tu vois une **liste déroulante** : sélectionne ton vrai calendrier
   - Si c'est un **champ texte** : entre ton **email Google complet**

5. **Coche bien ces options :**
   - ✅ Enable Google Calendar
   - ✅ Pull from Google Calendar (pour importer de Google)
   - ✅ Push to Google Calendar (pour exporter vers Google)

6. **Sauvegarde**

7. **Clique sur "Authorize API Access"** pour reconnecter

8. **Attends 2-3 minutes** pour la synchronisation

9. **Va dans : Home → CRM → Event**

10. **Tes rendez-vous devraient apparaître !**

---

## 🗑️ Supprimer le faux calendrier "primary"

Une fois que ça marche :

1. **Va sur [calendar.google.com](https://calendar.google.com)**

2. **Trouve le calendrier nommé "primary"** (celui qui est vide)

3. **Clique sur les 3 points → Paramètres et partage**

4. **Descendre → "Supprimer l'agenda"**

5. **Confirmer**

---

## 📝 Checklist

- [ ] J'ai identifié l'email/ID de mon vrai calendrier Google principal
- [ ] J'ai mis cet ID dans ERPNext → Google Settings → Calendar
- [ ] J'ai coché "Pull from Google Calendar"
- [ ] J'ai sauvegardé et réautorisé
- [ ] J'ai attendu 2-3 minutes
- [ ] Je vois mes rendez-vous dans ERPNext → Event

---

## 🆘 Si ça ne marche toujours pas

**Donne-moi ces infos :**

1. L'email de ton compte Google
2. Capture d'écran de ta page Google Settings dans ERPNext
3. Le message d'erreur (s'il y en a un)

Et je t'aiderai à corriger !
