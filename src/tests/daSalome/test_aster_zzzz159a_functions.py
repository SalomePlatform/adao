import numpy
import pickle
import sys

sys.path.insert(0, init_data['SOURCES_ROOT'])
import test_aster_zzzz159a_aster_functions as Code_Aster

# Configuration du module
Code_Aster.debug = init_data["debug"]
Code_Aster.ASTER_ROOT = init_data["ASTER_ROOT"]
Code_Aster.SOURCES_ROOT = init_data['SOURCES_ROOT']
Code_Aster.export = init_data["export"]
Code_Aster.calcul = init_data["calcul"]
Code_Aster.parametres = init_data["parametres"]
Code_Aster.python_version = init_data["python_version"]

print computation
method = ""
for param in computation["specificParameters"]:
  if param["name"] == "method":
    method = param["value"]

# Extraction des données et remise en forme (normalement à faire
# dans le code
# On sait qu'on a trois variables
input_data = []
for i in range(3):
  input_data.append(computation["inputValues"][0][i][0])

if method == "Adjoint":
  input_data = (input_data, [])
  for i in range(22):
    if i < 11:
      input_data[1].append(computation["inputValues"][0][3][i])
    else:
      input_data[1].append(computation["inputValues"][0][4][i-11])

if method == "Direct":
  output_data = Code_Aster.Calcul_Aster_Ponctuel(input_data)

if method == "Tangent":
  output_data = Code_Aster.Calcul_Aster_Ponctuel(input_data)

if method == "Adjoint":
  output_data = Code_Aster.Calcul_Aster_Adjoint(input_data)

outputValues = [[[]]]
for val in output_data:
  outputValues[0][0].append(val)

result = {}
result["outputValues"] = outputValues
result["specificOutputInfos"] = []
result["returnCode"] = 0
result["errorMessage"] = ""
print "Computation end"
