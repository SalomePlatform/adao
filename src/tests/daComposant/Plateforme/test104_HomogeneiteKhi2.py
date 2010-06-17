#-*-coding:iso-8859-1-*-
__doc__ = """
    Test d'homogenéité des distributions de OMB et OMA lors d'une analyse Blue
"""
__author__ = "Sophie RICCI - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(dimension = 75):
    """
    Test d'homogenéité des distributions de OMB et OMA lors d'une analyse Blue
    """
    numpy.random.seed(1000)
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
    xa = numpy.array(ADD.get("Analysis").valueserie(0))
    d  = numpy.array(ADD.get("Innovation").valueserie(0))
    OMA = yo - xa
    #
    # Application du test d'adéquation du Khi-2 
    # -----------------------------------------
    ADD.setDiagnostic("HomogeneiteKhi2",
        name = "Test d'homogeneite entre OMB et OMA par calcul du khi2",
        parameters = { "tolerance":0.05, "nbclasses":8 , "dxclasse":None})
    #
    # Instanciation de l'objet testkhi2
    # ---------------------------------
    D = ADD.get("Test d'homogeneite entre OMB et OMA par calcul du khi2")
    #
    # Calcul du test et résultat
    # --------------------------
    D.calculate(d, OMA)
    print "    Reponse du test", D.valueserie()
    print

#==============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test()
