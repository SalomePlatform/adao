#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test v�rifiant sur le Blue que si l'erreur est nulle, l'incr�ment
    d'analyse est nul.
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

import numpy
from daCore.AssimilationStudy import AssimilationStudy

#===============================================================================
def test(precision = 1.e-13, dimension = 3):
    """
    Cas-test v�rifiant sur le Blue que si l'erreur est nulle, l'incr�ment
    d'analyse est nul.
    """
    #
    # D�finition des donn�es
    # ----------------------
    xt = numpy.matrix(numpy.arange(dimension)).T
    Eo = numpy.matrix(numpy.zeros((dimension,))).T
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
    # D�finition des matrices de covariances d'erreurs
    # ------------------------------------------------
    R  = numpy.matrix(numpy.core.identity(dimension)).T
    B  = numpy.matrix(numpy.core.identity(dimension)).T
    #
    # Analyse
    # -------
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
    # V�rification du r�sultat
    # ------------------------
    if max(abs(xa - xb)) > precision:
        raise ValueError("R�sultat du test erron� (1)")
    elif max(abs(d)) > precision:
        raise ValueError("R�sultat du test erron� (2)")
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inf�rieure � %s"%precision
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    #�numpy.random.seed(1000)
    
    test(dimension = 100)
