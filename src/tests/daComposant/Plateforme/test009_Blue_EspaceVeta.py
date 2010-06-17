#-*-coding:iso-8859-1-*-
__doc__ = """
    Vérification du calcul de BLUE dans l'espace des états plutôt que dans
    l'espace des observations.
"""
__author__ = "Sophie RICCI - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(precision = 1.e-13):
    """
    Vérification du calcul de BLUE dans l'espace des états plutôt que dans
    l'espace des observations.
    """
    #
    # Définition des données 
    # ------------------------------------------
    H  = numpy.matrix(([1., 1.])).T
    #
    xb = 6.
    xt = 3.
    yo = H * xt 
    #
    dimension = yo.size
    #
    # Définition des matrices de covariances d'erreurs
    # ------------------------------------------------
    B = numpy.matrix(([1.]))
    R  = numpy.matrix(numpy.core.identity(dimension)).T
    #
    # Analyse BLUE
    # ------------
    ADD = AssimilationStudy()
    ADD.setBackground         (asVector     = xb )
    ADD.setBackgroundError    (asCovariance = B )
    ADD.setObservation        (asVector     = yo )
    ADD.setObservationError   (asCovariance = R )
    ADD.setObservationOperator(asMatrix     = H )
    #
    ADD.setControls()
    ADD.setAlgorithm(choice="Blue")
    #
    ADD.analyze()
    #
    d = numpy.array(ADD.get("Innovation").valueserie(0))
    xa = numpy.array(ADD.get("Analysis").valueserie(0))
    #
    # Vérification du résultat
    # ------------------------
    if max(abs(xa - 4.)) > precision:
        raise ValueError("Résultat du test erroné")
    else:
        print test.__doc__
        print "    L'analyse Blue dans l'espace de contrôle est correcte."
        print "    Test correct, erreur maximale inférieure à %s"%precision
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test()
