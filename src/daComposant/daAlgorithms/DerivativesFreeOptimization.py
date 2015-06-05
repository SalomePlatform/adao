#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2015 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
from daCore import BasicObjects
import numpy, scipy.optimize

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "DERIVATIVESFREEOPTIMIZATION")
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
            message  = "Nombre maximal de d'évaluations de la function",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "StateVariationTolerance",
            default  = 1.e-4,
            typecast = float,
            message  = "Variation relative minimale de l'état lors de l'arrêt",
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
            listval  = ["CurrentState", "CostFunctionJ", "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"]
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
#         self.setParameterValue("StoreInternalVariables",True)
#         print self._parameters["StoreInternalVariables"]
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
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            #
            if QualityMeasure in ["AugmentedWeightedLeastSquares","AWLS","DA"]:
                if BI is None or RI is None:
                    raise ValueError("Background and Observation error covariance matrix has to be properly defined!")
                Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
                Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
            elif QualityMeasure in ["WeightedLeastSquares","WLS"]:
                if RI is None:
                    raise ValueError("Observation error covariance matrix has to be properly defined!")
                Jb  = 0.
                Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
            elif QualityMeasure in ["LeastSquares","LS","L2"]:
                Jb  = 0.
                Jo  = 0.5 * (Y - _HX).T * (Y - _HX)
            elif QualityMeasure in ["AbsoluteValue","L1"]:
                Jb  = 0.
                Jo  = numpy.sum( numpy.abs(Y - _HX) )
            elif QualityMeasure in ["MaximumError","ME"]:
                Jb  = 0.
                Jo  = numpy.max( numpy.abs(Y - _HX) )
            #
            J   = float( Jb ) + float( Jo )
            #
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
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
        if "SimulatedObservationAtBackground" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(Hm(Xb)) )
        if "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(Hm(Xa)) )
        #
        self._post_run()
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
