import joblib
import pandas as pd
import numpy as np  # Ajoutez cette ligne
from sklearn.model_selection import train_test_split
from pathlib import Path

# Configuration des chemins
BASE_DIR = Path(__file__).parent
CHEMIN_MATRICE = BASE_DIR / 'uvbf_tfidf_matrice_tfidf.pkl'
CHEMIN_DONNEES = BASE_DIR / 'uvbf_data.json'
CHEMIN_SAUVEGARDE = BASE_DIR / 'vectorisation'
CHEMIN_SAUVEGARDE.mkdir(exist_ok=True)

def preparer_donnees():
    # Charger la matrice TF-IDF
    print("Chargement de la matrice TF-IDF...")
    matrice_tfidf = joblib.load(CHEMIN_MATRICE)
    
    # Charger les données originales
    print("Chargement des données d'origine...")
    with open(CHEMIN_DONNEES, 'r', encoding='utf-8') as f:
        donnees = pd.read_json(f)
    
    # Simuler des étiquettes (à remplacer par vos vraies annotations)
    print("Génération des étiquettes...")
    sentiments = ['positif', 'négatif', 'neutre']
    y = pd.Series(np.random.choice(sentiments, size=len(donnees)))  # Modifié ici
    
    # Diviser les données
    print("Division des données...")
    X_train, X_test, y_train, y_test = train_test_split(
        matrice_tfidf, y, test_size=0.2, random_state=42
    )
    
    # Sauvegarder les ensembles de données
    print("Sauvegarde des ensembles de données...")
    joblib.dump(X_train, CHEMIN_SAUVEGARDE / 'X_train.pkl')
    joblib.dump(X_test, CHEMIN_SAUVEGARDE / 'X_test.pkl')
    joblib.dump(y_train, CHEMIN_SAUVEGARDE / 'y_train.pkl')
    joblib.dump(y_test, CHEMIN_SAUVEGARDE / 'y_test.pkl')
    
    print("Préparation des données terminée avec succès !")

if __name__ == "__main__":
    preparer_donnees()