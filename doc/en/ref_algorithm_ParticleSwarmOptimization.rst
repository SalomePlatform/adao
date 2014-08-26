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

.. index:: single: ParticleSwarmOptimization
.. _section_ref_algorithm_ParticleSwarmOptimization:

Calculation algorithm "*ParticleSwarmOptimization*"
---------------------------------------------------

Description
+++++++++++

This algorithm realizes an estimation of the state of a dynamic system by a
particle swarm.

This is an optimization method allowing for global minimum search of a general
error function :math:`J` of type :math:`L^1`, :math:`L^2` or :math:`L^{\infty}`,
with or without weights. The default error function is the augmented weighted
least squares function, classicaly used in data assimilation.

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: MaximumNumberOfSteps
.. index:: single: NumberOfInsects
.. index:: single: SwarmVelocity
.. index:: single: GroupRecallRate
.. index:: single: QualityCriterion
.. index:: single: BoxBounds
.. index:: single: SetSeed
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

  MaximumNumberOfSteps
    This key indicates the maximum number of iterations allowed for iterative
    optimization. The default is 50, which is an arbitrary limit. It is then
    recommended to adapt this parameter to the needs on real problems.

    Example : ``{"MaximumNumberOfSteps":100}``

  NumberOfInsects
    This key indicates the number of insects or particles in the swarm. The
    default is 100, which is a usual default for this algorithm.

    Example : ``{"NumberOfInsects":100}``

  SwarmVelocity
    This key indicates the part of the insect velocity which is imposed by the 
    swarm. It is a positive floating point value. The default value is 1.

    Example : ``{"SwarmVelocity":1.}``

  GroupRecallRate
    This key indicates the recall rate at the best swarm insect. It is a
    floating point value between 0 and 1. The default value is 0.5.

    Example : ``{"GroupRecallRate":0.5}``

  QualityCriterion
    This key indicates the quality criterion, minimized to find the optimal
    state estimate. The default is the usual data assimilation criterion named
    "DA", the augmented weighted least squares. The possible criteria has to be
    in the following list, where the equivalent names are indicated by the sign
    "=": ["AugmentedWeightedLeastSquares"="AWLS"="DA",
    "WeightedLeastSquares"="WLS", "LeastSquares"="LS"="L2",
    "AbsoluteValue"="L1", "MaximumError"="ME"].

    Example : ``{"QualityCriterion":"DA"}``

  BoxBounds
    This key allows to define upper and lower bounds for *increments* on every
    state variable being optimized (and not on state variables themselves).
    Bounds have to be given by a list of list of pairs of lower/upper bounds for
    each increment on variable, with extreme values every time there is no bound
    (``None`` is not allowed when there is no bound). This key is required and
    there is no default values.

    Example : ``{"BoxBounds":[[-0.5,0.5],[0.01,2.],[0.,1.e99],[-1.e99,1.e99]]}``

  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

    Example : ``{"SetSeed":1000}``

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
    are in the following list: ["BMA", "OMA", "OMB", "Innovation"].

    Example : ``{"StoreSupplementaryCalculations":["BMA","Innovation"]}``

See also
++++++++

References to other sections:
  - [WikipediaPSO]_