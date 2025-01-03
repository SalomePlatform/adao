# -*- coding: utf-8 -*-
#
import numpy
from adao import adaoBuilder
from Models.Lorenz1963 import EDS as Lorenz1963
numpy.set_printoptions(precision=5)
#
u0Back = numpy.array([2, 3, 4])    # Background (not equal to the true state)
sigma_m = 0.15                     # Standard deviation of the measure noise
sigma_b = 0.1                      # Standard deviation of the background noise
H = numpy.eye(3)                   # Observation operator
ODE = Lorenz1963(dt = 0.01)        # Dynamic model
ODE.ObservationStep = 0.2          # Observation interval
#
observations = numpy.loadtxt("simple_3DVAR4Observations.csv")[:, 1:]
#
case = adaoBuilder.New()
case.setAlgorithmParameters(
    Algorithm="3DVAR",
    Parameters={"EstimationOf": "State"},
)
case.setBackground(Vector=u0Back)
case.setBackgroundError(ScalarSparseMatrix=sigma_b**2)
case.setObservationError(ScalarSparseMatrix=sigma_m**2)
case.setEvolutionError(ScalarSparseMatrix=1.0e-8)
case.setObservationOperator(Matrix=H)
#
print("Successive analysis correcting the forecasted state using the observation:")
for i in range(observations.shape[0]):
    case.setEvolutionModel(OneFunction=ODE.StateTransition)
    case.setObservation(Vector=observations[i, :])
    case.execute(nextStep=True)
    #
    Xa = case.get("Analysis")[-1]
    print(
        "  After observation nb %02i : Xa[%02i] = %+9.5f %+9.5f %+9.5f"
        % (i + 1, i + 1, Xa[0], Xa[1], Xa[2])
    )
