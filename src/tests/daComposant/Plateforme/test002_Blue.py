#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test v�rifiant que l'application des coefficients de correction so et sb
    conduit � des matrices R et B pour lesquelles ces coefficients sont unitaires.
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(precision = 1.e-13, dimension = 3):
    """
    Cas-test v�rifiant que l'application des coefficients de correction so et sb
    conduit � des matrices R et B pour lesquelles ces coefficients sont unitaires.
    """
    #
    # D�finition des donn�es "th�oriques" vraies
    # ------------------------------------------
    xt = numpy.matrix(numpy.arange(dimension)).T
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
    # D�finition des matrices d'erreurs
    # ---------------------------------
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
    xa        = numpy.array(ADD.get("Analysis").valueserie(0))
    d         = numpy.array(ADD.get("Innovation").valueserie(0))
    SigmaObs2 = float( numpy.dot(d,(yo-numpy.dot(H,xa)).A1) / R.trace() )
    SigmaBck2 = float( numpy.dot(d,numpy.dot(H,(xa - xb)).A1) /(H * B * H.T).trace() )
    #
    # Analyse BLUE avec correction des matrices R et B
    # Attention : ce second calcul de BLUE avec le meme objet ADD
    #             conduit � stocker les r�sultats dans le second step,
    #             donc il faut appeller "valueserie(1)"
    # ------------------------------------------------
    ADD.setBackgroundError (asCovariance = SigmaBck2*B )
    ADD.setObservationError(asCovariance = SigmaObs2*R )
    ADD.analyze()
    new_xa        = numpy.array(ADD.get("Analysis").valueserie(1))
    new_d         = numpy.array(ADD.get("Innovation").valueserie(1))
    new_SigmaObs2 = float( numpy.dot(new_d,(yo-numpy.dot(H,new_xa)).A1) / (SigmaObs2*R.trace()) )
    new_SigmaBck2 = float( numpy.dot(new_d,numpy.dot(H,(new_xa - xb)).A1) /(H * (SigmaBck2*B) * H.T).trace() )
    #
    # V�rification du r�sultat
    # ------------------------
    if max(abs(xa - new_xa)) > precision:
        raise ValueError("R�sultat du test erron� (1)")
    elif max(abs(d - new_d)) > precision:
        raise ValueError("R�sultat du test erron� (2)")
    elif abs(new_SigmaObs2-1.) > precision:
        print "new_SigmaObs2 =",new_SigmaObs2
        raise ValueError("R�sultat du test erron� (3)")
    elif abs(new_SigmaBck2-1.) > precision :
        print "new_SigmaBck2 =",new_SigmaBck2
        raise ValueError("R�sultat du test erron� (4)")
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
