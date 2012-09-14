#-*-coding:iso-8859-1-*-
# Copyright (C) 2010-2012 EDF R&D
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

import numpy
parametres = init_data["parametres"]

xb = []
for parametre in parametres:
    xb.append( parametre[1] )

B  = numpy.matrix(numpy.core.identity(len(xb)))
alpha  = 1.e14
B[0,0] = alpha * 100
B[1,1] = alpha * 10
B[2,2] = alpha * 1
dimensionXb = len( xb )
B = numpy.matrix( B, numpy.float ).reshape((dimensionXb,dimensionXb))

BackgroundError = B
