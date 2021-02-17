# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2021 EDF R&D
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

import logging
from daCore import BasicObjects, NumericObjects
import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "ENSEMBLEKALMANFILTER")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "EnKF",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = [
                "EnKF",
                "ETKF",
                "ETKF-N",
                "MLEF",
                "IEnKF",
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
                "IEKF",
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
            message  = "Estimation d'etat ou de parametres",
            listval  = ["State", "Parameters"],
            )
        self.defineRequiredParameter(
            name     = "InflationType",
            default  = "MultiplicativeOnAnalysisCovariance",
            typecast = str,
            message  = "Méthode d'inflation d'ensemble",
            listval  = [
                "MultiplicativeOnAnalysisCovariance",
                "MultiplicativeOnBackgroundCovariance",
                "MultiplicativeOnAnalysisAnomalies",
                "MultiplicativeOnBackgroundAnomalies",
                "AdditiveOnAnalysisCovariance",
                "AdditiveOnBackgroundCovariance",
                "HybridOnBackgroundCovariance",
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
            name     = "LocalizationType",
            default  = "SchurLocalization",
            typecast = str,
            message  = "Méthode d'inflation d'ensemble",
            listval  = [
                "SchurLocalization",
                ],
            listadv  = [
                "CovarianceLocalization",
                "DomainLocalization",
                "GaspariCohnLocalization",
                ],
            )
        self.defineRequiredParameter(
            name     = "LocalizationFactor",
            default  = 1.,
            typecast = float,
            message  = "Facteur de localisation",
            minval   = 0.,
            )
        self.defineRequiredParameter( # Pas de type
            name     = "LocalizationMatrix",
            message  = "Matrice de localisation ou de distances",
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
                "ForecastState",
                "IndexOfOptimum",
                "InnovationAtCurrentAnalysis",
                "InnovationAtCurrentState",
                "SimulatedObservationAtCurrentAnalysis",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
                ]
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            optional = ("U", "EM", "CM", "Q"),
            )
        self.setAttributes(tags=(
            "DataAssimilation",
            "NonLinear",
            "Filter",
            "Ensemble",
            "Dynamic",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        #--------------------------
        # Default EnKF = EnKF-16 = StochasticEnKF
        if   self._parameters["Variant"] in ["EnKF-05"]:
            NumericObjects.senkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="KalmanFilterFormula05")
        #
        elif self._parameters["Variant"] in ["EnKF-16", "StochasticEnKF", "EnKF"]:
            NumericObjects.senkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="KalmanFilterFormula16")
        #
        #--------------------------
        # Default ETKF = ETKF-KFF
        elif self._parameters["Variant"] in ["ETKF-KFF", "ETKF"]:
            NumericObjects.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="KalmanFilterFormula")
        #
        elif self._parameters["Variant"] == "ETKF-VAR":
            NumericObjects.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="Variational")
        #
        #--------------------------
        # Default ETKF-N = ETKF-N-16
        elif self._parameters["Variant"] == "ETKF-N-11":
            NumericObjects.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="FiniteSize11")
        #
        elif self._parameters["Variant"] == "ETKF-N-15":
            NumericObjects.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="FiniteSize15")
        #
        elif self._parameters["Variant"] in ["ETKF-N-16", "ETKF-N"]:
            NumericObjects.etkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="FiniteSize16")
        #
        #--------------------------
        # Default MLEF = MLEF-T
        elif self._parameters["Variant"] in ["MLEF-T", "MLEF"]:
            NumericObjects.mlef(self, Xb, Y, U, HO, EM, CM, R, B, Q, BnotT=False)
        #
        elif self._parameters["Variant"] == "MLEF-B":
            NumericObjects.mlef(self, Xb, Y, U, HO, EM, CM, R, B, Q, BnotT=True)
        #
        #--------------------------
        # Default IEnKF = IEnKF-T
        elif self._parameters["Variant"] in ["IEnKF-T", "IEnKF"]:
            NumericObjects.ienkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, BnotT=False)
        #
        elif self._parameters["Variant"] in ["IEnKF-B", "IEKF"]:
            NumericObjects.ienkf(self, Xb, Y, U, HO, EM, CM, R, B, Q, BnotT=True)
        #
        #--------------------------
        else:
            raise ValueError("Error in Variant name: %s"%self._parameters["Minimizer"])
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
