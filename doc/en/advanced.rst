..
   Copyright (C) 2008-2015 EDF R&D

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

.. _section_advanced:

================================================================================
**[DocU]** Advanced usage of the ADAO module
================================================================================

This section presents advanced methods to use the ADAO module, how to get more
information during calculation, or how to use it without the graphical user
interface (GUI). It requires to know how to find files or commands included
inside the whole SALOME installation. All the names to be replaced by user are
indicated by the syntax ``<...>``.

Converting and executing an ADAO command file (JDC) using a shell script
------------------------------------------------------------------------

It is possible to convert and execute an ADAO command file (JDC, or ".comm/.py"
files pair, which resides in ``<ADAO JDC file directory>``) automatically by
using a template shell script containing all the required steps. The user has to
know where are the main SALOME launching files, and in particular the
``salome`` one. The directory in which this script resides is symbolically
named ``<SALOME main installation dir>`` and has to be replaced by the good one
in the shell file template.

When an ADAO command file is build by the ADAO graphical editor and saved, if
it is named for example "AdaoStudy1.comm", then a companion file named
"AdaoStudy1.py" is automatically created in the same directory. It is named
``<ADAO Python file>`` in the template, and it is converted to YACS as an
``<ADAO YACS xml scheme>``. After that, it can be executed in console mode using
the standard YACS console command (see YACS documentation for more information).

In the example, we choose to start and stop the SALOME application server in the
same script, which is not necessary, but useful to avoid stalling SALOME
sessions. We choose also to remove the ``<ADAO YACS xml scheme>`` file because
it is a generated one. The user of this script only need to replace the text
between these symbols ``<...>``.

The template of the shell script is the following::

    #!/bin/bash
    export USERDIR=<ADAO JDC file directory>
    export SALOMEDIR=<SALOME main installation directory>
    $SALOMEDIR/salome start -k -t
    $SALOMEDIR/salome shell python \
        $SALOMEDIR/bin/salome/AdaoYacsSchemaCreator.py \
        $USERDIR/<ADAO Python file> $USERDIR/<ADAO YACS xml scheme>
    $SALOMEDIR/salome shell driver $USERDIR/<ADAO YACS xml scheme>
    $SALOMEDIR/salome shell killSalome.py
    rm -f $USERDIR/<ADAO YACS xml scheme>

Standard output and errors come on console.

Running an ADAO calculation scheme in YACS using a TUI user mode
----------------------------------------------------------------

This section describes how to execute in TUI (Text User Interface) mode a YACS
calculation scheme, obtained using the ADAO "Export to YACS" function. It uses
the standard YACS TUI mode, which is briefly recalled here (see YACS
documentation for more information) through a simple example. As described in
documentation, a XML scheme can be loaded in a Python. We give here a whole
sequence of command lines to test the validity of the scheme before executing
it, adding some initial supplementary ones to explicitly load the types catalog
to avoid weird difficulties::

    import pilot
    import SALOMERuntime
    import loader
    SALOMERuntime.RuntimeSALOME_setRuntime()

    r = pilot.getRuntime()
    xmlLoader = loader.YACSLoader()
    xmlLoader.registerProcCataLoader()
    try:
     catalogAd = r.loadCatalog("proc", "<ADAO YACS xml scheme>")
    except:
      pass
    r.addCatalog(catalogAd)

    try:
        p = xmlLoader.load("<ADAO YACS xml scheme>")
    except IOError,ex:
        print "IO exception:",ex

    logger = p.getLogger("parser")
    if not logger.isEmpty():
        print "The imported file has errors :"
        print logger.getStr()

    if not p.isValid():
        print "The schema is not valid and can not be executed"
        print p.getErrorReport()

    info=pilot.LinkInfo(pilot.LinkInfo.ALL_DONT_STOP)
    p.checkConsistency(info)
    if info.areWarningsOrErrors():
        print "The schema is not consistent and can not be executed"
        print info.getGlobalRepr()

    e = pilot.ExecutorSwig()
    e.RunW(p)
    if p.getEffectiveState() != pilot.DONE:
        print p.getErrorReport()

This method allows for example to edit the YACS XML scheme in TUI, or to gather
results for further use.

.. _section_advanced_observer:

Getting information on special variables during the ADAO calculation in YACS
-----------------------------------------------------------------------------

.. index:: single: Observer
.. index:: single: Observers
.. index:: single: Observer Template

Some special internal optimization variables, used during calculations, can be
monitored during the ADAO calculation in YACS. These variables can be printed,
plotted, saved, etc. This can be done using "*observers*", that are scripts,
each associated with one variable. In order to use this feature, the user has to
build scripts using as standard inputs (e.g. available in the namespace) the
variables ``var`` and ``info``. The variable ``var`` is to be used in the same
way as for the final ADD object, that is as a list/tuple object.

Some templates are available when editing the ADAO case in graphical editor.
These simple scripts can be customized by the user, either at the EFICAS edition
stage, or at the YACS edition stage, to improve the tuning of the ADAO
calculation in YACS.

As an example, here is one very simple script (similar to the "*ValuePrinter*"
template) used to print the value of one monitored variable::

    print "    --->",info," Value =",var[-1]

Stored in a Python file, this script can be associated to each variable
available in the "*SELECTION*" keyword of the "*Observers*" command:
"*Analysis*", "*CurrentState*", "*CostFunction*"... The current value of the
variable will be printed at each step of the optimization or assimilation
algorithm. The observers can embed plotting capabilities, storage, complex
printing, statistical treatment, etc.

Getting more information when running a calculation
---------------------------------------------------

.. index:: single: Logging

When running a calculation, useful data and messages are logged. There are two
ways to obtain theses information.

