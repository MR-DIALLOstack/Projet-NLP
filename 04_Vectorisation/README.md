# 🔢 Vectorisation TF-IDF - Étape 4

## Objectif

Transformer les textes prétraités en vecteurs numériques que les algorithmes de machine learning peuvent utiliser.

## Méthode : TF-IDF

**TF-IDF** = Term Frequency - Inverse Document Frequency

### Formule

```
TF-IDF(mot, document) = TF(mot, document) × IDF(mot)

où:
  TF = Fréquence du mot dans le document
  IDF = log(Nombre total de documents / Nombre de documents contenant le mot)
```

### Avantages

- Pondère l'importance des mots
- Pénalise les mots trop fréquents
- Valorise les mots discriminants
- Rapide et efficace

## Paramètres Utilisés

```python
max_features=5000   # Top 5000 mots
min_df=2            # Mot dans au moins 2 documents
max_df=0.8          # Mot dans max 80% des documents
ngram_range=(1,2)   # Unigrammes et bigrammes
```

## Utilisation

```bash
cd 04_Vectorisation
python vectorisation_tfidf.py
```

## Fichiers Générés

- `vectoriseur.pkl` : Vectoriseur réutilisable
- `matrice_tfidf.pkl` : Matrice de features
- Résultats CSV avec termes importants

## Prochaine Étape

```bash
cd ../05_Entrainement
python entrainement.py
```

