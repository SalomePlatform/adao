..
   Copyright (C) 2008-2017 EDF R&D

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

.. index:: single: ASSIMILATION_STUDY
.. _section_ref_assimilation_keywords:

List of commands and keywords for an ADAO calculation case
----------------------------------------------------------

.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: ControlInput
.. index:: single: Debug
.. index:: single: EvolutionError
.. index:: single: EvolutionModel
.. index:: single: InputVariables
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Observer
.. index:: single: Observers
.. index:: single: Observer Template
.. index:: single: OutputVariables
.. index:: single: StudyName
.. index:: single: StudyRepertory
.. index:: single: UserDataInit
.. index:: single: UserPostAnalysis
.. index:: single: UserPostAnalysis Template

This set of commands is related to the description of a calculation case,
that is a *Data Assimilation* procedure or an *Optimization* procedure. The
terms are ordered in alphabetical order, except the first, which describes
choice between calculation or checking.

The different commands are the following:

  **ASSIMILATION_STUDY**
    *Required command*. This is the general command describing the data
    assimilation or optimization case. It hierarchically contains all the other
    commands.

  AlgorithmParameters
    *Required command*. This indicates the data assimilation or optimization
    algorithm chosen by the keyword "*Algorithm*", and its potential optional
    parameters. The algorithm choices are available through the GUI. There
    exists for example "3DVAR", "Blue"... Each algorithm is defined, below, by a
    specific subsection. Optionally, the command allows also to add some
    parameters to control the algorithm. Their values are defined either
    explicitly or in a "*Dict*" type object. See the
    :ref:`section_ref_options_Algorithm_Parameters` for the detailed use of this
    command part.

  Background
    *Required command*. This indicates the background or initial vector used,
    previously noted as :math:`\mathbf{x}^b`. Its value is defined as a
    "*Vector*" type object.

  BackgroundError
    *Required command*. This indicates the background error covariance matrix,
    previously noted as :math:`\mathbf{B}`. Its value is defined as a "*Matrix*"
    type object, a "*ScalarSparseMatrix*" type object, or a
    "*DiagonalSparseMatrix*" type object.

  ControlInput
    *Optional command*. This indicates the control vector used to force the
    evolution model at each step, usually noted as :math:`\mathbf{U}`. Its value
    is defined as a "*Vector*" or a *VectorSerie* type object. When there is no
    control, it has to be a void string ''.

  Debug
    *Optional command*. This define the level of trace and intermediary debug
    information. The choices are limited between 0 (for False) and 1 (for
    True).

  EvolutionError
    *Optional command*. This indicates the evolution error covariance matrix,
    usually noted as :math:`\mathbf{Q}`. It is defined as a "*Matrix*" type
    object, a "*ScalarSparseMatrix*" type object, or a "*DiagonalSparseMatrix*"
    type object.

  EvolutionModel
    *Optional command*. This indicates the evolution model operator, usually
    noted :math:`M`, which describes an elementary step of evolution. Its value
    is defined as a "*Function*" type object or a "*Matrix*" type one. In the
    case of "*Function*" type, different functional forms can be used, as
    described in the section :ref:`section_ref_operator_requirements`. If there
    is some control :math:`U` included in the evolution model, the operator has
    to be applied to a pair :math:`(X,U)`.

  InputVariables
    *Optional command*. This command allows to indicates the name and size of
    physical variables that are bundled together in the state vector. This
    information is dedicated to data processed inside an algorithm.

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
    :ref:`section_ref_operator_requirements`. If there is some control
    :math:`U` included in the observation, the operator has to be applied to a
    pair :math:`(X,U)`.

  Observers
    *Optional command*. This command allows to set internal observers, that are
    functions linked with a particular variable, which will be executed each
    time this variable is modified. It is a convenient way to monitor variables
    of interest during the data assimilation or optimization process, by
    printing or plotting it, etc. Common templates are provided to help the user
    to start or to quickly make his case.

  OutputVariables
    *Optional command*. This command allows to indicates the name and size of
    physical variables that are bundled together in the output observation
    vector. This information is dedicated to data processed inside an algorithm.

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

  UserPostAnalysis
    *Optional command*. This commands allows to process some parameters or data
    automatically after data assimilation or optimization algorithm processing.
    Its value is defined as a script file or a string, allowing to put
    post-processing code directly inside the ADAO case. Common templates are
    provided to help the user to start or to quickly make his case.
