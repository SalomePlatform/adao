..
   Copyright (C) 2008-2020 EDF R&D

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

.. index:: single: QuantileRegression
.. _section_ref_algorithm_QuantileRegression:

Calculation algorithm "*QuantileRegression*"
--------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm allows to estimate the conditional quantiles of the state
parameters distribution, expressed with a model of the observed variables. These
are then the quantiles on the observed variables which will allow to determine
the model parameters that satisfy to the quantiles conditions.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. include:: snippets/Quantile.rst

.. include:: snippets/MaximumNumberOfSteps.rst

.. include:: snippets/CostDecrementTolerance_6.rst

.. include:: snippets/BoundsWithNone.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *List of names*. This list indicates the names of the supplementary variables
  that can be available during or at the end of the algorithm, if they are
  initially required by the user. It involves potentially costly calculations
  or memory consumptions. The default is a void list, none of these variables
  being calculated and stored by default excepted the unconditionnal variables.
  The possible names are in the following list: [
  "Analysis",
  "BMA",
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CurrentIterationNumber",
  "CurrentState",
  "Innovation",
  "OMA",
  "OMB",
  "SimulatedObservationAtBackground",
  "SimulatedObservationAtCurrentState",
  "SimulatedObservationAtOptimum",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

*Tips for this algorithm:*

    As the *"BackgroundError"* and *"ObservationError"* commands are required
    for ALL the calculation algorithms in the interface, you have to provide a
    value, even if these commands are not required for this algorithm, and will
    not be used. The simplest way is to give "1" as a STRING for both.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/BMA.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CurrentIterationNumber.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/OMA.rst

.. include:: snippets/OMB.rst

.. include:: snippets/SimulatedObservationAtBackground.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtOptimum.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Buchinsky98]_
- [Cade03]_
- [Koenker00]_
- [Koenker01]_
- [WikipediaQR]_
