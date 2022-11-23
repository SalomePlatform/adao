# -*- coding: utf-8 -*-

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
    EIM
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy

# ==============================================================================
def EIM_offline(selfA, Verbose = False):
    """
    Établissement de base par Empirical Interpolation Method (EIM)
    """
    #
    # Initialisations
    # ---------------
    if isinstance(selfA._parameters["EnsembleOfSnapshots"], (numpy.ndarray,numpy.matrix)):
        __EOS = numpy.asarray(selfA._parameters["EnsembleOfSnapshots"])
    elif isinstance(selfA._parameters["EnsembleOfSnapshots"], (list,tuple)):
        __EOS = numpy.asarray(selfA._parameters["EnsembleOfSnapshots"]).T
    else:
        raise ValueError("EnsembleOfSnapshots has to be an array/matrix (each column being a vector) or a list/tuple (each element being a vector).")
    #
    if   selfA._parameters["ErrorNorm"] == "L2":
        MaxNormByColumn = MaxL2NormByColumn
    else:
        MaxNormByColumn = MaxLinfNormByColumn
    #
    if selfA._parameters["Variant"] == "PositioningByEIM":
        __LcCsts = False
    else:
        __LcCsts = True
    if __LcCsts and "ExcludeLocations" in selfA._parameters:
        __ExcludedMagicPoints = selfA._parameters["ExcludeLocations"]
    else:
        __ExcludedMagicPoints = []
    if __LcCsts and len(__ExcludedMagicPoints) > 0:
        __ExcludedMagicPoints = numpy.ravel(numpy.asarray(__ExcludedMagicPoints, dtype=int))
        __IncludedMagicPoints = numpy.setdiff1d(
            numpy.arange(__EOS.shape[0]),
            __ExcludedMagicPoints,
            assume_unique = True,
            )
    else:
        __IncludedMagicPoints = []
    #
    __dimS, __nbmS = __EOS.shape
    if "MaximumNumberOfLocations" in selfA._parameters and "MaximumRBSize" in selfA._parameters:
        selfA._parameters["MaximumRBSize"] = min(selfA._parameters["MaximumNumberOfLocations"],selfA._parameters["MaximumRBSize"])
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
    __mu     = []
    __I      = []
    __Q      = numpy.empty(__dimS)
    __errors = []
    #
    __M      = 0
    __iM     = -1
    __rhoM   = numpy.empty(__dimS)
    #
    __eM, __muM = MaxNormByColumn(__EOS, __LcCsts, __IncludedMagicPoints)
    __residuM = __EOS[:,__muM]
    __errors.append(__eM)
    #
    # Boucle
    # ------
    while __M < __maxM and __eM > selfA._parameters["EpsilonEIM"]:
        __M = __M + 1
        #
        __mu.append(__muM)
        #
        # Détermination du point et de la fonction magiques
        __abs_residuM = numpy.abs(__residuM)
        __iM   = numpy.argmax(__abs_residuM)
        __rhoM = __residuM / __abs_residuM[__iM]
        #
        if __LcCsts and __iM in __ExcludedMagicPoints:
            __sIndices = numpy.argsort(__abs_residuM)
            __rang = -1
            assert __iM == __sIndices[__rang]
            while __iM in __ExcludedMagicPoints and __rang >= -len(__abs_residuM):
                __rang = __rang - 1
                __iM   = __sIndices[__rang]
        #
        if __M > 1:
            __Q = numpy.column_stack((__Q, __rhoM))
        else:
            __Q = __rhoM
        __I.append(__iM)
        #
        __restrictedQi = __Q[__I]
        if __M > 1:
            __Qi_inv = numpy.linalg.inv(__restrictedQi)
        else:
            __Qi_inv = 1. / __restrictedQi
        #
        __restrictedEOSi = __EOS[__I]
        #
        __interpolator = numpy.empty(__EOS.shape)
        if __M > 1:
            __interpolator = numpy.dot(__Q,numpy.dot(__Qi_inv,__restrictedEOSi))
        else:
            __interpolator = numpy.outer(__Q,numpy.outer(__Qi_inv,__restrictedEOSi))
        #
        __dataForNextIter = __EOS - __interpolator
        __eM, __muM = MaxNormByColumn(__dataForNextIter, __LcCsts, __IncludedMagicPoints)
        __errors.append(__eM)
        #
        __residuM = __dataForNextIter[:,__muM]
    #
    #--------------------------
    if hasattr(selfA, "StoredVariables"):
        selfA.StoredVariables["OptimalPoints"].store( __I )
        if selfA._toStore("ReducedBasis"):
            selfA.StoredVariables["ReducedBasis"].store( __Q )
        if selfA._toStore("Residus"):
            selfA.StoredVariables["Residus"].store( __errors )
    #
    return __mu, __I, __Q, __errors

# ==============================================================================
def EIM_online(selfA, QEIM, mu, iEIM):
    raise NotImplementedError()

# ==============================================================================
def MaxL2NormByColumn(Ensemble, LcCsts = False, IncludedPoints = []):
    nmax, imax = -1, -1
    if LcCsts and len(IncludedPoints) > 0:
        for indice in range(Ensemble.shape[1]):
            norme = numpy.linalg.norm(
                numpy.take(Ensemble[:,indice], IncludedPoints, mode='clip'),
                )
            if norme > nmax:
                nmax, imax, = norme, indice
    else:
        for indice in range(Ensemble.shape[1]):
            norme = numpy.linalg.norm(
                Ensemble[:,indice],
                )
            if norme > nmax:
                nmax, imax, = norme, indice
    return nmax, imax

def MaxLinfNormByColumn(Ensemble, LcCsts = False, IncludedPoints = []):
    nmax, imax = -1, -1
    if LcCsts and len(IncludedPoints) > 0:
        for indice in range(Ensemble.shape[1]):
            norme = numpy.linalg.norm(
                numpy.take(Ensemble[:,indice], IncludedPoints, mode='clip'),
                ord=numpy.inf,
                )
            if norme > nmax:
                nmax, imax, = norme, indice
    else:
        for indice in range(Ensemble.shape[1]):
            norme = numpy.linalg.norm(
                Ensemble[:,indice],
                ord=numpy.inf,
                )
            if norme > nmax:
                nmax, imax, = norme, indice
    return nmax, imax

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
