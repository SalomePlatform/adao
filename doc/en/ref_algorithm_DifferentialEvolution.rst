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

.. index:: single: DifferentialEvolution
.. _section_ref_algorithm_DifferentialEvolution:

Calculation algorithm "*DifferentialEvolution*"
----------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm realizes an estimation of the state of a system by minimization
of a cost function :math:`J` by using an evolutionary strategy of differential
evolution. It is a method that does not use the derivatives of the cost
function. It falls in the same category than the
:ref:`section_ref_algorithm_DerivativeFreeOptimization`, the
:ref:`section_ref_algorithm_ParticleSwarmOptimization` or the
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

.. include:: snippets/Minimizer_DE.rst

.. include:: snippets/BoundsWithExtremes.rst

.. include:: snippets/CrossOverProbability_CR.rst

.. include:: snippets/MaximumNumberOfIterations.rst

.. include:: snippets/MaximumNumberOfFunctionEvaluations.rst

.. include:: snippets/MutationDifferentialWeight_F.rst

.. include:: snippets/PopulationSize.rst

.. include:: snippets/QualityCriterion.rst

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
  "Analysis",
  "BMA",
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CostFunctionJAtCurrentOptimum",
  "CostFunctionJbAtCurrentOptimum",
  "CostFunctionJoAtCurrentOptimum",
  "CurrentIterationNumber",
  "CurrentOptimum",
  "CurrentState",
  "IndexOfOptimum",
  "Innovation",
  "InnovationAtCurrentState",
  "OMA",
  "OMB",
  "SimulatedObservationAtBackground",
  "SimulatedObservationAtCurrentOptimum",
  "SimulatedObservationAtCurrentState",
  "SimulatedObservationAtOptimum",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/BMA.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CostFunctionJAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

.. include:: snippets/CurrentIterationNumber.rst

.. include:: snippets/CurrentOptimum.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/IndexOfOptimum.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/OMA.rst

.. include:: snippets/OMB.rst

.. include:: snippets/SimulatedObservationAtBackground.rst

.. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtOptimum.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_DifferentialEvolution_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_DerivativeFreeOptimization`
- :ref:`section_ref_algorithm_ParticleSwarmOptimization`
- :ref:`section_ref_algorithm_TabuSearch`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Chakraborty08]_
- [Das11]_
- [Das16]_
- [Price05]_
- [Storn97]_
