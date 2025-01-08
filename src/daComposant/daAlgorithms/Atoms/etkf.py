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
    Ensemble-Transform Kalman Filter
"""
__author__ = "Jean-Philippe ARGAUD"

import math, numpy, scipy, scipy.optimize, scipy.version
from daCore.NumericObjects import Apply3DVarRecentringOnEnsemble
from daCore.NumericObjects import CovarianceInflation
from daCore.NumericObjects import EnsembleErrorCovariance
from daCore.NumericObjects import EnsembleMean
from daCore.NumericObjects import EnsembleOfAnomalies
from daCore.NumericObjects import EnsembleOfBackgroundPerturbations
from daCore.NumericObjects import EnsemblePerturbationWithGivenCovariance
from daCore.PlatformInfo import vfloat

# ==============================================================================
def etkf( selfA, Xb, Y, U, HO, EM, CM, R, B, Q,
          VariantM="KalmanFilterFormula",
          Hybrid=None,
          ):
    """
    Ensemble-Transform Kalman Filter
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
    elif VariantM != "KalmanFilterFormula":
        RI = R.getI()
    if VariantM == "KalmanFilterFormula":
        RIdemi = R.sqrtmI()
    #
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    nbPreviousSteps  = len(selfA.StoredVariables["Analysis"])
    previousJMinimum = numpy.finfo(float).max
    #
    if len(selfA.StoredVariables["Analysis"]) == 0 or not selfA._parameters["nextStep"]:
        Xn = EnsembleOfBackgroundPerturbations( Xb, None, __m )
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B, "asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
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
        # Anomalies
        EaX   = EnsembleOfAnomalies( Xn_predicted, Xfm )
        EaHX  = EnsembleOfAnomalies( HX_predicted, Hfm)
        #
        # --------------------------
        if VariantM == "KalmanFilterFormula":
            mS    = RIdemi * EaHX / math.sqrt(__m - 1)
            mS    = mS.reshape((-1, __m))  # Pour dimension 1
            delta = RIdemi * ( Ynpu - Hfm )
            mT    = numpy.linalg.inv( numpy.identity(__m) + mS.T @ mS )
            vw    = mT @ mS.T @ delta
            #
            Tdemi = numpy.real(scipy.linalg.sqrtm(mT))
            mU    = numpy.identity(__m)
            #
            EaX   = EaX / math.sqrt(__m - 1)
            Xn    = Xfm + EaX @ ( vw.reshape((__m, 1)) + math.sqrt(__m - 1) * Tdemi @ mU )
        # --------------------------
        elif VariantM == "Variational":
            HXfm = H((Xfm[:, None], Un))  # Eventuellement Hfm

            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p, 1)) - (EaHX @ w).reshape((__p, 1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * (__m - 1) * w.T @ w
                _J  = _Jo + _Jb
                return vfloat(_J)

            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p, 1)) - (EaHX @ w).reshape((__p, 1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = (__m - 1) * w.reshape((__m, 1))
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)

            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
            )
            #
            Hto = EaHX.T @ (RI * EaHX).reshape((-1, __m))
            Htb = (__m - 1) * numpy.identity(__m)
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m - 1) * Pta))  # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw[:, None] + EWa)
        # --------------------------
        elif VariantM == "FiniteSize11":  # Jauge Boc2011
            HXfm = H((Xfm[:, None], Un))  # Eventuellement Hfm

            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p, 1)) - (EaHX @ w).reshape((__p, 1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * __m * math.log(1 + 1 / __m + w.T @ w)
                _J  = _Jo + _Jb
                return vfloat(_J)

            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p, 1)) - (EaHX @ w).reshape((__p, 1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = __m * w.reshape((__m, 1)) / (1 + 1 / __m + w.T @ w)
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)

            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
            )
            #
            Hto = EaHX.T @ (RI * EaHX).reshape((-1, __m))
            Htb = __m * \
                ( (1 + 1 / __m + vw.T @ vw) * numpy.identity(__m) - 2 * vw @ vw.T ) \
                / (1 + 1 / __m + vw.T @ vw)**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m - 1) * Pta))  # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw.reshape((__m, 1)) + EWa)
        # --------------------------
        elif VariantM == "FiniteSize15":  # Jauge Boc2015
            HXfm = H((Xfm[:, None], Un))  # Eventuellement Hfm

            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p, 1)) - (EaHX @ w).reshape((__p, 1))
                _Jo = 0.5 * _A.T * (RI * _A)
                _Jb = 0.5 * (__m + 1) * math.log(1 + 1 / __m + w.T @ w)
                _J  = _Jo + _Jb
                return vfloat(_J)

            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p, 1)) - (EaHX @ w).reshape((__p, 1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = (__m + 1) * w.reshape((__m, 1)) / (1 + 1 / __m + w.T @ w)
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)

            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
            )
            #
            Hto = EaHX.T @ (RI * EaHX).reshape((-1, __m))
            Htb = (__m + 1) * \
                ( (1 + 1 / __m + vw.T @ vw) * numpy.identity(__m) - 2 * vw @ vw.T ) \
                / (1 + 1 / __m + vw.T @ vw)**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m - 1) * Pta))  # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw.reshape((__m, 1)) + EWa)
        # --------------------------
        elif VariantM == "FiniteSize16":  # Jauge Boc2016
            HXfm = H((Xfm[:, None], Un))  # Eventuellement Hfm

            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p, 1)) - (EaHX @ w).reshape((__p, 1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * (__m + 1) * math.log(1 + 1 / __m + w.T @ w / (__m - 1))
                _J  = _Jo + _Jb
                return vfloat(_J)

            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p, 1)) - (EaHX @ w).reshape((__p, 1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = ((__m + 1) / (__m - 1)) * w.reshape((__m, 1)) / (1 + 1 / __m + w.T @ w / (__m - 1))
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)

            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
            )
            #
            Hto = EaHX.T @ (RI * EaHX).reshape((-1, __m))
            Htb = ((__m + 1) / (__m - 1)) * \
                ( (1 + 1 / __m + vw.T @ vw / (__m - 1)) * numpy.identity(__m) - 2 * vw @ vw.T / (__m - 1) ) \
                / (1 + 1 / __m + vw.T @ vw / (__m - 1))**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m - 1) * Pta))  # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw[:, None] + EWa)
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
