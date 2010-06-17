#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant que si l'erreur sur le background est nulle et que
    l'erreur sur les observations est connue, alors l'analyse donne le "milieu"
    du background et des observations.
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(precision = 1.e-13, dimension = 3):
    """
    Cas-test vérifiant que si l'erreur sur le background est nulle et que
    l'erreur sur les observations est connue, alors l'analyse donne le "milieu"
    du background et des observations.
    """
    #
    # Définition des données "théoriques" vraies
    # ------------------------------------------
    xt = numpy.matrix(numpy.arange(dimension)).T
    Eo = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    Eb = numpy.matrix(numpy.zeros((dimension,))).T
    #
    H  = numpy.matrix(numpy.core.identity(dimension))
    #
    xb = xt + Eb
    yo = H * xt + Eo
    #
    xb = xb.A1
    yo = yo.A1
    #
    # Définition des matrices de covariances d'erreurs
    # ------------------------------------------------
    R  = numpy.matrix(numpy.core.identity(dimension)).T
    B  = numpy.matrix(numpy.core.identity(dimension)).T
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
    Xa = ADD.get("Analysis")
    xa        = numpy.matrix(Xa.valueserie(0)).T
    SigmaObs2 = ADD.get("SigmaObs2")
    SigmaBck2 = ADD.get("SigmaBck2")
    d         = ADD.get("Innovation")
    #
    # Vérification du résultat
    # ------------------------
    if max(abs(xa.A1 - xb - Eo.A1/2.)) > precision:
        raise ValueError("Résultat du test erroné (1)")
    elif max(abs(yo - (H * xa).A1 - Eo.A1/2.)) > precision:
        raise ValueError("Résultat du test erroné (2)")
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inférieure à %s"%precision
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    # numpy.random.seed(1000)
    
    test(dimension = 100)
