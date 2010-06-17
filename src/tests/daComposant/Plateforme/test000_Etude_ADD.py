#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant que si les covariances d'erreur B et R sont identiques et
    unitaires, l'analyse est située au milieu de l'ébauche [0,1,2] et de
    l'observation [0.5,1.5,2.5].
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

import logging
# logging.getLogger().setLevel(logging.DEBUG)

#===============================================================================
def test(precision = 1.e-13):
    """
    Cas-test vérifiant que si les covariances d'erreur B et R sont identiques et
    unitaires, l'analyse est située au milieu de l'ébauche [0,1,2] et de
    l'observation [0.5,1.5,2.5].
    """
    #
    # Définition de l'étude d'assimilation
    # ------------------------------------
    ADD = AssimilationStudy("Ma premiere etude")
    #
    ADD.setBackground         (asVector     = [0,1,2])
    ADD.setBackgroundError    (asCovariance = "1 0 0;0 1 0;0 0 1")
    ADD.setObservation        (asVector     = [0.5,1.5,2.5])
    ADD.setObservationError   (asCovariance = "1 0 0;0 1 0;0 0 1")
    ADD.setObservationOperator(asMatrix     = "1 0 0;0 1 0;0 0 1")
    #
    ADD.setControls()
    ADD.setAlgorithm(choice="Blue")
    #
    ADD.analyze()
    #
    Xa = ADD.get("Analysis")
    print
    print "    Nombre d'analyses  :",Xa.stepnumber()
    print "    Analyse résultante :",Xa.valueserie(0)
    #
    # Vérification du résultat
    # ------------------------
    if max(numpy.array(Xa.valueserie(0))-numpy.array([0.25, 1.25, 2.25])) > precision:
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
