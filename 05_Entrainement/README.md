# Entraînement des Modèles - Étape 5

## Objectif

Entraîner et comparer plusieurs modèles de classification pour sélectionner le meilleur.

## Modèles Testés

1. **Naive Bayes** - Rapide, bon pour le texte
2. **Régression Logistique** - Équilibré, interprétable
3. **SVM Linéaire** - Performant sur haute dimension
4. **Random Forest** - Robuste, gère les interactions
5. **Modèle d'Ensemble** - Combinaison de plusieurs modèles

## Méthodologie

- **Division** : 80% train, 20% test
- **Validation croisée** : 5-fold
- **Optimisation** : GridSearchCV
- **Sélection** : Meilleur score de test

## Résultats Attendus

- **Exactitude** : > 70%
- **Meilleur modèle** : Automatiquement sauvegardé

## Utilisation

```bash
cd 05_Entrainement
python entrainement.py
```

## Fichiers Générés

- `modele_sentiment.pkl` : Meilleur modèle
- `encodeur_labels.pkl` : Encodeur
- `resultats/comparaison_modeles.csv` : Comparaison
- `resultats/comparaison_modeles.png` : Graphique

## Prochaine Étape

```bash
cd ../06_Evaluation
python evaluation.py
```

