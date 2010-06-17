#-*-coding:iso-8859-1-*-
__doc__ = """
    Cas-test calculant par 3D-VAR l'analyse d'expériences avec Code_Aster.

    ============================================================================
    Script à lancer avec l'environnement ASTER+SALOME4 surchargé par SALOME5.Dev
    ============================================================================
"""
__author__ = "Jean-Philippe ARGAUD - Octobre 2009"
import sys, numpy
print "Numpy version",numpy.version.version
print
#
from N_Parameters import debug
#
# Récupération du point courant et des bornes
# -------------------------------------------
from N_MR_Parameters import parametres
xb = []
Bornes = []
for parametre in parametres:
    xb.append( parametre[1] )
    Bornes.append( parametre[2:4] )
if debug:
    print
    print "Ebauche = ",xb
    print "Bornes  = ",Bornes
    print
#
# Récupération des valeurs d'observation
# --------------------------------------
from N_MR_Parameters import experience
nbmesures = 11 # De 0 à 1 par pas de 0.1
instants = numpy.array([0.1*i for i in range(nbmesures)])
yo = []
for reponse in experience:
    for t,v in list(reponse):
        if min(abs(t - instants)) < 1.e-8:
            yo.append(v)
            # print t,'===>',v
if debug:
    print "Observations = ",yo
    print
#
# Definition des matrices de covariances d'erreurs
# ------------------------------------------------
B  = numpy.matrix(numpy.core.identity(len(xb)))
alpha  = 1.e14
B[0,0] = alpha * 100
B[1,1] = alpha * 10
B[2,2] = alpha * 1
R  = numpy.matrix(numpy.core.identity(len(yo)))
#
# Chargement des fonctions donnant accès à ASTER
# ----------------------------------------------
from N_Code_Aster_dist import Calcul_Aster_Ponctuel, Calcul_Aster_Adjoint
#
# Coeur de l'algorithme
# ---------------------
import numpy

import sys, os
sys.path.insert(0, "../../Sources/daCore")
sys.path.insert(0, "../../ComposantAD/daCore")
from AssimilationStudy import AssimilationStudy
import logging
# Si on désire plus d'information sur le déroulement du calcul, on peut
# décommenter l'une des lignes qui suit :
# logging.getLogger().setLevel(logging.INFO)
if debug:
    logging.getLogger().setLevel(logging.DEBUG)

def calculation( Yo, B, R, FunctionH, TangentH, AdjointH, Xb, Bounds ):
    #
    # Remise en place des matrices
    # -------------------
    dimensionXb = len( Xb )
    dimensionYo = len( Yo )
    B = numpy.matrix( B, numpy.float ).reshape((dimensionXb,dimensionXb))
    R = numpy.matrix( R, numpy.float ).reshape((dimensionYo,dimensionYo))
    #
    # Analyse
    # -------
    ADD = AssimilationStudy()
    ADD.setBackground         (asVector     = Xb )
    ADD.setBackgroundError    (asCovariance = B )
    ADD.setObservation        (asVector     = Yo )
    ADD.setObservationError   (asCovariance = R )
    ADD.setObservationOperator(asFunction   = {"Direct":FunctionH,
                                               "Tangent":TangentH,
                                               "Adjoint":AdjointH} )
    #
    ADD.setAlgorithm(choice="3DVAR")
    ADD.setAlgorithmParameters(asDico={
        "Minimizer"           : "LBFGSB",
        "Bounds"              : Bounds,
        })
    #
    ADD.analyze()
    #
    Xa = ADD.get("Analysis").valueserie(0)
    Innovation = ADD.get("Innovation").valueserie(0)
    A = []
    J = ADD.get("CostFunctionJ").valueserie()
    #
    ADD.setDiagnostic("PlotVectors", "J")
    MonPlot = ADD.get("J")
    MonPlot.calculate([J,ADD.get("CostFunctionJb").valueserie(),ADD.get("CostFunctionJo").valueserie()],
        title = "Fonctionnelles J, Jb et Jo",
        ltitle = ["J","Jb","Jo"],
        xlabel = "Pas", ylabel = "Valeur",
        filename = "recherche_xx_Fonctionnelles.ps",
        pause = False )
    #
    return Xa, A, Innovation, J

xa, A, Innovation, J = calculation(
    yo, B, R,
    Calcul_Aster_Ponctuel,
    Calcul_Aster_Ponctuel,
    Calcul_Aster_Adjoint,
    xb, Bornes)

# Calcul de la RMS
# ----------------
Hxa = Calcul_Aster_Ponctuel( xa )
V1 = numpy.array(Hxa)
V2 = numpy.array(yo)
import math
rms = math.sqrt( ((V2 - V1)**2).sum() / float(V1.size) )

print
print "========="
print "Ebauche = ",xb
print "Analyse = ",xa
print "RMS     = ",rms
print
print "NbSteps = ",len(J)
print "J       = ",J
print
print "B[0,0]  = ",B[0,0]
print "B[1,1]  = ",B[1,1]
print "B[2,2]  = ",B[2,2]
print "Bornes  = ",Bornes
print "========="
print


