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
    Diagnostic sur l'arrêt (ou le ralentissement) de la réduction de la variance 
    au fil des pas (ou itérations) de l'analyse.
    Ce diagnostic s'applique typiquement au vecteur de différence entre la 
    variance de OMB et la variance de OMA au fil du temps ou des itérations:
    V[i] = vecteur des VAR(OMB)[i] - VAR(OMA)[i] au temps ou itération i.
"""
__author__ = "Sophie Ricci - Septembre 2008"

import sys ; sys.path.insert(0, "../daCore")

import numpy
import Persistence
from BasicObjects import Diagnostic
from AssimilationStudy import AssimilationStudy

# ==============================================================================
class ElementaryDiagnostic(Diagnostic,Persistence.OneScalar):
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = int )

    def _formula(self, V, CutOffSlope, MultiSlope0):
        """
        Recherche du pas de temps ou iteration pour laquelle la reduction 
        de la variance est 
        - inferieure a la valeur seuil CutOffSlope 
          (si une valeure est donnee a CutOffSlope)
        - inferieure a MultiSlope0 * la pente a la premiere iteration 
          (si une valeure est donnee a MultiSlope0)
        V[i] = vecteur des VAR(OMB)[i] - VAR(OMA)[i] au temps ou iteration i.
        """
        N = V.size
        pente = numpy.matrix(numpy.zeros((N,))).T
        iterstopreduction = 0.
        for i in range (1, N) :
            pente[i] = V[i]- V[i-1]
            if pente[i] > 0.0  :
               raise ValueError("The analysis is INCREASING the variance a l iteration ", i)
            if CutOffSlope is not None:     
                if  numpy.abs(pente[i]) < CutOffSlope  :
                    iterstopreduction = i
                    break
            if MultiSlope0 is not None:
                if  numpy.abs(pente[i]) < MultiSlope0 * numpy.abs(pente[1])  :
                    iterstopreduction = i
                    break
        #
        return iterstopreduction

    def calculate(self, vector = None, CutOffSlope = None, MultiSlope0 = None, step = None) :
        """
        Teste les arguments, active la formule de calcul et stocke le resultat
        Arguments :
            - vector : vecteur des VAR(OMB) - VAR(OMA) au fil des iterations
            - CutOffSlope : valeur minimale de la pente 
            - MultiSlope0 : Facteur multiplicatif de la pente initiale pour comparaison
        """
        if  (vector is None) :
            raise ValueError("One vector must be given to test the convergence of the variance after analysis")
        V = numpy.array(vector)
        if V.size < 1  :
            raise ValueError("The given vector must not be empty")
        if (MultiSlope0 is None) and (CutOffSlope is None) :
            raise ValueError("You must set the value of ONE of the CutOffSlope of MultiSlope0 key word")
        #
        value = self._formula( V, CutOffSlope, MultiSlope0 )
        #
        self.store( value = value,  step = step )

#===============================================================================
if __name__ == "__main__":
    print "\n AUTODIAGNOSTIC \n"

    # Instanciation de l'objet diagnostic
    # ------------------------------------------------
    D = ElementaryDiagnostic("Mon StopReductionVariance")

    # Vecteur de reduction VAR(OMB)-VAR(OMA)
    # ------------------------------------------------
    x = numpy.array(([0.60898111,  0.30449056,  0.15224528,  0.07612264,  0.03806132,  0.01903066, 0.00951533,  0.00475766,  0.00237883,  0.00118942]))
    print " Le vecteur choisi est :", x
    print " Sur ce vecteur, la reduction a l iteration N =  7 est inferieure a 0.005"
    print " Sur ce vecteur, la reduction a l iteration N =  8 est inferieure a 0.01 * la reduction a l iteration 1"
    
    # Comparaison a la valeur seuil de la reduction
    # ------------------------------------------------
    D.calculate( vector = x,  CutOffSlope = 0.005, MultiSlope0 = None)
    if (D.valueserie(0) - 7.) < 1.e-15 :
        print " Test : La comparaison a la valeur seuil de la reduction est juste"
    else :
        print " Test : La comparaison a la valeur seuil de la reduction est fausse"

    # Comparaison a alpha* la reduction a la premiere iteration
    # ------------------------------------------------
    D.calculate( vector = x,  CutOffSlope = None, MultiSlope0 = 0.01)
    if (D.valueserie(1) - 8.) < 1.e-15 :
        print " Test : La comparaison a la reduction a la premiere iteration est juste"
    else :
        print " Test : La comparaison a la reduction a la premiere iteration est fausse"
    print
