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

__author__="aribes/gboulant"

import salome
# Get SALOME PyQt interface
import SalomePyQt
__sgPyQt = SalomePyQt.SalomePyQt()

from . import adaoModuleHelper
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox

def waitCursor():
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

def restoreCursor():
    QApplication.restoreOverrideCursor()

def gui_warning(parent, msg="An error occurs" ):
    """
    This function displays a message dialog box displaying the specified message.
    """
    QMessageBox.warning( parent, "Alerte", msg)

def gui_information(parent, msg="Information" ):
    """
    This function displays a message dialog box displaying the specified message.
    """
    QMessageBox.information( parent, "Information", msg, QMessageBox.Close)

#~ def getActiveStudyId():
    #~ """
    #~ This function returns the id of the active study. The concept of active study
    #~ makes sens only in the GUI context.
    #~ """
    #~ return salome.sg.getActiveStudyId()

def refreshObjectBrowser():
    """
    Refresh the graphical representation of the SALOME study, in case where the
    GUI is working.
    """
    if salome.sg is not None:
        # salome.sg.updateObjBrowser(0)
        salome.sg.updateObjBrowser()

def selectItem(salomeStudyItem):
  if salome.sg is not None:
    salome.sg.ClearIObjects()
    salome.sg.AddIObject(salomeStudyItem)

def getSelectedItem():# salomeStudyId=-100):
    """
    Get the current selection. If more than one item are selected, the
    only first is considered. The object is return (not the id).
    The item can be of any type, no control is done in this function.
    """
    if salome.sg is None:
        raise Exception("GuiHelper.getSelectedItem can't be used without the GUI context")

    #~ if salomeStudyId != -100:
      #~ studyEditor = salome.kernel.studyedit.getStudyEditor(salomeStudyId)
    studyEditor = salome.kernel.studyedit.getStudyEditor()
    item = None
    listEntries=salome.sg.getAllSelected()
    if len(listEntries) >= 1:
        entry = listEntries[0]
        item = studyEditor.study.FindObjectID( entry )
    return item

def getAllSelected():# salomeStudyId):
    """
    Returns all selected items in the specified study.
    """
    if salome.sg is None:
        raise OmaException("getSelectedItem can't be used without the GUI context", OmaException.TYPES.DEVEL)

    # study = adaoModuleHelper.getStudyManager().GetStudyByID( salomeStudyId )
    selcount = salome.sg.SelectedCount()
    seltypes = {}
    for i in range( selcount ):
        __incObjToMap( seltypes, adaoModuleHelper.getObjectID( salome.sg.getSelected( i ) ) ) # study, salome.sg.getSelected( i ) ) )
        pass
    return selcount, seltypes

def __incObjToMap( m, id ):
    """
    Increment object counter in the specified map.
    Not to be used outside this module.
    """
    if id not in m: m[id] = 0
    m[id] += 1
    pass

def getDesktop():
    """
    Returns the active Desktop. Usefull to set the relative position of a dialog box
    """
    return __sgPyQt.getDesktop()

def warning(msg):
    """
    This function displays a message dialog box displaying the specified message.
    """
    gui_warning(getDesktop(),msg)

def information(msg):
    """
    This function displays a message dialog box displaying the specified message.
    """
    gui_information(getDesktop(),msg)
