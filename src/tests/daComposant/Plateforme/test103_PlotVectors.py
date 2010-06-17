#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant l'affichage multi-pas Gnuplot d'une liste de vecteurs.
"""
__author__ = "Jean-Philippe ARGAUD - Juillet 2008"

execfile("context.py")

from AssimilationStudy import AssimilationStudy

#===============================================================================
def test(dimension = 100):
    """
    Cas-test vérifiant l'affichage multi-pas Gnuplot d'une liste de vecteurs.
    """
    #
    ADD = AssimilationStudy()
    #
    ADD.setDiagnostic("PlotVectors", "Affichage multi-pas Gnuplot d'une liste de vecteurs")
    #
    MonPlot = ADD.get("Affichage multi-pas Gnuplot d'une liste de vecteurs")
    #
    vect1 = [1, 2, 1, 2, 1]
    MonPlot.calculate([vect1,], title = "Vecteur 1", xlabel = "Axe X", ylabel = "Axe Y", pause = False )
    vect2 = [1, 3, 1, 3, 1]
    MonPlot.calculate([vect1,vect2], title = "Vecteurs 1 et 2", filename = "liste_de_vecteurs.ps", pause = False )
    vect3 = [-1, 1, -1, 1, -1]
    MonPlot.calculate((vect1,vect2,vect3), title = "Vecteurs 1 a 3", pause = False )
    vect4 = 100*[0.29, 0.97, 0.73, 0.01, 0.20]
    MonPlot.calculate([vect4,], title = "Vecteur 4 : long construit par repetition", pause = False )
    MonPlot.calculate(
        (vect1,vect2,vect3),
        [0.1,0.2,0.3,0.4,0.5],
        title = "Vecteurs 1 a 3, temps modifie", pause = False)
    print
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
