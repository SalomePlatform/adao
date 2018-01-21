..
   Copyright (C) 2008-2018 EDF R&D

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

.. warning::

  in its present version, this algorithm is experimental, and so changes can be
  required in forthcoming versions.

Description
+++++++++++

This algorithm realizes an estimation of the state of a dynamic system by a
Ensemble Kalman Filter (EnKF), avoiding to have to perform the tangent and
adjoint operators for the observation and evolution operators, as in the simple
or extended Kalman filter.

It applies to non-linear observation and incremental evolution (process)
operators with excellent robustness and performance qualities. It can be
compared to the :ref:`section_ref_algorithm_UnscentedKalmanFilter`, whose
qualities are similar for non-linear systems.

In case of linear of "slightly" non-linear operators, one can easily use the
:ref:`section_ref_algorithm_ExtendedKalmanFilter` or even the
:ref:`section_ref_algorithm_KalmanFilter`, which are often far less expensive
to evaluate on small systems. One can verify the linearity of the operators
with the help of the :ref:`section_ref_algorithm_LinearityTest`.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

The general required commands, available in the editing user interface, are the
following:

  .. include:: snippets/Background.rst

  .. include:: snippets/BackgroundError.rst

  .. include:: snippets/EvolutionError.rst

  .. include:: snippets/EvolutionModel.rst

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationError.rst

  .. include:: snippets/ObservationOperator.rst

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`. Moreover, the parameters
of the command "*AlgorithmParameters*" allows to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_Algorithm_Parameters` for the good use of this
command.

The options of the algorithm are the following:

  .. include:: snippets/NumberOfMembers.rst

  .. include:: snippets/EstimationOf.rst

  .. include:: snippets/SetSeed.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["APosterioriCorrelations",
    "APosterioriCovariance", "APosterioriStandardDeviations",
    "APosterioriVariances", "BMA", "CostFunctionJ", "CostFunctionJb",
    "CostFunctionJo", "CurrentState"].

    Example :
    ``{"StoreSupplementaryCalculations":["CurrentState"]}``

Information and variables available at the end of the algorithm
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

At the output, after executing the algorithm, there are variables and
information originating from the calculation. The description of
:ref:`section_ref_output_variables` show the way to obtain them by the method
named ``get`` of the variable "*ADD*" of the post-processing. The input
variables, available to the user at the output in order to facilitate the
writing of post-processing procedures, are described in the
:ref:`subsection_r_o_v_Inventaire`.

The unconditional outputs of the algorithm are the following:

  .. include:: snippets/Analysis.rst

The conditional outputs of the algorithm are the following:

  .. include:: snippets/APosterioriCorrelations.rst

  .. include:: snippets/APosterioriCovariance.rst

  .. include:: snippets/APosterioriStandardDeviations.rst

  .. include:: snippets/APosterioriVariances.rst

  .. include:: snippets/BMA.rst

  .. include:: snippets/CostFunctionJ.rst

  .. include:: snippets/CostFunctionJb.rst

  .. include:: snippets/CostFunctionJo.rst

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/Innovation.rst

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_KalmanFilter`
  - :ref:`section_ref_algorithm_ExtendedKalmanFilter`
  - :ref:`section_ref_algorithm_UnscentedKalmanFilter`

Bibliographical references:
  - [Evensen94]_
  - [Burgers98]_
  - [Evensen03]_
  - [WikipediaEnKF]_
