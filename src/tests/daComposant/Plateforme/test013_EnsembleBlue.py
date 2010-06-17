#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant que si les covariances d'erreur B et R sont identiques et
    unitaires, l'analyse est située au milieu de l'ébauche [0,1,2] et de
    l'observation [0.5,1.5,2.5], avec une erreur d'un ordre inférieur à celle
    introduite dans R (si l'erreur est de 1 dans R, la précision de vérification
    est de 0.1*0.1).
"""
__author__ = "Jean-Philippe ARGAUD - Novembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy
import Persistence

import logging
# logging.getLogger().setLevel(logging.DEBUG)

#===============================================================================
def test(precision = 1.e-2):
    """
    Cas-test vérifiant que si les covariances d'erreur B et R sont identiques et
    unitaires, l'analyse est située au milieu de l'ébauche [0,1,2] et de
    l'observation [0.5,1.5,2.5], avec une erreur d'un ordre inférieur à celle
    introduite dans R (si l'erreur est de 1 dans R, la précision de vérification
    est de 0.1*0.1).
    """
    #
    # Définition de l'étude d'assimilation
    # ------------------------------------
    ADD = AssimilationStudy("Ma premiere etude")
    #
    Xb = Persistence.OneVector("Ebauche", basetype=numpy.matrix)
    for i in range(100):
        Xb.store( numpy.matrix( [0,10,20], numpy.float ).T )
    #
    ADD.setBackground         (asPersistentVector = Xb )
    ADD.setBackgroundError    (asCovariance = "1 0 0;0 1 0;0 0 1")
    ADD.setObservation        (asVector     = [0.5,10.5,20.5])
    ADD.setObservationError   (asCovariance = "1 0 0;0 1 0;0 0 1")
    ADD.setObservationOperator(asMatrix     = "1 0 0;0 1 0;0 0 1")
    #
    ADD.setControls()
    ADD.setAlgorithm(choice="EnsembleBlue")
    #
    ADD.analyze()
    #
    Xa = ADD.get("Analysis")
    Analyse_moyenne = numpy.matrix( Xa.valueserie() ).mean(axis=0).A1
    print
    print "    Ebauche            :",[0,1,2]
    print "    Analyse moyenne    :",Analyse_moyenne
    print "    Nombre d'analyses  :",Xa.stepnumber()
    #
    # Vérification du résultat
    # ------------------------
    if max(Analyse_moyenne-numpy.array([0.25, 10.25, 20.25]))/10 > precision:
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
    numpy.random.seed(1000)
    
    test()
