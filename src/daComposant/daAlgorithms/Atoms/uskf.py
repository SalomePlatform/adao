# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2023 EDF R&D
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
    Unscented Kalman Filter
"""
__author__ = "Jean-Philippe ARGAUD"

import math, numpy, scipy
from daCore.PlatformInfo import PlatformInfo, vfloat
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
def uskf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    Unscented Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    L     = Xb.size
    Alpha = selfA._parameters["Alpha"]
    Beta  = selfA._parameters["Beta"]
    if selfA._parameters["Kappa"] == 0:
        if selfA._parameters["EstimationOf"] == "State":
            Kappa = 0
        elif selfA._parameters["EstimationOf"] == "Parameters":
            Kappa = 3 - L
    else:
        Kappa = selfA._parameters["Kappa"]
    Lambda = float( Alpha**2 ) * ( L + Kappa ) - L
    Gamma  = math.sqrt( L + Lambda )
    #
    Ww = []
    Ww.append( 0. )
    for i in range(2*L):
        Ww.append( 1. / (2.*(L + Lambda)) )
    #
    Wm = numpy.array( Ww )
    Wm[0] = Lambda / (L + Lambda)
    Wc = numpy.array( Ww )
    Wc[0] = Lambda / (L + Lambda) + (1. - Alpha**2 + Beta)
    #
    # Durée d'observation et tailles
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
        __p = numpy.cumprod(Y.shape())[-1]
    else:
        duration = 2
        __p = numpy.size(Y)
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
        if hasattr(B,"asfullmatrix"):
            Pn = B.asfullmatrix(__n)
        else:
            Pn = B
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
        Pn = selfA._getInternalState("Pn")
    #
    if selfA._parameters["EstimationOf"] == "Parameters":
        XaMin            = Xn
        previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
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
        if CM is not None and "Tangent" in CM and U is not None:
            Cm = CM["Tangent"].asMatrix(Xn)
        else:
            Cm = None
        #
        Pndemi = numpy.real(scipy.linalg.sqrtm(Pn))
        Xnp = numpy.hstack([Xn, Xn+Gamma*Pndemi, Xn-Gamma*Pndemi])
        nbSpts = 2*Xn.size+1
        #
        XEtnnp = []
        for point in range(nbSpts):
            if selfA._parameters["EstimationOf"] == "State":
                Mm = EM["Direct"].appliedControledFormTo
                XEtnnpi = numpy.asarray( Mm( (Xnp[:,point], Un) ) ).reshape((-1,1))
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                    Cm = Cm.reshape(Xn.size,Un.size) # ADAO & check shape
                    XEtnnpi = XEtnnpi + Cm @ Un
            elif selfA._parameters["EstimationOf"] == "Parameters":
                # --- > Par principe, M = Id, Q = 0
                XEtnnpi = Xnp[:,point]
            XEtnnp.append( numpy.ravel(XEtnnpi).reshape((-1,1)) )
        XEtnnp = numpy.concatenate( XEtnnp, axis=1 )
        #
        Xncm = ( XEtnnp * Wm ).sum(axis=1)
        #
        if selfA._parameters["EstimationOf"] == "State":        Pnm = Q
        elif selfA._parameters["EstimationOf"] == "Parameters": Pnm = 0.
        for point in range(nbSpts):
            Pnm += Wc[i] * ((XEtnnp[:,point]-Xncm).reshape((-1,1)) * (XEtnnp[:,point]-Xncm))
        #
        Pnmdemi = numpy.real(scipy.linalg.sqrtm(Pnm))
        #
        Xnnp = numpy.hstack([Xncm.reshape((-1,1)), Xncm.reshape((-1,1))+Gamma*Pnmdemi, Xncm.reshape((-1,1))-Gamma*Pnmdemi])
        #
        Hm = HO["Direct"].appliedControledFormTo
        Ynnp = []
        for point in range(nbSpts):
            if selfA._parameters["EstimationOf"] == "State":
                Ynnpi = Hm( (Xnnp[:,point], None) )
            elif selfA._parameters["EstimationOf"] == "Parameters":
                Ynnpi = Hm( (Xnnp[:,point], Un) )
            Ynnp.append( numpy.ravel(Ynnpi).reshape((-1,1)) )
        Ynnp = numpy.concatenate( Ynnp, axis=1 )
        #
        Yncm = ( Ynnp * Wm ).sum(axis=1)
        #
        Pyyn = R
        Pxyn = 0.
        for point in range(nbSpts):
            Pyyn += Wc[i] * ((Ynnp[:,point]-Yncm).reshape((-1,1)) * (Ynnp[:,point]-Yncm))
            Pxyn += Wc[i] * ((Xnnp[:,point]-Xncm).reshape((-1,1)) * (Ynnp[:,point]-Yncm))
        #
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,1))
        _Innovation  = Ynpu - Yncm.reshape((-1,1))
        if selfA._parameters["EstimationOf"] == "Parameters":
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                _Innovation = _Innovation - Cm @ Un
        #
        Kn = Pxyn * Pyyn.I
        Xn = Xncm.reshape((-1,1)) + Kn * _Innovation
        Pn = Pnm - Kn * Pyyn * Kn.T
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
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( Hm((Xa, Un)) )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( Xncm )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( Pnm )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( Xncm - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( Yncm )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = vfloat( 0.5 * (Xa - Xb).T * (BI * (Xa - Xb)) )
            Jo  = vfloat( 0.5 * _Innovation.T * (RI * _Innovation) )
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
