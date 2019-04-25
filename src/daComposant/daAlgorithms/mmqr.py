# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2019 EDF R&D
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

__doc__ = """
    Implémentation informatique de l'algorithme MMQR, basée sur la publication :
    David R. Hunter, Kenneth Lange, "Quantile Regression via an MM Algorithm",
    Journal of Computational and Graphical Statistics, 9, 1, pp.60-77, 2000.
"""
__author__ = "Jean-Philippe ARGAUD"

import sys, math
from numpy import array, matrix, asarray, asmatrix
from numpy import sum, dot, linalg, ravel, max, min, hstack, argmin, argmax

# ==============================================================================
def mmqr(
        func     = None,
        x0       = None,
        fprime   = None,
        bounds   = None,
        quantile = 0.5,
        maxfun   = 15000,
        toler    = 1.e-06,
        y        = None,
        ):
    #
    # Recuperation des donnees et informations initiales
    # --------------------------------------------------
    variables = asmatrix(ravel( x0 ))
    mesures   = asmatrix(ravel( y )).T
    increment = sys.float_info[0]
    p         = len(variables.flat)
    n         = len(mesures.flat)
    quantile  = float(quantile)
    #
    # Calcul des parametres du MM
    # ---------------------------
    tn      = float(toler) / n
    e0      = -tn / math.log(tn)
    epsilon = (e0-tn)/(1+math.log(e0))
    #
    # Calculs d'initialisation
    # ------------------------
    residus  = ravel( mesures - func( variables ) )
    poids    = asarray( 1./(epsilon+abs(residus)) )
    veps     = 1. - 2. * quantile - residus * poids
    lastsurrogate = -sum(residus*veps) - (1.-2.*quantile)*sum(residus)
    iteration = 0
    #
    # Recherche iterative
    # -------------------
    while (increment > toler) and (iteration < maxfun) :
        iteration += 1
        #
        Derivees  = array(fprime(variables))
        Derivees  = Derivees.reshape(n,p) # Necessaire pour remettre en place la matrice si elle passe par des tuyaux YACS
        DeriveesT = array(matrix(Derivees).T)
        M         =   dot( DeriveesT , (array(matrix(p*[poids,]).T)*Derivees) )
        SM        =   dot( DeriveesT , veps ).T
        step      = - linalg.lstsq( M, SM, rcond=-1 )[0]
        #
        variables = variables + step
        if bounds is not None:
            while( (variables < ravel(asmatrix(bounds)[:,0])).any() or (variables > ravel(asmatrix(bounds)[:,1])).any() ):
                step      = step/2.
                variables = variables - step
        residus   = ravel( mesures - func(variables) )
        surrogate = sum(residus**2 * poids) + (4.*quantile-2.) * sum(residus)
        #
        while ( (surrogate > lastsurrogate) and ( max(list(abs(step))) > 1.e-16 ) ) :
            step      = step/2.
            variables = variables - step
            residus   = ravel( mesures-func(variables) )
            surrogate = sum(residus**2 * poids) + (4.*quantile-2.) * sum(residus)
        #
        increment     = lastsurrogate-surrogate
        poids         = 1./(epsilon+abs(residus))
        veps          = 1. - 2. * quantile - residus * poids
        lastsurrogate = -sum(residus * veps) - (1.-2.*quantile)*sum(residus)
    #
    # Mesure d'écart : q*Sum(residus)-sum(residus negatifs)
    # ----------------
    Ecart = quantile * sum(residus) - sum( residus[residus<0] )
    #
    return variables, Ecart, [n,p,iteration,increment,0]

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
