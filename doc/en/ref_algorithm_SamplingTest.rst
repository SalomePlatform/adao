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

.. index:: single: SamplingTest
.. _section_ref_algorithm_SamplingTest:

Checking algorithm "*SamplingTest*"
-----------------------------------

Description
+++++++++++

This algorithm allows to calculate the values, linked to a :math:`\mathbf{x}`
state, of a general error function :math:`J` of type :math:`L^1`, :math:`L^2` or
:math:`L^{\infty}`, with or without weights, and of the observation operator,
for an priori given states sample. The default error function is the augmented
weighted least squares function, classically used in data assimilation.

It is useful to test the sensitivity, of the error function :math:`J`, in
particular, to the state :math:`\mathbf{x}` variations. When a state is not
observable, a *"NaN"* value is returned.

The sampling of the states :math:`\mathbf{x}` can be given explicitly or under
the form of hyper-cubes, explicit or sampled using classic distributions. Be
careful to the size of the hyper-cube (and then to the number of calculations)
that can be reached, it can be big very quickly.

To be visible by the user, the results of sampling has to be explicitly asked
for. One use for that, on the desired variable, the final saving through
"*UserPostAnalysis*" or the treatment during the calculation by "*observer*".

To perform distributed or more complex sampling, see OPENTURNS module available
in SALOME.

Optional and required commands
++++++++++++++++++++++++++++++

The general required commands, available in the editing user interface, are the
following:

  .. include:: snippets/CheckingPoint.rst

  .. include:: snippets/BackgroundError.rst

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationError.rst

  .. include:: snippets/ObservationOperator.rst

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`. Moreover, the parameters
of the command "*AlgorithmParameters*" allow to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_Algorithm_Parameters` for the good use of this
command.

The options of the algorithm are the following:
.. index:: single: SampleAsnUplet
.. index:: single: SampleAsExplicitHyperCube
.. index:: single: SampleAsMinMaxStepHyperCube
.. index:: single: SampleAsIndependantRandomVariables

  SampleAsnUplet
    This key describes the calculations points as a list of n-uplets, each
    n-uplet being a state.

    Example :
    ``{"SampleAsnUplet":[[0,1,2,3],[4,3,2,1],[-2,3,-4,5]]}`` for 3 points in a state space of dimension 4

  SampleAsExplicitHyperCube
    This key describes the calculations points as an hyper-cube, from a given
    list of explicit sampling of each variable as a list. That is then a list of
    lists, each of them being potentially of different size.

    Example : ``{"SampleAsExplicitHyperCube":[[0.,0.25,0.5,0.75,1.], [-2,2,1]]}`` for a state space of dimension 2

  SampleAsMinMaxStepHyperCube
    This key describes the calculations points as an hyper-cube, from a given
    list of implicit sampling of each variable by a triplet *[min,max,step]*.
    That is then a list of the same size than the one of the state. The bounds
    are included.

    Example :
    ``{"SampleAsMinMaxStepHyperCube":[[0.,1.,0.25],[-1,3,1]]}`` for a state space of dimension 2

  SampleAsIndependantRandomVariables
    This key describes the calculations points as an hyper-cube, for which the
    points on each axis come from a independent random sampling of the axis
    variable, under the specification of the distribution, its parameters and
    the number of points in the sample, as a list ``['distribution',
    [parameters], number]`` for each axis. The possible distributions are
    'normal' of parameters (mean,std), 'lognormal' of parameters (mean,sigma),
    'uniform' of parameters (low,high), or 'weibull' of parameter (shape). That
    is then a list of the same size than the one of the state.

    Example :
    ``{"SampleAsIndependantRandomVariables":[ ['normal',[0.,1.],3], ['uniform',[-2,2],4]]`` for a state space of dimension 2

  .. include:: snippets/QualityCriterion.rst

  .. include:: snippets/SetDebug.rst

  .. include:: snippets/SetSeed.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["CostFunctionJ", "CostFunctionJb",
    "CostFunctionJo", "CurrentState", "InnovationAtCurrentState",
    "SimulatedObservationAtCurrentState"].

    Example :
    ``{"StoreSupplementaryCalculations":["CostFunctionJ", "SimulatedObservationAtCurrentState"]}``

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

  .. include:: snippets/CostFunctionJ.rst

  .. include:: snippets/CostFunctionJb.rst

  .. include:: snippets/CostFunctionJo.rst

The conditional outputs of the algorithm are the following:

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/InnovationAtCurrentState.rst

  .. include:: snippets/SimulatedObservationAtCurrentState.rst

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_FunctionTest`

References to other SALOME modules:
  - OPENTURNS, see the *User guide of OPENTURNS module* in the main "*Help*" menu of SALOME platform
