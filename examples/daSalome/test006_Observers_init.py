#-*-coding:iso-8859-1-*-
# Copyright (C) 2010-2011 EDF R&D
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

def FunctionH( X ):
  return H * X

dimension = 3
xt = numpy.matrix(numpy.arange(dimension)).T
Eo = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
Eb = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
H  = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,dimension)))
xb = xt + Eb
yo = FunctionH( xt ) + Eo
xb = xb.A1
yo = yo.A1
R  = numpy.matrix(numpy.core.identity(dimension)).T
B  = numpy.matrix(numpy.core.identity(dimension)).T

#
# Definition of the Background as a vector
# ----------------------------------------
Background = xb
#
# Definition of the Observation as a vector
# -----------------------------------------
Observation = yo
#
# Definition of the Background Error covariance as a matrix
# ---------------------------------------------------------
BackgroundError = B
#
# Definition of the Observation Error covariance as a matrix
# ----------------------------------------------------------
ObservationError = R

print xb
print B
print yo
print R

#
# Definition of the init_data dictionnary
# ---------------------------------------
init_data = {}
init_data["Background"]          = Background
init_data["Observation"]         = Observation
init_data["BackgroundError"]     = BackgroundError
init_data["ObservationError"]    = ObservationError

# Algorithm Parameters
init_data["AlgorithmParameters"] = {"Minimizer":"LBFGSB","MaximumNumberOfSteps":5}
