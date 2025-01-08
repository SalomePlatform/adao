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
    Non Linear Least Squares
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, scipy, scipy.optimize, scipy.version
from daCore.PlatformInfo import vt, vfloat, trmo

# ==============================================================================
def ecwnlls(selfA, Xb, Y, U, HO, CM, R, B, __storeState = False):
    """
    Correction
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
    Ha = HO["Adjoint"].appliedInXTo
    #
    if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
        HXb = numpy.asarray(Hm( Xb, HO["AppliedInX"]["HXb"] ))
    else:
        HXb = numpy.asarray(Hm( Xb ))
    HXb = HXb.reshape((-1, 1))
    if Y.size != HXb.size:
        raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size, HXb.size))  # noqa: E501
    if max(Y.shape) != max(HXb.shape):
        raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape, HXb.shape))  # noqa: E501
    #
    RI = R.getI()
    if selfA._parameters["Minimizer"] == "LM":
        RdemiI = R.choleskyI()
    #
    Xini = selfA._parameters["InitializationPoint"]
    #
    # Définition de la fonction-coût
    # ------------------------------

    def CostFunction(x):
        _X  = numpy.asarray(x).reshape((-1, 1))
        if selfA._parameters["StoreInternalVariables"] or \
                selfA._toStore("CurrentState") or \
                selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( _X )
        _HX = numpy.asarray(Hm( _X )).reshape((-1, 1))
        _Innovation = Y - _HX
        if selfA._toStore("SimulatedObservationAtCurrentState") or \
                selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        #
        Jb  = 0.
        Jo  = vfloat( 0.5 * _Innovation.T * (RI * _Innovation) )
        J   = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
                selfA._toStore("CurrentOptimum") or \
                selfA._toStore("CostFunctionJAtCurrentOptimum") or \
                selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
                selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
                selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )  # noqa: E501
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )  # noqa: E501
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )  # noqa: E501
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )  # noqa: E501
        return J

    def GradientOfCostFunction(x):
        _X      = numpy.asarray(x).reshape((-1, 1))
        _HX     = numpy.asarray(Hm( _X )).reshape((-1, 1))
        GradJb  = 0.
        GradJo  = - Ha( (_X, RI * (Y - _HX)) )
        GradJ   = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
        return GradJ

    def CostFunctionLM(x):
        _X  = numpy.ravel( x ).reshape((-1, 1))
        _HX = Hm( _X ).reshape((-1, 1))
        _Innovation = Y - _HX
        Jb  = 0.
        Jo  = vfloat( 0.5 * _Innovation.T * (RI * _Innovation) )
        J   = Jb + Jo
        if selfA._parameters["StoreInternalVariables"] or \
                selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( _X )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        #
        return numpy.ravel( RdemiI * _Innovation )

    def GradientOfCostFunctionLM(x):
        _X      = x.reshape((-1, 1))
        return - RdemiI * HO["Tangent"].asMatrix( _X )
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
        optimiseur = trmo()
        Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfIterations"] - 1,
            factr       = selfA._parameters["CostDecrementTolerance"] * 1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
        )
        # nfeval = Informations['funcalls']
        # rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfIterations"],
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            ftol        = selfA._parameters["CostDecrementTolerance"],
            messages    = selfA._parameters["optmessages"],
        )
    elif selfA._parameters["Minimizer"] == "CG":
        Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfIterations"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
        )
    elif selfA._parameters["Minimizer"] == "NCG":
        Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfIterations"],
            avextol     = selfA._parameters["CostDecrementTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
        )
    elif selfA._parameters["Minimizer"] == "BFGS":
        Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfIterations"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
        )
    elif selfA._parameters["Minimizer"] == "LM":
        Minimum, cov_x, infodict, mesg, rc = scipy.optimize.leastsq(
            func        = CostFunctionLM,
            x0          = Xini,
            Dfun        = GradientOfCostFunctionLM,
            args        = (),
            ftol        = selfA._parameters["CostDecrementTolerance"],
            maxfev      = selfA._parameters["MaximumNumberOfIterations"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            full_output = True,
        )
        # nfeval = infodict['nfev']
    else:
        raise ValueError("Error in minimizer name: %s is unkown"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
    #
    Xa = Minimum
    if __storeState:
        selfA._setInternalState("Xn", Xa)
    # --------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
            selfA._toStore("InnovationAtCurrentAnalysis") or \
            selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
        oma = Y - numpy.asarray(HXa).reshape((-1, 1))
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
            selfA._toStore("OMB"):
        Innovation  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( Innovation )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( oma )
    if selfA._toStore("InnovationAtCurrentAnalysis"):
        selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( oma )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( Innovation )
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
