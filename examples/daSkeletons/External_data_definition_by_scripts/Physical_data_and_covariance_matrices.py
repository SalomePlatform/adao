# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2017 EDF R&D
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

    External definition of physical data and simple error covariance matrices
    """
__author__ = "Jean-Philippe ARGAUD"
#
# ==============================================================================
#
import numpy
#
def True_state():
    """
    Arbitrary values and names, as a tuple of two series of same length
    """
    return (numpy.array([1, 2, 3]), ['Para1', 'Para2', 'Para3'])
#
def Simple_Matrix( size, diagonal=None ):
    """
    Diagonal matrix, with either 1 or a given vector on the diagonal
    """
    if diagonal is not None:
        S = numpy.diag( diagonal )
    else:
        S = numpy.matrix(numpy.identity(int(size)))
    return S
#
# ==============================================================================
if __name__ == "__main__":

    print("")
    print("AUTODIAGNOSTIC")
    print("==============")
    
    print("")
    print("True_state = ", True_state())
    print("")
    print("B or R =\n",Simple_Matrix(3))
    print("")
    print("B or R =\n",Simple_Matrix(4, diagonal=numpy.arange(4,dtype=float)))
    print("")
