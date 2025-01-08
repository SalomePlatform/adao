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
    Standard Kalman Filter
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy
from daCore.PlatformInfo import PlatformInfo, vfloat
mpr = PlatformInfo().MachinePrecision()

# ==============================================================================
def ecwstdkf(selfA, Xb, Y, U, HO, CM, R, B, __storeState = False):
    """
    Correction
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Initialisations
    # ---------------
    Hm = HO["Tangent"].asMatrix(Xb)
    Hm = Hm.reshape(Y.size, Xb.size)  # ADAO & check shape
    Ha = HO["Adjoint"].asMatrix(Xb)
    Ha = Ha.reshape(Xb.size, Y.size)  # ADAO & check shape
    #
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
            selfA._toStore("CurrentOptimum") or selfA._toStore("APosterioriCovariance") or \
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
        _u = numpy.linalg.solve( _A, Innovation )
        Xa = Xb + (B @ (Ha @ _u)).reshape((-1, 1))
        K  = B @ (Ha @ numpy.linalg.inv(_A))
    else:
        _HtRH = numpy.dot(Ha, RI @ Hm)
        _A = BI + _HtRH
        _u = numpy.linalg.solve( _A, numpy.dot(Ha, RI @ Innovation) )
        Xa = Xb + _u.reshape((-1, 1))
        K = numpy.linalg.inv(_A) @ (Ha @ RI.asfullmatrix(Y.size))
    #
    Pa = B - K @ (Hm @ B)
    Pa = (Pa + Pa.T) * 0.5  # Symétrie
    Pa = Pa + mpr * numpy.trace( Pa ) * numpy.identity(Xa.size)  # Positivité
    #
    if __storeState:
        selfA._setInternalState("Xn", Xa)
        selfA._setInternalState("Pn", Pa)
    # --------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
        selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( Hm @ Xa )
    if selfA._toStore("InnovationAtCurrentAnalysis"):
        selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( Innovation )
    # ---> avec current state
    if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
        selfA.StoredVariables["CurrentState"].store( Xa )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("InnovationAtCurrentState"):
        selfA.StoredVariables["InnovationAtCurrentState"].store( Innovation )
    if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
        selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HXb )
    # ---> autres
    if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") or selfA._toStore("APosterioriCovariance"):
        Jb  = vfloat( 0.5 * (Xa - Xb).T @ (BI @ (Xa - Xb)) )
        Jo  = vfloat( 0.5 * Innovation.T @ (RI @ Innovation) )
        J   = Jb + Jo
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        #
        if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][:] )
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
        if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )  # noqa: E501
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )  # noqa: E501
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )  # noqa: E501
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )  # noqa: E501
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( Pa )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
