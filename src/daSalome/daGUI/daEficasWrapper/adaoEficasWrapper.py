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

from eficasWrapper import *
from PyQt4 import QtGui,QtCore
import sys

# Configuration de l'installation
my_path = os.path.dirname(os.path.abspath(__file__))
ADAO_INSTALL_DIR = my_path + "/../daEficas"
sys.path[:0]=[ADAO_INSTALL_DIR]

#
# ============================================
# Specialization of the EficasWrapper for ADAO
# ============================================
#
class AdaoEficasWrapper(EficasWrapper):

    def __init__(self, parent, code="ADAO"):
        EficasWrapper.__init__(self, parent, code)
        self.__myCallbackId = {}
        self.__close_editor = None
        self.__file_open_name = ""

    def init_gui(self):
      EficasWrapper.init_gui(self)
      print "self.__myCallbackId", self.__myCallbackId
      save_CallbackId =  self.__myCallbackId.copy()
      for editor, myCallbackId in save_CallbackId.iteritems():
        self.notifyObserver(EficasEvent.EVENT_TYPES.REOPEN, callbackId=myCallbackId)

    # Association de l'objet editor avec le callbackId
    def setCallbackId(self, callbackId):
      index = self.viewmanager.myQtab.currentIndex()
      self.__myCallbackId[self.viewmanager.dict_editors[index]] = callbackId

    def getCallbackId(self):
      if self.__close_editor is None:
        index = self.viewmanager.myQtab.currentIndex()
        return self.__myCallbackId[self.viewmanager.dict_editors[index]]
      else:
        return self.__myCallbackId[self.__close_editor]

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
        fichier = QtGui.QFileDialog.getOpenFileName(self,
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

