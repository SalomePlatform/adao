# -*- coding: utf-8 -*-
#
from numpy import array, arange, ravel, set_printoptions
set_printoptions(precision=3)
#
dimension = 7
#
print("Defining a set of artificial physical fields")
print("--------------------------------------------")
Ensemble = array( [i+arange(dimension) for i in range(7)] ).T
print("- Dimension of physical field space....................: %i"%dimension)
print("- Number of physical field vectors.....................: %i"%Ensemble.shape[1])
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
print("Display of optimal positioning of measures")
print("------------------------------------------")
op = case.get("OptimalPoints")[-1]
print("- Number of optimal measurement positions..............: %i"%op.size)
print("- Optimal measurement positions, numbered by default...: %s"%op)
print()
#
print("Reconstruction by interpolation of known measured states")
print("--------------------------------------------------------")
rb = case.get("ReducedBasis")[-1]
measures_at_op = Ensemble[op,1]
#
interpolation = adaoBuilder.New()
interpolation.setAlgorithmParameters(
    Algorithm = 'InterpolationByReducedModelTask',
    Parameters = {
        "ReducedBasis":rb,
        "OptimalLocations":op,
        }
    )
interpolation.setObservation( Vector = measures_at_op )
interpolation.execute()
field = interpolation.get("Analysis")[-1]
print("- Reference state 1 used for the learning..............:",ravel(Ensemble[:,1]))
print("- Optimal measurement positions, numbered by default...: %s"%op)
print("- Measures extracted from state 1 for reconstruction...:",measures_at_op)
print("- State 1 reconstructed with the precision of 1%.......:",field)

if max(abs(ravel(Ensemble[:,1])-field)) < 1.e-2:
    print("  ===> There is no difference between the two states, as expected")
else:
    raise ValueError("Difference recorded in reference state 1")
print()
#
print("Reconstruction by interpolation of unknown measured states")
print("----------------------------------------------------------")
measures_at_op = array([4, 3])
interpolation.setObservation( Vector = measures_at_op )
interpolation.execute()
field = interpolation.get("Analysis")[-1]
print("  Illustration of an interpolation on unknown real measurements")
print("- Optimal measurement positions, numbered by default...: %s"%op)
print("- Measures not present in the known states.............:",measures_at_op)
print("- State reconstructed with the precision of 1%.........:",field)
print("  ===> At measure positions %s, the reconstructed field is equal to measures"%op)
print()
