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

"""
This file centralizes the definitions and implementations of ui components used
in the GUI part of the module.
"""

__author__ = "aribes/gboulant"

import traceback
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QScrollArea
import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

from daUtils.enumerate import Enumerate
from daGuiImpl.adaoCase import AdaoCase
from daEficasWrapper.adaoEficasWrapper import AdaoEficasWrapper

from daUtils.adaoEficasEvent import *
from . import adaoGuiHelper
from . import adaoStudyEditor
from daUtils import adaoLogger

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
        'VALIDATE_ADAOCASE_ID',
        'SHOWTREE_ADAOCASE_ID',
        'CLOSE_ADAOCASE_ID',
        'YACS_EXPORT_ID',
        ],offset=6950)

ACTIONS_MAP={
    UI_ELT_IDS.NEW_ADAOCASE_ID:"newAdaoCase",
    UI_ELT_IDS.OPEN_ADAOCASE_ID:"openAdaoCase",
    UI_ELT_IDS.SAVE_ADAOCASE_ID:"saveAdaoCase",
    UI_ELT_IDS.SAVE_AS_ADAOCASE_ID:"saveasAdaoCase",
    UI_ELT_IDS.VALIDATE_ADAOCASE_ID:"validateAdaoCase",
    UI_ELT_IDS.SHOWTREE_ADAOCASE_ID:"showTreeAdaoCase",
    UI_ELT_IDS.CLOSE_ADAOCASE_ID:"closeAdaoCase",
    UI_ELT_IDS.YACS_EXPORT_ID:"exportCaseToYACS",
}


class AdaoCaseManager(EficasObserver):
  """
  Cette classe gere les cas ADAO et coordonne les GUI de SALOME (l'etude)
  et le GUI de l'objet Eficas (heritage du module Eficas)
  """

  def __init__(self):

    # Creation d'un dictionnaire de cas
    # Key   == ref objet editor eficas (on est sur qu'elle est unique, cas duplication)
    # Value == objet AdaoCase()
    self.cases = {}

    # Creation des deux managers
    self.salome_manager = AdaoGuiUiComponentBuilder()
    self.eficas_manager = AdaoEficasWrapper(parent=SalomePyQt.SalomePyQt().getDesktop())

    # On s'enregistre comme observer pour les evenements venant d'Eficas
    # Les evenements du salome_manager viennent par le biais de la methode
    # processGUIEvent
    self.eficas_manager.addObserver(self)

    # Creation du GUI Eficas
    self.eficas_manager.init_gui()

    # Creation du viewer QT
    # Scroll Widget (pour les petites resolutions)
    area = QScrollArea(SalomePyQt.SalomePyQt().getDesktop());
    from PyQt5.QtWidgets  import QGridLayout
    gridLayout = QGridLayout(area)
    gridLayout.addWidget(self.eficas_manager)
    area.setWidgetResizable(1)
    wmType = "ADAO View"
    self.eficas_viewId = sgPyQt.createView(wmType, area)

    # On interdit que la vue soit fermee
    # Cela simplifier grandement le code
    sgPyQt.setViewClosable(self.eficas_viewId, False)

    # On s'abonne au gestionnaire de selection
    self.selection_manager = sgPyQt.getSelection()
    self.selection_manager.currentSelectionChanged.connect(self.currentSelectionChanged)

######
#
# Gestion de l'activation/desactivation du module
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
# Gestion de la selection entre le GUI d'Eficas
# et l'arbre d'etude de SALOME
#
#######

  # Depuis l'etude SALOME
  def currentSelectionChanged(self):
    """
    Cette methode permet de changer le tab vu dans eficas
    selon la selection de l'utilisateur dans l'etude SALOME
    """
    adaoLogger.debug("currentSelectionChanged")
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    if salomeStudyItem is not None:
      for case_editor, adao_case in self.cases.items():
        if hasattr(salomeStudyItem,"GetID") and adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
          self.eficas_manager.selectCase(adao_case.eficas_editor)
          break

  # Depuis Eficas
  def _processEficasTabChanged(self, eficasWrapper, eficasEvent):
    """
    Gestion de la synchonisation entre le tab courant d'Eficas
    et la selection dans l'etude SALOME
    """
    editor = eficasEvent.callbackId
    for case_editor, adao_case in self.cases.items():
      if case_editor is editor:
        adaoGuiHelper.selectItem(adao_case.salome_study_item.GetID())
        break

  # On remet la selection dans SALOME grâce au tab dans Eficas
  def harmonizeSelectionFromEficas(self):
    """
    Cette methode permet d'harmoniser la selection dans l'etude
    grâce au tab courant d'Eficas
    """
    if self.cases:
      # 1: Get current tab index in Eficas
      editor = self.eficas_manager.getCurrentEditor()
      # 2: sync with SALOME GUI is a tab is opened
      if editor:
        for case_editor, adao_case in self.cases.items():
          if case_editor is editor:
            adaoGuiHelper.selectItem(adao_case.salome_study_item.GetID())
            break

