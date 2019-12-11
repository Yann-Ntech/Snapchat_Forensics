#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable = C0103, C0301, E0611, E0401

__auteur__ = "Yann-Ntech"
__version__ = "0.2 Beta"
__date__ = "20/09/2018"
__licence__ = "GNU GENERAL PUBLIC LICENSE Version 3"

"""
Récupération des données dans la base de donnée Main.db
"""
import sqlite3
import shutil
import os
import re
import base64
from PIL import Image

### REQUETE MAIN.DB

requete_BestFriend = """    
	SELECT     
    BestFriend._id, 
    username, 
    displayName, 
    datetime(addedTimestamp/1000, 'unixepoch', 'localtime') AS 'Date Ajout'	
	FROM BestFriend, Friend
	WHERE BestFriend.friendRowId = Friend._id"""

requete_BlackListFriend = """	
	SELECT 
	BlackListFriend._id, 
	username, 
	displayName
	FROM BlackListFriend, Friend
	WHERE BlackListFriend.friendId = Friend.userId
"""

requete_Feed = """
	SELECT 
	Feed.key, 
	Friend.username, 
	Friend.displayName, 
	displayInteractionType, 
	datetime(displayTimestamp/1000, 'unixepoch', 'localtime') AS 'Date Display', 
	datetime(myReceivedSnapReleaseTimestamp/1000, 'unixepoch', 'localtime') AS Received, 
	datetime(mySentSnapReleaseTimestamp/1000, 'unixepoch', 'localtime') AS Sent, 
	datetime(clearedTimestamp/1000, 'unixepoch', 'localtime') AS Cleared, 
	datetime(lastReadTimestamp/1000, 'unixepoch', 'localtime') AS lastRead, 
	lastReader, 
	lastWriteType, datetime(lastWriteTimestamp/1000, 'unixepoch', 'localtime') AS lastWrite, 
	lastWriter, 
	datetime(myLastReadTimestamp/1000, 'unixepoch', 'localtime') AS myLastRead
	FROM Feed, Friend
	WHERE Feed.friendRowId = Friend._id AND displayTimestamp != 0
	ORDER BY displayTimestamp DESC
"""

requete_FeedGroupe = """
	SELECT
	key AS Clé, 
	participantsSize AS 'Nombre de participants', 
	fitScreenParticipantString AS 'Participants affichés',
	displayInteractionType AS 'Type Interaction', 
	datetime(displayTimestamp/1000, 'unixepoch', 'localtime') AS 'Date Display', 
	datetime(sortingTimestamp/1000, 'unixepoch', 'localtime') AS 'Sorting Timestamp',
	datetime(groupCreationTimestamp/1000, 'unixepoch', 'localtime') AS 'Date création Groupe',
	datetime(lastInteractionTimestamp/1000, 'unixepoch', 'localtime') AS 'Date dernière interaction',
	lastInteractionUserId AS 'UserID dernière interaction',
	lastInteractionWriterId AS 'UserID Dernier participant',
	lastWriter AS 'Dernier participant', 
	datetime(myReceivedSnapReleaseTimestamp/1000, 'unixepoch', 'localtime') AS Received, 
	datetime(mySentSnapReleaseTimestamp/1000, 'unixepoch', 'localtime') AS Sent, 
	datetime(clearedTimestamp/1000, 'unixepoch', 'localtime') AS Cleared, 
	datetime(lastReadTimestamp/1000, 'unixepoch', 'localtime') AS 'Date dernière lecture', 
	lastReader AS 'Dernier lecteur', 
	lastWriteType AS 'Type dernière écriture', 
	datetime(lastWriteTimestamp/1000, 'unixepoch', 'localtime') AS 'Date dernière écriture'
	FROM Feed
	WHERE groupCreationTimestamp != 0
	ORDER BY displayTimestamp DESC
"""

requete_Friend = """
	SELECT 
	_id as 'Friend ID',
	userId as 'User ID',
	username as 'Nom du compte',
	displayName as 'Nom affiché',
	phone as 'Téléphone',
	datetime(birthday/100, 'unixepoch', 'localtime')  as 'Date de naissance',
	datetime(addedTimestamp/1000, 'unixepoch', 'localtime')  as "Date d'ajout",
	datetime(reverseAddedTimestamp/1000, 'unixepoch', 'localtime')  as "Date ajoutée",
	friendLinkType as 'Type de Lien'
	FROM Friend
	ORDER BY addedTimestamp DESC
"""

