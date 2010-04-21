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
    Outil numérique de calcul des variables de Student pour 2 vecteurs
    dépendants ou indépendants, avec variances supposées égales ou différentes
"""
__author__ = "Sophie RICCI, Jean-Philippe ARGAUD - Octobre 2008"

import sys ; sys.path.insert(0, "../daCore")

import numpy
from scipy.stats import ttest_rel, ttest_ind, betai
import logging

# ==============================================================================
def DependantVectors(vector1 = None, vector2 = None, tolerance = 0.05 ):
    """
    Outil numérique de calcul de la variable de Student pour 2 vecteurs
    dépendants
    Ce calcul nécessite :
        - en input :
            - les deux vecteurs (comme liste, array ou matrix)
              d'échantillons dont on veut comparer la variance,
            - la tolérance
        - en output :
            - la p-value,
            - la valeur de la variable aléatoire,
            - la reponse au test pour une tolerance ainsi que
            - le message qui interprete la reponse du test.
    """
    if (vector1 is None) or (vector2 is None) :
        raise ValueError("Two vectors must be given to calculate the Student value")
    V1 = numpy.array(vector1)
    V2 = numpy.array(vector2)
    if (V1.size < 1) or (V2.size < 1):
        raise ValueError("The given vectors must not be empty")
    if V1.size != V2.size:
        raise ValueError("The two given vectors must have the same size, or the vector types are incompatible")
    #
    # Calcul de la p-value du Test de Student
    # --------------------------------------------------------------------
    [t, prob] = ttest_rel(V1, V2)
    areastudent = 100. * prob
    #
    logging.debug("DEPENDANTVECTORS t = %.3f, areastudent = %.3f"%(t, areastudent))
    #
    # Tests
    # --------------------------------------------------------------------
    message =  "DEPENDANTVECTORS Il y a %.2f %s de chance de se tromper en refusant l'hypothèse d'égalité des moyennes des 2 échantillons dépendants (si <%.2f %s on refuse effectivement l'égalité)"%(areastudent, "%", 100.*tolerance,"%")
    logging.debug(message)
    #
    if (areastudent < (100.*tolerance)) :
        answerTestStudent = False
    else:
        answerTestStudent = True
    #
    return  areastudent, t, answerTestStudent, message

# ==============================================================================
def IndependantVectorsDifferentVariance(vector1 = None, vector2 = None, tolerance = 0.05 ):
    """
    Outil numerique de calcul de la variable de Student pour 2 vecteurs independants supposes de variances vraies differentes
    En input : la tolerance
    En output : la p-value, la valeur de la variable aleatoire, la reponse au test pour une tolerance ainsi que le message qui interprete la reponse du test.
    """
    if (vector1 is None) or (vector2 is None) :
        raise ValueError("Two vectors must be given to calculate the Student value")
    V1 = numpy.array(vector1)
    V2 = numpy.array(vector2)
    if (V1.size < 1) or (V2.size < 1):
        raise ValueError("The given vectors must not be empty")
    #
    # Calcul de la p-value du Test de Student
    # --------------------------------------------------------------------
    # t = (m1 - m2)/ sqrt[ (var1/n1 + var2/n2) ]
    # ou var est calcule comme var = somme (xi -xmena)**2 /(n-1)
    n1 = V1.size
    n2 = V2.size
    mean1 = V1.mean()
    mean2 = V2.mean() 
    var1 = numpy.sqrt(n1)/numpy.sqrt(n1-1) * V1.std() * numpy.sqrt(n1)/numpy.sqrt(n1-1) * V1.std()
    var2 = numpy.sqrt(n2)/numpy.sqrt(n2-1) * V2.std() * numpy.sqrt(n2)/numpy.sqrt(n2-1) * V2.std()
    t = (mean1 - mean2)/ numpy.sqrt( var1/n1 + var2/n2 )
    df = ( (var1/n1 + var2/n2) * (var1/n1 + var2/n2) ) / ( (var1/n1)*(var1/n1)/(n1-1)  + (var2/n2)*(var2/n2)/(n2-1) )
    zerodivproblem = var1/n1 + var2/n2 == 0
    t = numpy.where(zerodivproblem, 1.0, t)           # replace NaN t-values with 1.0
    prob = betai(0.5*df,0.5,float(df)/(df+t*t))
    areastudent = 100. * prob
    #
    logging.debug("IndependantVectorsDifferentVariance t = %.3f, areastudent = %.3f"%(t, areastudent))
    #
    # Tests
    # --------------------------------------------------------------------
    message =  "IndependantVectorsDifferentVariance Il y a %.2f %s de chance de se tromper en refusant l'hypothèse d'égalité des moyennes des 2 échantillons indépendants supposés de variances différentes (si <%.2f %s on refuse effectivement l'égalité)"%(areastudent, "%", 100.* tolerance,"%")
    logging.debug(message)
    if (areastudent < (100.*tolerance)) :
        answerTestStudent = False
    else:
        answerTestStudent = True
    #
    return  areastudent, t, answerTestStudent, message

# ==============================================================================
def IndependantVectorsEqualVariance(vector1 = None, vector2 = None, tolerance = 0.05 ):
    """
    Outil numerique de calcul de la variable de Student pour 2 vecteurs independants supposes de meme variance vraie
    En input : la tolerance
    En output : la p-value, la valeur de la variable aleatoire, la reponse au test pour une tolerance ainsi que le message qui interprete la reponse du test.
    """
    if (vector1 is None) or (vector2 is None) :
        raise ValueError("Two vectors must be given to calculate the Student value")
    V1 = numpy.array(vector1)
    V2 = numpy.array(vector2)
    if (V1.size < 1) or (V2.size < 1):
        raise ValueError("The given vectors must not be empty")
    #
    # Calcul de la p-value du Test de Student
    # --------------------------------------------------------------------
    # t = sqrt(n1+n2-2) * (m1 - m2)/ sqrt[ (1/n1 +1/n2) * ( (n1-1)var1 + (n2-1)var2 )]
    # ou var est calcule comme var = somme (xi -xmena)**2 /(n-1)
    [t, prob] = ttest_ind(V1, V2)
    areastudent = 100. * prob
    #
    logging.debug("IndependantVectorsEqualVariance t = %.3f, areastudent = %.3f"%(t, areastudent))
    # Tests
    # --------------------------------------------------------------------
    message =  "IndependantVectorsEqualVariance Il y a %.2f %s de chance de se tromper en refusant l'hypothèse d'égalité des moyennes des 2 échantillons indépendants supposés de même variance (si <%.2f %s on refuse effectivement l'égalité)"%(areastudent, "%", 100.* tolerance,"%")
    logging.debug(message)
    if (areastudent < (100.*tolerance)) :
        answerTestStudent = False
    else:
        answerTestStudent = True

    return  areastudent, t, answerTestStudent, message

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    # logging.getLogger().setLevel(logging.DEBUG)

    print
    print " Test de Student pour des vecteurs dépendants"
    print " --------------------------------------------"
    # Tirage de l'echantillon 
    V1 = numpy.matrix(([-1., 0., 4.])).T
    V2 = numpy.matrix(([-2., 0., 8.])).T
    V1 = V1.A1
    V2 = V2.A1
    #
    # Appel de l outil DependantVectors et initialisation des inputs
    [aire, Q, reponse, message] = DependantVectors(
        vector1 = V1,
        vector2 = V2,
        tolerance = 0.05)
    #
    # Verification par les calculs sans les routines de scipy.stats
    # (ref numerical recipes)
    n = V1.size
    df= n -1
    # Les routines de scipy.stats utilisent une variance calculee avec n-1 et non n comme dans std
    # t =  (m1 - m2)/ sqrt[(varx1 + varx2 - 2 cov(x1, x2))/n ]
    # ou var est calcule comme var = somme (xi -xmean)**2 /(n-1)
    var1 = numpy.sqrt(n)/numpy.sqrt(n-1)* V1.std() * numpy.sqrt(n)/numpy.sqrt(n-1) * V1.std()
    var2 = numpy.sqrt(n)/numpy.sqrt(n-1)* V2.std() * numpy.sqrt(n)/numpy.sqrt(n-1) * V2.std()
    m1 = V1.mean()
    m2 = V2.mean()
    cov = 0.
    for j in range(0, n) :
       cov = cov + (V1[j] - m1)*(V2[j] - m2)
    cov = cov /df
    sd = numpy.sqrt((var1 + var2 - 2. *cov) / n)
    tverif = (m1 -m2) /sd
    aireverif = 100. * betai(0.5*df,0.5,float(df)/(df+tverif*tverif))
    if  (aireverif - aire < 1.e-5)   :
       print " Le calcul est conforme à celui de l'algorithme du Numerical Recipes"
    else :
       raise ValueError("Le calcul n'est pas conforme à celui de l'algorithme Numerical Recipes")

    if  (numpy.abs(aire - 57.99159)< 1.e-5)  :
       print " Le calcul est JUSTE sur cet exemple."
    else :
       raise ValueError("Le calcul est FAUX sur cet exemple.")

    print
    print " Test de Student pour des vecteurs independants supposés de même variance"
    print " ------------------------------------------------------------------------"
    # Tirage de l'echantillon 
    V1 = numpy.matrix(([-1., 0., 4.])).T
    V2 = numpy.matrix(([-2., 0., 8.])).T
    V1 = V1.A1
    V2 = V2.A1
    #
    # Appel de l outil IndependantVectorsDifferentVariance et initialisation des inputs
    [aire, Q, reponse, message] = IndependantVectorsDifferentVariance(
        vector1 = V1,
        vector2 = V2,
        tolerance = 0.05)
    #
    if  (numpy.abs(aire - 78.91339)< 1.e-5)  :
       print " Le calcul est JUSTE sur cet exemple."
    else :
       raise ValueError("Le calcul est FAUX sur cet exemple.")

    print
    print " Test de Student pour des vecteurs indépendants supposés de même variance"
    print " ------------------------------------------------------------------------"
    # Tirage de l'echantillon 
    V1 = numpy.matrix(([-1., 0., 4.])).T
    V2 = numpy.matrix(([-2., 0., 8.])).T
    V1 = V1.A1
    V2 = V2.A1
    #
    # Appel de l outil IndependantVectorsEqualVariance et initialisation des inputs
    [aire, Q, reponse, message] = IndependantVectorsEqualVariance(
        vector1 = V1,
        vector2 = V2,
        tolerance = 0.05)
    #
    # Verification par les calculs sans les routines de scipy.stats (ref numerical recipes)
    n1 = V1.size
    n2 = V2.size
    df= n1 + n2 -2
    # Les routines de scipy.stats utilisent une variance calculee avec n-1 et non n comme dans std
    var1 = numpy.sqrt(n1)/numpy.sqrt(n1-1)* V1.std() * numpy.sqrt(n1)/numpy.sqrt(n1-1) * V1.std()
    var2 = numpy.sqrt(n2)/numpy.sqrt(n2-1)* V2.std() * numpy.sqrt(n2)/numpy.sqrt(n2-1) * V2.std()
    m1 = V1.mean()
    m2 = V2.mean()
    var = ((n1 -1.) *var1 + (n2 -1.) *var2 ) /df
    tverif = (m1 -m2) /numpy.sqrt(var*(1./n1 + 1./n2))
    aireverif = 100. * betai(0.5*df,0.5,float(df)/(df+tverif*tverif))
    #
    if  (aireverif - aire < 1.e-5)   :
       print " Le calcul est conforme à celui de l'algorithme du Numerical Recipes"
    else :
       raise ValueError("Le calcul n'est pas conforme à celui de l'algorithme Numerical Recipes")

    if  (numpy.abs(aire - 78.42572)< 1.e-5)  :
       print " Le calcul est JUSTE sur cet exemple."
    else :
       raise ValueError("Le calcul est FAUX sur cet exemple.")

    print
