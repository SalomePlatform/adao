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
from daAlgorithms.Atoms import std4dvar

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):

    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "4DVAR")
        self.defineRequiredParameter(
            name     = "ConstrainedBy",
            default  = "EstimateProjection",
            typecast = str,
            message  = "Prise en compte des contraintes",
            listval  = ["EstimateProjection"],
        )
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "4DVAR",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "4DVAR",
            ],
            listadv  = [
                "4DVAR-Std",
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
            name     = "Minimizer",
            default  = "LBFGSB",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = [
                "LBFGSB",
                "TNC",
                "CG",
                "BFGS",
            ],
            listadv  = [
                "NCG",
            ],
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
            name     = "CostDecrementTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Diminution relative minimale du coût lors de l'arrêt",
            minval   = 0.,
        )
        self.defineRequiredParameter(
            name     = "ProjectedGradientTolerance",
            default  = -1,
            typecast = float,
            message  = "Maximum des composantes du gradient projeté lors de l'arrêt",
            minval   = -1,
        )
        self.defineRequiredParameter(
            name     = "GradientNormTolerance",
            default  = 1.e-05,
            typecast = float,
            message  = "Maximum des composantes du gradient lors de l'arrêt",
            minval   = 0.,
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
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJb",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJo",
                "CostFunctionJoAtCurrentOptimum",
                "CurrentIterationNumber",
                "CurrentOptimum",
                "CurrentState",
                "IndexOfOptimum",
            ]
        )
        self.defineRequiredParameter(  # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
        )
        self.defineRequiredParameter(
            name     = "InitializationPoint",
            typecast = numpy.ravel,
            message  = "État initial imposé (par défaut, c'est l'ébauche si None)",
        )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "EM", "R", "B"),
            optional = ("U", "CM", "Q"),
        )
        self.setAttributes(
            tags=(
                "DataAssimilation",
                "NonLinear",
                "Variational",
                "Dynamic",
            ),
            features=(
                "NonLocalOptimization",
                "DerivativeNeeded",
                "ParallelDerivativesOnly",
                "ConvergenceOnBoth",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        # --------------------------
        if self._parameters["Variant"] in ["4DVAR", "4DVAR-Std"]:
            std4dvar.std4dvar(self, Xb, Y, U, HO, EM, CM, R, B, Q)
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
