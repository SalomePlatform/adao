# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 CEA/DEN, EDF R&D
#
# This file is part of SALOME ADAO module
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
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

def buildInstance(orb):
    from ADAO import ADAO

    # set SSL mode, if not done yes
    import KernelBasis
    KernelBasis.setSSLMode(True)

    # check if ADAO is already registered
    import KernelServices
    try:
        return KernelServices.RetrieveCompo("ADAO"), orb
    except Exception:
        pass

    # initialize and register ADAO engine
    import PortableServer
    obj = orb.resolve_initial_references("RootPOA")
    poa = obj._narrow(PortableServer.POA)
    pman = poa._get_the_POAManager()
    pman.activate()
    #
    from SALOME_ContainerPy import SALOME_ContainerPy_SSL_i
    cont = SALOME_ContainerPy_SSL_i(orb, poa, "FactoryServer")
    conObj = poa.id_to_reference(poa.activate_object(cont))
    #
    servant = ADAO(orb, poa, conObj, "FactoryServer", "ADAO_inst_1", "ADAO")
    ret = servant.getCorbaRef()
    KernelServices.RegisterCompo("ADAO", ret)
    return ret, orb
