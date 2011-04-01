import numpy
import pickle

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

if method == "Direct":
  result = FunctionH(numpy.matrix(computation["inputValues"][0][0]).T)

if method == "Tangent":
  result = FunctionH(numpy.matrix(computation["inputValues"][0][0]).T)

if method == "Adjoint":
  result = AdjointH((numpy.matrix(computation["inputValues"][0][0]).T, numpy.matrix(computation["inputValues"][0][1]).T))

print "Computation end"
