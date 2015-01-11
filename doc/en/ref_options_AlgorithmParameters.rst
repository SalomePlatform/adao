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

.. index:: single: AlgorithmParameters
.. _section_ref_options_AlgorithmParameters:

Description of options of an algorithm by "*AlgorithmParameters*"
-----------------------------------------------------------------

Each algorithm can be controlled using some specific options, given through the
"*AlgorithmParameters*" optional command.

There are 2 practical methods for the user to provide these options. The
method is chosen by the keyword "*FROM*", included in the entry
"*AlgorithmParameters*" in EFICAS.

If an option is specified by the user for an algorithm that doesn't support it,
the option is simply left unused and don't stop the treatment. The meaning of
the acronyms or particular names can be found in the :ref:`genindex` or the
:ref:`section_glossary`.

First method : using a string in EFICAS
+++++++++++++++++++++++++++++++++++++++

To give the values for the command "*AlgorithmParameters*" as a string, directly
in the EFICAS graphical interface, the user selects this type in the keyword
"*FROM*", as shown in the following figure:

  .. :adao_algopar_string
  .. image:: images/adao_algopar_string.png
    :align: center
    :width: 100%
  .. centered::
    **Using a string for algorithmic parameters**

In the entry, one must enclose a standard dictionary definition between simple
quotes, as for example::

    '{"StoreInternalVariables":True,"MaximumNumberOfSteps":25}'

It is the recommended way to define algorithmic parameters.

Second method : using an external Python script file
++++++++++++++++++++++++++++++++++++++++++++++++++++

To give the values for the command "*AlgorithmParameters*" in an external Python
script file, the user selects in EFICAS this type in the keyword "*FROM*", as
shown in the following figure:

  .. :adao_algopar_script
  .. image:: images/adao_algopar_script.png
    :align: center
    :width: 100%
  .. centered::
    **Using an external file for algorithmic parameters**

This external Python script file has then to define a variable with the required
name "*AlgorithmParameters*", as in the following example::

    AlgorithmParameters = {
        "StoreInternalVariables" : True,
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

The file can also contain other Python commands.