#######
#
# Gestion de la creation d'un nouveau cas
# 1: la fonction newAdaoCase est appelee par le GUI SALOME
# 2: la fonction _processEficasNewEvent est appelee par le manager EFICAS
#
#######

  def newAdaoCase(self):
    adaoLogger.debug("Creation d'un nouveau cas adao")
    self.eficas_manager.adaofileNew(AdaoCase())

  def _processEficasNewEvent(self, eficasWrapper, eficasEvent):
    adao_case = eficasEvent.callbackId
    # Ajout dand l'etude
    #~ salomeStudyId   = adaoGuiHelper.getActiveStudyId()
    salomeStudyItem = adaoStudyEditor.addInStudy( adao_case ) # salomeStudyId, adao_case)
    # Affichage correct dans l'etude
    adaoGuiHelper.refreshObjectBrowser()
    adaoGuiHelper.selectItem(salomeStudyItem.GetID())
    # Finalisation des donnees du cas
    #~ adao_case.salome_study_id   = salomeStudyId
    adao_case.salome_study_item = salomeStudyItem
    # Ajout du cas
    self.cases[adao_case.eficas_editor] = adao_case

#######
#
# Gestion de l'ouverture d'un cas
# 1: la fonction openAdaoCase est appelee par le GUI SALOME
# 2: la fonction _processEficasOpenEvent est appelee par le manager EFICAS
#
#######

# Rq: l'ouverture d'un cas adao est un cas particulier de la creation d'un cas adao

  def openAdaoCase(self):
    adaoLogger.debug("Ouverture d'un cas adao")
    self.eficas_manager.adaoFileOpen(AdaoCase())

  def _processEficasOpenEvent(self, eficasWrapper, eficasEvent):
    self._processEficasNewEvent(eficasWrapper, eficasEvent)

#######
#
# Gestion de la sauvegarde d'un cas
# 1: la fonction saveAdaoCase est appelee par le GUI SALOME
# 1 bis: la fonction saveasAdaoCase est appelee par le GUI SALOME
# 2: la fonction _processEficasSaveEvent est appelee par le manager EFICAS
#
#######

  def saveAdaoCase(self):
    adaoLogger.debug("Sauvegarde du cas s'il y a modification (version save)")
    # A priori, l'utilisateur s'attend a sauvegarder le cas qui est ouvert
    # dans le GUI d'Eficas
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.items():
      if hasattr(salomeStudyItem,"GetID") and adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        if not adao_case.isOk():
          adaoLogger.debug("Cas invalide, donc il est sauvegarde, mais il ne peut pas etre exporte vers YACS ensuite")
        self.eficas_manager.adaoFileSave(adao_case)
        break

  def saveasAdaoCase(self):
    adaoLogger.debug("Sauvegarde du cas s'il y a modification (version save as)")
    # A priori, l'utilisateur s'attend a sauvegarder le cas qui est ouvert
    # dans le GUI d'Eficas
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.items():
      if hasattr(salomeStudyItem,"GetID") and adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        if not adao_case.isOk():
          adaoLogger.debug("Cas invalide, donc il est sauvegarde, mais il ne peut pas etre exporte vers YACS ensuite")
        self.eficas_manager.adaoFileSaveAs(adao_case)
        break

  def _processEficasSaveEvent(self, eficasWrapper, eficasEvent):
    adao_case = eficasEvent.callbackId
    # On met a jour l'etude
    adaoStudyEditor.updateItem(adao_case.salome_study_item, adao_case) # adao_case.salome_study_id, adao_case.salome_study_item, adao_case)
    # Affichage correct dans l'etude
    adaoGuiHelper.refreshObjectBrowser()
    adaoGuiHelper.selectItem(adao_case.salome_study_item.GetID())
    # Ajout du cas
    self.cases[adao_case.name] = adao_case

#######
#
# Gestion de la fermeture d'un cas
# 1: la fonction closeAdaoCase est appelee par le GUI SALOME
# 2: la fonction _processEficasCloseEvent est appelee par le manager EFICAS
#
#######

  def closeAdaoCase(self):
    adaoLogger.debug("Fermeture d'un cas")
    # A priori, l'utilisateur s'attend a sauvegarder le cas qui est ouvert
    # dans le GUI d'Eficas
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.items():
      if hasattr(salomeStudyItem,"GetID") and adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        self.eficas_manager.adaoFileClose(adao_case)
        break

  def _processEficasCloseEvent(self, eficasWrapper, eficasEvent):
    from Extensions.param2 import originalMath
    originalMath.toOriginal()
    adaoLogger.debug("Destruction d'un cas")
    editor = eficasEvent.callbackId
    # Recuperation du cas
    adao_case = self.cases[editor]
    # Suppression de l'objet dans l'etude
    adaoStudyEditor.removeItem(adao_case.salome_study_item) # adao_case.salome_study_id, adao_case.salome_study_item)
    # Suppression du cas
    self.cases.pop(editor)
    # Refresh GUI -> appelle currentSelectionChanged()
    adaoGuiHelper.refreshObjectBrowser()

