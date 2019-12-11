#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable = C0103, C0301, E0611, E0401

__auteur__ = "Yann-Ntech"
__version__ = "0.2 Beta"
__date__ = "20/09/2018"
__licence__ = "GNU GENERAL PUBLIC LICENSE Version 3"

import json

"""
TEMPLATE sans variables de la def
"""
footer = """
	<script>
	var $table = $('#table')

	$(function() {
	var data = """

#Insertion du json dans le var data	entre footer et footer2
  
footer2 = """

 $table.bootstrapTable({data: data})
  })
</script>

</body></html>
"""		
		
def Export_html(liste_messages, titre):
	"""
	Export html
	"""    		
	"""
	TEMPLATE
	"""	
	template = """
	<!doctype html>
	<html lang="en">
	<head>
		<meta charset="utf-8" />
		<title>{0}</title>
		
	<link rel="stylesheet" href="./css/bootstrap.min.css">
		  <link rel="stylesheet" href="./css/all.css">    
		  <link rel="stylesheet" href="./css/bootstrap-table.min.css">
		  <link rel="stylesheet" href="./css/sticky-footer-navbar.css">
		  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">
		  <link href="https://unpkg.com/bootstrap-table@1.15.4/dist/bootstrap-table.min.css" rel="stylesheet">
			<script src="https://unpkg.com/bootstrap-table@1.15.4/dist/bootstrap-table.min.js"></script>
		  <script type="text/javascript" src="./js/all.js"></script>
		  <script type="text/javascript" src="./js/jquery-3.4.0.min.js"></script>
		  <script type="text/javascript" src="./js/popper.min.js"></script>
		  <script type="text/javascript" src="./js/bootstrap.min.js"></script>
		  <script type="text/javascript" src="./js/bootstrap-table.min.js"></script>
	</head>

	<header>
		<nav class="navbar navbar-expand-md navbar-dark fixed-top" style="background-color: #607d8b;">
			<a class="navbar-brand" href="#" align="center"><img src="./img/snapchat.png" alt="Bug image" height="50" weight="50">    Rapport d'analyse SNAPCHAT - {1}</a>	  
		</nav>
	</header>

	<body>		

	<div class="container-fluid">
	  <div class="row justify-content-around">
		<div class="col-md-12" style="margin-top: 80px; height: 75%">	
		
		<table id="table"			           
				data-pagination="true"            
				data-search="true"
				data-sortable="true"
				data-show-columns="true"
				data-show-fullscreen=True
				data-page-list="[5, 10, 25, 50, 100, ALL]"
				class="table-bordered table-striped">
	  <thead>
	<tr>""".format(titre, titre)
			
	# Récupération du chemin du JSON
	
	path_titre_json = './Rapport/json/'+titre+'.json'
	
	with open(path_titre_json, "r") as j:
		json_str = j.read()
		j.close
		
	# Récupération des données du JSON	 
 
