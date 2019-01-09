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

  Minimizer
    .. index:: single: Minimizer

    This key allows to choose the optimization minimizer. The default choice is
    "LBFGSB", and the possible ones are "LBFGSB" (nonlinear constrained
    minimizer, see [Byrd95]_, [Morales11]_ and [Zhu97]_), "TNC" (nonlinear
    constrained minimizer), "CG" (nonlinear unconstrained minimizer), "BFGS"
    (nonlinear unconstrained minimizer), "NCG" (Newton CG minimizer). It is
    strongly recommended to stay with the default.

    Example :
    ``{"Minimizer":"LBFGSB"}``

  .. include:: snippets/BoundsWithNone.rst

  .. include:: snippets/ConstrainedBy.rst

  .. include:: snippets/MaximumNumberOfSteps.rst

  .. include:: snippets/CostDecrementTolerance.rst

  .. include:: snippets/EstimationOf.rst

  .. include:: snippets/ProjectedGradientTolerance.rst

  .. include:: snippets/GradientNormTolerance.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

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

  .. include:: snippets/Analysis.rst

  .. include:: snippets/CostFunctionJ.rst

  .. include:: snippets/CostFunctionJb.rst

  .. include:: snippets/CostFunctionJo.rst

The conditional outputs of the algorithm are the following:

  .. include:: snippets/BMA.rst

  .. include:: snippets/CostFunctionJAtCurrentOptimum.rst

  .. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

  .. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

  .. include:: snippets/CurrentOptimum.rst

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/IndexOfOptimum.rst

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
