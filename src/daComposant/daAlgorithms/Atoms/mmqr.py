# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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
    MMQR
"""
__author__ = "Jean-Philippe ARGAUD"

import sys, math, numpy
from daCore.PlatformInfo import PlatformInfo
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
def mmqr( func     = None,
          x0       = None,
          fprime   = None,
          bounds   = None,
          quantile = 0.5,
          maxfun   = 15000,
          toler    = 1.e-06,
          y        = None,
          ):
    """
    Implémentation informatique de l'algorithme MMQR, basée sur la publication :
    David R. Hunter, Kenneth Lange, "Quantile Regression via an MM Algorithm",
    Journal of Computational and Graphical Statistics, 9, 1, pp.60-77, 2000.
    """
    #
    # Récupération des données et informations initiales
    # --------------------------------------------------
    variables = numpy.ravel( x0 )
    mesures   = numpy.ravel( y )
    increment = sys.float_info[0]
    p         = variables.size
    n         = mesures.size
    quantile  = float(quantile)
    #
    # Calcul des paramètres du MM
    # ---------------------------
    tn      = float(toler) / n
    e0      = -tn / math.log(tn)
    epsilon = (e0 - tn) / (1 + math.log(e0))
    #
    # Calculs d'initialisation
    # ------------------------
    residus  = mesures - numpy.ravel( func( variables ) )
    poids    = 1. / (epsilon + numpy.abs(residus))
    veps     = 1. - 2. * quantile - residus * poids
    lastsurrogate = - numpy.sum(residus * veps) - (1. - 2. * quantile) * numpy.sum(residus)
    iteration = 0
    #
    # Recherche itérative
    # -------------------
    while (increment > toler) and (iteration < maxfun):
        iteration += 1
        #
        Derivees  = numpy.array(fprime(variables))
        Derivees  = Derivees.reshape(n, p)  # ADAO & check shape
        DeriveesT = Derivees.transpose()
        M         = numpy.dot( DeriveesT, (numpy.array(p * [poids,]).T * Derivees) )
        SM        = numpy.transpose(numpy.dot( DeriveesT, veps ))
        step      = - numpy.linalg.lstsq( M, SM, rcond=-1 )[0]
        #
        variables = variables + step
        if bounds is not None:
            # Attention : boucle infinie à éviter si un intervalle est trop petit
            while ( (variables < numpy.ravel(numpy.asarray(bounds)[:, 0])).any() or (variables > numpy.ravel(numpy.asarray(bounds)[:, 1])).any() ):  # noqa: E501
                step      = step / 2.
                variables = variables - step
        residus   = mesures - numpy.ravel( func(variables) )
        surrogate = numpy.sum(residus**2 * poids) + (4. * quantile - 2.) * numpy.sum(residus)
        #
        while ( (surrogate > lastsurrogate) and ( max(list(numpy.abs(step))) > 1.e-16 ) ):
            step      = step / 2.
            variables = variables - step
            residus   = mesures - numpy.ravel( func(variables) )
            surrogate = numpy.sum(residus**2 * poids) + (4. * quantile - 2.) * numpy.sum(residus)
        #
        increment     = abs(lastsurrogate - surrogate)
        poids         = 1. / (epsilon + numpy.abs(residus))
        veps          = 1. - 2. * quantile - residus * poids
        lastsurrogate = -numpy.sum(residus * veps) - (1. - 2. * quantile) * numpy.sum(residus)
    #
    # Mesure d'écart
    # --------------
    Ecart = quantile * numpy.sum(residus) - numpy.sum( residus[residus < 0] )
    #
    return variables, Ecart, [n, p, iteration, increment, 0]

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
