# -*- coding: utf-8 -*-
#
from numpy import array, random
random.seed(1234567)
Xtrue = -0.37727
Yobs = []
for i in range(51):
    Yobs.append([random.normal(Xtrue, 0.1, size=(1,)),])
#
print("Variational estimation of a time trajectory")
print("-------------------------------------------")
print("  Noisy measurements acquired on %i time steps"%(len(Yobs)-1,))
print("")
from adao import adaoBuilder
case = adaoBuilder.New()
#
case.setBackground         (Vector             = [0.])
case.setBackgroundError    (ScalarSparseMatrix = 0.1**2)
#
case.setObservationOperator(Matrix             = [1.])
case.setObservation        (VectorSerie        = Yobs)
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
case.execute()
Xa = case.get("Analysis")
Pa = case.get("APosterioriCovariance")
#
print("  Analyzed state at final observation:", Xa[-1])
print("")
print("  Final a posteriori variance:", Pa[-1])
print("")
#
#-------------------------------------------------------------------------------
#
Observations = array([yo[0]   for yo in Yobs])
Estimates    = array([xa[0]   for xa in case.get("Analysis")])
Variances    = array([pa[0,0] for pa in case.get("APosterioriCovariance")])
#
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 4)
#
plt.figure()
plt.plot(Observations,'kx',label='Noisy measurements')
plt.plot(Estimates,'r-',label='Estimated state')
plt.axhline(Xtrue,color='b',label='Truth value')
plt.legend()
plt.title('Estimate of the state', fontweight='bold')
plt.xlabel('Observation step')
plt.ylabel('Voltage')
plt.savefig("simple_3DVAR2_state.png")
#
plt.figure()
iobs = range(1,len(Observations))
plt.plot(iobs,Variances[iobs],label='A posteriori error variance')
plt.title('Estimate of the a posteriori error variance', fontweight='bold')
plt.xlabel('Observation step')
plt.ylabel('$(Voltage)^2$')
plt.setp(plt.gca(),'ylim',[0,.01])
plt.savefig("simple_3DVAR2_variance.png")
