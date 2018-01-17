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

.. index:: single: QuantileRegression
.. _section_ref_algorithm_QuantileRegression:

Calculation algorithm "*QuantileRegression*"
--------------------------------------------

Description
+++++++++++

This algorithm allows to estimate the conditional quantiles of the state
parameters distribution, expressed with a model of the observed variables. These
are then the quantiles on the observed variables which will allow to determine
the model parameters that satisfy to the quantiles conditions.

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: Observation
.. index:: single: ObservationOperator
.. index:: single: Quantile
.. index:: single: Minimizer
.. index:: single: MaximumNumberOfSteps
.. index:: single: CostDecrementTolerance
.. index:: single: Bounds
.. index:: single: StoreSupplementaryCalculations

The general required commands, available in the editing user interface, are the
following:

  Background
    *Required command*. This indicates the background or initial vector used,
    previously noted as :math:`\mathbf{x}^b`. Its value is defined as a
    "*Vector*" or a *VectorSerie*" type object.

  Observation
    *Required command*. This indicates the observation vector used for data
    assimilation or optimization, previously noted as :math:`\mathbf{y}^o`. It
    is defined as a "*Vector*" or a *VectorSerie* type object.

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

  Quantile
    This key allows to define the real value of the desired quantile, between
    0 and 1. The default is 0.5, corresponding to the median.

    Example : ``{"Quantile":0.5}``

  MaximumNumberOfSteps
    This key indicates the maximum number of iterations allowed for iterative
    optimization. The default is 15000, which is very similar to no limit on
    iterations. It is then recommended to adapt this parameter to the needs on
    real problems.

    Example : ``{"MaximumNumberOfSteps":100}``

  CostDecrementTolerance
    This key indicates a limit value, leading to stop successfully the
    iterative optimization process when the cost function or the surrogate
    decreases less than this tolerance at the last step. The default is 1.e-6,
    and it is recommended to adapt it to the needs on real problems.

    Example : ``{"CostDecrementTolerance":1.e-7}``

  Bounds
    This key allows to define upper and lower bounds for every state variable
    being optimized. Bounds have to be given by a list of list of pairs of
    lower/upper bounds for each variable, with possibly ``None`` every time
    there is no bound. The bounds can always be specified, but they are taken
    into account only by the constrained optimizers.

    Example : ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["BMA", "CostFunctionJ", "CostFunctionJb",
    "CostFunctionJo", "CurrentState", "OMA", "OMB", "Innovation",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum"].

    Example : ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

*Tips for this algorithm:*

    As the *"BackgroundError"* and *"ObservationError"* commands are required
    for ALL the calculation algorithms in the interface, you have to provide a
    value, even if these commands are not required for this algorithm, and will
    not be used. The simplest way is to give "1" as a STRING for both.

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

  CurrentState
    *List of vectors*. Each element is a usual state vector used during the
    optimization algorithm procedure.

    Example : ``Xs = ADD.get("CurrentState")[:]``

  Innovation
    *List of vectors*. Each element is an innovation vector, which is in static
    the difference between the optimal and the background, and in dynamic the
    evolution increment.

    Example : ``d = ADD.get("Innovation")[-1]``

  OMA
    *List of vectors*. Each element is a vector of difference between the
    observation and the optimal state in the observation space.

    Example : ``oma = ADD.get("OMA")[-1]``

  OMB
    *List of vectors*. Each element is a vector of difference between the
    observation and the background state in the observation space.

    Example : ``omb = ADD.get("OMB")[-1]``

  SimulatedObservationAtBackground
    *List of vectors*. Each element is a vector of observation simulated from
    the background :math:`\mathbf{x}^b`.

    Example : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtCurrentState
    *List of vectors*. Each element is an observed vector at the current state,
    that is, in the observation space.

    Example : ``Ys = ADD.get("SimulatedObservationAtCurrentState")[-1]``

  SimulatedObservationAtOptimum
    *List of vectors*. Each element is a vector of observation simulated from
    the analysis or optimal state :math:`\mathbf{x}^a`.

    Example : ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``

See also
++++++++

Bibliographical references:
  - [Buchinsky98]_
  - [Cade03]_
  - [Koenker00]_
  - [Koenker01]_
  - [WikipediaQR]_
