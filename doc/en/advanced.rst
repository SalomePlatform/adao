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

.. _section_advanced:

================================================================================
**[DocU]** Advanced usage of the ADAO module and interoperability
================================================================================

This section presents advanced methods to use the ADAO module, how to get more
information during calculation, or how to use it without the graphical user
interface (GUI). It requires to know how to find files or commands included
inside the whole SALOME installation. All the names to be replaced by user are
indicated by the syntax ``<...>``.

.. _section_advanced_convert_JDC:

Converting and executing an ADAO command file (JDC) using a Shell script
------------------------------------------------------------------------

It is possible to convert and execute an ADAO command file (JDC, or ".comm/.py"
files pair, which resides in ``<ADAO JDC file directory>``) automatically by
using a template Shell script containing all the required steps. If the SALOME
main launching command , named ``salome``, is not available in a classical
terminal, the user has to know where are the main SALOME launching files, and
in particular the ``salome`` one. The directory in which this script resides is
symbolically named ``<SALOME main installation dir>`` and has to be replaced by
the good one in the Shell file template.

When an ADAO command file is build by the ADAO graphical editor and saved, if
it is named for example "AdaoStudy1.comm", then a companion file named
"AdaoStudy1.py" is automatically created in the same directory. It is named
``<ADAO Python file>`` in the template, and it is converted to YACS as an
``<ADAO YACS xml scheme>`` as a ".xml" file named "AdaoStudy1.xml". After that,
this last one can be executed in console mode using the standard YACS console
command (see YACS documentation for more information).

In all launching command Shell files examples, we choose to start and stop the
SALOME application server in the same script. It is not mandatory, but it is
useful to avoid stalling SALOME sessions.

The simplest example consist in only launching the given YACS scheme, which was
previously generated by the user in the graphical interface. In this case,
after having replaced the strings between ``<...>`` symbols, one needs only to
save the following Shell script::

    #!/bin/bash
    USERDIR="<ADAO JDC file directory>"
    SALOMEDIR="<SALOME main installation directory>"
    $SALOMEDIR/salome start -k -t
    $SALOMEDIR/salome shell -- "driver $USERDIR/<ADAO YACS xml scheme>"
    $SALOMEDIR/salome shell killSalome.py

It is then required to change it to be in executable mode.

