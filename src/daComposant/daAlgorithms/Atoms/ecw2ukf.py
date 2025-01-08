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
    Constrained Unscented Kalman Filter
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, scipy, copy
from daCore.NumericObjects import GenerateWeightsAndSigmaPoints
from daCore.PlatformInfo import PlatformInfo, vfloat
from daCore.NumericObjects import ApplyBounds, ForceNumericBounds
mpr = PlatformInfo().MachinePrecision()

# ==============================================================================
def ecw2ukf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="UKF"):
    """
    Constrained Unscented Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    selfA._parameters["Bounds"] = ForceNumericBounds( selfA._parameters["Bounds"] )
    #
    wsp = GenerateWeightsAndSigmaPoints(
        Nn       = Xb.size,
        EO       = selfA._parameters["EstimationOf"],
        VariantM = VariantM,
        Alpha    = selfA._parameters["Alpha"],
        Beta     = selfA._parameters["Beta"],
        Kappa    = selfA._parameters["Kappa"],
    )
    Wm, Wc, SC = wsp.get()
    #
    # Durée d'observation et tailles
    if hasattr(Y, "stepnumber"):
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
    if len(selfA.StoredVariables["Analysis"]) == 0 or not selfA._parameters["nextStep"]:
        Xn = Xb
        if hasattr(B, "asfullmatrix"):
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
    for step in range(duration - 1):
        #
        if U is not None:
            if hasattr(U, "store") and len(U) > 1:
                Un = numpy.ravel( U[step] ).reshape((-1, 1))
            elif hasattr(U, "store") and len(U) == 1:
                Un = numpy.ravel( U[0] ).reshape((-1, 1))
            else:
                Un = numpy.ravel( U ).reshape((-1, 1))
        else:
            Un = None
        #
        if CM is not None and "Tangent" in CM and U is not None:
            Cm = CM["Tangent"].asMatrix(Xn)
        else:
            Cm = None
        #
        Pndemi = numpy.real(scipy.linalg.sqrtm(Pn))
        Xnmu = Xn + Pndemi @ SC
        nbSpts = SC.shape[1]
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            for point in range(nbSpts):
                Xnmu[:, point] = ApplyBounds( Xnmu[:, point], selfA._parameters["Bounds"] )
        #
        if selfA._parameters["EstimationOf"] == "State":
            Mm = EM["Direct"].appliedControledFormTo
            XEnnmu = Mm( [(Xnmu[:, point].reshape((-1, 1)), Un) for point in range(nbSpts)],
                         argsAsSerie = True,
                         returnSerieAsArrayMatrix = True )
            if Cm is not None and Un is not None:  # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n, Un.size)  # ADAO & check shape
                XEnnmu = XEnnmu + Cm @ Un
        elif selfA._parameters["EstimationOf"] == "Parameters":
            # --- > Par principe, M = Id, Q = 0
            XEnnmu = numpy.array( Xnmu )
        #
        Xhmn = ( XEnnmu * Wm ).sum(axis=1)
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xhmn = ApplyBounds( Xhmn, selfA._parameters["Bounds"] )
        #
        if selfA._parameters["EstimationOf"] == "State":
            Pmn = copy.copy(Q)
        elif selfA._parameters["EstimationOf"] == "Parameters":
            Pmn = 0.
        for point in range(nbSpts):
            dXEnnmuXhmn = XEnnmu[:, point].flat - Xhmn
            Pmn += Wc[point] * numpy.outer(dXEnnmuXhmn, dXEnnmuXhmn)
        #
        if selfA._parameters["EstimationOf"] == "Parameters" and selfA._parameters["Bounds"] is not None:
            Pmndemi = selfA._parameters["Reconditioner"] * numpy.real(scipy.linalg.sqrtm(Pmn))
        else:
            Pmndemi = numpy.real(scipy.linalg.sqrtm(Pmn))
        #
        Xnnmu = Xhmn.reshape((-1, 1)) + Pmndemi @ SC
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            for point in range(nbSpts):
                Xnnmu[:, point] = ApplyBounds( Xnnmu[:, point], selfA._parameters["Bounds"] )
        #
        Hm = HO["Direct"].appliedControledFormTo
        Ynnmu = Hm( [(Xnnmu[:, point], None) for point in range(nbSpts)],
                    argsAsSerie = True,
                    returnSerieAsArrayMatrix = True )
        #
        Yhmn = ( Ynnmu * Wm ).sum(axis=1)
        #
        Pyyn = copy.copy(R)
        Pxyn = 0.
        for point in range(nbSpts):
            dYnnmuYhmn = Ynnmu[:, point].flat - Yhmn
            dXnnmuXhmn = Xnnmu[:, point].flat - Xhmn
            Pyyn += Wc[point] * numpy.outer(dYnnmuYhmn, dYnnmuYhmn)
            Pxyn += Wc[point] * numpy.outer(dXnnmuXhmn, dYnnmuYhmn)
        #
        if hasattr(Y, "store"):
            Ynpu = numpy.ravel( Y[step + 1] ).reshape((__p, 1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p, 1))
        _Innovation  = Ynpu - Yhmn.reshape((-1, 1))
        if selfA._parameters["EstimationOf"] == "Parameters":
            if Cm is not None and Un is not None:  # Attention : si Cm est aussi dans H, doublon !
                _Innovation = _Innovation - Cm @ Un
        #
        Kn = Pxyn @ scipy.linalg.inv(Pyyn)
        Xn = Xhmn.reshape((-1, 1)) + Kn @ _Innovation
        Pn = Pmn - Kn @ (Pyyn @ Kn.T)
        #
        if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
            Xn = ApplyBounds( Xn, selfA._parameters["Bounds"] )
        #
        Xa = Xn  # Pointeurs
        # --------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("Pn", Pn)
        # --------------------------
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( Hm((Xa, None)) )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
                or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( Xhmn )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( Pmn )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( Xhmn - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( Yhmn )
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
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )  # noqa: E501
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )  # noqa: E501
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )  # noqa: E501
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )  # noqa: E501
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
