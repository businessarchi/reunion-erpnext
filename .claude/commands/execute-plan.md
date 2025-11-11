---
description: Exécuter un plan de développement avec intégration complète de la gestion des tâches Archon
argument-hint: [chemin-fichier-plan]
---

# Exécuter un plan de développement avec la gestion des tâches Archon

Vous allez exécuter un plan de développement complet avec la gestion intégrée des tâches Archon. Ce workflow garantit un suivi systématique des tâches et de l'implémentation tout au long du processus de développement.

## Exigences critiques

**OBLIGATOIRE** : Tout au long de l'exécution de ce plan, vous DEVEZ maintenir une utilisation continue d'Archon pour la gestion des tâches. NE PAS abandonner ou sauter l'intégration Archon à aucun moment. Chaque tâche du plan doit être suivie dans Archon de la création à la finalisation.

## Étape 1 : Lire et analyser le plan

Lire le fichier de plan spécifié dans : $ARGUMENTS

Le fichier de plan contiendra :
- Une liste de tâches à implémenter
- Des références aux composants existants du code et points d'intégration
- Le contexte sur où chercher dans le code pour l'implémentation

## Étape 2 : Configuration du projet dans Archon

1. Vérifier si un ID de projet est spécifié dans CLAUDE.md pour cette fonctionnalité
   - Chercher toute référence de projet Archon dans CLAUDE.md
   - Si trouvé, utiliser cet ID de projet

2. Si aucun projet n'existe :
   - Créer un nouveau projet dans Archon avec `mcp__archon__manage_project`
   - Utiliser un titre descriptif basé sur les objectifs du plan
   - Conserver l'ID du projet pour l'utiliser tout au long de l'exécution

## Étape 3 : Créer toutes les tâches dans Archon

Pour CHAQUE tâche identifiée dans le plan :
1. Créer une tâche correspondante dans Archon avec `mcp__archon__manage_task("create", ...)`
2. Définir le statut initial comme "todo"
3. Inclure les descriptions détaillées du plan
4. Maintenir l'ordre/priorité des tâches du plan

**IMPORTANT** : Créer TOUTES les tâches dans Archon dès le début avant de commencer l'implémentation. Cela assure une visibilité complète de la portée du travail.

## Étape 4 : Analyse du code existant

Avant de commencer l'implémentation :
1. Analyser TOUS les points d'intégration mentionnés dans le plan
2. Utiliser les outils Grep et Glob pour :
   - Comprendre les patterns de code existants
   - Identifier où les changements doivent être faits
   - Trouver des implémentations similaires comme référence
3. Lire tous les fichiers et composants référencés
4. Construire une compréhension complète du contexte du code

## Étape 5 : Cycle d'implémentation

Pour CHAQUE tâche dans l'ordre :

### 5.1 Démarrer la tâche
- Passer la tâche actuelle au statut "doing" dans Archon : `mcp__archon__manage_task("update", task_id=..., status="doing")`
- Utiliser TodoWrite pour suivre les sous-tâches locales si nécessaire

### 5.2 Implémenter
- Exécuter l'implémentation basée sur :
  - Les exigences de la tâche du plan
  - Les résultats de votre analyse du code
  - Les bonnes pratiques et patterns existants
- Effectuer tous les changements de code nécessaires
- Assurer la qualité et la cohérence du code

### 5.3 Finaliser la tâche
- Une fois l'implémentation terminée, passer la tâche au statut "review" : `mcp__archon__manage_task("update", task_id=..., status="review")`
- NE PAS marquer comme "done" encore - cela vient après la validation

### 5.4 Passer à la suivante
- Passer à la tâche suivante dans la liste
- Répéter les étapes 5.1-5.3

**CRITIQUE** : Une SEULE tâche doit être au statut "doing" à la fois. Terminer chaque tâche avant de commencer la suivante.

## Étape 6 : Phase de validation

Après que TOUTES les tâches sont au statut "review" :

**IMPORTANT : Utiliser l'agent `validator` pour des tests complets**
1. Lancer l'agent validator via l'outil Task
   - Fournir au validator une description détaillée de ce qui a été construit
   - Inclure la liste des fonctionnalités implémentées et fichiers modifiés
   - Le validator créera des tests unitaires simples et efficaces
   - Il exécutera les tests et rapportera les résultats

L'agent validator va :
- Créer des tests unitaires ciblés pour les fonctionnalités principales
- Tester les cas limites critiques et la gestion d'erreurs
- Exécuter les tests avec le framework de test du projet
- Rapporter ce qui a été testé et les problèmes trouvés

Validation supplémentaire que vous devez effectuer :
- Vérifier les problèmes d'intégration entre composants
- S'assurer que tous les critères d'acceptation du plan sont satisfaits

## Étape 7 : Finaliser les tâches dans Archon

Après une validation réussie :

1. Pour chaque tâche ayant une couverture de tests unitaires correspondante :
   - Passer du statut "review" à "done" : `mcp__archon__manage_task("update", task_id=..., status="done")`

2. Pour les tâches sans couverture de tests :
   - Laisser au statut "review" pour attention future
   - Documenter pourquoi elles restent en review (ex: "En attente de tests d'intégration")

## Étape 8 : Rapport final

Fournir un résumé incluant :
- Total des tâches créées et terminées
- Tâches restant en review et pourquoi
- Couverture de tests atteinte
- Fonctionnalités clés implémentées
- Problèmes rencontrés et comment ils ont été résolus

## Règles du workflow

1. **JAMAIS** sauter la gestion des tâches Archon à aucun moment
2. **TOUJOURS** créer toutes les tâches dans Archon avant de commencer l'implémentation
3. **MAINTENIR** une tâche au statut "doing" à la fois
4. **VALIDER** tout le travail avant de marquer les tâches comme "done"
5. **SUIVRE** le progrès continuellement via les mises à jour de statut Archon
6. **ANALYSER** le code en profondeur avant l'implémentation
7. **TESTER** tout avant la finalisation

## Gestion des erreurs

Si à tout moment les opérations Archon échouent :
1. Réessayer l'opération
2. Si échecs persistants, documenter le problème mais continuer le suivi localement
3. Ne jamais abandonner l'intégration Archon - trouver des solutions de contournement si nécessaire

Rappel : Le succès de cette exécution dépend du maintien d'une gestion systématique des tâches via Archon tout au long du processus. Cela garantit la responsabilité, le suivi du progrès et une livraison de qualité.