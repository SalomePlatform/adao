..
   Copyright (C) 2008-2016 EDF R&D

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

Description
+++++++++++

This algorithm realizes an estimation of the state of a dynamic system by a
Kalman Filter.

It is theoretically reserved for observation and incremental evolution operators
cases which are linear, even if it sometimes works in "slightly" non-linear
cases. One can verify the linearity of the observation operator with the help of
the :ref:`section_ref_algorithm_LinearityTest`.

In case of non-linearity, even slightly marked, it will be preferred the
:ref:`section_ref_algorithm_ExtendedKalmanFilter` or the
:ref:`section_ref_algorithm_UnscentedKalmanFilter`.

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: EstimationOf
.. index:: single: StoreSupplementaryCalculations

The general required commands, available in the editing user interface, are the
following:

  Background
    *Required command*. This indicates the background or initial vector used,
    previously noted as :math:`\mathbf{x}^b`. Its value is defined as a
    "*Vector*" or a *VectorSerie*" type object.

  BackgroundError
    *Required command*. This indicates the background error covariance matrix,
    previously noted as :math:`\mathbf{B}`. Its value is defined as a "*Matrix*"
    type object, a "*ScalarSparseMatrix*" type object, or a
    "*DiagonalSparseMatrix*" type object.

  Observation
    *Required command*. This indicates the observation vector used for data
    assimilation or optimization, previously noted as :math:`\mathbf{y}^o`. It
    is defined as a "*Vector*" or a *VectorSerie* type object.

  ObservationError
    *Required command*. This indicates the observation error covariance matrix,
    previously noted as :math:`\mathbf{R}`. It is defined as a "*Matrix*" type
    object, a "*ScalarSparseMatrix*" type object, or a "*DiagonalSparseMatrix*"
    type object.

  ObservationOperator
    *Required command*. This indicates the observation operator, previously
    noted :math:`H`, which transforms the input parameters :math:`\mathbf{x}` to
    results :math:`\mathbf{y}` to be compared to observations
    :math:`\mathbf{y}^o`. Its value is defined as a "*Function*" type object or
    a "*Matrix*" type one. In the case of "*Function*" type, different
    functional forms can be used, as described in the section
    :ref:`section_ref_operator_requirements`. If there is some control :math:`U`
    included in the observation, the operator has to be applied to a pair
    :math:`(X,U)`.

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`. Moreover, the parameters
of the command "*AlgorithmParameters*" allows to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_Algorithm_Parameters` for the good use of this
command.

The options of the algorithm are the following:

  EstimationOf
    This key allows to choose the type of estimation to be performed. It can be
    either state-estimation, with a value of "State", or parameter-estimation,
    with a value of "Parameters". The default choice is "State".

    Example : ``{"EstimationOf":"Parameters"}``

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["APosterioriCorrelations",
    "APosterioriCovariance", "APosterioriStandardDeviations",
    "APosterioriVariances", "BMA", "CostFunctionJ", "CurrentState",
    "Innovation"].

    Example : ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

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

  Analysis
    *List of vectors*. Each element is an optimal state :math:`\mathbf{x}*` in
    optimization or an analysis :math:`\mathbf{x}^a` in data assimilation.

    Example : ``Xa = ADD.get("Analysis")[-1]``

The conditional outputs of the algorithm are the following:

  APosterioriCorrelations
    *List of matrices*. Each element is an *a posteriori* error correlation
    matrix of the optimal state.

    Example : ``C = ADD.get("APosterioriCorrelations")[-1]``

  APosterioriCovariance
    *List of matrices*. Each element is an *a posteriori* error covariance
    matrix :math:`\mathbf{A}*` of the optimal state.

    Example : ``A = ADD.get("APosterioriCovariance")[-1]``

  APosterioriStandardDeviations
    *List of matrices*. Each element is an *a posteriori* error standard
    deviation matrix of the optimal state.

    Example : ``E = ADD.get("APosterioriStandardDeviations")[-1]``

  APosterioriVariances
    *List of matrices*. Each element is an *a posteriori* error variance matrix
    of the optimal state.

    Example : ``V = ADD.get("APosterioriVariances")[-1]``

  BMA
    *List of vectors*. Each element is a vector of difference between the
    background and the optimal state.

    Example : ``bma = ADD.get("BMA")[-1]``

  CostFunctionJ
    *List of values*. Each element is a value of the error function :math:`J`.

    Example : ``J = ADD.get("CostFunctionJ")[:]``

  CostFunctionJb
    *List of values*. Each element is a value of the error function :math:`J^b`,
    that is of the background difference part.

    Example : ``Jb = ADD.get("CostFunctionJb")[:]``

  CostFunctionJo
    *List of values*. Each element is a value of the error function :math:`J^o`,
    that is of the observation difference part.

    Example : ``Jo = ADD.get("CostFunctionJo")[:]``

  CurrentState
    *List of vectors*. Each element is a usual state vector used during the
    optimization algorithm procedure.

    Example : ``Xs = ADD.get("CurrentState")[:]``

  Innovation
    *List of vectors*. Each element is an innovation vector, which is in static
    the difference between the optimal and the background, and in dynamic the
    evolution increment.

    Exemple : ``d = ADD.get("Innovation")[-1]``

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_ExtendedKalmanFilter`
  - :ref:`section_ref_algorithm_UnscentedKalmanFilter`
