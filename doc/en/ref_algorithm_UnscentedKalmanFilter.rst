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

.. index:: single: UnscentedKalmanFilter
.. _section_ref_algorithm_UnscentedKalmanFilter:

Calculation algorithm "*UnscentedKalmanFilter*"
-----------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm realizes an estimation of the state of a dynamic system by a
Kalman Filter using an "unscented" transform and a sampling by "sigma" points,
avoiding to have to perform the tangent and adjoint operators for the
observation and evolution operators, as in the simple or extended Kalman
filters.

It applies to non-linear observation and incremental evolution (process)
operators with excellent robustness and performance qualities. It can be
compared to the :ref:`section_ref_algorithm_EnsembleKalmanFilter`, whose
qualities are similar for non-linear systems.

We notice that there is no analysis performed at the initial time step
(numbered 0 in the time indexing) because there is no forecast at this time
(the background is stored as a pseudo analysis at the initial time step). If
the observations are provided in series by the user, the first one is therefore
not used. For a good understanding of time management, please refer to the
:ref:`schema_d_AD_temporel` and the explanations in the section
:ref:`section_theory_dynamic`.

In case of linear of "slightly" non-linear operators, one can easily use the
:ref:`section_ref_algorithm_ExtendedKalmanFilter` or even the
:ref:`section_ref_algorithm_KalmanFilter`, which are often far less expensive
to evaluate on small systems. One can verify the linearity of the operators
with the help of the :ref:`section_ref_algorithm_LinearityTest`.

There exists various variants of this algorithm. The following stable and
robust formulations are proposed here:

.. index::
    pair: Variant ; UKF
    pair: Variant ; S3F
    pair: Variant ; CUKF
    pair: Variant ; CS3F
    pair: Variant ; 2UKF

- "UKF" (Unscented Kalman Filter, see [Julier95]_, [Julier00]_, [Wan00]_),
  original and reference canonical algorithm, highly robust and efficient,
- "CUKF", also named "2UKF" (Constrained Unscented Kalman Filter, see
  [Julier07]_), inequality or boundary constrained version of the  algorithm
  "UKF",
- "S3F" (Scaled Spherical Simplex Filter, see [Papakonstantinou22]_),
  improved algorithm, reducing the number of sampling (sigma) points to achieve
  the same quality as the canonical "UKF" variant,
- "CS3F" (Constrained Scaled Spherical Simplex Filter), inequality or boundary
  constrained version of the  algorithm "S3F".

The following are a few practical suggestions for the effective use of these
algorithms:

- The recommended variant of this algorithm is the "S3F" even if the canonical
  "UKF" algorithm remains by default the more robust one.
- When there are no defined bounds, the constraint-aware versions of the
  algorithms are identical to the unconstrained versions. This is not the case
  if constraints are defined, even if the bounds are very wide.
- An essential difference between the algorithms is the number of sampling
  "sigma" points used, depending on the :math:`n` dimension of the state space.
  The canonical "UKF" algorithm uses :math:`2n+1`, the "S3F" algorithm uses
  :math:`n+2`. This means that about twice as many evaluations of the function to
  be simulated are required for one as for the other.
- The evaluations of the function to be simulated are algorithmically
  independent at each filtering stage (evolution or observation) and can
  therefore be parallelized or distributed if the function to be simulated
  supports this.

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

.. include:: snippets/ConstrainedBy.rst

.. include:: snippets/EstimationOf_State.rst

.. include:: snippets/AlphaBeta.rst

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
  "APosterioriCorrelations",
  "APosterioriCovariance",
  "APosterioriStandardDeviations",
  "APosterioriVariances",
  "BMA",
  "CostFunctionJ",
  "CostFunctionJAtCurrentOptimum",
  "CostFunctionJb",
  "CostFunctionJbAtCurrentOptimum",
  "CostFunctionJo",
  "CostFunctionJoAtCurrentOptimum",
  "CurrentOptimum",
  "CurrentState",
  "ForecastCovariance",
  "ForecastState",
  "IndexOfOptimum",
  "InnovationAtCurrentAnalysis",
  "InnovationAtCurrentState",
  "SimulatedObservationAtCurrentAnalysis",
  "SimulatedObservationAtCurrentOptimum",
  "SimulatedObservationAtCurrentState",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. include:: snippets/Variant_UKF.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/APosterioriCorrelations.rst

.. include:: snippets/APosterioriCovariance.rst

.. include:: snippets/APosterioriStandardDeviations.rst

.. include:: snippets/APosterioriVariances.rst

.. include:: snippets/BMA.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

.. include:: snippets/CurrentOptimum.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/ForecastCovariance.rst

.. include:: snippets/ForecastState.rst

.. include:: snippets/IndexOfOptimum.rst

.. include:: snippets/InnovationAtCurrentAnalysis.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentAnalysis.rst

.. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_UnscentedKalmanFilter_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_KalmanFilter`
- :ref:`section_ref_algorithm_ExtendedKalmanFilter`
- :ref:`section_ref_algorithm_EnsembleKalmanFilter`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Julier95]_
- [Julier00]_
- [Julier07]_
- [Papakonstantinou22]_
- [Wan00]_
- [WikipediaUKF]_
