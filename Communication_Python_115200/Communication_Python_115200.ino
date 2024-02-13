// Rajout de librairies
#include <SoftwareSerial.h>           // Utilisé pour creer un port sérial virtuel
char Donnees_a_envoyer;
char Donnees_recues = "";


// Définition des variables
SoftwareSerial Port_Bluetooth(10,11);  // On crée un port virtuel   //Entrée // Sortie


// Fonction de démarrage, s'exécute une seule fois:
void setup() {
  Serial.begin(9600);
  Port_Bluetooth.begin(115200);
  }



 // Fonction principale du programme, séxécute en boucle:
void loop() {
  // Récepetion/envoi des données
  if (Serial.available()>0){
    Donnees_a_envoyer = Serial.read();
    Port_Bluetooth.write(Donnees_a_envoyer);
    Serial.print(Donnees_a_envoyer);
    }
  
  if (Port_Bluetooth.available()>0){
    Donnees_recues = Port_Bluetooth.read();
    Serial.print(Donnees_recues);
    }
  
  if (Donnees_recues != ""){
    Donnees_recues = "";
    }
}
