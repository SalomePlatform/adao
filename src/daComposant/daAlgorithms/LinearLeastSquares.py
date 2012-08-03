#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2012 EDF R&D
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

import logging
from daCore import BasicObjects, PlatformInfo
m = PlatformInfo.SystemUsage()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "LINEARLEASTSQUARES")

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Calcul de l'estimateur moindres carr�s pond�r�s lin�aires
        (assimilation variationnelle sans �bauche)
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        # Param�tres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Op�rateur d'observation
        # -----------------------
        Hm = H["Direct"].asMatrix()
        Ha = H["Adjoint"].asMatrix()
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
        logging.debug("%s Analyse Xa = %s"%(self._name, Xa))
        #
        # Calcul de la fonction co�t
        # --------------------------
        d  = Y - Hm * Xa
        Jb  = 0.
        Jo  = 0.5 * d.T * RI * d
        J   = float( Jb ) + float( Jo )
        logging.debug("%s CostFunction Jb = %s"%(self._name, Jb))
        logging.debug("%s CostFunction Jo = %s"%(self._name, Jo))
        logging.debug("%s CostFunction J  = %s"%(self._name, J))
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        self.StoredVariables["Innovation"].store( d.A1 )
        self.StoredVariables["CostFunctionJb"].store( Jb )
        self.StoredVariables["CostFunctionJo"].store( Jo )
        self.StoredVariables["CostFunctionJ" ].store( J )
        #
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        logging.debug("%s Termin�"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
