..
   Copyright (C) 2008-2019 EDF R&D

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

.. index:: single: ExtendedKalmanFilter
.. _section_ref_algorithm_ExtendedKalmanFilter:

Calculation algorithm "*ExtendedKalmanFilter*"
----------------------------------------------

Description
+++++++++++

This algorithm realizes an estimation of the state of a dynamic system by a
extended Kalman Filter, using a non-linear calculation of the state and the
incremental evolution (process).

In case of really non-linear operators, one can easily use the
:ref:`section_ref_algorithm_EnsembleKalmanFilter` or the
:ref:`section_ref_algorithm_UnscentedKalmanFilter`, which are often far more
adapted to non-linear behavior but more costly. One can verify the linearity of
the operators with the help of the :ref:`section_ref_algorithm_LinearityTest`.

Optional and required commands
++++++++++++++++++++++++++++++

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

  .. include:: snippets/BoundsWithExtremes.rst

  .. include:: snippets/ConstrainedBy.rst

  .. include:: snippets/EstimationOf.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["APosterioriCorrelations",
    "APosterioriCovariance", "APosterioriStandardDeviations",
    "APosterioriVariances", "BMA", "CostFunctionJ", "CostFunctionJb",
    "CostFunctionJo", "CurrentState", "Innovation"].

    Example :
    ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

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
  - :ref:`section_ref_algorithm_EnsembleKalmanFilter`
  - :ref:`section_ref_algorithm_UnscentedKalmanFilter`
