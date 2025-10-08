"""
Module d'annotation manuelle des sentiments pour le projet UVBF
Permet d'annoter les publications avec des labels : positif, négatif, neutre
"""

import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

class AnnotateurSentiment:
    """Classe pour annoter manuellement les sentiments des publications"""
    
    def __init__(self, chemin_donnees=None, chemin_sauvegarde=None):
        """
        Initialise l'annotateur
        
        Args:
            chemin_donnees: Chemin vers le fichier JSON des données (optionnel)
            chemin_sauvegarde: Chemin pour sauvegarder les annotations (optionnel)
        """
        from pathlib import Path
        
        # Si pas de chemin spécifié, utiliser la nouvelle structure
        if chemin_donnees is None:
            script_dir = Path(__file__).parent
            projet_dir = script_dir.parent
            self.chemin_donnees = str(projet_dir / '01_Collecte_Donnees' / 'uvbf_data.json')
            self.chemin_sauvegarde = str(projet_dir / '02_Annotation' / 'uvbf_data_annote.json')
        else:
            self.chemin_donnees = chemin_donnees
            self.chemin_sauvegarde = chemin_sauvegarde or chemin_donnees.replace('.json', '_annote.json')
        
        self.donnees = self.charger_donnees()
        self.sentiments_valides = ['positif', 'negatif', 'neutre']
        
    def charger_donnees(self):
        """Charge les données depuis le fichier JSON"""
        with open(self.chemin_donnees, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def sauvegarder_annotations(self):
        """Sauvegarde les annotations dans un fichier JSON"""
        with open(self.chemin_sauvegarde, 'w', encoding='utf-8') as f:
            json.dump(self.donnees, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Annotations sauvegardées dans : {self.chemin_sauvegarde}")
    
    def afficher_statistiques(self):
        """Affiche les statistiques d'annotation"""
        annotes = [item for item in self.donnees if 'sentiment' in item]
        non_annotes = len(self.donnees) - len(annotes)
        
        print("\n" + "="*60)
        print("STATISTIQUES D'ANNOTATION")
        print("="*60)
        print(f"Total de publications : {len(self.donnees)}")
        print(f"Publications annotées : {len(annotes)}")
        print(f"Publications non annotées : {non_annotes}")
        
        if annotes:
            sentiments = [item['sentiment'] for item in annotes]
            df_stats = pd.Series(sentiments).value_counts()
            print("\nRépartition des sentiments annotés :")
            for sentiment, count in df_stats.items():
                pourcentage = (count / len(annotes)) * 100
                print(f"  {sentiment.capitalize()}: {count} ({pourcentage:.1f}%)")
        print("="*60)
    
    def annoter_manuel(self, debut=0, fin=None, afficher_contexte=True):
        """
        Lance l'annotation manuelle interactive
        
        Args:
            debut: Index de début
            fin: Index de fin (None = jusqu'à la fin)
            afficher_contexte: Affiche les métadonnées (auteur, plateforme, etc.)
        """
        fin = fin or len(self.donnees)
        print("\n" + "="*60)
        print("ANNOTATION MANUELLE DES SENTIMENTS")
        print("="*60)
        print("Instructions :")
        print("  [p] = Positif")
        print("  [n] = Négatif")
        print("  [e] = Neutre (nEutre)")
        print("  [s] = Sauter")
        print("  [q] = Quitter et sauvegarder")
        print("="*60 + "\n")
        
        annotations_session = 0
        
        for i in range(debut, fin):
            item = self.donnees[i]
            
            # Passer si déjà annoté
            if 'sentiment' in item:
                continue
            
            # Afficher les informations
            print(f"\n[{i+1}/{len(self.donnees)}] " + "-"*50)
            if afficher_contexte:
                print(f"ID: {item.get('id', 'N/A')}")
                print(f"Auteur: {item.get('auteur', 'N/A')}")
                print(f"Plateforme: {item.get('plateforme', 'N/A')}")
                print(f"Date: {item.get('date_publication', 'N/A')}")
            
            print(f"\nTexte : {item.get('texte', '')}")
            print("-"*50)
            
            # Demander l'annotation
            while True:
                choix = input("Sentiment [p/n/e/s/q] : ").lower().strip()
                
                if choix == 'q':
                    print("\nArrêt de l'annotation...")
                    self.sauvegarder_annotations()
                    self.afficher_statistiques()
                    return
                
                elif choix == 's':
                    print("Publication sautée.")
                    break
                
                elif choix == 'p':
                    item['sentiment'] = 'positif'
                    item['date_annotation'] = datetime.now().isoformat()
                    annotations_session += 1
                    print("✓ Annoté comme POSITIF")
                    break
                
                elif choix == 'n':
                    item['sentiment'] = 'negatif'
                    item['date_annotation'] = datetime.now().isoformat()
                    annotations_session += 1
                    print("✓ Annoté comme NÉGATIF")
                    break
                
                elif choix == 'e':
                    item['sentiment'] = 'neutre'
                    item['date_annotation'] = datetime.now().isoformat()
                    annotations_session += 1
                    print("✓ Annoté comme NEUTRE")
                    break
                
                else:
                    print("Choix invalide. Utilisez p, n, e, s ou q.")
            
            # Sauvegarde automatique tous les 20 éléments
            if annotations_session > 0 and annotations_session % 20 == 0:
                self.sauvegarder_annotations()
                print(f"\n💾 Sauvegarde automatique effectuée ({annotations_session} annotations)")
        
        # Sauvegarde finale
        if annotations_session > 0:
            self.sauvegarder_annotations()
            print(f"\n✓ {annotations_session} nouvelles annotations effectuées dans cette session")
        
        self.afficher_statistiques()
    
    def annoter_automatique_demo(self, nombre=100):
        """
        Annotation automatique basée sur des mots-clés pour DÉMONSTRATION UNIQUEMENT
        À REMPLACER par une vraie annotation manuelle pour un projet réel
        
        Args:
            nombre: Nombre de publications à annoter automatiquement
        """
        print("\n⚠️  MODE DÉMONSTRATION - Annotation automatique basique")
        print("Pour un projet réel, utilisez annoter_manuel() à la place\n")
        
        # Listes de mots-clés pour classification simple
        mots_positifs = [
            'excellent', 'super', 'génial', 'parfait', 'bravo', 'merci', 
            'formidable', 'content', 'satisfait', 'motivé', 'qualité',
            'bon', 'bien', 'meilleur', 'apprécier', 'heureux', 'félicitations'
        ]
        
        mots_negatifs = [
            'mauvais', 'nul', 'problème', 'difficile', 'échec', 'déçu',
            'insatisfait', 'pire', 'insuffisant', 'manque', 'erreur',
            'lent', 'compliqué', 'frustrant', 'cher', 'inadapté'
        ]
        
        annotes = 0
        for i, item in enumerate(self.donnees[:nombre]):
            if 'sentiment' in item:
                continue
            
            texte_lower = item.get('texte', '').lower()
            
            # Compter les mots positifs et négatifs
            score_positif = sum(1 for mot in mots_positifs if mot in texte_lower)
            score_negatif = sum(1 for mot in mots_negatifs if mot in texte_lower)
            
            # Classifier
            if score_positif > score_negatif:
                item['sentiment'] = 'positif'
            elif score_negatif > score_positif:
                item['sentiment'] = 'negatif'
            else:
                item['sentiment'] = 'neutre'
            
            item['date_annotation'] = datetime.now().isoformat()
            item['annotation_auto'] = True  # Marquer comme annotation automatique
            annotes += 1
        
        self.sauvegarder_annotations()
        print(f"✓ {annotes} publications annotées automatiquement")
        self.afficher_statistiques()
        print("\n⚠️  N'oubliez pas de vérifier et corriger ces annotations !")


def main():
    """Fonction principale"""
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='Outil d\'annotation de sentiments')
    parser.add_argument('--donnees', type=str, default=None,
                       help='Chemin vers le fichier de données (optionnel, utilise nouvelle structure par défaut)')
    parser.add_argument('--mode', type=str, choices=['manuel', 'auto', 'stats'],
                       default='stats', help='Mode d\'annotation')
    parser.add_argument('--nombre', type=int, default=100,
                       help='Nombre d\'éléments à annoter')
    parser.add_argument('--debut', type=int, default=0,
                       help='Index de début pour annotation manuelle')
    
    args = parser.parse_args()
    
    # Créer l'annotateur (utilise la nouvelle structure si pas de chemin spécifié)
    annotateur = AnnotateurSentiment(args.donnees)
    
    if args.mode == 'manuel':
        annotateur.annoter_manuel(debut=args.debut, fin=args.debut + args.nombre)
    elif args.mode == 'auto':
        annotateur.annoter_automatique_demo(nombre=args.nombre)
    elif args.mode == 'stats':
        annotateur.afficher_statistiques()


if __name__ == "__main__":
    main()


