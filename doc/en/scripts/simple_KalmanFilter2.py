# -*- coding: utf-8 -*-
#
from numpy import array, random
random.seed(1234567)
Xtrue = -0.37727
Yobs = []
for i in range(51):
    Yobs.append([random.normal(Xtrue, 0.1, size=(1,)),])
#
print("Estimation of a constant variable by filtering")
print("----------------------------------------------")
print("  Noisy measurements acquired on %i time steps"%(len(Yobs)-1,))
print("")
from adao import adaoBuilder
case = adaoBuilder.New('')
#
case.setObservationOperator(Matrix             = [1.])
case.setObservationError   (ScalarSparseMatrix = 0.1**2)
#
case.setEvolutionModel     (Matrix             = [1.])
case.setEvolutionError     (ScalarSparseMatrix = 1e-5)
#
case.setAlgorithmParameters(
    Algorithm="KalmanFilter",
    Parameters={
        "StoreSupplementaryCalculations":[
            "Analysis",
            "APosterioriCovariance",
            ],
        },
    )
#
XaStep, VaStep = 0., 1.
for i in range(1,len(Yobs)):
    case.setBackground         (Vector             = "%s"%float(XaStep))
    case.setBackgroundError    (ScalarSparseMatrix = "%s"%float(VaStep))
    case.setObservation        (Vector             = Yobs[i])
    case.execute( nextStep = True )
    XaStep = case.get("Analysis")[-1]
    VaStep = case.get("APosterioriCovariance")[-1]
#
Xa = case.get("Analysis")
Pa = case.get("APosterioriCovariance")
#
print("")
print("  Final a posteriori variance:",Pa[-1])
print("")
