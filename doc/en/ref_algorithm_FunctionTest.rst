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

.. index:: single: FunctionTest
.. _section_ref_algorithm_FunctionTest:

Checking algorithm "FunctionTest"
---------------------------------

Description
+++++++++++

This algorithm allows to verify that the observation operator is working
correctly and that its call is compatible with its usage in ADAO algorithms. In
practice, it allows to call one or several times the operator, activating or not
the "debug" mode during execution.

Statistics on input and output vectors for each execution of operator are given,
and an another global statistic is given at the end of the checking algorithm.
The precision of printed outputs can be controlled to facilitate automatic tests
of operator.

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: NumberOfPrintedDigits
.. index:: single: NumberOfRepetition
.. index:: single: SetDebug

The general required commands, available in the editing user interface, are the
following:

  CheckingPoint
    *Required command*. This indicates the vector used as the state around which
    to perform the required check, noted :math:`\mathbf{x}` and similar to the
    background :math:`\mathbf{x}^b`. It is defined as a "*Vector*" type object.

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

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`. In particular, the
optional command "*AlgorithmParameters*" allows to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_AlgorithmParameters` for the good use of this command.

The options of the algorithm are the following:

  NumberOfPrintedDigits
    This key indicates the number of digits of precision for floating point
    printed output. The default is 5, with a minimum of 0.

  NumberOfRepetition
    This key indicates the number of time to repeat the function evaluation. The
    default is 1.
  
  SetDebug
    This key requires the activation, or not, of the debug mode during the
    function evaluation. The default is "True", the choices are "True" or
    "False".

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_LinearityTest`
