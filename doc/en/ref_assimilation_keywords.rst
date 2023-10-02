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

.. _section_ref_assimilation_keywords:

List of commands and keywords for data assimilation or optimisation case
------------------------------------------------------------------------

We summarize here all the commands and keywords available to describe a
calculation case, by avoiding the particularities of each algorithm. It is
therefore a common inventory of commands.

The set of commands for an data assimilation or optimisation case is related to
the description of a calculation case, that is a *Data Assimilation* procedure
(chosen  in graphical user interface by the command "*ASSIMILATION_STUDY*"), a
*Reduction Method* procedure (chosen  in graphical user interface by the
command "*REDUCTION_STUDY*") or an *Optimization* procedure (chosen  in
graphical user interface by the command "*OPTIMIZATION_STUDY*").

All the possible terms, nested or not, are listed by alphabetical order. They
are not required for all the algorithms. The commands or keywords available are
the following

.. include:: snippets/AlgorithmParameters.rst

.. include:: snippets/ASSIMILATION_STUDY.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/ControlInput.rst

.. include:: snippets/Debug.rst

.. include:: snippets/EvolutionError.rst

.. include:: snippets/EvolutionModel.rst

.. include:: snippets/ExecuteInContainer.rst

.. include:: snippets/InputVariables.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. include:: snippets/Observers.rst

.. include:: snippets/OPTIMIZATION_STUDY.rst

.. include:: snippets/OutputVariables.rst

.. include:: snippets/REDUCTION_STUDY.rst

.. include:: snippets/StudyName.rst

.. include:: snippets/StudyRepertory.rst

.. include:: snippets/UserDataInit.rst

.. include:: snippets/UserPostAnalysis.rst
