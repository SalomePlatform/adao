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
from daAlgorithms.Atoms import ecwnpso, ecwopso, ecwapso, ecwspso, ecwpspso

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "PARTICLESWARMOPTIMIZATION")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "CanonicalPSO",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "CanonicalPSO",
                "OGCR",
                "SPSO-2011",
                "SPSO-2011-AIS",
                "SPSO-2011-SIS",
                "SPSO-2011-PSIS",
                "CanonicalPSO-VLS",
                "OGCR-VLS",
                "SPSO-2011-AIS-VLS",
                "SPSO-2011-SIS-VLS",
                "SPSO-2011-PSIS-VLS",
            ],
            listadv  = [
                "PSO",
                "PSO-VLS",
                "SPSO-2011-VLS",
                "VLS",
            ],
        )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfIterations",
            default  = 50,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = 0,
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
            name     = "GlobalCostReductionTolerance",
            default  = 1.e-16,
            typecast = float,
            message  = "Réduction du coût sur l'ensemble de la recherche lors de l'arrêt",
            minval   = 0.,
        )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
        )
        self.defineRequiredParameter(
            name     = "NumberOfInsects",
            default  = 40,
            typecast = int,
            message  = "Nombre d'insectes dans l'essaim",
            minval   = -1,
        )
        self.defineRequiredParameter(
            name     = "SwarmInitialization",
            default  = "UniformByComponents",
            typecast = str,
            message  = "Mode d'initialisation de l'essaim",
            listval  = [
                "UniformByComponents",
                "LogUniformByComponents",
                "LogarithmicByComponents",
                "DistributionByComponents",
            ],
        )
        self.defineRequiredParameter(
            name     = "DistributionByComponents",
            default  = [],
            typecast = tuple,
            message  = "Lois aléatoires d'initialisation par composante",
        )
        self.defineRequiredParameter(
            name     = "SwarmTopology",
            default  = "FullyConnectedNeighborhood",
            typecast = str,
            message  = "Mode de définition du voisinage de chaque particule",
            listval  = [
                "FullyConnectedNeighborhood", "FullyConnectedNeighbourhood", "gbest",
                "RingNeighborhoodWithRadius1", "RingNeighbourhoodWithRadius1", "lbest",
                "RingNeighborhoodWithRadius2", "RingNeighbourhoodWithRadius2",
                "AdaptativeRandomWith3Neighbors", "AdaptativeRandomWith3Neighbours", "abest",
                "AdaptativeRandomWith5Neighbors", "AdaptativeRandomWith5Neighbours",
            ],
            listadv  = [
                "VonNeumannNeighborhood", "VonNeumannNeighbourhood",
            ],
        )
        self.defineRequiredParameter(
            name     = "InertiaWeight",
            default  = 0.72135,  # 1/(2*ln(2))
            typecast = float,
            message  = "Part de la vitesse de l'essaim qui est imposée à l'insecte, ou poids de l'inertie (entre 0 et 1)",  # noqa: E501
            minval   = 0.,
            maxval   = 1.,
            oldname  = "SwarmVelocity",
        )
        self.defineRequiredParameter(
            name     = "CognitiveAcceleration",
            default  = 1.19315,  # 1/2+ln(2)
            typecast = float,
            message  = "Taux de rappel à la meilleure position de l'insecte précédemment connue (positif)",
            minval   = 0.,
        )
        self.defineRequiredParameter(
            name     = "CognitiveAccelerationControl",
            default  = 0.,
            typecast = float,
            message  = "Ralentissement du rappel à la meilleure position (positif)",
            minval   = 0.,
        )
        self.defineRequiredParameter(
            name     = "SocialAcceleration",
            default  = 1.19315,  # 1/2+ln(2)
            typecast = float,
            message  = "Taux de rappel au meilleur insecte du groupe local (positif)",
            minval   = 0.,
            oldname  = "GroupRecallRate",
        )
        self.defineRequiredParameter(
            name     = "SocialAccelerationControl",
            default  = 0.,
            typecast = float,
            message  = "Accroissement au rappel au meilleur insecte du groupe local (positif)",
            minval   = 0.,
        )
        self.defineRequiredParameter(
            name     = "VelocityClampingFactor",
            default  = 0.3,
            typecast = float,
            message  = "Facteur de réduction de l'amplitude de variation des vitesses (entre 0 et 1)",
            minval   = 0.0001,
            maxval   = 1.,
        )
        self.defineRequiredParameter(
            name     = "QualityCriterion",
            default  = "AugmentedWeightedLeastSquares",
            typecast = str,
            message  = "Critère de qualité utilisé",
            listval  = [
                "AugmentedWeightedLeastSquares", "AWLS", "DA",
                "WeightedLeastSquares", "WLS",
                "LeastSquares", "LS", "L2",
                "AbsoluteValue", "L1",
                "MaximumError", "ME", "Linf",
            ],
        )
        self.defineRequiredParameter(
            name     = "HybridNumberOfWarmupIterations",
            default  = 0,
            typecast = int,
            message  = "Nombre d'itérations initiales non accélérées avant l'accélération en optimisation hybride",
            minval   = -1,
        )
        self.defineRequiredParameter(
            name     = "HybridNumberOfLocalHunters",
            default  = 1,
            typecast = int,
            message  = "Nombre maximal d'insectes accélérés en optimisation hybride",
            minval   = -1,
        )
        self.defineRequiredParameter(
            name     = "HybridMaximumNumberOfIterations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation en optimisation hybride",
            minval   = -1,
        )
        self.defineRequiredParameter(
            name     = "HybridCostDecrementTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Diminution relative minimale du coût lors de l'arrêt en optimisation hybride",
            minval   = 0.,
        )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
        )
        self.defineRequiredParameter(
            name     = "StoreInitialState",
            default  = False,
            typecast = bool,
            message  = "Stockage du premier état à la manière des algorithmes récursifs",
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
                "CostFunctionJb",
                "CostFunctionJo",
                "CurrentIterationNumber",
                "CurrentState",
                "EnsembleOfStates",
                "EnsembleOfSimulations",
                "Innovation",
                "InternalCostFunctionJ",
                "InternalCostFunctionJb",
                "InternalCostFunctionJo",
                "OMA",
                "OMB",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
            ],
            listadv  = [
                "InternalAPosterioriCovariance",
            ],
        )
        self.defineRequiredParameter(  # Pas de type
            name     = "Bounds",
            message  = "Liste des paires de bornes",
        )
        self.defineRequiredParameter(  # Pas de type
            name     = "BoxBounds",
            message  = "Liste des paires de bornes d'incréments",
        )
        self.defineRequiredParameter(
            name     = "InitializationPoint",
            typecast = numpy.ravel,
            message  = "État initial imposé (par défaut, c'est l'ébauche si None)",
        )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
        )
        self.setAttributes(
            tags=(
                "Optimization",
                "NonLinear",
                "MetaHeuristic",
                "Population",
            ),
            features=(
                "NonLocalOptimization",
                "DerivativeFree",
                "ParallelAlgorithm",
                "ConvergenceOnNumbers",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        # --------------------------
        # CanonicalPSO = PSO
        if self._parameters["Variant"] in ["CanonicalPSO", "PSO"]:
            ecwnpso.ecwnpso(self, Xb, Y, HO, R, B)
        #
        elif self._parameters["Variant"] in ["OGCR"]:
            ecwopso.ecwopso(self, Xb, Y, HO, R, B)
        #
        # SPSO-2011 = SPSO-2011-AIS
        elif self._parameters["Variant"] in ["SPSO-2011", "SPSO-2011-AIS"]:
            ecwapso.ecwapso(self, Xb, Y, HO, R, B)
        #
        elif self._parameters["Variant"] in ["SPSO-2011-SIS"]:
            ecwspso.ecwspso(self, Xb, Y, HO, R, B)
        #
        elif self._parameters["Variant"] in ["SPSO-2011-PSIS"]:
            ecwpspso.ecwpspso(self, Xb, Y, HO, R, B)
        #
        # --------------------------
        # CanonicalPSO-VLS = PSO-VLS = VLS
        elif self._parameters["Variant"] in ["CanonicalPSO-VLS", "PSO-VLS", "VLS"]:
            ecwnpso.ecwnpso(self, Xb, Y, HO, R, B, Hybrid="VarLocalSearch")
        #
        elif self._parameters["Variant"] in ["OGCR-VLS"]:
            ecwopso.ecwopso(self, Xb, Y, HO, R, B, Hybrid="VarLocalSearch")
        #
        # SPSO-2011-VLS = SPSO-2011-AIS-VLS
        elif self._parameters["Variant"] in ["SPSO-2011-VLS", "SPSO-2011-AIS-VLS"]:
            ecwapso.ecwapso(self, Xb, Y, HO, R, B, Hybrid="VarLocalSearch")
        #
        elif self._parameters["Variant"] in ["SPSO-2011-SIS-VLS"]:
            ecwspso.ecwspso(self, Xb, Y, HO, R, B, Hybrid="VarLocalSearch")
        #
        elif self._parameters["Variant"] in ["SPSO-2011-PSIS-VLS"]:
            ecwpspso.ecwpspso(self, Xb, Y, HO, R, B, Hybrid="VarLocalSearch")
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
