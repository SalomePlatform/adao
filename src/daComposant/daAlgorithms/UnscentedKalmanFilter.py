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

from daCore import BasicObjects
from daAlgorithms.Atoms import ecwukf, ecw2ukf

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):

    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "UNSCENTEDKALMANFILTER")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "2UKF",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "UKF",
                "S3F",
                "CUKF", "2UKF",
                "CS3F", "2S3F",
            ],
            listadv  = [
                "UKF-Std",
                "MSS",
                "CMSS", "2MSS",
                "5OS",
                "C5OS", "25OS",
            ],
        )
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "State",
            typecast = str,
            message  = "Estimation d'état ou de paramètres",
            listval  = ["State", "Parameters"],
        )
        self.defineRequiredParameter(
            name     = "ConstrainedBy",
            default  = "EstimateProjection",
            typecast = str,
            message  = "Prise en compte des contraintes",
            listval  = ["EstimateProjection"],
        )
        self.defineRequiredParameter(
            name     = "Alpha",
            default  = 1.e-2,
            typecast = float,
            message  = "Coefficient Alpha d'échelle",
            minval   = 1.e-4,
            maxval   = 1.,
        )
        self.defineRequiredParameter(
            name     = "Beta",
            default  = 2,
            typecast = float,
            message  = "Coefficient Beta d'information a priori sur la distribution",
        )
        self.defineRequiredParameter(
            name     = "Kappa",
            default  = 0,
            typecast = int,
            message  = "Coefficient Kappa secondaire d'échelle",
            maxval   = 2,
        )
        self.defineRequiredParameter(
            name     = "Reconditioner",
            default  = 1.,
            typecast = float,
            message  = "Coefficient de reconditionnement",
            minval   = 1.e-3,
            maxval   = 1.e+1,
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
                "ForecastCovariance",
                "ForecastState",
                "IndexOfOptimum",
                "InnovationAtCurrentAnalysis",
                "InnovationAtCurrentState",
                "SimulatedObservationAtCurrentAnalysis",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
            ]
        )
        self.defineRequiredParameter(  # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
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
                "Ensemble",
                "Dynamic",
                "Reduction",
            ),
            features=(
                "LocalOptimization",
                "DerivativeFree",
                "ParallelAlgorithm",
                "ConvergenceOnStatic",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        # --------------------------
        if self._parameters["Variant"] in ["UKF", "UKF-Std"]:
            ecwukf.ecwukf(self, Xb, Y, U, HO, EM, CM, R, B, Q, "UKF")
        #
        elif self._parameters["Variant"] == "S3F":
            ecwukf.ecwukf(self, Xb, Y, U, HO, EM, CM, R, B, Q, "S3F")
        #
        elif self._parameters["Variant"] == "MSS":
            ecwukf.ecwukf(self, Xb, Y, U, HO, EM, CM, R, B, Q, "MSS")
        #
        elif self._parameters["Variant"] == "5OS":
            ecwukf.ecwukf(self, Xb, Y, U, HO, EM, CM, R, B, Q, "5OS")
        #
        # --------------------------
        elif self._parameters["Variant"] in ["CUKF", "2UKF"]:
            ecw2ukf.ecw2ukf(self, Xb, Y, U, HO, EM, CM, R, B, Q, "UKF")
        #
        elif self._parameters["Variant"] in ["CS3F", "2S3F"]:
            ecw2ukf.ecw2ukf(self, Xb, Y, U, HO, EM, CM, R, B, Q, "S3F")
        #
        elif self._parameters["Variant"] in ["CMSS", "2MSS"]:
            ecw2ukf.ecw2ukf(self, Xb, Y, U, HO, EM, CM, R, B, Q, "MSS")
        #
        elif self._parameters["Variant"] in ["C5OS", "25OS"]:
            ecw2ukf.ecw2ukf(self, Xb, Y, U, HO, EM, CM, R, B, Q, "5OS")
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
