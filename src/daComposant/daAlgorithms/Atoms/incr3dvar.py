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
    3DVAR incrémental
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, scipy, scipy.optimize, scipy.version
from daCore.NumericObjects import HessienneEstimation, QuantilesEstimations
from daCore.NumericObjects import RecentredBounds
from daCore.PlatformInfo import PlatformInfo, vt, vfloat
mpr = PlatformInfo().MachinePrecision()

# ==============================================================================
def incr3dvar(selfA, Xb, Y, U, HO, CM, R, B, __storeState = False):
    """
    Correction
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
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
    if selfA._toStore("JacobianMatrixAtBackground"):
        HtMb = HO["Tangent"].asMatrix(ValueForMethodForm = Xb)
        HtMb = HtMb.reshape(Y.size, Xb.size)  # ADAO & check shape
        selfA.StoredVariables["JacobianMatrixAtBackground"].store( HtMb )
    #
    BI = B.getI()
    RI = R.getI()
    #
    Innovation = Y - HXb
    #
    # Outer Loop
    # ----------
    iOuter = 0
    J      = 1. / mpr
    DeltaJ = 1. / mpr
    Xr     = numpy.asarray(selfA._parameters["InitializationPoint"]).reshape((-1, 1))
    while abs(DeltaJ) >= selfA._parameters["CostDecrementTolerance"] and iOuter <= selfA._parameters["MaximumNumberOfIterations"]:  # noqa: E501
        #
        # Inner Loop
        # ----------
        Ht = HO["Tangent"].asMatrix(Xr)
        Ht = Ht.reshape(Y.size, Xr.size)  # ADAO & check shape
        #
        # Définition de la fonction-coût
        # ------------------------------

        def CostFunction(dx):
            _dX  = numpy.asarray(dx).reshape((-1, 1))
            if selfA._parameters["StoreInternalVariables"] or \
                    selfA._toStore("CurrentState") or \
                    selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentState"].store( Xb + _dX )
            _HdX = (Ht @ _dX).reshape((-1, 1))
            _dInnovation = Innovation - _HdX
            if selfA._toStore("SimulatedObservationAtCurrentState") or \
                    selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HXb + _HdX )
            if selfA._toStore("InnovationAtCurrentState"):
                selfA.StoredVariables["InnovationAtCurrentState"].store( _dInnovation )
            #
            Jb  = vfloat( 0.5 * _dX.T @ (BI @ _dX) )
            Jo  = vfloat( 0.5 * _dInnovation.T @ (RI @ _dInnovation) )
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

        def GradientOfCostFunction(dx):
            _dX          = numpy.ravel( dx )
            _HdX         = (Ht @ _dX).reshape((-1, 1))
            _dInnovation = Innovation - _HdX
            GradJb       = BI @ _dX
            GradJo       = - Ht.T @ (RI * _dInnovation)
            GradJ        = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
            return GradJ
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
        #
        if selfA._parameters["Minimizer"] == "LBFGSB":
            # Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
            if vt("0.19")  <= vt(scipy.version.version) <= vt("1.4.99"):
                import daAlgorithms.Atoms.lbfgsb14hlt as optimiseur
            elif vt("1.5.0") <= vt(scipy.version.version) <= vt("1.7.99"):
                import daAlgorithms.Atoms.lbfgsb17hlt as optimiseur
            elif vt("1.8.0") <= vt(scipy.version.version) <= vt("1.8.99"):
                import daAlgorithms.Atoms.lbfgsb18hlt as optimiseur
            elif vt("1.9.0") <= vt(scipy.version.version) <= vt("1.10.99"):
                import daAlgorithms.Atoms.lbfgsb19hlt as optimiseur
            elif vt("1.11.0") <= vt(scipy.version.version) <= vt("1.11.99"):
                import daAlgorithms.Atoms.lbfgsb111hlt as optimiseur
            elif vt("1.12.0") <= vt(scipy.version.version) <= vt("1.12.99"):
                import daAlgorithms.Atoms.lbfgsb112hlt as optimiseur
            elif vt("1.13.0") <= vt(scipy.version.version) <= vt("1.13.99"):
                import daAlgorithms.Atoms.lbfgsb113hlt as optimiseur
            else:
                import scipy.optimize as optimiseur
            Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
                func        = CostFunction,
                x0          = numpy.zeros(Xb.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = RecentredBounds(selfA._parameters["Bounds"], Xb),
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
                x0          = numpy.zeros(Xb.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = RecentredBounds(selfA._parameters["Bounds"], Xb),
                maxfun      = selfA._parameters["MaximumNumberOfIterations"],
                pgtol       = selfA._parameters["ProjectedGradientTolerance"],
                ftol        = selfA._parameters["CostDecrementTolerance"],
                messages    = selfA._parameters["optmessages"],
            )
        elif selfA._parameters["Minimizer"] == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(Xb.size),
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
                x0          = numpy.zeros(Xb.size),
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
                x0          = numpy.zeros(Xb.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = selfA._parameters["MaximumNumberOfIterations"],
                gtol        = selfA._parameters["GradientNormTolerance"],
                disp        = selfA._parameters["optdisp"],
                full_output = True,
            )
        else:
            raise ValueError("Error in minimizer name: %s is unkown"%selfA._parameters["Minimizer"])
        #
        IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
        #
        if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
            Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
        else:
            Minimum = Xb + Minimum.reshape((-1, 1))
        #
        Xr     = Minimum
        DeltaJ = selfA.StoredVariables["CostFunctionJ" ][-1] - J
        iOuter = selfA.StoredVariables["CurrentIterationNumber"][-1]
    #
    Xa = Xr
    if __storeState:
        selfA._setInternalState("Xn", Xa)
    # --------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
            selfA._toStore("InnovationAtCurrentAnalysis") or \
            selfA._toStore("SigmaObs2") or \
            selfA._toStore("SimulationQuantiles") or \
            selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
        oma = Y - numpy.asarray(HXa).reshape((-1, 1))
    #
    if selfA._toStore("APosterioriCovariance") or \
            selfA._toStore("SimulationQuantiles") or \
            selfA._toStore("JacobianMatrixAtOptimum") or \
            selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size, Xa.size)  # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
            selfA._toStore("SimulationQuantiles") or \
            selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size, Y.size)  # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
            selfA._toStore("SimulationQuantiles"):
        A = HessienneEstimation(selfA, Xa.size, HaM, HtM, BI, RI)
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if (Y.size <= Xb.size):
            KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size > Xb.size):
            KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
            selfA._toStore("SigmaObs2") or \
            selfA._toStore("MahalanobisConsistency") or \
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
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( vfloat( (Innovation.T @ oma) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2. * MinJ / Innovation.size ) )
    if selfA._toStore("SimulationQuantiles"):
        QuantilesEstimations(selfA, A, Xa, HXa, Hm, HtM)
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
