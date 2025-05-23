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

import numpy, logging, scipy.optimize
from daCore import BasicObjects
from daCore.NumericObjects import CostFunction3D as CostFunction
from daCore.PlatformInfo import vfloat

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "DIFFERENTIALEVOLUTION")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "DifferentialEvolution",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "DifferentialEvolution",
            ],
        )
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "BEST1BIN",
            typecast = str,
            message  = "Stratégie de minimisation utilisée",
            listval  = [
                "BEST1BIN",
                "BEST1EXP",
                "BEST2BIN",
                "BEST2EXP",
                "RAND1BIN",
                "RAND1EXP",
                "RAND2BIN",
                "RAND2EXP",
                "RANDTOBEST1BIN",
                "RANDTOBEST1EXP",
            ],
            listadv  = [
                "CURRENTTOBEST1EXP",
                "CURRENTTOBEST1BIN",
            ],
        )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfIterations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de générations",
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
            name     = "PopulationSize",
            default  = 100,
            typecast = int,
            message  = "Taille approximative de la population à chaque génération",
            minval   = 1,
        )
        self.defineRequiredParameter(
            name     = "MutationDifferentialWeight_F",
            default  = (0.5, 1),
            typecast = tuple,
            message  = "Poids différentiel de mutation, constant ou aléatoire dans l'intervalle, noté F",
            minval   = 0.,
            maxval   = 2.,
        )
        self.defineRequiredParameter(
            name     = "CrossOverProbability_CR",
            default  = 0.7,
            typecast = float,
            message  = "Probabilité de recombinaison ou de croisement, notée CR",
            minval   = 0.,
            maxval   = 1.,
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
            default  = ["CurrentState",],
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
                "Population",
            ),
            features=(
                "NonLocalOptimization",
                "DerivativeFree",
                "ConvergenceOnNumbers",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        len_X = numpy.asarray(Xb).size
        popsize = round(self._parameters["PopulationSize"] / len_X)
        maxiter = min(self._parameters["MaximumNumberOfIterations"], round(self._parameters["MaximumNumberOfFunctionEvaluations"] / (popsize * len_X) - 1))  # noqa: E501
        logging.debug("%s Nombre maximal de générations = %i, taille de la population à chaque génération = %i"%(self._name, maxiter, popsize * len_X))  # noqa: E501
        #
        Hm = HO["Direct"].appliedTo
        #
        BI = B.getI()
        RI = R.getI()
        #
        Xini = numpy.ravel(Xb)
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = self.StoredVariables["CostFunctionJ"].stepnumber()
        #
        scipy.optimize.differential_evolution(
            CostFunction,
            self._parameters["Bounds"],
            args          = (self, Xb, Hm, Y, BI, RI, nbPreviousSteps, "DA", True),
            strategy      = str(self._parameters["Minimizer"]).lower(),
            maxiter       = maxiter,
            popsize       = popsize,
            mutation      = self._parameters["MutationDifferentialWeight_F"],
            recombination = self._parameters["CrossOverProbability_CR"],
            disp          = self._parameters["optdisp"],
            x0            = Xini,
        )
        #
        IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        Minimum  = self.StoredVariables["CurrentState"][IndexMin]
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = Minimum
        #
        self.StoredVariables["Analysis"].store( Xa )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._toStore("EnsembleOfStates"):
            self.StoredVariables["EnsembleOfStates"].store( numpy.asarray(self.StoredVariables["CurrentState"][nbPreviousSteps:]).T )
        if self._toStore("EnsembleOfSimulations"):
            self.StoredVariables["EnsembleOfSimulations"].store( numpy.asarray(self.StoredVariables["SimulatedObservationAtCurrentState"][nbPreviousSteps:]).T )
        if self._toStore("OMA") or \
                self._toStore("SimulatedObservationAtOptimum"):
            if self._toStore("SimulatedObservationAtCurrentState"):
                HXa = self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
            elif self._toStore("SimulatedObservationAtCurrentOptimum"):
                HXa = self.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
            else:
                HXa = Hm(Xa)
            HXa = HXa.reshape((-1, 1))
        if self._toStore("Innovation") or \
                self._toStore("OMB") or \
                self._toStore("SimulatedObservationAtBackground"):
            HXb = Hm(Xb).reshape((-1, 1))
            Innovation = Y - HXb
        if self._toStore("Innovation"):
            self.StoredVariables["Innovation"].store( Innovation )
        if self._toStore("OMB"):
            self.StoredVariables["OMB"].store( Innovation )
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( Y - HXa )
        if self._toStore("SimulatedObservationAtBackground"):
            self.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