requete_FriendWhoAddedMe = """
	SELECT 
	username, displayName,
	addSource AS "Source d'ajout",
	added as 'Ajouté',
	ignored as 'Ignoré'
	FROM Friend, FriendWhoAddedMe
	WHERE Friend.userId = FriendWhoAddedMe.userId

"""

requete_InteractionMessages = """
	SELECT 
	feedRowId as 'ID',
	Friend.username as 'Username',
	Friend.displayName as 'Nom affiché',
	messageType 'Type Message',
	chatMessageId as 'Chat ID',
	datetime(chatMessageTimestamp/1000, 'unixepoch', 'localtime') as 'Date Chat',
	InteractionMessages.snapId as 'Snap ID',
	datetime(InteractionMessages.snapMessageTimestamp/1000, 'unixepoch', 'localtime') as 'Date Snap',
	datetime(InteractionMessages.interactionTimestamp/1000, 'unixepoch', 'localtime') as 'Date Interaction'
	FROM Feed
	JOIN InteractionMessages ON InteractionMessages.feedRowId = Feed._id
	JOIN Friend ON Feed.friendRowId = Friend._id
"""

requete_Message = """
	SELECT 
	feedRowId as 'Numéro Conversation',
	Feed.key as 'Conversation',
	datetime(timestamp/1000, 'unixepoch', 'localtime') as 'Date emission',
	senderId as 'Emetteur',
    username,
    displayname,
	datetime(seenTimestamp/1000, 'unixepoch', 'localtime') as 'Date de vue',
	type as 'Type',
	content as 'Contenu',
	screenshottedOrReplayed as 'Screenshot ou Replay',
	datetime(Message.lastInteractionTimestamp/1000, 'unixepoch', 'localtime') as 'Dernière interaction'
	FROM Message, Feed, Friend
	WHERE Message.feedRowId = Feed.rowid
    AND Message.senderId = Friend._id
    ORDER BY 'Date emission' DESC
"""

requete_MessageSnap = """
	SELECT 
	Feed.key as 'Conversation',
	datetime(MessagingSnap.sendStartTimestamp/1000, 'unixepoch', 'localtime') AS 'Date Envoi',
	MessagingSnap.senderId,
	Friend.username,
	Friend.displayName,
	datetime(MessagingSnap.lastInteractionTimestamp/1000, 'unixepoch', 'localtime') AS 'Dernière Interaction',
	Snap.snapId,
	Snap.mediaId,
	Snap.mediakey
	FROM MessagingSnap, Friend, Feed, Snap
	WHERE Friend._id = MessagingSnap.senderId 
	AND Feed._id = MessagingSnap.feedRowId 
	AND MessagingSnap.snapRowId = Snap.rowid
"""

requete_ProfileSavedMediaMessage = """
	SELECT 
	Message.key,
	ProfileSavedMediaMessage.conversationId,
	Message.senderId,
	ProfileSavedMediaMessage.senderUsername,
	Friend.displayName,
	datetime(timestamp/1000, 'unixepoch', 'localtime') AS 'Date Display',
	Message.type,
	ProfileSavedMediaMessage.serializedParcelContent,
	ProfileSavedMediaMessage.mediaIDs,
	datetime(seenTimestamp/1000, 'unixepoch', 'localtime') AS 'Seen Display',
	Message.savedStates,
	Message.screenshottedOrReplayed
	FROM Message, ProfileSavedMediaMessage, Friend
	WHERE Message.key == ProfileSavedMediaMessage.messageID
	AND Message.senderId == Friend._id
"""

requete_SendToLastSnapRecipients = """
	SELECT 
	SendToLastSnapRecipients.key,
	datetime(selectionTimestamp/1000, 'unixepoch', 'localtime') as selectionTimestamp,
	Friend.username,
	Friend.displayName
	FROM SendToLastSnapRecipients, Friend
	WHERE SendToLastSnapRecipients.key == Friend.userId
"""

requete_NetworkMessage = """
SELECT 
conversationId,
datetime(sentTimestamp/1000, 'unixepoch', 'localtime') AS 'Date Envoi',
datetime(seenTimestamp/1000, 'unixepoch', 'localtime') AS 'Date Vue',
senderId,
Friend.username,
Friend.displayName,
messageType,
content,
screenshottedOrReplayed,
datetime(lastInteractionTimestamp/1000, 'unixepoch', 'localtime') AS 'Dernière Interaction'

FROM NetworkMessage, Friend
WHERE NetworkMessage.senderId == Friend._id
"""

### REQUETE MEMORIES.DB

requete_memories_entry = """
SELECT 
_id,
snap_ids,
datetime(create_time/1000, 'unixepoch', 'localtime') as 'Date Création',
is_private
FROM memories_entry
"""

