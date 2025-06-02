# -*- coding: utf-8 -*-
#
from numpy import array, random
random.seed(1234567)
Xtrue = -0.37727
Yobs = []
for i in range(51):
    Yobs.append([random.normal(Xtrue, 0.1, size=(1,)),])
#
print("Estimation variationnelle d'une trajectoire temporelle")
print("------------------------------------------------------")
print("  Observations bruitées acquises sur %i pas de temps"%(len(Yobs)-1,))
print("")
from adao import adaoBuilder
case = adaoBuilder.New()
#
case.setBackground         (Vector             = [0.])
#
case.setObservationOperator(Matrix             = [1.])
case.setObservationError   (ScalarSparseMatrix = 0.3**2)
#
case.setEvolutionModel     (Matrix             = [1.])
case.setEvolutionError     (ScalarSparseMatrix = 1e-5)
#
case.setAlgorithmParameters(
    Algorithm="3DVAR",
    Parameters={
        "EstimationOf":"State",
        "StoreSupplementaryCalculations":[
            "Analysis",
            "APosterioriCovariance",
            ],
        },
    )
#
# Boucle pour obtenir une analyse à l'arrivée de chaque observation
#
Ca = 1.
for i in range(1,len(Yobs)):
    case.setObservation(Vector = Yobs[i])
    case.setBackgroundError(ScalarSparseMatrix = Ca) # Covariance remise à jour
    case.execute( nextStep = True )
    #
    # Hypothèse de décroissance de la covariance a priori de l'erreur d'ébauche
    #
    if float(Ca) <= 0.1**2:
        Ca = 0.1**2
    else:
        Ca = Ca * 0.9**2
#
Xa = case.get("Analysis")
Pa = case.get("APosterioriCovariance")
#
print("  État analysé à l'observation finale :", Xa[-1])
print("")
print("  Variance a posteriori finale :", Pa[-1])
print("")
#
#-------------------------------------------------------------------------------
#
Observations = array([yo[0]   for yo in Yobs])
Estimates    = array([xa[0]   for xa in case.get("Analysis")])
Variances    = array([pa[0,0] for pa in case.get("APosterioriCovariance")])
#
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10, 4)
#
plt.figure()
plt.plot(Observations,"kx",label="Mesures bruitées")
plt.plot(Estimates,"r-",label="État estimé")
plt.axhline(Xtrue,color="b",label="Valeur vraie")
plt.legend()
plt.title("Estimation de l'état", fontweight="bold")
plt.xlabel("Pas d'observation")
plt.ylabel("Tension")
plt.savefig("simple_3DVAR3_state.png")
#
plt.figure()
iobs = range(1,len(Observations))
plt.plot(iobs,Variances[iobs],label="Variance d'erreur a posteriori")
plt.title("Estimation de la variance d'erreur a posteriori", fontweight="bold")
plt.xlabel("Pas d'observation")
plt.ylabel("$(Tension)^2$")
plt.savefig("simple_3DVAR3_variance.png")
