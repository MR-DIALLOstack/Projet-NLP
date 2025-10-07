import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from pathlib import Path

# Configuration des chemins
BASE_DIR = Path(__file__).parent
CHEMIN_MODELE = BASE_DIR / 'modele_sentiment.pkl'
CHEMIN_ENCODEUR = BASE_DIR / 'encodeur_sentiment.pkl'
CHEMIN_MATRICE_TEST = BASE_DIR / 'vectorisation' / 'X_test.pkl'
CHEMIN_Y_TEST = BASE_DIR / 'vectorisation' / 'y_test.pkl'
CHEMIN_RESULTATS = BASE_DIR / 'resultats_evaluation'
CHEMIN_RESULTATS.mkdir(exist_ok=True)

def charger_et_preparer_donnees():
    """Charge et prépare les données pour l'évaluation"""
    print("Chargement du modèle et des données...")
    
    # Charger le modèle et l'encodeur
    modele = joblib.load(CHEMIN_MODELE)
    encodeur = joblib.load(CHEMIN_ENCODEUR)
    
    # Charger les données de test
    X_test = joblib.load(CHEMIN_MATRICE_TEST)
    y_test = joblib.load(CHEMIN_Y_TEST)
    
    # Convertir en tableaux numpy
    y_test = np.array(y_test)
    
    # Récupérer les noms des classes
    classes = list(encodeur.classes_)
    print(f"Classes de l'encodeur: {classes}")
    
    # Faire les prédictions
    print("Génération des prédictions...")
    y_pred = modele.predict(X_test)
    
    # Afficher les informations de débogage
    print("\n=== INFORMATIONS DE DÉBOGAGE ===")
    print(f"Type de y_test: {type(y_test[0])}, Type de y_pred: {type(y_pred[0])}")
    print(f"Valeurs uniques dans y_test: {np.unique(y_test)}")
    print(f"Valeurs uniques dans y_pred: {np.unique(y_pred)}")
    print(f"Taille de y_test: {len(y_test)}, Taille de y_pred: {len(y_pred)}")
    
    # Afficher la distribution des classes
    print("\nDistribution des classes dans y_test:")
    unique, counts = np.unique(y_test, return_counts=True)
    print(dict(zip(unique, counts)))
    
    print("\nDistribution des classes dans y_pred (avant conversion):")
    unique, counts = np.unique(y_pred, return_counts=True)
    print(dict(zip(unique, counts)))
    
    return modele, encodeur, X_test, y_test, y_pred, classes

def generer_rapport(y_test, y_pred, classes, chemin_sauvegarde):
    """Génère un rapport d'évaluation complet"""
    print("\n" + "="*50)
    print("RAPPORT D'ÉVALUATION DU MODÈLE")
    print("="*50)
    
    # Convertir en tableaux numpy
    y_test = np.array(y_test)
    y_pred = np.array(y_pred)
    
    # Si y_pred est numérique, le convertir en étiquettes
    if np.issubdtype(y_pred.dtype, np.number):
        print("\nConversion des prédictions numériques en étiquettes...")
        # S'assurer que les indices sont valides
        y_pred = np.clip(y_pred, 0, len(classes)-1)
        # Convertir les indices en étiquettes
        y_pred = np.array([classes[int(i)] for i in y_pred])
    
    # Vérifier les valeurs uniques après conversion
    print("\n=== VALEURS APRÈS CONVERSION ===")
    print(f"Classes uniques dans y_test: {np.unique(y_test)}")
    print(f"Classes uniques dans y_pred: {np.unique(y_pred)}")
    
    # Filtrer pour ne garder que les classes attendues
    mask = np.isin(y_test, classes)
    y_test_filtered = y_test[mask]
    y_pred_filtered = y_pred[mask]
    
    print(f"\nTaille des données après filtrage: {len(y_test_filtered)} échantillons")
    
    try:
        # Générer le rapport de classification
        rapport = classification_report(
            y_test_filtered, 
            y_pred_filtered,
            labels=classes,
            target_names=classes,
            output_dict=True,
            zero_division=0
        )
        
        # Afficher le rapport
        print("\n=== RAPPORT DE CLASSIFICATION ===")
        print(classification_report(
            y_test_filtered, 
            y_pred_filtered,
            labels=classes,
            target_names=classes,
            zero_division=0
        ))
        
        # Calculer et afficher l'exactitude
        accuracy = accuracy_score(y_test_filtered, y_pred_filtered)
        print(f"\nExactitude (accuracy): {accuracy:.4f}")
        
        # Sauvegarder le rapport
        df_rapport = pd.DataFrame(rapport).transpose()
        df_rapport.to_csv(chemin_sauvegarde / 'rapport_classification.csv')
        print(f"\nRapport sauvegardé dans {chemin_sauvegarde}/rapport_classification.csv")
        
        return rapport, y_test_filtered, y_pred_filtered
        
    except Exception as e:
        print(f"\nErreur lors de la génération du rapport: {str(e)}")
        print(f"Classes attendues: {classes}")
        print(f"Valeurs uniques dans y_test: {np.unique(y_test)}")
        print(f"Valeurs uniques dans y_pred: {np.unique(y_pred)}")
        raise

def tracer_matrice_confusion(y_test, y_pred, classes, chemin_sauvegarde):
    """Génère et affiche la matrice de confusion"""
    try:
        print("\nGénération de la matrice de confusion...")
        
        # Calculer la matrice de confusion
        cm = confusion_matrix(y_test, y_pred, labels=classes)
        
        # Créer une figure
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Reds',
                    xticklabels=classes,
                    yticklabels=classes)
        plt.title('Matrice de Confusion')
        plt.ylabel('Vérité terrain')
        plt.xlabel('Prédictions')
        
        # Sauvegarder la figure
        plt.tight_layout()
        plt.savefig(chemin_sauvegarde / 'matrice_confusion.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Matrice de confusion sauvegardée dans {chemin_sauvegarde}/matrice_confusion.png")
        
        return cm
        
    except Exception as e:
        print(f"\nErreur lors de la génération de la matrice de confusion: {str(e)}")
        print(f"Classes: {classes}")
        print(f"Taille de y_test: {len(y_test)}, Taille de y_pred: {len(y_pred)}")
        raise

def main():
    try:
        # Charger et préparer les données
        modele, encodeur, X_test, y_test, y_pred, classes = charger_et_preparer_donnees()
        
        # Générer le rapport
        rapport, y_test_filtered, y_pred_filtered = generer_rapport(y_test, y_pred, classes, CHEMIN_RESULTATS)
        
        # Tracer la matrice de confusion
        tracer_matrice_confusion(y_test_filtered, y_pred_filtered, classes, CHEMIN_RESULTATS)
        
        # Afficher un message de succès
        print("\n" + "="*50)
        print("ÉVALUATION TERMINÉE AVEC SUCCÈS")
        print(f"Les résultats ont été enregistrés dans : {CHEMIN_RESULTATS}")
        print("="*50)
        
    except Exception as e:
        print("\n" + "="*50)
        print("ERREUR LORS DE L'ÉVALUATION")
        print("="*50)
        print(f"Erreur: {str(e)}")
        print("\nVeuillez vérifier que :")
        print("1. Le modèle et l'encodeur sont correctement entraînés")
        print("2. Les données d'entrée sont au bon format")
        print("3. Les chemins des fichiers sont corrects")
        print("="*50)
        raise

if __name__ == "__main__":
    main()