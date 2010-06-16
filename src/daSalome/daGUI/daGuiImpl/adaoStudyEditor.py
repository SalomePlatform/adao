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

__author__="aribes/gboulant"

from enumerate import Enumerate
import studyedit
import adaoModuleHelper
from daGuiImpl.adaoCase import AdaoCase

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

def addInStudy(salomeStudyId, adaoCase):
    """
    This function adds in the specified SALOME study a study entry that corresponds
    to the specified adao case. This study case is put in a folder under
    the ADAO component and is identified by the case name.
    """

    studyEditor = studyedit.getStudyEditor(salomeStudyId)

    adaoRootEntry = studyEditor.findOrCreateComponent(
        engineName    = adaoModuleHelper.componentName(),
        componentName = adaoModuleHelper.componentUserName())

    itemName  = adaoCase.get_name()
    itemValue = str(adaoCase.get_filename())
    itemType  = ADAO_ITEM_TYPES.ADAO_CASE

    salomeStudyItem = studyEditor.createItem(
        adaoRootEntry, itemName,
        comment = itemValue,
        typeId  = itemType)
    # _MEM_ Note that we use the comment attribute to store the serialize
    # description of the data.

    return salomeStudyItem

def updateItem(salomeStudyId, salomeStudyItem, adaoCase):

    studyEditor = studyedit.getStudyEditor(salomeStudyId)
    
    if salomeStudyItem.GetName()[:-2] != adaoCase.get_name():
      itemName  = adaoCase.get_name()
      itemValue = adaoCase.get_filename()
    else:
      itemName  = salomeStudyItem.GetName()
      itemValue = adaoCase.get_filename()

    studyEditor.setItem(salomeStudyItem,
        name    = itemName,
        comment = itemValue)

def removeItem(salomeStudyId, item):
    """
    Remove the item from the specified study.
    """
    studyEditor = studyedit.getStudyEditor(salomeStudyId)
    return studyEditor.removeItem(item,True)


def isValidAdaoCaseItem(salomeStudyId,item):
    """
    Return true if the specified item corresponds to a valid adaoCase
    """
    if item is None:
        return False

    studyEditor = studyedit.getStudyEditor(salomeStudyId)
    itemType = studyEditor.getTypeId(item)
    if itemType != ADAO_ITEM_TYPES.ADAO_CASE:
        return False

    return True
