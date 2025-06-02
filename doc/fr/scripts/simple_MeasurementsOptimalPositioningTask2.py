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
    Algorithm = "MeasurementsOptimalPositioningTask",
    Parameters = {
        "EnsembleOfSnapshots":Ensemble,
        "MaximumNumberOfLocations":3,
        "ErrorNorm":"L2",
        "StoreSupplementaryCalculations":[
            "ReducedBasis",
            "Residus",
        ],
    }
)
case.execute()
print("- Calcul ADAO effectué")
print()
#
print("Affichage des positions optimales de mesure")
print("-------------------------------------------")
op = case.get("OptimalPoints")[-1]
print("- Nombre de positions optimales de mesure..............: %i"%op.size)
print("- Positions optimales de mesure, numérotées par défaut.: %s"%op)
print()
#
print("Représentation réduite et informations d'erreurs")
print("------------------------------------------------")
rb = case.get("ReducedBasis")[-1]
print("- Nombre de vecteurs de la base réduite................: %i"%rb.shape[1])
print("- Vecteurs de la base réduite (un par colonne)\n")
print(rb)
rs = case.get("Residus")[-1]
print("- Résidus ordonnés d'erreur de reconstruction\n ",rs)
print()
a0, a1 = 7, -2.5
print("- Exemple élémentaire de reconstruction du second champ comme une")
print("  combinaison linéaire des deux vecteurs de base, qui peuvent être")
print("  multipliés par les coefficients respectifs %.1f et %.1f :"%(a0,a1))
print( a0*rb[:,0] + a1*rb[:,1])
print()
