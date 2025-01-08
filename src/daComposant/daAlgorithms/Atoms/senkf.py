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
    Stochastic EnKF
"""
__author__ = "Jean-Philippe ARGAUD"

import math, numpy
from daCore.NumericObjects import Apply3DVarRecentringOnEnsemble
from daCore.NumericObjects import CovarianceInflation
from daCore.NumericObjects import EnsembleErrorCovariance
from daCore.NumericObjects import EnsembleMean
from daCore.NumericObjects import EnsembleOfAnomalies
from daCore.NumericObjects import EnsembleOfBackgroundPerturbations
from daCore.NumericObjects import EnsembleOfCenteredPerturbations
from daCore.NumericObjects import EnsemblePerturbationWithGivenCovariance
from daCore.PlatformInfo import PlatformInfo, vfloat
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
def senkf( selfA, Xb, Y, U, HO, EM, CM, R, B, Q,
           VariantM="KalmanFilterFormula16",
           Hybrid=None,
           ):
    """
    Stochastic EnKF
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
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None
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
    if hasattr(R, "asfullmatrix"):
        Rn = R.asfullmatrix(__p)
    else:
        Rn = R
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
        if selfA._parameters["EstimationOf"] == "State":  # Forecast + Q and observation of forecast
            EMX = M( [(Xn[:, i], Un) for i in range(__m)],
                     argsAsSerie = True,
                     returnSerieAsArrayMatrix = True )
            Xn_predicted = EnsemblePerturbationWithGivenCovariance( EMX, Q )
            HX_predicted = H( [(Xn_predicted[:, i], None) for i in range(__m)],
                              argsAsSerie = True,
                              returnSerieAsArrayMatrix = True )
            if Cm is not None and Un is not None:  # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n, Un.size)  # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm @ Un
        elif selfA._parameters["EstimationOf"] == "Parameters":  # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = EMX = Xn
            HX_predicted = H( [(Xn_predicted[:, i], Un) for i in range(__m)],
                              argsAsSerie = True,
                              returnSerieAsArrayMatrix = True )
        #
        # Mean of forecast and observation of forecast
        Xfm  = EnsembleMean( Xn_predicted )
        Hfm  = EnsembleMean( HX_predicted )
        #
        # --------------------------
        if VariantM == "KalmanFilterFormula05":
            PfHT, HPfHT = 0., 0.
            for i in range(__m):
                Exfi = Xn_predicted[:, i].reshape((__n, 1)) - Xfm
                Eyfi = HX_predicted[:, i].reshape((__p, 1)) - Hfm
                PfHT  += Exfi * Eyfi.T
                HPfHT += Eyfi * Eyfi.T
            PfHT  = (1. / (__m - 1)) * PfHT
            HPfHT = (1. / (__m - 1)) * HPfHT
            Kn     = PfHT * ( R + HPfHT ).I
            del PfHT, HPfHT
            #
            for i in range(__m):
                ri = numpy.random.multivariate_normal(numpy.zeros(__p), Rn)
                Xn[:, i] = numpy.ravel(Xn_predicted[:, i]) + Kn @ (numpy.ravel(Ynpu) + ri - HX_predicted[:, i])
        # --------------------------
        elif VariantM == "KalmanFilterFormula16":
            EpY   = EnsembleOfCenteredPerturbations(Ynpu, Rn, __m)
            EpYm  = EpY.mean(axis=1, dtype=mfp).astype('float').reshape((__p, 1))
            #
            EaX   = EnsembleOfAnomalies( Xn_predicted ) / math.sqrt(__m - 1)
            EaY = (HX_predicted - Hfm - EpY + EpYm) / math.sqrt(__m - 1)
            #
            Kn = EaX @ EaY.T @ numpy.linalg.inv( EaY @ EaY.T)
            #
            for i in range(__m):
                Xn[:, i] = numpy.ravel(Xn_predicted[:, i]) + Kn @ (numpy.ravel(EpY[:, i]) - HX_predicted[:, i])
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
        if Hybrid == "E3DVAR":
            Xn = Apply3DVarRecentringOnEnsemble(Xn, EMX, Ynpu, HO, R, B, selfA._parameters)
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
            _HXa = numpy.ravel( H((Xa, None)) ).reshape((-1, 1))
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
            selfA.StoredVariables["ForecastState"].store( EMX )
        if selfA._toStore("ForecastCovariance"):
            selfA.StoredVariables["ForecastCovariance"].store( EnsembleErrorCovariance(EMX) )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( EMX - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HX_predicted + Ynpu )
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
