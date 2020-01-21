# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
#
# This file is part of SALOME ADAO module
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D

"""
    Ce module sert pour charger les paramètres de configuration d'EFICAS
"""
# Modules Python
# print "passage dans la surcharge de configuration pour Adao"
import os, sys, string, types, re
import traceback
from PyQt5.QtGui  import *

# Modules Eficas
from InterfaceQT4 import configuration

# Classe de base permettant de lire, afficher
# et sauvegarder les fichiers utilisateurs
class CONFIG(configuration.configBase): # configuration.CONFIG_BASE):

  def __init__(self,appli,repIni):

    # self.labels_eficas = ['lang']
    self.labels_eficas = ['lang','rep_cata','catalogues','closeAutreCommande','closeFrameRechercheCommande','closeEntete','taille']
    configuration.configBase.__init__(self,appli,repIni)
    #~ configuration.CONFIG_BASE.__init__(self,appli,repIni)

    self.rep_user         = os.environ["HOME"]
    self.appli            = appli
    self.code             = appli.code
    # self.lang           = "fr"
    self.rep_ini          = repIni
    self.rep_mat          = " " # Compatbilite Aster
    self.savedir          = self.rep_user
    self.generator_module = "generator_adao"
    self.convert_module   = "convert_adao"

    # Format des catalogues...
    # (code, version, catalogue, formatIn, formatOut)
    # Il faut les mettre dans un tuple
    self.catalogues = (("ADAO", "V0", os.path.join(self.rep_ini, 'ADAO_Cata_V0.py'), "adao"),)
# JPA 21/09/2017 : self.catalogues = (("ADAO", "V0", os.path.join(self.rep_ini, 'ADAO_Cata_V0.py'), "python", "adao"),)

def make_config(appli,rep):

    return CONFIG(appli,rep)

def make_config_style(appli,rep):

    return None
