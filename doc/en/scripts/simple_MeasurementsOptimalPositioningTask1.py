# -*- coding: utf-8 -*-
#
from numpy import array, arange
#
dimension = 7
#
print("Defining a set of artificial physical fields")
print("--------------------------------------------")
Ensemble = array( [i+arange(dimension) for i in range(7)] ).T
print("- Dimension of physical field space....................: %i"%dimension)
print("- Number of physical field vectors.....................: %i"%Ensemble.shape[1])
print("- Collection of physical fields (one per column)")
print(Ensemble)
print()
#
print("Search for optimal measurement positions")
print("-------------------------------------------")
from adao import adaoBuilder
case = adaoBuilder.New()
case.setAlgorithmParameters(
    Algorithm = 'MeasurementsOptimalPositioningTask',
    Parameters = {
        "EnsembleOfSnapshots":Ensemble,
        "MaximumNumberOfLocations":3,
        "ErrorNorm":"L2",
    }
)
case.execute()
print("- ADAO calculation performed")
print()
#
print("Display the optimal positioning of measures")
print("-------------------------------------------")
op = case.get("OptimalPoints")[-1]
print("- Number of optimal measurement positions..............: %i"%op.size)
print("- Optimal measurement positions, numbered by default...: %s"%op)
print()
