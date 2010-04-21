#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2009  EDF R&D
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
__doc__ = """
    Algorithme de Kalman pour un système discret
    
    Remarque : les observations sont exploitées à partir du pas de temps 1, et
    sont utilisées dans Yo comme rangées selon ces indices. Donc le pas 0 n'est
    pas utilisé puisque la première étape de Kalman passe de 0 à 1 avec
    l'observation du pas 1.
"""
__author__ = "Jean-Philippe ARGAUD - Septembre 2008"

import sys ; sys.path.insert(0, "../daCore")
import logging
import Persistence
from BasicObjects import Algorithm
import PlatformInfo ; m = PlatformInfo.SystemUsage()

# ==============================================================================
class ElementaryAlgorithm(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self._name = "KALMAN"
        logging.debug("%s Initialisation"%self._name)

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Par=None):
        """
        Calcul de l'estimateur de Kalman
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        # Opérateur d'observation
        # -----------------------
        Hm = H["Direct"].asMatrix()
        Ht = H["Adjoint"].asMatrix()
        #
        # Opérateur d'évolution
        # ---------------------
        Mm = M["Direct"].asMatrix()
        Mt = M["Adjoint"].asMatrix()
        #
        duration = Y.stepnumber()
        #
        # Initialisation
        # --------------
        Xn = Xb
        Pn = B
        self.StoredVariables["Analysis"].store( Xn.A1 )
        self.StoredVariables["CovarianceAPosteriori"].store( Pn )
        #
        for step in range(duration-1):
            logging.debug("%s Etape de Kalman %i (i.e. %i->%i) sur un total de %i"%(self._name, step+1, step,step+1, duration-1))
            #
            # Etape de prédiction
            # -------------------
            Xn_predicted = Mm * Xn
            Pn_predicted = Mm * Pn * Mt + Q
            #
            # Etape de correction
            # -------------------
            d  = Y.valueserie(step+1) - Hm * Xn_predicted
            K  = Pn_predicted * Ht * (Hm * Pn_predicted * Ht + R).I
            Xn = Xn_predicted + K * d
            Pn = Pn_predicted - K * Hm * Pn_predicted
            #
            self.StoredVariables["Analysis"].store( Xn.A1 )
            self.StoredVariables["CovarianceAPosteriori"].store( Pn )
            self.StoredVariables["Innovation"].store( d.A1 )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
