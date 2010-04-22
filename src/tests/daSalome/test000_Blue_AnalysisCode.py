#-*-coding:iso-8859-1-*-
import numpy
precision = 1.e-13

Xa = ADD.get("Analysis")
print
print "    Nombre d'analyses  :",Xa.stepnumber()
print "    Analyse résultante :",Xa.valueserie(0)
#
# Vérification du résultat
# ------------------------
if max(numpy.array(Xa.valueserie(0))-numpy.array([0.25, 1.25, 2.25])) > precision:
  raise ValueError("Résultat du test erroné")
else:
  print "    Test correct, erreur maximale inférieure à %s"%precision
  print

