import numpy
import pickle

print computation["method"]

dimension = 300

H  = numpy.matrix(numpy.core.identity(dimension))

def FunctionH( X ):
    return H * X

def AdjointH( (X, Y) ):
    return H.T * Y

if computation["method"] == "Direct":
  result = FunctionH(computation["data"])

if computation["method"] == "Tangent":
  result = FunctionH(computation["data"])

if computation["method"] == "Adjoint":
  result = AdjointH(computation["data"])

print "Computation end"
