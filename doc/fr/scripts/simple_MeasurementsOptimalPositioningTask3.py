# -*- coding: utf-8 -*-
#
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(123456789)
#
dimension = 20
nbmeasures = 15
#
print("Définition d'un ensemble artificiel de champs physiques")
from Models.TwoDimensionalInverseDistanceCS2010 \
     import TwoDimensionalInverseDistanceCS2010 as Equation
Eq = Equation(dimension, dimension)
print()
#
print("Recherche des positions optimales de mesure")
from adao import adaoBuilder
case = adaoBuilder.New()
case.setAlgorithmParameters(
    Algorithm = "MeasurementsOptimalPositioningTask",
    Parameters = {
        "Variant":"DEIM",
        "SampleAsnUplet":Eq.get_sample_of_mu(15, 15),
        "MaximumNumberOfLocations":nbmeasures,
        "ErrorNorm":"Linf",
        "ErrorNormTolerance":0.,
        "StoreSupplementaryCalculations":[
            "SingularValues",
            "OptimalPoints",
            "EnsembleOfSimulations",
            ],
        }
    )
case.setBackground(Vector = [1,1] )
case.setObservationOperator(OneFunction = Eq.OneRealisation)
case.execute()
#
#-------------------------------------------------------------------------------
print()
print("Affichage graphique des résultats")
#
sp = case.get("EnsembleOfSimulations")[-1]
sv = case.get("SingularValues")[-1]
op = case.get("OptimalPoints")[-1]
#
x1, x2 = Eq.get_x()
x1, x2 = np.meshgrid(x1, x2)
posx1 = [x1.reshape((-1,))[ip] for ip in op]
posx2 = [x2.reshape((-1,))[ip] for ip in op]
Omega = Eq.get_bounds_on_space()
#
fig = plt.figure(figsize=(18, 6))
name = "Recherche de points optimaux de mesure par "
name += '"ADAO/MeasurementsOptimalPositioningTask/DEIM"'
fig.suptitle(name, fontsize=20, fontstyle="italic")
#
ax = fig.add_subplot(1, 3, 1)
name = "Valeurs singulières de l'ensemble des %i simulations de G"%sp.shape[1]
print("  -", name)
ax.set_title(name, fontstyle="italic", color="red")
ax.set_xlabel("Index des valeurs singulières, numérotées à partir de 1")
ax.set_ylabel("Amplitude des valeurs singulières")
ax.set_xlim(1, len(sv))
ax.set_yscale("log")
ax.grid(True)
ax.plot(range(1, 1 + len(sv)), sv)
#
ax = fig.add_subplot(1, 3, 2, projection = "3d")
name = "Quelques simulations de G sur un total de %i"%sp.shape[1]
print("  -", name)
ax.set_title(name, fontstyle="italic", color="red")
ax.set_xlabel("Position x1")
ax.set_ylabel("Position x2")
ax.set_zlabel("Amplitude de G")
for i in range(sp.shape[1]):
    if i % 44 != 0: continue
    Gfield = sp[:,i].reshape((dimension, dimension))
    ax.plot_surface(x1, x2, Gfield, cmap="coolwarm")
#
ax = fig.add_subplot(1, 3, 3)
name = "Ensemble des %i premiers points optimaux de mesure"%nbmeasures
print("  -", name)
ax.set_title(name, fontstyle="italic", color="red")
ax.set_xlabel("Position x1")
ax.set_ylabel("Position x2")
ax.set_xlim(Omega[0][0] - 0.05, Omega[0][1] + 0.05)
ax.set_ylim(Omega[1][0] - 0.05, Omega[1][1] + 0.05)
ax.grid(True, which="both", linestyle=(0, (1, 5)), linewidth=0.5)
ax.plot(posx1, posx2, markersize=6, marker="o", linestyle="")
for i in range(len(posx1)):
    ax.text(posx1[i] + 0.005, posx2[i] + 0.01, str(i + 1), fontweight="bold")
#
plt.tight_layout()
fig.savefig("simple_MeasurementsOptimalPositioningTask3.png")
plt.close()
