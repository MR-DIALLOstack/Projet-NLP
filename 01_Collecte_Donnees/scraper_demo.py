"""
Script de Démonstration - Scraping UVBF

⚠️ ATTENTION : Ce script est fourni à TITRE DE DÉMONSTRATION uniquement.

En raison des restrictions d'accès aux API des plateformes sociales :
- Twitter/X : Nécessite un compte développeur payant ($100+/mois)
- Facebook : Processus d'approbation complexe et restrictions strictes
- Instagram : API limitée, accès restreint
- TikTok : Pas d'API publique accessible

Les données réelles ont été COLLECTÉES MANUELLEMENT en respectant :
✅ Les conditions d'utilisation des plateformes
✅ La vie privée des utilisateurs (anonymisation)
✅ Les règles éthiques de la recherche académique

Ce script permet de :
1. Générer des données fictives pour tester le pipeline
2. Montrer comment le code fonctionnerait avec un accès API complet
3. Servir de référence pour une future intégration API
"""

import json
import os
from datetime import datetime, timedelta
import random
from pathlib import Path


class GenerateurDonneesDemo:
    """Générateur de données de démonstration pour tester le pipeline"""
    
    def __init__(self, chemin_sortie='uvbf_data.json'):
        """
        Initialise le générateur
        
        Args:
            chemin_sortie: Chemin où sauvegarder les données générées
        """
        self.chemin_sortie = chemin_sortie
        self.donnees = []
        
        # Templates de publications (inspirés de vraies publications)
        self.templates = {
            'positif': [
                "Excellent programme de formation à l'UVBF ! Je recommande vivement.",
                "Les cours en ligne de l'UVBF sont de très bonne qualité.",
                "Merci à l'UVBF pour cette opportunité d'apprentissage accessible.",
                "Fier d'étudier à l'UVBF, une institution innovante.",
                "La plateforme d'e-learning de l'UVBF est très bien conçue.",
                "Je viens de terminer ma formation à l'UVBF et je suis très satisfait !",
                "L'UVBF offre une excellente flexibilité pour les étudiants travailleurs.",
                "Bravo à l'équipe de l'UVBF pour la qualité des enseignements.",
                "Super expérience d'apprentissage à l'UVBF, les professeurs sont compétents.",
            ],
            'negatif': [
                "Problèmes de connexion récurrents sur la plateforme UVBF...",
                "Les frais d'inscription à l'UVBF sont trop élevés.",
                "Déçu par le manque de support technique à l'UVBF.",
                "La qualité de certains cours à l'UVBF laisse à désirer.",
                "Trop de bugs sur le site de l'UVBF, c'est frustrant.",
                "Les délais de correction des devoirs à l'UVBF sont trop longs.",
                "Manque de communication entre l'administration et les étudiants à l'UVBF.",
                "Difficile de joindre le service client de l'UVBF.",
            ],
            'neutre': [
                "Inscription ouverte à l'UVBF pour la rentrée prochaine.",
                "L'UVBF propose des formations en ligne dans plusieurs domaines.",
                "Comment s'inscrire à l'UVBF ? Quelqu'un peut m'aider ?",
                "Réunion d'information à l'UVBF ce samedi.",
                "L'UVBF c'est l'Université Virtuelle du Burkina Faso.",
                "Quelqu'un étudie à l'UVBF ici ? J'aimerais avoir des retours.",
                "L'UVBF organise une journée portes ouvertes ce mois-ci.",
                "Quelles sont les filières disponibles à l'UVBF ?",
            ]
        }
        
        self.auteurs = [
            'Ouédraogo', 'Traoré', 'Kaboré', 'Sawadogo', 'Compaoré', 
            'Nikièma', 'Zongo', 'Ilboudo', 'Barry', 'Sana',
            'Ouattara', 'Diallo', 'Koné', 'Tapsoba', 'Bila'
        ]
        
        self.prenoms = [
            'Aminata', 'Ibrahim', 'Fatou', 'Moussa', 'Aïcha', 
            'Seydou', 'Salimata', 'Abdoul', 'Mariam', 'Hamidou',
            'Fanta', 'Boureima', 'Rasmata', 'Souleymane', 'Awa'
        ]
        
        self.plateformes = ['Twitter', 'Facebook', 'Instagram', 'TikTok']
        self.hashtags = ['#UVBF', '#UniversitéVirtuelle', '#BurkinaFaso', '#Formation']
    
    def generer_donnees(self, nombre=300):
        """
        Génère des données de démonstration
        
        Args:
            nombre: Nombre de publications à générer
        """
        print("="*70)
        print("GÉNÉRATION DE DONNÉES DE DÉMONSTRATION")
        print("="*70)
        print("\n⚠️  Ces données sont FICTIVES et générées automatiquement")
        print("⚠️  Les vraies données ont été collectées MANUELLEMENT\n")
        
        date_debut = datetime.now() - timedelta(days=270)  # 9 mois
        
        for i in range(nombre):
            # Choisir un type de sentiment aléatoire
            sentiment_type = random.choice(['positif', 'negatif', 'neutre'])
            texte = random.choice(self.templates[sentiment_type])
            
            # Choisir une plateforme avec distribution réaliste
            plateforme = random.choices(
                self.plateformes,
                weights=[40, 40, 15, 5],  # Twitter, FB, Insta, TikTok
                k=1
            )[0]
            
            publication = {
                'id': f"DEMO_{i:04d}",
                'auteur': f"{random.choice(self.prenoms)} {random.choice(self.auteurs)}",
                'plateforme': plateforme,
                'texte': texte,
                'date_publication': (date_debut + timedelta(days=random.randint(0, 270))).strftime('%Y-%m-%d %H:%M:%S'),
                'hashtags': random.sample(self.hashtags, k=random.randint(1, 3)),
                'likes': random.randint(5, 200),
                'retweets_partages': random.randint(0, 100),
                'commentaires': random.randint(0, 50)
            }
            
            self.donnees.append(publication)
        
        print(f"✓ {len(self.donnees)} publications générées")
    
    def sauvegarder(self):
        """Sauvegarde les données générées"""
        with open(self.chemin_sortie, 'w', encoding='utf-8') as f:
            json.dump(self.donnees, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Données sauvegardées dans : {self.chemin_sortie}")
    
    def afficher_statistiques(self):
        """Affiche les statistiques des données générées"""
        import pandas as pd
        
        df = pd.DataFrame(self.donnees)
        
        print("\n" + "="*70)
        print("STATISTIQUES DES DONNÉES GÉNÉRÉES")
        print("="*70)
        
        print(f"\nNombre total : {len(df)}")
        print(f"\nRépartition par plateforme :")
        print(df['plateforme'].value_counts())
        
        print(f"\nMoyennes d'engagement :")
        print(f"  Likes : {df['likes'].mean():.1f}")
        print(f"  Partages : {df['retweets_partages'].mean():.1f}")
        print(f"  Commentaires : {df['commentaires'].mean():.1f}")
        
        print("="*70)


def main():
    """Fonction principale"""
    print("\n" + "="*70)
    print("SCRIPT DE DÉMONSTRATION - GÉNÉRATION DE DONNÉES UVBF")
    print("="*70)
    print("\n📌 IMPORTANT :")
    print("  - Ces données sont FICTIVES")
    print("  - Pour le projet réel, les données ont été collectées MANUELLEMENT")
    print("  - Les API des réseaux sociaux sont devenues inaccessibles/payantes")
    print("="*70 + "\n")
    
    # Créer le générateur
    generateur = GenerateurDonneesDemo()
    
    # Générer les données
    generateur.generer_donnees(nombre=300)
    
    # Afficher les statistiques
    generateur.afficher_statistiques()
    
    # Sauvegarder
    generateur.sauvegarder()
    
    print("\n✅ Génération terminée !")
    print("\n📌 Prochaines étapes :")
    print("  1. Annoter les sentiments : cd ../02_Annotation && python annotation_manuelle.py")
    print("  2. Prétraiter les données : cd ../03_Pretraitement && python pretraitement.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

