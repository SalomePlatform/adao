#-*-coding:iso-8859-1-*-
__doc__ = """
    Test d adequation des distributions de OMB et OMA avec une distribution 
    gaussienne dont la moyenne et la std sont calculees sur l echantillon.
    L analyse est un Blue.
"""
__author__ = "Sophie RICCI - Septembre 2008"

execfile("context.py")

import numpy
from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(dimension = 10):
    """
    Test d adequation des distributions de OMB et OMA avec une distribution 
    gaussienne dont la moyenne et la std sont calculees sur l echantillon.
    L analyse est un Blue.
    """
    #
    # Définition des données "théoriques" vraies
    # ------------------------------------------
    xt = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension))).T
    Eo = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension))).T
    Eb = numpy.matrix(numpy.random.normal(0.,1.,size=(dimension))).T
    H  = numpy.matrix(numpy.identity(dimension))
    xb = xt + Eb
    yo = H * xt + Eo
    xb = xb.A1
    yo = yo.A1
    # Définition des matrices de covariances d'erreurs
    # ------------------------------------------------
    R  = numpy.matrix(numpy.identity(dimension)).T
    B  = numpy.matrix(numpy.identity(dimension)).T
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
    OMA  = yo - xa
    
    #
    # Application du test d adequation du Khi-2 
    # -------------------------------------------------
    ADD.setDiagnostic("GaussianAdequation",
        name = "Test d adequation a une gaussienne par calcul du khi2",
        parameters = { "tolerance":0.05, "nbclasses":8., "dxclasse":None })
    #
    # Instanciation de l'objet testkhi2
    # --------------------------------------------------------------------
    D = ADD.get("Test d adequation a une gaussienne par calcul du khi2")
    #
    # Calcul
    # --------------------------------------------------------------------
    print test.__doc__
    D.calculate(d)
    if not D.valueserie(0) :
        raise ValueError("L'adéquation à une gaussienne pour la variable OMB n'est pasvalide.")
    else :
        print "    L'adéquation à une gaussienne pour la variable OMB est valide."
    D.calculate(OMA)
    if not D.valueserie(1) :
        raise ValueError("L'adéquation à une gaussienne pour la variable OMA n'est pasvalide.")
    else :
        print "    L'adéquation à une gaussienne pour la variable OMA est valide."
    print

#==============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test()
