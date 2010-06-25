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
    Diagnostic qui effectue le test du Khi2 pour juger de l'homogénéite entre
    les distributions de 2 vecteurs quelconques.
        - entrée : la tolerance (tolerance) et le nombre de classes (nbclasse),
          sous forme de paramètres dans le dictionnaire Par
        - sortie : le resultat du diagnostic est une reponse booleenne au test :
          True si l homogeneite est valide au sens du test du Khi2,
          False dans le cas contraire.
"""
__author__ = "Sophie RICCI - Juillet 2008"

import numpy
from daCore import BasicObjects, Persistence
from ComputeKhi2 import ComputeKhi2_Homogen
import logging

# ==============================================================================
class ElementaryDiagnostic(BasicObjects.Diagnostic,Persistence.OneScalar):
    def __init__(self, name="", unit="", basetype = None, parameters = {} ):
        BasicObjects.Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = bool )
        for key in ["tolerance", "dxclasse", "nbclasses"]:
            if not self.parameters.has_key(key):
                raise ValueError("A parameter named \"%s\" is required."%key)

    def _formula(self, V1, V2):
        """
        Effectue le calcul de la p-value pour deux vecteurs et un nombre de 
        classes donne en parametre du diagnostic. 
        """
        [classes, eftheo, efobs, valeurKhi2, areaKhi2, message] = ComputeKhi2_Homogen(
            vectorV1 = V1,
            vectorV2 = V2,
            dx = self.parameters["dxclasse"],
            nbclasses = self.parameters["nbclasses"],
            SuppressEmptyClasses = True)
        #
        logging.info( message )
        logging.info( "(si <%.2f %s on refuse effectivement l'homogeneite)"%(100.*self.parameters["tolerance"],"%") )
        #
        answerKhisquareTest = False
        if (areaKhi2 < (100.*self.parameters["tolerance"])) :
            answerKhisquareTest = False
        else:
            answerKhisquareTest = True
        #
        return answerKhisquareTest

    def calculate(self, vector1 = None, vector2 = None,  step = None):
        """
        Active la formule de calcul
        """
        if (vector1 is None) or (vector2 is None) :
            raise ValueError("Two vectors must be given to calculate the Khi2 value")
        V1 = numpy.array(vector1)
        V2 = numpy.array(vector2)
        if (V1.size < 1) or (V2.size < 1):
            raise ValueError("The given vectors must not be empty")
        if V1.size != V2.size:
            raise ValueError("The two given vectors must have the same size")
        #
        value = self._formula( V1, V2 )
        #
        self.store( value = value, step = step )

# ==============================================================================
if __name__ == "__main__":
    print "\n AUTODIAGNOSTIC \n"

    print " Test d'homogeneite du Khi-2 pour deux vecteurs de taille 10,"
    print " issus d'une distribution gaussienne normale"
    print
    #
    # Initialisation des inputs et appel du diagnostic
    # --------------------------------------------------------------------
    tolerance = 0.05
    dxclasse = 0.5
    D = ElementaryDiagnostic("HomogeneiteKhi2", parameters = {
        "tolerance":tolerance,
        "dxclasse":dxclasse,
        "nbclasses":None,
        })
    #
    # Tirage de l'echantillon aleatoire 
    # --------------------------------------------------------------------
    numpy.random.seed(4000)
    x1 = numpy.random.normal(50.,1.5,10000)
    numpy.random.seed(2490)
    x2 = numpy.random.normal(50.,1.5,10000)
    #
    # Calcul 
    # --------------------------------------------------------------------
    D.calculate(x1, x2)
    #
    print " La reponse du test est \"%s\" pour une tolerance de %.2e et une largeur de classe de %.2e "%(D.valueserie(0), tolerance, dxclasse)
    print
