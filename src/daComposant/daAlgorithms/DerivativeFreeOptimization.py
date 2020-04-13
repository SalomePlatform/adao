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
from daCore import BasicObjects, PlatformInfo
import numpy, scipy.optimize

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "DERIVATIVEFREEOPTIMIZATION")
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "BOBYQA",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = ["BOBYQA", "COBYLA", "NEWUOA", "POWELL", "SIMPLEX", "SUBPLEX"],
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
            message  = "Nombre maximal d'évaluations de la fonction",
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
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        if not PlatformInfo.has_nlopt and not self._parameters["Minimizer"] in ["COBYLA", "POWELL", "SIMPLEX"]:
            logging.warning("%s Minimization by SIMPLEX is forced because %s is unavailable (COBYLA, POWELL are also available)"%(self._name,self._parameters["Minimizer"]))
            self._parameters["Minimizer"] = "SIMPLEX"
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
        if len(Xini) < 2 and self._parameters["Minimizer"] == "NEWUOA":
            raise ValueError("The minimizer %s can not be used when the optimisation state dimension is 1. Please choose another minimizer."%self._parameters["Minimizer"])
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
                maxfun      = self._parameters["MaximumNumberOfFunctionEvaluations"],
                xtol        = self._parameters["StateVariationTolerance"],
                ftol        = self._parameters["CostDecrementTolerance"],
                full_output = True,
                disp        = self._parameters["optdisp"],
                )
        elif self._parameters["Minimizer"] == "COBYLA" and not PlatformInfo.has_nlopt:
            def make_constraints(bounds):
                constraints = []
                for (i,(a,b)) in enumerate(bounds):
                    lower = lambda x: x[i] - a
                    upper = lambda x: b - x[i]
                    constraints = constraints + [lower] + [upper]
                return constraints
            if self._parameters["Bounds"] is None:
                raise ValueError("Bounds have to be given for all axes as a list of lower/upper pairs!")
            Minimum = scipy.optimize.fmin_cobyla(
                func        = CostFunction,
                x0          = Xini,
                cons        = make_constraints( self._parameters["Bounds"] ),
                args        = (self._parameters["QualityCriterion"],),
                consargs    = (), # To avoid extra-args
                maxfun      = self._parameters["MaximumNumberOfFunctionEvaluations"],
                rhobeg      = 1.0,
                rhoend      = self._parameters["StateVariationTolerance"],
                catol       = 2.*self._parameters["StateVariationTolerance"],
                disp        = self._parameters["optdisp"],
                )
        elif self._parameters["Minimizer"] == "COBYLA" and PlatformInfo.has_nlopt:
            import nlopt
            opt = nlopt.opt(nlopt.LN_COBYLA, Xini.size)
            def _f(_Xx, Grad):
                # DFO, so no gradient
                return CostFunction(_Xx, self._parameters["QualityCriterion"])
            opt.set_min_objective(_f)
            if self._parameters["Bounds"] is not None:
                lub = numpy.array(self._parameters["Bounds"],dtype=float).reshape((Xini.size,2))
                lb = lub[:,0] ; lb[numpy.isnan(lb)] = -float('inf')
                ub = lub[:,1] ; ub[numpy.isnan(ub)] = +float('inf')
                if self._parameters["optdisp"]:
                    print("%s: upper bounds %s"%(opt.get_algorithm_name(),ub))
                    print("%s: lower bounds %s"%(opt.get_algorithm_name(),lb))
                opt.set_upper_bounds(ub)
                opt.set_lower_bounds(lb)
            opt.set_ftol_rel(self._parameters["CostDecrementTolerance"])
            opt.set_xtol_rel(2.*self._parameters["StateVariationTolerance"])
            opt.set_maxeval(self._parameters["MaximumNumberOfFunctionEvaluations"])
            Minimum = opt.optimize( Xini )
            if self._parameters["optdisp"]:
                print("%s: optimal state: %s"%(opt.get_algorithm_name(),Minimum))
                print("%s: minimum of J: %s"%(opt.get_algorithm_name(),opt.last_optimum_value()))
                print("%s: return code: %i"%(opt.get_algorithm_name(),opt.last_optimize_result()))
        elif self._parameters["Minimizer"] == "SIMPLEX" and not PlatformInfo.has_nlopt:
            Minimum, J_optimal, niter, nfeval, rc = scipy.optimize.fmin(
                func        = CostFunction,
                x0          = Xini,
                args        = (self._parameters["QualityCriterion"],),
                maxiter     = self._parameters["MaximumNumberOfSteps"]-1,
                maxfun      = self._parameters["MaximumNumberOfFunctionEvaluations"],
                xtol        = self._parameters["StateVariationTolerance"],
                ftol        = self._parameters["CostDecrementTolerance"],
                full_output = True,
                disp        = self._parameters["optdisp"],
                )
        elif self._parameters["Minimizer"] == "SIMPLEX" and PlatformInfo.has_nlopt:
            import nlopt
            opt = nlopt.opt(nlopt.LN_NELDERMEAD, Xini.size)
            def _f(_Xx, Grad):
                # DFO, so no gradient
                return CostFunction(_Xx, self._parameters["QualityCriterion"])
            opt.set_min_objective(_f)
            if self._parameters["Bounds"] is not None:
                lub = numpy.array(self._parameters["Bounds"],dtype=float).reshape((Xini.size,2))
                lb = lub[:,0] ; lb[numpy.isnan(lb)] = -float('inf')
                ub = lub[:,1] ; ub[numpy.isnan(ub)] = +float('inf')
                if self._parameters["optdisp"]:
                    print("%s: upper bounds %s"%(opt.get_algorithm_name(),ub))
                    print("%s: lower bounds %s"%(opt.get_algorithm_name(),lb))
                opt.set_upper_bounds(ub)
                opt.set_lower_bounds(lb)
            opt.set_ftol_rel(self._parameters["CostDecrementTolerance"])
            opt.set_xtol_rel(2.*self._parameters["StateVariationTolerance"])
            opt.set_maxeval(self._parameters["MaximumNumberOfFunctionEvaluations"])
            Minimum = opt.optimize( Xini )
            if self._parameters["optdisp"]:
                print("%s: optimal state: %s"%(opt.get_algorithm_name(),Minimum))
                print("%s: minimum of J: %s"%(opt.get_algorithm_name(),opt.last_optimum_value()))
                print("%s: return code: %i"%(opt.get_algorithm_name(),opt.last_optimize_result()))
        elif self._parameters["Minimizer"] == "BOBYQA" and PlatformInfo.has_nlopt:
            import nlopt
            opt = nlopt.opt(nlopt.LN_BOBYQA, Xini.size)
            def _f(_Xx, Grad):
                # DFO, so no gradient
                return CostFunction(_Xx, self._parameters["QualityCriterion"])
            opt.set_min_objective(_f)
            if self._parameters["Bounds"] is not None:
                lub = numpy.array(self._parameters["Bounds"],dtype=float).reshape((Xini.size,2))
                lb = lub[:,0] ; lb[numpy.isnan(lb)] = -float('inf')
                ub = lub[:,1] ; ub[numpy.isnan(ub)] = +float('inf')
                if self._parameters["optdisp"]:
                    print("%s: upper bounds %s"%(opt.get_algorithm_name(),ub))
                    print("%s: lower bounds %s"%(opt.get_algorithm_name(),lb))
                opt.set_upper_bounds(ub)
                opt.set_lower_bounds(lb)
            opt.set_ftol_rel(self._parameters["CostDecrementTolerance"])
            opt.set_xtol_rel(2.*self._parameters["StateVariationTolerance"])
            opt.set_maxeval(self._parameters["MaximumNumberOfFunctionEvaluations"])
            Minimum = opt.optimize( Xini )
            if self._parameters["optdisp"]:
                print("%s: optimal state: %s"%(opt.get_algorithm_name(),Minimum))
                print("%s: minimum of J: %s"%(opt.get_algorithm_name(),opt.last_optimum_value()))
                print("%s: return code: %i"%(opt.get_algorithm_name(),opt.last_optimize_result()))
        elif self._parameters["Minimizer"] == "NEWUOA" and PlatformInfo.has_nlopt:
            import nlopt
            opt = nlopt.opt(nlopt.LN_NEWUOA, Xini.size)
            def _f(_Xx, Grad):
                # DFO, so no gradient
                return CostFunction(_Xx, self._parameters["QualityCriterion"])
            opt.set_min_objective(_f)
            if self._parameters["Bounds"] is not None:
                lub = numpy.array(self._parameters["Bounds"],dtype=float).reshape((Xini.size,2))
                lb = lub[:,0] ; lb[numpy.isnan(lb)] = -float('inf')
                ub = lub[:,1] ; ub[numpy.isnan(ub)] = +float('inf')
                if self._parameters["optdisp"]:
                    print("%s: upper bounds %s"%(opt.get_algorithm_name(),ub))
                    print("%s: lower bounds %s"%(opt.get_algorithm_name(),lb))
                opt.set_upper_bounds(ub)
                opt.set_lower_bounds(lb)
            opt.set_ftol_rel(self._parameters["CostDecrementTolerance"])
            opt.set_xtol_rel(2.*self._parameters["StateVariationTolerance"])
            opt.set_maxeval(self._parameters["MaximumNumberOfFunctionEvaluations"])
            Minimum = opt.optimize( Xini )
            if self._parameters["optdisp"]:
                print("%s: optimal state: %s"%(opt.get_algorithm_name(),Minimum))
                print("%s: minimum of J: %s"%(opt.get_algorithm_name(),opt.last_optimum_value()))
                print("%s: return code: %i"%(opt.get_algorithm_name(),opt.last_optimize_result()))
        elif self._parameters["Minimizer"] == "SUBPLEX" and PlatformInfo.has_nlopt:
            import nlopt
            opt = nlopt.opt(nlopt.LN_SBPLX, Xini.size)
            def _f(_Xx, Grad):
                # DFO, so no gradient
                return CostFunction(_Xx, self._parameters["QualityCriterion"])
            opt.set_min_objective(_f)
            if self._parameters["Bounds"] is not None:
                lub = numpy.array(self._parameters["Bounds"],dtype=float).reshape((Xini.size,2))
                lb = lub[:,0] ; lb[numpy.isnan(lb)] = -float('inf')
                ub = lub[:,1] ; ub[numpy.isnan(ub)] = +float('inf')
                if self._parameters["optdisp"]:
                    print("%s: upper bounds %s"%(opt.get_algorithm_name(),ub))
                    print("%s: lower bounds %s"%(opt.get_algorithm_name(),lb))
                opt.set_upper_bounds(ub)
                opt.set_lower_bounds(lb)
            opt.set_ftol_rel(self._parameters["CostDecrementTolerance"])
            opt.set_xtol_rel(2.*self._parameters["StateVariationTolerance"])
            opt.set_maxeval(self._parameters["MaximumNumberOfFunctionEvaluations"])
            Minimum = opt.optimize( Xini )
            if self._parameters["optdisp"]:
                print("%s: optimal state: %s"%(opt.get_algorithm_name(),Minimum))
                print("%s: minimum of J: %s"%(opt.get_algorithm_name(),opt.last_optimum_value()))
                print("%s: return code: %i"%(opt.get_algorithm_name(),opt.last_optimize_result()))
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
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._toStore("OMA" ) or \
            self._toStore("SimulatedObservationAtOptimum"):
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
