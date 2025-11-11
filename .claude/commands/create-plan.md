---
description: Créer un plan d'implémentation complet à partir d'un document d'exigences via une recherche approfondie
argument-hint: [chemin-fichier-exigences]
---

# Créer un plan d'implémentation à partir des exigences

Vous allez créer un plan d'implémentation complet basé sur des exigences initiales. Cela implique une recherche approfondie, une analyse et une planification pour produire une feuille de route détaillée pour l'exécution.

## Étape 1 : Lire et analyser les exigences

Lire le document d'exigences depuis : $ARGUMENTS

Extraire et comprendre :
- Les demandes de fonctionnalités principales et objectifs
- Les exigences techniques et contraintes
- Les résultats attendus et critères de succès
- Les points d'intégration avec les systèmes existants
- Les exigences de performance et évolutivité
- Les technologies ou frameworks spécifiques mentionnés

## Étape 2 : Phase de recherche

### 2.1 Recherche dans la base de connaissances (si demandé)
Si Archon RAG est disponible et pertinent :
- Utiliser `mcp__archon__rag_get_available_sources()` pour voir la documentation disponible
- Rechercher des motifs pertinents : `mcp__archon__rag_search_knowledge_base(query="...")`
- Trouver des exemples de code : `mcp__archon__rag_search_code_examples(query="...")`
- Se concentrer sur les patterns d'implémentation, bonnes pratiques et fonctionnalités similaires

### 2.2 Analyse du code existant (pour les projets existants)
Si c'est pour un code existant :

**IMPORTANT : Utiliser l'agent `codebase-analyst` pour une analyse approfondie des patterns**
- Lancer l'agent codebase-analyst via l'outil Task pour effectuer une découverte complète des patterns
- L'agent analysera : patterns d'architecture, conventions de code, approches de tests et implémentations similaires
- Utiliser les résultats de l'agent pour s'assurer que le plan suit les patterns et conventions existants

Pour des recherches rapides, vous pouvez également :
- Utiliser Grep pour trouver des fonctionnalités ou patterns spécifiques
- Identifier la structure du projet et ses conventions
- Localiser les modules et composants pertinents
- Comprendre l'architecture et les patterns de conception existants
- Trouver les points d'intégration pour les nouvelles fonctionnalités
- Vérifier les utilitaires ou helpers existants à réutiliser

## Étape 3 : Planification et conception

Sur la base de vos recherches, créer un plan détaillé qui inclut :

### 3.1 Découpage des tâches
Créer une liste priorisée des tâches d'implémentation :
- Chaque tâche doit être spécifique et actionnable
- Les tâches doivent avoir une taille appropriée
- Inclure les dépendances entre tâches
- Ordonner les tâches logiquement pour le flux d'implémentation

### 3.2 Architecture technique
Définir l'approche technique :
- Structure et organisation des composants
- Flux de données et gestion d'état
- Conception d'API (si applicable)
- Modifications du schéma de base de données (si nécessaire)
- Points d'intégration avec le code existant

### 3.3 Références d'implémentation
Documenter les ressources clés pour l'implémentation :
- Fichiers de code existants à référencer ou modifier
- Liens vers la documentation des technologies utilisées
- Exemples de code issus de la recherche
- Patterns à suivre du code existant
- Bibliothèques ou dépendances à ajouter

## Étape 4 : Créer le document de plan

Rédiger un plan complet dans `PRPs/[nom-fonctionnalite].md` avec approximativement cette structure (n représente un nombre quelconque de ces éléments) :

```markdown
# Plan d'implémentation : [Nom de la fonctionnalité]

## Vue d'ensemble
[Brève description de ce qui sera implémenté]

## Résumé des exigences
- [Exigence clé 1]
- [Exigence clé 2]
- [Exigence clé n]

## Résultats de la recherche
### Bonnes pratiques
- [Découverte 1]
- [Découverte n]

### Implémentations de référence
- [Exemple 1 avec lien/emplacement]
- [Exemple n avec lien/emplacement]

### Décisions technologiques
- [Choix technologique 1 et justification]
- [Choix technologique n et justification]

## Tâches d'implémentation

### Phase 1 : Fondations
1. **Nom de la tâche**
   - Description : [Ce qui doit être fait]
   - Fichiers à modifier/créer : [Liste des fichiers]
   - Dépendances : [Prérequis éventuels]
   - Effort estimé : [estimation de temps]

2. **Nom de la tâche**
   - Description : [Ce qui doit être fait]
   - Fichiers à modifier/créer : [Liste des fichiers]
   - Dépendances : [Prérequis éventuels]
   - Effort estimé : [estimation de temps]

### Phase 2 : Implémentation principale
[Continuer avec les tâches numérotées...]

### Phase 3 : Intégration et tests
[Continuer avec les tâches numérotées...]

## Points d'intégration dans le code
### Fichiers à modifier
- `chemin/vers/fichier1.js` - [Modifications nécessaires]
- `chemin/vers/fichiern.py` - [Modifications nécessaires]

### Nouveaux fichiers à créer
- `chemin/vers/nouveaufichier1.js` - [Objectif]
- `chemin/vers/nouveaufichiern.py` - [Objectif]

### Patterns existants à suivre
- [Pattern 1 du code existant]
- [Pattern n du code existant]

## Conception technique

### Diagramme d'architecture (si applicable)
```
[Diagramme ASCII ou description]
```

### Flux de données
[Description du flux de données à travers la fonctionnalité]

### Points d'API (si applicable)
- `POST /api/endpoint` - [Objectif]
- `GET /api/endpoint/:id` - [Objectif]

## Dépendances et bibliothèques
- [Bibliothèque 1] - [Objectif]
- [Bibliothèque n] - [Objectif]

## Stratégie de test
- Tests unitaires pour [composants]
- Tests d'intégration pour [workflows]
- Cas limites à couvrir : [liste]

## Critères de succès
- [ ] [Critère 1]
- [ ] [Critère 2]
- [ ] [Critère n]

## Notes et considérations
- [Notes importantes]
- [Défis potentiels]
- [Améliorations futures]

---
*Ce plan est prêt à être exécuté avec `/execute-plan`*
```

## Étape 5 : Validation

Avant de finaliser le plan :
1. S'assurer que toutes les exigences sont traitées
2. Vérifier que les tâches sont correctement séquencées
3. Vérifier que les points d'intégration sont identifiés
4. Confirmer que la recherche supporte l'approche
5. S'assurer que le plan est actionnable et clair

## Directives importantes

- **Être minutieux dans la recherche** : La qualité du plan dépend de la compréhension des bonnes pratiques
- **Le rendre actionnable** : Chaque tâche doit être claire et implémentable
- **Tout référencer** : Inclure les liens, chemins de fichiers et exemples
- **Tenir compte du code existant** : Suivre les patterns et conventions établis
- **Penser aux tests** : Inclure les tâches de test dans le plan
- **Dimensionner les tâches correctement** : Ni trop grandes, ni trop granulaires

## Résultat

Enregistrer le plan dans le répertoire PRPs et informer l'utilisateur :
"Plan d'implémentation créé à : PRPs/[nom-fonctionnalite].md
Vous pouvez maintenant exécuter ce plan avec : `/execute-plan PRPs/[nom-fonctionnalite].md`"