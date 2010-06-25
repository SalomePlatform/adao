#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2010  EDF R&D
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
    Calcul du biais (i.e. la moyenne) à chaque pas. Ce diagnostic très simple
    est présent pour rappeller à l'utilisateur de l'assimilation qu'il faut
    qu'il vérifie le biais de ses erreurs en particulier.
"""
__author__ = "Sophie RICCI - Aout 2008"

import numpy
from daCore import BasicObjects, Persistence

# ==============================================================================
class ElementaryDiagnostic(BasicObjects.Diagnostic,Persistence.OneScalar):
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        BasicObjects.Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = float )

    def _formula(self, V):
        """
        Calcul du biais, qui est simplement la moyenne du vecteur
        """
        biais = V.mean() 
        #
        return biais

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
    # Instanciation de l'objet diagnostic
    # -----------------------------------
    D = ElementaryDiagnostic("Mon ComputeBiais")
    #
    # Tirage d un vecteur choisi
    # --------------------------
    x = numpy.matrix(([3., 4., 5.]))
    print " Le vecteur de type 'matrix' choisi est..:", x
    print " Le biais attendu de ce vecteur est......:", x.mean()
    #
    D.calculate( vector = x)
    print " Le biais obtenu de ce vecteur est.......:", D.valueserie(0)
    print
    #
    # Tirage d un vecteur choisi
    # --------------------------
    x = numpy.array(range(11))
    print " Le vecteur de type 'array' choisi est...:", x
    print " Le biais attendu de ce vecteur est......:", x.mean()
    #
    D.calculate( vector = x)
    print " Le biais obtenu de ce vecteur est.......:", D.valueserie(1)
    print
