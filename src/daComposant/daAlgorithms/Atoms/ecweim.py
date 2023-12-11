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
    Empirical Interpolation Method EIM & lcEIM
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, logging
import daCore.Persistence
from daCore.NumericObjects import FindIndexesFromNames

# ==============================================================================
def EIM_offline(selfA, EOS = None, Verbose = False):
    """
    Établissement de la base
    """
    #
    # Initialisations
    # ---------------
    if isinstance(EOS, (numpy.ndarray, numpy.matrix)):
        __EOS = numpy.asarray(EOS)
    elif isinstance(EOS, (list, tuple, daCore.Persistence.Persistence)):
        __EOS = numpy.stack([numpy.ravel(_sn) for _sn in EOS], axis=1)
        # __EOS = numpy.asarray(EOS).T
    else:
        raise ValueError("EnsembleOfSnapshots has to be an array/matrix (each column being a vector) or a list/tuple (each element being a vector).")
    __dimS, __nbmS = __EOS.shape
    logging.debug("%s Using a collection of %i snapshots of individual size of %i"%(selfA._name,__nbmS,__dimS))
    #
    if   selfA._parameters["ErrorNorm"] == "L2":
        MaxNormByColumn = MaxL2NormByColumn
    else:
        MaxNormByColumn = MaxLinfNormByColumn
    #
    if selfA._parameters["Variant"] in ["EIM", "PositioningByEIM"]:
        __LcCsts = False
    else:
        __LcCsts = True
    if __LcCsts and "ExcludeLocations" in selfA._parameters:
        __ExcludedMagicPoints = selfA._parameters["ExcludeLocations"]
    else:
        __ExcludedMagicPoints = ()
    if __LcCsts and "NameOfLocations" in selfA._parameters:
        if isinstance(selfA._parameters["NameOfLocations"], (list, numpy.ndarray, tuple)) and len(selfA._parameters["NameOfLocations"]) == __dimS:
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
    __Q      = numpy.empty(__dimS).reshape((-1,1))
    __errors = []
    #
    __M      = 0
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
        __rhoM = __residuM / __residuM[__iM]
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
            __Q = __rhoM.reshape((-1,1))
        __I.append(__iM)
        #
        __restrictedQi = numpy.tril( __Q[__I,:] )
        if __M > 1:
            __Qi_inv = numpy.linalg.inv(__restrictedQi)
        else:
            __Qi_inv = 1. / __restrictedQi
        #
        __restrictedEOSi = __EOS[__I,:]
        #
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
    if __errors[-1] < selfA._parameters["EpsilonEIM"]:
        logging.debug("%s %s (%.1e)"%(selfA._name,"The convergence is obtained when reaching the required EIM tolerance",selfA._parameters["EpsilonEIM"]))
    if __M >= __maxM:
        logging.debug("%s %s (%i)"%(selfA._name,"The convergence is obtained when reaching the maximum number of RB dimension",__maxM))
    logging.debug("%s The RB of size %i has been correctly build"%(selfA._name,__Q.shape[1]))
    logging.debug("%s There are %i points that have been excluded from the potential optimal points"%(selfA._name,len(__ExcludedMagicPoints)))
    if hasattr(selfA, "StoredVariables"):
        selfA.StoredVariables["OptimalPoints"].store( __I )
        if selfA._toStore("ReducedBasis"):
            selfA.StoredVariables["ReducedBasis"].store( __Q )
        if selfA._toStore("Residus"):
            selfA.StoredVariables["Residus"].store( __errors )
        if selfA._toStore("ExcludedPoints"):
            selfA.StoredVariables["ExcludedPoints"].store( __ExcludedMagicPoints )
    #
    return __mu, __I, __Q, __errors

# ==============================================================================
def EIM_online(selfA, QEIM, gJmu = None, mPoints = None, mu = None, PseudoInverse = True, rbDimension = None, Verbose = False):
    """
    Reconstruction du champ complet
    """
    if gJmu is None and mu is None:
        raise ValueError("Either measurements or parameters has to be given as a list, both can not be None simultaneously.")
    if mPoints is None:
        raise ValueError("List of optimal locations for measurements has to be given.")
    if gJmu is not None:
        if len(gJmu) > len(mPoints):
            raise ValueError("The number of measurements (%i) has to be less or equal to the number of optimal locations (%i)."%(len(gJmu),len(mPoints)))
        if len(gJmu) > QEIM.shape[1]:
            raise ValueError("The number of measurements (%i) in optimal locations has to be less or equal to the dimension of the RB (%i)."%(len(gJmu),QEIM.shape[1]))
        __gJmu = numpy.ravel(gJmu)
    if mu is not None:
        # __gJmu = H(mu)
        raise NotImplementedError()
    if rbDimension is not None:
        rbDimension = min(QEIM.shape[1], rbDimension)
    else:
        rbDimension = QEIM.shape[1]
    __rbDim = min(QEIM.shape[1],len(mPoints),len(gJmu),rbDimension) # Modulation
    #--------------------------
    #
    # Restriction aux mesures
    if PseudoInverse:
        __QJinv = numpy.linalg.pinv( QEIM[mPoints,0:__rbDim] )
        __gammaMu = numpy.dot( __QJinv, __gJmu[0:__rbDim])
    else:
        __gammaMu = numpy.linalg.solve( QEIM[mPoints,0:__rbDim], __gJmu[0:__rbDim] )
    #
    # Interpolation du champ complet
    __gMmu = numpy.dot( QEIM[:,0:__rbDim], __gammaMu )
    #
    #--------------------------
    logging.debug("%s The full field of size %i has been correctly build"%(selfA._name,__gMmu.size))
    if hasattr(selfA, "StoredVariables"):
        selfA.StoredVariables["Analysis"].store( __gMmu )
        if selfA._toStore("ReducedCoordinates"):
            selfA.StoredVariables["ReducedCoordinates"].store( __gammaMu )
    #
    return __gMmu

# ==============================================================================
def MaxL2NormByColumn(Ensemble, LcCsts = False, IncludedPoints = []):
    if LcCsts and len(IncludedPoints) > 0:
        normes = numpy.linalg.norm(
            numpy.take(Ensemble, IncludedPoints, axis=0, mode='clip'),
            axis = 0,
            )
    else:
        normes = numpy.linalg.norm( Ensemble, axis = 0)
    nmax = numpy.max(normes)
    imax = numpy.argmax(normes)
    return nmax, imax

def MaxLinfNormByColumn(Ensemble, LcCsts = False, IncludedPoints = []):
    if LcCsts and len(IncludedPoints) > 0:
        normes = numpy.linalg.norm(
            numpy.take(Ensemble, IncludedPoints, axis=0, mode='clip'),
            axis = 0, ord=numpy.inf,
            )
    else:
        normes = numpy.linalg.norm( Ensemble, axis = 0, ord=numpy.inf)
    nmax = numpy.max(normes)
    imax = numpy.argmax(normes)
    return nmax, imax

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
