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

.. index:: single: DerivativeFreeOptimization
.. _section_ref_algorithm_DerivativeFreeOptimization:

Calculation algorithm "*DerivativeFreeOptimization*"
----------------------------------------------------

.. warning::

  in its present version, this algorithm is experimental, and so changes can be
  required in forthcoming versions.

Description
+++++++++++

This algorithm realizes an estimation of the state of a system by minimization
of a cost function :math:`J` without gradient. It is a method that does not use
the derivatives of the cost function. It fall, for example, in the same category
than the :ref:`section_ref_algorithm_ParticleSwarmOptimization`.

This is an optimization method allowing for global minimum search of a general
error function :math:`J` of type :math:`L^1`, :math:`L^2` or :math:`L^{\infty}`,
with or without weights. The default error function is the augmented weighted
least squares function, classically used in data assimilation.

Optional and required commands
++++++++++++++++++++++++++++++

The general required commands, available in the editing user interface, are the
following:

  .. include:: snippets/Background.rst

  .. include:: snippets/BackgroundError.rst

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

  .. include:: snippets/Minimizer_DFO.rst

  .. include:: snippets/BoundsWithNone.rst

  .. include:: snippets/MaximumNumberOfSteps.rst

  .. include:: snippets/MaximumNumberOfFunctionEvaluations.rst

  .. include:: snippets/StateVariationTolerance.rst

  .. include:: snippets/CostDecrementTolerance.rst

  .. include:: snippets/QualityCriterion.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["BMA", "CostFunctionJ",
    "CostFunctionJb", "CostFunctionJo", "CostFunctionJAtCurrentOptimum",
    "CostFunctionJbAtCurrentOptimum", "CostFunctionJoAtCurrentOptimum",
    "CurrentOptimum", "CurrentState", "IndexOfOptimum",
    "InnovationAtCurrentState", "OMA", "OMB",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentOptimum",
    "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"].

    Example :
    ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

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

  .. include:: snippets/CurrentState.rst

The conditional outputs of the algorithm are the following:

  .. include:: snippets/CostFunctionJAtCurrentOptimum.rst

  .. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

  .. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

  .. include:: snippets/CurrentOptimum.rst

  .. include:: snippets/IndexOfOptimum.rst

  .. include:: snippets/InnovationAtCurrentState.rst

  .. include:: snippets/OMA.rst

  .. include:: snippets/OMB.rst

  .. include:: snippets/SimulatedObservationAtBackground.rst

  .. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

  .. include:: snippets/SimulatedObservationAtCurrentState.rst

  .. include:: snippets/SimulatedObservationAtOptimum.rst

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_ParticleSwarmOptimization`

Bibliographical references:
  - [Johnson08]_
  - [Nelder65]_
  - [Powell64]_
  - [Powell94]_
  - [Powell98]_
  - [Powell04]_
  - [Powell07]_
  - [Powell09]_
  - [Rowan90]_