requete_memories_snap_complete = """
SELECT 
memories_snap._id as 'Snap ID',
memories_snap.media_id as 'Nom du fichier : media_id',
memories_snap.memories_entry_id as 'ID Memories Entry',
memories_snap.external_id as 'ID Externe',
datetime(snap_capture_time/1000, 'unixepoch', 'localtime') AS 'Snap Capture',
datetime(latest_snap_create_time/1000, 'unixepoch', 'localtime') AS 'Date Creation Memories',
time_zone_id 'Fuseau Horaire',
memories_media.size,
memories_media.format,
duration as 'Durée',
latitude,
longitude,
snap_create_user_agent as 'Snap User Agent',
front_facing as 'Selfie = 1',
has_deleted as 'Effacé = 1',
memories_entry.is_private as 'Privé - Me Only = 1',
memories_media.is_decrypted_video as 'Chiffré = 0',
encrypted_media_key as 'Clé Chiffrement',
encrypted_media_iv as 'Vecteur Initialisation IV',
overlay_size as 'Superposition',
memories_remote_operation.operation,
memories_remote_operation.schedule_state
FROM memories_snap, memories_media, memories_entry, memories_remote_operation
WHERE Memories_media._id == memories_snap.media_id
AND memories_snap.memories_entry_id == memories_entry._id
AND memories_remote_operation.target_entry == memories_snap.memories_entry_id
"""

requete_memories_snap_simple = """
SELECT 
_id as 'Snap ID',
media_id as 'Nom du fichier : media_id',
memories_entry_id as 'ID Memories Entry',
external_id as 'ID Externe',
datetime(snap_capture_time/1000, 'unixepoch', 'localtime') AS 'Snap Capture',
time_zone_id 'Fuseau Horaire',
duration as 'Durée',
latitude,
longitude,
snap_create_user_agent as 'Snap User Agent',
front_facing as 'Selfie = 1',
has_deleted as 'Effacé = 1',
encrypted_media_key as 'Clé Chiffrement',
encrypted_media_iv as 'Vecteur Initialisation IV',
overlay_size as 'Superposition'
FROM memories_snap
"""

requete_memories_remote_operation = """
SELECT 
target_entry as 'ID Memories Entry',
memories_snap.media_id as 'Nom Fichier',
datetime(created_timestamp/1000, 'unixepoch', 'localtime') as 'Date Création Opération',
operation,
schedule_state,
serialized_operation
FROM memories_remote_operation, memories_snap
WHERE memories_remote_operation.target_entry == memories_snap.memories_entry_id
"""

requete_memories_remote_operation_meo = """
SELECT 
target_entry as 'SNAP ID',
memories_snap.media_id as 'Nom Fichier',
datetime(created_timestamp/1000, 'unixepoch', 'localtime') as 'Date Création Opération',
operation,
schedule_state,
serialized_operation
FROM memories_remote_operation, memories_snap
WHERE memories_remote_operation.target_entry == memories_snap.memories_entry_id
AND memories_remote_operation.operation = 'UPDATE_PRIVATE_ENTRY_OPERATION'
"""

requete_memories_upload_status = """
SELECT 
snap_id,
memories_snap.media_id as 'Nom Fichier',
upload_state,
datetime(snap_create_time/1000, 'unixepoch', 'localtime') as 'Date Création',
upload_progress
FROM memories_snap_upload_status, memories_snap
WHERE memories_snap_upload_status.snap_id == memories_snap._id
"""

requete_memories_meo_confidential = """
SELECT 
hashed_passcode,
master_key,
master_key_iv
FROM memories_meo_confidential
"""

######## REQUETE JOURNAL.DB

requete_media_291 ="""
SELECT 
journal._id as 'Journal ID',
Path,
journal_entry.key as 'Nom de fichier',
datetime(last_update_time/1000, 'unixepoch', 'localtime') as 'Last Update Time',
datetime(last_read_time/1000, 'unixepoch', 'localtime') as 'Last Read Time',
total_size/1024 as 'Taille (Ko)'
FROM journal, journal_entry
WHERE journal._id == journal_entry.journal_id
AND journal._id == 291
"""

requete_media_229 ="""
SELECT 
journal._id as 'Journal ID',
Path,
journal_entry.key as 'Nom de fichier',
datetime(last_update_time/1000, 'unixepoch', 'localtime') as 'Last Update Time',
datetime(last_read_time/1000, 'unixepoch', 'localtime') as 'Last Read Time',
total_size/1024 as 'Taille (Ko)'
FROM journal, journal_entry
WHERE journal._id == journal_entry.journal_id
AND journal._id == 229
"""

