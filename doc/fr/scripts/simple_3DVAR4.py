# -*- coding: utf-8 -*-
#
import numpy
from adao import adaoBuilder
from Models.Lorenz1963 import EDS as Lorenz1963
numpy.set_printoptions(precision=5)
#
u0Back = numpy.array([2, 3, 4])    # Ébauche (différente de l'état vrai)
sigma_m = 0.15                     # Écart-type du bruit de mesure
sigma_b = 0.1                      # Écart-type du bruit d'ébauche
H = numpy.eye(3)                   # Opérateur d'observation
ODE = Lorenz1963(dt = 0.01)        # Modèle dynamique
ODE.ObservationStep = 0.2          # Intervalle d'observation
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
print("Analyses successives corrigeant l'état prévu en utilisant l'observation :")
for i in range(observations.shape[0]):
    case.setEvolutionModel(OneFunction=ODE.StateTransition)
    case.setObservation(Vector=observations[i, :])
    case.execute(nextStep=True)
    #
    Xa = case.get("Analysis")[-1]
    print(
        "  Après l'observation no %02i : Xa[%02i] = %+9.5f %+9.5f %+9.5f"
        % (i + 1, i + 1, Xa[0], Xa[1], Xa[2])
    )
