# -*- coding: utf-8 -*-
#
from numpy import array, ravel, abs, max, set_printoptions
set_printoptions(precision=7)
def QuadFunction( coefficients ):
    """
    Quadratic simulation in x points: y = a x^2 + b x + c
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
from adao import adaoBuilder
case = adaoBuilder.New()
case.setBackground( Vector = Xb, Stored=True )
case.setBackgroundError( ScalarSparseMatrix = 1.e6 )
case.setObservation( Vector = Yobs, Stored=True )
case.setObservationError( ScalarSparseMatrix = 1. )
case.setObservationOperator( OneFunction = QuadFunction )
case.setAlgorithmParameters(
    Algorithm="ParameterCalibrationTask",
    Parameters={
        "Variant":"3DVARGradientOptimization",
        "Minimizer":"LBFGSB",
        "MaximumNumberOfIterations": 100,
        "StoreSupplementaryCalculations": [
            "CurrentState",
            "OMA",
            ],
        },
    )
case.execute()
#
#-------------------------------------------------------------------------------
#
print("Calibration of %i coefficients in a 1D quadratic function on %i measures"%(
    len(case.get("Background")),
    len(case.get("Observation")),
    ))
print("----------------------------------------------------------------------")
print("")
print("Observation vector.................:", ravel(case.get("Observation")))
print("A priori background state..........:", ravel(case.get("Background")))
print("")
print("Expected theoretical coefficients..:", ravel((2,-1,2)))
print("")
print("Number of simulations..............:", len(case.get("CurrentState"))*4)
print("Maximum diff. Observation-Analyse..:", "%.2e"%max(abs(ravel(case.get("OMA")[-1]))))
print("Calibration resulting coefficients.:", ravel(case.get("Analysis")[-1]))
#
Xa = case.get("Analysis")[-1]
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10, 4)
#
plt.figure()
plt.plot((-5,0,1,3,10),QuadFunction(Xb),"b--",label="Simulation at background")
plt.plot((-5,0,1,3,10),Yobs,            "kX", label="Observation",markersize=10)
plt.plot((-5,0,1,3,10),QuadFunction(Xa),"r-", label="Simulation at optimum")
plt.legend()
plt.title("Coefficients calibration", fontweight="bold")
plt.xlabel("Arbitrary coordinate")
plt.ylabel("Observations")
plt.savefig("simple_ParameterCalibrationTask1.png")
