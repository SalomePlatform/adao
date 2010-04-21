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
    Calcul de la fonction coût avec Hlin
              HX = Hxb + Hlin dx
"""
__author__ = "Sophie RICCI - Octobre 2008"

import sys ; sys.path.insert(0, "../daCore") 

import numpy
import Persistence
from BasicObjects import Diagnostic
from AssimilationStudy import AssimilationStudy
import logging

# ==============================================================================
class ElementaryDiagnostic(Diagnostic,Persistence.OneScalar):
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        Diagnostic.__init__(self, name)
        Persistence.OneScalar.__init__( self, name, unit, basetype = float)
        self.__name = str( name )

    def _formula(self,  X = None, dX = None, Hlin = None, Xb=None, HXb = None, Y=None, R=None, B=None):

        """
        Calcul de la fonction cout
        """
        HX = HXb + Hlin.T * dX 
        if hasattr(HX, 'A1') :
            HX = HX.A1
        #
        Jb = 1./2. * (X - Xb).T * B.I * (X - Xb)
        logging.info( "Partial cost function : Jb = %s"%Jb )
        #
        Jo = 1./2. * (Y - HX).T  * R.I * (Y - HX)
        logging.info( "Partial cost function : Jo = %s"%Jo )
        #
        J = Jb + Jo
        logging.info( "Total cost function : J = Jo + Jb = %s"%J )
        return J

    def calculate(self, x = None, dx = None, Hlin = None, xb = None, Hxb = None, yo = None, R = None, B = None , step = None):
        """
        Teste les arguments, active la formule de calcul et stocke le résultat
        """
        if (x is None) or (xb is None) or (yo is None)  or (dx is None):
            raise ValueError("Vectors x, dx, xb and yo must be given to compute J")
        dX = dx
        if hasattr(numpy.matrix(x), 'A1') :
            X = numpy.matrix(x).A1
        if hasattr(numpy.matrix(xb), 'A1') :
            Xb = numpy.matrix(xb).A1
        if hasattr(numpy.matrix(yo), 'A1') :
            Y = numpy.matrix(yo).A1
        B = numpy.matrix(B)
        R = numpy.matrix(R)
        if (Hlin is None ) :
            raise ValueError("HlinT vector must be given")
        if (Hxb is None ) :
            raise ValueError("The given vector must be given")
        HXb = Hxb
        if (B is None ) or (R is None ):
            raise ValueError("The matrices B and R must be given")
        #
        value = self._formula(X, dX, Hlin, Xb, HXb, Y, R, B)
        #
        self.store( value = value,  step = step )

#===============================================================================
if __name__ == "__main__":
    print "\nAUTOTEST\n"
    #
    D = ElementaryDiagnostic("Ma fonction cout")
    #
    # Vecteur de type array
    # ---------------------
    x = numpy.array([1., 2.])
    dx = numpy.array([0.1, 0.2])
    xb = numpy.array([2., 2.])
    yo = numpy.array([5., 6.])
    Hlin = numpy.matrix(numpy.identity(2))
    Hxb = Hlin *xb 
    Hxb = Hxb.T
    Hxb = Hxb.A1
    B =  numpy.matrix(numpy.identity(2))
    R =  numpy.matrix(numpy.identity(2))
    #
    D.calculate( x = x, dx = dx, Hlin = Hlin, xb = xb, Hxb = Hxb,  yo = yo, R = R, B = B)
    print "Le vecteur x choisi est...:", x
    print "L ebauche xb choisie est...:", xb
    print "Le vecteur d observation est...:", yo
    print "B = ", B
    print "R = ", R
    print "La fonction cout J vaut ...: %.2e"%D.valueserie(0)
    #
    if (abs(D.valueserie(0) - 11.925) > 1.e-6)  :
        raise ValueError("The computation of the cost function is NOT correct")
    else :
        print "The computation of the cost function is OK"
    print
