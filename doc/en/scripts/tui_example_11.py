# -*- coding: utf-8 -*-
#
import numpy
from adao import adaoBuilder
#
# =============================================================
# PROBLEM SETTINGS
#
# Artificial building of an example of user data
# ----------------------------------------------
alpha = 5.
beta = 7
gamma = 9.0
#
alphamin, alphamax = 0., 10.
betamin,  betamax  = 3, 13
gammamin, gammamax = 1.5, 15.5
#
def simulation(x):
    "Simulation function H to perform Y=H(X)"
    __x = numpy.ravel(x)
    __H = numpy.array([[1,0,0],[0,2,0],[0,0,3],[1,2,3]])
    return numpy.dot(__H, __x)
#
# Observations obtained by simulation
# -----------------------------------
Xtrue = (2, 3, 4)
observations = simulation(Xtrue)
#
# =============================================================
# SOLVING THE PROBLEM
#
# Formatting entries
# ------------------
Xb = (alpha, beta, gamma)
Bounds = (
    (alphamin, alphamax),
    (betamin,  betamax ),
    (gammamin, gammamax))
#
# ADAO TUI
# --------
case = adaoBuilder.New()
case.set(
    'AlgorithmParameters',
    Algorithm = '3DVAR',
    Parameters = {
        "Bounds":Bounds,
        "MaximumNumberOfSteps":100,
        "StoreSupplementaryCalculations":[
            "CostFunctionJ",
            "CurrentState",
            "SimulatedObservationAtOptimum",
            ],
        }
    )
case.set( 'Background', Vector = numpy.array(Xb), Stored = True )
case.set( 'Observation', Vector = numpy.array(observations) )
case.set( 'BackgroundError', ScalarSparseMatrix = 1.0e10 )
case.set( 'ObservationError', ScalarSparseMatrix = 1.0 )
case.set(
    'ObservationOperator',
    OneFunction = simulation,
    Parameters  = {"DifferentialIncrement":0.0001},
    )
case.set( 'Observer', Variable="CurrentState", Template="ValuePrinter" )
case.execute()
#
# Getting variables of interest
# -----------------------------
Xbackground   = case.get("Background")
Xoptimum      = case.get("Analysis")[-1]
FX_at_optimum = case.get("SimulatedObservationAtOptimum")[-1]
J_values      = case.get("CostFunctionJ")[:]
#
# =============================================================
# INDEPENDENT HOLDING OF RESULTS
#
print("")
print("Number of internal iterations...: %i"%len(J_values))
print("Initial state...................: %s"%(numpy.ravel(Xbackground),))
print("Idealized state.................: %s"%(numpy.ravel(Xtrue)*1.,))
print("Optimal state...................: %s"%(numpy.ravel(Xoptimum),))
print("Simulation at optimal state.....: %s"%(numpy.ravel(FX_at_optimum),))
print("")
