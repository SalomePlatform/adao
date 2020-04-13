# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
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

import logging
from daCore import BasicObjects
import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "ENSEMBLEBLUE")
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "Analysis",
                "CurrentState",
                "Innovation",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
                ]
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            )
        self.setAttributes(tags=(
            "DataAssimilation",
            "NonLinear",
            "Filter",
            "Ensemble",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # Nombre d'ensemble pour l'ébauche
        # --------------------------------
        nb_ens = Xb.stepnumber()
        #
        # Construction de l'ensemble des observations, par génération a partir
        # de la diagonale de R
        # --------------------------------------------------------------------
        DiagonaleR = R.diag(Y.size)
        EnsembleY = numpy.zeros([Y.size,nb_ens])
        for npar in range(DiagonaleR.size):
            bruit = numpy.random.normal(0,DiagonaleR[npar],nb_ens)
            EnsembleY[npar,:] = Y[npar] + bruit
        #
        # Initialisation des opérateurs d'observation et de la matrice gain
        # -----------------------------------------------------------------
        Hm = HO["Tangent"].asMatrix(None)
        Hm = Hm.reshape(Y.size,Xb[0].size) # ADAO & check shape
        Ha = HO["Adjoint"].asMatrix(None)
        Ha = Ha.reshape(Xb[0].size,Y.size) # ADAO & check shape
        #
        # Calcul de la matrice de gain dans l'espace le plus petit et de l'analyse
        # ------------------------------------------------------------------------
        if Y.size <= Xb[0].size:
            K  = B * Ha * (R + Hm * B * Ha).I
        else:
            K = (BI + Ha * RI * Hm).I * Ha * RI
        #
        # Calcul du BLUE pour chaque membre de l'ensemble
        # -----------------------------------------------
        for iens in range(nb_ens):
            HXb = numpy.ravel(numpy.dot(Hm, Xb[iens]))
            if self._toStore("SimulatedObservationAtBackground"):
                self.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
            d  = numpy.ravel(EnsembleY[:,iens]) - HXb
            if self._toStore("Innovation"):
                self.StoredVariables["Innovation"].store( d )
            Xa = numpy.ravel(Xb[iens]) + numpy.dot(K, d)
            self.StoredVariables["CurrentState"].store( Xa )
            if self._toStore("SimulatedObservationAtCurrentState"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.dot(Hm, Xa) )
        #
        # Fabrication de l'analyse
        # ------------------------
        Members = self.StoredVariables["CurrentState"][-nb_ens:]
        Xa = numpy.array( Members ).mean(axis=0)
        self.StoredVariables["Analysis"].store( Xa )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.dot(Hm, Xa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
