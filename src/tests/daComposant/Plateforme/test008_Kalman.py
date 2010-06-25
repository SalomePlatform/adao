#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test vérifiant le fonctionnement du filtre de Kalman sur un système
    dynamique de trajectoire 1D constante
"""
__author__ = "Jean-Philippe ARGAUD - Septembre 2008"

import numpy
from daCore.AssimilationStudy import AssimilationStudy
from daCore.Persistence       import OneScalar

#===============================================================================
def test(dimension = 3):
    """
    Cas-test vérifiant le fonctionnement du filtre de Kalman sur un système
    dynamique de trajectoire 1D constante
    """
    print test.__doc__
    #
    # Définition des données
    # ----------------------
    a_size = (dimension,)
    #
    # Valeur vraie
    xt = -0.4
    Xt = OneScalar("Valeur vraie", basetype=float)
    Xt.store(xt)
    for i in range(dimension):
        Xt.store(xt)
    #
    # Observations bruitées
    yo = numpy.random.normal(xt, 0.1, size=a_size)
    Yo = OneScalar("Observations", basetype=float)
    Yo.store(0.)
    for v in yo:
        Yo.store(v)
    #
    # Création de l'étude et résolution
    # ---------------------------------
    ADD = AssimilationStudy("Assimilation temporelle de Kalman")
    #
    ADD.setBackground         (asVector     = "0.")
    ADD.setBackgroundError    (asCovariance = "1.")
    #
    ADD.setObservationOperator(asMatrix     = "1.")
    ADD.setObservation        (asPersistentVector = Yo)
    ADD.setObservationError   (asCovariance = "1.e-2")
    #
    ADD.setEvolutionModel     (asMatrix     = "1")
    ADD.setEvolutionError     (asCovariance = "1.e-5")
    #
    ADD.setControls()
    ADD.setAlgorithm(choice="Kalman")
    #
    ADD.analyze()
    #
    Xa = ADD.get("Analysis")
    print "    Valeur vraie visée........................:",xt
    print "    Ebauche, i.e. valeur initiale d'analyse...:",Xa.valueserie(0)[0]
    print "    Nombre d'analyses (sans l'ébauche)........:",Xa.stepnumber()-1
    print "    Moyenne des analyses......................:",Xa.stepmean()
    #
    # Biais des erreurs
    EpsY = []
    for i in range(Yo.stepnumber()):
        EpsY.append(Yo.valueserie(i) - Xt.valueserie(i))
    print "    Biais des erreurs <Obs-Vraie>.............:",numpy.array(EpsY).mean()
    print "    Variance des erreurs <Obs-Vraie>..........:",numpy.array(EpsY).var()
    EpsY = []
    for i in range(Xa.stepnumber()):
        EpsY.append(Xa.valueserie(i)[0] - Xt.valueserie(i))
    print "    Biais des erreurs <Ana-Vraie>.............:",numpy.array(EpsY).mean()
    print "    Variance des erreurs <Ana-Vraie>..........:",numpy.array(EpsY).var()
    print
    #
    ADD.setDiagnostic("PlotVectors", "Affichage de Xa et Xt")
    MonPlot = ADD.get("Affichage de Xa et Xt")
    MonPlot.calculate(
        ( [ x[0] for x in Xa.valueserie()], Xt.valueserie(), Yo.valueserie() ),
        title = "Analyse de Kalman sur trajectoire constante",
        ltitle = ["Analyse", "Valeur vraie", "Observations"],
        filename = "kalman_sur_trajectoire_constante.ps",
        pause = False,
        )

#===============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    numpy.random.seed(1000)

    test(100)
