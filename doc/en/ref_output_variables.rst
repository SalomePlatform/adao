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

.. _section_ref_output_variables:

Variables and informations available at the output
--------------------------------------------------

How to obtain the information available at the output
+++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: UserPostAnalysis
.. index:: single: algoResults
.. index:: single: getResults
.. index:: single: get
.. index:: single: ADD

At the output, after executing data assimilation, optimization or checking
study, there are variables and information originating from the calculation. The
obtaining of this information is then carried out in a standardized way using
the post-processing step of calculation.

The step is easily identified by the user into its ADAO definition case (by the
keyword "*UserPostAnalysis*") or in its YACS execution scheme (by nodes or
blocks located after the calculation block, and graphically connected to the
output port "*algoResults*" of the calculation block):

#. In the case where the user defines the post-processing in his ADAO case, it uses an external script file or commands in the field type "*String*" or "*Template*". The script it provides has a fixed variable "*ADD*" in the namespace.
#. In the case where the user defines the post-processing in its YACS scheme by a Python node located after the block of calculation, it should add a input port of type "*pyobj*" named for example "*Study*", graphically connected to the output port "*algoResults*" of the calculation block. The Python post-processing node must then start with ``ADD = Study.getResults()``.

Templates are given hereafter as :ref:`subsection_r_o_v_Template`. In all cases,
the post-processing of the user has in the namespace a variable whose name is
"*ADD*", and whose only available method is named ``get``. The arguments of this
method are an output information name, as described in the
:ref:`subsection_r_o_v_Inventaire`.

For example, to have the optimal state after a data assimilation or optimization
calculation, one use the following call::

    ADD.get("Analysis")

This call returns a list of values of the requested notion (or, in the case of
input variables that are by nature only a unique specimen, the value itself).
One can then request a particular item in the list by the standard list commands
(especially ``[-1]`` for the last, and ``[:]`` for all items).

.. _subsection_r_o_v_Template:

Examples of Python scripts to obtain or treat the outputs
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Template
.. index:: single: AnalysisPrinter
.. index:: single: AnalysisSaver
.. index:: single: AnalysisPrinterAndSaver

These examples present Python commands or scripts which allow to obtain or to
treat the output of an algorithm run. To help the user, they are directly
available in the user interface, when building the ADAO case in the embedded
case editor, in the "*Template*" type fields. In an equivalent way, these
commands can be integrated in an external user script (and inserted in the ADAO
case by a "*Script*" type input) or can exist as a string, including line feeds
(and inserted in the ADAO case by a "*String*" type input). Lot of variants can
be build from these simple examples, the main objective being to help the user
to elaborate the exact procedure he needs in output.

The first example (named "*AnalysisPrinter*" in the inputs of type
"*Template*") consists in printing, in the standard log output, the value of the
analysis or the optimal state, noted as :math:`\mathbf{x}^a` in the section
:ref:`section_theory`. It is realized by the commands::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    print('Analysis:',xa)

The ``numpy.ravel`` function is here to be sure that the ``xa`` variable will
contain a real unidimensional vector, whatever the previous computing choices
are.

A second example (named "*AnalysisSaver*" in the inputs of type  "*Template*")
consists in saving on file the value of the analysis or the optimal state
:math:`\mathbf{x}^a`. It is realized by the commands::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)"

The chosen recording file is a text one named ``/tmp/analysis.txt``.

It is easy to combine these two examples by building a third one (named
"*AnalysisPrinterAndSaver*" in the inputs of type  "*Template*"). It consists in
simultaneously printing in the standard log output and in saving on file the
value of :math:`\mathbf{x}^a`. It is realized by the commands::

    import numpy
    xa=numpy.ravel(ADD.get('Analysis')[-1])
    print('Analysis:',xa)
    f='/tmp/analysis.txt'
    print('Analysis saved in "%s"'%f)
    numpy.savetxt(f,xa)

To facilitate these examples extension for user needs, we recall that all the
SALOME functions are available at the same level than these commands. The user
can for example request for graphical representation with the PARAVIS [#]_ or
other modules, for computing operations driven by YACS [#]_ or an another
module, etc.

Other usage examples are also given for :ref:`section_u_step4` of the
:ref:`section_using` section, or in part :ref:`section_examples`.

Cross compliance of the information available at the output
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Stored

The availability of information after the calculation is conditioned by the fact
that they have been calculated or requested.

Each algorithm does not necessarily provide the same information, and not
necessarily for example uses the same intermediate quantities. Thus, there is
information that are always present such as the optimal state resulting from the
calculation. The other information are only present for certain algorithms
and/or if they have been requested before the execution of the calculation.

It is recalled that the user can request additional information during the
preparation of its ADAO case, using the optional control "*AlgorithmParameters*" of
ADAO case. Reference will be made to the
:ref:`section_ref_options_Algorithm_Parameters` for the proper use of this
command, and to the description of each algorithm for the information available
by algorithm. One can also ask to keep some input information by changing the
boolean "* * Stored" associated with it in the edition of the ADAO case.

.. _subsection_r_o_v_Inventaire:

Inventory of potentially available information at the output
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The main set of potentially available information at the output is listed here
regardless of algorithms, for inventory. One has to look directly to algorithm
details to get full inventory.

The optimal state is an information that is always naturally available after an
optimization or a data assimilation calculation. It is indicated by the
following keywords:

  .. include:: snippets/Analysis.rst

The following variables are input variables.  They are made available to the
user at the output in order to facilitate the writing of post-processing
procedures, and are conditioned by a user request using a boolean "*Stored*"
at the input. All these returned input variables can be obtained with the
standard command ".get(...)", which return the unique object given on input.

  .. include:: snippets/Background.rst

  .. include:: snippets/BackgroundError.rst

  .. include:: snippets/EvolutionError.rst

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationError.rst

All other information are conditioned by the algorithm and/or the user requests
of availability. The main ones are the following, in alphabetical order:

  .. include:: snippets/APosterioriCorrelations.rst

  .. include:: snippets/APosterioriCovariance.rst

  .. include:: snippets/APosterioriStandardDeviations.rst

  .. include:: snippets/APosterioriVariances.rst

  .. include:: snippets/BMA.rst

  .. include:: snippets/CostFunctionJ.rst

  .. include:: snippets/CostFunctionJb.rst

  .. include:: snippets/CostFunctionJo.rst

  .. include:: snippets/CostFunctionJAtCurrentOptimum.rst

  .. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

  .. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

  .. include:: snippets/CurrentOptimum.rst

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/IndexOfOptimum.rst

  .. include:: snippets/Innovation.rst

  .. include:: snippets/InnovationAtCurrentState.rst

  .. include:: snippets/OMA.rst

  .. include:: snippets/OMB.rst

  .. include:: snippets/Residu.rst

  .. include:: snippets/SimulatedObservationAtBackground.rst

  .. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

  .. include:: snippets/SimulatedObservationAtCurrentState.rst

  .. include:: snippets/SimulatedObservationAtOptimum.rst

  .. include:: snippets/SimulationQuantiles.rst

.. [#] For more information on PARAVIS, see the *PARAVIS module* and its integrated help available from the main menu *Help* of the SALOME platform.

.. [#] For more information on YACS, see the *YACS module* and its integrated help available from the main menu *Help* of the SALOME platform.
