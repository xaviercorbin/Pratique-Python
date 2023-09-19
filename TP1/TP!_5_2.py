from TP1 import liste_mots

import random

def générer_clé(source="liste_mots.txt", longueur=20, encoding="utf-8"):
    with open(source, 'r', encoding=encoding) as f:
        mots = f.read().split()
    
    # Sélectionne aléatoirement des mots jusqu'à la longueur spécifiée
    mots_clé = random.sample(mots, longueur)
    
    return ' '.join(mots_clé)


print(f"Clé générée : \n{générer_clé()}")