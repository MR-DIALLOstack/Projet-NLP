import pandas as pd
import re
import spacy
from collections import Counter

# Charger le modèle français de spaCy
nlp = spacy.load("fr_core_news_sm")

# Charger les données
df = pd.read_json('uvbf_data.json')

def nettoyer_texte(texte):
    """
    Nettoie un texte en supprimant les éléments non pertinents
    """
    if pd.isna(texte) or texte is None:
        return ""
    
    # Convertir en minuscules
    texte = texte.lower()
    
    # Supprimer les URLs
    texte = re.sub(r'http\S+|www\S+', '', texte)
    
    # Supprimer les mentions (@)
    texte = re.sub(r'@\w+', '', texte)
    
    # Supprimer les hashtags (#)
    texte = re.sub(r'#\w+', '', texte)
    
    # Supprimer les emojis
    texte = re.sub(r'[^\w\s\']', ' ', texte)
    
    # Supprimer les espaces multiples
    texte = re.sub(r'\s+', ' ', texte).strip()
    
    return texte

def lemmatiser_texte(texte):
    """
    Tokenise, supprime les stop words et lemmatise le texte
    """
    if not texte:
        return ""
    
    # Traiter avec spaCy
    doc = nlp(texte)
    
    # Lemmatisation + suppression des stop words et ponctuation
    tokens = [token.lemma_ for token in doc 
              if not token.is_stop and not token.is_punct and len(token.text) > 2]
    
    return ' '.join(tokens)

def pretraiter_donnees(df, colonne_texte):
    """
    Prétraite une colonne de texte du dataframe
    """
    # Nettoyer
    df[f'{colonne_texte}_nettoye'] = df[colonne_texte].apply(nettoyer_texte)
    
    # Lemmatiser
    df[f'{colonne_texte}_lemmatise'] = df[f'{colonne_texte}_nettoye'].apply(lemmatiser_texte)
    
    return df

# Application du prétraitement
colonnes_a_traiter = [
    "Qu'est-ce que vous appréciez le plus à l'UV-BF ?",
    "Quelles sont les principales difficultés ou aspects négatifs que vous rencontrez à l'UV-BF ?"
]

for colonne in colonnes_a_traiter:
    if colonne in df.columns:
        df = pretraiter_donnees(df, colonne)
        print(f"✓ Colonne '{colonne}' prétraitée")

# Sauvegarder les résultats
df.to_json('uvbf_data_pretraite.json')
print("\n✓ Données prétraitées sauvegardées dans 'uvbf_data_pretraite.json'")

# Afficher un exemple
print("\n=== EXEMPLE DE PRÉTRAITEMENT ===")
exemple = df.iloc[0]
print(f"Texte original: {exemple[colonnes_a_traiter[0]][:100]}...")
print(f"Texte nettoyé: {exemple[colonnes_a_traiter[0] + '_nettoye'][:100]}...")
print(f"Texte lemmatisé: {exemple[colonnes_a_traiter[0] + '_lemmatise'][:100]}...")