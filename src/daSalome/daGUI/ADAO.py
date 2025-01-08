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

import ADAO_COMPONENT__POA
import SALOME_ComponentPy
import SALOME_DriverPy
import SALOME_Embedded_NamingService_ClientPy

from daUtils.adaoLogger import *

class ADAO(ADAO_COMPONENT__POA.ADAO_ENGINE,
           SALOME_ComponentPy.SALOME_ComponentPy_i,
           SALOME_DriverPy.SALOME_DriverPy_i):
  """
      Pour etre un composant SALOME cette classe Python
      doit avoir le nom du composant et heriter de la
      classe ADAO_COMPONENT issue de la compilation de l'idl
      par omniidl et de la classe SALOME_ComponentPy_i
      qui porte les services generaux d'un composant SALOME
  """
  def __init__ ( self, orb, poa, contID, containerName, instanceName,
      interfaceName ):
    debug("Creating ADAO component instance", "ENGINE")
    SALOME_ComponentPy.SALOME_ComponentPy_i.__init__(self, orb, poa,
        contID, containerName, instanceName, interfaceName)
    SALOME_DriverPy.SALOME_DriverPy_i.__init__(self, interfaceName)

    # On stocke dans l'attribut _naming_service, une ref sur le Naming Service
    #
    emb_ns = self._contId.get_embedded_NS_if_ssl()
    import CORBA
    if CORBA.is_nil(emb_ns):
        self._naming_service = SALOME_ComponentPy.SALOME_NamingServicePy_i( self._orb )
    else:
        self._naming_service = SALOME_Embedded_NamingService_ClientPy.SALOME_Embedded_NamingService_ClientPy(emb_ns)
    #

  def print_ping():
    info("ADAO ENGINE Ping", "ENGINE")