A more complete example consist in launching execution of a YACS scheme given
by the user, having previously verified its availability. For that, replacing
the text ``<SALOME main installation directory>``, one needs only to save the
following Shell script::

    #!/bin/bash
    if (test $# != 1)
    then
      echo -e "\nUsage: $0 <ADAO YACS xml scheme>\n"
      exit
    else
      USERFILE="$1"
    fi
    if (test ! -e $USERFILE)
    then
      echo -e "\nError : the XML file named $USERFILE does not exist.\n"
      exit
    else
      SALOMEDIR="<SALOME main installation directory>"
      $SALOMEDIR/salome start -k -t
      $SALOMEDIR/salome shell -- "driver $USERFILE"
      $SALOMEDIR/salome shell killSalome.py
    fi

An another example consist in adding the conversion of the ADAO command file
(JDC, or ".comm/.py" files pair) in an associated YACS scheme (".xml" file). At
the end of the script, one choose also to remove the ``<ADAO YACS xml scheme>``
because it is a generated file. For that, after having carefully replaced the
text ``<SALOME main installation directory>``, one needs only to save the
following Shell script::

    #!/bin/bash
    if (test $# != 1)
    then
      echo -e "\nUsage: $0 <ADAO .comm/.py case>\n"
      exit
    else
      D=`dirname $1`
      F=`basename -s .comm $1`
      F=`basename -s .py $F`
      USERFILE="$D/$F"
    fi
    if (test ! -e $USERFILE.py)
    then
      echo -e "\nError : the PY file named $USERFILE.py does not exist.\n"
      exit
    else
      SALOMEDIR="<SALOME main installation directory>"
      $SALOMEDIR/salome start -k -t
      $SALOMEDIR/salome shell -- "python $SALOMEDIR/bin/AdaoYacsSchemaCreator.py $USERFILE.py $USERFILE.xml"
      $SALOMEDIR/salome shell -- "driver $USERFILE.xml"
      $SALOMEDIR/salome shell killSalome.py
      rm -f $USERFILE.xml
    fi

In all cases, the standard output and errors come in the launching terminal.

.. _section_advanced_YACS_tui:

Running an ADAO calculation scheme in YACS using the text user mode (YACS TUI)
------------------------------------------------------------------------------

This section describes how to execute in TUI (Text User Interface) YACS mode a
YACS calculation scheme, obtained in the graphical interface by using the ADAO
"Export to YACS" function. It uses the standard YACS TUI mode, which is briefly
recalled here (see YACS documentation for more information) through a simple
example. As described in documentation, a XML scheme can be loaded in a Python.
We give here a whole sequence of command lines to test the validity of the
scheme before executing it, adding some initial supplementary ones to
explicitly load the types catalog to avoid weird difficulties::

    import pilot
    import SALOMERuntime
    import loader
    SALOMERuntime.RuntimeSALOME_setRuntime()

    r = pilot.getRuntime()
    xmlLoader = loader.YACSLoader()
    xmlLoader.registerProcCataLoader()
    try:
        catalogAd = r.loadCatalog("proc", "<ADAO YACS xml scheme>")
        r.addCatalog(catalogAd)
    except:
        pass

    try:
        p = xmlLoader.load("<ADAO YACS xml scheme>")
    except IOError,ex:
        print("IO exception:",ex)

    logger = p.getLogger("parser")
    if not logger.isEmpty():
        print("The imported file has errors :")
        print(logger.getStr())

    if not p.isValid():
        print("The schema is not valid and can not be executed")
        print(p.getErrorReport())

    info=pilot.LinkInfo(pilot.LinkInfo.ALL_DONT_STOP)
    p.checkConsistency(info)
    if info.areWarningsOrErrors():
        print("The schema is not consistent and can not be executed")
        print(info.getGlobalRepr())

    e = pilot.ExecutorSwig()
    e.RunW(p)
    if p.getEffectiveState() != pilot.DONE:
        print(p.getErrorReport())

This method allows for example to edit the YACS XML scheme in TUI, or to gather
results for further use.

.. _section_advanced_R:

Running an ADAO calculation in R environment using the TUI ADAO interface
-------------------------------------------------------------------------

.. index:: single: R
.. index:: single: rPython
.. index:: single: reticulate

To extend the analysis and treatment capacities, it is possible to use ADAO
calculations in **R** environment (see [R]_ for more details). It is available
in SALOME by launching the R interpreter in the shell "``salome shell``".
Moreover, the package "*rPython*" (or the more recent "*reticulate*" one) has
to be available, it can be installed by the user if required by the following R
command::

    #
    # IMPORTANT: to be run in R interpreter
    # -------------------------------------
    install.packages("rPython")

One will refer to the [GilBellosta15]_ documentation for more information on
this package.

The ADAO calculations defined in text interface (API/TUI, see
:ref:`section_tui`) can be interpreted from the R environment, using some data
and information from R. The approach is illustrated in the example
:ref:`subsection_tui_example`, suggested in the API/TUI interface description.
In the R interpreter, one can run the following commands, directly coming from
the simple example::

    #
    # IMPORTANT: to be run in R interpreter
    # -------------------------------------
    library(rPython)
    python.exec("
        from numpy import array
        from adao import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=[0, 1, 2] )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
        case.set( 'Observer',            Variable='Analysis', Template='ValuePrinter' )
        case.execute()
    ")

giving the result::

    Analysis [ 0.25000264  0.79999797  0.94999939]

In writing the ADAO calculations run from R, one must take close attention to
the good use of single and double quotes, that should not collide between the
two languages.

The data can come from the R environment and should be stored in properly
assigned variables to be used later in Python for ADAO. One will refer to the
[GilBellosta15]_ documentation for the implementation work. We can transform the
above example to use data from R to feed the three variables of background,
observation and observation operator. We get in the end the optimal state also
in a R variable. The other lines are identical. The example thus becomes::

    #
    # IMPORTANT: to be run in R interpreter
    # -------------------------------------
    #
    # R variables
    # -----------
    xb <- 0:2
    yo <- c(0.5, 1.5, 2.5)
    h <- '1 0 0;0 2 0;0 0 3'
    #
    # Python code
    # -----------
    library(rPython)
    python.assign( "xb",  xb )
    python.assign( "yo",  yo )
    python.assign( "h",  h )
    python.exec("
        from numpy import array
        from adao import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=xb )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array(yo) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix=str(h) )
        case.set( 'Observer',            Variable='Analysis', Template='ValuePrinter' )
        case.execute()
        xa = list(case.get('Analysis')[-1])
    ")
    #
    # R variables
    # -----------
    xa <- python.get("xa")

One notices the explicit ``str`` and ``list`` type conversions to ensure that
the data are transmitted as known standard types from "*rPython*" package.
Moreover, it is the data that can be transferred between the two languages, not
functions or methods. It is therefore necessary to prepare generically in
Python the functions to execute required by ADAO, and to forward them correctly
the data available in R.

The most comprehensive cases, proposed in :ref:`subsection_tui_advanced`, can
be executed in the same way, and they give the same result as in the standard
Python interface.

.. _section_advanced_eficas_gui:

Using the ADAO EFICAS graphical interface as an ADAO TUI command
----------------------------------------------------------------

To make it easier to quickly edit an ADAO command file with ADAO EFICAS (JDC,
or pair of files ".comm/.py", that are together in a user study directory), you
can launch the graphical user interface from the Python interpreter. To do
this, in a Python interpreter obtained from the "SALOME shell", the following
commands are used::

    from adao import adaoBuilder
    adaoBuilder.Gui()

As a reminder, the easiest way to get a Python interpreter included in a
"SALOME shell" session is to run the following command in a terminal::

    $SALOMEDIR/salome shell -- python

with ``SALOMEDIR`` the ``<SALOME main installation directory>``.

If necessary, explicit messages can be used to identify the required
environment variables that are missing. However, **this command should not be
run in the SALOME Python console** (because in this case it is enough to
activate the module since we already are in the graphical environment...) or in
an independent Python install, but it can be run in a "SALOME shell" session
obtained from the "Tools/Extensions" menu of SALOME.

.. _section_advanced_execution_mode:

Change the default execution mode of nodes in YACS
--------------------------------------------------

.. index:: single: YACS
.. index:: single: ExecuteInContainer

Various reasons may lead to want to change the default mode of node execution
in YACS (see [#]_ for the correct use of these possibilities). This may be for
performance reasons, or for example for reasons of resource conflicts.

One may want to use this change in execution mode to extend the use of local
computing resources or to set remote calculations for a node that requires it.
This is particularly the case for a node that should use a simulation resource
available on a cluster, for example.

In addition, the various calculations that are carried out (user-provided
operators, results retrieval functions, etc.) may also present conflicts if
they are performed in a single process, and in particular in the main process
of SALOME. This is the default YACS operating mode for performance and
simplicity reasons. However, it is recommended to change this functioning when
encountering execution instabilities or error messages in the graphical
interface.

In any case, in the YACS schema being edited, it is sufficient to change the
execution mode of the node(s) that require it. They have to be executed in a
new container created for the occasion (it is not enough to use the default
container, it is explicitly necessary to create a new one) and whose properties
are adapted to the intended use. The procedure is therefore as follows:

#. Create a new YACS container, using the context menu in the tree view of the YACS schema (usually on the left),
#. Adapt the characteristics of the container, for example by selecting a "*type*" property with the value "*multi*" for a truly parallel execution, or by choosing a remote computing resource defined by the "*Resource*" property, or by using advanced parameters,
#. Graphically select in the central view the node whose execution mode you want to change,
#. In the panel to the right of the node entries, unfold the execution choices (named "*Execution Mode*"), check the "*Container*" box instead of the "*YACS*" default, and choose the newly created container (it is usually named "*container0*"),
#. Save the modified schema

This can be repeated for each node that requires it, by reusing the same new
container for all nodes, or by creating a new container for each node.

A more generic way to impose a global execution in a separate container is to
use a variable named "*ExecuteInContainer*". This variable is available for
ADAO cases through graphical user interface (GUI) or the textual one (it is for
example available by default in the :ref:`section_ref_assimilation_keywords`).

.. warning::

  This change in execution mode is extremely powerful and flexible. It is
  therefore recommended that the user both use it, and at the same time be
  attentive to the interaction of the different choices he makes, to avoid, for
  example, an unintended performance deterioration, or computer conflicts that
  are complicated to diagnose.

.. _section_advanced_observer:

Getting information on special variables during the ADAO calculation
--------------------------------------------------------------------

.. index:: single: Observer
.. index:: single: Observer Template

Some special internal optimization variables, used during calculations, can be
monitored during the ADAO calculation. These variables can be printed, plotted,
saved, etc. This can be done using "*observer*", that are commands gathered in
scripts, each associated with one variable.

Some templates are available when editing the ADAO case in graphical editor.
These simple scripts can be customized by the user, either at the embedded
edition stage, or at the edition stage before execution, to improve the tuning
of the ADAO calculation.

To implement these "*observer*" efficiently, one can look to the
:ref:`section_ref_observers_requirements`.

.. _section_advanced_logging:

Getting more information when running a calculation
---------------------------------------------------

.. index:: single: Logging
.. index:: single: Debug
.. index:: single: setDebug

When running a calculation, useful data and messages are logged. There are two
ways to obtain theses information.

The first one, and the preferred way, is to use the built-in variable "*Debug*"
available in every ADAO case. It can be reached in the module's graphical user
interface (GUI) as well as in the textual interface (TUI). Setting it to "*1*"
will send messages in the log window of the YACS scheme execution.

The second one consist in using the "*logging*" native module of Python (see
the Python documentation http://docs.python.org/library/logging.html for more
information on this module). Everywhere in the YACS scheme, mainly through the
scripts entries, the user can set the logging level in accordance to the needs
of detailed information. The different logging levels are: "*DEBUG*", "*INFO*",
"*WARNING*", "*ERROR*", "*CRITICAL*". All the information flagged with a
certain level will be printed for whatever activated level above this
particular one (included). The easiest way is to change the log level by using
the following Python lines::

    import logging
    logging.getLogger().setLevel(logging.DEBUG)

The standard logging module default level is "*WARNING*", the default level in
the ADAO module is "*INFO*".

It is also recommended to include logging monitoring or debugging mechanisms in
the user's physical simulation code, and to exploit them in conjunction with
the previous two methods. But be careful not to store "too big" variables
because it cost time or memory, whatever logging level is chosen (that is, even
if these variables are not printed).

.. _subsection_ref_parallel_df:

Accelerating numerical derivatives calculations by using a parallel mode
------------------------------------------------------------------------

.. index:: single: EnableWiseParallelism
.. index:: single: NumberOfProcesses

When setting an operator, as described in
:ref:`section_ref_operator_requirements`, the user can choose a functional form
"*ScriptWithOneFunction*". This form explicitly leads to approximate the
tangent and adjoint operators (if they are required) by a finite differences
calculation. It requires several calls to the direct operator (which is the
user defined function), at least as many times as the dimension of the state
vector. This are these calls that can potentially be executed in parallel.

Under some conditions (described right after), it is then possible to
accelerate the numerical derivatives calculations by using a parallel mode for
the finite differences approximation. When setting up an ADAO case, it is done
by adding the optional keyword "*EnableWiseParallelism*", set to "1" or
"*True*". This keyword is included in the "*SCRIPTWITHONEFUNCTION*" command in
the operator definition by graphical interface, or in the "*Parameters*"
accompanying the command "*OneFunction*" by textual interaface. By default,
this parallel mode is disabled ("*EnableWiseParallelism=0*"). The parallel mode
will only use local resources (both multi-cores or multi-processors) of the
computer on which execution is running, requiring by default as many resources
as available. If necessary, one can reduce the available resources by limiting
the possible number of parallel processes using the keyword
"*NumberOfProcesses*", set to desired maximum number (or to "0" for automatic
control, which is the default value).

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
#. The user defined direct function does not already use parallelism (or parallel execution is disabled in the user calculation).
#. The user defined direct function avoids read/write access to common resources, mainly stored data, output files or memory capacities.
#. The "*observer*" added by the user avoid read/write access to common resources, such as files or memory.

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

  In case of doubt, it is recommended NOT TO ACTIVATE this parallelism.

It is also recalled that one have to choose the type "*multi*" for the default
container in order to launch the scheme, to allow a really parallel execution.

.. _subsection_iterative_convergence_control:

Convergence control for calculation cases and iterative algorithms
------------------------------------------------------------------

.. index:: single: Convergence
.. index:: single: Iterative convergence

There are many reasons to want to control the convergence of available
calculation cases or algorithms in ADAO. For example, one may want
*repeatability* of optimal solutions, certified *quality*, *stability* of
optimal search conditions in studies, *saving of global computation time*, etc.
Moreover, we notice that the methods used in ADAO are frequently iterative,
reinforcing the interest of this convergence control.

By default, **the available calculation cases or algorithms in ADAO give access
to multiple ways to control their convergence, specially adapted to each
method**. These controls are derived from classical optimization theory and
from the possibilities of each algorithm. The default values of the controls
are chosen to ensure an optimal search for high quality simulation functions
with "*standard*" behavior (regularity, physical and numerical quality...),
which is not necessarily the main property of real simulations due to various
constraints. It is therefore quite normal to adapt the convergence criteria to
the study cases encountered, but it is an expert approach to establish the
correct adaptation.

There are fairly generic ways to control the optimal search and the convergence
of algorithms. We indicate here the most useful ones, in a non-exhaustive way,
and with the significant restriction that there are many exceptions to the
recommendations made. To go further, this generic information must be completed
by the information specific to each algorithm or calculation case, indicated in
the documentation of the different :ref:`section_reference_assimilation`.

**A first way is to limit the default number of iterations in the iterative
search processes**. Even if this is not the best theoretical way to control the
algorithm, it is very effective in a real study process. For this purpose, the
keyword "*MaximumNumberOfIterations*" exists in all cases of calculations that
support it, and its default value is usually set to an equivalent of infinity
so that it is not the stopping criterion. This is the case for calculations
based on variational methods such as :ref:`section_ref_algorithm_3DVAR`,
:ref:`section_ref_algorithm_4DVAR` and
:ref:`section_ref_algorithm_NonLinearLeastSquares`, but this is also the case
for other ones like the :ref:`section_ref_algorithm_DerivativeFreeOptimization`
or :ref:`section_ref_algorithm_QuantileRegression`. In practice, a value
between 10 and 30 is recommended to make this control parameter effective and
still obtain an optimal search of good quality. For an optimal search of
sufficient quality, this restriction should not be set too strictly, i.e. a 30
iteration limit should be more favorable than a 10 iteration limit.

**A second way to control convergence is to adapt the relative decrement
tolerance in the minimization of the cost functional considered**. This
tolerance is controlled by the keyword "*CostDecrementTolerance*" in the
algorithms that support it. The default value is rather strict, it is chosen
for a theoretical convergence control when the numerical simulations are of
high numerical quality. In practice, it can be adapted without hesitation to be
between :math:`10^{-5}` and :math:`10^{-2}`. This adaptation allows in
particular to reduce or avoid the difficulties of optimal search which are
manifested by many successive iterations on almost identical states.

**A third way to improve convergence is to adapt the default setting of the
finite difference approximation, primarily for the observation operator and a
single-operator representation**. The control of this property is done with the
keyword "*DifferentialIncrement*" which sets the definition using the
:ref:`section_ref_operator_one`. Its default value is :math:`10^{-2}` (or 1%),
and it can usually be adjusted between :math:`10^{-5}` and :math:`10^{-3}`
(although it is wise to check carefully the relevance of its value, it is easy
in ADAO to change this parameter). The convergence criterion must then be
adjusted so that it does not exceed the order of magnitude of this
approximation. In practice, it is sufficient to set the
"*CostDecrementTolerance*" criterion to approximately the same precision (i.e.
with an order of magnitude more or less) as the "*DifferentialIncrement*"
criterion. This way of improvement is also to be completed with analyses using
the :ref:`section_ref_algorithm_LinearityTest` and
:ref:`section_ref_algorithm_GradientTest`.

From experience, it is *a priori* not recommended to use other means to control
convergence, even if they exist. These parameter adjustments are simple to
implement, and it is favorable to try them (in twin experiments or not) because
they solve many problems encountered in practice.

.. [#] For more information on YACS, see the *YACS module* and its integrated help available from the main menu *Help* of the SALOME platform.
