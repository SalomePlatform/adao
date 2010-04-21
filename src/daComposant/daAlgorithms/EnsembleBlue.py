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
    Algorithme de methode d'ensemble simple
"""
__author__ = "Sebastien MASSART, Jean-Philippe ARGAUD - Novembre 2008"

import sys ; sys.path.insert(0, "../daCore")
import logging
import numpy
import Persistence
from BasicObjects import Algorithm
import PlatformInfo ; m = PlatformInfo.SystemUsage()

# ==============================================================================
class ElementaryAlgorithm(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self._name = "ENSEMBLEBLUE"
        logging.debug("%s Initialisation"%self._name)

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Par=None ):
        """
        Calcul d'une estimation BLUE d'ensemble :
            - génération d'un ensemble d'observations, de même taille que le
              nombre d'ébauches
            - calcul de l'estimateur BLUE pour chaque membre de l'ensemble
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        # Nombre d'ensemble pour l'ébauche 
        # --------------------------------
        nb_ens = Xb.stepnumber()
        #
        # Construction de l'ensemble des observations, par génération a partir
        # de la diagonale de R
        # --------------------------------------------------------------------
        DiagonaleR = numpy.diag(R)
        EnsembleY = numpy.zeros([len(Y),nb_ens])
        for npar in range(len(DiagonaleR)) : 
            bruit = numpy.random.normal(0,DiagonaleR[npar],nb_ens)
            EnsembleY[npar,:] = Y[npar] + bruit
        EnsembleY = numpy.matrix(EnsembleY)
        #
        # Initialisation des opérateurs d'observation et de la matrice gain
        # -----------------------------------------------------------------
        Hm = H["Direct"].asMatrix()
        Ht = H["Adjoint"].asMatrix()
        
        K  = B * Ht * (Hm * B * Ht + R).I
        
        # Calcul du BLUE pour chaque membre de l'ensemble
        # -----------------------------------------------
        for iens in range(nb_ens):
            d  = EnsembleY[:,iens] - Hm * Xb.valueserie(iens)
            Xa = Xb.valueserie(iens) + K*d
            
            self.StoredVariables["Analysis"].store( Xa.A1 )
            self.StoredVariables["Innovation"].store( d.A1 )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        logging.debug("%s Terminé"%self._name)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'

        
