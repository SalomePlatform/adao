..
   Copyright (C) 2008-2023 EDF R&D

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

.. index:: single: LinearLeastSquares
.. _section_ref_algorithm_LinearLeastSquares:

Calculation algorithm "*LinearLeastSquares*"
--------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm realizes a "Least Squares" linear type estimation of the state of
a system. It is similar to a :ref:`section_ref_algorithm_Blue`, without its
background part.

This algorithm is always the fastest of all the optimization algorithms of
ADAO. It is theoretically reserved for observation operator cases which are
explicitly linear, even if it sometimes works in "slightly" non-linear cases.
One can verify the linearity of the observation operator with the help of a
:ref:`section_ref_algorithm_LinearityTest`.

This algorithm is naturally written for a single estimate, without any dynamic
or iterative notion (there is no need in this case for an incremental evolution
operator, nor for an evolution error covariance). In ADAO, it can also be used
on a succession of observations, placing the estimate in a recursive framework
partly similar to a Kalman Filter. A standard estimate is made at each
observation step on the state predicted by the incremental evolution model.

In all cases, it is recommanded to prefer at least a
:ref:`section_ref_algorithm_Blue`, or a
:ref:`section_ref_algorithm_ExtendedBlue` or a
:ref:`section_ref_algorithm_3DVAR`.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. include:: snippets/EstimationOf_Parameters.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *List of names*. This list indicates the names of the supplementary
  variables, that can be available during or at the end of the algorithm, if
  they are initially required by the user. Their avalability involves,
  potentially, costly calculations or memory consumptions. The default is then
  a void list, none of these variables being calculated and stored by default
  (excepted the unconditionnal variables). The possible names are in the
  following list (the detailed description of each named variable is given in
  the following part of this specific algorithmic documentation, in the
  sub-section "*Information and variables available at the end of the
  algorithm*"): [
  "Analysis",
  "CostFunctionJ",
  "CostFunctionJAtCurrentOptimum",
  "CostFunctionJb",
  "CostFunctionJbAtCurrentOptimum",
  "CostFunctionJo",
  "CostFunctionJoAtCurrentOptimum",
  "CurrentOptimum",
  "CurrentState",
  "CurrentStepNumber",
  "ForecastState",
  "InnovationAtCurrentAnalysis",
  "OMA",
  "SimulatedObservationAtCurrentOptimum",
  "SimulatedObservationAtCurrentState",
  "SimulatedObservationAtOptimum",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

*Tips for this algorithm:*

    As the *"Background"* and *"BackgroundError"* commands are required for ALL
    the calculation algorithms in the interface, you have to provide a value,
    even if these commands are not required for this algorithm, and will not be
    used. The simplest way is to give "1" as a STRING for both.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

.. include:: snippets/CurrentOptimum.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/CurrentStepNumber.rst

.. include:: snippets/ForecastState.rst

.. include:: snippets/InnovationAtCurrentAnalysis.rst

.. include:: snippets/OMA.rst

.. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtOptimum.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_LinearLeastSquares_examples:
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_Blue`
- :ref:`section_ref_algorithm_ExtendedBlue`
- :ref:`section_ref_algorithm_3DVAR`
- :ref:`section_ref_algorithm_LinearityTest`
