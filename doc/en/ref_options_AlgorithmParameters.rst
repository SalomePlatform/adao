..
   Copyright (C) 2008-2020 EDF R&D

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

.. index:: single: AlgorithmParameters
.. index:: single: Parameters
.. index:: single: Defaults
.. index:: single: setAlgorithmParameters
.. _section_ref_options_Algorithm_Parameters:

Description of options of an algorithm by "*AlgorithmParameters*"
-----------------------------------------------------------------

Each algorithm can be controlled using some specific options or parameters. They
are given through the "*Parameters*" optional command included in the mandatory
command "*AlgorithmParameters*".

There are 3 practical methods for the user of the EFICAS graphical user
interface of ADAO (GUI) to provide these options. The method is determined as
follows in the ADAO EFICAS graphical user interface:

#. firstly using the "*Parameters*" keyword in the "*AlgorithmParameters*"
   command, which allows to choose between "*Defaults*" (use of explicit
   pre-filled keywords by default parameters values) and "*Dict*" (use of a
   dictionary to fill the necessary keywords),
#. then secondly or thirdly, only in the "*Dict*" case of "*Parameters*", by
   the included keyword "*FROM*" which allows to choose between a string entry
   and a Python script file entry.

These two last options can be also used in the ADAO textual interface (TUI),
through the keywords "*Parameters*" and "*Script*" of the corresponding command
"*AlgorithmParameters*" (see the :ref:`section_tui` part for detailed
description).

If an option or a parameter is specified by the user for an algorithm that does
not support it, the option is simply ignored (left unused) and don't stop the
treatment. The meaning of the acronyms or particular names can be found in the
:ref:`genindex` or the :ref:`section_glossary`.

First method : using explicit pre-filled keywords
+++++++++++++++++++++++++++++++++++++++++++++++++

To give the parameters values by explicit pre-filled keywords, directly in the
graphical interface, the user selects the type "*Defaults*" in the keyword
"*Parameters*", then the keywords in the given "*Parameters[Algo]*" list which
appears, linked with the chosen algorithm, as shown in the following figure:

  .. adao_algopar_defaults:
  .. image:: images/adao_algopar_defaults.png
    :align: center
    :width: 100%
  .. centered::
    **Using explicit pre-filled keywords for algorithmic parameters**

Each parameter is optional, and it is presented with its default value when it
is selected by the user. One can then modify its value, or fill it in list cases
for example.

It is the recommended way to modify only some algorithmic parameters in a safe
way. This method allows only to define authorized parameters for a given
algorithm, and the defined values are not kept if the user changes the
algorithm.

This method is naturally not usable in TUI interface.

Second method : using a string in the graphical interface
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

To give the parameters values as a string, directly in the graphical interface,
the user selects the type "*Dict*" in the keyword "*Parameters*", then the type
"*String*" in the keyword "*FROM*" of the "*Dict*" command which appears, as
shown in the following figure:

  .. :adao_algopar_string
  .. image:: images/adao_algopar_string.png
    :align: center
    :width: 100%
  .. centered::
    **Using a string for algorithmic parameters**

In the entry, one must enclose a standard dictionary definition between simple
quotes, as for example::

    '{"MaximumNumberOfSteps":25,"SetSeed":1000}'

It is the recommended way to define algorithmic parameters. This method allows
in particular to keep options or parameters for other algorithms than the
currently used one. It is then easier to change of algorithm or to keep default
values different of the standard defaults.

In the textual interface TUI, the dictionary has only to be given as argument
of the "*Parameters*" keyword.

Third method : using an external Python script file
+++++++++++++++++++++++++++++++++++++++++++++++++++

To give the parameters values as an external Python script file, the user
selects in the graphical interface the type "*Dict*" in the keyword
"*Parameters*", then the type "*Script*" in the keyword "*FROM*" of the "*Dict*"
command which appears, as shown in the following figure:

  .. :adao_algopar_script
  .. image:: images/adao_algopar_script.png
    :align: center
    :width: 100%
  .. centered::
    **Using an external file for algorithmic parameters**

This external Python script file has then to define a variable with the required
name "*AlgorithmParameters*", as in the following example::

    AlgorithmParameters = {
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

The file can also contain other Python commands. This method also allows, as
the previous one, to keep options or parameters for other algorithms than the
currently used one.

In the textual interface TUI, the file name has only to be given as argument of
the "*Script*" keyword.
