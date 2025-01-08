# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

__doc__ = """
    ADAO skeleton case, for wide script usage in case definition
    ------------------------------------------------------------

    External definition of the physical simulation operator, its tangent and
    its adjoint form. In case adjoint is not known, a finite difference version
    is given by default in this skeleton.
    """
__author__ = "Jean-Philippe ARGAUD"
#
# ==============================================================================
#
import os, numpy, time
#
def DirectOperator( XX ):
    # Opérateur identité
    return numpy.ravel(XX)
#
def TangentOperator(paire  ):
    # Opérateur identité
    (XX, dX) = paire
    return numpy.ravel(dX)
#
def AdjointOperator( paire ):
    # Opérateur identité
    (XX, YY) = paire
    return numpy.ravel(YY)
#
# ==============================================================================
if __name__ == "__main__":

    print()
    print("AUTODIAGNOSTIC")
    print("==============")

    from Physical_data_and_covariance_matrices import True_state
    X0, noms = True_state()

    FX = DirectOperator( X0 )
    print("FX =", FX)
    print()
