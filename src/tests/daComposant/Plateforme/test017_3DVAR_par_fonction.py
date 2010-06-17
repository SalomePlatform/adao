#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test v�rifiant sur le 3D-VAR que si l'erreur d'observation est nulle, on
    trouve comme analyse la demi-somme de l'�bauche et de la valeur vraie.
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2009"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy
import Persistence

import logging
# Si on d�sire plus d'information sur le d�roulement du calcul, on peut
# d�commenter l'une des lignes qui suit :
# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG)

#===============================================================================
def test(precision = 1.e-10, dimension = 3):
    """
    Cas-test v�rifiant sur le 3D-VAR que si l'erreur d'observation est nulle, on
    trouve comme analyse la demi-somme de l'�bauche et de la valeur vraie.
    """
    #
    # D�finition des donn�es
    # ----------------------
    xt = numpy.matrix(numpy.arange(dimension)).T
    Eo = numpy.matrix(numpy.zeros((dimension,))).T
    #�Eo = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    #�Eb = numpy.matrix(numpy.zeros((dimension,))).T
    Eb = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension,))).T
    #
    H  = numpy.matrix(numpy.core.identity(dimension))
    #
    # D�finition de l'effet de l'op�rateur H comme une fonction
    # ---------------------------------------------------------
    def FunctionH( X ):
        return H * X
    def AdjointH( (X, Y) ):
        return H.T * Y
    #
    xb = xt + Eb
    yo = FunctionH( xt ) + Eo
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
    ADD.setObservationOperator(asFunction   = {"Direct":FunctionH,
                                               "Tangent":FunctionH,
                                               "Adjoint":AdjointH} )
    #
    ADD.setAlgorithm(choice="3DVAR")
    #
    ADD.analyze()
    #
    xa = numpy.array(ADD.get("Analysis").valueserie(0))
    d  = numpy.array(ADD.get("Innovation").valueserie(0))
    #
    # V�rification du r�sultat
    # ------------------------
    if max(abs(xa - (xb+xt.A1)/2)) > precision:
        raise ValueError("R�sultat du test erron� (1)")
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inf�rieure � %s"%precision
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    numpy.random.seed(1000)
    
    test(dimension = 300)
