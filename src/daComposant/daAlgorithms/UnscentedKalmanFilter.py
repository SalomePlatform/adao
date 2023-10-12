# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2023 EDF R&D
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
from daAlgorithms.Atoms import c2ukf, uskf

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
                "2UKF",
                ],
            )
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "State",
            typecast = str,
            message  = "Estimation d'etat ou de parametres",
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
            default  = 1.,
            typecast = float,
            message  = "",
            minval   = 1.e-4,
            maxval   = 1.,
            )
        self.defineRequiredParameter(
            name     = "Beta",
            default  = 2,
            typecast = float,
            message  = "",
            )
        self.defineRequiredParameter(
            name     = "Kappa",
            default  = 0,
            typecast = int,
            message  = "",
            maxval   = 2,
            )
        self.defineRequiredParameter(
            name     = "Reconditioner",
            default  = 1.,
            typecast = float,
            message  = "",
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
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
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
            "Reduction",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        #--------------------------
        # Default UKF
        #--------------------------
        if   self._parameters["Variant"] == "UKF":
            uskf.uskf(self, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        #--------------------------
        # Default 2UKF
        elif self._parameters["Variant"] == "2UKF":
            c2ukf.c2ukf(self, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        #--------------------------
        else:
            raise ValueError("Error in Variant name: %s"%self._parameters["Variant"])
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
