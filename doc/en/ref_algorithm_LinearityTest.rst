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

.. index:: single: LinearityTest
.. _section_ref_algorithm_LinearityTest:

Checking algorithm "*LinearityTest*"
------------------------------------

Description
+++++++++++

This algorithm allows to check the linear quality of the operator, by
calculating a residue with known theoretical properties. Different residue
formula are available.

In any cases, one take :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` and
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` is the calculation code.

"CenteredDL" residue
********************

One observe the following residue, coming from the centered difference of the
:math:`F` values at nominal point and at perturbed points, normalized by the
value at the nominal point:

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) + F(\mathbf{x}-\alpha*\mathbf{dx}) - 2*F(\mathbf{x}) ||}{|| F(\mathbf{x}) ||}

If it stays constantly really small with respect to 1, the linearity hypothesis
of :math:`F` is verified.

If the residue is varying, or if it is of order 1 or more, and it is small only
at a certain order of increment, the linearity hypothesis of :math:`F` is not
verified.

If the residue is decreasing and the decrease change in :math:`\alpha^2` with
respect to :math:`\alpha`, it signifies that the gradient is correctly
calculated until the stopping level of the quadratic decrease.

"Taylor" residue
****************

One observe the residue coming from the Taylor development of the :math:`F`
function, normalized by the value at the nominal point:

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{|| F(\mathbf{x}) ||}

If it stay constantly really small with respect to 1, the linearity hypothesis
of :math:`F` is verified.

If the residue is varying, or if it is of order 1 or more, and it is small only
at a certain order of increment, the linearity hypothesis of :math:`F` is not
verified.

If the residue is decreasing and the decrease change in :math:`\alpha^2` with
respect to :math:`\alpha`, it signifies that the gradient is correctly
calculated until the stopping level of the quadratic decrease.

"NominalTaylor" residue
***********************

One observe the residue build from two approximations of order 1 of
:math:`F(\mathbf{x})`, normalized by the value at the nominal point:

.. math:: R(\alpha) = \max(|| F(\mathbf{x}+\alpha*\mathbf{dx}) - \alpha * F(\mathbf{dx}) || / || F(\mathbf{x}) ||,|| F(\mathbf{x}-\alpha*\mathbf{dx}) + \alpha * F(\mathbf{dx}) || / || F(\mathbf{x}) ||)

If the residue stays constant equal to 1 at less than 2 or 3 percents (that that
:math:`|R-1|` stays equal to 2 or 3 percents), the linearity hypothesis of
:math:`F` is verified.

If it is equal to 1 only on part of the variation domain of increment
:math:`\alpha`, it is on this sub-domain that the linearity hypothesis of
:math:`F` is verified.

"NominalTaylorRMS" residue
**************************

One observe the residue build from two approximations of order 1 of
:math:`F(\mathbf{x})`, normalized by the value at the nominal point, on which
one estimate the quadratic root mean square (RMS) with the value at the nominal
point:

.. math:: R(\alpha) = \max(RMS( F(\mathbf{x}), F(\mathbf{x}+\alpha*\mathbf{dx}) - \alpha * F(\mathbf{dx}) ) / || F(\mathbf{x}) ||,RMS( F(\mathbf{x}), F(\mathbf{x}-\alpha*\mathbf{dx}) + \alpha * F(\mathbf{dx}) ) / || F(\mathbf{x}) ||)

If it stay constantly equal to 0 at less than 1 or 2 percents, the linearity
hypothesis of :math:`F` is verified.

If it is equal to 0 only on part of the variation domain of increment
:math:`\alpha`, it is on this sub-domain that the linearity hypothesis of
:math:`F` is verified.

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

  ResiduFormula
    .. index:: single: ResiduFormula

    This key indicates the residue formula that has to be used for the test. The
    default choice is "CenteredDL", and the possible ones are "CenteredDL"
    (residue of the difference between the function at nominal point and the
    values with positive and negative increments, which has to stay very small),
    "Taylor" (residue of the Taylor development of the operator normalized by
    the nominal value, which has to stay very small), "NominalTaylor" (residue
    of the order 1 approximations of the operator, normalized to the nominal
    point, which has to stay close to 1), and "NominalTaylorRMS" (residue of the
    order 1 approximations of the operator, normalized by RMS to the nominal
    point, which has to stay close to 0).

    Example :
    ``{"ResiduFormula":"CenteredDL"}``

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
