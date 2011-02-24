# -*- coding: utf-8 -*-
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
from PyQt4.QtCore import *        # Import from PyQT
from PyQt4 import QtGui,QtCore
import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

from daGuiImpl.enumerate import Enumerate
from daGuiImpl.adaoCase import AdaoCase
from daEficasWrapper.adaoEficasWrapper import AdaoEficasWrapper

from daUtils.adaoEficasEvent import *
import adaoGuiHelper
import adaoStudyEditor
import adaoLogger

__cases__ = {}

#
# ==============================================================================
# Classes to manage the building of UI components
# ==============================================================================
#
UI_ELT_IDS = Enumerate([
        'ADAO_MENU_ID',
        'NEW_ADAOCASE_ID',
        'OPEN_ADAOCASE_ID',
        'SAVE_ADAOCASE_ID',
        'SAVE_AS_ADAOCASE_ID',
        'CLOSE_ADAOCASE_ID',

        'EDIT_ADAOCASE_POP_ID',
        'YACS_EXPORT_POP_ID',
        ],offset=6950)

ACTIONS_MAP={
    UI_ELT_IDS.NEW_ADAOCASE_ID:"newAdaoCase",
    UI_ELT_IDS.OPEN_ADAOCASE_ID:"openAdaoCase",
    UI_ELT_IDS.SAVE_ADAOCASE_ID:"saveAdaoCase",
    UI_ELT_IDS.SAVE_AS_ADAOCASE_ID:"saveasAdaoCase",
    UI_ELT_IDS.CLOSE_ADAOCASE_ID:"closeAdaoCase",

    UI_ELT_IDS.EDIT_ADAOCASE_POP_ID:"editAdaoCase",
    UI_ELT_IDS.YACS_EXPORT_POP_ID:"exportCaseToYACS",
}


class AdaoCaseManager(EficasObserver):
  """
  Cette classe gére les cas ADAO et coordonne les GUI de SALOME (l'étude)
  et le GUI de l'objet Eficas (héritage du module Eficas)
  """

  def __init__(self):

    # Création d'un dictionnaire de cas
    # Key   == ref objet editor eficas (on est sur qu'elle est unique, cas duplication)
    # Value == objet AdaoCase()
    self.cases = {}

    # Création des deux managers
    self.salome_manager = AdaoGuiUiComponentBuilder()
    self.eficas_manager = AdaoEficasWrapper(parent=SalomePyQt.SalomePyQt().getDesktop())

    # On s'enregistre comme observer pour les évènements venant d'Eficas
    # Les évènements du salome_manager viennent par le biais de la méthode
    # processGUIEvent
    self.eficas_manager.addObserver(self)

    # Création du GUI Eficas
    self.eficas_manager.init_gui()

    # Création du viewer QT
    # Scroll Widget (pour les petites résolutions)
    area = QtGui.QScrollArea(SalomePyQt.SalomePyQt().getDesktop());
    area.setWidget(self.eficas_manager)
    area.setWidgetResizable(1)
    wmType = "ADAO View"
    self.eficas_viewId = sgPyQt.createView(wmType, area)

    # On interdit que la vue soit fermée
    # Cela simplifier grandement le code
    sgPyQt.setViewClosable(self.eficas_viewId, False)

    # On s'abonne au gestionnaire de selection
    self.selection_manager = sgPyQt.getSelection()
    QtCore.QObject.connect(self.selection_manager, QtCore.SIGNAL('currentSelectionChanged()'), self.currentSelectionChanged)

######
#
# Gestion de l'activation/désactivation du module
#
######

  def activate(self):
    self.eficas_manager.setEnabled(True)
    sgPyQt.activateView(self.eficas_viewId)
    self.harmonizeSelectionFromEficas()

  def deactivate(self):
    self.eficas_manager.setEnabled(False)

