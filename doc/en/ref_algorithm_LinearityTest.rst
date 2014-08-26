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

.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
.. index:: single: ResiduFormula
.. index:: single: SetSeed

The general required commands, available in the editing user interface, are the
following:

  CheckingPoint
    *Required command*. This indicates the vector used as the state around which
    to perform the required check, noted :math:`\mathbf{x}` and similar to the
    background :math:`\mathbf{x}^b`. It is defined as a "*Vector*" type object.

  ObservationOperator
    *Required command*. This indicates the observation operator, previously
    noted :math:`H`, which transforms the input parameters :math:`\mathbf{x}` to
    results :math:`\mathbf{y}` to be compared to observations
    :math:`\mathbf{y}^o`. Its value is defined as a "*Function*" type object or
    a "*Matrix*" type one. In the case of "*Function*" type, different
    functional forms can be used, as described in the section
    :ref:`section_ref_operator_requirements`. If there is some control
    :math:`U` included in the observation, the operator has to be applied to a
    pair :math:`(X,U)`.

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`. In particular, the
optional command "*AlgorithmParameters*" allows to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_AlgorithmParameters` for the good use of this command.

The options of the algorithm are the following:

  AmplitudeOfInitialDirection
    This key indicates the scaling of the initial perturbation build as a vector
    used for the directional derivative around the nominal checking point. The
    default is 1, that means no scaling.

    Example : ``{"AmplitudeOfInitialDirection":0.5}``

  EpsilonMinimumExponent
    This key indicates the minimal exponent value of the power of 10 coefficient
    to be used to decrease the increment multiplier. The default is -8, and it
    has to be between 0 and -20. For example, its default value leads to
    calculate the residue of the scalar product formula with a fixed increment
    multiplied from 1.e0 to 1.e-8.

    Example : ``{"EpsilonMinimumExponent":-12}``

  InitialDirection
    This key indicates the vector direction used for the directional derivative
    around the nominal checking point. It has to be a vector. If not specified,
    this direction defaults to a random perturbation around zero of the same
    vector size than the checking point.

    Example : ``{"InitialDirection":[0.1,0.1,100.,3}``

  ResiduFormula
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

    Example : ``{"ResiduFormula":"CenteredDL"}``

  SetSeed
    This key allow to give an integer in order to fix the seed of the random
    generator used to generate the ensemble. A convenient value is for example
    1000. By default, the seed is left uninitialized, and so use the default
    initialization from the computer.

    Example : ``{"SetSeed":1000}``

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_FunctionTest`
