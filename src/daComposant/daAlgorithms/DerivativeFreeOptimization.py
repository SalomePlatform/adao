#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2016 EDF R&D
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
        BasicObjects.Algorithm.__init__(self, "DERIVATIVEFREEOPTIMIZATION")
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "POWELL",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = ["POWELL", "SIMPLEX"],
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfSteps",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfFunctionEvaluations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de d'évaluations de la fonction",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "StateVariationTolerance",
            default  = 1.e-4,
            typecast = float,
            message  = "Variation relative maximale de l'état lors de l'arrêt",
            )
        self.defineRequiredParameter(
            name     = "CostDecrementTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Diminution relative minimale du cout lors de l'arrêt",
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
            listval  = ["CurrentState", "CostFunctionJ", "CostFunctionJb", "CostFunctionJo", "CostFunctionJAtCurrentOptimum", "CurrentOptimum", "IndexOfOptimum", "InnovationAtCurrentState", "BMA", "OMA", "OMB", "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentOptimum", "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"]
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        if logging.getLogger().level < logging.WARNING:
            self.__disp = 1
        else:
            self.__disp = 0
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
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
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"] or \
               "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            if "InnovationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
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
            if "IndexOfOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "CurrentOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "CostFunctionJAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if "IndexOfOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if "CurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentOptimum"].store( self.StoredVariables["CurrentState"][IndexMin] )
            if "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
            if "CostFunctionJAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJb"][IndexMin] )
                self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJo"][IndexMin] )
                self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( self.StoredVariables["CostFunctionJ" ][IndexMin] )
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
        if self._parameters["Minimizer"] == "POWELL":
            Minimum, J_optimal, direc, niter, nfeval, rc = scipy.optimize.fmin_powell(
                func        = CostFunction,
                x0          = Xini,
                args        = (self._parameters["QualityCriterion"],),
                maxiter     = self._parameters["MaximumNumberOfSteps"]-1,
                maxfun      = self._parameters["MaximumNumberOfFunctionEvaluations"]-1,
                xtol        = self._parameters["StateVariationTolerance"],
                ftol        = self._parameters["CostDecrementTolerance"],
                full_output = True,
                disp        = self.__disp,
                )
        elif self._parameters["Minimizer"] == "SIMPLEX":
            Minimum, J_optimal, niter, nfeval, rc = scipy.optimize.fmin(
                func        = CostFunction,
                x0          = Xini,
                args        = (self._parameters["QualityCriterion"],),
                maxiter     = self._parameters["MaximumNumberOfSteps"]-1,
                maxfun      = self._parameters["MaximumNumberOfFunctionEvaluations"]-1,
                xtol        = self._parameters["StateVariationTolerance"],
                ftol        = self._parameters["CostDecrementTolerance"],
                full_output = True,
                disp        = self.__disp,
                )
        else:
            raise ValueError("Error in Minimizer name: %s"%self._parameters["Minimizer"])
        #
        IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = self.StoredVariables["CostFunctionJ"][IndexMin]
        Minimum  = self.StoredVariables["CurrentState"][IndexMin]
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(numpy.ravel( Minimum )).T
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        if "OMA"                           in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                HXa = self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
            elif "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                HXa = self.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
            else:
                HXa = Hm(Xa)
        #
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
        if "SimulatedObservationAtBackground" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(Hm(Xb)) )
        if "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run()
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
