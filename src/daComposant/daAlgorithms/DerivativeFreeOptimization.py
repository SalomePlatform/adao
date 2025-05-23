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

from daCore import BasicObjects, NumericObjects
from daAlgorithms.Atoms import ecwdfo

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "DERIVATIVEFREEOPTIMIZATION")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "DFO",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "DerivativeFreeOptimization",
            ],
            listadv  = [
                "OneCorrection",
                "DFO",
            ],
        )
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "BOBYQA",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = [
                "BOBYQA",
                "COBYLA",
                "NEWUOA",
                "POWELL",
                "SIMPLEX",
                "SUBPLEX",
            ],
        )
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "Parameters",
            typecast = str,
            message  = "Estimation d'état ou de paramètres",
            listval  = ["State", "Parameters"],
        )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfIterations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = -1,
            oldname  = "MaximumNumberOfSteps",
        )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfFunctionEvaluations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal d'évaluations de la fonction",
            minval   = -1,
        )
        self.defineRequiredParameter(
            name     = "StateVariationTolerance",
            default  = 1.e-4,
            typecast = float,
            message  = "Variation relative maximale de l'état lors de l'arrêt",
        )
        self.defineRequiredParameter(
            name     = "CostDecrementTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Diminution relative minimale du cout lors de l'arrêt",
        )
        self.defineRequiredParameter(
            name     = "QualityCriterion",
            default  = "AugmentedWeightedLeastSquares",
            typecast = str,
            message  = "Critère de qualité utilisé",
            listval  = [
                "AugmentedWeightedLeastSquares",
                "WeightedLeastSquares",
                "LeastSquares",
                "AbsoluteValue",
                "MaximumError",
            ],
            listadv  = [
                "AWLS", "DA", "WLS", "L2", "LS", "L1", "ME", "Linf",
            ],
        )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
        )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "Analysis",
                "BMA",
                "CostFunctionJ",
                "CostFunctionJb",
                "CostFunctionJo",
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJoAtCurrentOptimum",
                "CurrentIterationNumber",
                "CurrentOptimum",
                "CurrentState",
                "EnsembleOfSimulations",
                "EnsembleOfStates",
                "IndexOfOptimum",
                "Innovation",
                "InnovationAtCurrentState",
                "OMA",
                "OMB",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
            ],
        )
        self.defineRequiredParameter(  # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
        )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
        )
        self.setAttributes(
            tags=(
                "Optimization",
                "NonLinear",
                "MetaHeuristic",
            ),
            features=(
                "NonLocalOptimization",
                "DerivativeFree",
                "ParallelFree",
                "ConvergenceOnBoth",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        # --------------------------
        if self._parameters["Variant"] in ["DFO", "DerivativeFreeOptimization"]:
            NumericObjects.multiXOsteps(
                self, Xb, Y, U, HO, EM, CM, R, B, Q, ecwdfo.ecwdfo
            )
        #
        # --------------------------
        elif self._parameters["Variant"] == "OneCorrection":
            Xini = self._parameters["InitializationPoint"]
            ecwdfo.ecwdfo(self, Xb, Xini, Y, U, HO, CM, R, B)
        #
        # --------------------------
        else:
            raise ValueError("Error in Variant name: %s" % self._parameters["Variant"])
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
