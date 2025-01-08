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
    Ensemble Kalman Smoother
"""
__author__ = "Jean-Philippe ARGAUD"

import copy, math, numpy, scipy, scipy.optimize, scipy.version
from daCore.NumericObjects import EnsembleErrorCovariance
from daCore.NumericObjects import EnsembleOfAnomalies
from daCore.NumericObjects import EnsembleOfBackgroundPerturbations
from daCore.NumericObjects import EnsemblePerturbationWithGivenCovariance
from daAlgorithms.Atoms import etkf
from daCore.PlatformInfo import PlatformInfo
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
def enks(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="EnKS16-KalmanFilterFormula"):
    """
    Ensemble Kalman Smoother
    """
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
    # Précalcul des inversions de B et R
    RIdemi = R.sqrtmI()
    #
    # Durée d'observation et tailles
    LagL = selfA._parameters["SmootherLagL"]
    if (not hasattr(Y, "store")) or (not hasattr(Y, "stepnumber")):
        raise ValueError("Fixed-lag smoother requires a series of observation")
    if Y.stepnumber() < LagL:
        raise ValueError("Fixed-lag smoother requires a series of observation greater then the lag L")
    duration = Y.stepnumber()
    __p = numpy.cumprod(Y.shape())[-1]
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    #
    if len(selfA.StoredVariables["Analysis"]) == 0 or not selfA._parameters["nextStep"]:
        selfA.StoredVariables["Analysis"].store( Xb )
        if selfA._toStore("APosterioriCovariance"):
            if hasattr(B, "asfullmatrix"):
                selfA.StoredVariables["APosterioriCovariance"].store( B.asfullmatrix(__n) )
            else:
                selfA.StoredVariables["APosterioriCovariance"].store( B )
    #
    # Calcul direct initial (on privilégie la mémorisation au recalcul)
    __seed = numpy.random.get_state()
    selfB = copy.deepcopy(selfA)
    selfB._parameters["StoreSupplementaryCalculations"] = ["CurrentEnsembleState"]
    if VariantM == "EnKS16-KalmanFilterFormula":
        etkf.etkf(selfB, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM = "KalmanFilterFormula")
    else:
        raise ValueError("VariantM has to be chosen in the authorized methods list.")
    if LagL > 0:
        EL  = selfB.StoredVariables["CurrentEnsembleState"][LagL - 1]
    else:
        EL = EnsembleOfBackgroundPerturbations( Xb, None, __m )  # Cf. etkf
    selfA._parameters["SetSeed"] = numpy.random.set_state(__seed)
    #
    for step in range(LagL, duration - 1):
        #
        sEL = selfB.StoredVariables["CurrentEnsembleState"][step + 1 - LagL:step + 1]
        sEL.append(None)
        #
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
        # --------------------------
        if VariantM == "EnKS16-KalmanFilterFormula":
            if selfA._parameters["EstimationOf"] == "State":  # Forecast
                EL = M( [(EL[:, i], Un) for i in range(__m)],
                        argsAsSerie = True,
                        returnSerieAsArrayMatrix = True )
                EL = EnsemblePerturbationWithGivenCovariance( EL, Q )
                EZ = H( [(EL[:, i], Un) for i in range(__m)],
                        argsAsSerie = True,
                        returnSerieAsArrayMatrix = True )
                if Cm is not None and Un is not None:  # Attention : si Cm est aussi dans M, doublon !
                    Cm = Cm.reshape(__n, Un.size)  # ADAO & check shape
                    EZ = EZ + Cm @ Un
            elif selfA._parameters["EstimationOf"] == "Parameters":
                # --- > Par principe, M = Id, Q = 0
                EZ = H( [(EL[:, i], Un) for i in range(__m)],
                        argsAsSerie = True,
                        returnSerieAsArrayMatrix = True )
            #
            vEm   = EL.mean(axis=1, dtype=mfp).astype('float').reshape((__n, 1))
            vZm   = EZ.mean(axis=1, dtype=mfp).astype('float').reshape((__p, 1))
            #
            mS    = RIdemi @ EnsembleOfAnomalies( EZ, vZm, 1. / math.sqrt(__m - 1) )
            mS    = mS.reshape((-1, __m))  # Pour dimension 1
            delta = RIdemi @ ( Ynpu - vZm )
            mT    = numpy.linalg.inv( numpy.identity(__m) + mS.T @ mS )
            vw    = mT @ mS.T @ delta
            #
            Tdemi = numpy.real(scipy.linalg.sqrtm(mT))
            mU    = numpy.identity(__m)
            wTU   = (vw.reshape((__m, 1)) + math.sqrt(__m - 1) * Tdemi @ mU)
            #
            EX    = EnsembleOfAnomalies( EL, vEm, 1. / math.sqrt(__m - 1) )
            EL    = vEm + EX @ wTU
            #
            sEL[LagL] = EL
            for irl in range(LagL):  # Lissage des L précédentes analysis
                vEm = sEL[irl].mean(axis=1, dtype=mfp).astype('float').reshape((__n, 1))
                EX = EnsembleOfAnomalies( sEL[irl], vEm, 1. / math.sqrt(__m - 1) )
                sEL[irl] = vEm + EX @ wTU
            #
            # Conservation de l'analyse retrospective d'ordre 0 avant rotation
            Xa = sEL[0].mean(axis=1, dtype=mfp).astype('float').reshape((__n, 1))
            if selfA._toStore("APosterioriCovariance"):
                EXn = sEL[0]
            #
            for irl in range(LagL):
                sEL[irl] = sEL[irl + 1]
            sEL[LagL] = None
        # --------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( EnsembleErrorCovariance(EXn) )
    #
    # Stockage des dernières analyses incomplètement remises à jour
    for irl in range(LagL):
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        Xa = sEL[irl].mean(axis=1, dtype=mfp).astype('float').reshape((__n, 1))
        selfA.StoredVariables["Analysis"].store( Xa )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
