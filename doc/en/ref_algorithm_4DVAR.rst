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

.. index:: single: 4DVAR
.. _section_ref_algorithm_4DVAR:

Calculation algorithm "*4DVAR*"
-------------------------------

.. warning::

  in its present version, this algorithm is experimental, and so changes can be
  required in forthcoming versions.

Description
+++++++++++

This algorithm realizes an estimation of the state of a dynamic system, by a
variational minimization method of the classical :math:`J` function in data
assimilation:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\sum_{t\in T}(\mathbf{y^o}(t)-H(\mathbf{x},t))^T.\mathbf{R}^{-1}.(\mathbf{y^o}(t)-H(\mathbf{x},t))

which is usually designed as the "*4D-VAR*" function (see for example
[Talagrand97]_). It is well suited in cases of non-linear observation and
evolution operators, its application domain is similar to the one of Kalman
filters, specially the :ref:`section_ref_algorithm_ExtendedKalmanFilter` or the
:ref:`section_ref_algorithm_UnscentedKalmanFilter`.

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Bounds
.. index:: single: ConstrainedBy
.. index:: single: EstimationOf
.. index:: single: MaximumNumberOfSteps
.. index:: single: CostDecrementTolerance
.. index:: single: ProjectedGradientTolerance
.. index:: single: GradientNormTolerance
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

  Minimizer
    This key allows to choose the optimization minimizer. The default choice is
    "LBFGSB", and the possible ones are "LBFGSB" (nonlinear constrained
    minimizer, see [Byrd95]_, [Morales11]_ and [Zhu97]_), "TNC" (nonlinear
    constrained minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS"
    (nonlinear unconstrained minimizer), "NCG" (Newton CG minimizer). It is
    strongly recommended to stay with the default.

    Example : ``{"Minimizer":"LBFGSB"}``

  Bounds
    This key allows to define upper and lower bounds for every state variable
    being optimized. Bounds have to be given by a list of list of pairs of
    lower/upper bounds for each variable, with possibly ``None`` every time
    there is no bound. The bounds can always be specified, but they are taken
    into account only by the constrained optimizers.

    Example : ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``

  ConstrainedBy
    This key allows to choose the method to take into account the bounds
    constraints. The only one available is the "EstimateProjection", which
    projects the current state estimate on the bounds constraints.

    Example : ``{"ConstrainedBy":"EstimateProjection"}``

  MaximumNumberOfSteps
    This key indicates the maximum number of iterations allowed for iterative
    optimization. The default is 15000, which is very similar to no limit on
    iterations. It is then recommended to adapt this parameter to the needs on
    real problems. For some optimizers, the effective stopping step can be
    slightly different of the limit due to algorithm internal control
    requirements.

    Example : ``{"MaximumNumberOfSteps":100}``

  CostDecrementTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the cost function decreases less than
    this tolerance at the last step. The default is 1.e-7, and it is
    recommended to adapt it to the needs on real problems.

    Example : ``{"CostDecrementTolerance":1.e-7}``

  EstimationOf
    This key allows to choose the type of estimation to be performed. It can be
    either state-estimation, with a value of "State", or parameter-estimation,
    with a value of "Parameters". The default choice is "State".

    Example : ``{"EstimationOf":"Parameters"}``

  ProjectedGradientTolerance
    This key indicates a limit value, leading to stop successfully the iterative
    optimization process when all the components of the projected gradient are
    under this limit. It is only used for constrained optimizers. The default is
    -1, that is the internal default of each minimizer (generally 1.e-5), and it
    is not recommended to change it.

    Example : ``{"ProjectedGradientTolerance":-1}``

  GradientNormTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the norm of the gradient is under this
    limit. It is only used for non-constrained optimizers.  The default is
    1.e-5 and it is not recommended to change it.

    Example : ``{"GradientNormTolerance":1.e-5}``

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["BMA", "CostFunctionJ",
    "CostFunctionJb", "CostFunctionJo", "CostFunctionJAtCurrentOptimum",
    "CostFunctionJbAtCurrentOptimum", "CostFunctionJoAtCurrentOptimum",
    "CurrentOptimum", "CurrentState", "IndexOfOptimum"].

    Example : ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

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

The conditional outputs of the algorithm are the following:

  BMA
    *List of vectors*. Each element is a vector of difference between the
    background and the optimal state.

    Example : ``bma = ADD.get("BMA")[-1]``

  CostFunctionJAtCurrentOptimum
    *List of values*. Each element is a value of the error function :math:`J`.
    At each step, the value corresponds to the optimal state found from the
    beginning.

    Example : ``JACO = ADD.get("CostFunctionJAtCurrentOptimum")[:]``

  CostFunctionJbAtCurrentOptimum
    *List of values*. Each element is a value of the error function :math:`J^b`,
    that is of the background difference part. At each step, the value
    corresponds to the optimal state found from the beginning.

    Example : ``JbACO = ADD.get("CostFunctionJbAtCurrentOptimum")[:]``

  CostFunctionJoAtCurrentOptimum
    *List of values*. Each element is a value of the error function :math:`J^o`,
    that is of the observation difference part. At each step, the value
    corresponds to the optimal state found from the beginning.

    Example : ``JoACO = ADD.get("CostFunctionJoAtCurrentOptimum")[:]``

  CurrentOptimum
    *List of vectors*. Each element is the optimal state obtained at the current
    step of the optimization algorithm. It is not necessarily the last state.

    Example : ``Xo = ADD.get("CurrentOptimum")[:]``

  CurrentState
    *List of vectors*. Each element is a usual state vector used during the
    optimization algorithm procedure.

    Example : ``Xs = ADD.get("CurrentState")[:]``

  IndexOfOptimum
    *List of integers*. Each element is the iteration index of the optimum
    obtained at the current step the optimization algorithm. It is not
    necessarily the number of the last iteration.

    Example : ``i = ADD.get("IndexOfOptimum")[-1]``

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_3DVAR`
  - :ref:`section_ref_algorithm_KalmanFilter`
  - :ref:`section_ref_algorithm_ExtendedKalmanFilter`

Bibliographical references:
  - [Byrd95]_
  - [Morales11]_
  - [Talagrand97]_
  - [Zhu97]_
