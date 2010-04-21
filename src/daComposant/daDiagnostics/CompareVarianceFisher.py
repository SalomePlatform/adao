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
    Diagnostic qui compare les variances de 2 vecteurs au sens de Fisher à
    l'aide du calcul de la p-value pour le test de Fisher.
        - entrée : la tolérance (tolerance) sous forme de paramètres dans le
          dictionnaire Par, et les deux vecteurs d'échantillons.
        - sortie : le résultat du diagnostic est une réponse booléenne au test :
          True si l'égalite des variances est valide au sens du test de Fisher, 
          False dans le cas contraire
"""
__author__ = "Sophie RICCI - Juillet 2008"

import sys ; sys.path.insert(0, "../daCore")

import numpy
import Persistence
from BasicObjects import Diagnostic
from ComputeFisher import ComputeFisher
import logging

# ==============================================================================
class ElementaryDiagnostic(Diagnostic,Persistence.OneScalar):
    """
    Diagnostic qui compare les variances de 2 vecteurs au sens de Fisher à
    l'aide du calcul de la p-value pour le test de Fisher.
        - entrée : la tolérance (tolerance) sous forme de paramètres dans le
          dictionnaire Par, et les deux vecteurs d'échantillons.
        - sortie : le résultat du diagnostic est une réponse booléenne au test :
          True si l'égalite des variances est valide au sens du test de Fisher, 
          False dans le cas contraire
    """
    def __init__(self, name="", unit="", basetype = None, parameters = {} ):
        Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = bool)
        if not self.parameters.has_key("tolerance"):
            raise ValueError("A parameter named \"tolerance\" is required.")

    def formula(self, V1, V2):
        """
        Effectue le test de Fisher avec la p-value pour 2 vecteurs
        """
        [aire, f, reponse, message] = ComputeFisher(
            vector1 = V1, 
            vector2 = V2, 
            tolerance = self.parameters["tolerance"],
            )
        answerKhisquareTest = False
        if (aire < (100.*self.parameters["tolerance"])) :
            answerKhisquareTest = False
        else:
            answerKhisquareTest = True
        logging.info( message )
        #
        return answerKhisquareTest

    def calculate(self, vector1 = None, vector2 = None,  step = None):
        """
        Active la formule de calcul
        """
        if (vector1 is None) or (vector2 is None) :
            raise ValueError("Two vectors must be given to calculate the Fisher p-value")
        V1 = numpy.array(vector1)
        V2 = numpy.array(vector2)
        if (V1.size < 1) or (V2.size < 1):
            raise ValueError("The given vectors must not be empty")
        if V1.size != V2.size:
            raise ValueError("The two given vectors must have the same size, or the vector types are incompatible")
        #
        value = self.formula( V1, V2 )
        #
        self.store( value = value, step = step)

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'

    print " Test d'égalite des variances pour deux vecteurs de taille 10"
    print
    #
    # Initialisation des inputs et appel du diagnostic
    # --------------------------------------------------------------------
    tolerance = 0.05
    D = ElementaryDiagnostic("CompareVarianceFisher", parameters = {
                 "tolerance":tolerance,
                 })
    #
    # Tirage de l'echantillon aleatoire 
    # --------------------------------------------------------------------
    x1 = numpy.array(([-0.23262176, 1.36065207,  0.32988102, 0.24400551, -0.66765848, -0.19088483, -0.31082575,  0.56849814,  1.21453443,  0.99657516]))
    x2 = numpy.array(([-0.23, 1.36,  0.32, 0.24, -0.66, -0.19, -0.31,  0.56,  1.21,  0.99]))
    #
    # Calcul 
    # --------------------------------------------------------------------
    D.calculate(x1, x2)
    #
    if D.valueserie(0) :
            print " L'hypothèse d'égalité des deux variances est correcte."
            print
    else :
            raise ValueError("L'hypothèse d'égalité des deux variances est fausse.")
