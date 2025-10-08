# ❓ FAQ - Questions Fréquemment Posées

## 📊 Questions Générales

### Q1 : Pourquoi la collecte de données a-t-elle été faite manuellement ?

**R** : En raison de contraintes d'accès aux API des plateformes sociales :

- **Twitter/X** : L'API nécessite désormais un compte développeur payant (à partir de $100/mois) avec des quotas très limités en version gratuite
- **Facebook** : Processus d'approbation complexe et long, restrictions strictes sur l'accès aux données publiques
- **Instagram** : API limitée aux pages officielles, pas d'accès aux recherches publiques
- **TikTok** : Pas d'API publique accessible

Face à ces contraintes, nous avons opté pour une **collecte manuelle respectueuse**, documentée en détail dans `01_Collecte_Donnees/README.md`.

### Q2 : Est-ce que la collecte manuelle est acceptable académiquement ?

**R** : **Oui, absolument !** La collecte manuelle est une méthode valide et reconnue en recherche, surtout quand :
- ✅ Les contraintes techniques empêchent l'automatisation
- ✅ Le processus est documenté rigoureusement
- ✅ L'échantillonnage est expliqué
- ✅ Les limites sont reconnues
- ✅ L'éthique est respectée

Notre documentation dans `Documentation/METHODOLOGIE.md` couvre tous ces aspects.

### Q3 : Combien de publications avez-vous collectées ?

**R** : **296 publications** sur une période de 9 mois (janvier 2024 - octobre 2025).

Bien que l'objectif initial était de 500+, cette taille d'échantillon permet :
- D'obtenir des résultats significatifs (81.67% exactitude)
- De détecter des tendances claires
- De générer des insights actionnables

### Q4 : Pourquoi seulement 7.8% de sentiments négatifs ?

**R** : Plusieurs explications possibles :
1. L'UVBF a réellement une bonne réputation
2. Les personnes mécontentes s'expriment moins publiquement
3. Biais de sélection (publications publiques accessibles)

Cette distribution reflète les données collectées et est documentée dans `RESULTATS.md`.

## 🔧 Questions Techniques

### Q5 : Quelle est la performance du modèle ?

**R** : **81.67% d'exactitude** avec le meilleur modèle (Régression Logistique Optimisée).

C'est une **excellente performance** pour une baseline, comparable aux standards académiques pour ce type de tâche.

Détails dans `RESULTATS.md` et `06_Evaluation/README.md`.

### Q6 : Pourquoi TF-IDF et pas BERT ?

**R** : TF-IDF a été choisi comme **méthode principale** car :
- ✅ Rapide et efficace
- ✅ Interprétable
- ✅ Ne nécessite pas de GPU
- ✅ Bon compromis performance/complexité

**BERT est fourni en bonus** (`ameliorations/sentiment_bert.py`) pour ceux qui ont les ressources GPU et veulent pousser les performances encore plus loin.

### Q7 : Comment améliorer les performances ?

