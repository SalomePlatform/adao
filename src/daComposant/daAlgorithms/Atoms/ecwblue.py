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
    BLUE
"""
__author__ = "Jean-Philippe ARGAUD"

import logging, numpy
from daCore.NumericObjects import QuantilesEstimations
from daCore.PlatformInfo import PlatformInfo, vfloat
mpr = PlatformInfo().MachinePrecision()

# ==============================================================================
def ecwblue(selfA, Xb, Y, U, HO, CM, R, B, __storeState = False):
    """
    Correction
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Tangent"].asMatrix(Xb)
    Hm = Hm.reshape(Y.size, Xb.size)  # ADAO & check shape
    Ha = HO["Adjoint"].asMatrix(Xb)
    Ha = Ha.reshape(Xb.size, Y.size)  # ADAO & check shape
    #
    if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
        HXb = numpy.asarray(HO["AppliedInX"]["HXb"])
    else:
        HXb = Hm @ Xb
    HXb = HXb.reshape((-1, 1))
    if Y.size != HXb.size:
        raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size, HXb.size))  # noqa: E501
    if max(Y.shape) != max(HXb.shape):
        raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape, HXb.shape))  # noqa: E501
    #
    if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CostFunctionJ" ) or selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJb") or selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJo") or selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("MahalanobisConsistency") or \
            (Y.size > Xb.size):
        if isinstance(B, numpy.ndarray):
            BI = numpy.linalg.inv(B)
        else:
            BI = B.getI()
        RI = R.getI()
    #
    Innovation  = Y - HXb
    if selfA._parameters["EstimationOf"] == "Parameters":
        if CM is not None and "Tangent" in CM and U is not None:  # Attention : si Cm est aussi dans H, doublon !
            Cm = CM["Tangent"].asMatrix(Xb)
            Cm = Cm.reshape(Xb.size, U.size)  # ADAO & check shape
            Innovation = Innovation - (Cm @ U).reshape((-1, 1))
    #
    # Calcul de l'analyse
    # -------------------
    if Y.size <= Xb.size:
        _HNHt = numpy.dot(Hm, B @ Ha)
        _A = R + _HNHt
        _u = numpy.linalg.solve( _A, numpy.ravel(Innovation) )
        Xa = Xb + (B @ numpy.ravel(Ha @ _u)).reshape((-1, 1))
    else:
        _HtRH = numpy.dot(Ha, RI @ Hm)
        _A = BI + _HtRH
        _u = numpy.linalg.solve( _A, numpy.ravel(numpy.dot(Ha, RI @ numpy.ravel(Innovation))) )
        Xa = Xb + _u.reshape((-1, 1))
    #
    if __storeState:
        selfA._setInternalState("Xn", Xa)
    # --------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    # Calcul de la fonction coût
    # --------------------------
    if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CostFunctionJ" ) or selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJb") or selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJo") or selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("OMA") or \
            selfA._toStore("InnovationAtCurrentAnalysis") or \
            selfA._toStore("SigmaObs2") or \
            selfA._toStore("MahalanobisConsistency") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum") or \
            selfA._toStore("SimulatedObservationAtCurrentState") or \
            selfA._toStore("SimulatedObservationAtOptimum") or \
            selfA._toStore("SimulationQuantiles"):
        HXa = Hm @ Xa
        oma = Y - HXa.reshape((-1, 1))
    if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CostFunctionJ" ) or selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJb") or selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJo") or selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("MahalanobisConsistency"):
        Jb  = vfloat( 0.5 * (Xa - Xb).T @ (BI @ (Xa - Xb)) )
        Jo  = vfloat( 0.5 * oma.T * (RI * oma) )
        J   = Jb + Jo
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( Jb )
        selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( Jo )
        selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( J )
    #
    # Calcul de la covariance d'analyse
    # ---------------------------------
    if selfA._toStore("APosterioriCovariance") or \
            selfA._toStore("SimulationQuantiles"):
        if (Y.size <= Xb.size):
            K  = B * Ha * (R + numpy.dot(Hm, B * Ha)).I
        elif (Y.size > Xb.size):
            K = (BI + numpy.dot(Ha, RI * Hm)).I * Ha * RI
        A = B - K * Hm * B
        A = (A + A.T) * 0.5  # Symétrie
        A = A + mpr * numpy.trace( A ) * numpy.identity(Xa.size)  # Positivité
        if min(A.shape) != max(A.shape):
            raise ValueError("The %s a posteriori covariance matrix A is of shape %s, despites it has to be a squared matrix. There is an error in the observation operator, please check it."%(selfA._name, str(A.shape)))  # noqa: E501
        if (numpy.diag(A) < 0).any():
            raise ValueError("The %s a posteriori covariance matrix A has at least one negative value %.2e on its diagonal. There is an error in the observation operator or in the covariances, please check them."%(selfA._name, min(numpy.diag(A))))  # noqa: E501
        if logging.getLogger().level < logging.WARNING:  # La vérification n'a lieu qu'en debug
            try:
                numpy.linalg.cholesky( A )
            except Exception:
                raise ValueError("The %s a posteriori covariance matrix A is not symmetric positive-definite. Please check your a priori covariances and your observation operator."%(selfA._name,))  # noqa: E501
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        selfA.StoredVariables["CurrentState"].store( Xa )
    if selfA._toStore("CurrentOptimum"):
        selfA.StoredVariables["CurrentOptimum"].store( Xa )
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
        selfA.StoredVariables["SigmaObs2"].store( vfloat( Innovation.T @ oma ) / TraceR )
    if selfA._toStore("SigmaBck2"):
        selfA.StoredVariables["SigmaBck2"].store( vfloat( (Innovation.T @ (Hm @ (numpy.ravel(Xa) - numpy.ravel(Xb)))) / (Hm * (B * Hm.T)).trace() ) )  # noqa: E501
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2. * J / Innovation.size ) )
    if selfA._toStore("SimulationQuantiles"):
        H  = HO["Direct"].appliedTo
        QuantilesEstimations(selfA, A, Xa, HXa, H, Hm)
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtCurrentState"):
        selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HXa )
    if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
        selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( HXa )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
