import torch
from transformers import CamembertTokenizer, CamembertModel
import numpy as np
import joblib
from pathlib import Path
import pandas as pd

# Configuration des chemins
BASE_DIR = Path(__file__).parent
CHEMIN_DONNEES = BASE_DIR / 'uvbf_data.json'
CHEMIN_SAUVEGARDE = BASE_DIR / 'bert_embeddings'
CHEMIN_SAUVEGARDE.mkdir(exist_ok=True)

def charger_donnees():
    """Charge les données depuis le fichier JSON"""
    print("Chargement des données...")
    df = pd.read_json(CHEMIN_DONNEES)
    return df['texte'].tolist(), df['sentiment'].tolist()

def generer_embeddings(textes, batch_size=8):
    """Génère les embeddings avec CamemBERT"""
    print("Chargement du modèle CamemBERT...")
    tokenizer = CamembertTokenizer.from_pretrained('camembert-base')
    model = CamembertModel.from_pretrained('camembert-base')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    
    embeddings = []
    
    print("Génération des embeddings...")
    for i in range(0, len(textes), batch_size):
        batch = textes[i:i + batch_size]
        
        # Tokenization
        inputs = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        ).to(device)
        
        # Génération des embeddings
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Utilisation du token comme représentation de la phrase
        batch_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        embeddings.extend(batch_embeddings)
        
        if (i // batch_size) % 10 == 0:
            print(f"Traitement du batch {i//batch_size + 1}/{(len(textes)//batch_size) + 1}")
    
    return np.array(embeddings)

def sauvegarder_resultats(embeddings, labels):
    """Sauvegarde les embeddings et les labels"""
    print("Sauvegarde des résultats...")
    joblib.dump(embeddings, CHEMIN_SAUVEGARDE / 'embeddings_camembert.pkl')
    joblib.dump(labels, CHEMIN_SAUVEGARDE / 'labels.pkl')
    print("Sauvegarde terminée !")

def main():
    # Charger les données
    textes, labels = charger_donnees()
    
    # Générer les embeddings
    embeddings = generer_embeddings(textes)
    
    # Sauvegarder les résultats
    sauvegarder_resultats(embeddings, labels)

if __name__ == "__main__":
    main()