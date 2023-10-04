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
    Empirical Interpolation Method DEIM & lcDEIM
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, scipy, logging
import daCore.Persistence
from daCore.NumericObjects import FindIndexesFromNames

# ==============================================================================
def DEIM_offline(selfA, EOS = None, Verbose = False):
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
    logging.debug("%s Building a RB using a collection of %i snapshots of individual size of %i"%(selfA._name,__nbmS,__dimS))
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
    __U, __vs, _ = scipy.linalg.svd( __EOS )
    __rhoM = numpy.compress(__vs > selfA._parameters["EpsilonEIM"], __U, axis=1)
    __lVs, __svdM = __rhoM.shape
    assert __lVs == __dimS, "Différence entre lVs et dim(EOS)"
    __qivs = (1. - __vs[:__svdM].cumsum()/__vs.sum())
    __maxM   = min(__maxM,__svdM)
    #
    if __LcCsts and len(__IncludedMagicPoints) > 0:
        __im = numpy.argmax( numpy.abs(
            numpy.take(__rhoM[:,0], __IncludedMagicPoints, mode='clip')
            ))
    else:
        __im = numpy.argmax( numpy.abs(
            __rhoM[:,0]
            ))
    #
    __mu     = [None,] # Convention
    __I      = [__im,]
    __Q      = __rhoM[:,0].reshape((-1,1))
    __errors = []
    #
    __M      = 1 # Car le premier est déjà construit
    __errors.append(__qivs[0])
    #
    # Boucle
    # ------
    while __M < __maxM:
        #
        __restrictedQi = __Q[__I,:]
        if __M > 1:
            __Qi_inv = numpy.linalg.inv(__restrictedQi)
        else:
            __Qi_inv = 1. / __restrictedQi
        #
        __restrictedrhoMi = __rhoM[__I,__M].reshape((-1,1))
        #
        if __M > 1:
            __interpolator = numpy.dot(__Q,numpy.dot(__Qi_inv,__restrictedrhoMi))
        else:
            __interpolator = numpy.outer(__Q,numpy.outer(__Qi_inv,__restrictedrhoMi))
        #
        __residuM = __rhoM[:,__M].reshape((-1,1)) - __interpolator
        #
        if __LcCsts and len(__IncludedMagicPoints) > 0:
            __im = numpy.argmax( numpy.abs(
                numpy.take(__residuM, __IncludedMagicPoints, mode='clip')
                ))
        else:
            __im = numpy.argmax( numpy.abs(
                __residuM
                ))
        __Q = numpy.column_stack((__Q, __rhoM[:,__M]))
        __I.append(__im)
        #
        __errors.append(__qivs[__M])
        __mu.append(None) # Convention
        #
        __M = __M + 1
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
        if selfA._toStore("SingularValues"):
            selfA.StoredVariables["SingularValues"].store( __vs )
    #
    return __mu, __I, __Q, __errors

# ==============================================================================
# DEIM_online == EIM_online
# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
