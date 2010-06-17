#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test v�rifiant que si les covariances d'erreur B et R sont identiques et
    unitaires, l'analyse est situ�e au milieu de l'�bauche [0,1,2] et de
    l'observation [0.5,1.5,2.5].
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

import logging
#�logging.getLogger().setLevel(logging.DEBUG)

#===============================================================================
def test(precision = 1.e-13):
    """
    Cas-test v�rifiant que si les covariances d'erreur B et R sont identiques et
    unitaires, l'analyse est situ�e au milieu de l'�bauche [0,1,2] et de
    l'observation [0.5,1.5,2.5].
    """
    #
    # D�finition de l'�tude d'assimilation
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
    print "    Analyse r�sultante :",Xa.valueserie(0)
    #
    # V�rification du r�sultat
    # ------------------------
    if max(numpy.array(Xa.valueserie(0))-numpy.array([0.25, 1.25, 2.25])) > precision:
        raise ValueError("R�sultat du test erron�")
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inf�rieure � %s"%precision
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test()
