#-*-coding:iso-8859-1-*-
__doc__ = """
    Diagnostic sur les variances dans B et R par rapport à l'ébauche Xb et aux
    observations Y. On teste si on a les conditions :
        1%*xb < sigma_b < 10%*xb
            et
        1%*yo < sigma_o < 10%*yo
    lors d une anlayse BLUE.
"""
__author__ = "Sophie RICCI - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(dimension = 3):
    """
    Diagnostic sur les variances dans B et R par rapport à l'ébauche Xb et aux
    observations Y. On teste si on a les conditions :
        1%*xb < sigma_b < 10%*xb
            et
        1%*yo < sigma_o < 10%*yo
    lors d une anlayse BLUE.
    """
    #
    # Définition des données "théoriques" vraies
    # ------------------------------------------
    xt = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    Eo = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    Eb = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    #
    H  = numpy.matrix(numpy.core.identity(dimension))
    #
    xb = xt + Eb
    yo = H * xt + Eo
    #
    # Définition des matrices de covariances d'erreurs
    # ------------------------------------------------
    R  = 1.e-3 * yo.mean() * yo.mean() * numpy.matrix(numpy.core.identity(dimension))
    B  = 1.e-3 * xb.mean() * xb.mean() * numpy.matrix(numpy.core.identity(dimension))
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
    xa = numpy.array(ADD.get("Analysis").valueserie(0))
    d  = numpy.array(ADD.get("Innovation").valueserie(0))
    #
    # Application du test
    # -------------------
    ADD.setDiagnostic("VarianceOrder", name = "Ordre des matrices de covariance")
    #
    D = ADD.get("Ordre des matrices de covariance")
    #
    D.calculate( Xb = xb, B = B, Y = yo, R  = R )
    #
    # Verification du resultat
    # ------------------------
    if not D.valueserie(0) :
        raise ValueError("Resultat du test errone ")
    else :
        print test.__doc__
        print "    Test correct"
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test()
