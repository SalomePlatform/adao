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
  data = FunctionH(numpy.matrix(computation["inputValues"][0][0]).T)

if method == "Tangent":
  data = FunctionH(numpy.matrix(computation["inputValues"][0][0]).T)

if method == "Adjoint":
  data = AdjointH((numpy.matrix(computation["inputValues"][0][0]).T, numpy.matrix(computation["inputValues"][0][1]).T))


outputValues = [[[]]]
it = data.flat
for val in it:
  outputValues[0][0].append(val)

print outputValues

result = {}
result["outputValues"] = outputValues
result["specificOutputInfos"] = []
result["returnCode"] = 0
result["errorMessage"] = ""

print result
print "Computation end"
