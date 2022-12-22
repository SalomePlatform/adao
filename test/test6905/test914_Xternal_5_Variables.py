# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2023 EDF R&D
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

#===============================================================================
import numpy
ObservationError = numpy.matrix('1 0 ; 0 1')
Background = numpy.array([1, 1])

def DirectOperator(x):
    return numpy.array(x)
def TangentOperator(paire):
    x,dx = paire
    return numpy.array(dx)
def AdjointOperator(paire):
    x,dy = paire
    return numpy.array(dy)

#===============================================================================
if __name__ == "__main__":
    print("\nAUTODIAGNOSTIC\n==============")
    print("ObservationError = %s"%(ObservationError,))
    print("Background       = %s"%(Background,))
    print("DirectOperator   = %s"%(DirectOperator([2,5,3]),))
    print("TangentOperator  = %s"%(TangentOperator(([2,5,3],[1,1,1])),))
    print("AdjointOperator  = %s"%(AdjointOperator(([2,5,3],[0,0,0])),))
    print("")
