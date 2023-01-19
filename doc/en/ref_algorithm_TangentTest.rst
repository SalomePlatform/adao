..
   Copyright (C) 2008-2023 EDF R&D

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

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

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

.. include:: snippets/SetSeed.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *List of names*. This list indicates the names of the supplementary
  variables, that can be available during or at the end of the algorithm, if
  they are initially required by the user. Their avalability involves,
  potentially, costly calculations or memory consumptions. The default is then
  a void list, none of these variables being calculated and stored by default
  (excepted the unconditionnal variables). The possible names are in the
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
.. _section_ref_algorithm_TangentTest_examples:
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LinearityTest`
- :ref:`section_ref_algorithm_AdjointTest`
- :ref:`section_ref_algorithm_GradientTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`
