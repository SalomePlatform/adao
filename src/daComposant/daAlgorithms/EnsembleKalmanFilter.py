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
from daCore import BasicObjects
from daAlgorithms.Atoms import enks, etkf, ienkf, mlef, senkf

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "ENSEMBLEKALMANFILTER")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "EnKF",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "EnKF",
                "ETKF",
                "ETKF-N",
                "MLEF",
                "IEnKF",
                "E3DVAR",
                "EnKS",
            ],
            listadv  = [
                "StochasticEnKF",
                "EnKF-05",
                "EnKF-16",
                "ETKF-KFF",
                "ETKF-VAR",
                "ETKF-N-11",
                "ETKF-N-15",
                "ETKF-N-16",
                "MLEF-T",
                "MLEF-B",
                "IEnKF-T",
                "IEnKF-B",
                "EnKS-KFF",
                "IEKF",
                "E3DVAR-EnKF",
                "E3DVAR-ETKF",
                "E3DVAR-MLEF",
            ],
        )
        self.defineRequiredParameter(
            name     = "NumberOfMembers",
            default  = 100,
            typecast = int,
            message  = "Nombre de membres dans l'ensemble",
            minval   = 2,
        )
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "State",
            typecast = str,
            message  = "Estimation d'état ou de paramètres",
            listval  = ["State", "Parameters"],
        )
        self.defineRequiredParameter(
            name     = "InflationType",
            default  = "MultiplicativeOnAnalysisAnomalies",
            typecast = str,
            message  = "Méthode d'inflation d'ensemble",
            listval  = [
                "MultiplicativeOnAnalysisAnomalies",
                "MultiplicativeOnBackgroundAnomalies",
            ],
            listadv  = [
                "MultiplicativeOnAnalysisCovariance",
                "MultiplicativeOnBackgroundCovariance",
                "AdditiveOnAnalysisCovariance",
                "AdditiveOnBackgroundCovariance",
                "HybridOnBackgroundCovariance",
                "Relaxation",
            ],
        )
        self.defineRequiredParameter(
            name     = "InflationFactor",
            default  = 1.,
            typecast = float,
            message  = "Facteur d'inflation",
            minval   = 0.,
        )
        self.defineRequiredParameter(
            name     = "SmootherLagL",
            default  = 0,
            typecast = int,
            message  = "Nombre d'intervalles de temps de lissage dans le passé",
            minval   = 0,
        )
        self.defineRequiredParameter(
            name     = "HybridCovarianceEquilibrium",
            default  = 0.5,
            typecast = float,
            message  = "Facteur d'équilibre entre la covariance statique et la covariance d'ensemble en hybride variationnel",  # noqa: E501
            minval   = 0.,
            maxval   = 1.,
        )
        self.defineRequiredParameter(
            name     = "HybridMaximumNumberOfIterations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation en hybride variationnel",
            minval   = -1,
        )
        self.defineRequiredParameter(
            name     = "HybridCostDecrementTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Diminution relative minimale du coût lors de l'arrêt en hybride variationnel",
            minval   = 0.,
        )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
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
                "CurrentIterationNumber",
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
            ],
            listadv  = [
                "CurrentEnsembleState",
            ],
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
        # Default EnKF = EnKF-16 = StochasticEnKF
        if self._parameters["Variant"] == "EnKF-05":
            senkf.senkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="KalmanFilterFormula05")
        #
        elif self._parameters["Variant"] in ["EnKF-16", "StochasticEnKF", "EnKF"]:
            senkf.senkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="KalmanFilterFormula16")
        #
        # --------------------------
        # Default ETKF = ETKF-KFF
        elif self._parameters["Variant"] in ["ETKF-KFF", "ETKF"]:
            etkf.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="KalmanFilterFormula")
        #
        elif self._parameters["Variant"] == "ETKF-VAR":
            etkf.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="Variational")
        #
        # --------------------------
        # Default ETKF-N = ETKF-N-16
        elif self._parameters["Variant"] == "ETKF-N-11":
            etkf.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="FiniteSize11")
        #
        elif self._parameters["Variant"] == "ETKF-N-15":
            etkf.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="FiniteSize15")
        #
        elif self._parameters["Variant"] in ["ETKF-N-16", "ETKF-N"]:
            etkf.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="FiniteSize16")
        #
        # --------------------------
        # Default MLEF = MLEF-T
        elif self._parameters["Variant"] in ["MLEF-T", "MLEF"]:
            mlef.mlef(self, Xb, Y, U, HO, EM, CM, R, B, Q, BnotT=False)
        #
        elif self._parameters["Variant"] == "MLEF-B":
            mlef.mlef(self, Xb, Y, U, HO, EM, CM, R, B, Q, BnotT=True)
        #
        # --------------------------
        # Default IEnKF = IEnKF-T
        elif self._parameters["Variant"] in ["IEnKF-T", "IEnKF"]:
            ienkf.ienkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, BnotT=False)
        #
        elif self._parameters["Variant"] in ["IEnKF-B", "IEKF"]:
            ienkf.ienkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, BnotT=True)
        #
        # --------------------------
        # Default EnKS = EnKS-KFF
        elif self._parameters["Variant"] in ["EnKS-KFF", "EnKS"]:
            enks.enks(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="EnKS16-KalmanFilterFormula")
        #
        # --------------------------
        # Default E3DVAR = E3DVAR-ETKF
        elif self._parameters["Variant"] == "E3DVAR-EnKF":
            senkf.senkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, Hybrid="E3DVAR")
        #
        elif self._parameters["Variant"] in ["E3DVAR-ETKF", "E3DVAR"]:
            etkf.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, Hybrid="E3DVAR")
        #
        elif self._parameters["Variant"] == "E3DVAR-MLEF":
            mlef.mlef(self, Xb, Y, U, HO, EM, CM, R, B, Q, Hybrid="E3DVAR")
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
