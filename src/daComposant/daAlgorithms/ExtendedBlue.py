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

import numpy
from daCore import BasicObjects, NumericObjects
from daAlgorithms.Atoms import ecwexblue

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "EXTENDEDBLUE")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "ExtendedBlue",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "ExtendedBlue",
            ],
            listadv  = [
                "OneCorrection",
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
                "APosterioriCorrelations",
                "APosterioriCovariance",
                "APosterioriStandardDeviations",
                "APosterioriVariances",
                "BMA",
                "CostFunctionJ",
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJb",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJo",
                "CostFunctionJoAtCurrentOptimum",
                "CurrentOptimum",
                "CurrentState",
                "CurrentStepNumber",
                "ForecastState",
                "Innovation",
                "InnovationAtCurrentAnalysis",
                "MahalanobisConsistency",
                "OMA",
                "OMB",
                "SampledStateForQuantiles",
                "SigmaBck2",
                "SigmaObs2",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
                "SimulationQuantiles",
            ]
        )
        self.defineRequiredParameter(
            name     = "Quantiles",
            default  = [],
            typecast = tuple,
            message  = "Liste des valeurs de quantiles",
            minval   = 0.,
            maxval   = 1.,
        )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
        )
        self.defineRequiredParameter(
            name     = "NumberOfSamplesForQuantiles",
            default  = 100,
            typecast = int,
            message  = "Nombre d'échantillons simulés pour le calcul des quantiles",
            minval   = 1,
        )
        self.defineRequiredParameter(
            name     = "SimulationForQuantiles",
            default  = "Linear",
            typecast = str,
            message  = "Type de simulation en estimation des quantiles",
            listval  = ["Linear", "NonLinear"]
        )
        self.defineRequiredParameter(  # Pas de type
            name     = "StateBoundsForQuantiles",
            message  = "Liste des paires de bornes pour les états utilisés en estimation des quantiles",
        )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            optional = ("U", "EM", "CM", "Q"),
        )
        self.setAttributes(
            tags=(
                "DataAssimilation",
                "NonLinear",
                "Filter",
            ),
            features=(
                "LocalOptimization",
                "DerivativeNeeded",
                "ParallelDerivativesOnly",
                "ConvergenceOnStatic",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        # --------------------------
        if self._parameters["Variant"] == "ExtendedBlue":
            NumericObjects.multiXOsteps(self, Xb, Y, U, HO, EM, CM, R, B, Q, ecwexblue.ecwexblue)
        #
        # --------------------------
        elif self._parameters["Variant"] == "OneCorrection":
            ecwexblue.ecwexblue(self, Xb, Y, U, HO, CM, R, B)
        #
        # --------------------------
        else:
            raise ValueError("Error in Variant name: %s"%self._parameters["Variant"])
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
