..
   Copyright (C) 2008-2017 EDF R&D

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

.. index:: single: ExtendedBlue
.. _section_ref_algorithm_ExtendedBlue:

Calculation algorithm "*ExtendedBlue*"
--------------------------------------

Description
+++++++++++

This algorithm realizes an extended BLUE (Best Linear Unbiased Estimator) type
estimation of the state of a system.

This algorithm is a partially non-linear generalization of the
:ref:`section_ref_algorithm_Blue`. It is equivalent for a linear observation
operator. One can verify the linearity of the observation operator with the help
of the :ref:`section_ref_algorithm_LinearityTest`.

In case of non-linearity, it is close to the :ref:`section_ref_algorithm_3DVAR`,
without being entirely equivalent.

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
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
indicated in :ref:`section_ref_assimilation_keywords`. Moreover, the parameters
of the command "*AlgorithmParameters*" allows to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_Algorithm_Parameters` for the good use of this
command.

The options of the algorithm are the following:

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["APosterioriCorrelations",
    "APosterioriCovariance", "APosterioriStandardDeviations",
    "APosterioriVariances", "BMA", "OMA", "OMB", "CurrentState",
    "CostFunctionJ", "CostFunctionJb", "CostFunctionJo", "Innovation",
    "SigmaBck2", "SigmaObs2", "MahalanobisConsistency", "SimulationQuantiles",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum"].

    Example : ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

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

  SigmaBck2
    *List of values*. Each element is a value of the quality indicator
    :math:`(\sigma^b)^2` of the background part.

    Example : ``sb2 = ADD.get("SigmaBck")[-1]``

  SigmaObs2
    *List of values*. Each element is a value of the quality indicator
    :math:`(\sigma^o)^2` of the observation part.

    Example : ``so2 = ADD.get("SigmaObs")[-1]``

  SimulatedObservationAtBackground
    *List of vectors*. Each element is a vector of observation simulated from
    the background :math:`\mathbf{x}^b`.

    Example : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtOptimum
    *List of vectors*. Each element is a vector of observation simulated from
    the analysis or optimal state :math:`\mathbf{x}^a`.

    Example : ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``

  SimulationQuantiles
    *List of vectors*. Each element is a vector corresponding to the observed
    state which realize the required quantile, in the same order than the
    quantiles required by the user.

    Example : ``sQuantiles = ADD.get("SimulationQuantiles")[:]``

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_Blue`
  - :ref:`section_ref_algorithm_3DVAR`
  - :ref:`section_ref_algorithm_LinearityTest`
