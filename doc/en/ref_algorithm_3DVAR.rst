..
   Copyright (C) 2008-2015 EDF R&D

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

.. index:: single: 3DVAR
.. _section_ref_algorithm_3DVAR:

Calculation algorithm "*3DVAR*"
-------------------------------

Description
+++++++++++

This algorithm performs a state estimation by variational minimization of the
classical :math:`J` function in static data assimilation:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

which is usually designed as the "*3D-VAR*" function (see for example
[Talagrand97]_).

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Minimizer
.. index:: single: Bounds
.. index:: single: MaximumNumberOfSteps
.. index:: single: CostDecrementTolerance
.. index:: single: ProjectedGradientTolerance
.. index:: single: GradientNormTolerance
.. index:: single: StoreInternalVariables
.. index:: single: StoreSupplementaryCalculations
.. index:: single: Quantiles
.. index:: single: SetSeed
.. index:: single: NumberOfSamplesForQuantiles
.. index:: single: SimulationForQuantiles

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

  StoreInternalVariables
    This Boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

    Example : ``{"StoreInternalVariables":True}``

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaObs2", "MahalanobisConsistency", "SimulationQuantiles"].

    Example : ``{"StoreSupplementaryCalculations":["BMA","Innovation"]}``

  Quantiles
    This list indicates the values of quantile, between 0 and 1, to be estimated
    by simulation around the optimal state. The sampling uses a multivariate
    gaussian random sampling, directed by the *a posteriori* covariance matrix.
    This option is useful only if the supplementary calculation
    "SimulationQuantiles" has been chosen. The default is a void list.

    Example : ``{"Quantiles":[0.1,0.9]}``

  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

    Example : ``{"SetSeed":1000}``

  NumberOfSamplesForQuantiles
    This key indicates the number of simulation to be done in order to estimate
    the quantiles. This option is useful only if the supplementary calculation
    "SimulationQuantiles" has been chosen. The default is 100, which is often
    sufficient for correct estimation of common quantiles at 5%, 10%, 90% or
    95%.

    Example : ``{"NumberOfSamplesForQuantiles":100}``

  SimulationForQuantiles
    This key indicates the type of simulation, linear (with the tangent
    observation operator applied to perturbation increments around the optimal
    state) or non-linear (with standard observation operator applied to
    perturbated states), one want to do for each perturbation. It changes mainly
    the time of each elementary calculation, usually longer in non-linear than
    in linear. This option is useful only if the supplementary calculation
    "SimulationQuantiles" has been chosen. The default value is "Linear", and
    the possible choices are "Linear" and "NonLinear".

    Example : ``{"SimulationForQuantiles":"Linear"}``

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

  APosterioriCovariance
    *List of matrices*. Each element is an *a posteriori* error covariance
    matrix :math:`\mathbf{A}*` of the optimal state.

    Example : ``A = ADD.get("APosterioriCovariance")[-1]``

  BMA
    *List of vectors*. Each element is a vector of difference between the
    background and the optimal state.

    Example : ``bma = ADD.get("BMA")[-1]``

  CurrentState
    *List of vectors*. Each element is a usual state vector used during the
    optimization algorithm procedure.

    Example : ``Xs = ADD.get("CurrentState")[:]``

  Innovation
    *List of vectors*. Each element is an innovation vector, which is in static
    the difference between the optimal and the background, and in dynamic the
    evolution increment.

    Example : ``d = ADD.get("Innovation")[-1]``

  MahalanobisConsistency
    *List of values*. Each element is a value of the Mahalanobis quality
    indicator.

    Example : ``m = ADD.get("MahalanobisConsistency")[-1]``

  OMA
    *List of vectors*. Each element is a vector of difference between the
    observation and the optimal state in the observation space.

    Example : ``oma = ADD.get("OMA")[-1]``

  OMB
    *List of vectors*. Each element is a vector of difference between the
    observation and the background state in the observation space.

    Example : ``omb = ADD.get("OMB")[-1]``

  SigmaObs2
    *List of values*. Each element is a value of the quality indicator
    :math:`(\sigma^o)^2` of the observation part.

    Example : ``so2 = ADD.get("SigmaObs")[-1]``

  SimulationQuantiles
    *List of vectors*. Each element is a vector corresponding to the observed
    state which realize the required quantile, in the same order than the
    quantiles required by the user.

    Example : ``sQuantiles = ADD.get("SimulationQuantiles")[:]``

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_Blue`
  - :ref:`section_ref_algorithm_ExtendedBlue`
  - :ref:`section_ref_algorithm_LinearityTest`

Bibliographical references:
  - [Byrd95]_
  - [Morales11]_
  - [Talagrand97]_
