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

.. index:: single: ControledFunctionTest
.. _section_ref_algorithm_ControledFunctionTest:

Checking algorithm "*ControledFunctionTest*"
--------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This verification algorithm allows to analyze in a simple way the stability of
an operator :math:`F` during its execution. The operator is any operator, so it
can be the observation operator :math:`\mathcal{H}` as well as the evolution
operator :math:`\mathcal{D}`, as long as it is provided in each case according
to the :ref:`section_ref_operator_requirements`. The operator :math:`F` is
considered as depending on a vector variable :math:`\mathbf{x}` and on a
control vector variable :math:`\mathbf{u}`, the two not necessarily being of
the same size, and returning another vector variable :math:`\mathbf{y}`.

The algorithm verifies that the operator is working correctly and that its call
is compatible with its usage in ADAO algorithms. In practice, it allows to call
one or several times the operator, activating or not the "debug" mode during
execution.

Statistics on :math:`\mathbf{x}` input and :math:`\mathbf{y}` output vectors
are given for each execution of operator, and an another global statistic is
given at the end. The precision of printed outputs can be controlled to
facilitate automatic tests of operator. It may also be useful to check the
entries themselves beforehand with the intended test
:ref:`section_ref_algorithm_InputValuesTest`.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/ObservationOperator.rst

.. include:: snippets/ControlInput.rst

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
  "CurrentState",
  "SimulatedObservationAtCurrentState",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/NoUnconditionalOutput.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_ControledFunctionTest_examples:

.. include:: snippets/Header2Algo09.rst

.. --------- ..
.. include:: scripts/simple_ControledFunctionTest1.rst

.. literalinclude:: scripts/simple_ControledFunctionTest1.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_ControledFunctionTest1.res
    :language: none

.. --------- ..
.. include:: scripts/simple_ControledFunctionTest2.rst

.. literalinclude:: scripts/simple_ControledFunctionTest2.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_ControledFunctionTest2.res
    :language: none

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_InputValuesTest`
- :ref:`section_ref_algorithm_LinearityTest`
- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_ParallelFunctionTest`
