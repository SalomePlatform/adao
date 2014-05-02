#-*-coding:iso-8859-1-*-
#  Copyright (C) 2010-2014 EDF R&D
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

import sys
import os

import eficasSalome               # Import from EFICAS_SRC
from InterfaceQT4 import qtEficas # Import from Eficas
from PyQt4.QtGui  import *        # Import from PyQT
from PyQt4.QtCore import *        # Import from PyQT
# from PyQt4.QtAssistant import *   # Import from PyQT

from daUtils.adaoEficasEvent import *
from daUtils.adaoLogger import *

#
# ============================================
# Specialization of the EficasWrapper for ADAO
# ============================================
#
class AdaoEficasWrapper(eficasSalome.MyEficas):

    def __init__(self, parent):
        # Configuration de l'installation
        # Permet � EFICAS de faire ses import correctement
        my_path = os.path.dirname(os.path.abspath(__file__))
        ADAO_INSTALL_DIR = my_path + "/../daEficas"
        sys.path.insert(0,ADAO_INSTALL_DIR)

        self.__parent = parent

    def init_gui(self):

      eficasSalome.MyEficas.__init__(self, self.__parent, code="ADAO", module="ADAO")
      self.connect(self.viewmanager.myQtab, SIGNAL('currentChanged(int)'), self.tabChanged)
      self.menubar.hide()
      self.toolBar.hide()

    def addJdcInSalome(self, jdcPath):
      debug("addJdcInSalome is called " + str(jdcPath))
      # On gere nous meme l'etude
      pass

#######
#
# Gestion des �v�nements provenant des widgets QT d'Eficas
#
#######

    def tabChanged(self, index):
      debug("tabChanged " + str(index))
      # This signal is also emit when a new case is created/added
      # On regarde que le dictionnaire contient l'index
      if index in self.viewmanager.dict_editors.keys():
        self.notifyObserver(EficasEvent.EVENT_TYPES.TABCHANGED, callbackId=self.viewmanager.dict_editors[index])

#######
#
# M�thodes g�rant les boutons dans SALOME
#
#######

# Rq: Utilisation de la m�thode str() pour passer d'un Qstring � un string

    def adaofileNew(self, adao_case):

      qtEficas.Appli.fileNew(self)
      index = self.viewmanager.myQtab.currentIndex()
      adao_case.name          = str(self.viewmanager.myQtab.tabText(index))
      adao_case.setEditor(self.viewmanager.dict_editors[index])
      self.notifyObserver(EficasEvent.EVENT_TYPES.NEW, callbackId=adao_case)

    def adaoFileSave(self, adao_case):

      ok = qtEficas.Appli.fileSave(self)
      if ok:
        index = self.viewmanager.myQtab.currentIndex()
        adao_case.name          = str(self.viewmanager.myQtab.tabText(index))
        adao_case.filename      = str(self.viewmanager.dict_editors[index].fichier)
        adao_case.setEditor(self.viewmanager.dict_editors[index])
        self.notifyObserver(EficasEvent.EVENT_TYPES.SAVE, callbackId=adao_case)

    def adaoFileSaveAs(self, adao_case):

      ok = qtEficas.Appli.fileSaveAs(self)
      if ok:
        index = self.viewmanager.myQtab.currentIndex()
        adao_case.name          = str(self.viewmanager.myQtab.tabText(index))
        adao_case.filename      = str(self.viewmanager.dict_editors[index].fichier)
        adao_case.setEditor(self.viewmanager.dict_editors[index])
        self.notifyObserver(EficasEvent.EVENT_TYPES.SAVE, callbackId=adao_case)

    def adaoFileOpen(self, adao_case):

      tab_number = self.viewmanager.myQtab.count()
      ok = self.viewmanager.handleOpen()
      if ok:
        # On regarde si c'est un nouveau editeur
        if self.viewmanager.myQtab.count() > tab_number:
          index = self.viewmanager.myQtab.currentIndex()
          adao_case.name          = str(self.viewmanager.myQtab.tabText(index))
          adao_case.filename      = str(self.viewmanager.dict_editors[index].fichier)
          adao_case.setEditor(self.viewmanager.dict_editors[index])
          self.notifyObserver(EficasEvent.EVENT_TYPES.OPEN, callbackId=adao_case)

    def adaoFileClose(self, adao_case):

        index = self.viewmanager.myQtab.currentIndex()
        close_editor = self.viewmanager.dict_editors[index]
        res = self.viewmanager.handleClose(self)
        if res != 2: # l utilsateur a annule
          if close_editor.fichier is None:
            # Cas fichier vide
            self.notifyObserver(EficasEvent.EVENT_TYPES.CLOSE, callbackId=close_editor)
          else:
            # Cas fichier existant
            self.notifyObserver(EficasEvent.EVENT_TYPES.CLOSE, callbackId=close_editor)

#######
#
# M�thodes auxiliares de gestion du GUI Eficas pour synchronisation
# avec la partie GUI de SALOME
#
#######

    def selectCase(self, editor):
      rtn = False
      for indexEditor in self.viewmanager.dict_editors.keys():
        if editor is self.viewmanager.dict_editors[indexEditor]:
          self.viewmanager.myQtab.setCurrentIndex(indexEditor)
          rtn = True
          break
      return rtn

    def getCurrentEditor(self):
      index = self.viewmanager.myQtab.currentIndex()
      editor = None
      if index >= 0:
        editor = self.viewmanager.dict_editors[index]
      return editor




#######
#
# M�thodes secondaires permettant de g�rer les observeurs du
# GUI d'Eficas
#
#######

    def addObserver(self, observer):
        """
        In fact, only one observer may be defined for the moment.
        """
        try:
            observer.processEficasEvent
        except:
            raise DevelException("the argument should implement the function processEficasEvent")
        self.__observer = observer

    def notifyObserver(self, eventType, callbackId=None):
      eficasEvent = EficasEvent(eventType, callbackId)
      self.__observer.processEficasEvent(self, eficasEvent)
