"""
Génération du Rapport Final du Projet
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


class GenerateurRapport:
    """Générateur de rapport final"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.projet_dir = self.script_dir.parent
        self.dossier_sortie = self.script_dir / 'rapport_final'
        self.dossier_sortie.mkdir(parents=True, exist_ok=True)
        
        self.rapport = {
            'date_generation': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sections': {}
        }
    
    def analyser_donnees(self):
        """Analyse les données et annotations"""
        print("\n📊 Analyse des données...")
        
        # Données annotées
        chemin = self.projet_dir / '02_Annotation' / 'uvbf_data_annote.json'
        with open(chemin, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        
        donnees_annotees = [d for d in donnees if 'sentiment' in d]
        df = pd.DataFrame(donnees_annotees)
        
        # Statistiques
        stats = df['sentiment'].value_counts(normalize=True) * 100
        
        self.rapport['sections']['donnees'] = {
            'total': len(donnees),
            'annotees': len(donnees_annotees),
            'sentiments': {
                'positif': float(stats.get('positif', 0)),
                'negatif': float(stats.get('negatif', 0) + stats.get('négatif', 0)),
                'neutre': float(stats.get('neutre', 0))
            }
        }
        
        print(f"  ✓ {len(donnees_annotees)} publications annotées")
        print(f"  ✓ Positif: {stats.get('positif', 0):.1f}%")
        print(f"  ✓ Négatif: {stats.get('negatif', 0) + stats.get('négatif', 0):.1f}%")
    
    def analyser_performances(self):
        """Analyse les performances des modèles"""
        print("\n📊 Analyse des performances...")
        
        chemin = self.projet_dir / '05_Entrainement' / 'resultats' / 'comparaison_modeles.csv'
        if chemin.exists():
            df = pd.read_csv(chemin)
            meilleur = df.loc[df['Score Test'].idxmax()]
            
            self.rapport['sections']['performance'] = {
                'meilleur_modele': str(meilleur['Modèle']),
                'exactitude': float(meilleur['Score Test'])
            }
            
            print(f"  ✓ Meilleur modèle: {meilleur['Modèle']}")
            print(f"  ✓ Exactitude: {meilleur['Score Test']:.2%}")
    
    def generer_rapport_texte(self):
        """Génère le rapport au format texte"""
        lignes = []
        lignes.append("="*70)
        lignes.append("RAPPORT FINAL - ANALYSE DE SENTIMENT UVBF")
        lignes.append("="*70)
        lignes.append(f"\nDate : {self.rapport['date_generation']}")
        
        # Section Données
        if 'donnees' in self.rapport['sections']:
            d = self.rapport['sections']['donnees']
            lignes.append("\n" + "-"*70)
            lignes.append("1. DONNÉES COLLECTÉES ET ANNOTÉES")
            lignes.append("-"*70)
            lignes.append(f"Total de publications : {d['total']}")
            lignes.append(f"Publications annotées : {d['annotees']}")
            lignes.append("\nRépartition des sentiments :")
            lignes.append(f"  Positif : {d['sentiments']['positif']:.1f}%")
            lignes.append(f"  Négatif : {d['sentiments']['negatif']:.1f}%")
            lignes.append(f"  Neutre  : {d['sentiments']['neutre']:.1f}%")
            lignes.append(f"\n📊 TAUX DE COMMENTAIRES SUR L'UVBF:")
            lignes.append(f"  ✓ Positifs: {d['sentiments']['positif']:.1f}%")
            lignes.append(f"  ✗ Négatifs: {d['sentiments']['negatif']:.1f}%")
        
        # Section Performance
        if 'performance' in self.rapport['sections']:
            p = self.rapport['sections']['performance']
            lignes.append("\n" + "-"*70)
            lignes.append("2. PERFORMANCE DU MODÈLE")
            lignes.append("-"*70)
            lignes.append(f"Meilleur modèle : {p['meilleur_modele']}")
            lignes.append(f"Exactitude : {p['exactitude']:.2%}")
        
        lignes.append("\n" + "-"*70)
        lignes.append("3. RECOMMANDATIONS")
        lignes.append("-"*70)
        lignes.append("\nPoints forts identifiés :")
        lignes.append("  ✓ Qualité de l'enseignement")
        lignes.append("  ✓ Flexibilité de la formation")
        lignes.append("  ✓ Innovation pédagogique")
        lignes.append("\nAxes d'amélioration :")
        lignes.append("  • Infrastructure technique (priorité haute)")
        lignes.append("  • Accessibilité financière (priorité moyenne)")
        lignes.append("  • Support client (priorité moyenne)")
        
        lignes.append("\n" + "="*70)
        lignes.append("FIN DU RAPPORT")
        lignes.append("="*70)
        
        rapport_texte = "\n".join(lignes)
        
        # Sauvegarder
        with open(self.dossier_sortie / 'rapport_final.txt', 'w', encoding='utf-8') as f:
            f.write(rapport_texte)
        
        print(f"\n✓ Rapport texte : {self.dossier_sortie}/rapport_final.txt")
        
        return rapport_texte
    
    def sauvegarder_json(self):
        """Sauvegarde le rapport au format JSON"""
        with open(self.dossier_sortie / 'rapport_complet.json', 'w', encoding='utf-8') as f:
            json.dump(self.rapport, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Rapport JSON : {self.dossier_sortie}/rapport_complet.json")


def main():
    print("\n" + "="*70)
    print("GÉNÉRATION DU RAPPORT FINAL")
    print("="*70)
    
    generateur = GenerateurRapport()
    
    # Analyser
    generateur.analyser_donnees()
    generateur.analyser_performances()
    
    # Générer
    generateur.generer_rapport_texte()
    generateur.sauvegarder_json()
    
    print("\n" + "="*70)
    print("✅ RAPPORT FINAL GÉNÉRÉ")
    print("="*70)
    print("\nConsultez :")
    print(f"  - {generateur.dossier_sortie}/rapport_final.txt")
    print(f"  - ../RESULTATS.md (résumé)")


if __name__ == "__main__":
    main()