#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant que la minimisation CG de Scipy fonctionne
    sur un cas simple.
"""
__author__ = "Jean-Philippe ARGAUD - Avril 2009"

import numpy
import scipy.optimize

import logging
# Si on désire plus d'information sur le déroulement du calcul, on peut
# décommenter l'une des lignes qui suit :
# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG)

#===============================================================================
class CostFunction:
    """
    Classe permettant de rassembler toutes les informations disponibles sur la
    fonction-coût nécessaires à la minimisation.
    
    Il y a 2 méthodes :
    - value    : renvoie la valeur de la fonction-coût, i.e. J
    - gradient : renvoie son gradient, i.e. grad(J)
    
    La fonction-coût choisie est une simple norme quadratique sur l'écart entre
    la variable de minimisation X et une valeur constante X0. Le gradient est
    donc de deux fois cet écart, et le minimum est atteint quand X=X0.
    """
    def __init__(self, X0 = None ):
        self.X0 = X0
        self.i  = 0
        logging.debug("")
        logging.debug("Initialisations pour J :")
        logging.debug("  X0 = %s"%self.X0)

    def value(self, X = None ):
        #
        self.i += 1
        #
        J = numpy.dot( ( X - self.X0 ), ( X - self.X0 ) )
        J = float( J )
        #
        logging.debug("")
        logging.debug("Etape de minimisation numéro %i"%self.i)
        logging.debug("------------------------------")
        logging.debug("Calcul de la valeur de J :")
        logging.debug("  X = %s"%X)
        logging.debug("  J = %s"%J)
        return J

    def gradient(self, X = None ):
        #
        gradJ = 2. * ( X - self.X0 )
        #
        logging.debug("Calcul du gradient de J :")
        logging.debug("  grad(J) = %s"%gradJ)
        return gradJ

    def iterations(self):
        return self.i

#===============================================================================
def test(precision = 1.e-07, dimension = 3):
    """
    Cas-test vérifiant que la minimisation CG de Scipy fonctionne
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
    # X_optimal, J_optimal, Informations
    X_optimal, J_optimal, func_calls, grad_calls, warnflag = scipy.optimize.fmin_cg(
        f      = J.value,
        x0     = X_initial,
        fprime = J.gradient,
        args   = (),
        gtol   = precision,
        full_output = True,
        )
    #
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
    if max(abs(GradJ_opt)) > precision:
        raise ValueError("Résultat du test erroné sur le gradient de J")
    elif J_optimal > precision:
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
