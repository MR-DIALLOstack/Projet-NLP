# 🧹 Prétraitement des Textes - Étape 3

## Objectif

Nettoyer et normaliser les textes des publications annotées pour les préparer à la vectorisation. Le prétraitement est essentiel pour améliorer la qualité des features extraites.

## Transformations Appliquées

### 1. Nettoyage Basique
- ❌ Suppression des mentions (@utilisateur)
- ❌ Suppression des hashtags (#mot)
- ❌ Suppression des URLs (http://, www.)
- ❌ Suppression de la ponctuation
- ✅ Normalisation des espaces

### 2. Normalisation
- Conversion en minuscules
- Suppression des caractères spéciaux

### 3. Tokenisation
- Découpage en mots (tokens)
- Utilisation de spaCy pour le français

### 4. Lemmatisation
- Réduction à la forme canonique
- "cours" ← "cours", "courais", "courir"

### 5. Filtrage
- Suppression des stop words (le, la, de, un, etc.)
- Suppression des mots courts (< 3 caractères)
- Suppression des chiffres isolés

## Utilisation

```bash
cd 03_Pretraitement
python pretraitement.py
```

## Exemple de Transformation

**Texte original** :
```
"Les cours en ligne de l'UVBF sont vraiment de très bonne qualité ! 😊 #Formation"
```

**Après prétraitement** :
```
"cours ligne uvbf vraiment bonne qualité"
```

## Fichiers

- **Entrée** : `../02_Annotation/uvbf_data_annote.json`
- **Sortie** : `uvbf_data_pretraite.json`
- **Script** : `pretraitement.py`

## Prochaine Étape

```bash
cd ../04_Vectorisation
python vectorisation_tfidf.py
```

