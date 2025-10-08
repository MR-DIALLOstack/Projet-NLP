# 📦 Guide d'Installation - Projet Analyse de Sentiment UVBF

## Prérequis Système

### Configuration Minimale

- **Système d'exploitation** : Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+
- **Python** : Version 3.8 ou supérieure
- **RAM** : 4 Go minimum (8 Go recommandé)
- **Espace disque** : 2 Go d'espace libre
- **Connexion Internet** : Pour télécharger les dépendances

### Vérification de Python

Ouvrez un terminal et vérifiez votre version de Python :

```bash
python --version
# ou
python3 --version
```

Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/).

## Installation Pas à Pas

### Étape 1 : Télécharger le Projet

```bash
# Si vous avez git
git clone [URL_DU_PROJET]
cd Projet-NLP

# Ou téléchargez et décompressez l'archive ZIP
```

### Étape 2 : Créer un Environnement Virtuel

**Pourquoi ?** Un environnement virtuel isole les dépendances du projet.

#### Sur Windows :

```bash
# Créer l'environnement
python -m venv virtuel

# Activer l'environnement
virtuel\Scripts\activate

# Vous devriez voir (virtuel) au début de votre invite de commande
```

#### Sur Linux/macOS :

```bash
# Créer l'environnement
python3 -m venv virtuel

# Activer l'environnement
source virtuel/bin/activate

# Vous devriez voir (virtuel) au début de votre terminal
```

### Étape 3 : Installer les Dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer toutes les dépendances
pip install -r requirements.txt
```

Cette commande installera :
- numpy (calculs numériques)
- pandas (manipulation de données)
- scikit-learn (machine learning)
- spacy (NLP)
- matplotlib, seaborn (visualisations)
- tqdm (barres de progression)
- joblib (sauvegarde de modèles)

**Temps estimé** : 5-10 minutes selon votre connexion.

### Étape 4 : Télécharger le Modèle spaCy

spaCy nécessite un modèle de langue française :

```bash
python -m spacy download fr_core_news_sm
```

**Note** : Ce téléchargement fait environ 16 Mo.

### Étape 5 : Vérifier l'Installation

Testez que tout fonctionne :

```bash
# Vérifier spaCy
python -c "import spacy; nlp = spacy.load('fr_core_news_sm'); print('✓ spaCy OK')"

# Vérifier scikit-learn
python -c "import sklearn; print('✓ scikit-learn OK')"

# Vérifier pandas
python -c "import pandas; print('✓ pandas OK')"
```

Si toutes les commandes affichent "✓ OK", l'installation est réussie !

## Dépendances Optionnelles

### Pour l'Amélioration avec BERT (Optionnel)

**⚠️ Attention** : Nécessite beaucoup plus d'espace disque (~4 Go) et un GPU est recommandé.

```bash
pip install transformers torch
```

### Pour la Génération de PDF (Optionnel)

```bash
pip install fpdf
```

## Résolution des Problèmes Courants

### Problème : "command not found: python"

**Solution** : Essayez `python3` au lieu de `python`.

### Problème : "Permission denied"

**Solution Linux/macOS** :
```bash
sudo pip install -r requirements.txt
```

**Solution Windows** : Exécutez PowerShell en tant qu'administrateur.

### Problème : "spacy.cli.download not found"

**Solution** :
```bash
pip install -U spacy
python -m spacy download fr_core_news_sm
```

### Problème : Installation très lente

**Solution** : Utilisez un miroir pip plus rapide :
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Problème : Erreur avec numpy/scipy

**Solution** : Installez d'abord les dépendances scientifiques :
```bash
pip install numpy scipy
pip install -r requirements.txt
```

## Désactivation de l'Environnement

Quand vous avez fini de travailler :

```bash
deactivate
```

## Réactivation pour une Prochaine Session

```bash
# Windows
virtuel\Scripts\activate

# Linux/macOS
source virtuel/bin/activate
```

## Vérification de l'Installation Complète

Script de test complet :

```bash
python Documentation/test_installation.py
```

Vous devriez voir :

```
✓ Python version OK (3.8+)
✓ numpy installé
✓ pandas installé
✓ scikit-learn installé
✓ spacy installé
✓ Modèle français spaCy chargé
✓ matplotlib installé
✓ seaborn installé

✅ Installation complète et fonctionnelle !
```

## Prochaines Étapes

Une fois l'installation terminée, consultez :

- **GUIDE_UTILISATION.md** : Guide complet d'utilisation
- **README_PROJET.md** : Vue d'ensemble du projet
- **01_Collecte_Donnees/README.md** : Commencer par la collecte de données

## Support

En cas de problème persistant :

1. Vérifiez que vous utilisez Python 3.8+
2. Essayez de recréer l'environnement virtuel
3. Consultez la FAQ dans `Documentation/FAQ.md`
4. Vérifiez les logs d'erreur complets

---

**Installation réussie ? Passez au guide d'utilisation !**

