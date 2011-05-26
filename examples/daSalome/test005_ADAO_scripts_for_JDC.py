#-*-coding:iso-8859-1-*-
import numpy
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
dimension = len( Xcurrent )
H  = numpy.matrix(numpy.core.identity(dimension))
#
def FunctionH( X ):
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
