# Copyright (C) 2010-2013 EDF R&D
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

numpy.random.seed(1000)
dimension = 300

xt = numpy.matrix(numpy.arange(dimension)).T
Eo = numpy.matrix(numpy.zeros((dimension,))).T
Eb = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
H  = numpy.matrix(numpy.core.identity(dimension))
B = numpy.matrix(numpy.core.identity(dimension)).T
R = numpy.matrix(numpy.core.identity(dimension)).T

def FunctionH( X ):
    return H * X

xb = xt + Eb
xb = xb.A1
yo = FunctionH( xt ) + Eo
yo = yo.A1

Background = xb
BackgroundError = B
Observation = yo
ObservationError = R
