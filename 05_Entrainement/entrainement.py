"""
Entraînement des Modèles de Classification de Sentiments
"""

import joblib
import numpy as np
import pandas as pd
import json
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class EntraineurSentiment:
    """Classe pour entraîner les modèles"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.projet_dir = self.script_dir.parent
        self.dossier_resultats = self.script_dir / 'resultats'
        self.dossier_resultats.mkdir(exist_ok=True)
        
        self.encodeur = LabelEncoder()
        self.meilleur_modele = None
        self.meilleur_score = 0
        self.meilleur_nom = ""
    
    def charger_donnees(self):
        """Charge les données annotées et la matrice TF-IDF"""
        print("Chargement des données...")
        
        # Charger les données annotées
        chemin_donnees = self.projet_dir / '02_Annotation' / 'uvbf_data_annote.json'
        with open(chemin_donnees, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        
        # Filtrer les données annotées
        donnees_annotees = [item for item in donnees if 'sentiment' in item]
        print(f" {len(donnees_annotees)} publications annotées")
        
        # Charger le vectoriseur et la matrice
        chemin_vectoriseur = self.projet_dir / '04_Vectorisation' / 'vectoriseur.pkl'
        chemin_matrice = self.projet_dir / '04_Vectorisation' / 'matrice_tfidf.pkl'
        
        vectoriseur = joblib.load(chemin_vectoriseur)
        
        # Recréer la matrice pour les données annotées
        df = pd.DataFrame(donnees_annotees)
        X = vectoriseur.transform(df['texte_traite'] if 'texte_traite' in df.columns else df['texte'])
        
        # Encoder les labels
        y = self.encodeur.fit_transform(df['sentiment'])
        
        return X, y, df
    
    def diviser_donnees(self, X, y):
        """Divise les données en train/test"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n Division effectuée :")
        print(f"  Train : {X_train.shape[0]} échantillons")
        print(f"  Test  : {X_test.shape[0]} échantillons")
        
        # Sauvegarder
        joblib.dump(X_train, self.dossier_resultats / 'X_train.pkl')
        joblib.dump(X_test, self.dossier_resultats / 'X_test.pkl')
        joblib.dump(y_train, self.dossier_resultats / 'y_train.pkl')
        joblib.dump(y_test, self.dossier_resultats / 'y_test.pkl')
        
        return X_train, X_test, y_train, y_test
    
    def entrainer_modeles(self, X_train, y_train):
        """Entraîne plusieurs modèles"""
        print("\n" + "="*70)
        print("ENTRAÎNEMENT DES MODÈLES")
        print("="*70)
        
        modeles = {
            'Naive Bayes': MultinomialNB(),
            'Régression Logistique': LogisticRegression(max_iter=1000, random_state=42),
            'SVM Linéaire': SVC(kernel='linear', random_state=42, probability=True),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        resultats = {}
        
        for nom, modele in modeles.items():
            print(f"\n {nom}")
            modele.fit(X_train, y_train)
            
            score_train = modele.score(X_train, y_train)
            cv_scores = cross_val_score(modele, X_train, y_train, cv=5)
            
            print(f"  Train : {score_train:.2%}")
            print(f"  CV    : {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")
            
            resultats[nom] = {
                'modele': modele,
                'score_train': score_train,
                'score_cv': cv_scores.mean()
            }
        
        return resultats
    
    def optimiser_modele(self, X_train, y_train):
        """Optimise les hyperparamètres"""
        print("\n" + "="*70)
        print("OPTIMISATION DES HYPERPARAMÈTRES")
        print("="*70)
        
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'penalty': ['l2'],
            'solver': ['lbfgs']
        }
        
        print("\nOptimisation de la Régression Logistique...")
        grid = GridSearchCV(
            LogisticRegression(max_iter=1000, random_state=42),
            param_grid, cv=5, n_jobs=-1, verbose=0
        )
        
        grid.fit(X_train, y_train)
        
        print(f"✓ Meilleurs paramètres : {grid.best_params_}")
        print(f"✓ Meilleur score CV : {grid.best_score_:.2%}")
        
        return {'Régression Logistique Optimisée': {
            'modele': grid.best_estimator_,
            'score_train': grid.best_estimator_.score(X_train, y_train),
            'score_cv': grid.best_score_
        }}
    
    def evaluer_modeles(self, resultats, X_test, y_test):
        """Évalue tous les modèles sur le test"""
        print("\n" + "="*70)
        print("ÉVALUATION SUR L'ENSEMBLE DE TEST")
        print("="*70)
        
        comparaison = []
        
        for nom, info in resultats.items():
            modele = info['modele']
            y_pred = modele.predict(X_test)
            score_test = accuracy_score(y_test, y_pred)
            
            print(f"\n{nom} : {score_test:.2%}")
            
            comparaison.append({
                'Modèle': nom,
                'Score Train': info['score_train'],
                'Score CV': info['score_cv'],
                'Score Test': score_test
            })
            
            if score_test > self.meilleur_score:
                self.meilleur_score = score_test
                self.meilleur_modele = modele
                self.meilleur_nom = nom
        
        # Sauvegarder la comparaison
        df_comp = pd.DataFrame(comparaison)
        df_comp.to_csv(self.dossier_resultats / 'comparaison_modeles.csv', index=False)
        
        # Graphique
        self._visualiser_comparaison(df_comp)
        
        print("\n" + "="*70)
        print(f"🏆 MEILLEUR MODÈLE : {self.meilleur_nom}")
        print(f"   Exactitude : {self.meilleur_score:.2%}")
        print("="*70)
        
        return df_comp
    
    def _visualiser_comparaison(self, df):
        """Crée un graphique de comparaison"""
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(df))
        width = 0.25
        
        ax.bar(x - width, df['Score Train'], width, label='Train', alpha=0.8)
        ax.bar(x, df['Score CV'], width, label='CV', alpha=0.8)
        ax.bar(x + width, df['Score Test'], width, label='Test', alpha=0.8)
        
        ax.set_xlabel('Modèles')
        ax.set_ylabel('Exactitude')
        ax.set_title('Comparaison des Performances des Modèles')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Modèle'], rotation=45, ha='right')
        ax.legend()
        ax.set_ylim(0, 1)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.dossier_resultats / 'comparaison_modeles.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Graphique sauvegardé : {self.dossier_resultats}/comparaison_modeles.png")
    
    def sauvegarder_modele(self):
        """Sauvegarde le meilleur modèle"""
        joblib.dump(self.meilleur_modele, self.script_dir / 'modele_sentiment.pkl')
        joblib.dump(self.encodeur, self.script_dir / 'encodeur_labels.pkl')
        
        # Copier aussi vers le dossier d'évaluation
        eval_dir = self.projet_dir / '06_Evaluation'
        eval_dir.mkdir(exist_ok=True)
        joblib.dump(self.meilleur_modele, eval_dir / 'modele_sentiment.pkl')
        joblib.dump(self.encodeur, eval_dir / 'encodeur_sentiment.pkl')
        
        print(f"\n✓ Modèle sauvegardé :")
        print(f"  - {self.script_dir}/modele_sentiment.pkl")
        print(f"  - {self.script_dir}/encodeur_labels.pkl")
    
    def calculer_statistiques_sentiment(self, df):
        """Calcule les statistiques de sentiment"""
        print("\n" + "="*70)
        print("STATISTIQUES DES SENTIMENTS")
        print("="*70)
        
        stats = df['sentiment'].value_counts(normalize=True) * 100
        
        print("\nRépartition des sentiments :")
        for sentiment, pct in stats.items():
            count = df['sentiment'].value_counts()[sentiment]
            print(f"  {sentiment.capitalize()}: {count} ({pct:.1f}%)")
        
        if 'plateforme' in df.columns:
            print("\nPar plateforme :")
            pivot = pd.crosstab(df['plateforme'], df['sentiment'], normalize='index') * 100
            print(pivot.round(1).to_string())
        
        print("="*70)


def main():
    print("\n" + "="*70)
    print("ENTRAÎNEMENT - CLASSIFICATION DE SENTIMENTS UVBF")
    print("="*70)
    
    entraineur = EntraineurSentiment()
    
    # Charger
    X, y, df = entraineur.charger_donnees()
    
    # Statistiques
    entraineur.calculer_statistiques_sentiment(df)
    
    # Diviser
    X_train, X_test, y_train, y_test = entraineur.diviser_donnees(X, y)
    
    # Entraîner
    resultats = entraineur.entrainer_modeles(X_train, y_train)
    
    # Optimiser
    resultats_opt = entraineur.optimiser_modele(X_train, y_train)
    resultats.update(resultats_opt)
    
    # Évaluer
    entraineur.evaluer_modeles(resultats, X_test, y_test)
    
    # Sauvegarder
    entraineur.sauvegarder_modele()
    
    print("\n ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS !")
    print(f" Résultats dans : {entraineur.dossier_resultats}")


if __name__ == "__main__":
    main()