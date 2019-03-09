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

.. index:: single: SamplingTest
.. _section_ref_algorithm_SamplingTest:

Checking algorithm "*SamplingTest*"
-----------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

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

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/QualityCriterion.rst

.. include:: snippets/SampleAsExplicitHyperCube.rst

.. include:: snippets/SampleAsIndependantRandomVariables.rst

.. include:: snippets/SampleAsMinMaxStepHyperCube.rst

.. include:: snippets/SampleAsnUplet.rst

.. include:: snippets/SetDebug.rst

.. include:: snippets/SetSeed.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  This list indicates the names of the supplementary variables that can be
  available at the end of the algorithm. It involves potentially costly
  calculations or memory consumptions. The default is a void list, none of
  these variables being calculated and stored by default. The possible names
  are in the following list: [
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CurrentState",
  "InnovationAtCurrentState",
  "SimulatedObservationAtCurrentState",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CostFunctionJ", "SimulatedObservationAtCurrentState"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo08.rst

- OPENTURNS, see the *User guide of OPENTURNS module* in the main "*Help*" menu of SALOME platform
