#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable = C0103, C0301, E0611, E0401

__auteur__ = "Yann-Ntech"
__version__ = "0.2 Beta"
__date__ = "20/09/2018"
__licence__ = "GNU GENERAL PUBLIC LICENSE Version 3"

from os import path
import os.path
from inspect import getsourcefile
from Modules.Recup_messages import table_message
from Modules.Creation_html import Export_html
import datetime
from datetime import datetime
import json
from zipfile import ZipFile 
from lxml import etree
	
if __name__ == '__main__':
      
	print("""Snapchat Forensics
Version 0.2 Beta
Septembre 2019
Author : Yann-Ntech 
Licence : GNU GENERAL PUBLIC LICENSE Version 3

########################################################

Analyse de l'application : com.snapchat.android

- Extraction de la liste d'amis
- Extraction des messages écrits
- Extraction des données d'activité 
- Extraction des données de géolocalisation
- Extraction des données liées aux fichiers medias

########################################################
""")
	print("Début d'Analyse\n\n")
		
	cas = input("N° Cas : ")
	try:
		cas = cas.replace('/','_')
	except:
		pass
	sc = input("Objet : ")
	try:
		sc = sc.replace('/','_')
	except:
		pass
	analyst = input("Analyste : ")	
	unité = input("Service : ")	
	
	## Création du Cas
	
	path_script = path.dirname(path.abspath(getsourcefile(lambda: 0)))
	path_cas = path_script+'\Rapport'
	
	if not os.path.exists(path_cas):				
			
		## Copie des fichiers utiles	
			   
		file = "./main.p"
		zip_destination = './'   
		with ZipFile(file, 'r') as zip:         
			zip.extractall(zip_destination)				
			print('Extraction réussie')
						
		print("Dossier :", path_cas, "créé.")	
		
		### Détection de l'application
		
		path_script = path.dirname(path.abspath(getsourcefile(lambda: 0)))
		path_app = '.\com.snapchat.android'			
		
		### Bases de données Snapchat
			
		# Main.db
		path_main_db = path_app+'\databases\main.db'
		liste_requete_main_db = ['requete_BestFriend', 'requete_BlackListFriend', 'requete_Feed', 'requete_FeedGroupe', 'requete_Friend', 'requete_FriendWhoAddedMe', 'requete_InteractionMessages', 'requete_InteractionMessages', 'requete_Message', 'requete_MessageSnap', 'requete_ProfileSavedMediaMessage', 'requete_SendToLastSnapRecipients', 'requete_NetworkMessage']
		
		# Memories.db 	 
		path_memories_db = path_app+'\databases\memories.db'
		liste_requete_memories_db = ['requete_memories_entry', 'requete_memories_snap_complete', 'requete_memories_snap_simple', 'requete_memories_meo_confidential', 'requete_memories_remote_operation', 'requete_memories_remote_operation_meo', 'requete_memories_upload_status']
		
		# Journal.db
		path_journal_db = path_app+'\databases\journal.db'	
		liste_journal_db = ['requete_media_291', 'requete_media_229', 'requete_media_228', 'requete_media_290']
				
		# Fichiers pas encore exploité - à faire
		path_files = path_script+'\Snapchat'
		
		## Analyse des données de l'application : shared_prefs
		
				# identity_persistent_store.xml
		
		path_shared_prefs = './com.snapchat.android/shared_prefs/'
		identity_persistent_store = path_shared_prefs+'identity_persistent_store.xml'	
		if os.path.isfile(identity_persistent_store) is True:
			print('Fichier identity_persistent_store.xml détecté')	
			print('Parsing du fichier en cours')			
			arbre = etree.parse(identity_persistent_store)
			racine = arbre.getroot()	
			dico_long = {}
			dico_string = {}
			try:
				for noeud in arbre.xpath('/map'):
					for nom in noeud.xpath('long'):
						balise, valeur = nom.get("name"), nom.get("value")
						dico_long[balise] = valeur			
					for nom in noeud.xpath('string'):
						balise, valeur = nom.get("name"), nom.text
						dico_string[balise] = valeur		
			except:
				dico_string['LONG_CLIENT_ID'] = 'Version non prise en charge'
				dico_string['LAST_LOGGED_IN_USERNAME'] = 'Version non prise en charge'
		else:
			print('Fichier identity_persistent_store.xml non détecté')
			dico_long = {}
			dico_string = {}
			dico_string['LONG_CLIENT_ID'] = 'Non renseigné - identity_persistent_store.xml non détecté'
			dico_string['LAST_LOGGED_IN_USERNAME'] = 'Non renseigné - identity_persistent_store.xml non détecté'								
			
				# identity_persistent_store.xml
		user_session = path_shared_prefs+'user_session_shared_pref.xml'	
		if os.path.isfile(user_session) is True:
			print('Fichier user_session_shared_pref.xml détecté')	
			print('Parsing du fichier en cours')		
			arbre = etree.parse(user_session)				
			racine = arbre.getroot()			
			user_dico_long = {}
			user_dico_string = {}
			try:				
				for noeud in arbre.xpath('/map'):
					for nom in noeud.xpath('long'):
						balise, valeur = nom.get("name"), nom.get("value")
						user_dico_long[balise] = valeur			
					for nom in noeud.xpath('string'):
						balise, valeur = nom.get("name"), nom.text
						user_dico_string[balise] = valeur
				timestamp_install = dico_long['INSTALL_ON_DEVICE_TIMESTAMP']
				installation = datetime.fromtimestamp(int(timestamp_install)/1000)
				timestamp_anniv = user_dico_long['key_birthday']
				date_naissance = datetime.fromtimestamp(int(timestamp_anniv)/1000)		
			except:
				user_dico_string['key_display_name'] = 'Version non prise en charge'
				user_dico_string['key_phone'] = 'Version non prise en charge'
				user_dico_string['key_email'] = 'Version non prise en charge'
				user_dico_string['key_ip_based_country_code'] = 'Version non prise en charge'
				dico_long['INSTALL_ON_DEVICE_TIMESTAMP'] = 'Version non prise en charge'
				installation = dico_long['INSTALL_ON_DEVICE_TIMESTAMP']
				user_dico_long['key_birthday'] = 'Version non prise en charge'
				date_naissance = user_dico_long['key_birthday']											
		else:
			print('Fichier user_session_shared_pref.xml non détecté')	
			user_dico_long = {}
			user_dico_string = {}		
			user_dico_string['key_display_name'] = 'Non renseigné - user_session_shared_pref.xml détecté non détecté'	
			user_dico_string['key_phone'] = 'Non renseigné - user_session_shared_pref.xml détecté non détecté'	
			user_dico_string['key_email'] = 'Non renseigné - user_session_shared_pref.xml détecté non détecté'
			user_dico_string['key_ip_based_country_code'] = 'Non renseigné - user_session_shared_pref.xml détecté non détecté'
			dico_long['INSTALL_ON_DEVICE_TIMESTAMP'] = 'Non renseigné - user_session_shared_pref.xml détecté non détecté'
			installation = dico_long['INSTALL_ON_DEVICE_TIMESTAMP']
			user_dico_long['key_birthday'] = 'Non renseigné - user_session_shared_pref.xml détecté non détecté'
			date_naissance = user_dico_long['key_birthday']				
		
			
		## Création du fichier cas.html		
				
		with open("./Rapport/html/cas.html", 'w', encoding='utf-8') as f:
			f.write("""
<html><head><meta charset='UTF-8'><title>Rapport Snapchat Forensics</title>
<link rel="stylesheet" href="css/bootstrap.min.css" />
</head>
<body>
<div class="p-3 mb-2 bg-dark text-white"><h1>Rapport Snapchat Forensics</h1></div>	
<h4>
</br>
<ul>		
	<ol>Numéro de procédure : {0}</ol>
	<ol>Numéro de scellé : {1} </ol>
	<ol>Analyste : {2} </ol>
	<ol>Unité : {3} </ol>
</ul>
</h4>
</br>
	
	
<div class="p-3 mb-2 bg-dark text-white"><h1>Application Snapchat</h1></div>	
<h4>
</br>
<ul>
	<ol>Date d'installation de l'application: {6}	</ol>			
	<ol>Utilisateur enregistré : {5} </ol>
	<ol>Pseudonyme : {7} </ol>
	<ol>ID Utilisateur  : {4}	</ol>
	<ol>Date Naissance  : {10}		</ol>
	<ol>Téléphone : {8} </ol>
	<ol>E-mail : {9} </ol>
	<ol>Pays : {11}</ol>
</ul>	
</h4>
</br>
	
</body>
</html>
	""".format(cas, sc, analyst, unité, dico_string['LONG_CLIENT_ID'], dico_string['LAST_LOGGED_IN_USERNAME'], installation, user_dico_string['key_display_name'], user_dico_string['key_phone'], user_dico_string['key_email'], date_naissance, user_dico_string['key_ip_based_country_code']))						
		
		# Fonction Création Json
				
		def Creation_JSON(liste, titre):
			"""
			Creation JSON
			"""    
			path_json = './Rapport/json/'+titre+'.json'
			with open(path_json, "w") as f:
				json_str = json.dumps(liste)        
				f.write(json_str)
			f.close
			
		### Fonction Sqlite_Analyzer
		
		def sqlite_analyzer(db, requests):
			   
			for requete in requests:
				print("Base selectionnée :", db)
				print("Requête en cours :", requete)
				print("Début extraction Requête en cours :", requete)
				donnees_bdd = table_message(db, requete)
				print("Fin extraction Requête en cours :", requete)
				print("Début Création JSON :", requete)
				Creation_JSON(donnees_bdd, requete)
				print("Fin Création JSON :", requete)
				print("Début Création Rapport HTML :", requete)
				Export_html(donnees_bdd, requete)
				print("Fin Création Rapport HTML :", requete)
				print("#"*50)	
		
		### Analyse
		
		if os.path.exists(path_app) is True:
			print('Application détectée : '+path_app)
			print('#'*50)
					
			if os.path.isfile(path_main_db):
				print('Base main.db détectée')
				sqlite_analyzer(path_main_db, liste_requete_main_db)			
			else:
				('Base main.db non détectée dans le dossier \com.snapchat.android\databases\ ')	
					
			if os.path.isfile(path_memories_db):
				print('Base memories.db détectée')
				sqlite_analyzer(path_memories_db, liste_requete_memories_db)		
			else:
				('Base memories.db non détectée dans le dossier \com.snapchat.android\databases\ ')
				
			if os.path.isfile(path_journal_db):
				print('Base journal.db détectée')
				sqlite_analyzer(path_journal_db, liste_journal_db)		
			else:
				('Base journal.db non détectée dans le dossier \com.snapchat.android\databases\ ')
			print("Fin d'analyse...")				
			
			# Nom de dossier en fonction du n° du cas
			os.rename('./Rapport', './Rapport'+'_'+cas)			
			input('Appuyez sur une touche pour quitter')			
			
		else:
			print("Application Snapchat : 'com.snapchat.android' non détectée")
			print("Veuillez insérer l'application dans le dossier "+path_script+" avant de relancer l'application")
			input('Appuyez sur une touche pour quitter')

	else:    
		print("Dossier " , path_cas ,  " déjà existant, veuillez supprimer l'ancien dossier avant de relancer une analyse.")	
