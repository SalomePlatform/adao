#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant l'affichage multi-pas Gnuplot d'un vecteur.
"""
__author__ = "Jean-Philippe ARGAUD - Juillet 2008"

from daCore.AssimilationStudy import AssimilationStudy

#===============================================================================
def test(dimension = 100):
    """
    Cas-test vérifiant l'affichage multi-pas Gnuplot d'un vecteur.
    """
    #
    ADD = AssimilationStudy()
    #
    ADD.setDiagnostic("PlotVector", "Affichage multi-pas Gnuplot d'un vecteur")
    #
    MonPlot = ADD.get("Affichage multi-pas Gnuplot d'un vecteur")
    #
    vect = [1, 2, 1, 2, 1]
    MonPlot.calculate(vect, title = "Vecteur 1", xlabel = "Axe X", ylabel = "Axe Y", pause = False )
    vect = [1, 3, 1, 3, 1]
    MonPlot.calculate(vect, title = "Vecteur 2", filename = "vecteur.ps", pause = False)
    vect = [-1, 1, 1, 1, -1]
    MonPlot.calculate(vect, title = "Vecteur 3", pause = False)
    vect = [0.29, 0.97, 0.73, 0.01, 0.20]
    MonPlot.calculate(vect, title = "Vecteur 4", pause = False)
    vect = [-0.23262176, 1.36065207,  0.32988102, 0.24400551, -0.66765848, -0.19088483, -0.31082575,  0.56849814,  1.21453443,  0.99657516]
    MonPlot.calculate(vect, title = "Vecteur 5", pause = False)
    vect = dimension*[0.29, 0.97, 0.73, 0.01, 0.20]
    MonPlot.calculate(vect, title = "Vecteur 6 : long construit par repetition", pause = False)
    vect = [0.29, 0.97, 0.73, 0.01, 0.20]
    MonPlot.calculate(vect, title = "Vecteur 7", pause = False)
    temps = [0.1,0.2,0.3,0.4,0.5]
    MonPlot.calculate(vect, temps, title = "Vecteur 8 avec axe du temps modifie", pause = False)
    #
    # Vérification du résultat
    # ------------------------
    print test.__doc__
    print "    Test correct"
    print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test()
