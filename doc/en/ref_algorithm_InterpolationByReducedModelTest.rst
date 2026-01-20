..
   Copyright (C) 2008-2026 EDF R&D

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

.. index:: single: InterpolationByReducedModelTest
.. _section_ref_algorithm_InterpolationByReducedModelTest:

Checking algorithm "*InterpolationByReducedModelTest*"
------------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm provides a simple way of analyzing the quality of the empirical
interpolation obtained by a reduced basis for complete states, using
measurements at precise points.

The results displayed by default are simple statistics related to the
normalized errors between the interpolation with a reduced basis and the
complete states we seek to represent on the reduced basis. The test requires a
reduced basis and a set of optimal measurement positions, and uses
pseudo-measurements from each complete state ("*snapshot*") included in the
given test set.

Please note: to be consistent, this test must use the same mathematical norm as
that used to construct the reduced basis. As the norm is chosen by the user
when defining the test, the norm used to construct the reduced basis must be
verified.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/EnsembleOfSnapshots.rst

.. include:: snippets/MeasurementLocations.rst

.. include:: snippets/ReducedBasis.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/ErrorNorm.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/ShowElementarySummary.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/NoUnconditionalOutput.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/NoConditionalOutput.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_InterpolationByReducedModelTest_examples:

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_InterpolationByReducedModelTask`
- :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`
- :ref:`section_ref_algorithm_ReducedModelingTest`
