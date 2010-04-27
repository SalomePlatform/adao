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
        'NEW_DATASSIMCASE_ID',
        ],offset=950)

ACTIONS_MAP={
    UI_ELT_IDS.NEW_DATASSIMCASE_ID:"newDatassimCase",
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

        a = sgPyQt.createAction( UI_ELT_IDS.NEW_DATASSIMCASE_ID, "New case", "New case", "Create a new datassim case", "" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)

class DatassimGuiActionImpl():
    """
    This class implements the ui actions concerning the management of oma study
    cases.
    """
    __dlgNewStudyCase = None
    __dlgEficasWrapper = None

    def __init__(self):
        pass
        # This dialog is created once so that it can be recycled for each call
        # to newOmaCase().
        #self.__dlgNewStudyCase = DlgNewStudyCase()
        #self.__dlgEficasWrapper = OmaEficasWrapper(parent=SalomePyQt.SalomePyQt().getDesktop())

    # ==========================================================================
    # Processing of ui actions
    #
    def processAction(self,actionId):
        """
        Main switch function for ui actions processing
        """
        if ACTIONS_MAP.has_key(actionId):
            try:
                functionName = ACTIONS_MAP[actionId]
                getattr(self,functionName)()
            except:
                traceback.print_exc()
        else:
            msg = "The requested action is not implemented: " + str(actionId)
            print msg

    def newDatassimCase(self):
      print "newDatassimCase"
