import numpy
import pickle
import test_aster_zzzz159a_aster_functions as Code_Aster

# Configuration du module
Code_Aster.debug = init_data["debug"]
Code_Aster.ASTER_ROOT = init_data["ASTER_ROOT"]
Code_Aster.SOURCES_ROOT = init_data['SOURCES_ROOT']
Code_Aster.export = init_data["export"]
Code_Aster.calcul = init_data["calcul"]
Code_Aster.parametres = init_data["parametres"]
Code_Aster.python_version = init_data["python_version"]

print computation["method"]

if computation["method"] == "Direct":
  result = Code_Aster.Calcul_Aster_Ponctuel(computation["data"])

if computation["method"] == "Tangent":
  result = Code_Aster.Calcul_Aster_Ponctuel(computation["data"])

if computation["method"] == "Adjoint":
  result = Code_Aster.Calcul_Aster_Adjoint(computation["data"])

print "Computation end"

