# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import os, sys

#
# Configuration de Eficas
# =======================
#
# Positionnee a repin au debut, mise a jour dans configuration
repIni=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,repIni)
#
# Sert comme directory initial des QFileDialog
initialdir = os.getcwd()
#
# Traductions et codages
#
# Indique la langue du catalogue utilisee pour les chaines d'aide : fr ou ang
# lang = 'fr'
# Traduction des labels de boutons ou autres
lookfor = os.path.abspath(os.path.join(os.path.dirname(__file__),"../resources"))
if os.path.exists(lookfor):
    translatorFichier = os.path.join(lookfor, "adao")
else:
    # Ce nom sera complete par EFICAS avec _<LANG>.qm
    translatorFichier = os.environ["ADAO_ENGINE_ROOT_DIR"] + "/share/resources/adao/adao"
#
# Pilotage des sous-fenetres d'EFICAS
closeAutreCommande = True
closeFrameRechercheCommande = True
closeFrameRechercheCommandeSurPageDesCommandes = True
closeEntete = True
closeArbre = True
taille = 800
nombreDeBoutonParLigne = 2

catalogues = (("ADAO", "V0", os.path.join(repIni, 'ADAO_Cata_V0.py'), "adao"),)
readerModule = "convert_adao"
writerModule = "generator_adao"
