..
   Copyright (C) 2008-2020 EDF R&D

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

.. index:: single: ParticleSwarmOptimization
.. _section_ref_algorithm_ParticleSwarmOptimization:

Calculation algorithm "*ParticleSwarmOptimization*"
---------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm realizes an estimation of the state of a system by minimization
of a cost function :math:`J` by using an evolutionary strategy of particle
swarm. It is a method that does not use the derivatives of the cost function.
It falls in the same category than the
:ref:`section_ref_algorithm_DerivativeFreeOptimization`, the
:ref:`section_ref_algorithm_DifferentialEvolution` or the
:ref:`section_ref_algorithm_TabuSearch`.

This is an optimization method allowing for global minimum search of a general
error function :math:`J` of type :math:`L^1`, :math:`L^2` or :math:`L^{\infty}`,
with or without weights. The default error function is the augmented weighted
least squares function, classically used in data assimilation.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. index:: single: NumberOfInsects
.. index:: single: SwarmVelocity
.. index:: single: GroupRecallRate
.. index:: single: QualityCriterion
.. index:: single: BoxBounds

.. include:: snippets/MaximumNumberOfSteps_50.rst

.. include:: snippets/MaximumNumberOfFunctionEvaluations.rst

.. include:: snippets/QualityCriterion.rst

NumberOfInsects
  This key indicates the number of insects or particles in the swarm. The
  default is 100, which is a usual default for this algorithm.

  Example :
  ``{"NumberOfInsects":100}``

SwarmVelocity
  This key indicates the part of the insect velocity which is imposed by the
  swarm. It is a positive floating point value. The default value is 1.

  Example :
  ``{"SwarmVelocity":1.}``

GroupRecallRate
  This key indicates the recall rate at the best swarm insect. It is a
  floating point value between 0 and 1. The default value is 0.5.

  Example :
  ``{"GroupRecallRate":0.5}``

BoxBounds
  This key allows to define upper and lower bounds for *increments* on every
  state variable being optimized (and not on state variables themselves).
  Bounds have to be given by a list of list of pairs of lower/upper bounds for
  each increment on variable, with extreme values every time there is no bound
  (``None`` is not allowed when there is no bound). This key is required and
  there is no default values.

  Example :
  ``{"BoxBounds":[[-0.5,0.5], [0.01,2.], [0.,1.e99], [-1.e99,1.e99]]}``

.. include:: snippets/SetSeed.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  This list indicates the names of the supplementary variables that can be
  available at the end of the algorithm, if they are initially required by the
  user. It involves potentially costly calculations or memory consumptions. The
  default is a void list, none of these variables being calculated and stored
  by default excepted the unconditionnal variables. The possible names are in
  the following list: [
  "Analysis",
  "BMA",
  "CurrentState",
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "Innovation",
  "OMA",
  "OMB",
  "SimulatedObservationAtBackground",
  "SimulatedObservationAtCurrentState",
  "SimulatedObservationAtOptimum",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/BMA.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/OMA.rst

.. include:: snippets/OMB.rst

.. include:: snippets/SimulatedObservationAtBackground.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtOptimum.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_DerivativeFreeOptimization`
- :ref:`section_ref_algorithm_DifferentialEvolution`
- :ref:`section_ref_algorithm_TabuSearch`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [WikipediaPSO]_
