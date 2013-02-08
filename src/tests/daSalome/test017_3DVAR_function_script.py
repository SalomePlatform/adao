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

print computation
method = ""
for param in computation["specificParameters"]:
  if param["name"] == "method":
    method = param["value"]
print "Method found is", method

dimension = 300
H  = numpy.matrix(numpy.core.identity(dimension))

def FunctionH( X ):
    return H * X

def AdjointH( (X, Y) ):
    return H.T * Y

print computation["inputValues"][0][0][0]
print computation["inputValues"][0][0][0][0]

if method == "Direct":
  data = FunctionH(numpy.matrix(computation["inputValues"][0][0][0]).T)

if method == "Tangent":
  data = FunctionH(numpy.matrix(computation["inputValues"][0][0][0]).T)

if method == "Adjoint":
  data = AdjointH((numpy.matrix(computation["inputValues"][0][0][0]).T, numpy.matrix(computation["inputValues"][0][0][1]).T))


outputValues = [[[[]]]]
it = data.flat
for val in it:
  outputValues[0][0][0].append(val)

print outputValues

result = {}
result["outputValues"] = outputValues
result["specificOutputInfos"] = []
result["returnCode"] = 0
result["errorMessage"] = ""

print result
print "Computation end"
