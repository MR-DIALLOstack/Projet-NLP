import pandas as pd
import json
import random
from datetime import datetime, timedelta

# Charger les données existantes
with open('uvbf_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Listes pour générer des noms d'utilisateurs réalistes
prenoms = ["Abdoul", "Fatima", "Moussa", "Aminata", "Ibrahim", "Aïcha", "Ousmane", "Mariama", 
           "Souleymane", "Fatoumata", "Amadou", "Kadiatou", "Boureima", "Salimata", "Issouf",
           "Rasmata", "Adama", "Bintou", "Seydou", "Hawa", "Mamadou", "Awa", "Yacouba", 
           "Assétou", "Zakaria", "Djénéba", "Karim", "Safiatou", "Hamidou", "Mariam"]

noms = ["Traoré", "Ouédraogo", "Sawadogo", "Kaboré", "Compaoré", "Zoungrana", "Zongo",
        "Ouattara", "Sanogo", "Diallo", "Barry", "Sow", "Touré", "Koné", "Camara", 
        "Cissé", "Sana", "Yé", "Ilboudo", "Nikièma", "Barro", "Tapsoba", "Bancé"]

plateformes = ["Twitter", "Facebook"]

def generer_nom_utilisateur():
    """Génère un nom d'utilisateur réaliste"""
    prenom = random.choice(prenoms)
    nom = random.choice(noms)
    
    formats = [
        f"{prenom}{nom}",
        f"{prenom}_{nom}",
        f"{prenom}.{nom}",
        f"{prenom}{random.randint(10, 99)}",
        f"{nom}{prenom}",
        f"{prenom[0]}{nom}"
    ]
    return random.choice(formats)

def generer_date_aleatoire(date_debut, date_fin):
    """Génère une date aléatoire entre deux dates"""
    delta = date_fin - date_debut
    random_days = random.randint(0, delta.days)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    
    return date_debut + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)

# Préparer les données pour le dataset
dataset = []
date_debut = datetime(2025, 9, 1)
date_fin = datetime(2025, 9, 21)

# Limiter à 540 posts maximum
posts_a_generer = min(540, len(data))

for i in range(posts_a_generer):
    entry = data[i]
    
    # Extraire le texte (en priorisant la première question)
    texte = entry.get("Qu'est-ce que vous appréciez le plus à l'UV-BF ?", "")
    
    # Si le texte est vide ou trop court, utiliser la deuxième question
    if not texte or len(texte) < 10:
        texte = entry.get("Quelles sont les principales difficultés ou aspects négatifs que vous rencontrez à l'UV-BF ?", "")
    
    # Si toujours vide, passer
    if not texte or len(texte) < 10:
        continue
    
    # Générer les métadonnées
    post = {
        "id": f"UVBF_{i+1:04d}",
        "auteur": generer_nom_utilisateur(),
        "plateforme": random.choice(plateformes),
        "texte": texte,
        "date_publication": generer_date_aleatoire(date_debut, date_fin).strftime("%Y-%m-%d %H:%M:%S"),
        "hashtags": random.choice([
            ["#UVBF", "#UniversitéVirtuelle"],
            ["#UVBF", "#BurkinaFaso"],
            ["#UVBF"],
            ["#UniversitéVirtuelle", "#UVBF", "#Education"],
            []
        ]),
        "likes": random.randint(0, 150),
        "retweets_partages": random.randint(0, 50) if random.choice(plateformes) == "Twitter" else random.randint(0, 30),
        "commentaires": random.randint(0, 25)
    }
    
    dataset.append(post)

# Trier par date
dataset.sort(key=lambda x: x['date_publication'])

# Sauvegarder en JSON
with open('uvbf_dataset_social_media.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

# Sauvegarder en CSV
df = pd.DataFrame(dataset)
df.to_csv('uvbf_dataset_social_media.csv', index=False, encoding='utf-8')

print(f"✓ Dataset créé avec {len(dataset)} publications")
print(f"✓ Période : {date_debut.strftime('%Y-%m-%d')} à {date_fin.strftime('%Y-%m-%d')}")
print(f"✓ Fichiers générés :")
print(f"  - uvbf_dataset_social_media.json")
print(f"  - uvbf_dataset_social_media.csv")

# Statistiques
twitter_count = sum(1 for p in dataset if p['plateforme'] == 'Twitter')
facebook_count = sum(1 for p in dataset if p['plateforme'] == 'Facebook')

print(f"\n📊 STATISTIQUES :")
print(f"  - Twitter : {twitter_count} posts")
print(f"  - Facebook : {facebook_count} posts")
print(f"  - Total : {len(dataset)} posts")