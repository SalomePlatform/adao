#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2017 EDF R&D
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

import math, numpy
from daCore import BasicObjects, Persistence

# ==============================================================================
class ElementaryDiagnostic(BasicObjects.Diagnostic,Persistence.OneScalar):
    """
    Calcul d'une RMS
    """
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        BasicObjects.Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = float)

    def _formula(self, V1, V2):
        """
        Fait un écart RMS entre deux vecteurs V1 et V2
        """
        rms = math.sqrt( ((V2 - V1)**2).sum() / float(V1.size) )
        #
        return rms

    def calculate(self, vector1 = None, vector2 = None, step = None):
        """
        Teste les arguments, active la formule de calcul et stocke le résultat
        """
        if vector1 is None or vector2 is None:
            raise ValueError("Two vectors must be given to calculate their RMS")
        V1 = numpy.array(vector1)
        V2 = numpy.array(vector2)
        if V1.size < 1 or V2.size < 1:
            raise ValueError("The given vectors must not be empty")
        if V1.size != V2.size:
            raise ValueError("The two given vectors must have the same size")
        #
        value = self._formula( V1, V2 )
        #
        self.store( value = value, step = step )

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'

    D = ElementaryDiagnostic("Ma RMS")

    vect1 = [1, 2, 1, 2, 1]
    vect2 = [2, 1, 2, 1, 2]
    D.calculate(vect1,vect2)
    vect1 = [1, 3, 1, 3, 1]
    vect2 = [2, 2, 2, 2, 2]
    D.calculate(vect1,vect2)
    vect1 = [1, 1, 1, 1, 1]
    vect2 = [2, 2, 2, 2, 2]
    D.calculate(vect1,vect2)
    vect1 = [1, 1, 1, 1, 1]
    vect2 = [4, -2, 4, -2, -2]
    D.calculate(vect1,vect2)
    vect1 = [0.29, 0.97, 0.73, 0.01, 0.20]
    vect2 = [0.92, 0.86, 0.11, 0.72, 0.54]
    D.calculate(vect1,vect2)
    vect1 = [-0.23262176, 1.36065207,  0.32988102, 0.24400551, -0.66765848, -0.19088483, -0.31082575,  0.56849814,  1.21453443,  0.99657516]
    vect2 = [0,0,0,0,0,0,0,0,0,0]
    D.calculate(vect1,vect2)
    print " Les valeurs de RMS attendues sont les suivantes : [1.0, 1.0, 1.0, 3.0, 0.53162016515553656, 0.73784217096601323]"
    print " Les RMS obtenues................................:", D[:]
    print " La moyenne......................................:", D.mean()
    print

