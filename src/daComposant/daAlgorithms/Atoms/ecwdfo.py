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

__doc__ = """
    DFO
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, logging, scipy.optimize
from daCore.NumericObjects import ApplyBounds, ForceNumericBounds
from daCore.NumericObjects import CostFunction3D as CostFunction
from daCore import PlatformInfo
lpi = PlatformInfo.PlatformInfo()

# ==============================================================================
def ecwdfo(selfA, Xb, Xini, Y, U, HO, CM, R, B, __storeState = False):
    """
    Correction
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
    Xini = Xini.reshape((-1,))
    #
    if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
        HXb = numpy.asarray(Hm( Xb, HO["AppliedInX"]["HXb"] )).reshape((-1, 1))
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size, HXb.size))  # noqa: E501
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape, HXb.shape))  # noqa: E501
    #
    if not lpi.has_nlopt and not selfA._parameters["Minimizer"] in ["COBYLA", "POWELL", "SIMPLEX"]:
        logging.warning(
            "%s Minimization by SIMPLEX is forced because %s "%(selfA._name, selfA._parameters["Minimizer"]) + \
            "is unavailable (COBYLA, POWELL are also available)")
        selfA._parameters["Minimizer"] = "SIMPLEX"
    if numpy.asarray(Xini).size < 2 and selfA._parameters["Minimizer"] == "NEWUOA":
        raise ValueError(
            "The minimizer %s "%selfA._parameters["Minimizer"] + \
            "can not be used when the optimisation state dimension " + \
            "is 1. Please choose another minimizer.")
    if not selfA._toStore("CurrentState"):
        selfA._parameters["StoreSupplementaryCalculations"] = tuple(
            list(selfA._parameters["StoreSupplementaryCalculations"]) + ["CurrentState"]
        )
    #
    BI = B.getI()
    RI = R.getI()
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "POWELL":
        Minimum, J_optimal, direc, niter, nfeval, rc = scipy.optimize.fmin_powell(
            func        = CostFunction,
            x0          = Xini,
            args        = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False),
            maxiter     = selfA._parameters["MaximumNumberOfIterations"] - 1,
            maxfun      = selfA._parameters["MaximumNumberOfFunctionEvaluations"],
            xtol        = selfA._parameters["StateVariationTolerance"],
            ftol        = selfA._parameters["CostDecrementTolerance"],
            full_output = True,
            disp        = selfA._parameters["optdisp"],
        )
    elif selfA._parameters["Minimizer"] == "COBYLA" and not lpi.has_nlopt:
        def make_constraints(bounds):
            constraints = []
            for (i, (a, b)) in enumerate(bounds):
                lower = lambda x: x[i] - a  # noqa: E731
                upper = lambda x: b - x[i]  # noqa: E731
                constraints = constraints + [lower] + [upper]
            return constraints
        if selfA._parameters["Bounds"] is None:
            raise ValueError("Bounds have to be given for all axes as a list of lower/upper pairs!")
        selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
        Xini = ApplyBounds( Xini, selfA._parameters["Bounds"] )
        Minimum = scipy.optimize.fmin_cobyla(
            func        = CostFunction,
            x0          = Xini,
            cons        = make_constraints( selfA._parameters["Bounds"] ),
            args        = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False),
            consargs    = (),  # To avoid extra-args
            maxfun      = selfA._parameters["MaximumNumberOfFunctionEvaluations"],
            rhobeg      = 1.0,
            rhoend      = selfA._parameters["StateVariationTolerance"],
            catol       = 2. * selfA._parameters["StateVariationTolerance"],
            disp        = selfA._parameters["optdisp"],
        )
    elif selfA._parameters["Minimizer"] == "COBYLA" and lpi.has_nlopt:
        import nlopt
        opt = nlopt.opt(nlopt.LN_COBYLA, Xini.size)

        def _f(_Xx, Grad):
            # DFO, so no gradient
            args = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False)
            return CostFunction(_Xx, *args)
        opt.set_min_objective(_f)
        selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
        Xini = ApplyBounds( Xini, selfA._parameters["Bounds"] )
        if selfA._parameters["Bounds"] is not None:
            lub = numpy.array(selfA._parameters["Bounds"], dtype=float).reshape((Xini.size, 2))
            lb = lub[:, 0]; lb[numpy.isnan(lb)] = -float('inf')  # noqa: E702
            ub = lub[:, 1]; ub[numpy.isnan(ub)] = +float('inf')  # noqa: E702
            if selfA._parameters["optdisp"]:
                print("%s: upper bounds %s"%(opt.get_algorithm_name(), ub))
                print("%s: lower bounds %s"%(opt.get_algorithm_name(), lb))
            opt.set_upper_bounds(ub)
            opt.set_lower_bounds(lb)
        opt.set_ftol_rel(selfA._parameters["CostDecrementTolerance"])
        opt.set_xtol_rel(2. * selfA._parameters["StateVariationTolerance"])
        opt.set_maxeval(selfA._parameters["MaximumNumberOfFunctionEvaluations"])
        Minimum = opt.optimize( Xini )
        if selfA._parameters["optdisp"]:
            print("%s: optimal state: %s"%(opt.get_algorithm_name(), Minimum))
            print("%s: minimum of J: %s"%(opt.get_algorithm_name(), opt.last_optimum_value()))
            print("%s: return code: %i"%(opt.get_algorithm_name(), opt.last_optimize_result()))
    elif selfA._parameters["Minimizer"] == "SIMPLEX" and not lpi.has_nlopt:
        Minimum, J_optimal, niter, nfeval, rc = scipy.optimize.fmin(
            func        = CostFunction,
            x0          = Xini,
            args        = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False),
            maxiter     = selfA._parameters["MaximumNumberOfIterations"] - 1,
            maxfun      = selfA._parameters["MaximumNumberOfFunctionEvaluations"],
            xtol        = selfA._parameters["StateVariationTolerance"],
            ftol        = selfA._parameters["CostDecrementTolerance"],
            full_output = True,
            disp        = selfA._parameters["optdisp"],
        )
    elif selfA._parameters["Minimizer"] == "SIMPLEX" and lpi.has_nlopt:
        import nlopt
        opt = nlopt.opt(nlopt.LN_NELDERMEAD, Xini.size)

        def _f(_Xx, Grad):
            # DFO, so no gradient
            args = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False)
            return CostFunction(_Xx, *args)
        opt.set_min_objective(_f)
        selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
        Xini = ApplyBounds( Xini, selfA._parameters["Bounds"] )
        if selfA._parameters["Bounds"] is not None:
            lub = numpy.array(selfA._parameters["Bounds"], dtype=float).reshape((Xini.size, 2))
            lb = lub[:, 0]; lb[numpy.isnan(lb)] = -float('inf')  # noqa: E702
            ub = lub[:, 1]; ub[numpy.isnan(ub)] = +float('inf')  # noqa: E702
            if selfA._parameters["optdisp"]:
                print("%s: upper bounds %s"%(opt.get_algorithm_name(), ub))
                print("%s: lower bounds %s"%(opt.get_algorithm_name(), lb))
            opt.set_upper_bounds(ub)
            opt.set_lower_bounds(lb)
        opt.set_ftol_rel(selfA._parameters["CostDecrementTolerance"])
        opt.set_xtol_rel(2. * selfA._parameters["StateVariationTolerance"])
        opt.set_maxeval(selfA._parameters["MaximumNumberOfFunctionEvaluations"])
        Minimum = opt.optimize( Xini )
        if selfA._parameters["optdisp"]:
            print("%s: optimal state: %s"%(opt.get_algorithm_name(), Minimum))
            print("%s: minimum of J: %s"%(opt.get_algorithm_name(), opt.last_optimum_value()))
            print("%s: return code: %i"%(opt.get_algorithm_name(), opt.last_optimize_result()))
    elif selfA._parameters["Minimizer"] == "BOBYQA" and lpi.has_nlopt:
        import nlopt
        opt = nlopt.opt(nlopt.LN_BOBYQA, Xini.size)

        def _f(_Xx, Grad):
            # DFO, so no gradient
            args = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False)
            return CostFunction(_Xx, *args)
        opt.set_min_objective(_f)
        selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
        Xini = ApplyBounds( Xini, selfA._parameters["Bounds"] )
        if selfA._parameters["Bounds"] is not None:
            lub = numpy.array(selfA._parameters["Bounds"], dtype=float).reshape((Xini.size, 2))
            lb = lub[:, 0]; lb[numpy.isnan(lb)] = -float('inf')  # noqa: E702
            ub = lub[:, 1]; ub[numpy.isnan(ub)] = +float('inf')  # noqa: E702
            if selfA._parameters["optdisp"]:
                print("%s: upper bounds %s"%(opt.get_algorithm_name(), ub))
                print("%s: lower bounds %s"%(opt.get_algorithm_name(), lb))
            opt.set_upper_bounds(ub)
            opt.set_lower_bounds(lb)
        opt.set_ftol_rel(selfA._parameters["CostDecrementTolerance"])
        opt.set_xtol_rel(2. * selfA._parameters["StateVariationTolerance"])
        opt.set_maxeval(selfA._parameters["MaximumNumberOfFunctionEvaluations"])
        Minimum = opt.optimize( Xini )
        if selfA._parameters["optdisp"]:
            print("%s: optimal state: %s"%(opt.get_algorithm_name(), Minimum))
            print("%s: minimum of J: %s"%(opt.get_algorithm_name(), opt.last_optimum_value()))
            print("%s: return code: %i"%(opt.get_algorithm_name(), opt.last_optimize_result()))
    elif selfA._parameters["Minimizer"] == "NEWUOA" and lpi.has_nlopt:
        import nlopt
        opt = nlopt.opt(nlopt.LN_NEWUOA, Xini.size)

        def _f(_Xx, Grad):
            # DFO, so no gradient
            args = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False)
            return CostFunction(_Xx, *args)
        opt.set_min_objective(_f)
        selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
        Xini = ApplyBounds( Xini, selfA._parameters["Bounds"] )
        if selfA._parameters["Bounds"] is not None:
            lub = numpy.array(selfA._parameters["Bounds"], dtype=float).reshape((Xini.size, 2))
            lb = lub[:, 0]; lb[numpy.isnan(lb)] = -float('inf')  # noqa: E702
            ub = lub[:, 1]; ub[numpy.isnan(ub)] = +float('inf')  # noqa: E702
            if selfA._parameters["optdisp"]:
                print("%s: upper bounds %s"%(opt.get_algorithm_name(), ub))
                print("%s: lower bounds %s"%(opt.get_algorithm_name(), lb))
            opt.set_upper_bounds(ub)
            opt.set_lower_bounds(lb)
        opt.set_ftol_rel(selfA._parameters["CostDecrementTolerance"])
        opt.set_xtol_rel(2. * selfA._parameters["StateVariationTolerance"])
        opt.set_maxeval(selfA._parameters["MaximumNumberOfFunctionEvaluations"])
        Minimum = opt.optimize( Xini )
        if selfA._parameters["optdisp"]:
            print("%s: optimal state: %s"%(opt.get_algorithm_name(), Minimum))
            print("%s: minimum of J: %s"%(opt.get_algorithm_name(), opt.last_optimum_value()))
            print("%s: return code: %i"%(opt.get_algorithm_name(), opt.last_optimize_result()))
    elif selfA._parameters["Minimizer"] == "SUBPLEX" and lpi.has_nlopt:
        import nlopt
        opt = nlopt.opt(nlopt.LN_SBPLX, Xini.size)

        def _f(_Xx, Grad):
            # DFO, so no gradient
            args = (selfA, Xb, Hm, Y, BI, RI, nbPreviousSteps, selfA._parameters["QualityCriterion"], True, False, False)
            return CostFunction(_Xx, *args)
        opt.set_min_objective(_f)
        selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
        Xini = ApplyBounds( Xini, selfA._parameters["Bounds"] )
        if selfA._parameters["Bounds"] is not None:
            lub = numpy.array(selfA._parameters["Bounds"], dtype=float).reshape((Xini.size, 2))
            lb = lub[:, 0]; lb[numpy.isnan(lb)] = -float('inf')  # noqa: E702
            ub = lub[:, 1]; ub[numpy.isnan(ub)] = +float('inf')  # noqa: E702
            if selfA._parameters["optdisp"]:
                print("%s: upper bounds %s"%(opt.get_algorithm_name(), ub))
                print("%s: lower bounds %s"%(opt.get_algorithm_name(), lb))
            opt.set_upper_bounds(ub)
            opt.set_lower_bounds(lb)
        opt.set_ftol_rel(selfA._parameters["CostDecrementTolerance"])
        opt.set_xtol_rel(2. * selfA._parameters["StateVariationTolerance"])
        opt.set_maxeval(selfA._parameters["MaximumNumberOfFunctionEvaluations"])
        Minimum = opt.optimize( Xini )
        if selfA._parameters["optdisp"]:
            print("%s: optimal state: %s"%(opt.get_algorithm_name(), Minimum))
            print("%s: minimum of J: %s"%(opt.get_algorithm_name(), opt.last_optimum_value()))
            print("%s: return code: %i"%(opt.get_algorithm_name(), opt.last_optimize_result()))
    else:
        raise ValueError("Error in minimizer name: %s is unkown"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    Minimum  = selfA.StoredVariables["CurrentState"][IndexMin]
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = Minimum
    if __storeState:
        selfA._setInternalState("Xn", Xa)
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("OMA") or \
            selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm(Xa)
        HXa = HXa.reshape((-1, 1))
    if selfA._toStore("Innovation") or \
            selfA._toStore("OMB") or \
            selfA._toStore("SimulatedObservationAtBackground"):
        HXb = Hm(Xb).reshape((-1, 1))
        Innovation = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( Innovation )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( Innovation )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( Y - HXa )
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    if selfA._toStore("EnsembleOfStates"):
        selfA.StoredVariables["EnsembleOfStates"].store( numpy.array(selfA.StoredVariables["CurrentState"][nbPreviousSteps:]).T )
    if selfA._toStore("EnsembleOfSimulations"):
        selfA.StoredVariables["EnsembleOfSimulations"].store( numpy.array(selfA.StoredVariables["SimulatedObservationAtCurrentState"][nbPreviousSteps:]).T )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
