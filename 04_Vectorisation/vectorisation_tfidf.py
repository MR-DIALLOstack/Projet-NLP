import json
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from pathlib import Path

def charger_donnees(chemin):
    """Charge les données JSON prétraitées"""
    with open(chemin, 'r', encoding='utf-8') as f:
        return json.load(f)

def creer_dataframe(donnees):
    """Crée un DataFrame à partir des données JSON"""
    textes = []
    metadonnees = []
    
    for item in donnees:
        if 'texte_traite' in item and item['texte_traite']:
            textes.append(item['texte_traite'])
            metadonnees.append({
                'id': item.get('id', ''),
                'plateforme': item.get('plateforme', ''),
                'auteur': item.get('auteur', ''),
                'sentiment': item.get('sentiment', '')
            })
    
    df = pd.DataFrame(metadonnees)
    df['texte'] = textes
    return df

def vectoriser_tfidf(df, colonne_texte='texte'):
    """Effectue la vectorisation TF-IDF sur les textes"""
    vectoriseur = TfidfVectorizer(
        max_features=5000,
        min_df=2,
        max_df=0.8,
        ngram_range=(1, 2)
    )
    
    matrice_tfidf = vectoriseur.fit_transform(df[colonne_texte])
    return matrice_tfidf, vectoriseur

def sauvegarder_resultats(df, matrice_tfidf, vectoriseur, dossier_sortie):
    """Sauvegarde les résultats de la vectorisation"""
    dossier_sortie.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder la matrice et le vectoriseur
    joblib.dump(matrice_tfidf, dossier_sortie / 'matrice_tfidf.pkl')
    joblib.dump(vectoriseur, dossier_sortie / 'vectoriseur.pkl')
    
    # Afficher les termes importants
    somme_poids = matrice_tfidf.sum(axis=0)
    termes_importants = [
        (mot, somme_poids[0, idx])
        for mot, idx in vectoriseur.vocabulary_.items()
    ]
    termes_importants = sorted(termes_importants, key=lambda x: x[1], reverse=True)[:20]
    
    print("\n20 termes les plus importants par TF-IDF :")
    for terme, score in termes_importants:
        print(f"  {terme}: {score:.2f}")

def main():
    # Chemins
    script_dir = Path(__file__).parent
    projet_dir = script_dir.parent
    
    chemin_entree = projet_dir / '03_Pretraitement' / 'uvbf_data_pretraite.json'
    dossier_sortie = script_dir
    
    print("="*70)
    print("VECTORISATION TF-IDF")
    print("="*70)
    
    # Charger les données
    print(f"\nChargement depuis : {chemin_entree}")
    donnees = charger_donnees(chemin_entree)
    print(f"✓ {len(donnees)} publications chargées")
    
    # Créer le DataFrame
    print("\nCréation du DataFrame...")
    df = creer_dataframe(donnees)
    print(f"✓ {len(df)} textes prétraités trouvés")
    
    if len(df) == 0:
        print("\n❌ Aucun texte prétraité trouvé !")
        return
    
    # Vectoriser
    print("\nVectorisation TF-IDF en cours...")
    matrice_tfidf, vectoriseur = vectoriser_tfidf(df)
    
    print(f"\n✓ Matrice TF-IDF créée !")
    print(f"  Dimensions : {matrice_tfidf.shape[0]} documents × {matrice_tfidf.shape[1]} features")
    
    # Sauvegarder
    print("\nSauvegarde des résultats...")
    sauvegarder_resultats(df, matrice_tfidf, vectoriseur, dossier_sortie)
    
    print(f"\n✓ Fichiers sauvegardés dans : {dossier_sortie}/")
    print("  - vectoriseur.pkl")
    print("  - matrice_tfidf.pkl")
    
    print("\n" + "="*70)
    print("✅ VECTORISATION TERMINÉE")
    print("="*70)

if __name__ == "__main__":
    main()