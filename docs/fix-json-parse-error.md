# Fix : Erreur "Aucun événement is not valid JSON" - Google Calendar ERPNext

## 🐛 Problème

Erreur JavaScript dans la console :
```
jQuery.Deferred exception: Unexpected token 'A', "Aucun évén"... is not valid JSON
SyntaxError: Unexpected token 'A', "Aucun évén"... is not valid JSON
```

## 🔍 Diagnostic

Le problème vient de :
1. **Une méthode Python retourne une chaîne de texte** `"Aucun événement"` au lieu d'un JSON valide
2. **Le JavaScript essaie de parser cette chaîne comme du JSON** et échoue
3. **Cela se produit probablement quand il n'y a pas d'événements** dans Google Calendar

## ✅ Solution : Corriger le code backend

### Localiser le fichier problématique

L'erreur vient probablement d'un fichier Python custom ou d'une surcharge de la méthode Google Calendar.

Recherchons où se trouve le code :

```bash
# Dans votre site ERPNext
cd frappe-bench

# Chercher les fichiers qui retournent "Aucun événement"
grep -r "Aucun événement" --include="*.py" apps/
grep -r "Aucun évén" --include="*.py" apps/
```

### Correction standard

Le code devrait ressembler à ceci :

#### ❌ Code incorrect (retourne du texte)

```python
@frappe.whitelist()
def get_google_calendar_events():
    """Récupère les événements Google Calendar"""
    try:
        # ... code pour récupérer les événements ...

        if not events:
            return "Aucun événement"  # ❌ MAUVAIS : Retourne du texte

        return events
    except Exception as e:
        return f"Erreur : {str(e)}"  # ❌ MAUVAIS : Retourne du texte
```

#### ✅ Code correct (retourne du JSON)

```python
@frappe.whitelist()
def get_google_calendar_events():
    """Récupère les événements Google Calendar"""
    try:
        # ... code pour récupérer les événements ...

        if not events:
            return {
                "success": True,
                "message": "Aucun événement trouvé",
                "events": []
            }

        return {
            "success": True,
            "message": "Événements récupérés",
            "events": events
        }
    except Exception as e:
        frappe.log_error(str(e), "Google Calendar Error")
        return {
            "success": False,
            "message": f"Erreur : {str(e)}",
            "events": []
        }
```

## 📁 Fichiers à vérifier

### 1. Fichier Google Calendar standard de Frappe

Si vous utilisez l'intégration native ERPNext, le fichier est :

```
frappe-bench/apps/frappe/frappe/integrations/doctype/google_calendar/google_calendar.py
```

**NE PAS MODIFIER CE FICHIER DIRECTEMENT** - Utilisez plutôt des hooks ou créez une app custom.

### 2. Si vous avez du code custom

Cherchez dans votre app custom :

```bash
# Chercher les méthodes whitelisted qui retournent du texte
grep -r "@frappe.whitelist()" frappe-bench/apps/frappe_app/ -A 20 | grep -i "google\|calendar"
```

### 3. Créer une surcharge propre

Si vous devez corriger le comportement, créez une surcharge :

```python
# frappe_app/meeting_management/api/google_calendar_fix.py

import frappe
from frappe.integrations.doctype.google_calendar.google_calendar import get_google_calendar_object

@frappe.whitelist()
def get_events_fixed(start, end):
    """
    Version corrigée qui retourne toujours du JSON valide
    """
    try:
        # Récupérer le service Google Calendar
        calendar_service = get_google_calendar_object()

        if not calendar_service:
            return {
                "success": False,
                "message": "Service Google Calendar non disponible",
                "events": []
            }

        # Récupérer les événements
        calendar_id = frappe.db.get_single_value("Google Calendar", "calendar_id") or "primary"

        events_result = calendar_service.events().list(
            calendarId=calendar_id,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return {
                "success": True,
                "message": "Aucun événement trouvé dans cette période",
                "events": []
            }

        # Formatter les événements pour ERPNext
        formatted_events = []
        for event in events:
            formatted_events.append({
                "id": event.get("id"),
                "subject": event.get("summary", "Sans titre"),
                "starts_on": event.get("start", {}).get("dateTime", event.get("start", {}).get("date")),
                "ends_on": event.get("end", {}).get("dateTime", event.get("end", {}).get("date")),
                "description": event.get("description", ""),
                "location": event.get("location", "")
            })

        return {
            "success": True,
            "message": f"{len(formatted_events)} événement(s) trouvé(s)",
            "events": formatted_events
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Google Calendar Get Events Error")
        return {
            "success": False,
            "message": str(e),
            "events": []
        }
```

## 🔧 Fix immédiat : Patch JavaScript

Si vous ne pouvez pas modifier le backend immédiatement, vous pouvez patcher le JavaScript :

### Créer un fichier JavaScript custom

