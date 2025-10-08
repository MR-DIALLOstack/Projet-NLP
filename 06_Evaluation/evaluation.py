"""
Évaluation du Modèle de Classification de Sentiments
"""

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from pathlib import Path


def charger_modele_et_donnees():
    """Charge le modèle et les données de test"""
    script_dir = Path(__file__).parent
    projet_dir = script_dir.parent
    
    print("Chargement du modèle et des données...")
    
    # Charger le modèle et l'encodeur
    modele = joblib.load(script_dir / 'modele_sentiment.pkl')
    encodeur = joblib.load(script_dir / 'encodeur_sentiment.pkl')
    
    # Charger les données de test
    X_test = joblib.load(projet_dir / '05_Entrainement' / 'resultats' / 'X_test.pkl')
    y_test = joblib.load(projet_dir / '05_Entrainement' / 'resultats' / 'y_test.pkl')
    
    print(f"✓ Modèle chargé")
    print(f"✓ Classes : {list(encodeur.classes_)}")
    
    return modele, encodeur, X_test, y_test


def evaluer_modele(modele, encodeur, X_test, y_test):
    """Évalue le modèle"""
    print("\n" + "="*70)
    print("ÉVALUATION DU MODÈLE")
    print("="*70)
    
    # Prédictions
    y_pred = modele.predict(X_test)
    
    # Convertir en labels textuels
    y_test_labels = encodeur.inverse_transform(y_test)
    y_pred_labels = encodeur.inverse_transform(y_pred)
    
    # Exactitude
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✓ Exactitude globale : {accuracy:.2%}")
    
    # Rapport de classification
    print("\n" + "-"*70)
    print("MÉTRIQUES DÉTAILLÉES PAR CLASSE")
    print("-"*70)
    print(classification_report(
        y_test_labels, y_pred_labels,
        target_names=encodeur.classes_,
        zero_division=0
    ))
    
    return y_test_labels, y_pred_labels, encodeur.classes_


def creer_matrice_confusion(y_test, y_pred, classes):
    """Crée et sauvegarde la matrice de confusion"""
    script_dir = Path(__file__).parent
    dossier_resultats = script_dir / 'resultats_evaluation'
    dossier_resultats.mkdir(exist_ok=True)
    
    print("\nGénération de la matrice de confusion...")
    
    cm = confusion_matrix(y_test, y_pred, labels=classes)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=classes, yticklabels=classes)
    plt.title('Matrice de Confusion - Analyse de Sentiment UVBF', fontsize=14, fontweight='bold')
    plt.ylabel('Vérité Terrain', fontsize=12)
    plt.xlabel('Prédictions', fontsize=12)
    plt.tight_layout()
    
    chemin = dossier_resultats / 'matrice_confusion.png'
    plt.savefig(chemin, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Matrice sauvegardée : {chemin}")
    
    # Sauvegarder aussi les métriques
    rapport_dict = classification_report(y_test, y_pred, target_names=classes, output_dict=True, zero_division=0)
    df_rapport = pd.DataFrame(rapport_dict).transpose()
    df_rapport.to_csv(dossier_resultats / 'rapport_metriques.csv')
    
    print(f"✓ Métriques sauvegardées : {dossier_resultats}/rapport_metriques.csv")


def main():
    print("\n" + "="*70)
    print("ÉVALUATION - MODÈLE DE SENTIMENT UVBF")
    print("="*70)
    
    # Charger
    modele, encodeur, X_test, y_test = charger_modele_et_donnees()
    
    # Évaluer
    y_test_labels, y_pred_labels, classes = evaluer_modele(modele, encodeur, X_test, y_test)
    
    # Matrice de confusion
    creer_matrice_confusion(y_test_labels, y_pred_labels, classes)
    
    print("\n" + "="*70)
    print("✅ ÉVALUATION TERMINÉE")
    print("="*70)
    print("\nConsultez les résultats dans : 06_Evaluation/resultats_evaluation/")


if __name__ == "__main__":
    main()