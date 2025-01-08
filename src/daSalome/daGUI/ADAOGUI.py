# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D

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

import adao
if not hasattr(adao, "adao_py_dir"):
    if hasattr(adao, "__file__"):
        lieu = " A potential candidate file is %s."%repr(adao.__file__)
    else:
        lieu = ""
    raise ImportError("\n\nFailed to activate module ADAO. Is it perhaps because you own a personnal perturbating file \'adao.py\' somewhere in your PATH?%s Rename, remove or move it before retrying to launch SALOME/ADAO.\n"%lieu)
from daGuiImpl import ADAOGUI_impl as GuiImpl
from daUtils import adaoLogger

adaoLogger.debug("Import ADAOGUI")

# called when module is initialized
# perform initialization actions
def initialize():
  adaoLogger.debug("initialize")
  GuiImpl.initialize()

# called when module is initialized
# return map of popup windows to be used by the module
def windows():
  adaoLogger.debug("windows")
  return GuiImpl.windows()

def views():
  adaoLogger.debug("views")
  return GuiImpl.views()

# called when module is initialized
# export module's preferences
def createPreferences():
  adaoLogger.debug("createPreferences")
  GuiImpl.createPreferences()

# called when module is activated
# returns True if activating is successfull and False otherwise
def activate():
  adaoLogger.debug("activate")
  return GuiImpl.activate()

# called when module is deactivated
def deactivate():
  adaoLogger.debug("deactivate")
  GuiImpl.deactivate()

# called when active study is changed
# active study ID is passed as parameter
#~ def activeStudyChanged( studyID ):
  #~ adaoLogger.debug("activeStudyChanged")
  #~ GuiImpl.activeStudyChanged( studyID )

# called when popup menu is invoked
# popup menu and menu context are passed as parameters
def createPopupMenu( popup, context ):
  adaoLogger.debug("createPopupMenu")
  GuiImpl.createPopupMenu(popup, context )

# called when GUI action is activated
# action ID is passed as parameter
def OnGUIEvent(commandID) :
  adaoLogger.debug("OnGUIEvent")
  GuiImpl.OnGUIEvent(commandID)

# called when module's preferences are changed
# preference's resources section and setting name are passed as parameters
def preferenceChanged( section, setting ):
  adaoLogger.debug("preferenceChanged")
  GuiImpl.preferenceChanged( section, setting )

def activeViewChanged(myView):
  adaoLogger.debug("activeViewChanged")
  GuiImpl.activeViewChanged(myView)
