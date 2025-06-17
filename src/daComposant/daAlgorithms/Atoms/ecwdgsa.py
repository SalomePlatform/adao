# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

__doc__ = """
    (Dual) Generalized Simulated Annealing
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, logging, scipy
from daCore.NumericObjects import CostFunction3D as CostFunction
from daCore.PlatformInfo import vt

# ==============================================================================
def ecwdgsa(selfA, Xb, Xini, Y, U, HO, CM, R, B, __storeState = False):
    """
    Correction
    """
    #
    # Initialisations
    # ---------------
    if vt(scipy.version.version) < vt("1.2.0"):
        __msg = (
            "In order to exploit Simulated Annealing algorithm, you must use"
            + " Scipy version 1.2.0 or above (and you are presently using"
            + " Scipy %s). No optimization is performed.\n" % scipy.version.version
        )
        logging.warning(__msg)
        return 0
    #
    Hm = HO["Direct"].appliedTo
    Xini = Xini.reshape((-1,))
    #
    if not selfA._toStore("CurrentState"):
        selfA._parameters["StoreSupplementaryCalculations"] = tuple(
            list(selfA._parameters["StoreSupplementaryCalculations"]) + ["CurrentState"]
        )
    #
    BI = B.getI()
    RI = R.getI()
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Variant"] in ["GSA", "GeneralizedSimulatedAnnealing"]:
        result = scipy.optimize.dual_annealing(
            func            = CostFunction,
            x0              = Xini,
            bounds          = selfA._parameters["Bounds"],
            args            = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False),
            maxiter         = selfA._parameters["MaximumNumberOfIterations"] - 1,
            maxfun          = selfA._parameters["MaximumNumberOfFunctionEvaluations"],
            no_local_search = True,
        )
        Minimum = numpy.ravel(result["x"])
        # J_optimal = vfloat(result["fun"])
    elif selfA._parameters["Variant"] in ["DA", "DualAnnealing"]:
        result = scipy.optimize.dual_annealing(
            func            = CostFunction,
            x0              = Xini,
            bounds          = selfA._parameters["Bounds"],
            args            = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False),
            maxiter         = selfA._parameters["MaximumNumberOfIterations"] - 1,
            maxfun          = selfA._parameters["MaximumNumberOfFunctionEvaluations"],
            no_local_search = False,
        )
        Minimum = numpy.ravel(result["x"])
        # J_optimal = vfloat(result["fun"])
    else:
        raise ValueError("Error in variant name: %s is unkown"%selfA._parameters["Variant"])
    #
    Xa = Minimum
    if __storeState:
        selfA._setInternalState("Xn", Xa)
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("OMA") or \
            selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps  # noqa: E501
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm(Xa)
        HXa = HXa.reshape((-1, 1))
    if selfA._toStore("Innovation") or \
            selfA._toStore("OMB") or \
            selfA._toStore("SimulatedObservationAtBackground"):
        HXb = Hm(Xb).reshape((-1, 1))
        Innovation = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( Innovation )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( Innovation )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( Y - HXa )
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    if selfA._toStore("EnsembleOfStates"):
        selfA.StoredVariables["EnsembleOfStates"].store( numpy.array(selfA.StoredVariables["CurrentState"][nbPreviousSteps:]).T )
    if selfA._toStore("EnsembleOfSimulations"):
        selfA.StoredVariables["EnsembleOfSimulations"].store( numpy.array(selfA.StoredVariables["SimulatedObservationAtCurrentState"][nbPreviousSteps:]).T )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
