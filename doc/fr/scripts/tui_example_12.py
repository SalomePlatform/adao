# -*- coding: utf-8 -*-
#
from matplotlib import pyplot as plt
from numpy import array, set_printoptions
from adao import adaoBuilder
set_printoptions(precision=4, floatmode="fixed")
#
#-------------------------------------------------------------------------------
#
case = adaoBuilder.New()
case.set( "AlgorithmParameters",
    Algorithm="3DVAR",
    Parameters = {
        "StoreSupplementaryCalculations":[
            "CostFunctionJ",
            "CurrentState",
            "InnovationAtCurrentState",
        ],
    }
)
case.set( "Background",          Vector=[0, 1, 2] )
case.set( "BackgroundError",     ScalarSparseMatrix=1.0 )
case.set( "Observation",         Vector=array([0.5, 1.5, 2.5]) )
case.set( "ObservationError",    DiagonalSparseMatrix="1 1 1" )
case.set( "ObservationOperator", Matrix="1 0 0;0 2 0;0 0 3" )
case.set( "Observer",
    Variable="CurrentState",
    Template="ValuePrinter",
    Info="  État courant :",
)
#
print("Affichage des valeurs de l'état courant, à chaque pas :")
case.execute()
print("")
#
#-------------------------------------------------------------------------------
#
print("Indicateurs sur les écarts (ou erreurs) calculs-mesures")
print("     (affichage des 3 premiers pas uniquement)")
print("")
CalculMeasureErrors = case.get("InnovationAtCurrentState")
#
print("===> Maximum de l'erreur entre calculs et mesures, à chaque pas :")
print("    ",array(
    CalculMeasureErrors.maxs()
    [0:3] ))
print("===> Minimum de l'erreur entre calculs et mesures, à chaque pas :")
print("    ",array(
    CalculMeasureErrors.mins()
    [0:3] ))
print("===> Norme de l'erreur entre calculs et mesures, à chaque pas :")
print("    ",array(
    CalculMeasureErrors.norms()
    [0:3] ))
print("===> Erreur absolue moyenne (MAE) entre calculs et mesures, à chaque pas :")
print("    ",array(
    CalculMeasureErrors.maes()
    [0:3] ))
print("===> Erreur quadratique moyenne (MSE) entre calculs et mesures, à chaque pas :")
print("    ",array(
    CalculMeasureErrors.mses()
    [0:3] ))
print("===> Racine de l'erreur quadratique moyenne (RMSE) entre calculs et mesures, à chaque pas :")
print("    ",array(
    CalculMeasureErrors.rmses()
    [0:3] ))
#
#-------------------------------------------------------------------------------
#
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (8, 12)
#
plt.figure()
plt.suptitle("Indicateurs construits sur valeur courante des écarts (ou erreurs) calculs-mesures\n", fontweight="bold")
plt.subplot(611)
plt.plot(CalculMeasureErrors.maxs(), "bx--", label="Indicateur au pas courant")
plt.ylabel("Maximum (u.a.)")
plt.legend()
plt.subplot(612)
plt.plot(CalculMeasureErrors.mins(), "bx--", label="Indicateur au pas courant")
plt.ylabel("Minimum (u.a.)")
plt.legend()
plt.subplot(613)
plt.plot(CalculMeasureErrors.norms(), "bx-", label="Indicateur au pas courant")
plt.ylabel("Norme (u.a.)")
plt.legend()
plt.subplot(614)
plt.plot(CalculMeasureErrors.maes(), "kx-", label="Indicateur au pas courant")
plt.ylabel("MAE (u.a.)")
plt.legend()
plt.subplot(615)
plt.plot(CalculMeasureErrors.mses(), "gx-", label="Indicateur au pas courant")
plt.ylabel("MSE (u.a.)")
plt.legend()
plt.subplot(616)
plt.plot(CalculMeasureErrors.rmses(), "rx-", label="Indicateur au pas courant")
plt.ylabel("RMSE (u.a.)")
plt.legend()
plt.xlabel("Pas de calcul de la grandeur (numéro ou rang du pas)")
plt.tight_layout()
plt.savefig("tui_example_12.png")
