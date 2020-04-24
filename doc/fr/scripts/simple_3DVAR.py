# -*- coding: utf-8 -*-
#
from numpy import array, ravel
def QuadFunction( coefficients ):
    """
    Fonction : y = a x^2 + b x + c
    """
    a, b, c = list(ravel(coefficients))
    x_points = (-5, 0, 1, 3, 10)
    y_points = []
    for x in x_points:
        y_points.append( a*x*x + b*x + c )
    return array(y_points)
#
print("Résolution itérative du problème de calibration")
print("-----------------------.-----------------------")
print("")
from adao import adaoBuilder
case = adaoBuilder.New('')
case.setBackground( Vector = array([1., 1., 1.]), Stored=True )
case.setBackgroundError( ScalarSparseMatrix = 1.e6 )
case.setObservation( Vector=array([57, 2, 3, 17, 192]), Stored=True )
case.setObservationError( ScalarSparseMatrix = 1. )
case.setObservationOperator( OneFunction = QuadFunction )
case.setAlgorithmParameters(
    Algorithm='3DVAR',
    Parameters={
        'StoreSupplementaryCalculations': [
            'CurrentState',
            ],
        },
    )
case.setObserver(
    Info="  État intermédiaire en itération courante :",
    Template='ValuePrinter',
    Variable='CurrentState',
    )
case.execute()
print("")
#
#-------------------------------------------------------------------------------
#
print("Calibration de %i coefficients pour une forme quadratique 1D sur %i mesures"%(
    len(case.get('Background')),
    len(case.get('Observation')),
    ))
print("------------------------------------------------------------------------")
print("")
print("Vecteur observation.......................:", ravel(case.get('Observation')))
print("État ébauche a priori.....................:", ravel(case.get('Background')))
print("")
print("Coefficients théoriques attendus..........:", ravel((2,-1,2)))
print("")
print("Coefficients résultants de la calibration.:", ravel(case.get('Analysis')[-1]))