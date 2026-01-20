..
   Copyright (C) 2008-2026 EDF R&D

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

.. index:: single: SimulatedAnnealing
.. _section_ref_algorithm_SimulatedAnnealing:

Calculation algorithm "*SimulatedAnnealing*"
--------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm estimates the state of a system by gradient-free minimization of
a cost function :math:`J`, using the simulated annealing search meta-heuristic.
It is based on reducing the :math:`J` error as far as possible, while allowing
a temporary rise in this error to avoid getting stuck in a local minimum. The
rise in error is driven by a statistical law of temperature, hence the analogy
with metal annealing, which gives the method its name. The method does not
require any particular information on the functional, nor does it need
derivatives (except in its hybrid "DualAnnealing" version).

It falls in the same category than the
:ref:`section_ref_algorithm_DerivativeFreeOptimization`,
:ref:`section_ref_algorithm_DifferentialEvolution`,
:ref:`section_ref_algorithm_ParticleSwarmOptimization`,
:ref:`section_ref_algorithm_TabuSearch`.

It is a single-objective optimization method, allowing the search for the
global minimum of any cost function :math:`J` of type :math:`L^1`, :math:`L^2`
or :math:`L^{\infty}`, with or without weights, as described in the section for
:ref:`section_theory_optimization`. As it is a meta-heuristic, except in
special cases, reaching a global or local optimal result is not guaranteed
(except in its hybrid "DualAnnealing" version). The default error functional is
that of weighted augmented least squares, classically used in data
assimilation.

There exists various variants of this algorithm. The following stable and
robust formulations are proposed here:

.. index::
    pair: Variant ; GeneralizedSimulatedAnnealing
    pair: Variant ; DualAnnealing

- "GeneralizedSimulatedAnnealing" (Generalized Simulated Annealing or GSA, see
  [Tsallis96]_), a classical algorithm combining classical and fast simulated
  annealing approaches. It is powerful, robust and represents a reference for
  simulated annealing methods.
- "DualAnnealing" (see [Xiang97]_), an algorithm combining the previous GSA
  with a local search strategy, applied to states acceptable from the point of
  view of simulated annealing, which improves the speed and accuracy of the
  GSA. This improvement requires the tangent and adjoint operators.

The following are a few practical suggestions for the effective use of these
algorithms:

- The recommended variant of this algorithm is "DualAnnealing", as it is both
  robust and converges very well, especially in high dimensions for such an
  algorithm. However, as it requires the tangent and adjoint operators, it is
  not always wise to use this acceleration feature.
- In cases where the error function or the observation operator are not
  derivable, the "GeneralizedSimulatedAnnealing" algorithm is suitable and
  achieves the same simulated annealing optimization as the accelerated
  variant.
- The easiest way to check convergence is to leave the parameters at their
  default values and let the simulated annealing stabilize. However, since
  stochastic convergence can take a long time, it is also possible to restrict
  calculations by limiting the number of simulation function evaluations. This
  does not limit theoretical convergence, but it does significantly reduce the
  number of calculations.

These suggestions are to be used as experimental indications, not as
requirements, because they are to be appreciated or adapted according to the
physics of each problem that is treated.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropGlobalOptimization.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. include:: snippets/FeaturePropParallelFree.rst

.. include:: snippets/FeaturePropConvergenceOnBoth.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/EvolutionError.rst

.. include:: snippets/EvolutionModel.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. include:: snippets/BoundsWithNone.rst

.. include:: snippets/EstimationOf_Parameters.rst

.. include:: snippets/MaximumNumberOfIterations.rst

.. include:: snippets/MaximumNumberOfFunctionEvaluations.rst

.. include:: snippets/Minimizer_xDVAR.rst

.. include:: snippets/QualityCriterion.rst

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
  "EnsembleOfSimulations",
  "EnsembleOfStates",
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

.. include:: snippets/Variant_SA.rst

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

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CostFunctionJAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

.. include:: snippets/CurrentIterationNumber.rst

.. include:: snippets/CurrentOptimum.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

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
.. _section_ref_algorithm_SimulatedAnnealing_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_DerivativeFreeOptimization`
- :ref:`section_ref_algorithm_DifferentialEvolution`
- :ref:`section_ref_algorithm_ParticleSwarmOptimization`
- :ref:`section_ref_algorithm_TabuSearch`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Kirkpatrick83]_
- [Tsallis96]_
- [WikipediaSA]_
- [Xiang97]_
