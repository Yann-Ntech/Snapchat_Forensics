#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable = C0103, C0301, E0611, E0401

__auteur__ = "Yann-Ntech"
__version__ = "0.2 Beta"
__date__ = "20/09/2018"
__licence__ = "GNU GENERAL PUBLIC LICENSE Version 3"

from os import path
import os.path
import os
from inspect import getsourcefile

def Rapport():
	
	# Inputs	
	cas = input("N° de procédure : ")
	try:
		cas = cas.replace('/','_')
	except:
		pass
	sc = input("N° de scellé : ")
	try:
		sc = sc.replace('/','_')
	except:
		pass
	analyst = input("Analyste : ")	
	unité = input("Service : ")	
	
	# Dossier
	path_script = path.dirname(path.abspath(getsourcefile(lambda: 0)))
	path_cas = path_script+'/'+cas
	
	if not os.path.exists(path_cas):
		os.mkdir(path_cas)		
		print("Dossier " , path_cas ,  " créé.")
		
		test = path_cas+'/test.html'
		
		print(path_script)
		print(path_cas)
		print(test)
		
		with open('test', 'w', encoding='utf-8') as f:
			f.write("""
		CECI EST UN TEST	
		""")
		
	else:    
		print("Dossier " , path_cas ,  " déjà existant, veuillez supprimer l'ancien dossier avant de relancer une analyse.")
	
	# Génération HTML	
	
