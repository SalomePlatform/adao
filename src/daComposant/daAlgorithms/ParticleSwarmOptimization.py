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

import numpy, logging, copy
from daCore import BasicObjects
from daAlgorithms.Atoms import ecwnpso, ecwopso

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "PARTICLESWARMOPTIMIZATION")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "PSO",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "PSO",
                "OGCR",
                ],
            listadv  = [
                "CanonicalPSO",
                "SPSO-2011",
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
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.defineRequiredParameter(
            name     = "NumberOfInsects",
            default  = 100,
            typecast = int,
            message  = "Nombre d'insectes dans l'essaim",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "InertiaWeight",
            default  = 1.,
            typecast = float,
            message  = "Part de la vitesse de l'essaim qui est imposée à l'insecte, ou poids de l'inertie (entre 0 et 1)",
            minval   = 0.,
            maxval   = 1.,
            oldname  = "SwarmVelocity",
            )
        self.defineRequiredParameter(
            name     = "CognitiveAcceleration",
            default  = 0.5,
            typecast = float,
            message  = "Taux de rappel à la meilleure position de l'insecte précédemment connue (entre 0 et 1)",
            minval   = 0.,
            maxval   = 1.,
            )
        self.defineRequiredParameter(
            name     = "SocialAcceleration",
            default  = 0.5,
            typecast = float,
            message  = "Taux de rappel au meilleur insecte du groupe local (entre 0 et 1)",
            minval   = 0.,
            maxval   = 1.,
            oldname  = "GroupRecallRate",
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
                "CurrentIterationNumber",
                "CurrentState",
                "Innovation",
                "OMA",
                "OMB",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
                ]
            )
        self.defineRequiredParameter( # Pas de type
            name     = "BoxBounds",
            message  = "Liste des valeurs de bornes d'incréments de paramètres",
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des paires de bornes",
            )
        self.defineRequiredParameter(
            name     = "InitializationPoint",
            typecast = numpy.ravel,
            message  = "État initial imposé (par défaut, c'est l'ébauche si None)",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            )
        self.setAttributes(tags=(
            "Optimization",
            "NonLinear",
            "MetaHeuristic",
            "Population",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        #--------------------------
        if   self._parameters["Variant"] in ["CanonicalPSO", "PSO"]:
            ecwnpso.ecwnpso(self, Xb, Y, HO, R, B)
        #
        elif self._parameters["Variant"] in ["OGCR"]:
            ecwopso.ecwopso(self, Xb, Y, HO, R, B)
        #
        #--------------------------
        else:
            raise ValueError("Error in Variant name: %s"%self._parameters["Variant"])
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
