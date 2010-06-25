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
    Diagnostic sur la reduction du biais lors de l'analyse
"""
__author__ = "Sophie RICCI - Aout 2008"

import numpy
from daCore import BasicObjects, Persistence

# ==============================================================================
class ElementaryDiagnostic(BasicObjects.Diagnostic,Persistence.OneScalar):
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        BasicObjects.Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = bool)

    def _formula(self, V1, V2):
        """
        Vérification de la reduction du biais entre OMB et OMA lors de l'analyse
        """
        biaisOMB = V1.mean() 
        biaisOMA = V2.mean() 
        #
        if biaisOMA > biaisOMB: 
            reducebiais = False
        else :
            reducebiais = True
        #
        return reducebiais

    def calculate(self, vectorOMB = None, vectorOMA = None, step = None):
        """
        Teste les arguments, active la formule de calcul et stocke le résultat
        Arguments :
            - vectorOMB : vecteur d'écart entre les observations et l'ébauche 
            - vectorOMA : vecteur d'écart entre les observations et l'analyse
        """
        if ( (vectorOMB is None) or (vectorOMA is None) ):
            raise ValueError("Two vectors must be given to test the reduction of the biais after analysis")
        V1 = numpy.array(vectorOMB)
        V2 = numpy.array(vectorOMA)
        if V1.size < 1 or V2.size < 1:
            raise ValueError("The given vectors must not be empty")
        if V1.size != V2.size:
            raise ValueError("The two given vectors must have the same size")
        #
        value = self._formula( V1, V2 )
        #
        self.store( value = value,  step = step )

#===============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    #
    # Instanciation de l'objet diagnostic
    # -----------------------------------
    D = ElementaryDiagnostic("Mon ReduceBiais")
    #
    # Tirage des 2 vecteurs choisis
    # -------------------------------
    x1 = numpy.matrix(([3. , 4., 5. ]))
    x2 = numpy.matrix(([1.5, 2., 2.5]))
    print " L'écart entre les observations et l'ébauche est OMB :", x1
    print " La moyenne de OMB (i.e. le biais) est de............:", x1.mean()
    print " L'écart entre les observations et l'analyse est OMA :", x2
    print " La moyenne de OMA (i.e. le biais) est de............:", x2.mean()
    #
    D.calculate( vectorOMB = x1,  vectorOMA = x2)
    if not D.valueserie(0) :
            print " Résultat : l'analyse NE RÉDUIT PAS le biais"
    else :
            print " Résultat : l'analyse RÉDUIT le biais"
    print
    #
    # Tirage des 2 vecteurs choisis
    # -------------------------------
    x1 = numpy.matrix(range(-5,6))
    x2 = numpy.array(range(11))
    print " L'écart entre les observations et l'ébauche est OMB :", x1
    print " La moyenne de OMB (i.e. le biais) est de............:", x1.mean()
    print " L'écart entre les observations et l'analyse est OMA :", x2
    print " La moyenne de OMA (i.e. le biais) est de............:", x2.mean()
    #
    D.calculate( vectorOMB = x1,  vectorOMA = x2)
    if not D.valueserie(1) :
            print " Résultat : l'analyse NE RÉDUIT PAS le biais"
    else :
            print " Résultat : l'analyse RÉDUIT le biais"
    print