The first one, and the preferred way, is to use the built-in variable "*Debug*"
available in every ADAO case. It is available through the edition GUI of the
module. Setting it to "*1*" will send messages in the log window of the YACS
scheme execution.

The second one consist in using the "*logging*" native module of Python (see the
Python documentation http://docs.python.org/library/logging.html for more
information on this module). Everywhere in the YACS scheme, mainly through the
scripts entries, the user can set the logging level in accordance to the needs
of detailed information. The different logging levels are: "*DEBUG*", "*INFO*",
"*WARNING*", "*ERROR*", "*CRITICAL*". All the information flagged with a
certain level will be printed for whatever activated level above this particular
one (included). The easiest way is to change the log level by using the
following Python lines::

    import logging
    logging.getLogger().setLevel(logging.DEBUG)

The standard logging module default level is "*WARNING*", the default level in
the ADAO module is "*INFO*". 

It is also recommended to include some logging or debug mechanisms in the
simulation code, and use them in conjunction with the two previous methods. But
be careful not to store too big variables because it cost time, whatever logging
level is chosen (that is, even if these variables are not printed).

.. _subsection_ref_parallel_df:

Accelerating numerical derivatives calculations by using a parallel mode
------------------------------------------------------------------------

.. index:: single: EnableMultiProcessing

When setting an operator, as described in
:ref:`section_ref_operator_requirements`, the user can choose a functional form
"*ScriptWithOneFunction*". This form explicitly leads to approximate the tangent
and adjoint operators by a finite differences calculation. It requires several
calls to the direct operator (user defined function), at least as many times as
the dimension of the state vector. This are these calls that can potentially be
executed in parallel.

Under some conditions, it is then possible to accelerate the numerical
derivatives calculations by using a parallel mode for the finite differences
approximation. When setting up an ADAO case, it is done by adding the optional
sub-command "*EnableMultiProcessing*", set to "1", for the
"*SCRIPTWITHONEFUNCTION*" command in the operator definition. The parallel mode
will only use local resources (both multi-cores or multi-processors) of the
computer on which SALOME is running, requiring as many resources as available.
By default, this parallel mode is disabled ("*EnableMultiProcessing=0*").

The main conditions to perform parallel calculations come from the user defined
function, that represents the direct operator. This function has at least to be
"thread safe" to be executed in Python parallel environment (notions out of
scope of this paragraph). It is not obvious to give general rules, so it's
recommended, for the user who enable this internal parallelism, to carefully
verify his function and the obtained results.

From a user point of view, some conditions, that have to be met to set up
parallel calculations for tangent and the adjoint operators approximations, are
the following ones:

#. The dimension of the state vector is more than 2 or 3.
#. Unitary calculation of user defined direct function "last for long time", that is, more than few minutes.
#. The user defined direct function doesn't already use parallelism (or parallel execution is disabled in the user calculation).
#. The user defined direct function avoids read/write access to common resources, mainly stored data, output files or memory capacities.
#. The observers added by the user avoid read/write access to common resources, such as files or memory.

If these conditions are satisfied, the user can choose to enable the internal
parallelism for the numerical derivative calculations. Despite the simplicity of
activating, by setting one variable only, the user is urged to verify the
results of its calculations. One must at least doing them one time with
parallelism enabled, and an another time with parallelism disabled, to compare
the results. If it does fail somewhere, you have to know that this parallel
scheme is working for complex codes, like *Code_Aster* in *SalomeMeca*
[SalomeMeca]_ for example. So, if it does not work in your case, check your
operator function before and during enabling parallelism...

.. warning::

  in case of doubt, it is recommended NOT TO ACTIVATE this parallelism.

Switching from a version of ADAO to a newer one
-----------------------------------------------

.. index:: single: Version

The ADAO module and its ".comm" case files are identified by versions, with
"Major", "Minor" and "Revision" characteristics. A particular version is
numbered as "Major.Minor.Revision", with strong link with the numbering of the
SALOME platform.

Each version "Major.Minor.Revision" of the ADAO module can read ADAO case files
of the previous minor version "Major.Minor-1.*". In general, it can also read
ADAO case files of all the previous minor versions for one major branch, but it
is not guaranteed for all the commands or keywords. In general also, an ADAO
case file for one version can not be read by a previous minor or major version
of the ADAO module.

Switching from 7.5 to 7.6
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name. This procedure proceed automatically to the required
modifications of the storage tree of the ADAO case file.

Switching from 7.4 to 7.5
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

Switching from 7.3 to 7.4
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

Switching from 7.2 to 7.3
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

Switching from 6.6 to 7.2
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

There is one incompatibility introduced for the post-processing or observer
script files. The old syntax to call a result object, such as the "*Analysis*"
one (in a script provided through the "*UserPostAnalysis*" keyword), was for
example::

    Analysis = ADD.get("Analysis").valueserie(-1)
    Analysis = ADD.get("Analysis").valueserie()

The new syntax is entirely similar to the (classical) one of a list or tuple
object::

    Analysis = ADD.get("Analysis")[-1]
    Analysis = ADD.get("Analysis")[:]

The post-processing scripts has to be modified.

Switching from 6.5 to 6.6
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case file. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

There is one incompatibility introduced for the naming of operators used to for
the observation operator. The new mandatory names are "*DirectOperator*",
"*TangentOperator*" and "*AdjointOperator*", as described in the last subsection
of the chapter :ref:`section_reference`. The operator scripts has to be
modified.

Switching from 6.4 to 6.5
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case file or the accompanying
scripts. The upgrade procedure is to read the old ADAO case file with the new
SALOME/ADAO module, and save it with a new name.

Switching from 6.3 to 6.4
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case file or the accompanying
scripts. The upgrade procedure is to read the old ADAO case file with the new
SALOME/ADAO module, and save it with a new name.
