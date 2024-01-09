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

.. index:: single: InterpolationByReducedModelTask
.. index:: single: Measurements interpolation
.. index:: single: Field reconstruction
.. index:: single: Snapshots (Ensemble)
.. index:: single: Reduced Order Model
.. index:: single: ROM
.. _section_ref_algorithm_InterpolationByReducedModelTask:

Task algorithm "*InterpolationByReducedModelTask*"
--------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo99.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm enables highly efficient interpolation of physical measurements
using a reduced representation of the model for that physics. The output, for
each set of measurements supplied at the required positions, is a complete
field :math:`\mathbf{y}` by interpolation. Put another way, it's a physical
field reconstruction using measurements and a reduced numerical model.

To interpolate these measurements, a method of Empirical Interpolation Method
(EIM [Barrault04]_) type is used, which uses a reduced model of type Reduced
Order Model (ROM) issued from EIM or DEIM decomposition, with or without
measurement positioning constraints.

To use this algorithm, you need the optimally positioned measurements and the
associated reduced basis for model representation. This can be achieved as
described below, by means of a preliminary analysis using a MOP, which provides
positions and base. Once the base has been constructed and the positions
determined, it is possible to perform as many interpolations as there are sets
of measurements at the required positions, without having to repeat the prior
analysis.

  .. _irm_determination:
  .. image:: images/irm_determination.png
    :align: center
    :width: 95%
  .. centered::
    **General scheme for using the algorithm**

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Observation.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Task.rst

.. include:: snippets/ObservationsAlreadyRestrictedOnOptimalLocations.rst

.. include:: snippets/OptimalLocations.rst

.. include:: snippets/ReducedBasis.rst

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
  "Analysis",
  "ReducedCoordinates",
  ].

  Example :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/ReducedCoordinates.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_InterpolationByReducedModelTask_examples:

.. include:: snippets/Header2Algo09.rst

.. --------- ..
.. include:: scripts/simple_InterpolationByReducedModelTask1.rst

.. literalinclude:: scripts/simple_InterpolationByReducedModelTask1.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_InterpolationByReducedModelTask1.res
    :language: none

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Barrault04]_
- [Quarteroni16]_
