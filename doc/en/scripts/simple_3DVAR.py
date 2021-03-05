# -*- coding: utf-8 -*-
#
from numpy import array, ravel
def QuadFunction( coefficients ):
    """
    Simulation : y = a x^2 + b x + c
    """
    a, b, c = list(ravel(coefficients))
    x_points = (-5, 0, 1, 3, 10)
    y_points = []
    for x in x_points:
        y_points.append( a*x*x + b*x + c )
    return array(y_points)
#
Xb   = array([1., 1., 1.])
Yobs = array([57, 2, 3, 17, 192])
#
print("Variational resolution of the calibration problem")
print("-------------------------------------------------")
print("")
from adao import adaoBuilder
case = adaoBuilder.New('')
case.setBackground( Vector = Xb, Stored=True )
case.setBackgroundError( ScalarSparseMatrix = 1.e6 )
case.setObservation( Vector = Yobs, Stored=True )
case.setObservationError( ScalarSparseMatrix = 1. )
case.setObservationOperator( OneFunction = QuadFunction )
case.setAlgorithmParameters(
    Algorithm='3DVAR',
    Parameters={
        'MaximumNumberOfSteps': 100,
        'StoreSupplementaryCalculations': [
            'CurrentState',
            ],
        },
    )
case.setObserver(
    Info="  Intermediate state at the current iteration:",
    Template='ValuePrinter',
    Variable='CurrentState',
    )
case.execute()
print("")
#
#-------------------------------------------------------------------------------
#
print("Calibration of %i coefficients in a 1D quadratic function on %i measures"%(
    len(case.get('Background')),
    len(case.get('Observation')),
    ))
print("----------------------------------------------------------------------")
print("")
print("Observation vector.................:", ravel(case.get('Observation')))
print("A priori background state..........:", ravel(case.get('Background')))
print("")
print("Expected theoretical coefficients..:", ravel((2,-1,2)))
print("")
print("Calibration resulting coefficients.:", ravel(case.get('Analysis')[-1]))
