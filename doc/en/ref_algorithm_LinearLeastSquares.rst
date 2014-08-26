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

.. index:: single: LinearLeastSquares
.. _section_ref_algorithm_LinearLeastSquares:

Calculation algorithm "*LinearLeastSquares*"
--------------------------------------------

Description
+++++++++++

This algorithm realizes a "Least Squares" linear type estimation of the state of
a system. It is similar to the :ref:`section_ref_algorithm_Blue`, without its
background part.

This algorithm is always the fastest of all the optimization algorithms of ADAO.
It is theoretically reserved for observation operator cases which are linear,
even if it sometimes works in "slightly" non-linear cases. One can verify the
linearity of the observation operator with the help of the
:ref:`section_ref_algorithm_LinearityTest`.

In all cases, it is recommanded to prefer at least the
:ref:`section_ref_algorithm_Blue`, or the
:ref:`section_ref_algorithm_ExtendedBlue` or the
:ref:`section_ref_algorithm_3DVAR`.

Optional and required commands
++++++++++++++++++++++++++++++

.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: StoreInternalVariables
.. index:: single: StoreSupplementaryCalculations

The general required commands, available in the editing user interface, are the
following:

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

The general optional commands, available in the editing user interface, are
indicated in :ref:`section_ref_assimilation_keywords`. In particular, the
optional command "*AlgorithmParameters*" allows to choose the specific options,
described hereafter, of the algorithm. See
:ref:`section_ref_options_AlgorithmParameters` for the good use of this command.

The options of the algorithm are the following:

  StoreInternalVariables
    This Boolean key allows to store default internal variables, mainly the
    current state during iterative optimization process. Be careful, this can be
    a numerically costly choice in certain calculation cases. The default is
    "False".

    Example : ``{"StoreInternalVariables":True}``

  StoreSupplementaryCalculations
    This list indicates the names of the supplementary variables that can be
    available at the end of the algorithm. It involves potentially costly
    calculations or memory consumptions. The default is a void list, none of
    these variables being calculated and stored by default. The possible names
    are in the following list: ["OMA"].

    Example : ``{"StoreSupplementaryCalculations":["OMA"]}``

*Tips for this algorithm:*

    As the *"Background"* and *"BackgroundError"* commands are required for ALL
    the calculation algorithms in the interface, you have to provide a value,
    even if these commands are not required for this algorithm, and will not be
    used. The simplest way is to give "1" as a STRING for both.

See also
++++++++

References to other sections:
  - :ref:`section_ref_algorithm_Blue`
  - :ref:`section_ref_algorithm_ExtendedBlue`
  - :ref:`section_ref_algorithm_3DVAR`
  - :ref:`section_ref_algorithm_LinearityTest`