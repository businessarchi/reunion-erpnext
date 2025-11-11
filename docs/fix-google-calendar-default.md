# Fix : Accès au calendrier par défaut Google Calendar dans ERPNext

## Problème
Vous arrivez à vous connecter à Google Calendar depuis ERPNext mais vous ne pouvez pas accéder à votre calendrier par défaut.

## Diagnostic

Le problème vient généralement de l'un de ces 4 points :
1. **Scopes OAuth insuffisants** : ERPNext n'a pas les bonnes permissions
2. **Calendar ID mal configuré** : ERPNext ne pointe pas vers "primary"
3. **Autorisation incomplète** : Vous n'avez pas accordé toutes les permissions lors de l'OAuth
4. **Configuration ERPNext incorrecte**

## Solutions étape par étape

### Solution 1 : Vérifier et corriger les Google Settings

1. **Aller dans ERPNext → Setup → Integrations → Google Settings**

2. **Vérifier les champs suivants :**
   - `Enabled` : Doit être coché ✅
   - `Client ID` : Votre client ID Google Cloud
   - `Client Secret` : Votre client secret Google Cloud

3. **Section "Google Calendar"**
   - Cocher `Enable Google Calendar`
   - Dans le champ `Calendar Name`, mettre exactement : **`primary`**
   - Ne pas mettre d'email ou d'autre ID

4. **Sauvegarder**

5. **Cliquer sur "Authorize API Access"** et réautoriser

---

### Solution 2 : Vérifier les Scopes OAuth dans Google Cloud

1. **Aller sur [Google Cloud Console](https://console.cloud.google.com/)**

2. **Sélectionner votre projet**

3. **Aller dans : APIs & Services → OAuth consent screen**

4. **Vérifier que les scopes suivants sont ajoutés :**
   ```
   https://www.googleapis.com/auth/calendar
   ```
   OU au minimum :
   ```
   https://www.googleapis.com/auth/calendar.events
   ```

5. **NE PAS utiliser uniquement** :
   ```
   https://www.googleapis.com/auth/calendar.app.created  ❌
   ```
   Ce scope ne donne accès qu'aux calendriers créés par l'app !

6. **Sauvegarder et réautoriser depuis ERPNext**

---

### Solution 3 : Révoquer et réautoriser complètement

1. **Révoquer l'accès existant :**
   - Aller sur [myaccount.google.com/permissions](https://myaccount.google.com/permissions)
   - Trouver votre application ERPNext
   - Cliquer sur "Remove Access"

2. **Dans ERPNext :**
   - Aller dans Google Settings
   - Cliquer sur "Authorize API Access"
   - **Bien vérifier que la page Google demande l'accès à "See, edit, share, and permanently delete all the calendars you can access"**
   - Autoriser complètement

3. **Tester l'accès**

---

### Solution 4 : Vérifier manuellement via Python (Diagnostic avancé)

Si les solutions ci-dessus ne fonctionnent pas, vous pouvez tester l'accès directement :

1. **Ouvrir la console Frappe :**
   ```bash
   bench console
   ```

2. **Tester l'accès au calendrier :**
   ```python
   from frappe.integrations.doctype.google_calendar.google_calendar import get_google_calendar_object

   # Récupérer le service Google Calendar
   calendar_service = get_google_calendar_object()

   # Lister les calendriers accessibles
   calendar_list = calendar_service.calendarList().list().execute()

   print("Calendriers accessibles :")
   for calendar in calendar_list.get('items', []):
       print(f"  - ID: {calendar['id']}")
       print(f"    Nom: {calendar['summary']}")
       print(f"    Primary: {calendar.get('primary', False)}")
       print()
   ```

3. **Vérifier la sortie :**
   - Vous devriez voir un calendrier avec `primary: True`
   - Si vous ne voyez aucun calendrier ou seulement des calendriers créés par l'app, c'est un problème de scope

---

### Solution 5 : Créer une application custom si ERPNext ne supporte pas bien

Si ERPNext ne permet pas d'accéder au calendrier par défaut avec sa configuration standard, vous pouvez créer une application custom :

1. **Créer votre propre intégration Google Calendar** (voir le plan d'implémentation dans `PRPs/meeting-management-google-calendar.md`)

2. **Contrôler complètement les scopes OAuth :**
   - Utiliser `https://www.googleapis.com/auth/calendar.events`
   - Spécifier `calendar_id = "primary"` dans votre code

3. **Avantages :**
   - Contrôle total sur l'intégration
   - Meilleure gestion des erreurs
   - Fonctionnalités personnalisées

---

## Checklist de vérification

Avant de contacter le support, vérifier :

- [ ] Google Calendar API est activée dans Google Cloud Console
- [ ] Les credentials OAuth (Client ID, Client Secret) sont corrects
- [ ] Les scopes OAuth incluent `calendar` ou `calendar.events`
- [ ] Le champ "Calendar Name" dans ERPNext est défini sur `primary`
- [ ] Vous avez réautorisé l'accès après modification des scopes
- [ ] Votre compte Google a bien un calendrier par défaut
- [ ] Vous n'avez pas d'erreurs dans ERPNext Error Log

---

## Scopes OAuth recommandés

Pour une intégration complète Google Calendar :

| Scope | Description | Recommandé |
|-------|-------------|-----------|
| `https://www.googleapis.com/auth/calendar` | Accès complet lecture/écriture | ✅ Oui |
| `https://www.googleapis.com/auth/calendar.events` | Lecture/écriture événements seulement | ✅ Oui (minimum) |
| `https://www.googleapis.com/auth/calendar.readonly` | Lecture seule | ⚠️ Si vous ne voulez pas modifier |
| `https://www.googleapis.com/auth/calendar.app.created` | Uniquement calendriers créés par l'app | ❌ Non pour calendrier par défaut |

---

## Codes d'erreur courants

| Erreur | Cause | Solution |
|--------|-------|----------|
| `403 Forbidden` | Scope insuffisant | Vérifier les scopes OAuth |
| `404 Not Found` | Calendar ID incorrect | Utiliser "primary" |
| `401 Unauthorized` | Token expiré ou invalide | Réautoriser |
| `Calendar not found` | Calendar ID n'existe pas | Vérifier que le calendrier existe |

---

## Ressources

- [ERPNext Google Calendar Documentation](https://docs.frappe.io/erpnext/user/manual/en/google_calendar)
- [Google Calendar API Scopes](https://developers.google.com/workspace/calendar/api/auth)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Gérer les accès Google](https://myaccount.google.com/permissions)

---

## Besoin d'aide ?

Si aucune de ces solutions ne fonctionne :

1. **Vérifier les logs ERPNext :**
   - Aller dans `Error Log` dans ERPNext
   - Chercher les erreurs liées à Google Calendar

2. **Poster sur le forum Frappe :**
   - [Frappe Forum - ERPNext](https://discuss.frappe.io/)
   - Inclure : version ERPNext, message d'erreur exact, scopes configurés

3. **Option custom :**
   - Implémenter votre propre intégration avec le plan dans `PRPs/meeting-management-google-calendar.md`
   - Contrôle total et meilleure intégration avec vos besoins spécifiques