#######
#
# Gestion de la validation d'un cas
# 1: la fonction validateAdaoCase est appelee par le GUI SALOME
#
#######

  def validateAdaoCase(self):
    adaoLogger.debug("Validation du cas par un rapport sur le JDC")
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.items():
      if hasattr(salomeStudyItem,"GetID") and adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        msg = adao_case.validationReportforJDC()
        adaoGuiHelper.gui_information(SalomePyQt.SalomePyQt().getDesktop(), msg)
        break

#######
#
# Gestion de l'affichage de l'arbre EFICAS
# 1: la fonction showTreeAdaoCase est appelee par le GUI SALOME
#
#######

  def showTreeAdaoCase(self):
    adaoLogger.debug("Validation du cas par un rapport sur le JDC")
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.items():
      if hasattr(salomeStudyItem,"GetID") and adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        msg = adao_case.showTreeAdaoCase()
        break

#######
#
# Gestion de la connexion avec YACS
# 1: la fonction exportCaseToYACS exporte l'etude vers YACS
#
#######
  def exportCaseToYACS(self):
    adaoLogger.debug("Export du cas vers YACS")

    # A priori, l'utilisateur s'attend a exporter le cas qui est ouvert
    # dans le GUI d'Eficas
    self.harmonizeSelectionFromEficas()
    salomeStudyItem = adaoGuiHelper.getSelectedItem()
    for case_name, adao_case in self.cases.items():
      if hasattr(salomeStudyItem,"GetID") and adao_case.salome_study_item.GetID() == salomeStudyItem.GetID():
        if adao_case.isOk():
          msg = adao_case.exportCaseToYACS()
          # If msg is not empty -> error found
          if msg != "":
            adaoGuiHelper.gui_warning(SalomePyQt.SalomePyQt().getDesktop(), msg)
        else:
          adaoGuiHelper.gui_warning(SalomePyQt.SalomePyQt().getDesktop(), "ADAO/EFICAS case can't be exported to ADAO/YACS, it is incomplete or invalid. Please return to ADAO/EFICAS edition stage.")
        break

#######
#
# Methodes secondaires permettant de rediriger les evenements
# de SALOME et d'Eficas vers les bonnes methodes de la classe
#
#######

  # Gestion des evenements venant du manager Eficas
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

  # Gestion des evenements venant du GUI de SALOME
  def processGUIEvent(self, actionId):
    """
    Main switch function for ui actions processing
    """
    if actionId in ACTIONS_MAP:
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

        a = sgPyQt.createAction( UI_ELT_IDS.NEW_ADAOCASE_ID, "New case", "New case", "Create a new ADAO case", "eficas_new.png" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.OPEN_ADAOCASE_ID, "Open case", "Open case", "Open an ADAO case", "eficas_open.png" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.SAVE_ADAOCASE_ID, "Save case", "Save case", "Save an ADAO case", "eficas_save.png" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.SAVE_AS_ADAOCASE_ID, "Save as case", "Save as case", "Save an ADAO case as", "eficas_saveas.png" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.VALIDATE_ADAOCASE_ID, "Validate case", "Validate case", "Validate an ADAO case", "eficas_valid.png" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.SHOWTREE_ADAOCASE_ID, "Show tree", "Show tree", "Show the commands tree", "eficas_tree.png" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.CLOSE_ADAOCASE_ID, "Close case", "Close case", "Close an ADAO case", "eficas_close.png" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)
        a = sgPyQt.createAction( UI_ELT_IDS.YACS_EXPORT_ID, "Export to YACS", "Export to YACS", "Generate a YACS graph executing this case", "eficas_yacs.png" )
        sgPyQt.createMenu(a, mid)
        sgPyQt.createTool(a, tid)

        # the following action are used in context popup
        a = sgPyQt.createAction( UI_ELT_IDS.CLOSE_ADAOCASE_ID, "Close case", "Close case", "Close the selected case", "" )
        a = sgPyQt.createAction( UI_ELT_IDS.YACS_EXPORT_ID, "Export to YACS", "Export to YACS", "Generate a YACS graph executing this case", "" )

    def createPopupMenuOnItem(self,popup,item): # salomeSudyId, item):
        if adaoStudyEditor.isValidAdaoCaseItem(item): # Attention : appel ancien avec un coquille (StudyId) : (salomeSudyId, item):
          popup.addAction( sgPyQt.action( UI_ELT_IDS.CLOSE_ADAOCASE_ID ) )
          popup.addAction( sgPyQt.action( UI_ELT_IDS.YACS_EXPORT_ID ) )
        return popup
