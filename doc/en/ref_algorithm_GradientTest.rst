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

.. index:: single: GradientTest
.. _section_ref_algorithm_GradientTest:

Checking algorithm "*GradientTest*"
-----------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm allows to check the quality of the adjoint operator, by
calculating a residue with known theoretical properties. Different residue
formula are available.

In any cases, one take :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` and
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0` with :math:`\alpha_0` a user scaling
of the initial perturbation, with default to 1. :math:`F` is the calculation
code.

"Taylor" residue
****************

One observe the residue coming from the Taylor development of the :math:`F`
function, normalized by the value at the nominal point:

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{|| F(\mathbf{x}) ||}

If the residue is decreasing and the decrease change in :math:`\alpha^2` with
respect to :math:`\alpha`, it signifies that the gradient is well calculated
until the stopping precision of the quadratic decrease, and that :math:`F` is
not linear.

If the residue is decreasing and the decrease change in :math:`\alpha` with
respect to :math:`\alpha`, until a certain level after which the residue remains
small and constant, it signifies that the :math:`F` is linear and that the
residue is decreasing due to the error coming from :math:`\nabla_xF` term
calculation.

"TaylorOnNorm" residue
**********************

One observe the residue coming from the Taylor development of the :math:`F`
function, with respect to the :math:`\alpha` parameter to the square:

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{\alpha^2}

This is a residue essentially similar to the classical Taylor criterion
previously described, but its behavior can differ depending on the numerical
properties of the calculation.

If the residue is constant until a certain level after which the residue will
growth, it signifies that the gradient is well calculated until this stopping
precision, and that :math:`F` is not linear.

If the residue is systematically growing from a very small value with respect to
:math:`||F(\mathbf{x})||`, it signifies that :math:`F` is (quasi-)linear and
that the gradient calculation is correct until the precision for which the
residue reaches the numerical order of :math:`||F(\mathbf{x})||`.

"Norm" residue
**************

One observe the residue based on the gradient approximation:

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) ||}{\alpha}

which has to remain stable until the calculation precision is reached.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/AmplitudeOfInitialDirection.rst

.. include:: snippets/EpsilonMinimumExponent.rst

.. include:: snippets/InitialDirection.rst

.. include:: snippets/SetSeed.rst

ResiduFormula
  .. index:: single: ResiduFormula

  This key indicates the residue formula that has to be used for the test. The
  default choice is "Taylor", and the possible ones are "Taylor" (normalized
  residue of the Taylor development of the operator, which has to decrease
  with the square power of the perturbation), "TaylorOnNorm" (residue of the
  Taylor development of the operator with respect to the perturbation to the
  square, which has to remain constant) and "Norm" (residue obtained by taking
  the norm of the Taylor development at zero order approximation, which
  approximate the gradient, and which has to remain constant).

  Example :
  ``{"ResiduFormula":"Taylor"}``

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  This list indicates the names of the supplementary variables that can be
  available at the end of the algorithm. It involves potentially costly
  calculations or memory consumptions. The default is a void list, none of
  these variables being calculated and stored by default. The possible names
  are in the following list: [
  "CurrentState",
  "Residu",
  "SimulatedObservationAtCurrentState",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Residu.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LinearityTest`
- :ref:`section_ref_algorithm_TangentTest`
- :ref:`section_ref_algorithm_AdjointTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`