########## GENERATION PAGES HTML MAIN.DB

	if titre == 'requete_BestFriend':
	
		colonnes = """
			  <th data-field="ID" data-sortable="true">ID</th>
			  <th data-field="Username" data-sortable="true">Username</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>
			  <th data-field="Date Ajout Ami" data-sortable="true">Date Ajout Ami</th>     
			</tr>
		  </thead>
		</table>
		"""
	elif titre == 'requete_BlackListFriend':
		colonnes = """
			  <th data-field="ID" data-sortable="true">_id</th>
			  <th data-field="Username" data-sortable="true">Username</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>			  
			</tr>
		  </thead>
		</table>
		"""			
	elif titre == 'requete_Feed':
		colonnes = """
			  <th data-field="Clé" data-sortable="true">Clé</th>
			  <th data-field="Username" data-sortable="true">Username</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>	
			  <th data-field="Type d'intéraction" data-sortable="true">Type d'intéraction</th>
			  <th data-field="Date Display" data-sortable="true">Date Display</th>
			  <th data-field="Reception" data-sortable="true">Reception</th>
			  <th data-field="Envoyé" data-sortable="true">Envoyé</th>
			  <th data-field="Effacé" data-sortable="true">Effacé</th>
			  <th data-field="Dernière lecture" data-sortable="true">Dernière lecture</th>
			  <th data-field="Dernier lecteur" data-sortable="true">Dernier lecteur</th>
			  <th data-field="Derniere écriture" data-sortable="true">Dernière écriture</th>
			  <th data-field="Dernier type d'écriture" data-sortable="true">Dernier type d'écriture</th>
			  <th data-field="Dernier participant" data-sortable="true">Dernier participant</th>	
			   <th data-field="Ma dernière lecture" data-sortable="true">Ma dernière lecture</th>
		  </thead>
		</table>			
		"""			
	elif titre == 'requete_FeedGroupe':
		colonnes = """
			 <th data-field="Clé" data-sortable="true">Clé</th>
			  <th data-field="Nombre Participants" data-sortable="true">Nombre Participants</th>
			  <th data-field="Participants" data-sortable="true">Participants</th>	
			  <th data-field="Type d'intéraction" data-sortable="true">Type d'intéraction</th>
			  <th data-field="Date Display" data-sortable="true">Date Display</th>
			  <th data-field="Sorting Timestamp" data-sortable="true">Sorting Timestamp</th>
			  <th data-field="Date Création Groupe" data-sortable="true">Date Création Groupe</th>
			  <th data-field="Date dernière Interaction" data-sortable="true">Date dernière Interaction</th>
			  <th data-field="User ID Dernier interaction" data-sortable="true">User ID Dernier interaction</th>
			  <th data-field="User ID Dernier Participant" data-sortable="true">User ID Dernier Participant</th>
			  <th data-field="Dernier Participant" data-sortable="true">Dernier Participant</th>			  
			  <th data-field="Reception" data-sortable="true">Reception</th>
			  <th data-field="Envoyé" data-sortable="true">Envoyé</th>
			  <th data-field="Effacé" data-sortable="true">Effacé</th>
			  <th data-field="Dernière lecture" data-sortable="true">Dernière lecture</th>
			  <th data-field="Dernier lecteur" data-sortable="true">Dernier lecteur</th>
			  <th data-field="Type Dernier Lecteur" data-sortable="true">Type Dernier Lecteur</th>
			  <th data-field="Dernier type d'écriture" data-sortable="true">Dernier type d'écriture</th>
			  <th data-field="Date dernière écriture" data-sortable="true">Date dernière écriture</th>			   
		  </thead>
		</table>		
		"""	
				
	elif titre == 'requete_Friend':
		colonnes = """			 
			  <th data-field="Friend ID" data-sortable="true">Friend ID</th>
			  <th data-field="User ID" data-sortable="true">User ID</th>
			  <th data-field="Username" data-sortable="true">Username</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>
			  <th data-field="Téléphone" data-sortable="true">Téléphone</th>
			  <th data-field="Date Naissance" data-sortable="true">Date Naissance</th>
			  <th data-field="Date Ajout Ami" data-sortable="true">Date Ajout Ami</th>
			  <th data-field="Follow par Ami" data-sortable="true">Follow par Ami</th>   
			  <th data-field="Type Lien" data-sortable="true">Type Lien</th>
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_FriendWhoAddedMe':
		colonnes = """
			  <th data-field="Username" data-sortable="true">Username</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>
			  <th data-field="Source Ajout" data-sortable="true">Source Ajout</th>
			  <th data-field="Ajouté" data-sortable="true">Ajouté</th>
			  <th data-field="Ignoré" data-sortable="true">Ignoré</th> 			 
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_InteractionMessages':
		colonnes = """
			  <th data-field="ID" data-sortable="true">ID</th>
			  <th data-field="Username" data-sortable="true">Username</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>
			  <th data-field="Type Message" data-sortable="true">Type Message</th>
			  <th data-field="Chat ID" data-sortable="true">Chat ID</th>
			  <th data-field="Date Chat" data-sortable="true">Date Chat</th> 	
			  <th data-field="Snap ID" data-sortable="true">Snap ID</th> 
			  <th data-field="Date Snap" data-sortable="true">Date Snap</th> 
			  <th data-field="Date Interaction" data-sortable="true">Date Interaction</th> 			  	 
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_Message':
		colonnes = """
			  <th data-field="ID Feed" data-sortable="true">ID Feed</th>
			  <th data-field="Clé Feed" data-sortable="true">Clé Feed</th>
			  <th data-field="Date Emission" data-sortable="true">Date Emission</th>
			  <th data-field="ID Emetteur" data-sortable="true">ID Emetteur</th>  
			  <th data-field="Emetteur" data-sortable="true">Emetteur</th> 
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th> 
			  <th data-field="Date Vue" data-sortable="true">Date Vue</th>
			  <th data-field="Type" data-sortable="true">Type</th>
			  <th data-field="Contenu" data-sortable="true">Contenu</th>
			  <th data-field="Screenshot ou Replay" data-sortable="true">Screenshot ou Replay</th>
			  <th data-field="Dernière Intéraction" data-sortable="true">Dernière Intéraction</th>   
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_MessageSnap':
		colonnes = """
			 <th data-field="Clé Feed" data-sortable="true">Clé Feed</th>
			  <th data-field="Date Envoi" data-sortable="true">Date Envoi</th>
			  <th data-field="ID Emetteur" data-sortable="true">ID Emetteur</th>
			  <th data-field="Emetteur" data-sortable="true">Emetteur</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>     
			  <th data-field="Dernière Interaction" data-sortable="true">Dernière Interaction</th>
			  <th data-field="Snap ID" data-sortable="true">Snap ID</th>
			  <th data-field="Media ID" data-sortable="true">Media ID</th>
			  <th data-field="Media Key" data-sortable="true">Media Key</th>
			</tr>
		  </thead>
		</table>
		"""			

	elif titre == 'requete_ProfileSavedMediaMessage':
		colonnes = """
			 <th data-field="messageID" data-sortable="true">messageID</th>
			  <th data-field="conversationID" data-sortable="true">conversationID</th>
			  <th data-field="ID Emetteur" data-sortable="true">ID Emetteur</th>
			  <th data-field="Emetteur" data-sortable="true">Emetteur</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>   
			  <th data-field="Date Display" data-sortable="true">Date Display</th> 			  
			  <th data-field="Type" data-sortable="true">Type</th>
			  <th data-field="Media" data-sortable="true">Media</th>
			  <th data-field="Media ID" data-sortable="true">Media ID</th>
			  <th data-field="Date vue" data-sortable="true">Date vue</th>
			  <th data-field="savedStates" data-sortable="true">savedStates</th>
			  <th data-field="Screenshot ou Replayed" data-sortable="true">Screenshot ou Replayed</th>
			</tr>
		  </thead>
		</table>
		"""	
		
		
	elif titre == 'requete_SendToLastSnapRecipients':
		colonnes = """
			 <th data-field="Clé" data-sortable="true">Clé</th>
			  <th data-field="Timestamp" data-sortable="true">Timestamp</th>			  
			  <th data-field="Utilisateur" data-sortable="true">Utilisateur</th>
			  <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>   		  
			</tr>
		  </thead>
		</table>
		"""	
	
	elif titre == 'requete_NetworkMessage':
		colonnes = """
			 <th data-field="conversationID" data-sortable="true">ID Conversation</th>
			 <th data-field="Date Envoi" data-sortable="true">Date Envoi</th>			  
			 <th data-field="Date Vue" data-sortable="true">Date Vue</th>
			 <th data-field="ID Emetteur" data-sortable="true">ID Emetteur</th>
			 <th data-field="Emetteur" data-sortable="true">Emetteur</th>
			 <th data-field="Pseudonyme" data-sortable="true">Pseudonyme</th>
			 <th data-field="Type" data-sortable="true">Type</th>
			 <th data-field="Contenu" data-sortable="true">Contenu</th>
			 <th data-field="Screenshot ou Replayed" data-sortable="true">Screenshot ou Replayed</th>
			 <th data-field="Dernière Interaction" data-sortable="true">Dernière Interaction</th>   		  
			</tr>
		  </thead>
		</table>
		"""	
		
