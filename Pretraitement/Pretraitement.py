import json
import re
import spacy
from tqdm import tqdm

# Charger le modèle français de spaCy
nlp = spacy.load('fr_core_news_sm')

def nettoyer_texte(texte):
    if not isinstance(texte, str):
        return ""
    
    # Suppression des mentions @utilisateur
    texte = re.sub(r'@\w+', '', texte)
    # Suppression des hashtags
    texte = re.sub(r'#\w+', '', texte)
    # Suppression des URLs
    texte = re.sub(r'https?://\S+|www\.\S+', '', texte)
    # Suppression des caractères spéciaux et de la ponctuation
    texte = re.sub(r'[^\w\s]', ' ', texte)
    # Suppression des espaces multiples
    texte = ' '.join(texte.split())
    return texte.lower()

def pretraitement_texte(texte):
    if not isinstance(texte, str) or not texte.strip():
        return []
    
    doc = nlp(texte)
    # Lemmatisation et suppression des stop words
    tokens = [token.lemma_ for token in doc 
              if not token.is_stop and not token.is_punct 
              and not token.is_space and not token.is_digit
              and len(token.text) > 2]  # Suppression des mots trop courts
    
    return tokens

def main():
    # Charger les données
    with open('uvbf_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Prétraitement des données
    for item in tqdm(data, desc="Traitement des données"):
        if 'texte' in item:
            texte_propre = nettoyer_texte(item['texte'])
            tokens = pretraitement_texte(texte_propre)
            item['texte_traite'] = ' '.join(tokens)
    
    # Sauvegarder les données prétraitées
    with open('uvbf_data_pretraitement.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Prétraitement terminé. Les données ont été sauvegardées dans 'uvbf_data_preprocesse.json'")

if __name__ == "__main__":
    main()
