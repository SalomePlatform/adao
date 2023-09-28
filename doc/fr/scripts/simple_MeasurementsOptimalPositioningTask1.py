# -*- coding: utf-8 -*-
#
from numpy import array, arange
#
dimension = 7
#
print("Définition d'un ensemble artificiel de champs physiques")
print("-------------------------------------------------------")
Ensemble = array( [i+arange(dimension) for i in range(7)] ).T
print("- Dimension de l'espace des champs physiques...........: %i"%dimension)
print("- Nombre de vecteurs de champs physiques...............: %i"%Ensemble.shape[1])
print("- Collection des champs physiques (un par colonne)")
print(Ensemble)
print()
#
print("Recherche des positions optimales de mesure")
print("-------------------------------------------")
from adao import adaoBuilder
case = adaoBuilder.New()
case.setAlgorithmParameters(
    Algorithm = 'MeasurementsOptimalPositioningTask',
    Parameters = {
        "EnsembleOfSnapshots":Ensemble,
        "MaximumNumberOfLocations":3,
        "ErrorNorm":"L2",
    }
)
case.execute()
print("- Calcul ADAO effectué")
print()
#
print("Positions optimales de mesure")
print("-----------------------------")
op = case.get("OptimalPoints")[-1]
print("- Nombre de positions optimales de mesure..............: %i"%op.size)
print("- Positions optimales de mesure, numérotées par défaut.: %s"%op)
print()
