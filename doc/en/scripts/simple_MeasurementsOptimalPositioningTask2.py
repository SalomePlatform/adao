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
        "StoreSupplementaryCalculations":[
            "ReducedBasis",
            "Residus",
        ],
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
#
print("Reduced representation and error information")
print("--------------------------------------------")
rb = case.get("ReducedBasis")[-1]
print("- Number of vectors of the reduced basis...............: %i"%rb.shape[1])
print("- Reduced basis vectors (one per column)\n")
print(rb)
rs = case.get("Residus")[-1]
print("- Ordered residuals of reconstruction error\n ",rs)
print()
a0, a1 = 7, -2.5
print("- Elementary example of second field reconstruction as a linear")
print("  combination of the two base vectors, that can be guessed to be")
print("  multiplied with the respective coefficients %.1f and %.1f:"%(a0,a1))
print( a0*rb[:,0] + a1*rb[:,1])
print()
