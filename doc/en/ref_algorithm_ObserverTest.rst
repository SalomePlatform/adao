..
   Copyright (C) 2008-2021 EDF R&D

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

.. index:: single: ObserverTest
.. _section_ref_algorithm_ObserverTest:

Checking algorithm "*ObserverTest*"
-----------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

This algorithm allows to verify an external function, given by the user, used as
an *observer*. This external function can be applied to every of the variables
that can be potentially observed. It is activated only on those who are
explicitly associated with the *observer* in the interface.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Observers.rst

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`.

*Tips for this algorithm:*

    Because *"CheckingPoint"* and *"ObservationOperator"* are required commands
    for ALL checking algorithms in the interface, you have to provide a value
    for them, despite the fact that these commands are not required for this
    test, and will not be used. The easiest way is to give "1" as a STRING for
    both, *"ObservationOperator"* having to be of type *Matrix*.