#######
#
# Gestion de la sélection entre le GUI d'Eficas
# et l'arbre d'étude de SALOME
#
#######

  # Depuis l'étude SALOME
  def currentSelectionChanged(self):
    """
    Cette méthode permet de changer le tab vu dans eficas
    selon la sélection de l'utilisateur dans l'étude SALOME
    """
    adaoLogger.debug("currentSelectionChanged")
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_editor, adao_case in self.cases.iteritems():
      if adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        self.eficas_manager.selectCase(adao_case.eficas_editor)
        break

  # Depuis Eficas
  def _processEficasTabChanged(self, eficasWrapper, eficasEvent):
    """
    Gestion de la synchonisation entre le tab courant d'Eficas
    et la selection dans l'étude SALOME
    """
    editor = eficasEvent.callbackId
    for case_editor, adao_case in self.cases.iteritems():
      if case_editor is editor:
        adaoGuiHelper.selectItem(adao_case.salome_study_item.GetID())
        break

  # On remet la sélection dans SALOME grâce au tab dans Eficas
  def harmonizeSelectionFromEficas(self):
    """
    Cette méthode permet d'harmoniser la sélection dans l'étude
    grâce au tab courant d'Eficas
    """
    if self.cases:
      # 1: Get current tab index in Eficas
      editor = self.eficas_manager.getCurrentEditor()
      # 2: sync with SALOME GUI is a tab is opened
      if editor:
        for case_editor, adao_case in self.cases.iteritems():
          if case_editor is editor:
            adaoGuiHelper.selectItem(adao_case.salome_study_item.GetID())
            break

#######
#
# Gestion de la création d'un nouveau cas
# 1: la fonction newAdaoCase est appelée par le GUI SALOME
# 2: la fonction _processEficasNewEvent est appelée par le manager EFICAS
#
#######

  def newAdaoCase(self):
    adaoLogger.debug("Création d'un nouveau cas adao")
    self.eficas_manager.adaofileNew(AdaoCase())

  def _processEficasNewEvent(self, eficasWrapper, eficasEvent):
    adao_case = eficasEvent.callbackId
    # Ajout dand l'étude
    salomeStudyId   = adaoGuiHelper.getActiveStudyId()
    salomeStudyItem = adaoStudyEditor.addInStudy(salomeStudyId, adao_case)
    # Affichage correct dans l'étude
    adaoGuiHelper.refreshObjectBrowser()
    adaoGuiHelper.selectItem(salomeStudyItem.GetID())
    # Finalisation des données du cas
    adao_case.salome_study_id   = salomeStudyId
    adao_case.salome_study_item = salomeStudyItem
    # Ajout du cas
    self.cases[adao_case.eficas_editor] = adao_case

#######
#
# Gestion de l'ouverture d'un cas
# 1: la fonction openAdaoCase est appelée par le GUI SALOME
# 2: la fonction _processEficasOpenEvent est appelée par le manager EFICAS
#
#######

# Rq: l'ouverture d'un cas adao est un cas particulier de la création d'un cas adao

  def openAdaoCase(self):
    adaoLogger.debug("Ouverture d'un cas adao")
    self.eficas_manager.adaoFileOpen(AdaoCase())

  def _processEficasOpenEvent(self, eficasWrapper, eficasEvent):
    self._processEficasNewEvent(eficasWrapper, eficasEvent)

#######
#
# Gestion de la sauvegarde d'un cas
# 1: la fonction saveAdaoCase est appelée par le GUI SALOME
# 1 bis: la fonction saveasAdaoCase est appelée par le GUI SALOME
# 2: la fonction _processEficasSaveEvent est appelée par le manager EFICAS
#
#######

  def saveAdaoCase(self):
    adaoLogger.debug("Sauvegarde du cas s'il y a modification")
    # A priori, l'utilisateur s'attend à sauvegarder le cas qui est ouvert
    # dans le GUI d'Eficas
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.iteritems():
      if adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        self.eficas_manager.adaoFileSave(adao_case)
        break

  def saveasAdaoCase(self):
    adaoLogger.debug("Sauvegarde du cas s'il y a modification (version save as)")
    # A priori, l'utilisateur s'attend à sauvegarder le cas qui est ouvert
    # dans le GUI d'Eficas
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.iteritems():
      if adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        self.eficas_manager.adaoFileSaveAs(adao_case)
        break

  def _processEficasSaveEvent(self, eficasWrapper, eficasEvent):
    adao_case = eficasEvent.callbackId
    # On met à jour l'étude
    adaoStudyEditor.updateItem(adao_case.salome_study_id, adao_case.salome_study_item, adao_case)
    # Affichage correct dans l'étude
    adaoGuiHelper.refreshObjectBrowser()
    adaoGuiHelper.selectItem(adao_case.salome_study_item.GetID())
    # Ajout du cas
    self.cases[adao_case.name] = adao_case

