# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2026 EDF R&D
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
    CMA-ES
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, logging
from daCore.NumericObjects import ForceNumericBounds
from daCore.NumericObjects import CostFunction3D as CostFunction
from daCore import PlatformInfo

lpi = PlatformInfo.PlatformInfo()


# ==============================================================================
def ecwcmaes(selfA, Xb, Xini, Y, U, HO, CM, R, B, __storeState=False):
    """
    Correction
    """
    #
    if not lpi.has_cmaes:
        raise ImportError(
            "%s Minimization by CMA-ES is not available, " % (selfA._name,)
            + 'please install the optional module "cma" .',
        )
    else:
        import cma
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
    Xini = Xini.reshape((-1,))
    #
    if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
        HXb = numpy.asarray(Hm(Xb, HO["AppliedInX"]["HXb"])).reshape((-1, 1))
        if Y.size != HXb.size:
            raise ValueError(
                "The size %i of observations Y and %i of observed calculation "
                + "H(X) are different, they have to be identical." % (Y.size, HXb.size)
            )  # noqa: E501
        if max(Y.shape) != max(HXb.shape):
            raise ValueError(
                "The shapes %s of observations Y and %s of observed calculation "
                + "H(X) are different, they have to be identical."
                % (Y.shape, HXb.shape)
            )  # noqa: E501
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
    verb_conversion = {0: -10, 1: 3}
    addoptions = {
        "maxiter": selfA._parameters["MaximumNumberOfIterations"] - 1,
        "maxfevals": selfA._parameters["MaximumNumberOfFunctionEvaluations"],
        "seed": selfA._parameters["SetSeed"],
        "tolx": selfA._parameters["StateVariationTolerance"],
        "tolfun": selfA._parameters["CostDecrementTolerance"],
        "verbose": verb_conversion[selfA._parameters["optdisp"]],
        "verb_disp": selfA._parameters["optiprint"],
    }
    if selfA._parameters["EvolutionaryPopulationSize"] > 0:
        addoptions.update(
            {
                "popsize": selfA._parameters["EvolutionaryPopulationSize"],
            }
        )
    if selfA._parameters["Bounds"] is not None and len(selfA._parameters["Bounds"]) > 0:
        lower = [float(numpy.ravel(lb)[0]) for lb, ub in selfA._parameters["Bounds"]]
        upper = [float(numpy.ravel(ub)[0]) for lb, ub in selfA._parameters["Bounds"]]
        bounds = [lower, upper]
        # Guess sigma0 per variable as about 1/4th of the search domain width
        widths = ForceNumericBounds(selfA._parameters["Bounds"])
        widths = numpy.ravel(widths[:, 1] - widths[:, 0]) / 4.0
        widths[numpy.isinf(widths)] = 1.0
        addoptions.update(
            {
                "bounds": bounds,
                "CMA_stds": widths,
            }
        )
    #
    xopt, es = cma.fmin2(
        CostFunction,
        Xini,
        sigma0=selfA._parameters["EvolutionaryCovarianceOverallScale"],
        args=(
            selfA,
            Xb,
            Hm,
            Y,
            BI,
            RI,
            nbPreviousSteps,
            selfA._parameters["QualityCriterion"],
            True,
            False,
            False,
        ),
        options=addoptions,
    )
    #
    IndexMin = (
        numpy.argmin(selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:])
        + nbPreviousSteps
    )
    Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = Minimum
    if __storeState:
        selfA._setInternalState("Xn", Xa)
    #
    selfA.StoredVariables["Analysis"].store(Xa)
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("OMA") or selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm(Xa)
        HXa = HXa.reshape((-1, 1))
    if (
        selfA._toStore("Innovation")
        or selfA._toStore("OMB")
        or selfA._toStore("SimulatedObservationAtBackground")
    ):
        HXb = Hm(Xb).reshape((-1, 1))
        Innovation = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store(Innovation)
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store(Innovation)
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store(numpy.ravel(Xb) - numpy.ravel(Xa))
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store(Y - HXa)
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store(HXb)
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store(HXa)
    if selfA._toStore("EnsembleOfStates"):
        selfA.StoredVariables["EnsembleOfStates"].store(
            numpy.array(selfA.StoredVariables["CurrentState"][nbPreviousSteps:]).T
        )
    if selfA._toStore("EnsembleOfSimulations"):
        selfA.StoredVariables["EnsembleOfSimulations"].store(
            numpy.array(
                selfA.StoredVariables["SimulatedObservationAtCurrentState"][
                    nbPreviousSteps:
                ]
            ).T
        )
    #
    return 0


# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
