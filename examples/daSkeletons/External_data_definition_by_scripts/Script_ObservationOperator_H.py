#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2016 EDF R&D
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

    Script defining the ObservationOperator
    """
__author__ = "Jean-Philippe ARGAUD"
#
# ==============================================================================
#
import Physical_simulation_functions
import numpy, logging
#
# -----------------------------------------------------------------------
# SALOME input data and parameters: all information are the required input
# variable "computation", containing for example:
#      {'inputValues': [[[[0.0, 0.0, 0.0]]]],
#       'inputVarList': ['adao_default'],
#       'outputVarList': ['adao_default'],
#       'specificParameters': [{'name': 'method', 'value': 'Direct'}]}
# -----------------------------------------------------------------------
#
# Recovering the type of computation: "Direct", "Tangent" or "Adjoint"
# --------------------------------------------------------------------
method = ""
for param in computation["specificParameters"]:
    if param["name"] == "method":
        method = param["value"]
logging.info("ComputationFunctionNode: Found method is \'%s\'"%method)
#
# Loading the H operator functions from external definitions
# ----------------------------------------------------------
logging.info("ComputationFunctionNode: Loading operator functions")
DirectOperator = Physical_simulation_functions.DirectOperator
TangentOperator  = Physical_simulation_functions.TangentOperator
AdjointOperator  = Physical_simulation_functions.AdjointOperator
#
# Executing the possible computations
# -----------------------------------
if method == "Direct":
    logging.info("ComputationFunctionNode: Direct computation")
    Xcurrent = computation["inputValues"][0][0][0]
    data = DirectOperator(numpy.matrix( Xcurrent ).T)
#
if method == "Tangent":
    logging.info("ComputationFunctionNode: Tangent computation")
    Xcurrent = computation["inputValues"][0][0][0]
    data = TangentOperator(numpy.matrix( Xcurrent ).T)
#
if method == "Adjoint":
    logging.info("ComputationFunctionNode: Adjoint computation")
    Xcurrent = computation["inputValues"][0][0][0]
    Ycurrent = computation["inputValues"][0][0][1]
    data = AdjointOperator((numpy.matrix( Xcurrent ).T, numpy.matrix( Ycurrent ).T))
#
# Formatting the output
# ---------------------
logging.info("ComputationFunctionNode: Formatting the output")
it = data.flat
outputValues = [[[[]]]]
for val in it:
  outputValues[0][0][0].append(val)
#
# Creating the required ADAO variable
# -----------------------------------
result = {}
result["outputValues"]        = outputValues
result["specificOutputInfos"] = []
result["returnCode"]          = 0
result["errorMessage"]        = ""
#
# ==============================================================================