```javascript
// frappe_app/public/js/google_calendar_fix.js

frappe.provide("frappe.integrations.google_calendar");

// Surcharger la méthode frappe.msgprint pour gérer les cas non-JSON
const original_msgprint = frappe.msgprint;

frappe.msgprint = function(msg, title) {
    // Si le message ressemble à une erreur de parsing Google Calendar
    if (typeof msg === 'string' && msg.includes('Aucun événement')) {
        // Afficher un message propre
        return original_msgprint({
            title: title || __('Google Calendar'),
            indicator: 'blue',
            message: __('Aucun événement trouvé dans la période sélectionnée')
        });
    }

    // Sinon, comportement normal
    return original_msgprint(msg, title);
};

// Alternative : wrapper pour les appels Google Calendar
frappe.call_google_calendar_safe = function(method, args, callback) {
    return frappe.call({
        method: method,
        args: args,
        callback: function(r) {
            // Vérifier si la réponse est du JSON valide
            if (r.message && typeof r.message === 'string') {
                try {
                    // Essayer de parser comme JSON
                    const parsed = JSON.parse(r.message);
                    r.message = parsed;
                } catch (e) {
                    // Si ce n'est pas du JSON, créer un objet standard
                    console.warn('Response is not JSON:', r.message);
                    r.message = {
                        success: false,
                        message: r.message,
                        events: []
                    };
                }
            }

            if (callback) {
                callback(r);
            }
        },
        error: function(r) {
            frappe.msgprint({
                title: __('Erreur Google Calendar'),
                indicator: 'red',
                message: __('Impossible de récupérer les événements')
            });
        }
    });
};
```

### Inclure ce fichier dans hooks.py

```python
# frappe_app/hooks.py

app_include_js = [
    "/assets/frappe_app/js/google_calendar_fix.js"
]
```

### Rebuild les assets

```bash
bench build --app frappe_app
bench clear-cache
```

## 🎯 Solution recommandée : Créer votre propre intégration

Le meilleur fix à long terme est de **créer votre propre intégration Google Calendar** au lieu d'utiliser celle d'ERPNext native qui semble avoir des problèmes.

Suivez le plan d'implémentation : [PRPs/meeting-management-google-calendar.md](../PRPs/meeting-management-google-calendar.md)

### Avantages :

✅ **Contrôle total** sur le format des réponses JSON
✅ **Meilleure gestion des erreurs**
✅ **Messages en français** adaptés à votre contexte
✅ **Fonctionnalités personnalisées** pour votre gestion de réunions
✅ **Pas de dépendance** aux bugs de l'intégration native ERPNext

## 🔍 Debugging avancé

### Trouver exactement où se produit l'erreur

1. **Ouvrir la console du navigateur** (F12)

2. **Cliquer sur l'erreur** pour voir la stack trace complète

3. **Identifier le fichier JS** qui appelle la méthode problématique

L'erreur mentionne :
```
at Object.eval (google_calendar__js:48:14)
```

Cela indique que le code est dans un fichier `google_calendar.js` ligne 48.

4. **Chercher ce fichier** :

```bash
find frappe-bench/apps -name "*google_calendar*.js" -type f
```

5. **Regarder le code autour de la ligne 48** pour voir quel appel `frappe.call()` ou `frappe.msgprint()` cause le problème

### Intercepter l'appel réseau

1. **Dans la console Chrome, aller dans l'onglet Network**

2. **Filtrer par "XHR"**

3. **Déclencher l'action** qui cause l'erreur (par exemple, ouvrir le calendrier)

4. **Trouver la requête** vers une méthode Google Calendar

5. **Regarder la réponse** :
   - Si c'est `"Aucun événement"` en texte brut → Le backend est le problème
   - Si c'est du JSON mais mal formé → Problème de parsing backend
   - Si c'est du JSON valide → Problème de traitement frontend

### Log détaillé

Ajouter du logging dans le code Python :

```python
# Dans la méthode problématique
import frappe
import json

@frappe.whitelist()
def problematic_method():
    try:
        result = get_events()

        # Logger ce qui est retourné
        frappe.log_error(
            f"Type: {type(result)}, Value: {result}",
            "Google Calendar Response Debug"
        )

        # S'assurer que c'est du JSON
        if isinstance(result, str):
            # Si c'est une string, la convertir en dict
            result = {"message": result, "events": []}

        return result

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Google Calendar Error")
        return {"success": False, "message": str(e)}
```

## 📚 Checklist de résolution

- [ ] Identifier le fichier Python qui retourne "Aucun événement"
- [ ] Corriger pour retourner un dict/JSON au lieu d'une string
- [ ] Tester avec `bench console` que la méthode retourne du JSON
- [ ] Rebuild les assets : `bench build`
- [ ] Clear cache : `bench clear-cache`
- [ ] Redémarrer : `bench restart`
- [ ] Tester dans le navigateur
- [ ] Vérifier qu'il n'y a plus d'erreur dans la console
- [ ] Vérifier que les événements s'affichent correctement

## 🚀 Alternative rapide : Désactiver temporairement

Si vous voulez juste que ça arrête de casser, vous pouvez désactiver temporairement la synchronisation :

1. **Aller dans Google Settings**
2. **Décocher "Enable Google Calendar"**
3. **Save**

Puis travaillez sur une vraie solution (votre propre intégration custom).

## 📞 Besoin d'aide ?

Si vous me montrez :
1. Le code exact du fichier qui cause l'erreur
2. La méthode Python appelée
3. Le contexte (quand l'erreur se produit)

Je peux vous créer un fix précis et immédiat !

---

**TL;DR** : Le backend retourne `"Aucun événement"` (string) au lieu de `{"events": []}` (JSON). Il faut corriger la méthode Python pour toujours retourner du JSON valide, même quand il n'y a pas d'événements.
