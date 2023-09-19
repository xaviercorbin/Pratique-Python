
# Bonjour, mon nom est Xavier. Qui êtes-vous?
# impartissons avalasses compensassions accolé interprété testerons éternuons écorée sous-exploitée catéchisée monétisâtes garde-à-vous savane contrevînt glanant cônes staffes cytogénétiques piaillâtes raccoutumai
# «ÜÞËáéÛÙÓ×ÑÜÆßßÊxÄåÖÕ×

# 5.3 Question 3 - programme principal :


import random

# Fonction pour générer la clé
def générer_clé(source="liste_mots.txt", longueur=20, encoding="utf-8"):
    with open(source, 'r', encoding=encoding) as f:
        mots = f.read().split()
    
    # Sélectionne aléatoirement des mots jusqu'à la longueur spécifiée
    mots_clé = random.sample(mots, longueur)
    return ' '.join(mots_clé)  # Retourner directement le résultat

# Fonction encrypter
def encrypter(message, clé):
    n = len(clé)
    unicode_clé = [ord(c) for c in clé]
    unicode_message = [ord(m) for m in message]
    message_encrypté_unicodes = [(unicode_message[i] + unicode_clé[i % n]) for i in range(len(unicode_message))]
    return ''.join([chr(uc) for uc in message_encrypté_unicodes])

# Fonction décrypter
def décrypter(message_encrypté, clé):
    n = len(clé)
    unicode_clé = [ord(c) for c in clé]
    unicode_message_encrypté = [ord(m) for m in message_encrypté]
    
    # Ajout d'une opération modulo 0x110000 pour rester dans une plage valide
    message_original_unicodes = [((unicode_message_encrypté[i] - unicode_clé[i % n]) % 0x110000) for i in range(len(unicode_message_encrypté))]
    return ''.join([chr(uc) for uc in message_original_unicodes])

# Fonction pour choisir d'encrypter
def choix_utilisateur_encrypter():
    print("Très bien ! je vais vous aider à encrypter votre message secret")
    choix = input(f'Désirez-vous générer une clé de cryptage dynamiquement ou en composer une vous-même?\n       - Taper "g" pour générer une clé,\n       - Taper "c" pour composer votre clé\n')
    
    if choix == 'g':
        clé = générer_clé()  # Stocker la clé générée
    elif choix == 'c':
        clé = input('Inscrire une phrase qui servira de clé secrète : ')
        while not clé:
            print("La clé doit être composé d'au moins un caractère!\n")
            clé = input('Inscrire une phrase qui servira de clé secrète : ')
    else:
        print(f"Le choix inscrit '{choix}' n'est pas valide. Les seuls choix possibles sont 'g' et 'c'.\n")
        return
    
    message_à_encrypter = input('\n\nInscrire le message que vous aimeriez encrypter : ')
    message_encrypté = encrypter(message_à_encrypter, clé)
    print(f'Voici le message encrypté :\n       {message_encrypté}')
    print(f'Voici la clé qui servira à décrypter le message :\n       {clé}')

# Fonction pour choisir de décrypter
def choix_utilisateur_decrypter():
    clé = input('Très bien ! Inscrire la phrase qui a servi de clé secrète : ')
    while not clé:
        print("\nLa clé doit être composé d'au moins un caractère!\n")
        clé = input('Inscrire la phrase qui a servi de clé secrète : ')
    message_encrypté = input('\nInscrire le message que vous aimeriez décrypter : ')
    message_original = décrypter(message_encrypté, clé)
    print(f'Voici le message décrypté :\n       {message_original}\nAu revoir!')

# Partir le programme
while True:
    choix = input(f'\nQuelle action désirez-vous réaliser ?\n       - Taper "e" pour encrypter un message,\n       - Taper "d" pour decrypter un message\n')
    if choix == 'e':
        choix_utilisateur_encrypter()
    elif choix == 'd':
        choix_utilisateur_decrypter()
    else:
        print(f"Le choix inscrit '{choix}' n'est pas valide. Les seuls choix possibles sont 'e' et 'd'.")