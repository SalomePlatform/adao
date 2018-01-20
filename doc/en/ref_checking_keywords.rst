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

.. index:: single: CHECKING_STUDY
.. _section_ref_checking_keywords:

List of commands and keywords for an ADAO checking case
-------------------------------------------------------

.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: Debug
.. index:: single: Observer
.. index:: single: Observers
.. index:: single: Observer Template
.. index:: single: StudyName
.. index:: single: StudyRepertory
.. index:: single: UserDataInit

This set of commands is related to the description of a checking case, that is a
procedure to check required properties on information, used somewhere else by a
calculation case. The terms are ordered in alphabetical order, except the first,
which describes the choice between calculation or checking.

The different commands are the following:

  **CHECKING_STUDY**
    *Required command*. This is the general command describing the checking
    case. It hierarchically contains all the other commands.

  AlgorithmParameters
    *Required command*. This indicates the checking algorithm chosen by the
    keyword "*Algorithm*", and its potential optional parameters. The algorithm
    choices are available through the GUI. There exists for example
    "FunctionTest", "GradientTest"... Each algorithm is defined, below, by a
    specific subsection. Optionaly, the command allows also to add some
    parameters to control the algorithm. Their values are defined either
    explicitly or in a "*Dict*" type object. See the
    :ref:`section_ref_options_Algorithm_Parameters` for the detailed use of this
    command part.

  .. include:: snippets/CheckingPoint.rst

  .. include:: snippets/BackgroundError.rst

  Debug
    *Optional command*. This define the level of trace and intermediary debug
    information. The choices are limited between 0 (for False) and 1 (for
    True).

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationError.rst

  .. include:: snippets/ObservationOperator.rst

  Observers
    *Optional command*. This command allows to set internal observers, that are
    functions linked with a particular variable, which will be executed each
    time this variable is modified. It is a convenient way to monitor variables
    of interest during the data assimilation or optimization process, by
    printing or plotting it, etc. Common templates are provided to help the user
    to start or to quickly make his case.

  StudyName
    *Required command*. This is an open string to describe the ADAO study by a
    name or a sentence.

  StudyRepertory
    *Optional command*. If available, this directory is used as base name for
    calculation, and used to find all the script files, given by name without
    path, that can be used to define some other commands by scripts.

  UserDataInit
    *Optional command*. This commands allows to initialize some parameters or
    data automatically before algorithm input processing. It indicates a script
    file name to be executed before entering in initialization phase of chosen
    variables.
