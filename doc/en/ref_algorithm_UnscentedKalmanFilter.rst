..
   Copyright (C) 2008-2014 EDF R&D

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

Description
+++++++++++

This algorithm realizes an estimation of the state of a dynamic system by a
"unscented" Kalman Filter, avoiding to have to perform the tangent and adjoint
operators for the observation and evolution operators, as in the simple or
extended Kalman filter.

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Bounds
.. index:: single: ConstrainedBy
.. index:: single: EstimationOf
.. index:: single: Alpha
.. index:: single: Beta
.. index:: single: Kappa
.. index:: single: Reconditioner
.. index:: single: StoreInternalVariables
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
indicated in :ref:`section_ref_assimilation_keywords`. In particular, the
optional command "*AlgorithmParameters*" allows to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_AlgorithmParameters` for the good use of this command.

The options of the algorithm are the following:

  Bounds
    This key allows to define upper and lower bounds for every state variable
    being optimized. Bounds have to be given by a list of list of pairs of
    lower/upper bounds for each variable, with extreme values every time there
    is no bound (``None`` is not allowed when there is no bound).

  ConstrainedBy
    This key allows to define the method to take bounds into account. The
    possible methods are in the following list: ["EstimateProjection"].

  EstimationOf
    This key allows to choose the type of estimation to be performed. It can be
    either state-estimation, with a value of "State", or parameter-estimation,
    with a value of "Parameters". The default choice is "State".
  
  Alpha, Beta, Kappa, Reconditioner
    These keys are internal scaling parameters. "Alpha" requires a value between
    1.e-4 and 1. "Beta" has an optimal value of 2 for Gaussian *a priori*
    distribution. "Kappa" requires an integer value, and the right default is
    obtained by setting it to 0. "Reconditioner" requires a value between 1.e-3
    and 10, it defaults to 1.

  StoreInternalVariables
    This Boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations. The default is a void list, none of these variables being
    calculated and stored by default. The possible names are in the following
    list: ["APosterioriCovariance", "BMA", "Innovation"].

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_KalmanFilter`
  - :ref:`section_ref_algorithm_ExtendedKalmanFilter`

Bibliographical references:
  - [WikipediaUKF]_
