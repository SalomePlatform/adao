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

.. _section_ref_userpostanalysis_requirements:

Requirements to describe a post-processing after an ADAO calculation
--------------------------------------------------------------------

.. index:: single: Post-processing
.. index:: single: UserPostAnalysis
.. index:: single: setUserPostAnalysis
.. index:: single: UserPostAnalysis Template

Results processing is usually needed after an ADAO calculation, to insert it in
a complete study. After execution of a calculation case, the main information
is the variable "*Analysis*" which contains a result of optimal estimation. In
addition, all calculation variables that have been requested in intermediate
storage are also available by means of the special algorithm variable
"*StoreSupplementaryCalculations*".

The simplest processing is often represented by a few lines of Python, which
can easily be repeated or carried over between studies. But more complex
processing of results, in the full SALOME study environment, is often done by
explicit parts of additional post-processing, either in YACS nodes or by Python
commands in TUI, or other methods. It is therefore often interesting to
identify at least part of the calculations following the ADAO estimation, and
to associate them in the calculation case.

ADAO thus gives the ability to define a general post-processing for each
calculation case. This definition is done by indicating the commands to be
performed at the output of the ADAO calculation.

Save a dedicated post-processing
++++++++++++++++++++++++++++++++

In the graphical interface EFICAS for ADAO, there are 3 convenient methods to
integrate a dedicated post-processing for an ADAO case. The method is chosen
using the "*FROM*" keyword of the main entry "*UserPostAnalysis*", as shown in
the following figure:

  .. eficas_userpostanalysis_nodetype:
  .. image:: images/eficas_userpostanalysis_nodetype.png
    :align: center
    :width: 100%
  .. centered::
    **Choose your input type for the recorded post-processing**

Post-processing can be provided as an explicit script (input of type
"*String*"), as a script contained in an external file (input of type
"*Script*"), or by using a template (input of type "*Template*"). Templates are
provided by default when using the graphical editor EFICAS for ADAO or the TUI
interface, and are detailed in the
:ref:`section_ref_userpostanalysis_templates` section that follows. These are
simple scripts that can be adapted by the user, either in the integrated case
editing step with EFICAS for ADAO, or in the schema editing step before
execution, to improve the performance of the ADAO calculation in the SALOME
execution supervisor.

In the ADAO TUI textual interface (see the :ref:`section_tui` section), the
same information can be given using the "*setUserPostAnalysis*" command. The
arguments of this command allow to define the treatment either as a template
(argument "*Template*") referring to one of the scripts detailed in the part
:ref:`section_ref_userpostanalysis_templates`, or as an explicit script
(argument "*String*"), or as a script contained in an external file (argument
"*Script*")

General form of a script to define a dedicated post-processing
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A set of post-processing commands is a special Python script, which is
automatically activated at the end of the estimation calculations in ADAO. Any
Python commands, which a user can add after a TUI calculation in ADAO, can be
part of this post-processing. Several command set templates are available by
default,essentially to give the simplest possible example of recording these
series.

To be usable in an automatic way, it is required that any call of the ADAO
calculation case, to recover a variable, is done only with the reserved name
"*ADD*". As an example, here is a very simple script (similar to the
"*ValuePrinter*" template), usable to display the value of the optimal
estimate::

    print('# Post-analysis')
    import numpy
    xa = numpy.ravel(ADD.get('Analysis')[-1])
    print('Analysis',xa)

If the command "*ADD.get(...)*", used to obtain a result variable, does not use
the reserved name "*ADD*" for the calculation case, then the call will lead to
a runtime error and will warn about the missing case name.

To illustrate, the declaration of a model, in TUI interface, is done by using
the command::

    ADD.setUserPostAnalysis(Template = "AnalysisPrinter")

.. warning::

    If not using the default available templates, it is up to the user to make
    carefully established function scripts or external programs that do not
    crash before being registered as an "*observer*" function. The debugging
    can otherwise be really difficult!

Hereinafter we give the identifier and the contents of all the available
simple templates.

.. _section_ref_userpostanalysis_templates:

Inventory of simple templates of post-processing ("*Template*")
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: AnalysisPrinter (Observer)

Modèle **AnalysisPrinter**
..........................

Print on standard output the optimal value.

::

    print('# Post-analysis')
    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    print('Analysis',xa)

.. index:: single: AnalysisSaver (Observer)

Modèle **AnalysisSaver**
........................

Save the optimal value in a file of the '/tmp' directory named 'analysis.txt'.

::

    print('# Post-analysis')
    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)

.. index:: single: AnalysisPrinterAndSaver (Observer)

Modèle **AnalysisPrinterAndSaver**
..................................

Print on standard output and, in the same time save in a file of the '/tmp' directory, the optimal value.

::

    print('# Post-analysis')
    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    print 'Analysis',xa
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)