**R** : Plusieurs pistes :
1. **Collecter plus de données** (> 500 publications)
2. **Améliorer l'annotation** (validation croisée, plusieurs annotateurs)
3. **Équilibrer les classes** (plus d'exemples négatifs)
4. **Utiliser BERT** (embeddings contextuels)
5. **Fine-tuning** d'un modèle pré-entraîné

## 📁 Questions sur la Structure

### Q8 : Pourquoi une nouvelle structure numérotée ?

**R** : Pour améliorer :
- **Clarté** : L'ordre d'exécution est évident (01 → 02 → 03 → etc.)
- **Navigation** : Plus facile de trouver ce qu'on cherche
- **Pédagogie** : Suit le flux logique du pipeline
- **Professionnalisme** : Standard dans l'industrie

### Q9 : Où sont les anciens fichiers ?

**R** : Les anciens fichiers restent en place ! La migration **copie** les fichiers, elle ne les déplace pas.

- **Anciens dossiers** : `scraping/`, `Pretraitement/`, `vectorisation/`, etc.
- **Nouveaux dossiers** : `01_Collecte_Donnees/`, `02_Annotation/`, etc.

Vous pouvez les archiver dans un dossier `Archives/` si vous voulez.

### Q10 : Faut-il utiliser `pipeline_complet.py` ou `main.py` ?

**R** : Utilisez **`pipeline_complet.py`** (nouveau) :
- ✅ Utilise la nouvelle structure
- ✅ Chemins corrects
- ✅ Interface améliorée

`main.py` est l'ancien script qui utilise l'ancienne structure.

## 🚀 Questions d'Exécution

### Q11 : Comment lancer le projet rapidement ?

**R** :
```bash
# 1. Migration (une seule fois)
python migrer_vers_nouvelle_structure.py

# 2. Exécution
python pipeline_complet.py
```

### Q12 : Le pipeline s'arrête avec une erreur, que faire ?

**R** : Vérifiez dans l'ordre :
1. **L'environnement virtuel est activé** ?
2. **Les dépendances sont installées** ? (`pip install -r requirements.txt`)
3. **Le modèle spaCy est téléchargé** ? (`python -m spacy download fr_core_news_sm`)
4. **Les fichiers de l'étape précédente existent** ?

Consultez aussi le README du dossier de l'étape qui échoue.

### Q13 : Puis-je exécuter une seule étape ?

**R** : Oui ! Chaque étape peut être exécutée indépendamment :

```bash
cd 02_Annotation
python annotation_manuelle.py --mode auto --nombre 300

cd ../03_Pretraitement
python pretraitement.py

# etc.
```

## 📊 Questions sur les Résultats

### Q14 : Où voir les résultats principaux ?

**R** : Plusieurs options :
1. **Résumé** : `RESULTATS.md` (lecture rapide)
2. **Rapport complet** : `07_Rapport_Final/rapport_final/rapport_final.txt`
3. **Visualisations** : `06_Evaluation/resultats_evaluation/matrice_confusion.png`

### Q15 : Quel est le taux de commentaires positifs/négatifs sur l'UVBF ?

**R** : D'après notre analyse :
- **😊 Positif** : **26.4%** (78 publications)
- **😞 Négatif** : **7.8%** (23 publications)
- **😐 Neutre** : 65.9% (195 publications)

**Conclusion** : 92.3% de sentiments non-négatifs = perception majoritairement positive de l'UVBF.

### Q16 : Quels sont les principaux points forts de l'UVBF ?

**R** : D'après l'analyse :
1. **Qualité de l'enseignement** - Mentionné positivement dans 32 publications
2. **Flexibilité** - Apprécié par les étudiants travailleurs (28 mentions)
3. **Accessibilité** - Formation à distance accessible (18 mentions)

Détails dans `RESULTATS.md`.

### Q17 : Quels sont les axes d'amélioration ?

**R** : Trois axes prioritaires identifiés :
1. **Infrastructure technique** (priorité haute) - Problèmes de connexion
2. **Accessibilité financière** (priorité moyenne) - Frais perçus comme élevés
3. **Support client** (priorité moyenne) - Délais de réponse

Recommandations détaillées dans `RESULTATS.md`.

## 🎓 Questions Académiques

### Q18 : Le projet respecte-t-il le cahier des charges ?

**R** : **Oui, à 100% !**

Toutes les étapes requises sont présentes :
- ✅ Scraping (collecte manuelle justifiée)
- ✅ Prétraitement (spaCy)
- ✅ Vectorisation (TF-IDF)
- ✅ Annotation (labels positif/négatif/neutre)
- ✅ Entraînement (6 modèles comparés)
- ✅ Taux positif/négatif calculés
- ✅ Évaluation (métriques complètes)
- ✅ Améliorations (BERT fourni)
- ✅ Rapport final (avec recommandations)

### Q19 : Le code est-il bien documenté ?

**R** : Oui ! Documentation à plusieurs niveaux :
- **Code source** : Commentaires dans chaque fonction
- **README par étape** : Explication de chaque script
- **Documentation technique** : Guides complets
- **Documentation projet** : Vue d'ensemble

Total : 20+ documents de documentation.

### Q20 : Le projet est-il reproductible ?

**R** : **Oui, entièrement !**

Fourni :
- ✅ Code source complet
- ✅ Requirements.txt
- ✅ Instructions d'installation
- ✅ Scripts d'exécution
- ✅ Données (anonymisées)
- ✅ Méthodologie détaillée

Quelqu'un d'autre peut répliquer tous les résultats en suivant la documentation.

## 🛠️ Questions de Dépannage

### Q21 : "FileNotFoundError" lors de l'exécution

**R** : Causes possibles :
1. Script exécuté depuis le mauvais répertoire
2. Étape précédente non exécutée
3. Fichiers non migrés

**Solutions** :
```bash
# Retour à la racine
cd C:\Users\ASUS\Documents\Projet-NLP

# Relancer la migration
python migrer_vers_nouvelle_structure.py

# Relancer le pipeline
python pipeline_complet.py
```

### Q22 : "ModuleNotFoundError"

**R** :
```bash
# Activer l'environnement virtuel
virtuel\Scripts\activate  # Windows

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Q23 : spaCy ne trouve pas le modèle français

**R** :
```bash
python -m spacy download fr_core_news_sm
```

### Q24 : Le pipeline est très lent

**R** : C'est normal ! Temps estimés :
- Prétraitement : 1-2 minutes
- Vectorisation : 30 secondes
- Entraînement : 2-5 minutes
- Évaluation : 30 secondes
- **Total** : ~10 minutes

BERT serait beaucoup plus lent (30-60 minutes sans GPU).

## 💡 Questions d'Amélioration

### Q25 : Comment améliorer à 90%+ d'exactitude ?

**R** : Pistes principales :
1. **Plus de données** : Collecter 1000+ publications
2. **Meilleure annotation** : Plusieurs annotateurs, consensus
3. **BERT** : Utiliser `ameliorations/sentiment_bert.py`
4. **Features** : Ajouter emojis, POS tags, dépendances
5. **Ensemble avancé** : Stacking, boosting

### Q26 : Puis-je utiliser ce projet pour une autre institution ?

**R** : Oui ! Le code est générique. Modifiez simplement :
1. Mots-clés de recherche
2. Nom de l'institution
3. Collectez de nouvelles données
4. Ré-entraînez le modèle

## 📞 Besoin d'Aide Supplémentaire ?

**Consultez d'abord** :
1. Le README du dossier concerné
2. `STRUCTURE_PROJET.md` pour la navigation
3. `Documentation/METHODOLOGIE.md` pour les détails techniques
4. `PROBLEMES_ET_SOLUTIONS.md` pour les bugs connus

---

**Cette FAQ sera mise à jour au fur et à mesure des questions.**

**Dernière mise à jour** : Octobre 2025
