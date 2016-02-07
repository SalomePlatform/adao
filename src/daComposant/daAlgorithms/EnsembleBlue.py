#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2016 EDF R&D
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
            message  = "Stockage des variables internes ou interm�diaires du calcul",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs suppl�mentaires � stocker et/ou effectuer",
            listval  = ["CurrentState", "Innovation", "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"]
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fix�e pour le g�n�rateur al�atoire",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        # Param�tres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Pr�calcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # Nombre d'ensemble pour l'�bauche
        # --------------------------------
        nb_ens = Xb.stepnumber()
        #
        # Construction de l'ensemble des observations, par g�n�ration a partir
        # de la diagonale de R
        # --------------------------------------------------------------------
        DiagonaleR = R.diag(Y.size)
        EnsembleY = numpy.zeros([Y.size,nb_ens])
        for npar in range(DiagonaleR.size):
            bruit = numpy.random.normal(0,DiagonaleR[npar],nb_ens)
            EnsembleY[npar,:] = Y[npar] + bruit
        EnsembleY = numpy.matrix(EnsembleY)
        #
        # Initialisation des op�rateurs d'observation et de la matrice gain
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
            HXb = Hm * Xb[iens]
            if "SimulatedObservationAtBackground" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
            d  = EnsembleY[:,iens] - HXb
            if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["Innovation"].store( numpy.ravel(d) )
            Xa = Xb[iens] + K*d
            self.StoredVariables["CurrentState"].store( Xa )
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( Hm * Xa )
        #
        # Fabrication de l'analyse
        # ------------------------
        Members = self.StoredVariables["CurrentState"][-nb_ens:]
        Xa = numpy.matrix( Members ).mean(axis=0)
        self.StoredVariables["Analysis"].store( Xa.A1 )
        if "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel( Hm * Xa ) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
