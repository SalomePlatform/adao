#-*-coding:iso-8859-1-*-
__doc__ = """
    V�rification de la r�duction de variance op�r�e par un BLUE lors de
    l'analyse
"""
__author__ = "Sophie RICCI - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(dimension = 10):
    """
    Cas-test v�rifiant que l'analyse BLUE permet de r�duire la variance entre
    les �carts OMB et les �carts OMA
    """
    #
    # D�finition des donn�es "th�oriques" vraies
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
    xb = xb
    yo = yo
    #
    # D�finition des matrices de covariances d'erreurs
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
    OMA  = yo.A1 -  xa
    #
    # Application du test
    # -------------------
    ADD.setDiagnostic("ReduceVariance",
        name = "Reduction de la variance entre OMB et OMA")
    #
    D = ADD.get("Reduction de la variance entre OMB et OMA")
    #
    D.calculate( vectorOMB = d, vectorOMA = OMA )
    #
    # V�rification du r�sultat
    # ------------------------
    if not D.valueserie(0) :
        raise ValueError("R�sultat du test erron� (1)")
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
