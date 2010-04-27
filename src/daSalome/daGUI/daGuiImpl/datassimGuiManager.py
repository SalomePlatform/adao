# -*- coding: iso-8859-1 -*-
#  Copyright (C) 2010 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

"""
This file centralizes the definitions and implementations of ui components used
in the GUI part of the module.
"""

__author__ = "aribes/gboulant"

import traceback
from PyQt4.QtCore import QObject
import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

from daGuiImpl.enumerate import Enumerate
#
# ==============================================================================
# Classes to manage the building of UI components
# ==============================================================================
#
UI_ELT_IDS = Enumerate([
        'DATASSIM_MENU_ID',
        ],offset=950)

ACTIONS_MAP={
}

class DatassimGuiUiComponentBuilder:
    """
    The initialisation of this class creates the graphic components involved
    in the GUI (menu, menu item, toolbar). A ui component builder should be
    created for each opened study and associated to its context (see usage in OMAGUI.py).
    """
    def __init__(self):
        self.initUiComponents()

    def initUiComponents(self):
        
        objectTR = QObject()

        # create top-level menu
        mid = sgPyQt.createMenu( "DATASSIM", -1, UI_ELT_IDS.DATASSIM_MENU_ID, sgPyQt.defaultMenuGroup() )
        # create toolbar
        tid = sgPyQt.createTool( "DATASSIM" )

