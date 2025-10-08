# 📊 Collecte des Données - UVBF

## Contexte

Pour ce projet d'analyse de sentiment, nous avions initialement prévu d'utiliser les API des différentes plateformes de réseaux sociaux (Twitter/X, Facebook, Instagram, TikTok). Cependant, nous avons rencontré plusieurs obstacles :

### Problèmes Rencontrés avec les API

#### 1. Twitter/X
- **Accès restreint** : L'API Twitter nécessite désormais un compte développeur payant (Twitter API v2)
- **Coûts élevés** : Les tarifs commencent à $100/mois pour l'accès basique
- **Limitations strictes** : Même avec un compte gratuit, les quotas sont très limités
- **Délais d'approbation** : Processus d'approbation peut prendre plusieurs jours

#### 2. Facebook/Instagram (Meta)
- **Restrictions d'accès** : L'API Graph nécessite une approbation de l'application
- **Données publiques limitées** : Accès restreint aux données des pages publiques uniquement
- **Processus complexe** : Configuration OAuth et permissions multiples requises
- **Politique de confidentialité** : Restrictions strictes sur la collecte de données

#### 3. TikTok
- **API non publique** : Pas d'API publique facilement accessible
- **Programme développeur fermé** : Accès limité aux partenaires officiels

## Solution Adoptée : Collecte Manuelle

Face à ces contraintes, nous avons opté pour une **collecte manuelle des données** en respectant les conditions d'utilisation des plateformes.

### Méthodologie de Collecte Manuelle

1. **Recherche de publications** : Utilisation des fonctions de recherche natives de chaque plateforme
   - Mots-clés : "UVBF", "Université UVBF", "Université Virtuelle du Burkina Faso"
   - Hashtags : #UVBF, #UniversitéVirtuelle, #BurkinaFaso

2. **Extraction des informations** : Pour chaque publication pertinente
   - Texte de la publication
   - Auteur (anonymisé si nécessaire)
   - Plateforme source
   - Date de publication
   - Métriques d'engagement (likes, partages, commentaires)

3. **Structuration des données** : Compilation dans un format JSON standardisé
   ```json
   {
     "id": "UVBF_0001",
     "auteur": "Nom Anonymisé",
     "plateforme": "Twitter",
     "texte": "Contenu de la publication",
     "date_publication": "2025-01-15 10:30:00",
     "hashtags": ["#UVBF"],
     "likes": 45,
     "retweets_partages": 12,
     "commentaires": 8
   }
   ```

### Données Collectées

- **Nombre total** : 296 publications
- **Période** : Janvier 2024 - Octobre 2025 (environ 9 mois)
- **Sources** :
  - Twitter/X : ~40%
  - Facebook : ~40%
  - Instagram : ~15%
  - Autres : ~5%

### Respect de l'Éthique et de la Vie Privée

✅ **Données publiques uniquement** : Seules les publications publiques ont été collectées  
✅ **Anonymisation** : Les noms d'auteurs ont été anonymisés dans les analyses  
✅ **Usage académique** : Les données sont utilisées uniquement à des fins de recherche académique  
✅ **Pas de revente** : Aucune commercialisation des données collectées  
✅ **Suppression possible** : Les données peuvent être supprimées à la demande  

## Structure du Fichier de Données

Le fichier `uvbf_data.json` contient les données collectées avec la structure suivante :

```json
[
  {
    "id": "UVBF_0217",
    "auteur": "Utilisateur anonymisé",
    "plateforme": "Twitter",
    "texte": "Malgré la charge de travail, je me sens motivé à l'UVBF.",
    "date_publication": "2025-09-01 06:22:00",
    "hashtags": ["#UVBF", "#BurkinaFaso"],
    "likes": 60,
    "retweets_partages": 45,
    "commentaires": 18
  }
]
```

## Alternative : Script de Scraping (Pour Référence)

Pour référence, nous avons développé un script `scraper_demo.py` qui montre comment le scraping automatisé aurait pu fonctionner avec un accès API complet. Ce script :

- Génère des données de démonstration pour tester le pipeline
- Montre la structure du code pour une future intégration API
- Peut être adapté si les accès API deviennent disponibles

**⚠️ Note** : Ce script est fourni à titre éducatif. Pour un usage en production, assurez-vous d'avoir :
- Les autorisations API appropriées
- Un compte développeur approuvé
- Le respect des quotas et limites de taux
- La conformité avec les CGU de chaque plateforme

## Fichiers dans ce Dossier

- `uvbf_data.json` : Données collectées manuellement (296 publications)
- `scraper_demo.py` : Script de démonstration (génération de données fictives)
- `README.md` : Ce fichier de documentation

## Prochaines Étapes

Une fois les données collectées, passez à l'étape suivante :
```bash
# Étape 2 : Annotation des sentiments
cd ../02_Annotation
python annotation_manuelle.py --mode manuel
```

