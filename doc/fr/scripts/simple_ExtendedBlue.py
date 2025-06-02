# -*- coding: utf-8 -*-
#
from numpy import array, ravel
from adao import adaoBuilder
case = adaoBuilder.New()
case.setBackground( Vector = array([0., 1., 2.]), Stored=True )
case.setBackgroundError( ScalarSparseMatrix = 1. )
case.setObservation( Vector = array([10., 11., 12.]), Stored=True )
case.setObservationError( ScalarSparseMatrix = 1. )
case.setObservationOperator( Matrix = array([[1., 0., 0.],
                                             [0., 1., 0.],
                                             [0., 0., 1.]]), )
case.setAlgorithmParameters(
    Algorithm="ExtendedBlue",
    Parameters={
        "StoreSupplementaryCalculations": [
            "APosterioriCovariance",
            ],
        },
    )
case.execute()
#
#-------------------------------------------------------------------------------
#
print("Interpolation entre deux états vectoriels, observation et ébauche")
print("-----------------------------------------------------------------")
print("")
print("Vecteur d'observation.........:", ravel(case.get("Observation")))
print("État d'ébauche a priori.......:", ravel(case.get("Background")))
print("")
print("État théorique attendu........:", ravel([5., 6., 7.]))
print("")
print("État obtenu par interpolation.:", ravel(case.get("Analysis")[-1]))
print("Covariance a posteriori.......:\n", case.get("APosterioriCovariance")[-1])
