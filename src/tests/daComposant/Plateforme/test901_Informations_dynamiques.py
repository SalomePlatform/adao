#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant les messages de sortie pour toutes les informations
    dynamiques
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

execfile("context.py")

from AssimilationStudy import AssimilationStudy

#===============================================================================
def test():
    """
    Cas-test vérifiant les messages de sortie pour toutes les informations
    dynamiques
    """
    #
    # Définition de l'étude d'assimilation
    # ------------------------------------
    ADD = AssimilationStudy("Verifications des informations dynamiques")
    #
    print test.__doc__
    # print "Chemin des algorithmes  :",ADD.get_algorithms_main_path()
    print "Algorithmes disponibles :",ADD.get_available_algorithms()
    print
    # print "Chemin des diagnostics  :",ADD.get_diagnostics_main_path()
    print "Diagnostics disponibles :",ADD.get_available_diagnostics()
    print
    chemin = "../../Sources"
    print "Ajout du chemin         :",chemin
    ADD.add_algorithms_path(chemin)
    print "Algorithmes disponibles :",ADD.get_available_algorithms()
    print
    print "Ajout du chemin         :",chemin
    ADD.add_diagnostics_path(chemin)
    print "Diagnostics disponibles :",ADD.get_available_diagnostics()
    print
    ADD.setAlgorithm(choice=ADD.get_available_algorithms()[0])
    liste = ADD.get().keys()
    liste.sort()
    print "Variables et diagnostics disponibles :",liste
    print

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    test()
