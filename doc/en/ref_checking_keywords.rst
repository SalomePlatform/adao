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

.. _section_ref_checking_keywords:

List of commands and keywords for an ADAO checking case
-------------------------------------------------------

We summarize here all the commands and keywords available to describe a
checking case, by avoiding the particularities of each algorithm. It is
therefore a common inventory of commands.

A special term allow to choose explicitly a checking. In the graphical user
interface, this choice is done by the command "*CHECKING_STUDY*".

All the possible terms, nested or not, are listed by alphabetical order. They
are not required for all the algorithms. The commands or keywords available are
the following

.. include:: snippets/AlgorithmParameters.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/CHECKING_STUDY.rst

.. include:: snippets/Debug.rst

.. include:: snippets/ExecuteInContainer.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. include:: snippets/Observers.rst

.. include:: snippets/StudyName.rst

.. include:: snippets/StudyRepertory.rst

.. include:: snippets/UserDataInit.rst
