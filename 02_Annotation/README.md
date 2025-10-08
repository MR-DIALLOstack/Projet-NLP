# 📝 Annotation des Sentiments - Étape 2

## Objectif

Attribuer un label de sentiment (positif, négatif, neutre) à chaque publication collectée. Cette étape est **CRITIQUE** car la qualité de l'annotation détermine directement la performance du modèle.

## Importance de l'Annotation

L'annotation est l'étape la plus importante du projet car :
- ✅ Un modèle ne peut apprendre que ce qu'on lui montre
- ✅ Des annotations de qualité = modèle performant
- ⚠️ Des annotations aléatoires ou incohérentes = modèle inutile

## Classes de Sentiments

| Classe | Description | Exemples |
|--------|-------------|----------|
| **Positif** | Satisfaction, éloge, recommandation | "Excellente formation !", "Très satisfait", "Je recommande" |
| **Négatif** | Mécontentement, critique, problème | "Déçu...", "Problèmes techniques", "Trop cher" |
| **Neutre** | Information factuelle, question neutre | "Ouverture des inscriptions", "Comment s'inscrire ?", "L'UVBF propose..." |

## Méthodes d'Annotation

### Option 1 : Annotation Manuelle (RECOMMANDÉE)

**Avantages** :
- ✅ Qualité maximale
- ✅ Compréhension du contexte
- ✅ Détection des nuances

**Utilisation** :
```bash
python annotation_manuelle.py --mode manuel --nombre 100
```

**Interface** :
```
[1/296] --------------------------------------------------
Texte : Malgré la charge de travail, je me sens motivé à l'UVBF.
--------------------------------------------------
Sentiment [p/n/e/s/q] : p
✓ Annoté comme POSITIF
```

**Commandes** :
- `p` → Positif
- `n` → Négatif
- `e` → nEutre
- `s` → Sauter
- `q` → Quitter et sauvegarder

### Option 2 : Annotation Semi-Automatique (DÉMONSTRATION)

**⚠️ Attention** : Utilisez uniquement pour tester le pipeline rapidement.

**Utilisation** :
```bash
python annotation_manuelle.py --mode auto --nombre 300
```

**Fonctionnement** : Basé sur des mots-clés simples (précision limitée).

## Conseils pour une Annotation de Qualité

### 1. Cohérence

- Définissez vos critères au début et ne changez pas en cours
- Si hésitation, choisissez "neutre"
- Gardez en tête qu'un texte court peut être ambigu

### 2. Contexte

- Lisez le texte complet
- Considérez le ton général, pas juste un mot
- L'ironie/sarcasme peut inverser le sentiment

### 3. Exemples Concrets

**Positif** :
- "Excellente formation à l'UVBF ! 👍"
- "Les cours sont de qualité"
- "Je recommande vivement"

**Négatif** :
- "Problèmes techniques constants..."
- "Déçu par le support"
- "Trop cher pour ce que c'est"

**Neutre** :
- "L'UVBF ouvre les inscriptions"
- "Comment s'inscrire à l'UVBF ?"
- "L'UVBF propose des formations en ligne"

### 4. Cas Difficiles

| Texte | Sentiment | Raison |
|-------|-----------|--------|
| "Pas mal mais peut mieux faire" | Neutre | Mitigé, pas clairement positif/négatif |
| "Enfin une solution accessible !" | Positif | Ton enthousiaste malgré "enfin" |
| "C'est une université en ligne" | Neutre | Purement factuel |
| "Dommage que ce soit si cher..." | Négatif | Regret exprimé |

## Statistiques et Qualité

### Vérifier vos Annotations

```bash
python annotation_manuelle.py --mode stats
```

Affiche :
- Nombre total annoté
- Répartition par sentiment
- % de chaque classe

### Distribution Idéale

Pour un bon entraînement :
- ✅ Au moins 100 exemples par classe
- ✅ Distribution relativement équilibrée
- ⚠️ Éviter < 10% pour une classe

**Exemple de bonne distribution** :
- Positif : 25-35%
- Neutre : 40-60%
- Négatif : 15-25%

## Résolution de Problèmes

### Problème : "Fichier source non trouvé"

**Solution** : Assurez-vous d'avoir les données dans :
```
01_Collecte_Donnees/uvbf_data.json
```

### Problème : "Annotations perdues après arrêt"

**Solution** : Le script sauvegarde automatiquement tous les 20 éléments.
Fichier de sauvegarde : `uvbf_data_annote.json`

### Problème : "Hésitation sur le sentiment"

**Solution** :
1. Relisez le texte complet
2. Identifiez le ton général
3. Si toujours hésitant → Neutre
4. Utilisez 's' pour sauter et revenir plus tard

## Fichiers Générés

- `uvbf_data_annote.json` : Données avec labels de sentiment
- Format : Même structure que les données d'origine + champ `sentiment`

```json
{
  "id": "UVBF_0001",
  "texte": "...",
  "sentiment": "positif",
  "date_annotation": "2025-10-08T14:30:00"
}
```

## Prochaine Étape

Une fois l'annotation terminée (au moins 100 publications annotées) :

```bash
cd ../03_Pretraitement
python pretraitement.py
```

## Ressources

- Script : `annotation_manuelle.py`
- Résultats : `uvbf_data_annote.json`
- Documentation générale : `../Documentation/GUIDE_UTILISATION.md`

---

**💡 Conseil** : Prenez votre temps ! 30 minutes d'annotation de qualité valent mieux que 2 heures d'annotation bâclée.

