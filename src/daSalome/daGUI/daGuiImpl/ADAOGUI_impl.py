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

__author__="aribes/gboulant"

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

################################################
# GUI context class
# Used to store actions, menus, toolbars, etc...
################################################
# A gui context instance is created for each study. The dictionnary __study2context__
# keeps the mapping in memory. This context contains graphical objects that have
# to be created for each study. It contains at least the ui component builder that
# creates the menu and toolbar items (must be created for every study)

from daGuiImpl import adaoGuiHelper
from daGuiImpl.adaoGuiManager import AdaoGuiUiComponentBuilder
from daGuiImpl.adaoGuiManager import AdaoGuiActionImpl
class GUIcontext:
    uiComponentBuilder = None
    actionImpl = None
    def __init__(self):
        self.uiComponentBuilder = AdaoGuiUiComponentBuilder()
        self.actionImpl = AdaoGuiActionImpl()


__study2context__   = {}
__current_context__ = None
def _setContext( studyID ):
    global __study2context__, __current_context__
    if not __study2context__.has_key(studyID):
        print "create new context"
        __study2context__[studyID] = GUIcontext()
        pass
    __current_context__ = __study2context__[studyID]
    return __current_context__

# This object does not need to be embedded in a GUI context object. A single
# instance for all studies is a priori sufficient.

################################################
# Implementation of SALOME GUI interface
################################################

# called when module is initialized
# perform initialization actions
def initialize():
    pass

# called when module is initialized
# return map of popup windows to be used by the module
def windows():
    wm = {}
    wm[SalomePyQt.WT_ObjectBrowser] = Qt.LeftDockWidgetArea
    wm[SalomePyQt.WT_PyConsole]     = Qt.BottomDockWidgetArea
    return wm

# called when module is initialized
# return list of 2d/3d views to be used ny the module
def views():
    return []

def createPreferences():
    """
    Called when module is initialized. Export module's preferences.
    """
    pass

# called when module is activated
# returns True if activating is successfull and False otherwise
def activate():
    print "activate study",  sgPyQt.getStudyId()
    ctx = _setContext( sgPyQt.getStudyId() )
    ctx.actionImpl.activate()
    return True

# called when module is deactivated
def deactivate():
    pass

# called when active study is changed
# active study ID is passed as parameter
def activeStudyChanged( studyID ):
    ctx = _setContext( sgPyQt.getStudyId() )
    pass


# called when popup menu is invoked
# popup menu and menu context are passed as parameters
def createPopupMenu( popup, context ):
  activeStudyId = sgPyQt.getStudyId()
  ctx = _setContext(sgPyQt.getStudyId())
  selcount, selected = adaoGuiHelper.getAllSelected(activeStudyId)
  if selcount == 1:
    selectedItem = adaoGuiHelper.getSelectedItem(activeStudyId)
    popup = ctx.uiComponentBuilder.createPopupMenuOnItem(popup, activeStudyId, selectedItem)

def OnGUIEvent(actionId) :
    """
    Called when an event is raised from a graphic item (click on menu item or
    toolbar button). The actionId value is the ID associated to the item.
    """
    pass
    ctx = _setContext( sgPyQt.getStudyId() )
    ctx.actionImpl.processAction(actionId)

# called when module's preferences are changed
# preference's resources section and setting name are passed as parameters
def preferenceChanged( section, setting ):
    pass

# called when active view is changed
# view ID is passed as parameter
def activeViewChanged( viewID ):
    pass

# called when active view is cloned
# cloned view ID is passed as parameter
def viewCloned( viewID ):
    pass

# called when active view is viewClosed
# view ID is passed as parameter
def viewClosed( viewID ):
    pass

