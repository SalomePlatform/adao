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
    Calcul de la variance d'un vecteur à chaque pas. Ce diagnostic très simple
    est présent pour rappeller à l'utilisateur de l'assimilation qu'il faut
    qu'il vérifie les variances de ses écarts en particulier.
"""
__author__ = "Jean-Philippe ARGAUD - Septembre 2008"

import sys ; sys.path.insert(0, "../daCore") 

import numpy
import Persistence
from BasicObjects import Diagnostic
from AssimilationStudy import AssimilationStudy

# ==============================================================================
class ElementaryDiagnostic(Diagnostic,Persistence.OneScalar):
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = float)

    def _formula(self, V):
        """
        Calcul de la variance du vecteur en argument. Elle est faite avec une
        division par la taille du vecteur.
        """
        variance = V.var() 
        #
        return variance

    def calculate(self, vector = None, step = None):
        """
        Teste les arguments, active la formule de calcul et stocke le résultat
        """
        if vector is None:
            raise ValueError("One vector must be given to compute biais")
        V = numpy.array(vector)
        if V.size < 1:
            raise ValueError("The given vector must not be empty")
        #
        value = self._formula( V)
        #
        self.store( value = value,  step = step )

#===============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    #
    D = ElementaryDiagnostic("Ma variance")
    #
    # Vecteur de type matrix
    # ----------------------
    x = numpy.matrix(([3., 4., 5.]))
    print " Le vecteur de type 'matrix' choisi est..:", x
    print " Le moyenne de ce vecteur est............:", x.mean()
    print " La variance attendue de ce vecteur est..:", x.var()
    #
    D.calculate( vector = x)
    print " La variance obtenue de ce vecteur est...:", D.valueserie(0)
    print
    #
    # Vecteur de type array
    # ---------------------
    x = numpy.array(range(11))
    print " Le vecteur de type 'array' choisi est...:", x
    print " Le moyenne de ce vecteur est............:", x.mean()
    print " La variance attendue de ce vecteur est..:", x.var()
    #
    D.calculate( vector = x)
    print " La variance obtenue de ce vecteur est...:", D.valueserie(1)
    print
