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
from PyQt4 import QtGui,QtCore
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
        'OPEN_DATASSIMCASE_ID',
        'EDIT_DATASSIMCASE_POP_ID',
        'DELETE_DATASSIMCASE_POP_ID',
        'YACS_EXPORT_POP_ID',
        ],offset=950)

ACTIONS_MAP={
    UI_ELT_IDS.NEW_DATASSIMCASE_ID:"newDatassimCase",
    UI_ELT_IDS.OPEN_DATASSIMCASE_ID:"openDatassimCase",
    UI_ELT_IDS.EDIT_DATASSIMCASE_POP_ID:"editDatassimCase",
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
        a = sgPyQt.createAction( UI_ELT_IDS.OPEN_DATASSIMCASE_ID, "Open case", "Open case", "Open a datassim case", "" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)

        # the following action are used in context popup
        a = sgPyQt.createAction( UI_ELT_IDS.EDIT_DATASSIMCASE_POP_ID, "Edit case", "Edit case", "Edit the selected study case", "" )
        a = sgPyQt.createAction( UI_ELT_IDS.DELETE_DATASSIMCASE_POP_ID, "Delete case", "Delete case", "Delete the selected study case", "" )
        a = sgPyQt.createAction( UI_ELT_IDS.YACS_EXPORT_POP_ID, "Export to YACS", "Export to YACS", "Generate a YACS graph executing this case", "" )

    def createPopupMenuOnItem(self,popup,salomeSudyId, item):
        if datassimStudyEditor.isValidDatassimCaseItem(salomeSudyId, item):
          popup.addAction( sgPyQt.action( UI_ELT_IDS.EDIT_DATASSIMCASE_POP_ID ) )
          popup.addAction( sgPyQt.action( UI_ELT_IDS.DELETE_DATASSIMCASE_POP_ID ) )
          popup.addAction( sgPyQt.action( UI_ELT_IDS.YACS_EXPORT_POP_ID ) )

        return popup

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

    def openDatassimCase(self):
      global __cases__
      fichier = QtGui.QFileDialog.getOpenFileName(SalomePyQt.SalomePyQt().getDesktop(),
                                                  self.__dlgEficasWrapper.trUtf8('Ouvrir Fichier'),
                                                  self.__dlgEficasWrapper.CONFIGURATION.savedir,
                                                  self.__dlgEficasWrapper.trUtf8('JDC Files (*.comm);;''All Files (*)'))
      if fichier.isNull(): return
      new_case = DatassimCase()
      new_case.set_filename(str(fichier))
      new_case.set_name(str(fichier.split('/')[-1]))
      salomeStudyId   = datassimGuiHelper.getActiveStudyId()
      salomeStudyItem = datassimStudyEditor.addInStudy(salomeStudyId, new_case)
      case_key = (salomeStudyId, salomeStudyItem.GetName())
      __cases__[case_key] = new_case

      # Open file in Eficas
      self.__dlgEficasWrapper.Openfile(new_case.get_filename())
      callbackId = [salomeStudyId, salomeStudyItem]
      self.__dlgEficasWrapper.setCallbackId(callbackId)
      self.__dlgEficasWrapper.show()
      datassimGuiHelper.refreshObjectBrowser()

    def editDatassimCase(self):
      global __cases__
      salomeStudyId   = datassimGuiHelper.getActiveStudyId()
      salomeStudyItem = datassimGuiHelper.getSelectedItem(salomeStudyId)
      case_key = (salomeStudyId, salomeStudyItem.GetName())
      try:
        case = __cases__[case_key]
        self.__dlgEficasWrapper.Openfile(case.get_filename())
        callbackId = [salomeStudyId, salomeStudyItem]
        self.__dlgEficasWrapper.setCallbackId(callbackId)
        self.__dlgEficasWrapper.show()
      except:
        print "Oups - cannot edit case !"
        traceback.print_exc()


    # ==========================================================================
    # Processing notifications from eficas
    #
    __processOptions={
        EficasEvent.EVENT_TYPES.CLOSE : "_processEficasCloseEvent",
        EficasEvent.EVENT_TYPES.SAVE  : "_processEficasSaveEvent",
        EficasEvent.EVENT_TYPES.NEW  : "_processEficasNewEvent",
        EficasEvent.EVENT_TYPES.DESTROY  : "_processEficasDestroyEvent",
        EficasEvent.EVENT_TYPES.OPEN  : "_processEficasOpenEvent"
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
        pass

    def _processEficasNewEvent(self, eficasWrapper, eficasEvent):
      global __cases__
      new_case = DatassimCase()
      salomeStudyId   = datassimGuiHelper.getActiveStudyId()
      salomeStudyItem = datassimStudyEditor.addInStudy(salomeStudyId, new_case)
      case_key = (salomeStudyId, salomeStudyItem.GetName())
      __cases__[case_key] = new_case
      datassimGuiHelper.refreshObjectBrowser()
      callbackId = [salomeStudyId, salomeStudyItem]
      self.__dlgEficasWrapper.setCallbackId(callbackId)

    def _processEficasOpenEvent(self, eficasWrapper, eficasEvent):
      global __cases__

      # Ouverture du fichier
      self.__dlgEficasWrapper.Openfile(self.__dlgEficasWrapper.getOpenFileName())

      # Creation d'un nouveau cas
      new_case = DatassimCase()
      salomeStudyId   = datassimGuiHelper.getActiveStudyId()
      salomeStudyItem = datassimStudyEditor.addInStudy(salomeStudyId, new_case)
      case_key = (salomeStudyId, salomeStudyItem.GetName())
      __cases__[case_key] = new_case

      # Connexion du nouveau cas
      callbackId = [salomeStudyId, salomeStudyItem]
      self.__dlgEficasWrapper.setCallbackId(callbackId)

      # On sauvegarde le cas
      self._processEficasSaveEvent(self.__dlgEficasWrapper, None, callbackId)

    def _processEficasSaveEvent(self, eficasWrapper, eficasEvent, callbackId=None):
        global __cases__
        if callbackId is None:
          callbackId = eficasEvent.callbackId
          if callbackId is None:
            raise DevelException("the callback data should not be None. Can't guess what are the study and case")
          [targetSalomeStudyId,targetSalomeStudyItem] = callbackId
          if ( targetSalomeStudyId is None ) or ( targetSalomeStudyItem is None ):
            raise DevelException("the parameters targetSalomeStudyId and targetSalomeStudyItem should not be None")
        else:
          [targetSalomeStudyId,targetSalomeStudyItem] = callbackId

        # Get Editor All infos we need !
        case_name = eficasWrapper.getCaseName()
        file_case_name = eficasWrapper.getFileCaseName()
        if case_name != "" :
          # Get case
          old_case_key = (targetSalomeStudyId, targetSalomeStudyItem.GetName())
          case =__cases__[old_case_key]

          # Set new informations
          case.set_name(case_name)
          case.set_filename(file_case_name)
          datassimStudyEditor.updateItem(targetSalomeStudyId, targetSalomeStudyItem, case)

          # Case key changed !
          new_case_key = (targetSalomeStudyId, targetSalomeStudyItem.GetName())
          # A ne pas inverser !!!
          __cases__.pop(old_case_key)
          __cases__[new_case_key] = case

          datassimGuiHelper.refreshObjectBrowser()

    def _processEficasDestroyEvent(self, eficasWrapper, eficasEvent):
        global __cases__
        callbackId = eficasEvent.callbackId
        if callbackId is None:
            raise DevelException("the callback data should not be None. Can't guess what are the study and case")
        [targetSalomeStudyId,targetSalomeStudyItem] = callbackId
        if ( targetSalomeStudyId is None ) or ( targetSalomeStudyItem is None ):
            raise DevelException("the parameters targetSalomeStudyId and targetSalomeStudyItem should not be None")

        case_key = (targetSalomeStudyId, targetSalomeStudyItem.GetName())
        __cases__.pop(case_key)
        datassimStudyEditor.removeItem(targetSalomeStudyId, targetSalomeStudyItem)
        datassimGuiHelper.refreshObjectBrowser()

    def _processEficasUnknownEvent(self, eficasWrapper, eficasEvent):
      print "Unknown Eficas Event"
