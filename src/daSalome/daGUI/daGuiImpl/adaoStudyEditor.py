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

__author__="aribes/gboulant"

from daUtils.enumerate import Enumerate

from salome.kernel import studyedit

from . import adaoModuleHelper

#
# ==============================================================================
# Constant parameters and identifiers
# ==============================================================================
#
ADAO_ITEM_TYPES = Enumerate([
    "ADAO_CASE",
])

#
# ==============================================================================
# Function dedicated to the data management in the salome study
# ==============================================================================
#
# For developpers, note that the data structures used here are:
# - the SALOME study whose API is defined by SALOMEDS::Study
# - an item in a study whose API is defined by SALOMEDS:SObject
# - a study component, whose API is defined by SALOMEDS::SComponent
#   a SComponent is a reference in a study toward a SALOME component
#

def addInStudy(adaoCase): # salomeStudyId, adaoCase):
    """
    This function adds in the specified SALOME study a study entry that corresponds
    to the specified adao case. This study case is put in a folder under
    the ADAO component and is identified by the case name.
    """

    studyEditor = studyedit.getStudyEditor() # salomeStudyId)

    adaoRootEntry = studyEditor.findOrCreateComponent(
        moduleName    = adaoModuleHelper.componentName(),
        componentName = adaoModuleHelper.componentUserName(),
        icon          = adaoModuleHelper.modulePixmap())

    itemName  = adaoCase.name
    itemValue = adaoCase.filename
    itemType  = ADAO_ITEM_TYPES.ADAO_CASE

    icon = adaoModuleHelper.studyItemPixmapNOk()
    if adaoCase.isOk():
      icon = adaoModuleHelper.studyItemPixmapOk()

    salomeStudyItem = studyEditor.createItem(
        adaoRootEntry, itemName,
        comment = itemValue,
        typeId  = itemType,
        icon    = icon)

    return salomeStudyItem

def updateItem(salomeStudyItem, adaoCase): # salomeStudyId, salomeStudyItem, adaoCase):

    studyEditor = studyedit.getStudyEditor() # salomeStudyId)

    if salomeStudyItem.GetName()[:-2] != adaoCase.name:
      itemName  = adaoCase.name
      itemValue = adaoCase.filename
    else:
      itemName  = salomeStudyItem.GetName()
      itemValue = adaoCase.filename

    icon = adaoModuleHelper.studyItemPixmapNOk()
    if adaoCase.isOk():
      icon = adaoModuleHelper.studyItemPixmapOk()

    studyEditor.setItem(salomeStudyItem,
        name    = itemName,
        comment = itemValue,
        icon    = icon)

def removeItem(item): # salomeStudyId, item):
    """
    Remove the item from the specified study.
    """
    studyEditor = studyedit.getStudyEditor() # salomeStudyId)
    return studyEditor.removeItem(item,True)


def isValidAdaoCaseItem(item): # salomeStudyId,item):
    """
    Return true if the specified item corresponds to a valid adaoCase
    """
    if item is None:
        return False

    studyEditor = studyedit.getStudyEditor() # salomeStudyId)
    itemType = studyEditor.getTypeId(item)
    if itemType != ADAO_ITEM_TYPES.ADAO_CASE:
        return False

    return True
