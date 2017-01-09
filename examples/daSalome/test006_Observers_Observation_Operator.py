#-*-coding:iso-8859-1-*-
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

import numpy
import time
import logging
logging.info("ComputationFunctionNode: Begin")
# ==============================================================================
# Input data and parameters: all is in the required input variable
# "computation", containing for example:
#      {'inputValues': [[[[0.0, 0.0, 0.0]]]],
#       'inputVarList': ['adao_default'],
#       'outputVarList': ['adao_default'],
#       'specificParameters': [{'name': 'method', 'value': 'Direct'}]}
# ==============================================================================
#
# Recovering the type of computation: "Direct", "Tangent" or "Adjoint"
# --------------------------------------------------------------------
method = ""
for param in computation["specificParameters"]:
    if param["name"] == "method":
        method = param["value"]
logging.info("ComputationFunctionNode: Found method is \'%s\'"%method)
#
# Recovering the current control state X
# --------------------------------------
Xcurrent = computation["inputValues"][0][0][0]
#
# Building explicit calculation or requiring external ones
# --------------------------------------------------------
dimension = 3
H  = numpy.matrix(numpy.core.identity(dimension))
#
def FunctionH( X ):
    time.sleep(1)
    return H * X
#
def AdjointH( (X, Y) ):
    return H.T * Y
#
# The possible computations
# -------------------------
if method == "Direct":
    logging.info("ComputationFunctionNode: Direct computation")
    data = FunctionH(numpy.matrix( Xcurrent ).T)
#
if method == "Tangent":
    logging.info("ComputationFunctionNode: Tangent computation")
    data = FunctionH(numpy.matrix( Xcurrent ).T)
#
if method == "Adjoint":
    logging.info("ComputationFunctionNode: Adjoint computation")
    Ycurrent = computation["inputValues"][0][0][1]
    data = AdjointH((numpy.matrix( Xcurrent ).T, numpy.matrix( Ycurrent ).T))
#
# Formatting the output
# ---------------------
logging.info("ComputationFunctionNode: Formatting the output")
it = data.flat
outputValues = [[[[]]]]
for val in it:
  outputValues[0][0][0].append(val)
#
result = {}
result["outputValues"]        = outputValues
result["specificOutputInfos"] = []
result["returnCode"]          = 0
result["errorMessage"]        = ""
#
logging.info("ComputationFunctionNode: End")
