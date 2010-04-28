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
from daGuiImpl.datassimCase import DatassimCase
from daEficasWrapper.datassimEficasWrapper import DatassimEficasWrapper
from daEficasWrapper.eficasWrapper import EficasObserver
from daEficasWrapper.eficasWrapper import EficasEvent
import datassimGuiHelper
import datassimStudyEditor

__cases__ = {}

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

class DatassimGuiActionImpl(EficasObserver):
    """
    This class implements the ui actions concerning the management of oma study
    cases.
    """
    __dlgEficasWrapper = None

    def __init__(self):
        pass
        # This dialog is created once so that it can be recycled for each call
        # to newOmaCase().
        #self.__dlgNewStudyCase = DlgNewStudyCase()
        self.__dlgEficasWrapper = DatassimEficasWrapper(parent=SalomePyQt.SalomePyQt().getDesktop())
        self.__dlgEficasWrapper.addObserver(self)

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
      self.__dlgEficasWrapper.displayNew()

    # ==========================================================================
    # Processing notifications from eficas
    #
    __processOptions={
        EficasEvent.EVENT_TYPES.CLOSE : "_processEficasCloseEvent",
        EficasEvent.EVENT_TYPES.SAVE  : "_processEficasSaveEvent",
        EficasEvent.EVENT_TYPES.NEW  : "_processEficasNewEvent",
        EficasEvent.EVENT_TYPES.DESTROY  : "_processEficasDestroyEvent"
        }
    def processEficasEvent(self, eficasWrapper, eficasEvent):
        """
        Implementation of the interface EficasObserver. The implementation is a
        switch on the possible types of events defined in EficasEvent.EVENT_TYPES.
        @overload
        """
        functionName = self.__processOptions.get(eficasEvent.eventType, lambda : "_processEficasUnknownEvent")
        return getattr(self,functionName)(eficasWrapper, eficasEvent)

    def _processEficasCloseEvent(self, eficasWrapper, eficasEvent):
        print "This is the process of EficasCloseEvent"
        print "Remove datassim case in study if empty..."
        pass

    def _processEficasNewEvent(self, eficasWrapper, eficasEvent):
      global __cases__
      new_case = DatassimCase()
      salomeStudyId   = datassimGuiHelper.getActiveStudyId()
      salomeStudyItem = datassimStudyEditor.addInStudy(salomeStudyId, new_case)
      case_key = (salomeStudyId, salomeStudyItem)
      __cases__[case_key] = new_case
      datassimGuiHelper.refreshObjectBrowser()
      callbackId = [salomeStudyId, salomeStudyItem]
      self.__dlgEficasWrapper.setCallbackId(callbackId)

    def _processEficasSaveEvent(self, eficasWrapper, eficasEvent):
        callbackId = eficasEvent.callbackId
        if callbackId is None:
            raise DevelException("the callback data should not be None. Can't guess what are the study and case")
        [targetSalomeStudyId,targetSalomeStudyItem] = callbackId
        if ( targetSalomeStudyId is None ) or ( targetSalomeStudyItem is None ):
            raise DevelException("the parameters targetSalomeStudyId and targetSalomeStudyItem should not be None")

        # Get Editor All infos we need !
        file_name = eficasWrapper.getCaseName()
        if file_name != "" :
          case_key = (targetSalomeStudyId, targetSalomeStudyItem)
          case =__cases__[case_key]
          case.set_name(file_name)
          datassimStudyEditor.updateItem(targetSalomeStudyId, targetSalomeStudyItem, case)
          datassimGuiHelper.refreshObjectBrowser()

    def _processEficasDestroyEvent(self, eficasWrapper, eficasEvent):
        callbackId = eficasEvent.callbackId
        if callbackId is None:
            raise DevelException("the callback data should not be None. Can't guess what are the study and case")
        [targetSalomeStudyId,targetSalomeStudyItem] = callbackId
        if ( targetSalomeStudyId is None ) or ( targetSalomeStudyItem is None ):
            raise DevelException("the parameters targetSalomeStudyId and targetSalomeStudyItem should not be None")

        case_key = (targetSalomeStudyId, targetSalomeStudyItem)
        __cases__.pop(case_key)
        datassimStudyEditor.removeItem(targetSalomeStudyId, targetSalomeStudyItem)
        datassimGuiHelper.refreshObjectBrowser()

    def _processEficasUnknownEvent(self, eficasWrapper, eficasEvent):
      print "Unknown Eficas Event"
