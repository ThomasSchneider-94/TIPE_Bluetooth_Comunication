// Rajout de librairies
#include <SoftwareSerial.h>           // Utilisé pour creer un port sérial virtuel
char commande;
boolean NL = true;


// Définition des variables
SoftwareSerial Serial_Virtuel(10,11);  // On crée un port virtuel //Entrée // Sortie


// Fonction de démarrage, s'exécute une seule fois:
void setup() {
  Serial.begin(9600);  //Fixe le débit de communication à 9600 caractères/s
  Serial.println("Entrer les commandes AT:");
  Serial_Virtuel.begin(38400);
  }



 // Fonction principale du programme, séxécute en boucle:
void loop() {
  if (Serial_Virtuel.available())   {
    Serial.write(Serial_Virtuel.read());
    }
  
  if (Serial.available())   {
    commande = Serial.read();
    Serial_Virtuel.write(commande);
    
    if (NL) {Serial.print(">"); NL = false;}
    Serial.write(commande);
    if (commande==10) {NL = true;}
    }
}

// Commandes AT:
// AT : vérifie connexion
// AT+NAME : retourne le nom du module
// AT+UART : retourne la vitesse de dialogue du module
// AT+ADDR : retourne l'adresse du module
// AT+VERSION : retourne la version du module
// AT+ROLE : retourne le role du module (0 si slave,1 si maitre, 2 si les 2)
// AT+RESET : redémarre le module et sortie de AT
// AT+ORGL : restorer le module d'usine
// AT+PSWD : retourne le mot de passe du module
// AT+BIND=adresse,du,slave : permet de se connecter à un module slave
//
// Lycée: 15,83,359db1
