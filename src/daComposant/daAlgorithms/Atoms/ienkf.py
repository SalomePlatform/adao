# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2024 EDF R&D
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
    Iterative Ensemble Kalman Filter
"""
__author__ = "Jean-Philippe ARGAUD"

import math, numpy, scipy, scipy.optimize, scipy.version
from daCore.NumericObjects import CovarianceInflation
from daCore.NumericObjects import EnsembleErrorCovariance
from daCore.NumericObjects import EnsembleMean
from daCore.NumericObjects import EnsembleOfAnomalies
from daCore.NumericObjects import EnsembleOfBackgroundPerturbations
from daCore.PlatformInfo import PlatformInfo, vfloat
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
def ienkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="IEnKF12",
          BnotT=False, _epsilon=1.e-3, _e=1.e-7, _jmax=15000):
    """
    Iterative Ensemble Kalman Filter
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedControledFormTo
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
    __m = selfA._parameters["NumberOfMembers"]
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    previousJMinimum = numpy.finfo(float).max
    #
    if len(selfA.StoredVariables["Analysis"]) == 0 or not selfA._parameters["nextStep"]:
        if hasattr(B, "asfullmatrix"):
            Pn = B.asfullmatrix(__n)
        else:
            Pn = B
        Xn = EnsembleOfBackgroundPerturbations( Xb, Pn, __m )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        selfA._setInternalState("seed", numpy.random.get_state())
    elif selfA._parameters["nextStep"]:
        Xn = selfA._getInternalState("Xn")
    #
    for step in range(duration - 1):
        numpy.random.set_state(selfA._getInternalState("seed"))
        if hasattr(Y, "store"):
            Ynpu = numpy.ravel( Y[step + 1] ).reshape((__p, 1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p, 1))
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
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation(
                Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
            )
        #
        # --------------------------
        if VariantM == "IEnKF12":
            Xfm = numpy.ravel(Xn.mean(axis=1, dtype=mfp).astype('float'))
            EaX = EnsembleOfAnomalies( Xn ) / math.sqrt(__m - 1)
            __j = 0
            Deltaw = 1
            if not BnotT:
                Ta  = numpy.identity(__m)
            vw  = numpy.zeros(__m)
            while numpy.linalg.norm(Deltaw) >= _e and __j <= _jmax:
                vx1 = (Xfm + EaX @ vw).reshape((__n, 1))
                #
                if BnotT:
                    E1 = vx1 + _epsilon * EaX
                else:
                    E1 = vx1 + math.sqrt(__m - 1) * EaX @ Ta
                #
                if selfA._parameters["EstimationOf"] == "State":  # Forecast + Q
                    E2 = M( [(E1[:, i, numpy.newaxis], Un) for i in range(__m)],
                            argsAsSerie = True,
                            returnSerieAsArrayMatrix = True )
                elif selfA._parameters["EstimationOf"] == "Parameters":
                    # --- > Par principe, M = Id
                    E2 = Xn
                vx2 = E2.mean(axis=1, dtype=mfp).astype('float').reshape((__n, 1))
                vy1 = H((vx2, Un)).reshape((__p, 1))
                #
                HE2 = H( [(E2[:, i, numpy.newaxis], Un) for i in range(__m)],
                         argsAsSerie = True,
                         returnSerieAsArrayMatrix = True )
                vy2 = HE2.mean(axis=1, dtype=mfp).astype('float').reshape((__p, 1))
                #
                if BnotT:
                    EaY = (HE2 - vy2) / _epsilon
                else:
                    EaY = ( (HE2 - vy2) @ numpy.linalg.inv(Ta) ) / math.sqrt(__m - 1)
                #
                GradJ = numpy.ravel(vw[:, None] - EaY.transpose() @ (RI * ( Ynpu - vy1 )))
                mH = numpy.identity(__m) + EaY.transpose() @ (RI * EaY).reshape((-1, __m))
                Deltaw = - numpy.linalg.solve(mH, GradJ)
                #
                vw = vw + Deltaw
                #
                if not BnotT:
                    Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
                #
                __j = __j + 1
            #
            A2 = EnsembleOfAnomalies( E2 )
            #
            if BnotT:
                Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
                A2 = math.sqrt(__m - 1) * A2 @ Ta / _epsilon
            #
            Xn = vx2 + A2
        # --------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation(
                Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
            )
        #
        Xa = EnsembleMean( Xn )
        # --------------------------
        selfA._setInternalState("Xn", Xn)
        selfA._setInternalState("seed", numpy.random.get_state())
        # --------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
                or selfA._toStore("CostFunctionJ") \
                or selfA._toStore("CostFunctionJb") \
                or selfA._toStore("CostFunctionJo") \
                or selfA._toStore("APosterioriCovariance") \
                or selfA._toStore("InnovationAtCurrentAnalysis") \
                or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.ravel( H((Xa, Un)) ).reshape((-1, 1))
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
                or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( E2 )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( EnsembleErrorCovariance(E2) )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( E2 - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HE2 + Ynpu )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HE2 )
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
            selfA.StoredVariables["APosterioriCovariance"].store( EnsembleErrorCovariance(Xn) )
        if selfA._parameters["EstimationOf"] == "Parameters" \
                and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = selfA.StoredVariables["APosterioriCovariance"][-1]
        # ---> Pour les smoothers
        if selfA._toStore("CurrentEnsembleState"):
            selfA.StoredVariables["CurrentEnsembleState"].store( Xn )
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
