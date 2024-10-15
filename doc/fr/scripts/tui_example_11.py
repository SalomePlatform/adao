# -*- coding: utf-8 -*-
#
import numpy
from adao import adaoBuilder
#
# =============================================================
# POSITION DU PROBLÈME
#
# Construction artificielle d'un exemple de données utilisateur
# -------------------------------------------------------------
alpha = 5.
beta = 7
gamma = 9.0
#
alphamin, alphamax = 0., 10.
betamin,  betamax  = 3, 13
gammamin, gammamax = 1.5, 15.5
#
def simulation(x):
    "Fonction de simulation H pour effectuer Y=H(X)"
    __x = numpy.ravel(x)
    __H = numpy.array([[1,0,0],[0,2,0],[0,0,3],[1,2,3]])
    return numpy.dot(__H, __x)
#
# Observations obtenues par simulation
# ------------------------------------
Xtrue = (2, 3, 4)
observations = simulation(Xtrue)
#
# =============================================================
# RÉSOLUTION DU PROBLÈME
#
# Mise en forme des entrées
# -------------------------
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
        "MaximumNumberOfIterations":100,
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
# Récupération des variables d'intérêt
# ------------------------------------
Xbackground   = case.get("Background")
Xoptimum      = case.get("Analysis")[-1]
FX_at_optimum = case.get("SimulatedObservationAtOptimum")[-1]
J_values      = case.get("CostFunctionJ")[:]
#
# =============================================================
# EXPLOITATION INDÉPENDANTE DES RÉSULTATS
#
print("")
print("Nombre d'itérations internes...: %i"%len(J_values))
print("État initial...................: %s"%(numpy.ravel(Xbackground),))
print("État idéalisé..................: %s"%(numpy.ravel(Xtrue)*1.,))
print("État optimal...................: %s"%(numpy.ravel(Xoptimum),))
print("Simulation à l'état optimal....: %s"%(numpy.ravel(FX_at_optimum),))
print("")
