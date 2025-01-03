# -*- coding: utf-8 -*-
#
from matplotlib import pyplot as plt
from numpy import array, set_printoptions
from adao import adaoBuilder
set_printoptions(precision=4, floatmode='fixed')
#
#-------------------------------------------------------------------------------
#
case = adaoBuilder.New()
case.set( 'AlgorithmParameters',
    Algorithm='3DVAR',
    Parameters = {
        "StoreSupplementaryCalculations":[
            "CostFunctionJ",
            "CurrentState",
            "InnovationAtCurrentState",
        ],
    }
)
case.set( 'Background',          Vector=[0, 1, 2] )
case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
case.set( 'Observer',
    Variable="CurrentState",
    Template="ValuePrinter",
    Info="  Current state:",
)
#
print("Displays current state values, at each step:")
case.execute()
print("")
#
#-------------------------------------------------------------------------------
#
print("Calculation-measurement deviation (or error) indicators")
print("     (only the first 3 steps are displayed here)")
print("")
CalculMeasureErrors = case.get("InnovationAtCurrentState")
#
print("===> Maximum error between calculations and measurements, at each step:")
print("    ",array(
    CalculMeasureErrors.maxs()
    [0:3] ))
print("===> Minimum error between calculations and measurements, at each step:")
print("    ",array(
    CalculMeasureErrors.mins()
    [0:3] ))
print("===> Norm of the error between calculation and measurement, at each step:")
print("    ",array(
    CalculMeasureErrors.norms()
    [0:3] ))
print("===> Mean absolute error (MAE) between calculations and measurements, at each step:")
print("    ",array(
    CalculMeasureErrors.maes()
    [0:3] ))
print("===> Mean square error (MSE) between calculations and measurements, at each step:")
print("    ",array(
    CalculMeasureErrors.mses()
    [0:3] ))
print("===> Root mean square error (RMSE) between calculations and measurements, at each step:")
print("    ",array(
    CalculMeasureErrors.rmses()
    [0:3] ))
#
#-------------------------------------------------------------------------------
#
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (8, 12)
#
plt.figure()
plt.suptitle('Indicators built on current calculation-measurement deviation (or error)\n', fontweight='bold')
plt.subplot(611)
plt.plot(CalculMeasureErrors.maxs(), 'bx--', label='Indicator at current step')
plt.ylabel('Maximum (a.u.)')
plt.legend()
plt.subplot(612)
plt.plot(CalculMeasureErrors.mins(), 'bx--', label='Indicator at current step')
plt.ylabel('Minimum (a.u.)')
plt.legend()
plt.subplot(613)
plt.plot(CalculMeasureErrors.norms(), 'bx-', label='Indicator at current step')
plt.ylabel('Norm (a.u.)')
plt.legend()
plt.subplot(614)
plt.plot(CalculMeasureErrors.maes(), 'kx-', label='Indicator at current step')
plt.ylabel('MAE (a.u.)')
plt.legend()
plt.subplot(615)
plt.plot(CalculMeasureErrors.mses(), 'gx-', label='Indicator at current step')
plt.ylabel('MSE (a.u.)')
plt.legend()
plt.subplot(616)
plt.plot(CalculMeasureErrors.rmses(), 'rx-', label='Indicator at current step')
plt.ylabel('RMSE (a.u.)')
plt.legend()
plt.xlabel('Step size calculation (step number or rank)')
plt.tight_layout()
plt.savefig("tui_example_12.png")
