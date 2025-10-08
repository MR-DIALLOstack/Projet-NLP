# Évaluation du Modèle - Étape 6

## Objectif

Évaluer les performances du meilleur modèle sur l'ensemble de test avec des métriques détaillées.

## Métriques Calculées

### Globales
- **Exactitude (Accuracy)** : % de prédictions correctes
- **Macro Average** : Moyenne des métriques par classe
- **Weighted Average** : Moyenne pondérée par classe

### Par Classe (Positif, Négatif, Neutre)
- **Précision** : VP / (VP + FP)
- **Rappel** : VP / (VP + FN)
- **F1-Score** : 2 × (Précision × Rappel) / (Précision + Rappel)

## Visualisations

- **Matrice de confusion** : Erreurs de classification
- **Graphiques** : Performance par classe

## Utilisation

```bash
cd 06_Evaluation
python evaluation.py
```

## Fichiers Générés

- `resultats_evaluation/matrice_confusion.png` : Visualisation
- `resultats_evaluation/rapport_metriques.csv` : Métriques détaillées

## Interprétation

**Exactitude > 80%** : Excellent   
**Exactitude 70-80%** : Bon ✓  
**Exactitude < 70%** : À améliorer 

## Prochaine Étape

```bash
cd ../07_Rapport_Final
python generer_rapport.py
```

