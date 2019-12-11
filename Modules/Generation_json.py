#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable = C0103, C0301, E0611, E0401

__auteur__ = "Yann-Ntech"
__version__ = "0.2 Beta"
__date__ = "20/09/2018"
__licence__ = "GNU GENERAL PUBLIC LICENSE Version 3"

"""
Création des fichiers JSON
"""

import json

def Creation_JSON(liste, titre):
    """
    Creation JSON
    """    
    path_json = './json/'+titre+'.json'
    with open(path_json, "w") as f:
        json_str = json.dumps(liste)        
        f.write(json_str)
    f.close
