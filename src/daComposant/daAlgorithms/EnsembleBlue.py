#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2013 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
from daCore import BasicObjects, PlatformInfo
m = PlatformInfo.SystemUsage()

import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "ENSEMBLEBLUE")
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if B is not None:
            BI = B.I
        elif self._parameters["B_scalar"] is not None:
            BI = 1.0 / self._parameters["B_scalar"]
            B = self._parameters["B_scalar"]
        else:
            raise ValueError("Background error covariance matrix has to be properly defined!")
        #
        if R is not None:
            RI = R.I
        elif self._parameters["R_scalar"] is not None:
            RI = 1.0 / self._parameters["R_scalar"]
        else:
            raise ValueError("Observation error covariance matrix has to be properly defined!")
        #
        # Nombre d'ensemble pour l'ébauche 
        # --------------------------------
        nb_ens = Xb.stepnumber()
        #
        # Construction de l'ensemble des observations, par génération a partir
        # de la diagonale de R
        # --------------------------------------------------------------------
        DiagonaleR = numpy.diag(R)
        EnsembleY = numpy.zeros([Y.size,nb_ens])
        for npar in range(DiagonaleR.size) : 
            bruit = numpy.random.normal(0,DiagonaleR[npar],nb_ens)
            EnsembleY[npar,:] = Y[npar] + bruit
        EnsembleY = numpy.matrix(EnsembleY)
        #
        # Initialisation des opérateurs d'observation et de la matrice gain
        # -----------------------------------------------------------------
        Hm = HO["Tangent"].asMatrix(None)
        Ha = HO["Adjoint"].asMatrix(None)
        #
        # Calcul de la matrice de gain dans l'espace le plus petit et de l'analyse
        # ------------------------------------------------------------------------
        if Y.size <= Xb[0].size:
            if self._parameters["R_scalar"] is not None:
                R = self._parameters["R_scalar"] * numpy.eye(Y.size, dtype=numpy.float)
            K  = B * Ha * (Hm * B * Ha + R).I
        else:
            K = (Ha * RI * Hm + BI).I * Ha * RI
        #
        # Calcul du BLUE pour chaque membre de l'ensemble
        # -----------------------------------------------
        for iens in range(nb_ens):
            d  = EnsembleY[:,iens] - Hm * Xb[iens]
            Xa = Xb[iens] + K*d
            
            self.StoredVariables["CurrentState"].store( Xa.A1 )
            self.StoredVariables["Innovation"].store( d.A1 )
        #
        # Fabrication de l'analyse
        # ------------------------
        Members = self.StoredVariables["CurrentState"][-nb_ens:]
        Xa = numpy.matrix( Members ).mean(axis=0)
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
