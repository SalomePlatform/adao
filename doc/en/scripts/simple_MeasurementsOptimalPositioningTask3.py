# -*- coding: utf-8 -*-
#
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(123456789)
#
dimension = 20
#
print("Defining a set of artificial physical fields")
from Models.TwoDimensionalInverseDistanceCS2010 \
     import TwoDimensionalInverseDistanceCS2010 as Equation
Eq = Equation(dimension, dimension)
print()
#
print("Search for optimal measurement positions")
from adao import adaoBuilder
case = adaoBuilder.New()
case.setAlgorithmParameters(
    Algorithm = 'MeasurementsOptimalPositioningTask',
    Parameters = {
        "Variant":"DEIM",
        "SampleAsnUplet":Eq.get_sample_of_mu(15, 15),
        "MaximumNumberOfLocations":50,
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
print()
print("Graphical display of the results")
#
sp = case.get("EnsembleOfSimulations")[-1]
x1, x2 = Eq.get_x()
x1, x2 = np.meshgrid(x1, x2)
name = "Representation of a few snapshots of G out of a total of %i"%sp.shape[1]
print("  -", name)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(6, 6))
fig.suptitle(name)
ax.set_xlabel("Position x1", fontweight='bold', color='red')
ax.set_ylabel("Position x2", fontweight='bold', color='red')
ax.set_zlabel("Magnitude of G", fontweight='bold', color='red')
for i in range(sp.shape[1]):
    if i % 44 != 0: continue
    ax.plot_surface(x1, x2, sp[:,i].reshape((dimension, dimension)), cmap='coolwarm')
fig.savefig("simple_MeasurementsOptimalPositioningTask31.png")
plt.close()
#
sv = case.get("SingularValues")[-1]
name = "Singular values of the set of G simulations"
print("  -", name)
fig, ax = plt.subplots(figsize=(6, 6))
fig.suptitle(name)
ax.set_xlabel("Index of singular values, numbered from 1")
ax.set_ylabel("Magnitude of singular values")
ax.set_xlim(1, len(sv))
ax.set_yscale("log")
ax.grid(True)
ax.plot(range(1, 1 + len(sv)), sv)
fig.savefig("simple_MeasurementsOptimalPositioningTask32.png")
plt.tight_layout()
plt.close()
#
nbmax = 15
op = case.get("OptimalPoints")[-1]
posx1 = [x1.reshape((-1,))[ip] for ip in op[:nbmax]]
posx2 = [x2.reshape((-1,))[ip] for ip in op[:nbmax]]
name = "Set of %i first optimal points of measurement"%nbmax
Omega = Eq.get_bounds_on_space()
print("  -", name)
fig, ax = plt.subplots(figsize=(6, 6))
fig.suptitle(name)
ax.set_xlabel("Position x1", fontweight='bold', color='red')
ax.set_ylabel("Position x2", fontweight='bold', color='red')
ax.set_xlim(Omega[0][0] - 0.05, Omega[0][1] + 0.05)
ax.set_ylim(Omega[1][0] - 0.05, Omega[1][1] + 0.05)
ax.grid(True, which='both', linestyle=(0, (1, 5)), linewidth=0.5)
ax.plot(posx1, posx2, markersize=6, marker="o", linestyle='')
for i in range(len(posx1)):
    ax.text(posx1[i] + 0.005, posx2[i] + 0.01, str(i + 1), fontweight='bold')
fig.savefig("simple_MeasurementsOptimalPositioningTask33.png")
plt.tight_layout()
plt.close()
