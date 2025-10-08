"""
Script principal pour orchestrer le pipeline complet d'analyse de sentiment UVBF

Ce script permet d'exécuter toutes les étapes du projet :
1. Scraping des données
2. Prétraitement
3. Annotation 
4. Vectorisation TF-IDF
5. Entraînement des modèles
6. Amélioration avec BERT 
7. Évaluation
8. Génération du rapport final

Auteur: Projet NLP - Analyse de Sentiment UVBF
Date: 2025
"""

import sys
import argparse
from pathlib import Path
import subprocess


class PipelineUVBF:
    """Classe pour orchestrer le pipeline complet"""
    
    def __init__(self, mode_demo=True, utiliser_bert=False):
        """
        Initialise le pipeline
        
        Args:
            mode_demo: Mode démonstration (données fictives)
            utiliser_bert: Utiliser BERT pour l'amélioration
        """
        self.mode_demo = mode_demo
        self.utiliser_bert = utiliser_bert
        self.etapes_completees = []
    
    def afficher_banniere(self):
        """Affiche la bannière du projet"""
        print("\n" + "="*80)
        print(" "*20 + "PROJET ANALYSE DE SENTIMENT UVBF")
        print(" "*15 + "Université Virtuelle du Burkina Faso")
        print("="*80)
        print("\nObjectif : Analyser les sentiments des publications sur l'UVBF")
        print("          depuis les réseaux sociaux (Twitter, Facebook, etc.)")
        print("="*80 + "\n")
    
    def verifier_fichier(self, chemin, description):
        """Vérifie si un fichier existe"""
        if Path(chemin).exists():
            print(f"  ✓ {description} trouvé")
            return True
        else:
            print(f"  ✗ {description} non trouvé")
            return False
    
    def executer_script(self, commande, description):
        """
        Exécute un script Python
        
        Args:
            commande: Commande à exécuter
            description: Description de l'étape
        
        Returns:
            True si succès, False sinon
        """
        print(f"\n{'='*80}")
        print(f"ÉTAPE : {description}")
        print(f"{'='*80}")
        
        try:
            result = subprocess.run(
                commande,
                shell=True,
                check=True,
                capture_output=False,
                text=True
            )
            
            print(f"\n✅ {description} - TERMINÉ")
            self.etapes_completees.append(description)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ {description} - ERREUR")
            print(f"Code de retour : {e.returncode}")
            return False
        except Exception as e:
            print(f"\n❌ {description} - ERREUR: {str(e)}")
            return False
    
    def etape_1_scraping(self):
        """Étape 1: Scraping des données"""
        print("\n" + "="*80)
        print("ÉTAPE 1: SCRAPING DES DONNÉES")
        print("="*80)
        
        # Vérifier si les données existent déjà
        if self.verifier_fichier('Dataset brute/uvbf_data.json', 'Données brutes'):
            reponse = input("\n📌 Des données existent déjà. Voulez-vous scraper de nouvelles données ? (o/n): ")
            if reponse.lower() != 'o':
                print("Étape de scraping sautée.")
                self.etapes_completees.append("Scraping (sauté)")
                return True
        
        # Exécuter le scraping
        commande = 'python scraping/scraper_reseaux_sociaux.py'
        return self.executer_script(commande, "Scraping des réseaux sociaux")
    
    def etape_2_pretraitement(self):
        """Étape 2: Prétraitement des données"""
        print("\n" + "="*80)
        print("ÉTAPE 2: PRÉTRAITEMENT DES TEXTES")
        print("="*80)
        
        # Vérifier les données d'entrée
        if not self.verifier_fichier('Dataset brute/uvbf_data.json', 'Données brutes'):
            print("❌ Impossible de continuer sans données brutes")
            return False
        
        # Vérifier si déjà fait
        if self.verifier_fichier('Pretraitement/uvbf_data_pretraitement.json', 'Données prétraitées'):
            reponse = input("\n📌 Données déjà prétraitées. Refaire le prétraitement ? (o/n): ")
            if reponse.lower() != 'o':
                print("Étape de prétraitement sautée.")
                self.etapes_completees.append("Prétraitement (sauté)")
                return True
        
        # Exécuter le prétraitement
        commande = 'cd Pretraitement && python Pretraitement.py'
        return self.executer_script(commande, "Prétraitement des textes")
    
    def etape_3_annotation(self, mode='stats'):
        """Étape 3: Annotation des sentiments"""
        print("\n" + "="*80)
        print("ÉTAPE 3: ANNOTATION DES SENTIMENTS")
        print("="*80)
        
        # Vérifier si déjà annoté
        if self.verifier_fichier('Dataset brute/uvbf_data_annote.json', 'Données annotées'):
            reponse = input("\n📌 Données déjà annotées. Voir les statistiques ? (o/n): ")
            if reponse.lower() == 'o':
                commande = 'python annotation/annotation_manuelle.py --mode stats'
                self.executer_script(commande, "Statistiques d'annotation")
            
            reponse = input("\n📌 Voulez-vous annoter plus de données ? (o/n): ")
            if reponse.lower() != 'o':
                print("Étape d'annotation sautée.")
                self.etapes_completees.append("Annotation (sauté)")
                return True
        
        print("\n📌 Modes d'annotation disponibles :")
        print("  [1] Manuel - Annoter manuellement (recommandé pour projet réel)")
        print("  [2] Auto - Annotation automatique pour démonstration")
        print("  [3] Stats - Voir les statistiques uniquement")
        
        if mode == 'auto':
            choix = '2'
        elif mode == 'stats':
            choix = '3'
        else:
            choix = input("\nVotre choix [1/2/3]: ").strip()
        
        if choix == '1':
            print("\n⚠️  Mode manuel sélectionné.")
            print("Vous allez annoter les publications une par une.")
            print("Appuyez sur 'q' à tout moment pour sauvegarder et quitter.")
            input("\nAppuyez sur Entrée pour commencer...")
            
            commande = 'python annotation/annotation_manuelle.py --mode manuel --nombre 50'
            return self.executer_script(commande, "Annotation manuelle")
        
        elif choix == '2':
            print("\n⚠️  Mode automatique (DÉMONSTRATION uniquement)")
            print("L'annotation sera basée sur des mots-clés simples.")
            print("Pour un projet réel, utilisez l'annotation manuelle.")
            
            commande = 'python annotation/annotation_manuelle.py --mode auto --nombre 300'
            return self.executer_script(commande, "Annotation automatique")
        
        elif choix == '3':
            commande = 'python annotation/annotation_manuelle.py --mode stats'
            return self.executer_script(commande, "Statistiques d'annotation")
        
        else:
            print("Choix invalide. Étape sautée.")
            return False
    
    def etape_4_vectorisation(self):
        """Étape 4: Vectorisation TF-IDF"""
        print("\n" + "="*80)
        print("ÉTAPE 4: VECTORISATION TF-IDF")
        print("="*80)
        
        # Vérifier les données prétraitées
        if not self.verifier_fichier('Pretraitement/uvbf_data_pretraitement.json', 'Données prétraitées'):
            print("❌ Impossible de continuer sans données prétraitées")
            return False
        
        # Exécuter la vectorisation
        commande = 'cd vectorisation && python vectorisation_tfidf.py'
        return self.executer_script(commande, "Vectorisation TF-IDF")
    
    def etape_5_entrainement(self):
        """Étape 5: Entraînement des modèles"""
        print("\n" + "="*80)
        print("ÉTAPE 5: ENTRAÎNEMENT DES MODÈLES")
        print("="*80)
        
        # Vérifier les prérequis
        if not self.verifier_fichier('Dataset brute/uvbf_data_annote.json', 'Données annotées'):
            print("❌ Impossible de continuer sans données annotées")
            return False
        
        if not self.verifier_fichier('vectorisation/uvbf_tfidf_vectoriseur.pkl', 'Vectoriseur TF-IDF'):
            print("❌ Impossible de continuer sans vectoriseur")
            return False
        
        # Exécuter l'entraînement
        commande = 'python EntrainementModele/entrainement_ameliore.py'
        return self.executer_script(commande, "Entraînement des modèles")
    
    def etape_6_bert(self):
        """Étape 6: Amélioration avec BERT (optionnel)"""
        if not self.utiliser_bert:
            print("\nÉtape BERT sautée (non demandée)")
            return True
        
        print("\n" + "="*80)
        print("ÉTAPE 6: AMÉLIORATION AVEC BERT")
        print("="*80)
        
        print("\n⚠️  Cette étape nécessite :")
        print("  - Bibliothèque transformers : pip install transformers torch")
        print("  - GPU recommandé pour de meilleures performances")
        print("  - Temps d'exécution plus long")
        
        reponse = input("\n📌 Voulez-vous continuer avec BERT ? (o/n): ")
        if reponse.lower() != 'o':
            print("Étape BERT sautée.")
            return True
        
        # Exécuter l'amélioration BERT
        commande = 'python ameliorations/sentiment_bert.py'
        return self.executer_script(commande, "Amélioration avec BERT")
    
    def etape_7_evaluation(self):
        """Étape 7: Évaluation du modèle"""
        print("\n" + "="*80)
        print("ÉTAPE 7: ÉVALUATION DU MODÈLE")
        print("="*80)
        
        # Vérifier le modèle
        if not self.verifier_fichier('EntrainementModele/modele_sentiment.pkl', 'Modèle entraîné'):
            print("❌ Impossible d'évaluer sans modèle entraîné")
            return False
        
        # Copier les fichiers nécessaires pour l'évaluation
        self._preparer_evaluation()
        
        # Exécuter l'évaluation
        commande = 'cd evaluation && python evaluation.py'
        return self.executer_script(commande, "Évaluation du modèle")
    
    def _preparer_evaluation(self):
        """Prépare les fichiers pour l'évaluation"""
        import shutil
        
        # Copier les fichiers si nécessaire
        fichiers_a_copier = [
            ('EntrainementModele/resultats/X_test.pkl', 'evaluation/vectorisation/X_test.pkl'),
            ('EntrainementModele/resultats/y_test.pkl', 'evaluation/vectorisation/y_test.pkl'),
            ('EntrainementModele/modele_sentiment.pkl', 'evaluation/modele_sentiment.pkl'),
            ('EntrainementModele/encodeur_sentiment.pkl', 'evaluation/encodeur_sentiment.pkl')
        ]
        
        for source, dest in fichiers_a_copier:
            if Path(source).exists():
                Path(dest).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(source, dest)
    
    def etape_8_rapport(self):
        """Étape 8: Génération du rapport final"""
        print("\n" + "="*80)
        print("ÉTAPE 8: GÉNÉRATION DU RAPPORT FINAL")
        print("="*80)
        
        # Exécuter la génération du rapport
        commande = 'python rapport/generer_rapport_final.py'
        return self.executer_script(commande, "Génération du rapport final")
    
    def afficher_resume(self):
        """Affiche le résumé de l'exécution"""
        print("\n" + "="*80)
        print("RÉSUMÉ DE L'EXÉCUTION")
        print("="*80)
        
        print(f"\nÉtapes complétées ({len(self.etapes_completees)}) :")
        for i, etape in enumerate(self.etapes_completees, 1):
            print(f"  {i}. ✓ {etape}")
        
        print("\n" + "="*80)
        print("📂 FICHIERS GÉNÉRÉS")
        print("="*80)
        
        fichiers_importants = [
            ('Dataset brute/uvbf_data.json', 'Données brutes'),
            ('Dataset brute/uvbf_data_annote.json', 'Données annotées'),
            ('Pretraitement/uvbf_data_pretraitement.json', 'Données prétraitées'),
            ('vectorisation/uvbf_tfidf_vectoriseur.pkl', 'Vectoriseur TF-IDF'),
            ('EntrainementModele/modele_sentiment.pkl', 'Modèle entraîné'),
            ('EntrainementModele/resultats/comparaison_modeles.csv', 'Comparaison des modèles'),
            ('evaluation/matrice_confusion.png', 'Matrice de confusion'),
            ('evaluation/rapport_classification.csv', 'Rapport d\'évaluation'),
            ('rapport/rapport_final/rapport_final.txt', 'Rapport final texte'),
            ('rapport/rapport_final/rapport_complet.json', 'Rapport final JSON')
        ]
        
        for chemin, description in fichiers_importants:
            if Path(chemin).exists():
                print(f"  ✓ {description}")
                print(f"    → {chemin}")
        
        print("\n" + "="*80)
        print("✅ PIPELINE TERMINÉ AVEC SUCCÈS !")
        print("="*80)
        print("\nConsultez le rapport final pour les résultats détaillés.")
        print("Fichier : rapport/rapport_final/rapport_final.txt")
        print("="*80 + "\n")
    
    def executer_pipeline_complet(self, mode_annotation='auto'):
        """Exécute le pipeline complet"""
        self.afficher_banniere()
        
        print("🚀 Démarrage du pipeline complet...\n")
        
        # Étape 1: Scraping
        if not self.etape_1_scraping():
            print("\n❌ Échec du scraping. Pipeline arrêté.")
            return False
        
        # Étape 2: Prétraitement
        if not self.etape_2_pretraitement():
            print("\n❌ Échec du prétraitement. Pipeline arrêté.")
            return False
        
        # Étape 3: Annotation
        if not self.etape_3_annotation(mode=mode_annotation):
            print("\n❌ Échec de l'annotation. Pipeline arrêté.")
            return False
        
        # Étape 4: Vectorisation
        if not self.etape_4_vectorisation():
            print("\n❌ Échec de la vectorisation. Pipeline arrêté.")
            return False
        
        # Étape 5: Entraînement
        if not self.etape_5_entrainement():
            print("\n❌ Échec de l'entraînement. Pipeline arrêté.")
            return False
        
        # Étape 6: BERT (optionnel)
        self.etape_6_bert()
        
        # Étape 7: Évaluation
        if not self.etape_7_evaluation():
            print("\n❌ Échec de l'évaluation. Pipeline arrêté.")
            return False
        
        # Étape 8: Rapport final
        self.etape_8_rapport()
        
        # Résumé
        self.afficher_resume()
        
        return True


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description='Pipeline complet d\'analyse de sentiment UVBF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py --complet                    # Exécuter le pipeline complet
  python main.py --complet --bert             # Avec amélioration BERT
  python main.py --etape scraping             # Exécuter une étape spécifique
  python main.py --etape annotation --manuel  # Annotation manuelle
        """
    )
    
    parser.add_argument('--complet', action='store_true',
                       help='Exécuter le pipeline complet')
    parser.add_argument('--etape', type=str,
                       choices=['scraping', 'pretraitement', 'annotation', 
                               'vectorisation', 'entrainement', 'bert', 
                               'evaluation', 'rapport'],
                       help='Exécuter une étape spécifique')
    parser.add_argument('--bert', action='store_true',
                       help='Inclure l\'amélioration avec BERT')
    parser.add_argument('--manuel', action='store_true',
                       help='Utiliser l\'annotation manuelle (au lieu d\'auto)')
    parser.add_argument('--demo', action='store_true', default=True,
                       help='Mode démonstration (données fictives)')
    
    args = parser.parse_args()
    
    # Créer le pipeline
    pipeline = PipelineUVBF(mode_demo=args.demo, utiliser_bert=args.bert)
    
    if args.complet:
        # Exécuter le pipeline complet
        mode_annotation = 'manuel' if args.manuel else 'auto'
        pipeline.executer_pipeline_complet(mode_annotation=mode_annotation)
    
    elif args.etape:
        # Exécuter une étape spécifique
        pipeline.afficher_banniere()
        
        if args.etape == 'scraping':
            pipeline.etape_1_scraping()
        elif args.etape == 'pretraitement':
            pipeline.etape_2_pretraitement()
        elif args.etape == 'annotation':
            mode = 'manuel' if args.manuel else 'auto'
            pipeline.etape_3_annotation(mode=mode)
        elif args.etape == 'vectorisation':
            pipeline.etape_4_vectorisation()
        elif args.etape == 'entrainement':
            pipeline.etape_5_entrainement()
        elif args.etape == 'bert':
            pipeline.etape_6_bert()
        elif args.etape == 'evaluation':
            pipeline.etape_7_evaluation()
        elif args.etape == 'rapport':
            pipeline.etape_8_rapport()
    
    else:
        # Afficher l'aide si aucun argument
        pipeline.afficher_banniere()
        print("Aucune option spécifiée. Utilisez --help pour voir les options.\n")
        print("🚀 Options rapides :")
        print("  python main.py --complet        # Exécuter tout le pipeline")
        print("  python main.py --help           # Voir toutes les options")
        print()


if __name__ == "__main__":
    main()


