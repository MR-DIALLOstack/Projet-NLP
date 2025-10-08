"""
Pipeline Complet - Analyse de Sentiment UVBF

Ce script exécute toutes les étapes du projet de manière séquentielle :
1. Vérification des données collectées
2. Annotation des sentiments
3. Prétraitement des textes
4. Vectorisation TF-IDF
5. Entraînement des modèles
6. Évaluation
7. Génération du rapport final

Utilisation :
    python pipeline_complet.py
"""

import sys
import subprocess
from pathlib import Path
import json


class PipelineUVBF:
    """Gestionnaire du pipeline complet d'analyse de sentiment"""
    
    def __init__(self):
        self.projet_dir = Path(__file__).parent
        self.etapes_completees = []
        self.erreurs = []
    
    def afficher_banniere(self):
        """Affiche la bannière du projet"""
        print("\n" + "="*80)
        print(" "*15 + "PIPELINE COMPLET - ANALYSE DE SENTIMENT UVBF")
        print(" "*18 + "Université Virtuelle du Burkina Faso")
        print("="*80)
        print("\nCe script va exécuter toutes les étapes du projet :")
        print("  1. ✓ Vérification des données collectées")
        print("  2. → Annotation des sentiments")
        print("  3. → Prétraitement des textes")
        print("  4. → Vectorisation TF-IDF")
        print("  5. → Entraînement des modèles")
        print("  6. → Évaluation du modèle")
        print("  7. → Génération du rapport final")
        print("="*80 + "\n")
    
    def verifier_fichier(self, chemin, description):
        """Vérifie l'existence d'un fichier"""
        fichier = self.projet_dir / chemin
        if fichier.exists():
            print(f"  ✓ {description}")
            return True
        else:
            print(f"  ✗ {description} manquant")
            return False
    
    def etape_1_verification_donnees(self):
        """Vérifie que les données ont été collectées"""
        print("\n" + "="*80)
        print("ÉTAPE 1/7 : VÉRIFICATION DES DONNÉES COLLECTÉES")
        print("="*80)
        
        chemin_donnees = self.projet_dir / "01_Collecte_Donnees" / "uvbf_data.json"
        
        if not chemin_donnees.exists():
            print("\n❌ Fichier de données non trouvé !")
            print("\n📌 Actions requises :")
            print("  1. Les données doivent être collectées manuellement")
            print("  2. Consultez 01_Collecte_Donnees/README.md pour les instructions")
            print("  3. Ou générez des données de démonstration :")
            print("     cd 01_Collecte_Donnees && python scraper_demo.py")
            return False
        
        # Vérifier le contenu
        with open(chemin_donnees, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        
        print(f"\n✓ Données trouvées : {len(donnees)} publications")
        
        if len(donnees) < 100:
            print(f"⚠️  Attention : Seulement {len(donnees)} publications")
            print("   Recommandation : Au moins 300 publications pour de bons résultats")
        
        self.etapes_completees.append("Vérification des données")
        return True
    
    def etape_2_annotation(self):
        """Lance l'annotation des sentiments"""
        print("\n" + "="*80)
        print("ÉTAPE 2/7 : ANNOTATION DES SENTIMENTS")
        print("="*80)
        
        chemin_annote = self.projet_dir / "02_Annotation" / "uvbf_data_annote.json"
        
        if chemin_annote.exists():
            print("\n✓ Données déjà annotées trouvées")
            reponse = input("Voulez-vous re-annoter ? (o/n) : ")
            if reponse.lower() != 'o':
                self.etapes_completees.append("Annotation (existante)")
                return True
        
        print("\n📌 Options d'annotation :")
        print("  [1] Annotation automatique (rapide, pour démonstration)")
        print("  [2] Annotation manuelle (recommandé, plus précis)")
        
        choix = input("\nVotre choix [1/2] : ").strip()
        
        if choix == '1':
            print("\nLancement de l'annotation automatique...")
            cmd = f'cd "{self.projet_dir / "02_Annotation"}" && python annotation_manuelle.py --mode auto --nombre 300'
        elif choix == '2':
            print("\nLancement de l'annotation manuelle...")
            print("Utilisez 'q' pour quitter et sauvegarder à tout moment\n")
            cmd = f'cd "{self.projet_dir / "02_Annotation"}" && python annotation_manuelle.py --mode manuel --nombre 100'
        else:
            print("Choix invalide. Étape sautée.")
            return False
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.etapes_completees.append("Annotation")
            return True
        except subprocess.CalledProcessError:
            self.erreurs.append("Erreur lors de l'annotation")
            return False
    
    def etape_3_pretraitement(self):
        """Lance le prétraitement des textes"""
        print("\n" + "="*80)
        print("ÉTAPE 3/7 : PRÉTRAITEMENT DES TEXTES")
        print("="*80)
        
        print("\nNettoyage et normalisation des textes...")
        print("- Suppression mentions, hashtags, URLs")
        print("- Tokenisation et lemmatisation")
        print("- Suppression des stop words\n")
        
        cmd = f'cd "{self.projet_dir / "03_Pretraitement"}" && python pretraitement.py'
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.etapes_completees.append("Prétraitement")
            return True
        except subprocess.CalledProcessError:
            self.erreurs.append("Erreur lors du prétraitement")
            return False
    
    def etape_4_vectorisation(self):
        """Lance la vectorisation TF-IDF"""
        print("\n" + "="*80)
        print("ÉTAPE 4/7 : VECTORISATION TF-IDF")
        print("="*80)
        
        print("\nTransformation des textes en vecteurs numériques...\n")
        
        cmd = f'cd "{self.projet_dir / "04_Vectorisation"}" && python vectorisation_tfidf.py'
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.etapes_completees.append("Vectorisation")
            return True
        except subprocess.CalledProcessError:
            self.erreurs.append("Erreur lors de la vectorisation")
            return False
    
    def etape_5_entrainement(self):
        """Lance l'entraînement des modèles"""
        print("\n" + "="*80)
        print("ÉTAPE 5/7 : ENTRAÎNEMENT DES MODÈLES")
        print("="*80)
        
        print("\nEntraînement et comparaison de plusieurs modèles...")
        print("Cela peut prendre quelques minutes...\n")
        
        cmd = f'cd "{self.projet_dir / "05_Entrainement"}" && python entrainement.py'
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.etapes_completees.append("Entraînement")
            return True
        except subprocess.CalledProcessError:
            self.erreurs.append("Erreur lors de l'entraînement")
            return False
    
    def etape_6_evaluation(self):
        """Lance l'évaluation du modèle"""
        print("\n" + "="*80)
        print("ÉTAPE 6/7 : ÉVALUATION DU MODÈLE")
        print("="*80)
        
        print("\nCalcul des métriques de performance...\n")
        
        cmd = f'cd "{self.projet_dir / "06_Evaluation"}" && python evaluation.py'
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.etapes_completees.append("Évaluation")
            return True
        except subprocess.CalledProcessError:
            self.erreurs.append("Erreur lors de l'évaluation")
            return False
    
    def etape_7_rapport(self):
        """Génère le rapport final"""
        print("\n" + "="*80)
        print("ÉTAPE 7/7 : GÉNÉRATION DU RAPPORT FINAL")
        print("="*80)
        
        print("\nCompilation des résultats et génération du rapport...\n")
        
        cmd = f'cd "{self.projet_dir / "07_Rapport_Final"}" && python generer_rapport.py'
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.etapes_completees.append("Rapport final")
            return True
        except subprocess.CalledProcessError:
            self.erreurs.append("Erreur lors de la génération du rapport")
            return False
    
    def afficher_resume(self):
        """Affiche le résumé de l'exécution"""
        print("\n" + "="*80)
        print("RÉSUMÉ DE L'EXÉCUTION")
        print("="*80)
        
        print(f"\n✓ Étapes complétées ({len(self.etapes_completees)}/7) :")
        for i, etape in enumerate(self.etapes_completees, 1):
            print(f"  {i}. ✓ {etape}")
        
        if self.erreurs:
            print(f"\n✗ Erreurs rencontrées ({len(self.erreurs)}) :")
            for erreur in self.erreurs:
                print(f"  - {erreur}")
        
        print("\n" + "="*80)
        
        if len(self.etapes_completees) == 7:
            print("✅ PIPELINE TERMINÉ AVEC SUCCÈS !")
            print("\n📊 Consultez les résultats :")
            print("  - Rapport final : 07_Rapport_Final/rapport_final.txt")
            print("  - Résumé : RESULTATS.md")
            print("  - Matrice de confusion : 06_Evaluation/matrice_confusion.png")
        else:
            print("⚠️  PIPELINE INCOMPLET")
            print("\nConsultez les messages d'erreur ci-dessus.")
        
        print("="*80 + "\n")
    
    def executer(self):
        """Exécute le pipeline complet"""
        self.afficher_banniere()
        
        # Demander confirmation
        reponse = input("Voulez-vous lancer le pipeline complet ? (o/n) : ")
        if reponse.lower() != 'o':
            print("\nPipeline annulé.")
            return
        
        # Exécuter chaque étape
        if not self.etape_1_verification_donnees():
            self.afficher_resume()
            return
        
        if not self.etape_2_annotation():
            self.afficher_resume()
            return
        
        if not self.etape_3_pretraitement():
            self.afficher_resume()
            return
        
        if not self.etape_4_vectorisation():
            self.afficher_resume()
            return
        
        if not self.etape_5_entrainement():
            self.afficher_resume()
            return
        
        if not self.etape_6_evaluation():
            self.afficher_resume()
            return
        
        if not self.etape_7_rapport():
            self.afficher_resume()
            return
        
        # Afficher le résumé final
        self.afficher_resume()


def main():
    """Point d'entrée principal"""
    pipeline = PipelineUVBF()
    pipeline.executer()


if __name__ == "__main__":
    main()

