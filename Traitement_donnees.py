## Modules

import serial
import random as rd
import time
from numpy import linspace
import matplotlib.pyplot as plt

## Définition des ports

port_envoi = serial.Serial("COM4" , baudrate=9600 , write_timeout = 1)

port_reception = serial.Serial("COM3" , baudrate=9600 , timeout=0.01)

## Ouverture des fichiers

fichier_tps = open("temps.txt", "a")
fichier_err = open("erreur.txt", "a")

## Fonctions

def echange_donnees(donnees):
    """ Entrée: liste de bystes à envoyer par le port_envoie
        Sortie: chaine de caractère contenant tout les bytes reçus par le port_reception"""
    reception = ""

    for i in range(len(donnees)):
        # Envoie
        port_envoi.write(donnees[i])

        # Réception
        lecture = str(port_reception.read())
        if lecture != "b''": # bit 'vide'
            reception += lecture

    return reception


def traitement_retour(str1,str2):
    """ Entrée: str1 --> chaine de caractère de référence
                str2 --> chaine de caractère à comparée avec str1
        Sortie: Nombre d'erreur dans la liste 2"""

    mini , maxi = min(len(str1),len(str2)) , max(len(str1),len(str2))
    erreur = 0
    for i in range(mini):
        if str1[i] != str2[i]:
            erreur += 1
    return erreur + maxi - mini


## Définition des variables

borne_inf = 10
borne_sup = 2000
nb_test = 20
nb_pts = 10

taille = linspace(borne_inf , borne_sup , nb_pts)
for i in range(len(taille)):
    taille[i] = int(taille[i])

temps = [0 for i in range(len(taille))]
erreurs = [0 for i in range(len(taille))]

## Programme

for i in range(len(taille)):
    for j in range(nb_test):

        ## Affichage dans le dossier texte / Shell
        print("Taille {}, Test {} :".format(i,j),taille[i])

        fichier_tps.write("Taille {}, Test {} \n".format(taille[i],j))
        fichier_err.write("Taille {}, Test {} \n".format(taille[i],j))

        ## Création des données

        donnees_utiles = [rd.randbytes(1) for i in range(int(taille[i]))]

        carac_utiles = ""
        for k in range(len(donnees_utiles)):
            carac_utiles += str(donnees_utiles[k])
        fichier_err.write(carac_utiles + "\n\n")

        # On rajoute du 'vide' avant et après les données à envoyer, pour être sûr que tout le message passera (pas de coupure avant ou après)
        donnees_a_envoyer = [b'' for i in range(60)] + donnees_utiles + [b'' for i in range(60)]

        ## Echange de donnees

        debut = time.time()
        recep = echange_donnees(donnees_a_envoyer)
        fin = time.time()

        ## Statistiques de temps

        temps[i] += (fin - debut)/nb_test
        fichier_tps.write(str(fin - debut) + "\n\n")

        ## Traitement du retour

        erreurs[i] += traitement_retour(carac_utiles,recep)/nb_test
        fichier_err.write(recep + "\n\n")

        print(fin - debut , erreurs[i] , "\n")


## Graphiques

plt.figure("Temps de réponse (en s)")
plt.plot(taille[1:],temps[1:])
plt.xlabel("Volume du signal (en bit)")
plt.ylabel("Temps de réponse ")
plt.savefig("Temps.png")
plt.show()



plt.figure("Erreur de transmission")
plt.plot(taille[1:],erreurs[1:])
plt.xlabel("Volume du signal (en bit)")
plt.ylabel("Nombre d'erreur")
plt.savefig("Erreurs.png")
plt.show()

fichier_err.close()
fichier_tps.close()