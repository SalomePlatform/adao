# -*- coding: utf-8 -*-
#
from numpy import array, ravel
def QuadFunction( coefficients ):
    """
    Quadratic simulation in x: y = a x^2 + b x + c
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
print("Resolution of the calibration problem")
print("-------------------------------------")
print("")
from adao import adaoBuilder
case = adaoBuilder.New('')
case.setBackground( Vector = Xb, Stored=True )
case.setObservation( Vector = Yobs, Stored=True )
case.setObservationError( ScalarSparseMatrix = 1. )
case.setObservationOperator( OneFunction = QuadFunction )
case.setAlgorithmParameters(
    Algorithm='NonLinearLeastSquares',
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
#
Xa = case.get('Analysis')[-1]
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 4)
#
plt.figure()
plt.plot((-5,0,1,3,10),QuadFunction(Xb),'b-',label="Simulation at background")
plt.plot((-5,0,1,3,10),Yobs,            'kX',label='Observation',markersize=10)
plt.plot((-5,0,1,3,10),QuadFunction(Xa),'r-',label="Simulation at optimum")
plt.legend()
plt.title('Coefficients calibration', fontweight='bold')
plt.xlabel('Arbitrary coordinate')
plt.ylabel('Observation Yobs')
plt.savefig("simple_NonLinearLeastSquares.png")
