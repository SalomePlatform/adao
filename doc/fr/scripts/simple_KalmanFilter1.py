# -*- coding: utf-8 -*-
#
from numpy import array, random
random.seed(1234567)
Xtrue = -0.37727
Yobs = []
for i in range(51):
    Yobs.append([random.normal(Xtrue, 0.1, size=(1,)),])
#
print("Estimation par filtrage d'une variable constante")
print("------------------------------------------------")
print("  Observations bruitées acquises sur %i pas de temps"%(len(Yobs)-1,))
print("")
from adao import adaoBuilder
case = adaoBuilder.New('')
#
case.setBackground         (Vector             = [0.])
case.setBackgroundError    (ScalarSparseMatrix = 1.)
#
case.setObservationOperator(Matrix             = [1.])
case.setObservation        (VectorSerie        = Yobs)
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
case.setObserver(
    Info="  État analysé à l'observation courante :",
    Template='ValuePrinter',
    Variable='Analysis',
    )
case.execute()
Xa = case.get("Analysis")
Pa = case.get("APosterioriCovariance")
#
print("")
print("  Variance a posteriori finale :",Pa[-1])
print("")