#######
#
# Gestion de la fermeture d'un cas
# 1: la fonction closeAdaoCase est appelée par le GUI SALOME
# 2: la fonction _processEficasCloseEvent est appelée par le manager EFICAS
#
#######

  def closeAdaoCase(self):
    adaoLogger.debug("Fermeture d'un cas")
    # A priori, l'utilisateur s'attend à sauvegarder le cas qui est ouvert
    # dans le GUI d'Eficas
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.iteritems():
      if adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        self.eficas_manager.adaoFileClose(adao_case)
        break

  def _processEficasCloseEvent(self, eficasWrapper, eficasEvent):
    editor = eficasEvent.callbackId
    # Recuperation du cas
    adao_case = self.cases[editor]
    # Suppression de l'objet dans l'étude
    adaoStudyEditor.removeItem(adao_case.salome_study_id, adao_case.salome_study_item)
    adaoGuiHelper.refreshObjectBrowser()
    # Suppression du cas
    del self.cases[editor]

#######
#
# Méthodes secondaires permettant de rediriger les évènements
# de SALOME et d'Eficas vers les bonnes méthodes de la classe
#
#######

  # Gestion des évènements venant du manager Eficas
  __processOptions={
      EficasEvent.EVENT_TYPES.CLOSE      : "_processEficasCloseEvent",
      EficasEvent.EVENT_TYPES.SAVE       : "_processEficasSaveEvent",
      EficasEvent.EVENT_TYPES.NEW        : "_processEficasNewEvent",
      EficasEvent.EVENT_TYPES.CLOSE      : "_processEficasCloseEvent",
      EficasEvent.EVENT_TYPES.OPEN       : "_processEficasOpenEvent",
      EficasEvent.EVENT_TYPES.TABCHANGED : "_processEficasTabChanged",
      EficasEvent.EVENT_TYPES.REOPEN     : "_processEficasReOpenEvent"
      }

  def processEficasEvent(self, eficasWrapper, eficasEvent):
      """
      Implementation of the interface EficasObserver. The implementation is a
      switch on the possible types of events defined in EficasEvent.EVENT_TYPES.
      @overload
      """
      functionName = self.__processOptions.get(eficasEvent.eventType, lambda : "_processEficasUnknownEvent")
      return getattr(self,functionName)(eficasWrapper, eficasEvent)

  def _processEficasUnknownEvent(self, eficasWrapper, eficasEvent):
    adaoLogger.error("Unknown Eficas Event")

  # Gestion des évènements venant du GUI de SALOME
  def processGUIEvent(self, actionId):
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
      adaoLogger.warning("The requested action is not implemented: " + str(actionId))

class AdaoGuiUiComponentBuilder:
    """
    The initialisation of this class creates the graphic components involved
    in the GUI (menu, menu item, toolbar). A ui component builder should be
    created for each opened study and associated to its context.
    """
    def __init__(self):
        self.initUiComponents()

    def initUiComponents(self):

        objectTR = QObject()

        # create top-level menu
        mid = sgPyQt.createMenu( "ADAO", -1, UI_ELT_IDS.ADAO_MENU_ID, sgPyQt.defaultMenuGroup() )
        # create toolbar
        tid = sgPyQt.createTool( "ADAO" )

        a = sgPyQt.createAction( UI_ELT_IDS.NEW_ADAOCASE_ID, "New case", "New case", "Create a new adao case", "" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.OPEN_ADAOCASE_ID, "Open case", "Open case", "Open an adao case", "" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.SAVE_ADAOCASE_ID, "Save case", "Save case", "Save an adao case", "" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.SAVE_AS_ADAOCASE_ID, "Save as case", "Save as case", "Save an adao case as", "" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.CLOSE_ADAOCASE_ID, "Close case", "Close case", "Close an adao case", "" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)

        # the following action are used in context popup
        a = sgPyQt.createAction( UI_ELT_IDS.CLOSE_ADAOCASE_ID, "Close case", "Close case", "Close the selected case", "" )

        a = sgPyQt.createAction( UI_ELT_IDS.EDIT_ADAOCASE_POP_ID, "Edit case", "Edit case", "Edit the selected study case", "" )
        a = sgPyQt.createAction( UI_ELT_IDS.YACS_EXPORT_POP_ID, "Export to YACS", "Export to YACS", "Generate a YACS graph executing this case", "" )

    def createPopupMenuOnItem(self,popup,salomeSudyId, item):
        if adaoStudyEditor.isValidAdaoCaseItem(salomeSudyId, item):
          popup.addAction( sgPyQt.action( UI_ELT_IDS.CLOSE_ADAOCASE_ID ) )

          popup.addAction( sgPyQt.action( UI_ELT_IDS.EDIT_ADAOCASE_POP_ID ) )
          popup.addAction( sgPyQt.action( UI_ELT_IDS.YACS_EXPORT_POP_ID ) )

        return popup

