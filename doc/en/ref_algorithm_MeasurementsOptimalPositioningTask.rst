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

.. index:: single: MeasurementsOptimalPositioningTask
.. index:: single: Optimal positioning of measurements
.. index:: single: Measurement locations
.. index:: single: Measurements (Optimal positioning)
.. index:: single: Ensemble of simulations
.. index:: single: Ensemble of snapshots
.. index:: single: Simulations (Ensemble)
.. index:: single: Snapshots (Ensemble)
.. _section_ref_algorithm_MeasurementsOptimalPositioningTask:

Task algorithm "*MeasurementsOptimalPositioningTask*"
-----------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. warning::

  This algorithm is only available in textual user interface (TUI) and not in
  graphical user interface (GUI).

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm provides optimal positioning of measurement points by an EIM
(Empirical Interpolation Method) analysis. These positions are determined in a
iterative greedy way, from a pre-existing set of state vectors (usually called
"snapshots" in reduced basis methodology) or obtained by a direct simulation
during the algorithm. Each of these state vectors are usually (but not
necessarily) the result :math:`\mathbf{y}` of a simulation or an observation
using the operator :math:`H` for a given set of parameters :math:`\mathbf{x}`.

There are two ways to use this algorithm:

#. In its simplest use, if the set of state vectors is pre-existing, it is only
   necessary to provide it by the algorithm option "*EnsembleOfSnapshots*". It
   is for example the case when set of states has been generated by an
   :ref:`section_ref_algorithm_EnsembleOfSimulationGenerationTask`.
#. If the set of state vectors is to be obtained by simulations during the
   course of the algorithm, then one must provide the :math:`H` simulation or
   observation operator and the parametric :math:`\mathbf{x}` state space
   design of experiments.

The sampling of the states :math:`\mathbf{x}` can be given explicitly or under
form of hyper-cubes, explicit or sampled according to classic distributions.
Beware of the size of the hyper-cube (and then to the number of computations)
that can be reached, it can grow quickly to be quite large.

It is possible to exclude a priori potential positions for optimal measurement
points, using the analysis variant "*lcEIM*" for a constrained positioning
search.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

*None*

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Task.rst

.. include:: snippets/EnsembleOfSnapshots.rst

.. include:: snippets/ExcludeLocations.rst

.. include:: snippets/ErrorNorm.rst

.. include:: snippets/ErrorNormTolerance.rst

.. include:: snippets/MaximumNumberOfLocations.rst

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
  they are initially required by the user. Their avalability involves,
  potentially, costly calculations or memory consumptions. The default is then
  a void list, none of these variables being calculated and stored by default
  (excepted the unconditionnal variables). The possible names are in the
  following list (the detailed description of each named variable is given in
  the following part of this specific algorithmic documentation, in the
  sub-section "*Information and variables available at the end of the
  algorithm*"): [
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  "OptimalPoints",
  "ReducedBasis",
  "Residus",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. include:: snippets/Variant_MOP.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/OptimalPoints.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. include:: snippets/OptimalPoints.rst

.. include:: snippets/ReducedBasis.rst

.. include:: snippets/Residus.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_MeasurementsOptimalPositioningTask_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_ParallelFunctionTest`
- :ref:`section_ref_algorithm_EnsembleOfSimulationGenerationTask`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Barrault04]_
- [Gong18]_
- [Quarteroni16]_