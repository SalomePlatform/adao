# -*- coding: utf-8 -*-
"""
    Ce module sert pour charger les paramètres de configuration d'EFICAS
"""
# Modules Python
print "passage dans la surcharge de configuration pour Datassim"
import os, sys, string, types, re
import traceback
from PyQt4.QtGui  import *

# Modules Eficas
from Editeur import utils

# Classe de base permettant de lire, afficher
# et sauvegarder les fichiers utilisateurs 
class CONFIG:

  def __init__(self,appli,repIni):

    self.rep_user = os.environ["HOME"]
    self.appli   = appli  
    self.code    = appli.code
    self.rep_ini = repIni
    self.savedir      = self.rep_user
    self.generator_module = "generator_datassim"
    self.convert_module = "convert_datassim"

    # Format des catalogues...
    # (code,version,catalogue,formatIn) et  ,formatOut) ?
    self.catalogues = []
    self.catalogues.append(["DATASSIM", "V0", os.path.join(self.rep_ini, 'DATASSIM_Cata_V0.py'), "datassim"])

def make_config(appli,rep):

    return CONFIG(appli,rep)

def make_config_style(appli,rep):

    return None
