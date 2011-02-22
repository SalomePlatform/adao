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

import sys
import os

import eficasSalome               # Import from EFICAS_SRC
from InterfaceQT4 import qtEficas # Import from Eficas
from PyQt4.QtGui  import *        # Import from PyQT
from PyQt4.QtCore import *        # Import from PyQT
from PyQt4.QtAssistant import *   # Import from PyQT

from daUtils.adaoEficasEvent import *
from daGuiImpl.adaoLogger import *

#
# ============================================
# Specialization of the EficasWrapper for ADAO
# ============================================
#
class AdaoEficasWrapper(eficasSalome.MyEficas):

    def __init__(self, parent):
        # Configuration de l'installation
        # Permet à EFICAS de faire ses import correctement
        my_path = os.path.dirname(os.path.abspath(__file__))
        ADAO_INSTALL_DIR = my_path + "/../daEficas"
        sys.path[:0]=[ADAO_INSTALL_DIR]

        self.__myCallbackId = {}
        self.__close_editor = None
        self.__file_open_name = ""
        self.__parent = parent

    def init_gui(self):

      eficasSalome.MyEficas.__init__(self, self.__parent, code="ADAO", module="ADAO")
      self.connect(self.viewmanager.myQtab, SIGNAL('currentChanged(int)'), self.tabChanged)


      # On réouvre tous les fichiers comm
      # On fait une copie pour ne pas tomber dans une boucle infinie
      # Deprecated
      # Normalement on ne ferme plus le GUI donc on ne passe plus par là
      save_CallbackId =  self.__myCallbackId.copy()
      for editor, myCallbackId in save_CallbackId.iteritems():
        self.notifyObserver(EficasEvent.EVENT_TYPES.REOPEN, callbackId=myCallbackId)

    def tabChanged(self, index):
      debug("tabChanged " + str(index))
      self.notifyObserver(EficasEvent.EVENT_TYPES.TABCHANGED, callbackId=self.viewmanager.dict_editors[index])

    def addJdcInSalome(  self, jdcPath ):
      # On gere nous meme l'etude
      pass

    def adaofileNew(self, adao_case):

        qtEficas.Appli.fileNew(self)
        index = self.viewmanager.myQtab.currentIndex()
        adao_case.name          = str(self.viewmanager.myQtab.tabText(index)) # Utilisation de str() pour passer d'un Qstring à un string
        adao_case.eficas_editor = self.viewmanager.dict_editors[index]
        self.notifyObserver(EficasEvent.EVENT_TYPES.NEW, callbackId=adao_case)

    def openEmptyCase(self, callbackId):
        qtEficas.Appli.fileNew(self)
        self.removeCallbackId(callbackId)
        self.setCallbackId(callbackId)

    def fileSave(self):
        """
        @overload
        """
        qtEficas.Appli.fileSave(self)
        index = self.viewmanager.myQtab.currentIndex()
        if index > -1 :
          self.notifyObserver(EficasEvent.EVENT_TYPES.SAVE)

    def fileSaveAs(self):
        """
        @overload
        """
        qtEficas.Appli.fileSaveAs(self)
        self.notifyObserver(EficasEvent.EVENT_TYPES.SAVE)

    def getCaseName(self):
      if self.__close_editor is None:
        index = self.viewmanager.myQtab.currentIndex()
        CaseName = self.viewmanager.myQtab.tabText(index)
        return CaseName
      else:
        CaseName = str(self.__close_editor.fichier.split('/')[-1])
        return CaseName

    def getFileCaseName(self):
      if self.__close_editor is None:
        index = self.viewmanager.myQtab.currentIndex()
        editor = self.viewmanager.dict_editors[index]
        return editor.fichier
      else:
        return self.__close_editor.fichier

    def Openfile(self, filename):
      self.viewmanager.handleOpen(fichier=filename)

    def handleOpenRecent(self):
      """
      @overload
      """
      idx = self.sender()
      fichier = self.ficRecents[idx]
      self.__file_open_name = fichier
      self.notifyObserver(EficasEvent.EVENT_TYPES.OPEN)
      self.__file_open_name = ""

    def fileOpen(self):
        """
        @overload
        """
        fichier = QFileDialog.getOpenFileName(self,
                                              self.trUtf8('Ouvrir Fichier'),
                                              self.CONFIGURATION.savedir,
                                              self.trUtf8('JDC Files (*.comm);;''All Files (*)'))
        if fichier.isNull(): return
        self.__file_open_name = fichier
        self.notifyObserver(EficasEvent.EVENT_TYPES.OPEN)
        self.__file_open_name = ""

    def getOpenFileName(self):
      return str(self.__file_open_name)

    def selectCase(self, callbackId):
      rtn = False
      for editor, myCallbackId in self.__myCallbackId.iteritems():
        if myCallbackId[0] == callbackId[0]:
          if myCallbackId[1].GetID() == callbackId[1].GetID():
            try:
              for indexEditor in self.viewmanager.dict_editors.keys():
                if editor is self.viewmanager.dict_editors[indexEditor]:
                  self.viewmanager.myQtab.setCurrentIndex(indexEditor)
                  rtn = True
            except:
              pass
      return rtn

    def fileClose(self):
        """
        @overload
        """
        index = self.viewmanager.myQtab.currentIndex()
        self.__close_editor = self.viewmanager.dict_editors[index]
        res = self.viewmanager.handleClose(self)
        if res != 2: # l utilsateur a annule
          if self.__close_editor.fichier is None:
            # We have to destroy the case
            self.notifyObserver(EficasEvent.EVENT_TYPES.DESTROY)
            self.__myCallbackId.pop(self.__close_editor)
          else:
            # Il faudrait en faire plus -> Voir Edit dans SALOME !
            self.notifyObserver(EficasEvent.EVENT_TYPES.SAVE)
            self.__myCallbackId.pop(self.__close_editor)
        self.__close_editor = None
        return res

    def fileCloseAll(self):
      """
      @overload
      """
      while len(self.viewmanager.dict_editors) > 0:
        self.viewmanager.myQtab.setCurrentIndex(0)
        if self.viewmanager.myQtab.currentIndex() == 0:
          res = self.fileClose()
          if res==2 : return res   # l utilsateur a annule
        else:
          return 0

    # ==========================================================================
    # Function for the notification interface between an EficasWrapper an an
    # EficasObserver.

    # Association de l'objet editor avec le callbackId
    def setCallbackId(self, callbackId):
      index = self.viewmanager.myQtab.currentIndex()
      self.__myCallbackId[self.viewmanager.dict_editors[index]] = callbackId

    def removeCallbackId(self, callbackId):
      key_to_remove = None
      print callbackId
      for k, v in self.__myCallbackId.iteritems():
        print k, v
        if v[0] == callbackId[0] and v[1].GetID() == callbackId[1].GetID():
          key_to_remove = k
      if key_to_remove is not None:
        del self.__myCallbackId[key_to_remove]
      else:
        print "Oups - cannot find callbackId"

    def getCallbackId(self):
      if self.__close_editor is None:
        index = self.viewmanager.myQtab.currentIndex()
        return self.__myCallbackId[self.viewmanager.dict_editors[index]]
      else:
        return self.__myCallbackId[self.__close_editor]

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
      if eventType != EficasEvent.EVENT_TYPES.OPEN:
        if callbackId is None :
          eficasEvent = EficasEvent(eventType, self.getCallbackId())
        else:
          eficasEvent = EficasEvent(eventType, callbackId)
      else:
        eficasEvent = EficasEvent(eventType)
      self.__observer.processEficasEvent(self, eficasEvent)

