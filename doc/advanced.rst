.. _section_advanced:

================================================================================
Advanced usage of the ADAO module
================================================================================

This section presents advanced methods to use the ADAO module, how to get more
information, or how to use it without the graphical user interface (GUI). It
requires to know how to find files or commands included inside the whole SALOME
installation. All the names to be replaced by user are indicated by the
following syntax ``<...>``.

Converting and executing an ADAO command file (JDC) using a shell script
------------------------------------------------------------------------

It is possible to convert and execute an ADAO command file (JDC, or ".comm"
file, which resides in ``<ADAO JDC file directory>``) automatically by using a
template script containing all the required steps. The user has to know where
are the main SALOME scripts, and in particular the ``runAppli`` one. The
directory in which this script resides is symbolically named ``<SALOME main
installation dir>`` and has to be replaced by the good one in the template.

When an ADAO command file is build by the ADAO GUI editor and saved, if it is
named for example "AdaoStudy1.comm", then a companion file named "AdaoStudy1.py"
is automatically created in the same directory. It is named ``<ADAO Python
file>`` in the template, and it is converted to YACS as an ``<ADAO YACS xml
scheme>``. After that, it can be executed in console mode using the standard
YACS console command (see YACS documentation for more information).

In the example, we choose to start and stop the SALOME application server in the
same script, which is not necessary, but useful to avoid stalling SALOME
sessions. We choose also to remove the ``<ADAO YACS xml scheme>`` because it is
a generated one. You only need to replace the text between these symbols
``<...>`` to use it.

The template of the shell script is the following::

    #!/bin/bash
    export USERDIR=<ADAO JDC file directory>
    export SALOMEDIR=<SALOME main installation directory>
    $SALOMEDIR/runAppli -k -t
    $SALOMEDIR/runSession python \
        $SALOMEDIR/bin/salome/AdaoYacsSchemaCreator.py \
        $USERDIR/<ADAO Python file> $USERDIR/<ADAO YACS xml scheme>
    $SALOMEDIR/runSession driver $USERDIR/<ADAO YACS xml scheme>
    $SALOMEDIR/runSession killSalome.py
    rm -f $USERDIR/<ADAO YACS xml scheme>

Standard output and errors come on console.

Running an ADAO calculation scheme in YACS using a TUI user mode
----------------------------------------------------------------

This section describes how to execute in TUI (Text User Interface) mode a YACS
calculation scheme, obtained using the ADAO "Export to YACS" function. It uses
the standard YACS TUI mode, which is briefly recalled here (see YACS
documentation for more information) through a simple example. As seen in
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

Getting information on special variables during the ADAO calculation in YACS
-----------------------------------------------------------------------------

Some special variables, used during calculations, can be monitored during the
ADAO calculation in YACS. These variables can be printed, plotted, saved, etc.
This can be done using "*observers*", that are scripts associated with one
variable. In order to use this feature, one has to build scripts using as
standard inputs (available in the namespace) the variables ``var`` and ``info``.
The variable ``var`` is to be used in the same way as for the final ADD object,
that is as a list/tuple object.

Some templates are available when editing the ADAO case in EFICAS editor. These
simple scripts can be customized by the user, either at the EFICAS edition stage
or at the YACS edition stage, to improve the tuning of the ADAO calculation in
YACS.

As an example, here is one very simple script (similar to the "*ValuePrinter*"
template) used to print the value of one monitored variable::

    print "    --->",info," Value =",var[-1]

Stored in a python file, this script can be associated to each variable
available in the "*SELECTION*" keyword of the "*Observers*" command:
"*Analysis*", "*CurrentState*", "*CostFunction*"... The current value of the
variable will be printed at each step of the optimization or assimilation
algorithm. The observers can embed plotting capabilities, storage, printing,
etc.

Getting more information when running a calculation
---------------------------------------------------

When running, useful data and messages are logged. There are two ways to obtain
theses information.

The first one, and the preferred way, is to use the built-in variable "*Debug*"
available in every ADAO case. It is available through the GUI of the module.
Setting it to "*1*" will send messages in the log window of the YACS scheme
execution.

The second one consist in using the "*logging*" native module of Python (see the
Python documentation http://docs.python.org/library/logging.html for more
information on this module). Everywhere in the YACS scheme, mainly through the
scripts entries, the user can set the logging level in accordance to the needs
of detailed informations. The different logging levels are: "*DEBUG*", "*INFO*",
"*WARNING*", "*ERROR*", "*CRITICAL*". All the informations flagged with a
certain level will be printed for whatever activated level above this particular
one (included). The easiest way is to change the log level is to write the
following Python lines::

    import logging
    logging.getLogger().setLevel(logging.DEBUG)

The standard logging module default level is "*WARNING*", the default level in
the ADAO module is "*INFO*". 

It is also recommended to include in the simulation code some logging or debug
mechanisms and use them in conjunction with the two previous methods. But be
careful not to store too big variables because it cost time, whatever logging
level is chosen.

Switching from a version of ADAO to a newer one
-----------------------------------------------

The ADAO module and cases are identified as versions, with "Major", "Minor" and
"Revision" characteristics. A particular version is numbered as
"Major.Minor.Revision".

Each version of the ADAO module can read ADAO case files of the previous minor
version. In general, it can also read ADAO case files of all the previous minor
versions for one major branch. In general also, an ADAO case file for one
version can not be read by a previous minor or major version.

Switching from 6.6 to 7.2
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case file. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

There is one incompatibility introduced for the post-processing or observer
script files. The old syntax to call a result object, such as the "*Analysis*"
one in a script provided through the "*UserPostAnalysis*" keyword), was for
example::

    Analysis = ADD.get("Analysis").valueserie(-1)
    Analysis = ADD.get("Analysis").valueserie()

The new syntax is entirely similar to the classical one of a list/tuple object::

    Analysis = ADD.get("Analysis")[-1]
    Analysis = ADD.get("Analysis")[:]

The post-processing scripts has to be modified.

Switching from 6.5 to 6.6
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case file. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

There is one incompatibility introduced for the designation of operators used to
for the observation operator. The new mandatory names are "*DirectOperator*",
"*TangentOperator*" and "*AdjointOperator*", as described in the last subsection
of the chapter :ref:`section_reference`.

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
