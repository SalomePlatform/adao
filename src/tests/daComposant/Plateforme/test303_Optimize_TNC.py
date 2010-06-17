#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant que la minimisation TNC de Scipy fonctionne
    sur un cas simple.
"""
__author__ = "Jean-Philippe ARGAUD - Avril 2009"

import numpy
import scipy.optimize

import logging
# Si on désire plus d'information sur le déroulement du calcul, on peut
# décommenter l'une des lignes qui suit :
# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG)

if logging.getLogger().level < 30:
    message = scipy.optimize.tnc.MSG_ALL
else:
    message = scipy.optimize.tnc.MSG_NONE

from test300_Optimize_CG import CostFunction

#===============================================================================
def test(precision = 1.e-07, dimension = 3):
    """
    Cas-test vérifiant que la minimisation TNC de Scipy fonctionne
    sur un cas simple.
    """
    #
    # Définition de l'objet contenant la fonction-coût
    # ------------------------------------------------
    X0 = numpy.random.normal(0.,1.,size=(dimension,))
    J = CostFunction( X0 )
    #
    X_initial = 3. * X0
    #
    X_optimal, neval, rc = scipy.optimize.fmin_tnc(
        func        = J.value,
        x0          = X_initial,
        fprime      = J.gradient,
        args        = (),
        approx_grad = False,
        pgtol       = precision,
        messages    = message,
        )
    #
    J_optimal = J.value( X_optimal )
    GradJ_opt = J.gradient( X_optimal )
    #
    logging.info("")
    logging.info("Résultats finaux :")
    logging.info("  X0        = %s"%X0)
    logging.info("  X_optimal = %s"%X_optimal)
    logging.info("  J_optimal = %s"%J_optimal)
    logging.info("  GradJ_opt = %s"%GradJ_opt)
    #
    # Vérification du résultat
    # ------------------------
    if J_optimal > precision:
        raise ValueError("Résultat du test erroné sur J")
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inférieure à %s"%precision
        print "    Nombre de calculs de la fonctionnelle J : %i"%J.iterations()
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    numpy.random.seed(1000)
    
    test(dimension = 100)
