..
   Copyright (C) 2008-2024 EDF R&D

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

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm allows to check the linear quality of the operator, by
calculating a residue with known theoretical properties. Different residue
formula are available. The test is applicable to any operator, of evolution
:math:`\mathcal{D}` or observation :math:`\mathcal{H}`.

In any cases, with :math:`\mathbf{x}` the current verification point, one take
:math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` and
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0` with :math:`\alpha_0`a user scale
parameter, at 1 by default. :math:`F` is the calculation code (given here by
the user by using the observation operator command "*ObservationOperator*").

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

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeNeeded.rst

.. include:: snippets/FeaturePropParallelDerivativesOnly.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/AmplitudeOfInitialDirection.rst

.. include:: snippets/AmplitudeOfTangentPerturbation.rst

.. include:: snippets/EpsilonMinimumExponent.rst

.. include:: snippets/InitialDirection.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/ResiduFormula_LinearityTest.rst

.. include:: snippets/SetSeed.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *List of names*. This list indicates the names of the supplementary
  variables, that can be available during or at the end of the algorithm, if
  they are initially required by the user. Their availability involves,
  potentially, costly calculations or memory consumptions. The default is then
  a void list, none of these variables being calculated and stored by default
  (excepted the unconditional variables). The possible names are in the
  following list (the detailed description of each named variable is given in
  the following part of this specific algorithmic documentation, in the
  sub-section "*Information and variables available at the end of the
  algorithm*"): [
  "CurrentState",
  "Residu",
  "SimulatedObservationAtCurrentState",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Residu.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/Residu.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_LinearityTest_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
