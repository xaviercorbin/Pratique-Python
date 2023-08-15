import sqlite3

print('.                                                       .')
print('---------------------- Bienvenidos ----------------------')
print('.                                                       .')

def ajouter_mot(espagnol, francais):
    conn = sqlite3.connect("espagnol.db")
    cursor = conn.cursor()

    # Vérifier si le mot espagnol existe déjà dans la base de données
    cursor.execute("SELECT * FROM vocabulaire WHERE espagnol = ?", (espagnol,))
    existing_word = cursor.fetchone()

    if existing_word:
        reponse = input(f"Le mot '{espagnol}' existe déjà dans la base de données. Voulez-vous ajouter une signification différente ? (o/n) ")
        if reponse.lower() == 'o':
            nouvelle_signification = input("Entrez la nouvelle signification en français : ")
            if nouvelle_signification.strip():  # Vérifier si la traduction n'est pas vide
                if nouvelle_signification not in existing_word[2]:
                    nouvelle_signification = existing_word[2] + ", " + nouvelle_signification
                    cursor.execute("UPDATE vocabulaire SET français = ? WHERE id = ?", (nouvelle_signification, existing_word[0]))
                    print("Nouvelle signification ajoutée.")
                else:
                    print("Cette signification existe déjà pour ce mot.")
            else:
                print("Traduction manquante. Le mot n'a pas été modifié.")
    else:
        if francais.strip():  # Vérifier si la traduction n'est pas vide
            cursor.execute('''INSERT INTO vocabulaire (espagnol, français) VALUES (?, ?)''', (espagnol, francais))
            print("Mot ajouté à la base de données.")
        else:
            print("Traduction manquante. Le mot n'a pas été ajouté à la base de données.")

    conn.commit()
    conn.close()

def modifier_entree(id_modif, champ_modif, nouvelle_valeur):
    conn = sqlite3.connect("espagnol.db")
    cursor = conn.cursor()

    # Vérifier si l'ID existe dans la base de données
    cursor.execute("SELECT * FROM vocabulaire WHERE id = ?", (id_modif,))
    existing_entry = cursor.fetchone()

    if existing_entry:
        if champ_modif == 1:
            cursor.execute("UPDATE vocabulaire SET espagnol = ? WHERE id = ?", (nouvelle_valeur, id_modif))
        elif champ_modif == 2:
            cursor.execute("UPDATE vocabulaire SET français = ? WHERE id = ?", (nouvelle_valeur, id_modif))
        print("Entrée modifiée.")
    else:
        print("L'ID spécifié n'existe pas dans la base de données.")

    conn.commit()
    conn.close()

def main():
    while True:
        action = input("Que voulez-vous faire? (a pour ajouter, m pour modifier, q pour quitter, b pour menu) : ")
        if action.lower() == 'q':
            break
        elif action.lower() == 'a':
            while True:  # Boucle pour rester dans le mode ajout
                espagnol = input("Entrez le mot en espagnol (ou 'b') : ")
                if espagnol.lower() == 'b':
                    break
                francais = input("Entrez la traduction en français : ")
                ajouter_mot(espagnol, francais)
        elif action.lower() == 'm':
            id_modif = int(input("Entrez l'ID de l'entrée que vous voulez modifier : "))
            champ_modif = int(input("Que voulez-vous modifier? (1 pour espagnol, 2 pour français) : "))
            nouvelle_valeur = input("Entrez la nouvelle valeur : ")
            modifier_entree(id_modif, champ_modif, nouvelle_valeur)
        else:
            print("Action non reconnue. Veuillez réessayer.")

if __name__ == "__main__":
    main()
