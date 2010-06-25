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
    Diagnostic sur les variances dans B et R par rapport à l'ébauche Xb et aux
    observations Y. On teste si on a les conditions :
        1%*xb < sigma_b < 10%*xb
            et
        1%*yo < sigma_o < 10%*yo
    Le diagnostic renvoie True si les deux conditions sont simultanément
    vérifiées, False dans les autres cas.
"""
__author__ = "Sophie RICCI, Jean-Philippe ARGAUD - Septembre 2008"

import numpy
from scipy.linalg import eig
from daCore import BasicObjects, Persistence
import logging

# ==============================================================================
class ElementaryDiagnostic(BasicObjects.Diagnostic,Persistence.OneScalar):
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        BasicObjects.Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = bool )

    def _formula(self, xb, B, yo, R):
        """
        Comparaison des variables et de leur variance relative
        """
        valpB = eig(B, left = False, right = False)
        valpR = eig(R, left = False, right = False)
        logging.info(" Si l on souhaite 1%s*xb < sigma_b < 10%s*xb, les valeurs propres de B doivent etre comprises dans l intervalle [%.3e,%.3e]"%("%","%",1.e-4*xb.mean()*xb.mean(),1.e-2*xb.mean()*xb.mean()))
        logging.info(" Si l on souhaite 1%s*yo < sigma_o < 10%s*yo, les valeurs propres de R doivent etre comprises dans l intervalle [%.3e,%.3e]"%("%","%",1.e-4*yo.mean()*yo.mean(),1.e-2*yo.mean()*yo.mean()))
        #
        limite_inf_valp = 1.e-4*xb.mean()*xb.mean()
        limite_sup_valp = 1.e-2*xb.mean()*xb.mean()
        variancexb = (valpB >= limite_inf_valp).all() and (valpB <= limite_sup_valp).all()
        logging.info(" La condition empirique sur la variance de Xb est....: %s"%variancexb)
        #
        limite_inf_valp = 1.e-4*yo.mean()*yo.mean()
        limite_sup_valp = 1.e-2*yo.mean()*yo.mean()
        varianceyo = (valpR >= limite_inf_valp).all() and (valpR <= limite_sup_valp).all()
        logging.info(" La condition empirique sur la variance de Y est.....: %s",varianceyo)
        #
        variance = variancexb and varianceyo
        logging.info(" La condition empirique sur la variance globale est..: %s"%variance)
        #
        return variance

    def calculate(self, Xb = None, B = None, Y = None, R = None,  step = None):
        """
        Teste les arguments, active la formule de calcul et stocke le résultat
        Arguments :
            - Xb : valeur d'ébauche du paramêtre
            - B  : matrice de covariances d'erreur d'ébauche
            - yo : vecteur d'observation
            - R  : matrice de covariances d'erreur d'observation 
        """
        if (Xb is None) or (B is None) or (Y is None) or (R is None):
            raise ValueError("You must specify Xb, B, Y, R")
        yo = numpy.array(Y)
        BB = numpy.matrix(B)
        xb = numpy.array(Xb)
        RR = numpy.matrix(R)
        if (RR.size < 1 ) or (BB.size < 1) :
            raise ValueError("The background and the observation covariance matrices must not be empty")
        if ( yo.size < 1 ) or ( xb.size < 1 ):
            raise ValueError("The Xb background and the Y observation vectors must not be empty")
        if xb.size*xb.size != BB.size:
            raise ValueError("Xb background vector and B covariance matrix sizes are not consistent")
        if yo.size*yo.size != RR.size:
            raise ValueError("Y observation vector and R covariance matrix sizes are not consistent")
        if yo.all() == 0. or xb.all() == 0. :
            raise ValueError("The diagnostic can not be applied to zero vectors")
        #
        value = self._formula( xb, BB, yo, RR)
        #
        self.store( value = value,  step = step )

#===============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    #
    # Instanciation de l'objet diagnostic
    # -----------------------------------
    D = ElementaryDiagnostic("Mon OrdreVariance")
    #
    # Vecteur de type matrix
    # ----------------------
    xb = numpy.array([11000.])
    yo = numpy.array([1.e12 , 2.e12, 3.e12 ])
    B = 1.e06 * numpy.matrix(numpy.identity(1))
    R = 1.e22 * numpy.matrix(numpy.identity(3))
    #
    D.calculate( Xb = xb, B = B, Y = yo, R = R)
    print " L'ébauche est.......................................:",xb
    print " Les observations sont...............................:",yo
    print " La valeur moyenne des observations est..............: %.2e"%yo.mean()
    print " La valeur moyenne de l'ebauche est..................: %.2e"%xb.mean()
    print " La variance d'ébauche specifiée est.................: %.2e"%1.e6
    print " La variance d'observation spécifiée est.............: %.2e"%1.e22
    #
    if D.valueserie(0) :
            print " Les variances specifiées sont de l'ordre de 1% a 10% de l'ébauche et des observations"
    else :
            print " Les variances specifiées ne sont pas de l'ordre de 1% a 10% de l'ébauche et des observations"
    print


