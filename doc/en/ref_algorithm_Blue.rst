..
   Copyright (C) 2008-2025 EDF R&D

   This file is part of SALOME ADAO module.

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with this library; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

   See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com

   Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

.. index:: single: Blue
.. _section_ref_algorithm_Blue:

Calculation algorithm "*Blue*"
------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm realizes a BLUE (Best Linear Unbiased Estimator) type estimation
of the state of a system. It is a linear, unbiased and optimal estimation.
Technically, it is here an Aitken estimator. It performs the best linear
estimate of the state using the initial background state and the observations.
It is theoretically reserved for observation operator cases which are linear,
even if it sometimes works in "slightly" non-linear cases. One can verify the
linearity of the observation operator with the help of the
:ref:`section_ref_algorithm_LinearityTest`. This algorithm is always the
fastest of all the assimilation algorithms of ADAO.

This mono-objective optimization algorithm is naturally written for a single
estimate, without any dynamic or iterative notion (there is no need in this
case for an incremental evolution operator, nor for an evolution error
covariance). In ADAO, it can also be used on a succession of observations,
placing the estimate in a recursive framework partly similar to a
:ref:`section_ref_algorithm_KalmanFilter`. A standard estimate is made at each
observation step on the state predicted by the incremental evolution model,
knowing that the state error covariance remains the background covariance
initially provided by the user. To be explicit, unlike Kalman-type filters, the
state error covariance is not updated.

In case of non-linearity, even slightly marked, it will be easily preferred a
:ref:`section_ref_algorithm_ExtendedBlue` or a
:ref:`section_ref_algorithm_3DVAR`.

.. index:: single: Optimal Interpolation
.. index:: single: OI

Additional remark: an algebraic simplification of the BLUE leads to the
so-called optimal interpolation method, named "*Optimal Interpolation*" or
"*OI*". It is a very simple and inexpensive method, especially adapted to very
(very) large problems, but whose disadvantage is to provide a globally
sub-optimal and noisy analysis result, even inconsistent. The way to avoid
these disadvantages is to adapt very precisely the elements of the method to
each physical model, making the method not robust. For these reasons, this
method is not proposed nor recommended.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropLocalOptimization.rst

.. include:: snippets/FeaturePropDerivativeNeeded.rst

.. include:: snippets/FeaturePropParallelDerivativesOnly.rst

.. include:: snippets/FeaturePropConvergenceOnStatic.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. include:: snippets/EstimationOf_Parameters.rst

.. include:: snippets/NumberOfSamplesForQuantiles.rst

.. include:: snippets/Quantiles.rst

.. include:: snippets/SetSeed.rst

.. include:: snippets/SimulationForQuantiles.rst

.. include:: snippets/StateBoundsForQuantilesWithNone.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *List of names*. This list indicates the names of the supplementary
  variables, that can be available during or at the end of the algorithm, if
  they are initially required by the user. Their availability involves,
  potentially, costly calculations or memory consumptions. The default is then
  a void list, none of these variables being calculated and stored by default
  (excepted the unconditional variables). The possible names are in the
  following list (the detailed description of each named variable is given in
  the following part of this specific algorithmic documentation, in the
  sub-section "*Information and variables available at the end of the
  algorithm*"): [
  "Analysis",
  "APosterioriCorrelations",
  "APosterioriCovariance",
  "APosterioriStandardDeviations",
  "APosterioriVariances",
  "BMA",
  "CostFunctionJ",
  "CostFunctionJAtCurrentOptimum",
  "CostFunctionJb",
  "CostFunctionJbAtCurrentOptimum",
  "CostFunctionJo",
  "CostFunctionJoAtCurrentOptimum",
  "CurrentOptimum",
  "CurrentState",
  "CurrentStepNumber",
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  "ForecastState",
  "Innovation",
  "InnovationAtCurrentAnalysis",
  "MahalanobisConsistency",
  "OMA",
  "OMB",
  "SampledStateForQuantiles",
  "SigmaBck2",
  "SigmaObs2",
  "SimulatedObservationAtBackground",
  "SimulatedObservationAtCurrentOptimum",
  "SimulatedObservationAtCurrentState",
  "SimulatedObservationAtOptimum",
  "SimulationQuantiles",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/APosterioriCorrelations.rst

.. include:: snippets/APosterioriCovariance.rst

.. include:: snippets/APosterioriStandardDeviations.rst

.. include:: snippets/APosterioriVariances.rst

.. include:: snippets/BMA.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

.. include:: snippets/CurrentOptimum.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/CurrentStepNumber.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. include:: snippets/ForecastState.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/InnovationAtCurrentAnalysis.rst

.. include:: snippets/MahalanobisConsistency.rst

.. include:: snippets/OMA.rst

.. include:: snippets/OMB.rst

.. include:: snippets/SampledStateForQuantiles.rst

.. include:: snippets/SigmaBck2.rst

.. include:: snippets/SigmaObs2.rst

.. include:: snippets/SimulatedObservationAtBackground.rst

.. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtOptimum.rst

.. include:: snippets/SimulationQuantiles.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_Blue_examples:

.. include:: snippets/Header2Algo09.rst

.. include:: scripts/simple_Blue.rst

.. literalinclude:: scripts/simple_Blue.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_Blue.res

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_ExtendedBlue`
- :ref:`section_ref_algorithm_3DVAR`
- :ref:`section_ref_algorithm_LinearityTest`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Bouttier99]_
