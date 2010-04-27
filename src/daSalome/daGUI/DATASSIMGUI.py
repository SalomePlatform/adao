# -*- coding: iso-8859-1 -*-
#  Copyright (C) 2010  EDF R&D
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
This python file provides the implementation of the interface of the GUI part of
this SALOME module. This interface is required by the SALOME GUI framework.
We use here a proxy module named under the alias GuiImpl for at least three
reasons:
1. To Keep the required interface as clear as possible in this file;
2. The concrete implementation can be substituted by an alternative version;
3. We could mix several concrete implementations provided by different proxy
   modules, for example for test purposes.
"""

from daGuiImpl import DATASSIMGUI_impl as GuiImpl


# called when module is initialized
# perform initialization actions
def initialize():
    GuiImpl.initialize()

# called when module is initialized
# return map of popup windows to be used by the module
def windows():
    return GuiImpl.windows()

# called when module is initialized
# export module's preferences
def createPreferences():
    GuiImpl.createPreferences()

# called when module is activated
# returns True if activating is successfull and False otherwise
def activate():
    return GuiImpl.activate()

# called when module is deactivated
def deactivate():
    GuiImpl.deactivate()

# called when active study is changed
# active study ID is passed as parameter
def activeStudyChanged( studyID ):
    GuiImpl.activeStudyChanged( studyID )

# called when popup menu is invoked
# popup menu and menu context are passed as parameters
def createPopupMenu( popup, context ):
    GuiImpl.createPopupMenu(popup, context )

# called when GUI action is activated
# action ID is passed as parameter
def OnGUIEvent(commandID) :
    GuiImpl.OnGUIEvent(commandID)

# called when module's preferences are changed
# preference's resources section and setting name are passed as parameters
def preferenceChanged( section, setting ):
    GuiImpl.preferenceChanged( section, setting )
