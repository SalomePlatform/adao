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
import sys

# Configuration de l'installation
my_path = os.path.dirname(os.path.abspath(__file__))
DATASSIM_INSTALL_DIR = my_path + "/../daEficas"
sys.path[:0]=[DATASSIM_INSTALL_DIR]

#
# ================================================
# Specialization of the EficasWrapper for DATASSIM
# ================================================
#
class DatassimEficasWrapper(EficasWrapper):
    def __init__(self, parent, code="DATASSIM"):
        EficasWrapper.__init__(self, parent, code)

    def fileSave(self):
        """
        @overload
        """
        qtEficas.Appli.fileSave(self)
        self.notifyObserver(EficasEvent.EVENT_TYPES.SAVE)

    def fileSaveAs(self):
        """
        @overload
        """
        qtEficas.Appli.fileSaveAs(self)
        self.notifyObserver(EficasEvent.EVENT_TYPES.SAVE)

    def getCurrentFileName(self):
       index = self.viewmanager.myQtab.currentIndex()
       print index
       rtn = ""
       if index > 0 :
         rtn  = self.viewmanager.myQtab.tabText(index)
       return rtn
