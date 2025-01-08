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
    Ensemble Of Simulations Generation
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, logging, copy
import daCore.NumericObjects

# ==============================================================================
def eosg(selfA, Xb, HO, outputEOX = False, assumeNoFailure = True):
    """
    Ensemble Of Simulations Generation
    """
    #
    sampleList = daCore.NumericObjects.BuildComplexSampleList(
        selfA._parameters["SampleAsnUplet"],
        selfA._parameters["SampleAsExplicitHyperCube"],
        selfA._parameters["SampleAsMinMaxStepHyperCube"],
        selfA._parameters["SampleAsMinMaxLatinHyperCube"],
        selfA._parameters["SampleAsMinMaxSobolSequence"],
        selfA._parameters["SampleAsIndependantRandomVariables"],
        Xb,
        selfA._parameters["SetSeed"],
    )
    #
    if hasattr(sampleList, "__len__") and len(sampleList) == 0:
        if outputEOX:
            return numpy.array([[]]), numpy.array([[]])
        else:
            return numpy.array([[]])
    #
    if outputEOX or selfA._toStore("EnsembleOfStates"):
        EOX = numpy.stack(tuple(copy.copy(sampleList)), axis=1)
    #
    # ----------
    if selfA._parameters["SetDebug"]:
        CUR_LEVEL = logging.getLogger().getEffectiveLevel()
        logging.getLogger().setLevel(logging.DEBUG)
        print("===> Beginning of evaluation, activating debug\n")
        print("     %s\n"%("-" * 75,))
    #
    Hm = HO["Direct"].appliedTo
    if assumeNoFailure:
        EOS = Hm(
            sampleList,
            argsAsSerie = True,
            returnSerieAsArrayMatrix = True,
        )
    else:
        try:
            EOS = Hm(
                sampleList,
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True,
            )
        except Exception:  # Reprise séquentielle sur erreur de calcul
            EOS, __s = [], 1
            for state in sampleList:
                if numpy.any(numpy.isin((None, numpy.nan), state)):
                    EOS.append( () )  # Résultat vide
                else:
                    try:
                        EOS.append( Hm(state) )
                        __s = numpy.asarray(EOS[-1]).size
                    except Exception:
                        EOS.append( () )  # Résultat vide
            for i, resultat in enumerate(EOS):
                if len(resultat) == 0:  # Résultat vide
                    EOS[i] = numpy.nan * numpy.ones(__s)
            EOS = numpy.stack(EOS, axis=1)
    #
    if len(EOS.shape) > 2 and EOS.shape[2] == 1:  # RaJ si transposition de Hm
        EOS = EOS.squeeze( axis = 2 )
    #
    if selfA._parameters["SetDebug"]:
        print("\n     %s\n"%("-" * 75,))
        print("===> End evaluation, deactivating debug if necessary\n")
        logging.getLogger().setLevel(CUR_LEVEL)
    # ----------
    #
    if selfA._toStore("EnsembleOfStates"):
        if EOX.shape[1] != EOS.shape[1]:
            raise ValueError("Numbers of states (=%i) and snapshots (=%i) has to be the same!"%(EOX.shape[1], EOS.shape[1]))  # noqa: E501
        selfA.StoredVariables["EnsembleOfStates"].store( EOX )
    if selfA._toStore("EnsembleOfSimulations"):
        selfA.StoredVariables["EnsembleOfSimulations"].store( EOS )
    #
    if outputEOX:
        if EOX.shape[1] != EOS.shape[1]:
            raise ValueError("Numbers of states (=%i) and snapshots (=%i) has to be the same!"%(EOX.shape[1], EOS.shape[1]))  # noqa: E501
        return EOX, EOS
    else:
        return EOS

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
