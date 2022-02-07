# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2022 EDF R&D
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
    Contrained Extended Kalman Filter
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy
from daCore.NumericObjects import ForceNumericBounds
from daCore.NumericObjects import ApplyBounds
from daCore.PlatformInfo import PlatformInfo
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
def cekf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    Contrained Extended Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.array(Y).size
    #
    # Précalcul des inversions de B et R
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    #
    __n = Xb.size
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        Xn = Xb
        Pn = B
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B,"asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
        Pn = selfA._getInternalState("Pn")
    #
    if selfA._parameters["EstimationOf"] == "Parameters":
        XaMin            = Xn
        previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        #
        Ht = HO["Tangent"].asMatrix(ValueForMethodForm = Xn)
        Ht = Ht.reshape(Ynpu.size,Xn.size) # ADAO & check shape
        Ha = HO["Adjoint"].asMatrix(ValueForMethodForm = Xn)
        Ha = Ha.reshape(Xn.size,Ynpu.size) # ADAO & check shape
        #
        if selfA._parameters["EstimationOf"] == "State":
            Mt = EM["Tangent"].asMatrix(ValueForMethodForm = Xn)
            Mt = Mt.reshape(Xn.size,Xn.size) # ADAO & check shape
            Ma = EM["Adjoint"].asMatrix(ValueForMethodForm = Xn)
            Ma = Ma.reshape(Xn.size,Xn.size) # ADAO & check shape
        #
        if U is not None:
            if hasattr(U,"store") and len(U)>1:
                Un = numpy.ravel( U[step] ).reshape((-1,1))
            elif hasattr(U,"store") and len(U)==1:
                Un = numpy.ravel( U[0] ).reshape((-1,1))
            else:
                Un = numpy.ravel( U ).reshape((-1,1))
        else:
            Un = None
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xn = ApplyBounds( Xn, selfA._parameters["Bounds"] )
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            Xn_predicted = numpy.ravel( M( (Xn, Un) ) ).reshape((__n,1))
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
            Pn_predicted = Q + Mt * (Pn * Ma)
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
            Pn_predicted = Pn
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xn_predicted = ApplyBounds( Xn_predicted, selfA._parameters["Bounds"] )
        #
        if selfA._parameters["EstimationOf"] == "State":
            HX_predicted = numpy.ravel( H( (Xn_predicted, None) ) ).reshape((__p,1))
            _Innovation  = Ynpu - HX_predicted
        elif selfA._parameters["EstimationOf"] == "Parameters":
            HX_predicted = numpy.ravel( H( (Xn_predicted, Un) ) ).reshape((__p,1))
            _Innovation  = Ynpu - HX_predicted
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                _Innovation = _Innovation - Cm @ Un
        #
        Kn = Pn_predicted * Ha * numpy.linalg.inv(R + numpy.dot(Ht, Pn_predicted * Ha))
        Xn = Xn_predicted + Kn * _Innovation
        Pn = Pn_predicted - Kn * Ht * Pn_predicted
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xn = ApplyBounds( Xn, selfA._parameters["Bounds"] )
        #
        Xa = Xn # Pointeurs
        #--------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("Pn", Pn)
        #--------------------------
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( H((Xa, Un)) )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( Xn_predicted )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( Pn_predicted )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( Xn_predicted - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX_predicted )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T @ (BI @ (Xa - Xb)) )
            Jo  = float( 0.5 * _Innovation.T @ (RI @ _Innovation) )
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
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
