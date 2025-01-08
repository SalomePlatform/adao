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
from daAlgorithms.Atoms import ecwlls

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "LINEARLEASTSQUARES")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "LinearLeastSquares",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "LinearLeastSquares",
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
                "InnovationAtCurrentAnalysis",
                "OMA",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
            ]
        )
        self.requireInputArguments(
            mandatory= ("Y", "HO"),
            optional = ("R"),
        )
        self.setAttributes(
            tags=(
                "Optimization",
                "Linear",
                "Variational",
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
        if self._parameters["Variant"] == "LinearLeastSquares":
            NumericObjects.multiXOsteps(self, Xb, Y, U, HO, EM, CM, R, B, Q, ecwlls.ecwlls)
        #
        # --------------------------
        elif self._parameters["Variant"] == "OneCorrection":
            ecwlls.ecwlls(self, Xb, Y, U, HO, CM, R, B)
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
