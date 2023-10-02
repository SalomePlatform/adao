# -*- coding: utf-8 -*-
#
from numpy import array, arange, ravel, set_printoptions
set_printoptions(precision=3)
#
dimension = 7
#
print("Définition d'un ensemble artificiel de champs physiques")
print("-------------------------------------------------------")
Ensemble = array( [i+arange(dimension) for i in range(7)] ).T
print("- Dimension de l'espace des champs physiques...........: %i"%dimension)
print("- Nombre de vecteurs de champs physiques...............: %i"%Ensemble.shape[1])
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
print("Reconstruction par interpolation d'états mesurés connus")
print("-------------------------------------------------------")
rb = case.get("ReducedBasis")[-1]
measures_at_op = Ensemble[op,1]
#
interpolation = adaoBuilder.New()
interpolation.setAlgorithmParameters(
    Algorithm = 'InterpolationByReducedModelTask',
    Parameters = {
        "ReducedBasis":rb,
        "OptimalLocations":op,
        }
    )
interpolation.setObservation( Vector = measures_at_op )
interpolation.execute()
field = interpolation.get("Analysis")[-1]
print("- État de référence 1 utilisé pour l'apprentissage.....:",ravel(Ensemble[:,1]))
print("- Positions optimales de mesure, numérotées par défaut.: %s"%op)
print("- Mesures extraites de l'état 1 pour la reconstruction.:",measures_at_op)
print("- État 1 reconstruit avec la précision de 1%...........:",field)
if max(abs(ravel(Ensemble[:,1])-field)) < 1.e-2:
    print("  ===> Aucune différence n'existe entre les deux états, comme attendu")
else:
    raise ValueError("Différence constatée sur l'état de référence 1")
print()
#
print("Reconstruction par interpolation d'états mesurés non connus")
print("-----------------------------------------------------------")
measures_at_op = array([4, 3])
interpolation.setObservation( Vector = measures_at_op )
interpolation.execute()
field = interpolation.get("Analysis")[-1]
print("  Illustration d'une interpolation sur mesures réelles non connues")
print("- Positions optimales de mesure, numérotées par défaut.: %s"%op)
print("- Mesures non présentes dans les états connus..........:",measures_at_op)
print("- État reconstruit avec la précision de 1%.............:",field)
print("  ===> Aux positions de mesure %s, le champ reconstruit est égal à la mesure"%op)
print()
