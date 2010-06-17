#-*-coding:iso-8859-1-*-
__doc__ = """
    Diagnotic de test sur la validité de l'hypothèse de linéarité de l'opérateur
    H entre xp et xm
"""
__author__ = "Jean-Philippe ARGAUD - Octobre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(tolerance = 0.1, dimension = 3):
    """
    Diagnotic de test sur la validité de l'hypothèse de linéarité de l'opérateur
    H entre xp et xm
    """
    #
    # Définition des données
    # ----------------------
    dxparam = 1. 
    Hxm = numpy.random.normal(0.,1.,size=(dimension,))
    Hxp = Hxm + 2*dxparam
    Hx = (Hxp + Hxm)/2.
    H =  (Hxp - Hxm)/2.
    #
    # Instanciation de l'objet diagnostic
    # -----------------------------------
    ADD = AssimilationStudy()
    ADD.setDiagnostic("HLinearity",
        name = "Test le linearite de Hlin",
        parameters = { "tolerance":tolerance })
    D = ADD.get("Test le linearite de Hlin")
    #
    # Calcul 
    # ------
    D.calculate(
        Hlin = H,
        deltaparam = dxparam,
        Hxp  = Hxp,
        Hxm  = Hxm,
        Hx   = Hx)
    #
    # Vérification du résultat
    # ------------------------
    if not D.valueserie(0) :
        raise ValueError("Résultat du test erroné")
    else:
        print test.__doc__
        print "    Test correct, tolerance du test fixée à %s"%tolerance
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    numpy.random.seed(1000)
    
    test(dimension = 1.e4) # Fonctionne bien jusqu'à 1.e7
