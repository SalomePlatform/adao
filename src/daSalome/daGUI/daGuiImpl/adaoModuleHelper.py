# -*- coding: utf-8 -*-
# Copyright (C) 2007-2008  CEA/DEN, EDF R&D, OPEN CASCADE
#
# Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
# CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
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

__all__ = [
    "moduleID",
    "objectID",
    "unknownID",
    "componentName",
    "modulePixmap",
    "verbose",
    "getORB",
    "getNS",
    "getLCC",
    "getStudyManager",
    "getEngine",
    "getEngineIOR",
    "findOrCreateComponent",
    "getObjectID",
    ]

from omniORB import CORBA
from SALOME_NamingServicePy import SALOME_NamingServicePy_i
from LifeCycleCORBA import LifeCycleCORBA
import SALOMEDS
import SALOMEDS_Attributes_idl
from salome.kernel.studyedit import getStudyEditor

#import OMA_ORB

###
# Get OMA module's ID
###
def moduleID():
    MODULE_ID = 6100
    return MODULE_ID

###
# Get OMA object's ID
###
def objectID():
    OBJECT_ID = 6110
    return OBJECT_ID

###
# Get unknown ID
###
def unknownID():
    FOREIGN_ID = -1
    return FOREIGN_ID

def componentName():
    """
    This provide the name of the module component to be associated to the study.
    """
    # Note that this name should be (i) the name used for the class implementing
    # the component CORBA interface and (ii) the name used to declare the component
    # in the catalog of the module.
    return "ADAO"

# _MEM_ we use here the tr() translation methode to manage constant parameters
# in the application. We could have specified instead constant values directly
# in the code below. It's a matter of convenience.
from PyQt5.QtCore import QObject
QObjectTR=QObject()

def componentUserName():
    return "ADAO"

def modulePixmap():
    """
    Get the reference pixmap for this module.
    """
    return "ADAO_small.png"

def studyItemPixmapOk():
    """
    Get the reference pixmap for items of this module.
    """
    return "ADAO_small_vert.png"

def studyItemPixmapNOk():
    """
    Get the reference pixmap for items of this module.
    """
    return "ADAO_small_rouge.png"

__verbose__ = None
def verbose():
    global __verbose__
    if __verbose__ is None:
        try:
            __verbose__ = int( os.getenv( 'SALOME_VERBOSE', 0 ) )
        except:
            __verbose__ = 0
            pass
        pass
    return __verbose__

###
# Get ORB reference
###
__orb__ = None
def getORB():
    global __orb__
    if __orb__ is None:
        __orb__ = CORBA.ORB_init( [''], CORBA.ORB_ID )
        pass
    return __orb__

###
# Get naming service instance
###
__naming_service__ = None
def getNS():
    global __naming_service__
    if __naming_service__ is None:
        __naming_service__ = SALOME_NamingServicePy_i( getORB() )
        pass
    return __naming_service__

##
# Get life cycle CORBA instance
##
__lcc__ = None
def getLCC():
    global __lcc__
    if __lcc__ is None:
        __lcc__ = LifeCycleCORBA( getORB() )
        pass
    return __lcc__

##
# Get study manager
###
__study_manager__ = None
def getStudyManager():
    global __study_manager__
    if __study_manager__ is None:
        obj = getNS().Resolve( '/myStudyManager' )
        __study_manager__ = obj._narrow( SALOMEDS.StudyManager )
        pass
    return __study_manager__

###
# Get OMA engine
###
__engine__ = None
def getEngine():
    global __engine__
    if __engine__ is None:
        __engine__ = getLCC().FindOrLoadComponent( "FactoryServer", componentName() )
        pass
    return __engine__

###
# Get OMA engine IOR
###
def getEngineIOR():
    IOR = ""
    if getORB() and getEngine():
        IOR = getORB().object_to_string( getEngine() )
        pass
    return IOR

###
# Find or create OMA component object in a study
###
def findOrCreateComponent( study ):
    father = study.FindComponent( componentName() )
    if father is None:
        builder = study.NewBuilder()
        father = builder.NewComponent( componentName() )
        attr = builder.FindOrCreateAttribute( father, "AttributeName" )
        attr.SetValue( componentName() )
        attr = builder.FindOrCreateAttribute( father, "AttributePixMap" )
        attr.SetPixMap( modulePixmap() )
        attr = builder.FindOrCreateAttribute( father, "AttributeLocalID" )
        attr.SetValue( moduleID() )
        try:
            builder.DefineComponentInstance( father, getEngine() )
            pass
        except:
            pass
        pass
    return father

###
# Get object's ID
###
def getObjectID( entry ): # study, entry ):
    ID = unknownID()
    if entry: # study and entry:
        sobj = getStudyEditor().study.FindObjectID( entry )
        if sobj is not None:
            test, anAttr = sobj.FindAttribute( "AttributeLocalID" )
            if test: ID = anAttr._narrow( SALOMEDS.AttributeLocalID ).Value()
            pass
        pass
    return

