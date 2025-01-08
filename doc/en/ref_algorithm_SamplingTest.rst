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

.. index:: single: SamplingTest
.. _section_ref_algorithm_SamplingTest:

Checking algorithm "*SamplingTest*"
-----------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm establishes the collection of values for any :math:`J` error
functional of type :math:`L^1`, :math:`L^2` or :math:`L^{\infty}`, with or
without weights, as described in the section for
:ref:`section_theory_optimization`. Each :math:`J` calculation is conducted
using the :math:`\mathcal{H}` observation operator and :math:`\mathbf{y}^o`
observations for a :math:`\mathbf{x}` state. The :math:`\mathbf{x}` states come
from a sample of states defined *a priori*. The default error functional is the
augmented weighted least squares functional, classically used in data
assimilation.

This test is useful for explicitly analyzing the sensitivity of the functional
:math:`J` to variations in the state :math:`\mathbf{x}`.

The sampling of the states :math:`\mathbf{x}` can be given explicitly or under
form of hypercubes, explicit or sampled according to classic distributions, or
using Latin hypercube sampling (LHS) or Sobol sequences. The computations are
optimized according to the computer resources available and the options
requested by the user. You can refer to the
:ref:`section_ref_sampling_requirements` for an illustration of sampling.
Beware of the size of the hypercube (and then to the number of computations)
that can be reached, it can grow quickly to be quite large. When a state is not
observable, a "*NaN*" value is returned.

It is also possible to supply a set of simulations :math:`\mathbf{y}` already
established elsewhere (so there's no explicit need for an operator
:math:`\mathcal{H}`), which are implicitly associated with a set of state
samples :math:`\mathbf{x}`. In this case where the set of simulations is
provided, it is imperative to also provide the set of states :math:`\mathbf{x}`
by explicit sampling, whose state order corresponds to the order of the
simulations :math:`\mathbf{y}`.

To access the calculated information, the results of the sampling or
simulations must be requested **explicitly** to avoid storage difficulties (if
no results are requested, nothing is available). One use for that, on the
desired variable, the final saving through "*UserPostAnalysis*" or the
treatment during the calculation by well suited "*observer*".

Note: in cases where sampling is generated, it may be useful to explicitly
obtain the collection of states :math:`\mathbf{x}` according to the definition
*a priori* without necessarily performing time-consuming calculations for the
functional :math:`J`. To do this, simply use this algorithm with simplified
calculations. For example, we can define a matrix observation operator equal to
the identity (square matrix of the state size), a draft and an observation
equal, worth 1 (vectors of the state size). Next, we set up the ADAO case with
this algorithm to recover the set of sampled states using the usual
“*CurrentState*” variable.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. include:: snippets/FeaturePropParallelAlgorithm.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/EnsembleOfSnapshots.rst

.. include:: snippets/QualityCriterion.rst

.. include:: snippets/SampleAsExplicitHyperCube.rst

.. include:: snippets/SampleAsIndependantRandomVariables.rst

.. include:: snippets/SampleAsMinMaxLatinHyperCube.rst

.. include:: snippets/SampleAsMinMaxSobolSequence.rst

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
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CurrentState",
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  "Innovation",
  "InnovationAtCurrentState",
  "SimulatedObservationAtCurrentState",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_SamplingTest_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo08.rst

- OPENTURNS, see the *User guide of OPENTURNS module* in the main "*Help*" menu of SALOME platform
