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
    Empirical Interpolation Method DEIM & lcDEIM
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, scipy, logging
import daCore.Persistence
from daCore.NumericObjects import FindIndexesFromNames
from daCore.NumericObjects import InterpolationErrorByColumn
from daCore.NumericObjects import SingularValuesEstimation
from daCore.PlatformInfo import vt

# ==============================================================================
def DEIM_offline(selfA, EOS = None, Verbose = False):
    """
    Établissement de la base
    """
    #
    # Initialisations
    # ---------------
    if numpy.array(EOS).size == 0:
        raise ValueError("EnsembleOfSnapshots has not to be void, but an array/matrix (each column being a vector) or a list/tuple (each element being a vector).")  # noqa: E501
    if isinstance(EOS, (numpy.ndarray, numpy.matrix)):
        __EOS = numpy.asarray(EOS)
    elif isinstance(EOS, (list, tuple, daCore.Persistence.Persistence)):
        __EOS = numpy.stack([numpy.ravel(_sn) for _sn in EOS], axis=1)
    else:
        raise ValueError("EnsembleOfSnapshots has to be an array/matrix (each column being a vector) or a list/tuple (each element being a vector).")  # noqa: E501
    __dimS, __nbmS = __EOS.shape
    logging.debug("%s Using a collection of %i snapshots of individual size of %i"%(selfA._name, __nbmS, __dimS))
    #
    if selfA._parameters["Variant"] in ["DEIM", "PositioningByDEIM"]:
        __LcCsts = False
    else:
        __LcCsts = True
    if __LcCsts and "ExcludeLocations" in selfA._parameters:
        __ExcludedMagicPoints = selfA._parameters["ExcludeLocations"]
    else:
        __ExcludedMagicPoints = ()
    if __LcCsts and "NameOfLocations" in selfA._parameters:
        if isinstance(selfA._parameters["NameOfLocations"], (list, numpy.ndarray, tuple)) and len(selfA._parameters["NameOfLocations"]) == __dimS:  # noqa: E501
            __NameOfLocations = selfA._parameters["NameOfLocations"]
        else:
            __NameOfLocations = ()
    else:
        __NameOfLocations = ()
    if __LcCsts and len(__ExcludedMagicPoints) > 0:
        __ExcludedMagicPoints = FindIndexesFromNames( __NameOfLocations, __ExcludedMagicPoints )
        __ExcludedMagicPoints = numpy.ravel(numpy.asarray(__ExcludedMagicPoints, dtype=int))
        __IncludedMagicPoints = numpy.setdiff1d(
            numpy.arange(__EOS.shape[0]),
            __ExcludedMagicPoints,
            assume_unique = True,
        )
    else:
        __IncludedMagicPoints = []
    #
    if "MaximumNumberOfLocations" in selfA._parameters and "MaximumRBSize" in selfA._parameters:
        selfA._parameters["MaximumRBSize"] = min(selfA._parameters["MaximumNumberOfLocations"], selfA._parameters["MaximumRBSize"])  # noqa: E501
    elif "MaximumNumberOfLocations" in selfA._parameters:
        selfA._parameters["MaximumRBSize"] = selfA._parameters["MaximumNumberOfLocations"]
    elif "MaximumRBSize" in selfA._parameters:
        pass
    else:
        selfA._parameters["MaximumRBSize"] = __nbmS
    __maxM   = min(selfA._parameters["MaximumRBSize"], __dimS, __nbmS)
    if "ErrorNormTolerance" in selfA._parameters:
        selfA._parameters["EpsilonEIM"] = selfA._parameters["ErrorNormTolerance"]
    else:
        selfA._parameters["EpsilonEIM"] = 1.e-2
    #
    __sv, __svsq, __tisv, __qisv = SingularValuesEstimation( __EOS )
    if vt(scipy.version.version) < vt("1.1.0"):
        __rhoM = scipy.linalg.orth( __EOS )
        __rhoM = numpy.compress(__sv > selfA._parameters["EpsilonEIM"] * max(__sv), __rhoM, axis=1)
    else:
        __rhoM = scipy.linalg.orth( __EOS, selfA._parameters["EpsilonEIM"] )
    __lVs, __svdM = __rhoM.shape
    assert __lVs == __dimS, "Différence entre lVs et dim(EOS)"
    __maxM   = min(__maxM, __svdM)
    #
    if __LcCsts and len(__IncludedMagicPoints) > 0:
        __iM = numpy.argmax( numpy.abs(
            numpy.take(__rhoM[:, 0], __IncludedMagicPoints, mode='clip')
        ))
    else:
        __iM = numpy.argmax( numpy.abs(
            __rhoM[:, 0]
        ))
    #
    __mu     = [None,]  # Convention
    __I      = [__iM,]
    __Q      = __rhoM[:, 0].reshape((-1, 1))
    __errors = []
    #
    __M      = 1  # Car le premier est déjà construit
    if selfA._toStore("Residus"):
        __eM, _ = InterpolationErrorByColumn(
            __EOS, __Q, __I, __M,
            __ErrorNorm = selfA._parameters["ErrorNorm"],
            __LcCsts = __LcCsts, __IncludedPoints = __IncludedMagicPoints)
        __errors.append(__eM)
    #
    # Boucle
    # ------
    while __M < __maxM:
        #
        __restrictedQi = __Q[__I, :]
        if __M > 1:
            __Qi_inv = numpy.linalg.inv(__restrictedQi)
        else:
            __Qi_inv = 1. / __restrictedQi
        #
        __restrictedrhoMi = __rhoM[__I, __M].reshape((-1, 1))
        #
        if __M > 1:
            __interpolator = numpy.dot(__Q, numpy.dot(__Qi_inv, __restrictedrhoMi))
        else:
            __interpolator = numpy.outer(__Q, numpy.outer(__Qi_inv, __restrictedrhoMi))
        #
        __residuM = __rhoM[:, __M].reshape((-1, 1)) - __interpolator
        #
        if __LcCsts and len(__IncludedMagicPoints) > 0:
            __iM = numpy.argmax( numpy.abs(
                numpy.take(__residuM, __IncludedMagicPoints, mode='clip')
            ))
        else:
            __iM = numpy.argmax( numpy.abs(
                __residuM
            ))
        __Q = numpy.column_stack((__Q, __rhoM[:, __M]))
        #
        __I.append(__iM)
        __mu.append(None)  # Convention
        if selfA._toStore("Residus"):
            __eM, _ = InterpolationErrorByColumn(
                __EOS, __Q, __I, __M + 1,
                __ErrorNorm = selfA._parameters["ErrorNorm"],
                __LcCsts = __LcCsts, __IncludedPoints = __IncludedMagicPoints)
            __errors.append(__eM)
        #
        __M = __M + 1
    #
    # --------------------------
    __mu = numpy.array(__mu)
    __I = numpy.array(__I)
    __errors = numpy.array(__errors)
    # --------------------------
    if len(__errors) > 0 and __errors[-1] < selfA._parameters["EpsilonEIM"]:
        logging.debug("%s %s (%.1e)"%(selfA._name, "The convergence is obtained when reaching the required EIM tolerance", selfA._parameters["EpsilonEIM"]))  # noqa: E501
    if __M >= __maxM:
        logging.debug("%s %s (%i)"%(selfA._name, "The convergence is obtained when reaching the maximum number of RB dimension", __maxM))  # noqa: E501
    logging.debug("%s The RB of size %i has been correctly build"%(selfA._name, __Q.shape[1]))
    logging.debug("%s There are %i points that have been excluded from the potential optimal points"%(selfA._name, len(__ExcludedMagicPoints)))  # noqa: E501
    if hasattr(selfA, "StoredVariables"):
        selfA.StoredVariables["OptimalPoints"].store( __I )
        if selfA._toStore("ReducedBasisMus"):
            selfA.StoredVariables["ReducedBasisMus"].store( __mu )
        if selfA._toStore("ReducedBasis"):
            selfA.StoredVariables["ReducedBasis"].store( __Q )
        if selfA._toStore("Residus"):
            selfA.StoredVariables["Residus"].store( __errors )
        if selfA._toStore("ExcludedPoints"):
            selfA.StoredVariables["ExcludedPoints"].store( __ExcludedMagicPoints )
        if selfA._toStore("SingularValues"):
            selfA.StoredVariables["SingularValues"].store( __sv )
    #
    return __mu, __I, __Q, __errors

# ==============================================================================
# DEIM_online == EIM_online
# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
