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
    Diagnostic qui effectue le test du Khi2 pour juger de l'adéquation entre 
    la distribution d'un échantillon et une distribution gaussienne dont la 
    moyenne et l'écart-type sont calculés sur l'échantillon.
    En input : la tolerance(tolerance) et le nombre de classes(nbclasse)
    En output : Le resultat du diagnostic est une reponse booleenne au test : 
                True si l adequation a une distribution gaussienne est valide 
                au sens du test du Khi2, 
                False dans le cas contraire. 
"""
__author__ = "Sophie RICCI - Juillet 2008"

import sys ; sys.path.insert(0, "../daCore")

import numpy
from numpy import random
import Persistence
from BasicObjects import Diagnostic
from ComputeKhi2 import ComputeKhi2_Gauss
import logging

# ==============================================================================
class ElementaryDiagnostic(Diagnostic,Persistence.OneScalar):
    """
    """
    def __init__(self, name="", unit="", basetype = None, parameters = {} ):
        Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = bool)
        for key in ["tolerance", "dxclasse", "nbclasses"]:
            if not self.parameters.has_key(key):
                raise ValueError("A parameter named \"%s\" is required."%key)

    def formula(self, V):
        """
        Effectue le calcul de la p-value pour un vecteur et une distribution 
        gaussienne et un nombre de classes donne en parametre du diagnostic. 
        """

        [vectclasse, eftho, efobs, valeurKhi2, areaKhi2, message] = ComputeKhi2_Gauss( 
            vectorV = V, 
            dx = self.parameters["dxclasse"],
            nbclasses = self.parameters["nbclasses"],
            SuppressEmptyClasses = True)


        logging.info( message )
        logging.info( "(si <%.2f %s on refuse effectivement l'adéquation)"%(100.*self.parameters["tolerance"],"%") )
        logging.info("vecteur des classes=%s"%numpy.size(vectclasse) )
        logging.info("valeurKhi2=%s"%valeurKhi2) 
        logging.info("areaKhi2=%s"%areaKhi2) 
        logging.info("tolerance=%s"%self.parameters["tolerance"])

        if (areaKhi2 < (100.*self.parameters["tolerance"])) :
            answerKhisquareTest = False
        else:
            answerKhisquareTest = True
        logging.info( "La réponse au test est donc est %s"%answerKhisquareTest )
        return answerKhisquareTest

    def calculate(self, vector = None,  step = None):
        """
        Active la formule de calcul
        """
        if vector is None:
            raise ValueError("One vector must be given to calculate the Khi2 test")
        V = numpy.array(vector)
        if V.size < 1:
            raise ValueError("The given vector must not be empty")
        #
        value = self.formula( V )
        #
        self.store( value = value,  step = step)

# ==============================================================================
if __name__ == "__main__":
    print "\n AUTODIAGNOSTIC \n"

    print " Test d adequation du khi-2 a une gaussienne pour un vecteur x"
    print " connu de taille 1000, issu d'une distribution gaussienne normale"
    print " en fixant la largeur des classes"
    print 
    #
    # Initialisation des inputs et appel du diagnostic
    # ------------------------------------------------
    tolerance = 0.05
    dxclasse = 0.1
    D = ElementaryDiagnostic("AdequationGaussKhi2", parameters = {
        "tolerance":tolerance,
        "dxclasse":dxclasse, 
        "nbclasses":None, 
        })
    #
    # Tirage de l'echantillon aleatoire 
    # ---------------------------------
    numpy.random.seed(2490)
    x = random.normal(50.,1.5,1000)
    #
    # Calcul 
    # ------
    D.calculate(x)
    #
    if D.valueserie(0) :
        print " L'adequation a une distribution gaussienne est valide."
        print
    else :
        raise ValueError("L'adéquation a une distribution gaussienne n'est pas valide.")


    print " Test d adequation du khi-2 a une gaussienne pour u:n vecteur x"
    print " connu de taille 1000, issu d'une distribution gaussienne normale"
    print " en fixant le nombre de classes"
    print
    #
    # Initialisation des inputs et appel du diagnostic
    # ------------------------------------------------
    tolerance = 0.05
    nbclasses = 70.
    D = ElementaryDiagnostic("AdequationGaussKhi2", parameters = {
        "tolerance":tolerance,
        "dxclasse":None, 
        "nbclasses":nbclasses 
        })
    #
    # Tirage de l'echantillon aleatoire 
    # ---------------------------------
    numpy.random.seed(2490)
    x = random.normal(50.,1.5,1000)
    #
    # Calcul 
    # ------
    D.calculate(x)
    #
    if D.valueserie(0) :
        print " L'adequation a une distribution gaussienne est valide."
        print
    else :
        raise ValueError("L'adequation a une distribution gaussienne n'est pas valide.")


