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
  result = FunctionH(computation["data"])

if method == "Tangent":
  result = FunctionH(computation["data"])

if method == "Adjoint":
  result = AdjointH(computation["data"])

print "Computation end"
