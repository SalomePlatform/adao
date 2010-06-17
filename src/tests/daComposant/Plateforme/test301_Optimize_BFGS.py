#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test v�rifiant que la minimisation BFGS de Scipy fonctionne
    sur un cas simple.
"""
__author__ = "Jean-Philippe ARGAUD - Avril 2009"

import numpy
import scipy.optimize

import logging
# Si on d�sire plus d'information sur le d�roulement du calcul, on peut
# d�commenter l'une des lignes qui suit :
# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG)

from test300_Optimize_CG import CostFunction

#===============================================================================
def test(precision = 1.e-07, dimension = 3):
    """
    Cas-test v�rifiant que la minimisation BFGS de Scipy fonctionne
    sur un cas simple.
    """
    #
    # D�finition de l'objet contenant la fonction-co�t
    # ------------------------------------------------
    X0 = numpy.random.normal(0.,1.,size=(dimension,))
    J = CostFunction( X0 )
    #
    X_initial = 3. * X0
    #
    X_optimal, J_optimal, GradJ_opt, Hopt, func_calls, grad_calls, warnflag = scipy.optimize.fmin_bfgs(
        f      = J.value,
        x0     = X_initial,
        fprime = J.gradient,
        args   = (),
        gtol   = precision,
        full_output = True,
        )
    #
    logging.info("")
    logging.info("R�sultats finaux :")
    logging.info("  X0        = %s"%X0)
    logging.info("  X_optimal = %s"%X_optimal)
    logging.info("  J_optimal = %s"%J_optimal)
    logging.info("  GradJ_opt = %s"%GradJ_opt)
    #
    # V�rification du r�sultat
    # ------------------------
    if max(abs(GradJ_opt)) > precision:
        raise ValueError("R�sultat du test erron� sur le gradient de J")
    elif J_optimal > precision:
        raise ValueError("R�sultat du test erron� sur J")
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inf�rieure � %s"%precision
        print "    Nombre de calculs de la fonctionnelle J : %i"%J.iterations()
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    numpy.random.seed(1000)
    
    test(dimension = 100)
