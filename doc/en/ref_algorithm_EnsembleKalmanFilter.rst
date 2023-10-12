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

.. index:: single: EnsembleKalmanFilter
.. _section_ref_algorithm_EnsembleKalmanFilter:

Calculation algorithm "*EnsembleKalmanFilter*"
----------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm realizes an estimation of the state of a dynamic system by a
Ensemble Kalman Filter (EnKF), avoiding to have to perform the tangent or
adjoint operators for the observation and evolution operators, as in the simple
or extended Kalman filters.

It applies to non-linear observation and incremental evolution (process)
operators with excellent robustness and performance qualities. It can be
interpreted as an order reduction of the classical Kalman filter, with a
remarkable assimilation quality of this filtering for large problems. It can be
compared to the :ref:`section_ref_algorithm_UnscentedKalmanFilter`, whose
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

There are many deterministic or stochastic variants of this algorithm, allowing
in particular to perform size reduction of algebraic problems at different
levels (by using reduced rank methods, dimension reduction, changes of
computational space, leading to schemes of type Ensemble Square Root Kalman
Filters (EnSRKF) or Reduced-Rank Square Root Filters (RRSQRT), to deterministic
transformations...). We do not go into the complex details of classifications
and algorithmic equivalences, which are available in the literature. The
following stable and robust formulations are proposed here:

.. index::
    pair: Variant ; EnKF
    pair: Variant ; ETKF
    pair: Variant ; ETKF-N
    pair: Variant ; MLEF
    pair: Variant ; IEnKF
    pair: Variant ; E3DVAR
    pair: Variant ; 3D-Var-Ben
    pair: Variant ; EnKS
    pair: Variant ; EnSRKF
    pair: Variant ; RRSQRT

- "EnKF" (Ensemble Kalman Filter, see [Evensen94]_), original stochastic algorithm, allowing consistent treatment of non-linear evolution operator,
- "ETKF" (Ensemble-Transform Kalman Filter), deterministic EnKF algorithm, allowing treatment of non-linear evolution operator with a lot less members (one recommends to use a number of members on the order of 10 or even sometimes less),
- "ETKF-N" (Ensemble-Transform Kalman Filter of finite size N), ETKF algorithm of "finite size N", that doesn't need inflation that is often required with the other algorithms,
- "MLEF" (Maximum Likelihood Kalman Filter, see [Zupanski05]_), deterministic EnKF algorithm, allowing in addition the consistent treatment of non-linear observation operator,
- "IEnKF" (Iterative EnKF), deterministic EnKF algorithm, improving treament of operators non-linearities
- "E3DVAR" (EnKF 3DVAR, or 3D-Var-Ben), algorithm coupling ensemble and variational assimilation, which uses in parallel a 3DVAR variational assimilation for a single best estimate and an EnKF ensemble algorithm to improve the estimation of *a posteriori* error covariances
- "EnKS" (Ensemble Kalman Smoother), smoothing algorithm with a fixed time lag L.

Without being a universal recommendation, one recommend to use "EnKF"
formulation as a reference algorithm, **"ETKF-N" ou "IEnKF" formulation for
robust performance**, and the other algorithms (in this order) as means to
obtain a less costly data assimilation with (hopefully) the same quality.

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

.. include:: snippets/EstimationOf_State.rst

.. include:: snippets/HybridCostDecrementTolerance.rst

.. include:: snippets/HybridCovarianceEquilibrium.rst

.. include:: snippets/HybridMaximumNumberOfIterations.rst

.. include:: snippets/InflationFactor.rst

.. include:: snippets/InflationType.rst

.. include:: snippets/NumberOfMembers.rst

.. include:: snippets/SetSeed.rst

.. include:: snippets/SmootherLagL.rst

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
  "CurrentIterationNumber",
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

.. include:: snippets/Variant_EnKF.rst

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

.. include:: snippets/CurrentIterationNumber.rst

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
.. _section_ref_algorithm_EnsembleKalmanFilter_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_KalmanFilter`
- :ref:`section_ref_algorithm_ExtendedKalmanFilter`
- :ref:`section_ref_algorithm_UnscentedKalmanFilter`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Evensen94]_
- [Burgers98]_
- [Bishop01]_
- [Evensen03]_
- [Zupanski05]_
- [Hamill00]_
- [WikipediaEnKF]_
