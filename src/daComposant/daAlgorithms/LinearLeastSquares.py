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
        BasicObjects.Algorithm.__init__(self, "LINEARLEASTSQUARES")
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = ["OMA"]
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Opérateur d'observation
        # -----------------------
        Hm = HO["Tangent"].asMatrix(None)
        Ha = HO["Adjoint"].asMatrix(None)
        #
        if R is not None:
            RI = R.I
        elif self._parameters["R_scalar"] is not None:
            RI = 1.0 / self._parameters["R_scalar"]
        else:
            raise ValueError("Observation error covariance matrix has to be properly defined!")
        #
        # Calcul de la matrice de gain et de l'analyse
        # --------------------------------------------
        K =  (Ha * RI * Hm ).I * Ha * RI
        Xa =  K * Y
        #
        # Calcul de la fonction coût
        # --------------------------
        oma = Y - Hm * Xa
        Jb  = 0.
        Jo  = 0.5 * oma.T * RI * oma
        J   = float( Jb ) + float( Jo )
        self.StoredVariables["Analysis"].store( Xa.A1 )
        self.StoredVariables["CostFunctionJb"].store( Jb )
        self.StoredVariables["CostFunctionJo"].store( Jo )
        self.StoredVariables["CostFunctionJ" ].store( J )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(oma) )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
