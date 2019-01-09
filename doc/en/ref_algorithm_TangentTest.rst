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

.. index:: single: TangentTest
.. _section_ref_algorithm_TangentTest:

Checking algorithm "*TangentTest*"
----------------------------------

Description
+++++++++++

This algorithm allows to check the quality of the tangent operator, by
calculating a residue with known theoretical properties.

One can observe the following residue, which is the comparison of increments
using the tangent linear operator:

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) ||}{|| \alpha * TangentF_x * \mathbf{dx} ||}

which has to remain stable in :math:`1+O(\alpha)` until the calculation
precision is reached.

When :math:`|R-1|/\alpha` is less or equal to a stable value when :math:`\alpha`
is varying, the tangent is valid, until the calculation precision is reached.

If :math:`|R-1|/\alpha` is really small, the calculation code :math:`F` is
almost linear or quasi-linear (which can be verified by the
:ref:`section_ref_algorithm_LinearityTest`), and the tangent is valid until the
calculation precision is reached.

One take :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` and
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` is the calculation code.

Optional and required commands
++++++++++++++++++++++++++++++

The general required commands, available in the editing user interface, are the
following:

  .. include:: snippets/CheckingPoint.rst

  .. include:: snippets/ObservationOperator.rst

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`. Moreover, the parameters
of the command "*AlgorithmParameters*" allow to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_Algorithm_Parameters` for the good use of this
command.

The options of the algorithm are the following:

  .. include:: snippets/AmplitudeOfInitialDirection.rst

  .. include:: snippets/EpsilonMinimumExponent.rst

  .. include:: snippets/InitialDirection.rst

  .. include:: snippets/SetSeed.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["CurrentState", "Residu",
    "SimulatedObservationAtCurrentState"].

    Example :
    ``{"StoreSupplementaryCalculations":["CurrentState"]}``

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

  .. include:: snippets/Residu.rst

The conditional outputs of the algorithm are the following:

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/SimulatedObservationAtCurrentState.rst

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_FunctionTest`
  - :ref:`section_ref_algorithm_LinearityTest`
  - :ref:`section_ref_algorithm_AdjointTest`
  - :ref:`section_ref_algorithm_GradientTest`
