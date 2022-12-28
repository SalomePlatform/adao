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
    Algorithm='ExtendedBlue',
    Parameters={
        'StoreSupplementaryCalculations': [
            'APosterioriCovariance',
            ],
        },
    )
case.execute()
#
#-------------------------------------------------------------------------------
#
print("Interpolation between two vectors, of observation and background")
print("----------------------------------------------------------------")
print("")
print("Observation vector............:", ravel(case.get('Observation')))
print("A priori background vector....:", ravel(case.get('Background')))
print("")
print("Expected theoretical state....:", ravel([5., 6., 7.]))
print("")
print("Interpolation result..........:", ravel(case.get('Analysis')[-1]))
print("A posteriori covariance.......:\n", case.get('APosterioriCovariance')[-1])
