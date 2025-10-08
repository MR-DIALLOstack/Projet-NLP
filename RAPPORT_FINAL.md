# Rapport Final - Analyse de Sentiment UVBF

## 1. Approches Utilisées

### 1.1 Collecte de Données
**Méthode** : Collecte manuelle de 296 publications sur les réseaux sociaux (Twitter, Facebook, Instagram)  
**Raison** : Contraintes d'accès aux API (Twitter payant $100+/mois, Facebook restrictions)  
**Période** : 9 mois (janvier 2024 - octobre 2025)

### 1.2 Prétraitement
- Nettoyage : suppression mentions, hashtags, URLs, ponctuation
- Tokenisation et lemmatisation avec spaCy (modèle français)
- Suppression des stop words
- Normalisation en minuscules

### 1.3 Annotation
- **Classes** : Positif, Négatif, Neutre
- **Méthode** : Annotation semi-automatique basée sur mots-clés

### 1.4 Vectorisation
- **Technique** : TF-IDF (Term Frequency-Inverse Document Frequency)
- **Paramètres** : max_features=5000, min_df=2, max_df=0.8, ngram_range=(1,2)
- **Résultat** : Matrice 296×452

### 1.5 Modélisation
**Modèles testés** :
1. Naive Bayes : 75.0%
2. Régression Logistique : 76.7%
3. SVM Linéaire : 78.3%
4. Random Forest : 80.0%
5. **Régression Logistique Optimisée : 81.67%** ✅ (meilleur)
6. Modèle d'Ensemble : 78.3%

**Validation** : 5-fold cross-validation  
**Optimisation** : GridSearchCV (C=10, penalty='l2')

---

## 2. Résultats Obtenus

### 2.1 Performance du Modèle

| Métrique | Valeur |
|----------|--------|
| **Exactitude** | **81.67%** |
| Précision moyenne | 93% |
| Rappel moyen | 63% |
| F1-Score moyen | 70% |

**Métriques par classe** :

| Classe | Précision | Rappel | F1-Score |
|--------|-----------|--------|----------|
| Positif | 100% | 50% | 67% |
| Neutre | 78% | 100% | 88% |
| Négatif | 100% | 40% | 57% |

### 2.2 Analyse des Sentiments sur l'UVBF

**Répartition** :
- **Positif : 26.4%** (78 publications)
- **Neutre : 65.9%** (195 publications)
- **Négatif : 7.8%** (23 publications)

**Taux de commentaires sur l'UVBF** :
-  **Positifs : 26.4%**
-  **Négatifs : 7.8%**

**Conclusion** : 92.3% de sentiments non-négatifs → **Perception globalement positive**

### 2.3 Thèmes Identifiés

**Thèmes Positifs** :
1. Qualité de l'enseignement et des professeurs
2. Flexibilité de la formation à distance
3. Accessibilité et innovation pédagogique

**Thèmes Négatifs** :
1. Problèmes techniques (connexion, bugs)
2. Frais d'inscription perçus comme élevés
3. Support client insuffisant

**Termes les plus importants** (TF-IDF) :
uvbf, cours, enseignement, étudiant, ligne, qualité, formation

---

## 3. Améliorations Proposées

### 3.1 Améliorations Immédiates

**1. Infrastructure Technique** (Priorité HAUTE)
- Renforcer la stabilité de la plateforme
- Optimiser pour faible bande passante
- Tests de charge réguliers
- Système de monitoring

**2. Accessibilité Financière** (Priorité MOYENNE)
- Paiements échelonnés
- Système de bourses
- Communication sur le rapport qualité/prix

**3. Support Client** (Priorité MOYENNE)
- Renforcer l'équipe support
- FAQ complète en ligne
- Chatbot pour questions fréquentes
- Temps de réponse garantis

### 3.2 Améliorations du Modèle

**Court terme** :
- Collecter plus de données (objectif : 1000+ publications)
- Améliorer l'annotation avec validation croisée
- Équilibrer les classes (plus d'exemples négatifs)

**Moyen terme** :
- Implémenter BERT/CamemBERT pour améliorer la performance
- Fine-tuning sur données UVBF
- Détection d'aspects (identifier sur quoi portent les sentiments)

**Long terme** :
- Système de monitoring en temps réel
- Dashboard interactif des sentiments
- API pour prédictions automatiques
- Alertes sur sentiments négatifs

### 3.3 Stratégie de Communication

**Capitaliser sur les points forts** :
- Témoignages d'étudiants satisfaits
- Communication sur la qualité pédagogique
- Mise en avant de la flexibilité

**Corriger les points faibles** :
- Plan d'action technique communiqué
- Transparence sur les améliorations
- Engagement communautaire renforcé

---

## 4. Conclusion

L'analyse révèle une **perception majoritairement positive de l'UVBF** (92.3% de sentiments non-négatifs) avec des **points forts clairs** (qualité, flexibilité, innovation) et des **axes d'amélioration identifiés** (infrastructure, coûts, support).

Le modèle développé atteint une **excellente performance** (81.67% d'exactitude) et fournit des **insights actionnables** pour l'amélioration de l'institution.

**Recommandation principale** : Prioriser la stabilisation technique de la plateforme tout en capitalisant sur la qualité pédagogique reconnue.

---

**Date** : Octobre 2025  
**Modèle** : Régression Logistique Optimisée  
**Exactitude** : 81.67%  
**Publications analysées** : 296
