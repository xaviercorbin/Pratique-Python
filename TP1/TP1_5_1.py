# 5.1 Question 1 - fonctions encrypter et décrypter

# Fonction encrypter
def encrypter(message, clé):
    # Calculer la longueur de la clé
    n = len(clé)
    
    # Convertir la clé et le message en codes Unicode
    unicode_clé = [ord(c) for c in clé]
    unicode_message = [ord(m) for m in message]
    
    # Créer un tableau pour stocker les codes Unicode du message crypté
    message_encrypté_unicodes = []
    
    # Pour chaque caractère du message, ajouter le code Unicode de la clé correspondante
    for i in range(len(unicode_message)):
        message_encrypté_unicodes.append(unicode_message[i] + unicode_clé[i % n])
    
    # Convertir les codes Unicode cryptés en caractères
    message_encrypté = ''.join([chr(uc) for uc in message_encrypté_unicodes])

    return message_encrypté


# Fonction décrypter
def décrypter(message_encrypté, clé):
    # Calculer la longueur de la clé
    n = len(clé)
    
    # Convertir la clé et le message crypté en codes Unicode
    unicode_clé = [ord(c) for c in clé]
    unicode_message_encrypté = [ord(m) for m in message_encrypté]
    
    # Créer un tableau pour stocker les codes Unicode du message original
    message_original_unicodes = []
    
    # Pour chaque caractère du message crypté, soustraire le code Unicode de la clé correspondante
    for i in range(len(unicode_message_encrypté)):
        message_original_unicodes.append(unicode_message_encrypté[i] - unicode_clé[i % n])
    
    # Convertir les codes Unicode originaux en caractères
    message_original = ''.join([chr(uc) for uc in message_original_unicodes])

    return message_original

# Définir la clé et le message
clé = "La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre."
message = "Bonjour Alice, je m'appelle Bob. Je suis également inscrit au cours TECH20704 cet Automne. J'aime beaucoup ce cours, on y apprend beaucoup de concepts intéressants. En plus, le langage Python qui y est étudié est très populaire et largement utilisé ..."

# Cryptage du message
message_encrypté = encrypter(message, clé)
print(f"\nLe texte codé est : \n{message_encrypté}")

# Décryptage du message
message_décrypté = décrypter(message_encrypté, clé)
print(f"\nLe texte décodé est : \n{message_décrypté}")

# Vérifier que le texte original est égale au texte décodé
print("\nLe texte décodé est égal au texte original : {0}".format(message_décrypté == message))