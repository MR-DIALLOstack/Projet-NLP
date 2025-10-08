"""
Module d'annotation manuelle des sentiments
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import pandas as pd


class AnnotateurSentiment:
    """Outil d'annotation de sentiments"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.projet_dir = self.script_dir.parent
        self.chemin_entree = self.projet_dir / '01_Collecte_Donnees' / 'uvbf_data.json'
        self.chemin_sortie = self.script_dir / 'uvbf_data_annote.json'
        self.donnees = []
    
    def charger_donnees(self):
        """Charge les données à annoter"""
        if self.chemin_sortie.exists():
            # Charger les données déjà annotées
            with open(self.chemin_sortie, 'r', encoding='utf-8') as f:
                self.donnees = json.load(f)
        elif self.chemin_entree.exists():
            # Charger les données originales
            with open(self.chemin_entree, 'r', encoding='utf-8') as f:
                self.donnees = json.load(f)
        else:
            raise FileNotFoundError(f"Fichier non trouvé : {self.chemin_entree}")
        
        print(f"✓ {len(self.donnees)} publications chargées")
    
    def afficher_statistiques(self):
        """Affiche les statistiques"""
        annotes = [d for d in self.donnees if 'sentiment' in d]
        
        print("\n" + "="*60)
        print("STATISTIQUES D'ANNOTATION")
        print("="*60)
        print(f"Total de publications : {len(self.donnees)}")
        print(f"Publications annotées : {len(annotes)}")
        print(f"Publications non annotées : {len(self.donnees) - len(annotes)}")
        
        if annotes:
            df = pd.DataFrame(annotes)
            stats = df['sentiment'].value_counts()
            print("\nRépartition des sentiments annotés :")
            for sentiment, count in stats.items():
                pct = (count / len(annotes)) * 100
                print(f"  {sentiment.capitalize()}: {count} ({pct:.1f}%)")
        
        print("="*60)
    
    def annoter_manuel(self, nombre=50):
        """Annotation manuelle interactive"""
        print("\n" + "="*60)
        print("ANNOTATION MANUELLE")
        print("="*60)
        print("Instructions :")
        print("  [p] = Positif")
        print("  [n] = Négatif")
        print("  [e] = nEutre")
        print("  [s] = Sauter")
        print("  [q] = Quitter")
        print("="*60)
        
        annotes = 0
        for i, item in enumerate(self.donnees):
            if 'sentiment' in item:
                continue
            
            if annotes >= nombre:
                break
            
            print(f"\n[{i+1}/{len(self.donnees)}] " + "-"*50)
            print(f"Texte : {item.get('texte', '')}")
            print("-"*50)
            
            while True:
                choix = input("Sentiment [p/n/e/s/q] : ").lower().strip()
                
                if choix == 'q':
                    self.sauvegarder()
                    return
                elif choix == 's':
                    break
                elif choix == 'p':
                    item['sentiment'] = 'positif'
                    item['date_annotation'] = datetime.now().isoformat()
                    annotes += 1
                    print("✓ Positif")
                    break
                elif choix == 'n':
                    item['sentiment'] = 'negatif'
                    item['date_annotation'] = datetime.now().isoformat()
                    annotes += 1
                    print("✓ Négatif")
                    break
                elif choix == 'e':
                    item['sentiment'] = 'neutre'
                    item['date_annotation'] = datetime.now().isoformat()
                    annotes += 1
                    print("✓ Neutre")
                    break
            
            if annotes > 0 and annotes % 20 == 0:
                self.sauvegarder()
                print(f"\n💾 Sauvegarde automatique ({annotes} annotations)")
        
        if annotes > 0:
            self.sauvegarder()
            print(f"\n✓ {annotes} nouvelles annotations")
    
    def annoter_automatique(self, nombre=300):
        """Annotation automatique pour démonstration"""
        print("\n⚠️  MODE DÉMONSTRATION - Annotation automatique basique")
        print("Pour un projet réel, utilisez annoter_manuel() à la place\n")
        
        mots_positifs = ['excellent', 'super', 'génial', 'parfait', 'bravo', 'merci', 
                        'formidable', 'content', 'satisfait', 'motivé', 'qualité',
                        'bon', 'bien', 'meilleur']
        
        mots_negatifs = ['mauvais', 'nul', 'problème', 'difficile', 'échec', 'déçu',
                        'insatisfait', 'pire', 'insuffisant', 'manque', 'lent', 'cher']
        
        annotes = 0
        for item in self.donnees[:nombre]:
            if 'sentiment' in item:
                continue
            
            texte_lower = item.get('texte', '').lower()
            score_pos = sum(1 for mot in mots_positifs if mot in texte_lower)
            score_neg = sum(1 for mot in mots_negatifs if mot in texte_lower)
            
            if score_pos > score_neg:
                item['sentiment'] = 'positif'
            elif score_neg > score_pos:
                item['sentiment'] = 'negatif'
            else:
                item['sentiment'] = 'neutre'
            
            item['date_annotation'] = datetime.now().isoformat()
            annotes += 1
        
        self.sauvegarder()
        print(f"✓ {annotes} publications annotées automatiquement")
    
    def sauvegarder(self):
        """Sauvegarde les annotations"""
        with open(self.chemin_sortie, 'w', encoding='utf-8') as f:
            json.dump(self.donnees, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Annotations sauvegardées dans : {self.chemin_sortie}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['manuel', 'auto', 'stats'], default='stats')
    parser.add_argument('--nombre', type=int, default=100)
    args = parser.parse_args()
    
    annotateur = AnnotateurSentiment()
    annotateur.charger_donnees()
    
    if args.mode == 'manuel':
        annotateur.annoter_manuel(nombre=args.nombre)
        annotateur.afficher_statistiques()
    elif args.mode == 'auto':
        annotateur.annoter_automatique(nombre=args.nombre)
        annotateur.afficher_statistiques()
    elif args.mode == 'stats':
        annotateur.afficher_statistiques()


if __name__ == "__main__":
    main()