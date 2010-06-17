#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant le calcul de RMS.
"""
__author__ = "Jean-Philippe ARGAUD - Juillet 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(precision = 1.e-13):
    """
    Cas-test vérifiant des calculs de RMS.
    """
    #
    ADD = AssimilationStudy()
    #
    ADD.setDiagnostic("RMS", "Calcul de RMS multi-pas")
    #
    # La ligne suivante permet de simplifier les écritures ultérieures pour
    # les "calculate", mais n'est pas indispensable : on aurait pu conserver à
    # chaque appel la commande "ADD.get("...")"
    #
    RMS = ADD.get("Calcul de RMS multi-pas")
    #
    vect1 = [1, 2, 1, 2, 1]
    vect2 = [2, 1, 2, 1, 2]
    RMS.calculate(vect1,vect2)
    vect1 = [1, 3, 1, 3, 1]
    vect2 = [2, 2, 2, 2, 2]
    RMS.calculate(vect1,vect2)
    vect1 = [1, 1, 1, 1, 1]
    vect2 = [2, 2, 2, 2, 2]
    RMS.calculate(vect1,vect2)
    vect1 = [1, 1, 1, 1, 1]
    vect2 = [4, -2, 4, -2, -2]
    RMS.calculate(vect1,vect2)
    vect1 = [0.29, 0.97, 0.73, 0.01, 0.20]
    vect2 = [0.92, 0.86, 0.11, 0.72, 0.54]
    RMS.calculate(vect1,vect2)
    vect1 = [-0.23262176, 1.36065207,  0.32988102, 0.24400551, -0.66765848, -0.19088483, -0.31082575,  0.56849814,  1.21453443,  0.99657516]
    vect2 = [0,0,0,0,0,0,0,0,0,0]
    RMS.calculate(vect1,vect2)
    #
    Valeurs_attendues = [1.0, 1.0, 1.0, 3.0, 0.53162016515553656, 0.73784217096601323]
    #
    # Vérification du résultat
    # ------------------------
    ecart = abs( max( numpy.array(RMS.valueserie()) - numpy.array(Valeurs_attendues) ) )
    if ecart > precision:
        raise "Résultat du test erroné"
    else:
        print test.__doc__
        print "    Test correct, erreur maximale inférieure à %s"%precision
        print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    # numpy.random.seed(1000)
    
    test()
