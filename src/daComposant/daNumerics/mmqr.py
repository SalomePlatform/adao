#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2012 EDF R&D
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

# L'algorithme est base sur la publication : David R. Hunter, Kenneth Lange,
# "Quantile Regression via an MM Algorithm", Journal of Computational and
# Graphical Statistics, 9, 1, pp.60-77, 2000

import sys, math
from numpy import sum, array, matrix, dot, linalg, asarray, asmatrix

# ==============================================================================
def mmqr(
        func     = None,
        x0       = None,
        fprime   = None,
        quantile = 0.5,
        maxfun   = 15000,
        toler    = 1.e-06,
        y        = None,
        ):
    #
    # Recuperation des donnees et informations initiales
    # --------------------------------------------------
    variables = asmatrix(x0).A1
    mesures   = asmatrix(asmatrix(y).A1).T
    increment = sys.float_info[0]
    p         = len(variables.flat)
    n         = len(mesures.flat)
    #
    # Calcul des parametres du MM
    # ---------------------------
    tn      = float(toler) / n
    e0      = -tn / math.log(tn)
    epsilon = (e0-tn)/(1+math.log(e0))
    #
    # Calculs d'initialisation
    # ------------------------
    residus  = asmatrix( mesures - func( variables ) ).A1
    poids    = 1./(epsilon+abs(residus))
    veps     = 1. - 2. * quantile - residus * poids
    lastsurrogate = -sum(residus*veps) - (1.-2.*quantile)*sum(residus)
    iteration = 0
    #
    # Recherche iterative
    # -------------------
    while (increment > toler) and (iteration < maxfun) :
        iteration += 1
        #
        Derivees  = fprime(variables)
        DeriveesT = matrix(Derivees).T
        M         = - dot( DeriveesT , (array(matrix(p*[poids]).T)*array(Derivees)) )
        SM        =   dot( DeriveesT , veps ).T
        step      = linalg.lstsq( M, SM )[0].A1
        #
        variables = asarray(variables) + asarray(step)
        residus   = ( mesures - func(variables) ).A1
        surrogate = sum(residus**2 * poids) + (4.*quantile-2.) * sum(residus)
        #
        while ( (surrogate > lastsurrogate) and ( max(list(abs(step))) > 1.e-16 ) ) :
            step      = step/2.
            variables = variables - step
            residus   = ( mesures-func(variables) ).A1
            surrogate = sum(residus**2 * poids) + (4.*quantile-2.) * sum(residus)
        #
        increment     = lastsurrogate-surrogate
        poids         = 1./(epsilon+abs(residus))
        veps          = 1. - 2. * quantile - residus * poids
        lastsurrogate = -sum(residus * veps) - (1.-2.*quantile)*sum(residus)
    #
    # Mesure d'�cart : q*Sum(residus)-sum(residus negatifs)
    # ----------------
    Ecart = quantile * sum(residus) - sum( residus[residus<0] )
    #
    return variables, Ecart, [n,p,iteration,increment,0]

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'