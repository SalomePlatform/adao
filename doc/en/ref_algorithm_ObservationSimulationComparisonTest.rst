..
   Copyright (C) 2008-2024 EDF R&D

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

.. index:: single: ObservationSimulationComparisonTest
.. _section_ref_algorithm_ObservationSimulationComparisonTest:

Checking algorithm "*ObservationSimulationComparisonTest*"
----------------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This verification algorithm allows to analyze in a simple way the stability of
the difference between measures and an operator :math:`F` during its execution.
The operator is any operator, so it can be the observation operator
:math:`\mathcal{H}` as well as the evolution operator :math:`\mathcal{D}`, as
long as it is provided in each case according to the
:ref:`section_ref_operator_requirements`. The operator :math:`F` is considered
as depending on a vector variable :math:`\mathbf{x}` and returning another
vector variable :math:`\mathbf{y}`.

The algorithm verifies that the difference is stable, that the operator is
working correctly and that its call is compatible with its usage in ADAO
algorithms. In practice, it allows to call one or several times the operator,
activating or not the "debug" mode during execution. It is very similar in its
current behavior to a :ref:`section_ref_algorithm_FunctionTest` but it tests
the stability of the measurement-calculation difference.

Statistics on :math:`\mathbf{x}` input and :math:`\mathbf{y}` output vectors,
and potentially on the classical data assimilation error function :math:`J`,
are given for each execution of operator, and an another global statistic is
given at the end. The precision of printed outputs can be controlled to
facilitate automatic tests of operator. It may also be useful to check the
entries themselves beforehand with the intended test
:ref:`section_ref_algorithm_InputValuesTest`.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/NumberOfRepetition.rst

.. include:: snippets/SetDebug.rst

.. include:: snippets/ShowElementarySummary.rst

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
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CurrentState",
  "Innovation",
  "InnovationAtCurrentState",
  "OMB",
  "SimulatedObservationAtCurrentState",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/NoUnconditionalOutput.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/OMB.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_ObservationSimulationComparisonTest_examples:

.. include:: snippets/Header2Algo09.rst

.. --------- ..
.. include:: scripts/simple_ObservationSimulationComparisonTest1.rst

.. literalinclude:: scripts/simple_ObservationSimulationComparisonTest1.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_ObservationSimulationComparisonTest1.res
    :language: none

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
