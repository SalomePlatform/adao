..
   Copyright (C) 2008-2014 EDF R&D

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
.. index:: single: CheckingPoint
.. index:: single: BackgroundError
.. index:: single: Debug
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Observer
.. index:: single: Observers
.. index:: single: Observer Template
.. index:: single: Study_name
.. index:: single: Study_repertory
.. index:: single: UserDataInit

This set of commands is related to the description of a checking case, that is a
procedure to check required properties on information, used somewhere else by a
calculation case. The terms are ordered in alphabetical order, except the first,
which describes the choice between calculation or checking.

The different commands are the following:

  **CHECKING_STUDY**
    *Required command*. This is the general command describing the checking
    case. It hierarchically contains all the other commands.

  Algorithm
    *Required command*. This is a string to indicate the checking algorithm chosen.
    The choices are limited and available through the GUI. There exists for
    example "FunctionTest", "AdjointTest"... See below the list of algorithms
    and associated parameters, each described by a subsection.

  AlgorithmParameters
    *Optional command*. This command allows to add some optional parameters to
    control the data assimilation or optimization algorithm. Its value is
    defined as a "*Dict*" type object. See the section
    :ref:`section_ref_options_AlgorithmParameters` for for the correct use of
    this command.

  CheckingPoint
    *Required command*. This indicates the vector used as the state around which
    to perform the required check, noted :math:`\mathbf{x}` and similar to the
    background :math:`\mathbf{x}^b`. It is defined as a "*Vector*" type object.

  BackgroundError
    *Required command*. This indicates the background error covariance matrix,
    previously noted as :math:`\mathbf{B}`. Its value is defined as a "*Matrix*"
    type object, a "*ScalarSparseMatrix*" type object, or a
    "*DiagonalSparseMatrix*" type object.

  Debug
    *Optional command*. This define the level of trace and intermediary debug
    information. The choices are limited between 0 (for False) and 1 (for
    True).

  Observation
    *Required command*. This indicates the observation vector used for data
    assimilation or optimization, previously noted as :math:`\mathbf{y}^o`. It
    is defined as a "*Vector*" or a *VectorSerie* type object.

  ObservationError
    *Required command*. This indicates the observation error covariance matrix,
    previously noted as :math:`\mathbf{R}`. It is defined as a "*Matrix*" type
    object, a "*ScalarSparseMatrix*" type object, or a "*DiagonalSparseMatrix*"
    type object.

  ObservationOperator
    *Required command*. This indicates the observation operator, previously
    noted :math:`H`, which transforms the input parameters :math:`\mathbf{x}` to
    results :math:`\mathbf{y}` to be compared to observations
    :math:`\mathbf{y}^o`. Its value is defined as a "*Function*" type object or
    a "*Matrix*" type one. In the case of "*Function*" type, different
    functional forms can be used, as described in the section
    :ref:`section_ref_operator_requirements`. If there is some control :math:`U`
    included in the observation, the operator has to be applied to a pair
    :math:`(X,U)`.

  Observers
    *Optional command*. This command allows to set internal observers, that are
    functions linked with a particular variable, which will be executed each
    time this variable is modified. It is a convenient way to monitor variables
    of interest during the data assimilation or optimization process, by
    printing or plotting it, etc. Common templates are provided to help the user
    to start or to quickly make his case.

  Study_name
    *Required command*. This is an open string to describe the ADAO study by a
    name or a sentence.

  Study_repertory
    *Optional command*. If available, this directory is used as base name for
    calculation, and used to find all the script files, given by name without
    path, that can be used to define some other commands by scripts.

  UserDataInit
    *Optional command*. This commands allows to initialize some parameters or
    data automatically before algorithm input processing. It indicates a script
    file name to be executed before entering in initialization phase of chosen
    variables.
