# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
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
from daCore import BasicObjects
import numpy, scipy.optimize

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "DIFFERENTIALEVOLUTION")
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "BEST1BIN",
            typecast = str,
            message  = "Stratégie de minimisation utilisée",
            listval  = [
                "BEST1BIN",
                "BEST1EXP",
                "RAND1EXP",
                "RANDTOBEST1EXP",
                # "CURRENTTOBEST1EXP",
                "BEST2EXP",
                "RAND2EXP",
                "RANDTOBEST1BIN",
                # "CURRENTTOBEST1BIN",
                "BEST2BIN",
                "RAND2BIN",
                "RAND1BIN",
                ],
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfSteps",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de générations",
            minval   = 0,
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfFunctionEvaluations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal d'évaluations de la fonction",
            minval   = -1,
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
            listval  = ["AugmentedWeightedLeastSquares","AWLS","DA",
                        "WeightedLeastSquares","WLS",
                        "LeastSquares","LS","L2",
                        "AbsoluteValue","L1",
                        "MaximumError","ME"],
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
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJoAtCurrentOptimum",
                "CurrentOptimum",
                "CurrentState",
                "IndexOfOptimum",
                "Innovation",
                "InnovationAtCurrentState",
                "OMA",
                "OMB",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
                ]
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B" ),
            )
        self.setAttributes(tags=(
            "Optimization",
            "NonLinear",
            "MetaHeuristic",
            "Population",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        len_X = numpy.asarray(Xb).size
        popsize = round(self._parameters["PopulationSize"]/len_X)
        maxiter = min(self._parameters["MaximumNumberOfSteps"],round(self._parameters["MaximumNumberOfFunctionEvaluations"]/(popsize*len_X) - 1))
        logging.debug("%s Nombre maximal de générations = %i, taille de la population à chaque génération = %i"%(self._name, maxiter, popsize*len_X))
        #
        # Opérateurs
        # ----------
        Hm = HO["Direct"].appliedTo
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(x, QualityMeasure="AugmentedWeightedLeastSquares"):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            self.StoredVariables["CurrentState"].store( _X )
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            _Innovation = Y - _HX
            if self._toStore("SimulatedObservationAtCurrentState") or \
                self._toStore("SimulatedObservationAtCurrentOptimum"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            if self._toStore("InnovationAtCurrentState"):
                self.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
            #
            if QualityMeasure in ["AugmentedWeightedLeastSquares","AWLS","DA"]:
                if BI is None or RI is None:
                    raise ValueError("Background and Observation error covariance matrix has to be properly defined!")
                Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
                Jo  = 0.5 * (_Innovation).T * RI * (_Innovation)
            elif QualityMeasure in ["WeightedLeastSquares","WLS"]:
                if RI is None:
                    raise ValueError("Observation error covariance matrix has to be properly defined!")
                Jb  = 0.
                Jo  = 0.5 * (_Innovation).T * RI * (_Innovation)
            elif QualityMeasure in ["LeastSquares","LS","L2"]:
                Jb  = 0.
                Jo  = 0.5 * (_Innovation).T * (_Innovation)
            elif QualityMeasure in ["AbsoluteValue","L1"]:
                Jb  = 0.
                Jo  = numpy.sum( numpy.abs(_Innovation) )
            elif QualityMeasure in ["MaximumError","ME"]:
                Jb  = 0.
                Jo  = numpy.max( numpy.abs(_Innovation) )
            #
            J   = float( Jb ) + float( Jo )
            #
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            if self._toStore("IndexOfOptimum") or \
                self._toStore("CurrentOptimum") or \
                self._toStore("CostFunctionJAtCurrentOptimum") or \
                self._toStore("CostFunctionJbAtCurrentOptimum") or \
                self._toStore("CostFunctionJoAtCurrentOptimum") or \
                self._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if self._toStore("IndexOfOptimum"):
                self.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if self._toStore("CurrentOptimum"):
                self.StoredVariables["CurrentOptimum"].store( self.StoredVariables["CurrentState"][IndexMin] )
            if self._toStore("SimulatedObservationAtCurrentOptimum"):
                self.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
            if self._toStore("CostFunctionJAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( self.StoredVariables["CostFunctionJ" ][IndexMin] )
            if self._toStore("CostFunctionJbAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJb"][IndexMin] )
            if self._toStore("CostFunctionJoAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJo"][IndexMin] )
            return J
        #
        # Point de démarrage de l'optimisation : Xini = Xb
        # ------------------------------------
        Xini = numpy.ravel(Xb)
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = self.StoredVariables["CostFunctionJ"].stepnumber()
        #
        optResults = scipy.optimize.differential_evolution(
            CostFunction,
            self._parameters["Bounds"],
            strategy      = str(self._parameters["Minimizer"]).lower(),
            maxiter       = maxiter,
            popsize       = popsize,
            mutation      = self._parameters["MutationDifferentialWeight_F"],
            recombination = self._parameters["CrossOverProbability_CR"],
            disp          = self._parameters["optdisp"],
            )
        #
        IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = self.StoredVariables["CostFunctionJ"][IndexMin]
        Minimum  = self.StoredVariables["CurrentState"][IndexMin]
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.ravel( Minimum )
        #
        self.StoredVariables["Analysis"].store( Xa )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._toStore("OMA") or self._toStore("SimulatedObservationAtOptimum"):
            if self._toStore("SimulatedObservationAtCurrentState"):
                HXa = self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
            elif self._toStore("SimulatedObservationAtCurrentOptimum"):
                HXa = self.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
            else:
                HXa = Hm(Xa)
        if self._toStore("Innovation") or \
           self._toStore("OMB"):
            d  = Y - HXb
        if self._toStore("Innovation"):
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if self._toStore("OMB"):
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
        if self._toStore("SimulatedObservationAtBackground"):
            self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(Hm(Xb)) )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run()
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