class AdaoGuiActionImpl(EficasObserver):
    """
    This class implements the ui actions concerning the management of oma study
    cases.
    """

    def __init__(self):
        pass
        # This dialog is created once so that it can be recycled for each call
        # to newOmaCase().
        #self.__dlgNewStudyCase = DlgNewStudyCase()
        self.__parent = SalomePyQt.SalomePyQt().getDesktop()
        self.__dlgEficasWrapper = AdaoEficasWrapper(parent=SalomePyQt.SalomePyQt().getDesktop())
        self.__dlgEficasWrapper.addObserver(self)
        self.__Eficas_viewId = -1

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

    def showEficas(self):
      if self.__Eficas_viewId == -1:
        self.__dlgEficasWrapper.init_gui()


        # Scroll Widget
        area = QtGui.QScrollArea(SalomePyQt.SalomePyQt().getDesktop());
        area.setWidget( self.__dlgEficasWrapper)
        area.setWidgetResizable(1)

        wmType = "ADAO View"
        self.__Eficas_viewId = sgPyQt.createView(wmType, area)
        sgPyQt.setViewClosable(self.__Eficas_viewId, False)
      else:
        if SalomePyQt.SalomePyQt().getActiveView() != self.__Eficas_viewId :
          result_activate = SalomePyQt.SalomePyQt().activateView(self.__Eficas_viewId)
          if result_activate == False:
            self.__dlgEficasWrapper.init_gui()

            # Scroll Widget
            area = QtGui.QScrollArea(SalomePyQt.SalomePyQt().getDesktop());
            area.setWidget( self.__dlgEficasWrapper)
            area.setWidgetResizable(1)

            wmType = "ADAO View"
            self.__Eficas_viewId = sgPyQt.createView(wmType, area)
            sgPyQt.setViewClosable(self.__Eficas_viewId, False)
        self.__dlgEficasWrapper.setEnabled(True)

    def activate(self):
      self.showEficas()

    def deactivate(self):
      self.showEficas()
      if self.__Eficas_viewId != -1:
        self.__dlgEficasWrapper.setEnabled(False)

    # Actions from SALOME GUI

    def newAdaoCase(self):

      adaoLogger.debug("newAdaoCase")
      self.showEficas()
      self.__dlgEficasWrapper.fileNew()

    def openAdaoCase(self):

      adaoLogger.debug("openAdaoCase")
      self.showEficas()
      global __cases__
      fichier = QtGui.QFileDialog.getOpenFileName(SalomePyQt.SalomePyQt().getDesktop(),
                                                  self.__dlgEficasWrapper.trUtf8('Ouvrir Fichier'),
                                                  self.__dlgEficasWrapper.CONFIGURATION.savedir,
                                                  self.__dlgEficasWrapper.trUtf8('JDC Files (*.comm);;''All Files (*)'))
      if fichier.isNull(): return
      new_case = AdaoCase()
      new_case.set_filename(str(fichier))
      new_case.set_name(str(fichier.split('/')[-1]))
      salomeStudyId   = adaoGuiHelper.getActiveStudyId()
      salomeStudyItem = adaoStudyEditor.addInStudy(salomeStudyId, new_case)
      case_key = (salomeStudyId, salomeStudyItem.GetID())
      __cases__[case_key] = new_case

      # Open file in Eficas
      self.__dlgEficasWrapper.Openfile(new_case.get_filename())
      callbackId = [salomeStudyId, salomeStudyItem]
      self.__dlgEficasWrapper.setCallbackId(callbackId)
      self.showEficas()
      adaoGuiHelper.refreshObjectBrowser()

    def editAdaoCase(self):

      adaoLogger.debug("editAdaoCase")
      global __cases__

      # Take study item
      salomeStudyId   = adaoGuiHelper.getActiveStudyId()
      salomeStudyItem = adaoGuiHelper.getSelectedItem(salomeStudyId)
      case_key = (salomeStudyId, salomeStudyItem.GetID())

      # ShowEficas, If case is an empty case - case is destroyed by reopen
      self.showEficas()
      try:
        case = __cases__[case_key]
        # Search if case is in Eficas !
        callbackId = [salomeStudyId, salomeStudyItem]
        case_open_in_eficas = self.__dlgEficasWrapper.selectCase(callbackId)

        # If case is not in eficas Open It !
        if case_open_in_eficas == False:
          if case.get_filename() != "":
            self.__dlgEficasWrapper.Openfile(case.get_filename())
            callbackId = [salomeStudyId, salomeStudyItem]
            self.__dlgEficasWrapper.setCallbackId(callbackId)
      except:
        # Case has been destroyed - create a new one
        self.__dlgEficasWrapper.fileNew()

    def closeAdaoCase(self):

      adaoLogger.debug("closeAdaoCase")
      global __cases__

      # First step: get selected case
      salomeStudyId   = adaoGuiHelper.getActiveStudyId()
      salomeStudyItem = adaoGuiHelper.getSelectedItem(salomeStudyId)

      # Check if there is a selected case
      if salomeStudyItem is None:
        print "[Close case] Please select a case"
        return

      callbackId = [salomeStudyId, salomeStudyItem]
      case_open_in_eficas = self.__dlgEficasWrapper.selectCase(callbackId)

      # If case is in eficas close it !
      if case_open_in_eficas:
        # fileClose: remove the CallbackId
        # fileClose: sends a destroy event
        self.__dlgEficasWrapper.fileClose()
      else:
        # Test if case exists
        case_key = (salomeStudyId, salomeStudyItem.GetID())
        if __cases__.has_key(case_key):
          __cases__.pop(case_key)
          adaoStudyEditor.removeItem(salomeStudyId, salomeStudyItem)
          adaoGuiHelper.refreshObjectBrowser()

    def saveAdaoCase(self):

      adaoLogger.debug("saveAdaoCase")
      global __cases__

    def saveasAdaoCase(self):

      adaoLogger.debug("saveasAdaoCase")
      global __cases__

    def exportCaseToYACS(self):

      adaoLogger.debug("exportCaseToYACS")
      global __cases__

      # Get case from study
      salomeStudyId   = adaoGuiHelper.getActiveStudyId()
      salomeStudyItem = adaoGuiHelper.getSelectedItem(salomeStudyId)
      case_key = (salomeStudyId, salomeStudyItem.GetID())
      case = __cases__[case_key]

      # Generates YACS schema and export it
      msg = case.exportCaseToYACS()

      # If msg is not empty -> error found
      if msg != "":
        adaoGuiHelper.gui_warning(self.__parent, msg)

    # ==========================================================================
    # Processing notifications from adaoEficasWrapper
    #
    __processOptions={
        EficasEvent.EVENT_TYPES.CLOSE   : "_processEficasCloseEvent",
        EficasEvent.EVENT_TYPES.SAVE    : "_processEficasSaveEvent",
        EficasEvent.EVENT_TYPES.NEW     : "_processEficasNewEvent",
        EficasEvent.EVENT_TYPES.OPEN    : "_processEficasOpenEvent",
        EficasEvent.EVENT_TYPES.REOPEN  : "_processEficasReOpenEvent"
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

      new_case = AdaoCase()
      case_name = eficasWrapper.getCaseName()
      new_case.set_name(case_name)
      salomeStudyId   = adaoGuiHelper.getActiveStudyId()
      salomeStudyItem = adaoStudyEditor.addInStudy(salomeStudyId, new_case)
      case_key = (salomeStudyId, salomeStudyItem.GetID())
      __cases__[case_key] = new_case
      adaoGuiHelper.refreshObjectBrowser()
      callbackId = [salomeStudyId, salomeStudyItem]
      self.__dlgEficasWrapper.setCallbackId(callbackId)

      # We need to select the case
      adaoGuiHelper.selectItem(salomeStudyItem.GetID())


    def _processEficasOpenEvent(self, eficasWrapper, eficasEvent):
      global __cases__

      # Ouverture du fichier
      self.__dlgEficasWrapper.Openfile(self.__dlgEficasWrapper.getOpenFileName())

      # Creation d'un nouveau cas
      new_case = AdaoCase()
      salomeStudyId   = adaoGuiHelper.getActiveStudyId()
      salomeStudyItem = adaoStudyEditor.addInStudy(salomeStudyId, new_case)
      case_key = (salomeStudyId, salomeStudyItem.GetID())
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
          old_case_key = (targetSalomeStudyId, targetSalomeStudyItem.GetID())
          case =__cases__[old_case_key]

          # Set new informations
          case.set_name(case_name)
          if str(case_name).startswith("Untitled"):
            pass
          else:
            case.set_filename(file_case_name)
          adaoStudyEditor.updateItem(targetSalomeStudyId, targetSalomeStudyItem, case)

          # Case key changed !
          #new_case_key = (targetSalomeStudyId, targetSalomeStudyItem.GetID())
          # A ne pas inverser !!!
          #__cases__.pop(old_case_key)
          #__cases__[new_case_key] = case

          adaoGuiHelper.refreshObjectBrowser()

    def _processEficasDestroyEvent(self, eficasWrapper, eficasEvent):
        global __cases__
        callbackId = eficasEvent.callbackId
        if callbackId is None:
            raise DevelException("the callback data should not be None. Can't guess what are the study and case")
        [targetSalomeStudyId,targetSalomeStudyItem] = callbackId
        if ( targetSalomeStudyId is None ) or ( targetSalomeStudyItem is None ):
            raise DevelException("the parameters targetSalomeStudyId and targetSalomeStudyItem should not be None")

        case_key = (targetSalomeStudyId, targetSalomeStudyItem.GetID())
        __cases__.pop(case_key)
        adaoStudyEditor.removeItem(targetSalomeStudyId, targetSalomeStudyItem)
        adaoGuiHelper.refreshObjectBrowser()

    # Deprecated
    # Normalement on ne ferme plus le GUI donc on ne passe plus par là
    def _processEficasReOpenEvent(self, eficasWrapper, eficasEvent):

      adaoLogger.warning("_processEficasReOpenEvent")
      global __cases__

      try:
        callbackId = eficasEvent.callbackId
        [salomeStudyId, salomeStudyItem] = callbackId
        case_key = (salomeStudyId, salomeStudyItem.GetID())
        case = __cases__[case_key]
        # Search if case is in Eficas !
        callbackId = [salomeStudyId, salomeStudyItem]
        case_open_in_eficas = self.__dlgEficasWrapper.selectCase(callbackId)
        # If case is not in eficas Open It !
        if case_open_in_eficas == False:
          if case.get_filename() != "":
            self.__dlgEficasWrapper.Openfile(case.get_filename())
            callbackId = [salomeStudyId, salomeStudyItem]
            self.__dlgEficasWrapper.setCallbackId(callbackId)
          else:
            # Since I am an empty case I destroy myself before reloading
            adaoStudyEditor.removeItem(salomeStudyId, salomeStudyItem)
            adaoGuiHelper.refreshObjectBrowser()
            __cases__.pop(case_key)
            callbackId = [salomeStudyId, salomeStudyItem]
            self.__dlgEficasWrapper.removeCallbackId(callbackId)
      except:
        print "Oups - cannot reopen case !"
        traceback.print_exc()

    def _processEficasUnknownEvent(self, eficasWrapper, eficasEvent):
      print "Unknown Eficas Event"
