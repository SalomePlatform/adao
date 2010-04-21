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
    Algorithme de moindre carres pond�r�s (analyse sans ebauche)
"""
__author__ = "Sophie RICCI, Jean-Philippe ARGAUD - Septembre 2008"

import sys ; sys.path.insert(0, "../daCore")
import logging
import Persistence
from BasicObjects import Algorithm
import PlatformInfo ; m = PlatformInfo.SystemUsage()

# ==============================================================================
class ElementaryAlgorithm(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self._name = "LINEARLEASTSQUARES"

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Par=None):
        """
        Calcul de l'estimateur au sens des moindres carres sans ebauche
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        Hm = H["Direct"].asMatrix()
        Ht = H["Adjoint"].asMatrix()
        #
        K =  (Ht * R.I * Hm ).I * Ht * R.I
        Xa =  K * Y
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        logging.debug("%s Termin�"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'


