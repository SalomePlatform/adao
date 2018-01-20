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

.. index:: single: QuantileRegression
.. _section_ref_algorithm_QuantileRegression:

Calculation algorithm "*QuantileRegression*"
--------------------------------------------

Description
+++++++++++

This algorithm allows to estimate the conditional quantiles of the state
parameters distribution, expressed with a model of the observed variables. These
are then the quantiles on the observed variables which will allow to determine
the model parameters that satisfy to the quantiles conditions.

Optional and required commands
++++++++++++++++++++++++++++++

The general required commands, available in the editing user interface, are the
following:

  .. include:: snippets/Background.rst

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationOperator.rst

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`. Moreover, the parameters
of the command "*AlgorithmParameters*" allows to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_Algorithm_Parameters` for the good use of this
command.

The options of the algorithm are the following:

  .. include:: snippets/Quantile.rst

  .. include:: snippets/MaximumNumberOfSteps.rst

  .. include:: snippets/CostDecrementTolerance_6.rst

  .. include:: snippets/BoundsWithNone.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["BMA", "CostFunctionJ", "CostFunctionJb",
    "CostFunctionJo", "CurrentState", "OMA", "OMB", "Innovation",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum"].

    Example :
    ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

*Tips for this algorithm:*

    As the *"BackgroundError"* and *"ObservationError"* commands are required
    for ALL the calculation algorithms in the interface, you have to provide a
    value, even if these commands are not required for this algorithm, and will
    not be used. The simplest way is to give "1" as a STRING for both.

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

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/Innovation.rst

  .. include:: snippets/OMA.rst

  .. include:: snippets/OMB.rst

  .. include:: snippets/SimulatedObservationAtBackground.rst

  .. include:: snippets/SimulatedObservationAtCurrentState.rst

  .. include:: snippets/SimulatedObservationAtOptimum.rst

See also
++++++++

Bibliographical references:
  - [Buchinsky98]_
  - [Cade03]_
  - [Koenker00]_
  - [Koenker01]_
  - [WikipediaQR]_
