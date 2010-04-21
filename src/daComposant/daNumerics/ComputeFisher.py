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
    Outil numérique de calcul de la variable de Fisher pour comparer les
    variances de 2 échantillons

    Ce calcul nécessite :
        - en input :
            - les deux vecteurs (comme liste, array ou matrix) d'échantillons
              dont on veut comparer la variance,
            - la tolérance
        - en output :
            - la p-value,
            - la valeur de la variable aléatoire,
            - la réponse au test ainsi que
            - le message qui interprete la reponse du test.
"""
__author__ = "Sophie RICCI - Juillet 2008"

import numpy
from scipy.stats import betai

# ==============================================================================
def ComputeFisher(vector1 = None, vector2 = None, tolerance = 0.05 ):
    """
    Outil numérique de calcul de la variable de Fisher pour comparer les
    variances de 2 échantillons

    Ce calcul nécessite :
        - en input : les deux vecteurs (comme liste, array ou matrix)
                     d'échantillons dont on veut comparer la variance, la
                     tolérance
        - en output : la p-value, la valeur de la variable aléatoire,
                      la réponse au test ainsi que le message qui interprete
                      la reponse du test.
    """
    if (vector1 is None) or (vector2 is None) :
        raise ValueError("Two vectors must be given to calculate the Fisher value value")
    V1 = numpy.array(vector1)
    V2 = numpy.array(vector2)
    if (V1.size < 1) or (V2.size < 1):
        raise ValueError("The given vectors must not be empty")
    #
    # Calcul des variances des echantillons
    # -------------------------------------
    # où var est calculee comme : var = somme (xi -xmean)**2 /(n-1)
    n1 = V1.size
    n2 = V2.size
    var1 = V1.std() * V1.std()
    var2 = V2.std() * V2.std() 
    if (var1 > var2):
        f = var1/var2
        df1 = n1-1
        df2 = n2-1
    else:
         f= var2/var1
         df1 = n2-1
         df2 = n1-1
    prob1= betai(0.5*df2,0.5*df1,float(df2)/float(df2+df1*f)) 
    prob2= (1. - betai(0.5*df1, 0.5*df2, float(df1)/float(df1+df2/f)))  
    prob = prob1 + prob2
    #
    # Calcul de la p-value
    # --------------------
    areafisher = 100 * prob
    #
    # Test
    # ----
    message = "Il y a %.2f%s de chance de se tromper en refusant l'hypothèse d'égalité des variances des 2 échantillons (si <%.2f%s, on refuse effectivement l'égalité)"%(areafisher,"%",100.*tolerance,"%")
    if (areafisher < (100.*tolerance)) :
        answerTestFisher = False
    else:
        answerTestFisher = True
    # print "La reponse au test est", answerTestFisher

    return areafisher, f, answerTestFisher, message

# ==============================================================================
if __name__ == "__main__":
    print "\nAUTOTEST\n"
    #
    # Echantillons
    # ------------
    x1 = [-1., 0., 4., 2., -1., 3.]
    x2 = [-1., 0., 4., 2., -1., 3.]
    #
    # Appel du calcul
    # ---------------
    [aire, f, reponse, message] = ComputeFisher(
        vector1   = x1,
        vector2   = x2,
        tolerance = 0.05 )
    #
    print " aire.....:", aire
    print " f........:", f
    print " reponse..:", reponse
    print " message..:", message
    print
