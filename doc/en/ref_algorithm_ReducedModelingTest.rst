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

.. index:: single: ReducedModelingTest
.. _section_ref_algorithm_ReducedModelingTest:

Checking algorithm "*ReducedModelingTest*"
------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm provides a simple analysis of the characteristics of the state
collection from the point of view of reduction. It aims to diagnose the
complexity of the information present in the available state collection, and
the possibility to represent this state information in a space smaller than the
entire state collection. Technically, based on a classical SVD (Singular Value
Decomposition) and in the same way as a PCA (Principal Component Analysis), it
evaluates how information decreases with the number of singular values, either
as values or, from a statistical point of view, as remaining variance.

Once the analysis is complete, a summary is displayed and, on request, a
graphical representation of the same information is produced.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/EnsembleOfSnapshots.rst

.. include:: snippets/ExcludeLocations.rst

.. include:: snippets/MaximumNumberOfLocations.rst

.. include:: snippets/MaximumNumberOfModes.rst

.. include:: snippets/NameOfLocations.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/PlotAndSave.rst

.. include:: snippets/SampleAsExplicitHyperCube.rst

.. include:: snippets/SampleAsIndependantRandomVariables.rst

.. include:: snippets/SampleAsMinMaxLatinHyperCube.rst

.. include:: snippets/SampleAsMinMaxSobolSequence.rst

.. include:: snippets/SampleAsMinMaxStepHyperCube.rst

.. include:: snippets/SampleAsnUplet.rst

.. include:: snippets/SetDebug.rst

.. include:: snippets/SetSeed.rst

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
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  "Residus",
  "SingularValues",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/NoUnconditionalOutput.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. include:: snippets/Residus.rst

.. include:: snippets/SingularValues.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_ReducedModelingTest_examples:

.. include:: snippets/Header2Algo09.rst

.. --------- ..
.. include:: scripts/simple_ReducedModelingTest1.rst

.. literalinclude:: scripts/simple_ReducedModelingTest1.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_ReducedModelingTest1.res
    :language: none

.. include:: snippets/Header2Algo11.rst

.. _simple_ReducedModelingTest1:
.. image:: scripts/simple_ReducedModelingTest1.png
  :align: center
  :width: 90%

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_ParallelFunctionTest`
- :ref:`section_ref_algorithm_EnsembleOfSimulationGenerationTask`
- :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`

