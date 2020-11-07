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

.. index:: single: KalmanFilter
.. _section_ref_algorithm_KalmanFilter:

Calculation algorithm "*KalmanFilter*"
--------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm realizes an estimation of the state of a dynamic system by a
Kalman Filter.

It is theoretically reserved for observation and incremental evolution operators
cases which are linear, even if it sometimes works in "slightly" non-linear
cases. One can verify the linearity of the operators with the help of
the :ref:`section_ref_algorithm_LinearityTest`.

Conceptually, we can represent the temporal pattern of action of the operators
for this algorithm in the following way, with **x** the state, **P** the state
error covariance, **H** the observation operator and **M** the evolution
operator :

  .. _schema_temporel_KF:
  .. image:: images/schema_temporel_KF.png
    :align: center
    :width: 50%
  .. centered::
    **Timeline of steps in Kalman filter assimilation**

We notice that there is no analysis performed at the initial time step
(numbered 0 in the time indexing) because there is no forecast at this time
(the background is stored as a pseudo analysis at the initial time step). If
the observations are provided in series by the user, the first one is therefore
not used.

In case of non-linearity, even slightly marked, it will be preferred the
:ref:`section_ref_algorithm_ExtendedKalmanFilter`, or the
:ref:`section_ref_algorithm_UnscentedKalmanFilter` and the
:ref:`section_ref_algorithm_UnscentedKalmanFilter` that are more powerful. One
can verify the linearity of the operators
with the help of the :ref:`section_ref_algorithm_LinearityTest`.

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

.. include:: snippets/EstimationOf.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *List of names*. This list indicates the names of the supplementary variables
  that can be available during or at the end of the algorithm, if they are
  initially required by the user. It involves potentially costly calculations
  or memory consumptions. The default is a void list, none of these variables
  being calculated and stored by default excepted the unconditionnal variables.
  The possible names are in the following list: [
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
  "ForecastState",
  "IndexOfOptimum",
  "InnovationAtCurrentAnalysis",
  "InnovationAtCurrentState",
  "SimulatedObservationAtCurrentAnalysis",
  "SimulatedObservationAtCurrentOptimum",
  "SimulatedObservationAtCurrentState",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

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

.. include:: snippets/ForecastState.rst

.. include:: snippets/IndexOfOptimum.rst

.. include:: snippets/InnovationAtCurrentAnalysis.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentAnalysis.rst

.. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_ExtendedKalmanFilter`
- :ref:`section_ref_algorithm_EnsembleKalmanFilter`
- :ref:`section_ref_algorithm_UnscentedKalmanFilter`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [WikipediaKF]_
