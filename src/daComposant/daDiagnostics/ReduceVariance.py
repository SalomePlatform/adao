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

import numpy
from daCore import BasicObjects, Persistence

# ==============================================================================
class ElementaryDiagnostic(BasicObjects.Diagnostic,Persistence.OneScalar):
    """
    Diagnostic sur la reduction de la variance lors de l'analyse
    """
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        BasicObjects.Diagnostic.__init__(self, name, parameters)
        Persistence.OneScalar.__init__( self, name, unit, basetype = bool )

    def _formula(self, V1, V2):
        """
        Vérification de la reduction de variance sur les écarts entre OMB et OMA
        lors de l'analyse
        """
        varianceOMB = V1.var() 
        varianceOMA = V2.var() 
        #
        if varianceOMA > varianceOMB: 
            reducevariance = False
        else :
            reducevariance = True
        #
        return reducevariance

    def calculate(self, vectorOMB = None, vectorOMA = None, step = None):
        """
        Teste les arguments, active la formule de calcul et stocke le résultat
        Arguments :
            - vectorOMB : vecteur d'écart entre les observations et l'ébauche 
            - vectorOMA : vecteur d'écart entre les observations et l'analyse
        """
        if ( (vectorOMB is None) or (vectorOMA is None) ):
            raise ValueError("Two vectors must be given to test the reduction of the variance after analysis")
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
    print('\n AUTODIAGNOSTIC \n')
    #
    # Instanciation de l'objet diagnostic
    # -----------------------------------
    D = ElementaryDiagnostic("Mon ReduceVariance")
    #
    # Vecteur de type matrix
    # ----------------------
    x1 = numpy.matrix(([3. , 4., 5. ]))
    x2 = numpy.matrix(([1.5, 2., 2.5]))
    print(" L'écart entre les observations et l'ébauche est OMB : %s"%(x1,))
    print(" La moyenne de OMB (i.e. le biais) est de............: %s"%(x1.mean(),))
    print(" La variance de OMB est de...........................: %s"%(x1.var(),))
    print(" L'écart entre les observations et l'analyse est OMA : %s"%(x2,))
    print(" La moyenne de OMA (i.e. le biais) est de............: %s"%(x2.mean(),))
    print(" La variance de OMA est de...........................: %s"%(x2.var(),))
    #
    D.calculate( vectorOMB = x1,  vectorOMA = x2)
    if not D[0] :
            print(" Résultat : l'analyse NE RÉDUIT PAS la variance")
    else :
            print(" Résultat : l'analyse RÉDUIT la variance")
    print("")
    #
    # Vecteur de type array
    # ---------------------
    x1 = numpy.array(range(11))
    x2 = numpy.matrix(range(-10,12,2))
    print(" L'écart entre les observations et l'ébauche est OMB : %s"%(x1,))
    print(" La moyenne de OMB (i.e. le biais) est de............: %s"%(x1.mean(),))
    print(" La variance de OMB est de...........................: %s"%(x1.var(),))
    print(" L'écart entre les observations et l'analyse est OMA : %s"%(x2,))
    print(" La moyenne de OMA (i.e. le biais) est de............: %s"%(x2.mean(),))
    print(" La variance de OMA est de...........................: %s"%(x2.var(),))
    #
    D.calculate( vectorOMB = x1,  vectorOMA = x2)
    if not D[1] :
            print(" Résultat : l'analyse NE RÉDUIT PAS la variance")
    else :
            print(" Résultat : l'analyse RÉDUIT la variance")
    print("")
