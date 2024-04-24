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

.. index:: single: InputValuesTest
.. _section_ref_algorithm_InputValuesTest:

Checking algorithm "*InputValuesTest*"
--------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm verifies the content of the current input variables and the way
the data is interpreted or read during its acquisition, through the display of
size information and statistics on the inputs. It also allows to display the
whole content of the variables read in printed form for verification (*warning,
if a variable is large in size, this can be difficult*).

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/Observation.rst

*Tips for this algorithm:*

    Because *"ObservationOperator"*, in the graphical interface, is a required
    command for ALL checking algorithms, you have to provide a value for it,
    despite the fact that this command is not required for this test, and will
    not be used. The easiest way is to give "1" as a STRING,
    *"ObservationOperator"* having to be of type sparse *Matrix*.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/PrintAllValuesFor.rst

.. include:: snippets/ShowInformationOnlyFor.rst

.. include:: snippets/SetDebug.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_InputValuesTest_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_ControledFunctionTest`
- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_ParallelFunctionTest`