requete_media_228 ="""
SELECT 
journal._id as 'Journal ID',
Path,
journal_entry.key as 'Nom de fichier',
datetime(last_update_time/1000, 'unixepoch', 'localtime') as 'Last Update Time',
datetime(last_read_time/1000, 'unixepoch', 'localtime') as 'Last Read Time',
total_size/1024 as 'Taille (Ko)'
FROM journal, journal_entry
WHERE journal._id == journal_entry.journal_id
AND journal._id == 228
"""

requete_media_290 ="""
SELECT 
journal._id as 'Journal ID',
Path,
journal_entry.key as 'Nom de fichier',
datetime(last_update_time/1000, 'unixepoch', 'localtime') as 'Last Update Time',
datetime(last_read_time/1000, 'unixepoch', 'localtime') as 'Last Read Time',
total_size/1024 as 'Taille (Ko)'
FROM journal, journal_entry
WHERE journal._id == journal_entry.journal_id
AND journal._id == 290"""

def table_message(base_db, titre):
	"""
	Récupération des messages dans la base db
	"""		
	# Dico pour transposer l'argument Titre de la définition en variables énumérées ci-dessus.
	dico = {
	'requete_BestFriend':requete_BestFriend, 
	'requete_BlackListFriend':requete_BlackListFriend, 
	'requete_Feed':requete_Feed, 
	'requete_FeedGroupe':requete_FeedGroupe, 
	'requete_Friend':requete_Friend, 
	'requete_FriendWhoAddedMe':requete_FriendWhoAddedMe,
	'requete_InteractionMessages':requete_InteractionMessages,
	'requete_Message':requete_Message,
	'requete_MessageSnap':requete_MessageSnap,
	'requete_ProfileSavedMediaMessage':requete_ProfileSavedMediaMessage,
	'requete_SendToLastSnapRecipients':requete_SendToLastSnapRecipients,
	'requete_NetworkMessage':requete_NetworkMessage,
	'requete_memories_entry':requete_memories_entry,
	'requete_memories_snap_complete':requete_memories_snap_complete,
	'requete_memories_snap_simple':requete_memories_snap_simple,
	'requete_memories_meo_confidential':requete_memories_meo_confidential,
	'requete_memories_remote_operation':requete_memories_remote_operation,
	'requete_memories_remote_operation_meo':requete_memories_remote_operation_meo,
	'requete_memories_upload_status':requete_memories_upload_status,
	'requete_media_291':requete_media_291,
	'requete_media_229':requete_media_229,
	'requete_media_228':requete_media_228,
	'requete_media_290':requete_media_290
	} 

	# Sélection des colonnes utiles de la table messages de la base de données.	
	print("Début d'extraction des données de la requête: ", titre)
	db_fic = sqlite3.connect(base_db)
	cursor = db_fic.cursor()
	
	# Execution de la requête SQL en transposant le titre avec sa correspondance VARIABLE dans le dico.	
	cursor.execute(dico[titre])
	rows = cursor.fetchall()	
	liste_messages = []
	
	# Traitement des heures nulles '1970-01-01 01:00:00' -------- A revoir	
	def null_unixepoch(heure):		
		if heure == '1970-01-01 01:00:00':
			heure == '--'						
		else:
			pass			
		return heure
	
	# Traitement du résultat de la requête SQL : Génération des colonnes	
	
	###### TRAITEMENT MAIN.DB
	
	if base_db == '.\com.snapchat.android\databases\main.db':
		if titre == 'requete_BestFriend':
			try:
				for elt in rows:				
					_id, username, displayName, date_ajout = elt		
					liste_messages.append({'ID':_id, 'Username':username, 'Pseudonyme':displayName, 'Date Ajout Ami':date_ajout})	
				return liste_messages		
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
				
		if titre == 'requete_BlackListFriend':
			try:	
				for elt in rows:				
					_id, username, displayName = elt		
					liste_messages.append({'ID':_id, 'Username':username, 'Pseudonyme':displayName})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')		
		
		if titre == 'requete_Feed':
			try:	
				for elt in rows:				
					key, username, displayName, displayInteractionType, dateDisplay, received, sent, cleared, lastRead, lastReader, lastWriteType, lastWrite, lastWriter, myLastRead = elt			
					for heure in elt:
						null_unixepoch(heure)	
					liste_messages.append({'Clé':key, 'Username':username, 'Pseudonyme':displayName, 'Type d\'intéraction':displayInteractionType, 'Date Display':dateDisplay, 'Reception':received, 'Envoyé':sent, 'Effacé':cleared, 'Dernière lecture':lastRead, 'Dernier lecteur':lastReader, 'Dernier type d\'écriture':lastWriteType, 'Derniere écriture':lastWrite, 'Dernier participant':lastWriter, 'Ma dernière lecture':myLastRead})						
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
			
		if titre == 'requete_FeedGroupe':
			try:	
				for elt in rows:				
					key, nombreParticipants, participants, typeInteraction, dateDisplay, sortingTimestamp, dateCréationGroupe, dateDernièreInteraction, userIdDerniereInteraction, userIdDernierParticipant, dernierParticipant, reception, envoi, effacé, dateDernièreLecture, dernierLecteur, typeDernierEcriture, dateDernierEcriture = elt			
					for heure in elt:
						null_unixepoch(heure)
					liste_messages.append({'Clé':key, 'Nombre Participants':nombreParticipants, 'Participants':participants, 'Type d\'intéraction':typeInteraction, 'Date Display':dateDisplay, "Sorting Timestamp":sortingTimestamp, "Date Création Groupe":dateCréationGroupe, "Date dernière Interaction":dateDernièreInteraction, 'User ID Dernier interaction':userIdDerniereInteraction, 'User ID Dernier Participant':userIdDernierParticipant, 'Dernier Participant':dernierParticipant, 'Reception':reception, 'Envoyé':envoi, 'Effacé':effacé, 'Dernière lecture':dateDernièreLecture, 'Dernier lecteur':dernierLecteur, 'Dernier type d\'écriture':typeDernierEcriture, 'Date dernière écriture':dateDernierEcriture})			
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
			
		if titre == 'requete_Friend':
			try:	
				for elt in rows:				
					_id, userId, username, displayName, phone, dateNaissance, dateAjout, follow ,typeLien = elt
					if dateAjout == '1970-01-01 01:00:00':
						dateAjoute = '--'
					if follow == '1970-01-01 01:00:00':
						follow = '--'
					liste_messages.append({'Friend ID':_id, 'User ID':userId,'Username':username, 'Pseudonyme':displayName, 'Téléphone':phone, 'Date Naissance':dateNaissance, 'Date Ajout Ami':dateAjout, 'Follow par Ami':follow, 'Type Lien':typeLien})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
				
		if titre == 'requete_FriendWhoAddedMe':
			try:
				for elt in rows:				
					username, displayName, sourceAjout, ajouté, ignoré = elt		
					liste_messages.append({'Username':username, 'Pseudonyme':displayName, 'Source Ajout':sourceAjout, 'Ajouté':ajouté, 'Ignoré':ignoré})	
				return liste_messages	
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
			
		if titre == 'requete_InteractionMessages':
			try:	
				for elt in rows:				
					_id, username, displayName, typeMessage, chatId, dateChat, snapId, dateSnap, dateInteraction = elt		
					liste_messages.append({'ID':_id, 'Username':username, 'Pseudonyme':displayName, 'Type Message':typeMessage, 'Chat ID':chatId, 'Date Chat':dateChat, 'Snap ID':snapId, 'Date Snap':dateSnap, 'Date Interaction':dateInteraction})	
				return liste_messages	
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
		
		if titre == 'requete_Message':
			try:
				for elt in rows:				
					idFeed, cléFeed, dateEmission, emetteur, username, displayName, dateVue, messagetype, content, screenshot, derniereInteraction = elt				
					#décodage des BLOB en UTF-8
					content = content.decode('utf-8', errors='ignore')					
					#traitement des type media - image - video afin d'extraire la chaine de caractère représentant le nom du fichier
					if messagetype == 'media_v4' or messagetype =='batched_media' or messagetype == 'media' or messagetype == 'audio_note':
						content = content[-55:]	# On affiche les derniers caractères utiles (avant une sorte de base64 non décodable)								
					liste_messages.append({'ID Feed':idFeed, 'Clé Feed':cléFeed, 'Date Emission':dateEmission, 'ID Emetteur':emetteur, 'Emetteur':username, 'Pseudonyme':displayName, 'Date Vue':dateVue, 'Type':messagetype, 'Contenu':content, 'Screenshot ou Replay':screenshot, 'Dernière Intéraction':derniereInteraction})								
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')	
				
		if titre == 'requete_MessageSnap':
			try:
				for elt in rows:				
					cléFeed, dateEnvoi, senderId, username, displayName, derniereInteraction, snapId, mediaId, mediaKey = elt		
					liste_messages.append({'Clé Feed':cléFeed, 'Date Envoi':dateEnvoi, 'ID Emetteur':senderId, 'Emetteur':username, 'Pseudonyme':displayName, 'Dernière Interaction':derniereInteraction, 'Snap ID':snapId, 'Media ID':mediaId, 'Media Key':mediaKey})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')			
		
		if titre == 'requete_ProfileSavedMediaMessage':
			try:
				for elt in rows:				
					messageID, conversationID, senderID, senderUsername, displayName, dateDisplay, type, serializedParcelContent, mediaID, seenDisplay, savedStates, screenshottedOrReplayed = elt					
					#décodage des BLOB en UTF-8
					serializedParcelContent = serializedParcelContent.decode('utf-8', errors='ignore')					
					liste_messages.append({'messageID':messageID, 'conversationID':conversationID, 'ID Emetteur':senderID, 'Emetteur':senderUsername, 'Pseudonyme':displayName, 'Date Display':dateDisplay, 'Type':type, 'Media':serializedParcelContent, 'Media ID':mediaID, 'Date vue':seenDisplay, 'savedStates':savedStates, 'Screenshot ou Replayed':screenshottedOrReplayed})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
			
		if titre == 'requete_SendToLastSnapRecipients':
			try:
				for elt in rows:				
					clé, timestamp, username, displayName = elt		
					liste_messages.append({'Clé':clé, 'Timestamp':timestamp,'Utilisateur':username, 'Pseudonyme':displayName})	
				return liste_messages	
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')					
				
		if titre == 'requete_NetworkMessage':
			try:
				for elt in rows:				
					conversationID, sentTimestamp, seenTimestamp, senderID, username, displayName, messagetype, content, screenshottedOrReplayed, lastInteraction = elt						
					#décodage des BLOB en UTF-8
					try:
						content = content.decode('utf-8', errors='ignore')				
					except:
						pass
					#traitement des type media - image - video afin d'extraire la chaine de caractère représentant le nom du fichier
					if messagetype == 'media_v4' or messagetype =='batched_media' or messagetype == 'media' or messagetype == 'audio_note':
						content = content[-55:]	# On affiche les derniers caractères utiles (avant une sorte de base64 non décodable)									
					liste_messages.append({'conversationID':conversationID, 'Date Envoi':sentTimestamp, 'Date Vue':seenTimestamp, 'ID Emetteur':senderID, 'Emetteur':username, 'Pseudonyme':displayName, 'Type':messagetype, 'Contenu':content, 'Screenshot ou Replayed':screenshottedOrReplayed, 'Dernière Interaction':lastInteraction})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
										
	###### TRAITEMENT MEMORIES.DB
	
	elif base_db == '.\com.snapchat.android\databases\memories.db':
		
		if titre == 'requete_memories_entry':
			try:
				for elt in rows:				
					_id, snap_id, dateCreation, is_private = elt				
					#décodage des BLOB en UTF-8
					try:
						snap_id = snap_id.decode('utf-8', errors='ignore')				
					except:
						pass					
								
					liste_messages.append({'Memories ID':_id, 'Snap ID':snap_id, 'Date Creation':dateCreation, 'Privé':is_private})	
				return liste_messages	
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')
		
		if titre == 'requete_memories_snap_complete':
			try:
				for elt in rows:				
					snap_id, media_id, ID_Memories_Entry, ID_Externe, snap_capture, snap_create, timezone, size, format, durée, latitude, longitude, user_agent, selfie, deleted, is_private, is_decrypted, media_key, media_iv, overlay, operation, etat_op = elt									
					liste_messages.append({'Snap ID':snap_id, 'Media ID':media_id, 'Memories Entry ID':ID_Memories_Entry, 'ID Externe':ID_Externe,'Date Capture':snap_capture, 'Date Creation Memories':snap_create, 'Fuseau Horaire':timezone, 'Taille':size, 'Format':format, 'Durée':durée, 'Latitude':latitude, 'Longitude':longitude, 'User Agent':user_agent, 'Selfie = 1':selfie, 'Effacé = 1':deleted, 'Privé - Me Only = 1':is_private, 'Chiffré = 0':is_decrypted, 'Clé Chiffrement':media_key, 'Vecteur Initialisation IV':media_iv, 'Filtres & Superposition':overlay, 'Operation':operation, 'Etat Operation':etat_op})			
				return liste_messages	
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')		
				
		if titre == 'requete_memories_snap_simple':
			try:
				for elt in rows:				
					snap_id, media_id, ID_Memories_Entry, ID_Externe, snap_capture, timezone, durée, latitude, longitude, user_agent, selfie, deleted, media_key, media_iv, overlay = elt									
					if latitude and longitude is not None:
						google = 'https://www.google.com/search?q='
						google_pos = google+str(latitude)+'+'+str(longitude)					
						google_position = "<center><a href="+google_pos+"""><img src="./img/geoloc.png" target="_blank" width=100 height=100></a></center>"""		
					else:
						pass							
					try:						
						media_id = media_id.upper()	
						media_id = media_id.replace('-','')											
						path_memories_media = './com.snapchat.android/files/file_manager/memories_media/'+media_id+'.media.0'					
						path_memories_copy = './Rapport/files/file_manager/memories_media/'+media_id+'.media.0'
						path_memories_thumb = './Rapport/files/file_manager/memories_media/thumbnails/'+media_id+'.media.0.thumb.jpg'						
						if os.path.exists(path_memories_media) is True:
							print('fichier memories_media détecté :'+media_id)
							shutil.copyfile(path_memories_media, path_memories_copy)
							print('Copie du fichier :'+media_id)
							im = Image.open(path_memories_copy)
							size = (100,100)
							im.thumbnail(size)
							im.save(path_memories_thumb)	
							print('Création du Thumbnail : ok')					
							href_memories_thumb = './files/file_manager/memories_media/thumbnails/'+media_id+'.0.thumb.jpg'
							href_memories_media = './files/file_manager/media/'+media_id+'.0'						
							href_fm_media = '<center><a href=../"'+href_media+'" target="_blank"><img src="../'+href_thumb+'" alt="Thumbnail non disponible"></center></a>'															
							href_memories_media = '<a href="'+path_memories_copy+'" target="_blank">'+path_memories_thumb+'</a>'
							print('Génération du Hypertexte : ok')
						else:						
							href_memories_media = 'Fichier non disponible'
					except:
						href_memories_media = 'Fichier non disponible'			
					liste_messages.append({'Snap ID':snap_id, 'Media ID':media_id, 'Memories Entry ID':ID_Memories_Entry, 'ID Externe':ID_Externe, 'Thumbnail':href_memories_media, 'Date Capture':snap_capture, 'Fuseau Horaire':timezone, 'Durée':durée, 'Latitude':latitude, 'Longitude':longitude, 'Geolocalisation':google_position, 'User Agent':user_agent, 'Selfie = 1':selfie, 'Effacé = 1':deleted, 'Clé Chiffrement':media_key, 'Vecteur Initialisation IV':media_iv, 'Filtres & Superposition':overlay})								
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')		
		
		if titre == 'requete_memories_meo_confidential':
			try:
				for elt in rows:				
					hashed_passcode, master_key, master_key_iv = elt						
					liste_messages.append({'Hash':hashed_passcode, 'Master Key':master_key, 'Master Key IV':master_key_iv})	
				return liste_messages	
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')				
			
		if titre == 'requete_memories_remote_operation':
			try:
				for elt in rows:				
					ID_Memories_Entry, media_id, dateCréation, operation, etat_op, serialized_operation = elt						
					liste_messages.append({'Memories Entry ID':ID_Memories_Entry, 'Media ID':media_id, 'Date Création Opération':dateCréation, 'Opération':operation, 'Etat Opération':etat_op, 'Serialized Operation':serialized_operation})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')		
		
		if titre == 'requete_memories_remote_operation_meo':
			try:
				for elt in rows:				
					ID_Memories_Entry, media_id, dateCréation, operation, etat_op, serialized_operation = elt						
					liste_messages.append({'Memories Entry ID':ID_Memories_Entry, 'Media ID':media_id, 'Date Création Opération':dateCréation, 'Opération':operation, 'Etat Opération':etat_op, 'Serialized Operation':serialized_operation})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')		
		
		if titre == 'requete_memories_upload_status':
			try:
				for elt in rows:				
					snap_id, media_id, uploadState, dateCreation, uploadProgress = elt						
					liste_messages.append({'Snap ID':snap_id, 'Media ID':media_id, 'Etat Upload':uploadState, 'Date':dateCreation, 'Progression Upload':uploadProgress})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')						

		##### TRAITEMENT JOURNAL.DB

	elif base_db == '.\com.snapchat.android\databases\journal.db':	
		
		if titre == 'requete_media_291':
			try:
				for elt in rows:				
					_id, path, key, dateUpdate, dateRead, taille = elt		
					try:
						path_fm_media = './com.snapchat.android/files/file_manager/media/'+key+'.0'
						path_fm_copy = './Rapport/files/file_manager/media/'+key+'.0'
						path_fm_thumb = './Rapport/files/file_manager/media/thumbnails/'+key+'.0.thumb.jpg'						
						if os.path.exists(path_fm_media) is True:						
							shutil.copyfile(path_fm_media, path_fm_copy)
							f = open(path_fm_copy, "rb")						
							im = Image.open(path_fm_copy)
							size = (100,100)
							im.thumbnail(size)
							im.save(path_fm_thumb)							
							href_thumb = './files/file_manager/media/thumbnails/'+key+'.0.thumb.jpg'
							href_media = './files/file_manager/media/'+key+'.0'						
							href_fm_media = '<center><a href="../'+href_media+'" target="_blank"><img src="../'+href_thumb+'" alt="Thumbnail non disponible"></a></center>'											
						else:
							href_fm_media = 'Fichier non disponible'				
					except:
						href_fm_media = 'Fichier non disponible'										
					liste_messages.append({'Journal ID':_id, 'Path':path, 'Nom Fichier':key, 'Thumbnail':href_fm_media, 'Date Update':dateUpdate, 'Date Dernière Lecture':dateRead, 'Taille (Ko)':taille})	
				return liste_messages	
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')					

		
		if titre == 'requete_media_229':
			try:
				for elt in rows:				
					_id, path, key, dateUpdate, dateRead, taille = elt								
					try:					
						path_gallery_media = './com.snapchat.android/files/gallery/files/'+key+'.0'
						path_gallery_copy = './Rapport/files/gallery/files/'+key+'.0'
						path_gallery_thumb = './Rapport/files/gallery/files/thumbnails/'+key+'.0.thumb.jpg'						
						if os.path.exists(path_gallery_media) is True:						
							shutil.copyfile(path_gallery_media, path_gallery_copy)
							im = Image.open(path_gallery_copy)
							size = (100,100)
							im.thumbnail(size)
							im.save(path_gallery_thumb)							
							href_thumb = './files/gallery/files/thumbnails/'+key+'.0.thumb.jpg'
							href_media = './files/gallery/files/'+key+'.0'						
							href_gallery_media = '<center><a href="../'+href_media+'" target="_blank"><img src="../'+href_thumb+'" alt="Thumbnail non disponible"></a></center>'											
						else:
							href_gallery_media = 'Fichier non disponible'				
					except:
						href_gallery_media = 'Fichier non disponible'	
					
					liste_messages.append({'Journal ID':_id, 'Path':path, 'Nom Fichier':key, 'Thumbnail':href_gallery_media, 'Date Update':dateUpdate, 'Date Dernière Lecture':dateRead, 'Taille (Ko)':taille})	
				return liste_messages	
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')						
			
		
		if titre == 'requete_media_228':
			try:
				for elt in rows:				
					_id, path, key, dateUpdate, dateRead, taille = elt				
					liste_messages.append({'Journal ID':_id, 'Path':path, 'Nom Fichier':key, 'Date Update':dateUpdate, 'Date Dernière Lecture':dateRead, 'Taille (Ko)':taille})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')						
	
		
		if titre == 'requete_media_290':
			try:
				for elt in rows:				
					_id, path, key, dateUpdate, dateRead, taille = elt								
					try:
						path_opera_media = './com.snapchat.android/files/file_manager/opera/'+key+'.0'
						path_opera_copy = './Rapport/files/file_manager/opera/'+key+'.0'
						path_opera_thumb = './Rapport/files/file_manager/opera/thumbnails/'+key+'.0.thumb.jpg'						
						if os.path.exists(path_opera_media) is True:						
							shutil.copyfile(path_opera_media, path_opera_copy)
							im = Image.open(path_opera_copy)
							size = (100,100)
							im.thumbnail(size)
							im.save(path_opera_thumb)							
							href_opera_thumb = './files/file_manager/opera/thumbnails/'+key+'.0.thumb.jpg'
							href__opera_media = './files/file_manager/opera/'+key+'.0'						
							href_opera_media = '<center><a href="../'+href_opera_media+'" target="_blank"><img src="../'+href_opera_thumb+'" alt="Thumbnail non disponible"></a></center>'											
						else:
							href_opera_media = 'Fichier non disponible'				
					except:
						href_opera_media = 'Fichier non disponible'		
					liste_messages.append({'Journal ID':_id, 'Path':path, 'Nom Fichier':key, 'Thumbnail':href_opera_media, 'Date Update':dateUpdate, 'Date Dernière Lecture':dateRead, 'Taille (Ko)':taille})	
				return liste_messages
			except:
				print('Erreur dans la requête précédente, vérifiez manuellement')						
	
