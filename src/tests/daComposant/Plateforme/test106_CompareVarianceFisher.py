#-*-coding:iso-8859-1-*-
__doc__ = """
    Test d'égalité des variances de OMB et OMA lors d'une analyse Blue 
    au sens du test de Fisher.
"""
__author__ = "Sophie RICCI - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(dimension = 500):
    """
    Test d'égalité des variances de OMB et OMA lors d'une analyse Blue 
    au sens du test de Fisher.
    """
    #
    # Définition des données "théoriques" vraies
    # ------------------------------------------
    xt = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    Eo = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    Eb = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    H  = numpy.matrix(numpy.identity(dimension))
    xb = xt + Eb
    yo = H * xt + Eo
    xb = xb.A1
    yo = yo.A1
    #
    # Définition des matrices de covariances d'erreurs
    # ------------------------------------------------
    R  = 1000. * numpy.matrix(numpy.identity(dimension)).T
    B  = numpy.matrix(numpy.identity(dimension)).T
    #
    # Analyse BLUE
    # ------------
    ADD = AssimilationStudy()
    ADD.setBackground         (asVector     = xb )
    ADD.setBackgroundError    (asCovariance = B )
    ADD.setObservation        (asVector     = yo )
    ADD.setObservationError   (asCovariance = R )
    ADD.setObservationOperator(asMatrix     = H )
    ADD.setControls()
    ADD.setAlgorithm(choice="Blue")
    ADD.analyze()
    xa = numpy.array(ADD.get("Analysis").valueserie(0))
    d  = numpy.array(ADD.get("Innovation").valueserie(0))
    OMA  = yo - xa
    #
    # Application du test d adequation du Khi-2 
    # -----------------------------------------
    ADD.setDiagnostic("CompareVarianceFisher",
        name = "Test de comparaison des variances de OMB et OMA par test de Fisher",
        parameters = { "tolerance":0.05 })
    #
    # Instanciation du diagnostic
    # ---------------------------
    D = ADD.get("Test de comparaison des variances de OMB et OMA par test de Fisher")
    #
    # Calcul
    # ------
    D.calculate(d, OMA)
    if not D.valueserie(0) :
            raise ValueError("L'analyse ne change pas de manière significative la variance. Le test est erroné.")
    else :
            print test.__doc__
            print "    L'analyse effectuée change de manière significative la variance."
            print "    Test correct"
            print 

#==============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="

    test()