########## GENERATION PAGES HTML MEMORIES.DB
		
	elif titre == 'requete_memories_entry':
		colonnes = """
			 <th data-field="Memories ID" data-sortable="true">Memories ID</th>
			  <th data-field="Snap ID" data-sortable="true">Snap ID</th>			  
			  <th data-field="Date Creation" data-sortable="true">Date Creation</th>
			  <th data-field="Privé" data-sortable="true">Privé</th>   		  
			</tr>
		  </thead>
		</table>
		"""			
		
	elif titre == 'requete_memories_snap_complete':
		colonnes = """
			  <th data-field="Snap ID" data-sortable="true">Snap ID</th>
			  <th data-field="Media ID" data-sortable="true">Media ID</th>	
			  <th data-field="Memories Entry ID" data-sortable="true">Memories Entry ID</th>	
			  <th data-field="ID Externe" data-sortable="true">ID Externe</th>				 		  
			  <th data-field="Date Capture" data-sortable="true">Date Capture</th>
			  <th data-field="Date Creation Memories" data-sortable="true">Date Creation Memories</th>   		  
			  <th data-field="Fuseau Horaire" data-sortable="true">Fuseau Horaire</th>
			  <th data-field="Taille" data-sortable="true">Taille</th>
			  <th data-field="Format" data-sortable="true">Format</th>
			  <th data-field="Durée" data-sortable="true">Durée</th>
			  <th data-field="Latitude" data-sortable="true">Latitude</th>
			  <th data-field="Longitude" data-sortable="true">Longitude</th>
			  <th data-field="User Agent" data-sortable="true">User Agent</th>
			  <th data-field="Selfie = 1" data-sortable="true">Selfie = 1</th>
			  <th data-field="Effacé = 1" data-sortable="true">Effacé = 1</th>
			  <th data-field="Privé - Me Only = 1" data-sortable="true">Privé - Me Only = 1</th>
			  <th data-field="Chiffré = 0" data-sortable="true">Chiffré = 0</th>
			  <th data-field="Clé Chiffrement" data-sortable="true">Clé Chiffrement</th>
			  <th data-field="Vecteur Initialisation IV" data-sortable="true">Vecteur Initialisation IV</th>
			  <th data-field="Filtres & Superposition appliqué(s)" data-sortable="true">Filtres & Superposition</th>
			  <th data-field="Operation" data-sortable="true">Operation</th>
			  <th data-field="Etat Operation" data-sortable="true">Etat Operation</th>
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_memories_snap_simple':
		colonnes = """
			  <th data-field="Snap ID" data-sortable="true">Snap ID</th>
			  <th data-field="Media ID" data-sortable="true">Media ID</th>	
			  <th data-field="Memories Entry ID" data-sortable="true">Memories Entry ID</th>	
			  <th data-field="ID Externe" data-sortable="true">ID Externe</th>
			  <th data-field="Thumbnail" data-sortable="true">Thumbnail</th>			 	 		  
			  <th data-field="Date Capture" data-sortable="true">Date Capture</th>			    		  
			  <th data-field="Fuseau Horaire" data-sortable="true">Fuseau Horaire</th>			  
			  <th data-field="Durée" data-sortable="true">Durée</th>
			  <th data-field="Latitude" data-sortable="true">Latitude</th>
			  <th data-field="Longitude" data-sortable="true">Longitude</th>
			  <th data-field="Geolocalisation" data-sortable="true">Geolocalisation</th>			 
			  <th data-field="User Agent" data-sortable="true">User Agent</th>
			  <th data-field="Selfie = 1" data-sortable="true">Selfie = 1</th>
			  <th data-field="Effacé = 1" data-sortable="true">Effacé = 1</th>			  
			  <th data-field="Clé Chiffrement" data-sortable="true">Clé Chiffrement</th>
			  <th data-field="Vecteur Initialisation IV" data-sortable="true">Vecteur Initialisation IV</th>
			  <th data-field="Filtres & Superposition appliqué(s)" data-sortable="true">Filtres & Superposition</th>			  
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_memories_meo_confidential':
		colonnes = """
			 <th data-field="Hash" data-sortable="true">Hash</th>
			  <th data-field="Master Key" data-sortable="true">Master Key</th>			  
			  <th data-field="Master Key IV" data-sortable="true">Master Key IV</th>			    
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_memories_remote_operation':
		colonnes = """
			 <th data-field="Memories Entry ID" data-sortable="true">Memories Entry ID</th>
			 <th data-field="Media ID" data-sortable="true">Media ID</th>			  
			  <th data-field="Date Création Opération" data-sortable="true">Date Création Opération</th>
			  <th data-field="Opération" data-sortable="true">Opération</th>   		  
			  <th data-field="Etat Opération" data-sortable="true">Etat Opération</th>
			  <th data-field="Serialized Operation" data-sortable="true">Serialized Operation</th>			    
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_memories_remote_operation_meo':
		colonnes = """
			 <th data-field="Memories Entry ID" data-sortable="true">Memories Entry ID</th>
			 <th data-field="Media ID" data-sortable="true">Media ID</th>			  
			  <th data-field="Date Création Opération" data-sortable="true">Date Création Opération</th>
			  <th data-field="Opération" data-sortable="true">Opération</th>   		  
			  <th data-field="Etat Opération" data-sortable="true">Etat Opération</th>
			  <th data-field="Serialized Operation" data-sortable="true">Serialized Operation</th>			    
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_memories_upload_status':
		colonnes = """
			 <th data-field="Snap ID" data-sortable="true">Snap ID</th>
			 <th data-field="Media ID" data-sortable="true">Media ID</th>			  
			  <th data-field="Etat Upload" data-sortable="true">Etat Upload</th>
			  <th data-field="Date" data-sortable="true">Date</th>   		  
			  <th data-field="Progression Upload" data-sortable="true">Progression Upload</th>			      
			</tr>
		  </thead>
		</table>
		"""	
				
	######## GENERATION PAGES HTML JOURNAL.DB	
	
	elif titre == 'requete_media_291':
		colonnes = """
			 <th data-field="Journal ID" data-sortable="true">Journal ID</th>
			 <th data-field="Path" data-sortable="true">Path</th>			  
			  <th data-field="Nom Fichier" data-sortable="true">Nom Fichier</th>
			  <th data-field="Thumbnail" data-sortable="true">Thumbnail</th>			  
			  <th data-field="Date Update" data-sortable="true">Date Update</th>   		  
			  <th data-field="Date Dernière Lecture" data-sortable="true">Date Dernière Lecture</th>
			  <th data-field="Taille (Ko)" data-sortable="true">Taille (Ko)</th>			      
			</tr>
		  </thead>
		</table>
		"""			
		
	elif titre == 'requete_media_229':
		colonnes = """
			 <th data-field="Journal ID" data-sortable="true">Journal ID</th>
			 <th data-field="Path" data-sortable="true">Path</th>			  
			  <th data-field="Nom Fichier" data-sortable="true">Nom Fichier</th>
			  <th data-field="Thumbnail" data-sortable="true">Thumbnail</th>	
			  <th data-field="Date Update" data-sortable="true">Date Update</th>   		  
			  <th data-field="Date Dernière Lecture" data-sortable="true">Date Dernière Lecture</th>
			  <th data-field="Taille (Ko)" data-sortable="true">Taille (Ko)</th>			      
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_media_228':
		colonnes = """
			 <th data-field="Journal ID" data-sortable="true">Journal ID</th>
			 <th data-field="Path" data-sortable="true">Path</th>			  
			  <th data-field="Nom Fichier" data-sortable="true">Nom Fichier</th>
			  <th data-field="Date Update" data-sortable="true">Date Update</th>   		  
			  <th data-field="Date Dernière Lecture" data-sortable="true">Date Dernière Lecture</th>
			  <th data-field="Taille (Ko)" data-sortable="true">Taille (Ko)</th>			      
			</tr>
		  </thead>
		</table>
		"""	
		
	elif titre == 'requete_media_290':
		colonnes = """
			 <th data-field="Journal ID" data-sortable="true">Journal ID</th>
			 <th data-field="Path" data-sortable="true">Path</th>			  
			  <th data-field="Nom Fichier" data-sortable="true">Nom Fichier</th>
			  <th data-field="Thumbnail" data-sortable="true">Thumbnail</th>	
			  <th data-field="Date Update" data-sortable="true">Date Update</th>   		  
			  <th data-field="Date Dernière Lecture" data-sortable="true">Date Dernière Lecture</th>
			  <th data-field="Taille (Ko)" data-sortable="true">Taille (Ko)</th>			      
			</tr>
		  </thead>
		</table>
		"""	
	
	# Récupération du chemin du fichier HTML à créer
	path_titre_html = './Rapport/html/'+titre+'.html'
	
	# Ecriture du fichier HTML avec template et variables précédente
	with open(path_titre_html, "w", encoding="utf-8") as f:
		f.write(template)
		f.write(colonnes)
		f.write(footer)  
		f.write(json_str)
		f.write(footer2)      		
	f.close
