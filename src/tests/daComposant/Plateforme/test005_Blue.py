#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant que si H est l'identité et que les matrices de covariance
    d'erreurs sont liées par R = alpha * B, alors l'ecart type de OMA est
    proportionnel a l'ecart type de l'innovation d selon la relation :
    rms(OMA)  = alpha/(1. + alpha) rms(d)
"""
__author__ = "Sophie RICCI - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(precision = 1.e-13, dimension = 3, alpha = 2.):
    """
    Cas-test vérifiant que si H est l'identité et que les matrices de covariance
    d'erreurs sont liées par R = alpha * B, alors l'ecart type de OMA est
    proportionnel a l'ecart type de l'innovation d selon la relation :
    rms(OMA)  = alpha/(1. + alpha) rms(d)
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
    B  = numpy.matrix(numpy.core.identity(dimension)).T
    R  = alpha * B
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
    xa = ADD.get("Analysis").valueserie(0)
    d  = ADD.get("Innovation").valueserie(0)
    #
    # Calcul RMS pour d et OMA
    # ------------------------
    ADD.setDiagnostic("RMS",
        name = "Calcul de la RMS sur l'innovation et OMA",
        )
    RMS = ADD.get("Calcul de la RMS sur l'innovation et OMA")
    #
    # La RMS de l'innovation d
    # ------------------------
    RMS.calculate(d,numpy.zeros(len(d)))
    # Le calcul ci-dessus doit être identique à : RMS.calculate(xb,yo)
    #
    # La RMS de l'écart OMA
    # ---------------------
    RMS.calculate(xa,yo)
    #
    # Vérification du résultat
    # ------------------------
    if (RMS.valueserie(1) - (alpha/(1. + alpha)) * RMS.valueserie(0)) > precision:
        raise ValueError("Résultat du test erroné")
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inférieure à %s"%precision
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test()
