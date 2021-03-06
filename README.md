# Snapchat_Forensics

**`Snapchat_Forensics`** est un outil destiné aux experts judiciaires / analystes voir même aux dfir (vecteur d'attaque sur BYOD etc), permettant d'analyser le contenu de l'application **` com.snapchat.android `**

Les outils professionnels classiques ne permettant pas d'exploiter ces données, cet outil permet ainsi d'obtenir un rapport contenant entre autres :
```
- Messages textes 
- Données de localisation, 
- Liste d'amis et +, 
- Bestfriends, 
- Friends blacklistés,
- Activité du compte,
- Memories,
- My Eyes Only
```
Snapchat effectuant des mises à jour régulières de l'app (chaque semaine), quelques changements apparaissent généralement
dans les fichiers xml ou des bases de données.

Quelques ajustations rapides du code seront nécessaires afin de gérer les diverses erreurs rencontrées.

## Fonctionnement

- Extraire le dossier com.snapchat.android et l'insérer à la racine du script avant execution.
- Le rapport Html est ensuite généré à la racine.

## Extraits de résultats

- Apercu général :
![Extrait](https://github.com/Yann-Ntech/Snapchat_Forensics/blob/master/Extraits_R%C3%A9sultats/extrait_1.PNG)

- Messages :
![Extrait](https://github.com/Yann-Ntech/Snapchat_Forensics/blob/master/Extraits_R%C3%A9sultats/extrait_2.PNG)

- Activité :
![Extrait](https://github.com/Yann-Ntech/Snapchat_Forensics/blob/master/Extraits_R%C3%A9sultats/extrait_3.PNG)

- Media :
![Extrait](https://github.com/Yann-Ntech/Snapchat_Forensics/blob/master/Extraits_R%C3%A9sultats/extrait_4.PNG)

- Géolocalisation :
![Extrait](https://github.com/Yann-Ntech/Snapchat_Forensics/blob/master/Extraits_R%C3%A9sultats/extrait_5.PNG)

## Versions compatibles

Version beta testée et fonctionnant sur les versions :

- 10.60.2.0 Beta
- 10.66.5.0

## Fonctionnement Application Snapchat

- Suppression des Snaps : https://support.snapchat.com/fr-FR/a/when-are-snaps-chats-deleted

- Memories : https://support.snapchat.com/fr-FR/a/about-memories

- Me Eyes Only : https://support.snapchat.com/fr-FR/a/about-memories

- Snap : https://support.snapchat.com/fr-FR/article/send-snap

- Best Friends : https://support.snapchat.com/fr-FR/a/best-friends

## Requirements

* lxml
* pillow

## Licence

GNU General Public License v3.0

## Historique & Futures Mises à jour

Snapchat_Forensics est basé sur la future ré-écriture de SQLite_Analyzer, sans y intégrer divers modules.

Plusieurs intégrations sont en cours :

- Ajout des thumbs vidéos dans le rapport via ffmpeg

- Configparser pour mise à jour rapide des requêtes SQL comme pour SQLite_Analyzer 

- Module de recherche de mots clés de SQLite_Analyzer à ré-écrire.

- Argparse si nécessaire

- Prise en charge des anciennes versions utilisant tcspahn.db

## Auteur

Yann-Ntech
Contact : yann.ntech.dev [at] gmail.com
