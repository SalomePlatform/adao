#-*-coding:iso-8859-1-*-
__doc__ = """
    Analyse moindre carres sans ebauche
"""
__author__ = "Sophie RICCI, Jean-Philippe ARGAUD - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy
#===============================================================================
def test(dimension = 100, precision = 1.e-13):
    """
    Analyse moindre carres sans ebauche
    """
    #
    # Définition des données "théoriques" vraies
    # ------------------------------------------
    xt = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    H  = numpy.identity(dimension)
    yo = H * xt
    #
    # Définition des matrices de covariances d'erreurs
    # ------------------------------------------------
    R  = numpy.identity(dimension)
    #
    # Analyse BLUE
    # ------------
    ADD = AssimilationStudy()
    # Les valeurs de xb et B ne sont pas utilisées dans l'algorithme 
    # pour lequel on ne considere pas d'ébauche
    ADD.setBackground         (asVector     = numpy.zeros((dimension,)) )
    ADD.setBackgroundError    (asCovariance = numpy.zeros((dimension,dimension)) )
    ADD.setObservation        (asVector     = yo )
    ADD.setObservationError   (asCovariance = R )
    ADD.setObservationOperator(asMatrix     = H )
    #
    ADD.setControls()
    #
    ADD.setAlgorithm(choice="LinearLeastSquares")
    #
    ADD.analyze()
    #
    xa = ADD.get("Analysis").valueserie(0)
    if max(abs(xa - xt.A1)) > precision :
        raise ValueError("Resultat du test errone")
    else :
        print test.__doc__
        print "    Test correct"
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test(3)
