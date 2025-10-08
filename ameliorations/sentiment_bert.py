"""
Module d'amélioration avec BERT pour la classification de sentiments
Utilise des embeddings pré-entraînés pour améliorer les performances
"""

import json
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import torch

# Note: Installation requise
# pip install transformers torch

try:
    from transformers import CamembertTokenizer, CamembertModel
    BERT_AVAILABLE = True
except ImportError:
    print("⚠️  Bibliothèque transformers non installée")
    print("Pour utiliser BERT : pip install transformers torch")
    BERT_AVAILABLE = False


class ClassificateurBERT:
    """Classe pour la classification de sentiments avec embeddings BERT"""
    
    def __init__(self, chemin_donnees_annotees, modele_bert='camembert-base'):
        """
        Initialise le classificateur BERT
        
        Args:
            chemin_donnees_annotees: Chemin vers les données annotées
            modele_bert: Nom du modèle BERT à utiliser (CamemBERT pour le français)
        """
        if not BERT_AVAILABLE:
            raise ImportError("Bibliothèque transformers requise. Installez avec: pip install transformers torch")
        
        self.chemin_donnees = chemin_donnees_annotees
        self.modele_bert_nom = modele_bert
        self.encodeur = LabelEncoder()
        
        # Charger le modèle BERT et le tokenizer
        print(f"Chargement du modèle {modele_bert}...")
        self.tokenizer = CamembertTokenizer.from_pretrained(modele_bert)
        self.modele_bert = CamembertModel.from_pretrained(modele_bert)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.modele_bert.to(self.device)
        self.modele_bert.eval()
        
        print(f"✓ Modèle chargé sur : {self.device}")
        
        # Dossier de sortie
        self.dossier_sortie = Path('ameliorations/resultats_bert')
        self.dossier_sortie.mkdir(parents=True, exist_ok=True)
    
    def charger_donnees(self):
        """Charge les données annotées"""
        print("\nChargement des données...")
        
        with open(self.chemin_donnees, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        
        # Filtrer les données annotées
        donnees_annotees = [item for item in donnees if 'sentiment' in item]
        
        if len(donnees_annotees) < 50:
            raise ValueError(
                f"Pas assez de données annotées ({len(donnees_annotees)}). "
                "Minimum requis : 50."
            )
        
        df = pd.DataFrame(donnees_annotees)
        print(f"✓ {len(df)} publications annotées chargées")
        
        return df
    
    def generer_embeddings_bert(self, textes, batch_size=16):
        """
        Génère les embeddings BERT pour une liste de textes
        
        Args:
            textes: Liste de textes
            batch_size: Taille des batchs pour le traitement
        
        Returns:
            Matrice d'embeddings (numpy array)
        """
        print(f"\nGénération des embeddings BERT pour {len(textes)} textes...")
        
        embeddings = []
        
        # Traiter par batches
        for i in range(0, len(textes), batch_size):
            batch_textes = textes[i:i+batch_size]
            
            # Tokeniser
            encoded = self.tokenizer(
                batch_textes,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors='pt'
            )
            
            # Déplacer sur le device
            input_ids = encoded['input_ids'].to(self.device)
            attention_mask = encoded['attention_mask'].to(self.device)
            
            # Générer les embeddings
            with torch.no_grad():
                outputs = self.modele_bert(input_ids=input_ids, attention_mask=attention_mask)
                # Utiliser le [CLS] token (premier token) comme représentation
                cls_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                embeddings.append(cls_embeddings)
            
            if (i // batch_size + 1) % 10 == 0:
                print(f"  Progression : {i+batch_size}/{len(textes)}")
        
        # Concaténer tous les embeddings
        embeddings = np.vstack(embeddings)
        print(f"✓ Embeddings générés : {embeddings.shape}")
        
        return embeddings
    
    def preparer_donnees(self, df):
        """
        Prépare les données avec embeddings BERT
        
        Args:
            df: DataFrame avec les données annotées
        
        Returns:
            X_train, X_test, y_train, y_test, embeddings
        """
        print("\nPréparation des données...")
        
        # Extraire les textes
        if 'texte_traite' in df.columns and df['texte_traite'].notna().all():
            textes = df['texte_traite'].tolist()
        else:
            textes = df['texte'].tolist()
        
        # Générer les embeddings
        embeddings = self.generer_embeddings_bert(textes)
        
        # Sauvegarder les embeddings
        np.save(self.dossier_sortie / 'bert_embeddings.npy', embeddings)
        print(f"✓ Embeddings sauvegardés dans {self.dossier_sortie}/bert_embeddings.npy")
        
        # Encoder les labels
        y = self.encodeur.fit_transform(df['sentiment'])
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            embeddings, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"✓ Taille ensemble d'entraînement : {X_train.shape[0]}")
        print(f"✓ Taille ensemble de test : {X_test.shape[0]}")
        
        return X_train, X_test, y_train, y_test, embeddings
    
    def entrainer_modeles(self, X_train, y_train):
        """
        Entraîne plusieurs modèles sur les embeddings BERT
        
        Args:
            X_train: Embeddings d'entraînement
            y_train: Labels d'entraînement
        
        Returns:
            Dictionnaire des modèles entraînés
        """
        print("\n" + "="*60)
        print("ENTRAÎNEMENT DES MODÈLES AVEC EMBEDDINGS BERT")
        print("="*60)
        
        modeles = {
            'Régression Logistique': LogisticRegression(max_iter=1000, random_state=42),
            'SVM RBF': SVC(kernel='rbf', random_state=42, probability=True),
            'Random Forest': RandomForestClassifier(n_estimators=200, random_state=42)
        }
        
        resultats = {}
        
        for nom, modele in modeles.items():
            print(f"\n📊 Entraînement : {nom}")
            modele.fit(X_train, y_train)
            score = modele.score(X_train, y_train)
            print(f"  Score d'entraînement : {score:.4f}")
            
            resultats[nom] = modele
        
        print("\n" + "="*60)
        
        return resultats
    
    def evaluer_modeles(self, modeles, X_test, y_test):
        """
        Évalue les modèles sur l'ensemble de test
        
        Args:
            modeles: Dictionnaire des modèles
            X_test: Embeddings de test
            y_test: Labels de test
        
        Returns:
            DataFrame avec les résultats, meilleur modèle
        """
        print("\n" + "="*60)
        print("ÉVALUATION SUR L'ENSEMBLE DE TEST")
        print("="*60)
        
        resultats = []
        meilleur_score = 0
        meilleur_modele = None
        meilleur_nom = None
        
        for nom, modele in modeles.items():
            y_pred = modele.predict(X_test)
            score = accuracy_score(y_test, y_pred)
            
            print(f"\n{nom} :")
            print(f"  Exactitude : {score:.4f}")
            print(classification_report(
                y_test, y_pred,
                target_names=self.encodeur.classes_,
                zero_division=0
            ))
            
            resultats.append({
                'Modèle': f'BERT + {nom}',
                'Exactitude': score
            })
            
            # Matrice de confusion
            cm = confusion_matrix(y_test, y_pred)
            self._sauvegarder_matrice_confusion(cm, nom, y_test, y_pred)
            
            if score > meilleur_score:
                meilleur_score = score
                meilleur_modele = modele
                meilleur_nom = nom
        
        print("\n" + "="*60)
        print(f"🏆 MEILLEUR MODÈLE : BERT + {meilleur_nom}")
        print(f"   Exactitude : {meilleur_score:.4f}")
        print("="*60)
        
        df_resultats = pd.DataFrame(resultats)
        df_resultats.to_csv(self.dossier_sortie / 'resultats_bert.csv', index=False)
        
        return df_resultats, meilleur_modele, meilleur_nom, meilleur_score
    
    def _sauvegarder_matrice_confusion(self, cm, nom_modele, y_test, y_pred):
        """Sauvegarde la matrice de confusion"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.encodeur.classes_,
                   yticklabels=self.encodeur.classes_)
        plt.title(f'Matrice de Confusion - BERT + {nom_modele}')
        plt.ylabel('Vérité terrain')
        plt.xlabel('Prédictions')
        plt.tight_layout()
        
        filename = f'matrice_confusion_bert_{nom_modele.replace(" ", "_").lower()}.png'
        plt.savefig(self.dossier_sortie / filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def sauvegarder_modele(self, modele, nom_modele, score):
        """Sauvegarde le meilleur modèle BERT"""
        # Sauvegarder le modèle
        joblib.dump(modele, self.dossier_sortie / 'modele_bert.pkl')
        joblib.dump(self.encodeur, self.dossier_sortie / 'encodeur_bert.pkl')
        
        # Métadonnées
        metadata = {
            'modele_bert': self.modele_bert_nom,
            'classificateur': nom_modele,
            'exactitude': float(score),
            'classes': self.encodeur.classes_.tolist(),
            'date_entrainement': datetime.now().isoformat()
        }
        
        with open(self.dossier_sortie / 'metadata_bert.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Modèle BERT sauvegardé dans {self.dossier_sortie}")
    
    def comparer_avec_tfidf(self):
        """Compare les performances avec le modèle TF-IDF"""
        print("\n" + "="*60)
        print("COMPARAISON BERT vs TF-IDF")
        print("="*60)
        
        # Charger les résultats TF-IDF si disponibles
        chemin_tfidf = Path('EntrainementModele/resultats/comparaison_modeles.csv')
        chemin_bert = self.dossier_sortie / 'resultats_bert.csv'
        
        if chemin_tfidf.exists() and chemin_bert.exists():
            df_tfidf = pd.read_csv(chemin_tfidf)
            df_bert = pd.read_csv(chemin_bert)
            
            print("\nMeilleurs scores TF-IDF :")
            print(df_tfidf[['Modèle', 'Score Test']].to_string(index=False))
            
            print("\nScores BERT :")
            print(df_bert[['Modèle', 'Exactitude']].to_string(index=False))
            
            # Visualisation comparative
            self._visualiser_comparaison_bert_tfidf(df_tfidf, df_bert)
        else:
            print("Fichiers de résultats TF-IDF non trouvés pour la comparaison")
        
        print("="*60)
    
    def _visualiser_comparaison_bert_tfidf(self, df_tfidf, df_bert):
        """Crée une visualisation comparative BERT vs TF-IDF"""
        plt.figure(figsize=(12, 6))
        
        # Préparer les données
        max_score_tfidf = df_tfidf['Score Test'].max()
        max_score_bert = df_bert['Exactitude'].max()
        
        categories = ['TF-IDF (Meilleur)', 'BERT (Meilleur)']
        scores = [max_score_tfidf, max_score_bert]
        colors = ['skyblue', 'lightcoral']
        
        bars = plt.bar(categories, scores, color=colors, alpha=0.7, edgecolor='black')
        
        # Ajouter les valeurs sur les barres
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{score:.2%}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        plt.ylabel('Exactitude (Accuracy)')
        plt.title('Comparaison des Performances : TF-IDF vs BERT')
        plt.ylim(0, 1)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        plt.savefig(self.dossier_sortie / 'comparaison_bert_tfidf.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n📊 Graphique de comparaison sauvegardé")


def main():
    """Fonction principale"""
    if not BERT_AVAILABLE:
        print("❌ Bibliothèque transformers non installée")
        print("Installation : pip install transformers torch")
        return
    
    print("="*60)
    print("AMÉLIORATION AVEC BERT - CLASSIFICATION DE SENTIMENTS")
    print("="*60)
    
    # Utiliser la nouvelle structure
    script_dir = Path(__file__).parent
    projet_dir = script_dir.parent
    chemin_donnees = projet_dir / '02_Annotation' / 'uvbf_data_annote.json'
    
    if not chemin_donnees.exists():
        print(f"\n❌ Erreur : Fichier {chemin_donnees} non trouvé")
        print("Veuillez d'abord annoter les données.")
        return
    
    try:
        # Créer le classificateur
        classificateur = ClassificateurBERT(chemin_donnees)
        
        # Charger les données
        df = classificateur.charger_donnees()
        
        # Préparer les données avec BERT
        X_train, X_test, y_train, y_test, embeddings = classificateur.preparer_donnees(df)
        
        # Entraîner les modèles
        modeles = classificateur.entrainer_modeles(X_train, y_train)
        
        # Évaluer les modèles
        df_resultats, meilleur_modele, meilleur_nom, meilleur_score = classificateur.evaluer_modeles(
            modeles, X_test, y_test
        )
        
        # Sauvegarder le meilleur modèle
        classificateur.sauvegarder_modele(meilleur_modele, meilleur_nom, meilleur_score)
        
        # Comparer avec TF-IDF
        classificateur.comparer_avec_tfidf()
        
        print("\n✅ AMÉLIORATION BERT TERMINÉE !")
        print(f"📂 Résultats dans : {classificateur.dossier_sortie}")
        
    except Exception as e:
        print(f"\n❌ Erreur : {str(e)}")
        raise


if __name__ == "__main__":
    main()


