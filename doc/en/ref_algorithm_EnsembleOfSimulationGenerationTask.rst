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

.. index:: single: EnsembleOfSimulationGenerationTask
.. index:: single: Génération d'ensemble de simulations
.. index:: single: Ensemble of simulations
.. index:: single: Ensemble of snapshots
.. index:: single: Simulations (Ensemble)
.. index:: single: Snapshots (Ensemble)
.. _section_ref_algorithm_EnsembleOfSimulationGenerationTask:

Task algorithm "*EnsembleOfSimulationGenerationTask*"
-----------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm allows to generate a set of physical results, of simulation or
observation type, using the :math:`H` operator for a design of experiment of
the :math:`\mathbf{x}` parametric state space. The result of this algorithm is
a homogeneous collection of simulated vectors :math:`\mathbf{y}` (available
using the storable variable "*EnsembleOfSimulations*") corresponding directly
to the chosen homogeneous collection of state vectors :math:`\mathbf{x}`
(available using the storable variable "*EnsembleOfStates*").

The sampling of the states :math:`\mathbf{x}` can be given explicitly or under
form of hyper-cubes, explicit or sampled according to classic distributions.
The computations are optimized according to the computer resources available
and the options requested by the user. Beware of the size of the hyper-cube
(and then to the number of computations) that can be reached, it can grow
quickly to be quite large.

To be visible by the user while reducing the risk of storage difficulties, the
results of sampling or simulations has to be **explicitly** asked for using the
required variable.

The results obtained with this algorithm can be used to feed an
:ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`. In a
complementary way, and if the goal is to evaluate the calculation-measurement
error, an :ref:`section_ref_algorithm_SamplingTest` uses the same sampling
commands to establish a set of error functional values :math:`J` from
observations :math:`\mathbf{y}^o`.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Task.rst

.. include:: snippets/SampleAsExplicitHyperCube.rst

.. include:: snippets/SampleAsIndependantRandomVariables.rst

.. include:: snippets/SampleAsMinMaxStepHyperCube.rst

.. include:: snippets/SampleAsnUplet.rst

.. include:: snippets/SetDebug.rst

.. include:: snippets/SetSeed.rst

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
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_EnsembleOfSimulationGenerationTask_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_ParallelFunctionTest`
- :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`

