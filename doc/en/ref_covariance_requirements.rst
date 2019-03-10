..
   Copyright (C) 2008-2019 EDF R&D

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

.. _section_ref_covariance_requirements:

Requirements to describe covariance matrices
--------------------------------------------

.. index:: single: BackgroundError
.. index:: single: ObservationError
.. index:: single: EvolutionError
.. index:: single: setBackgroundError
.. index:: single: setObservationError
.. index:: single: setEvolutionError
.. index:: single: covariance matrix
.. index:: single: background error covariances
.. index:: single: observation error covariances
.. index:: single: covariances

In general, a variance-covariance matrix, generally called a covariance matrix,
has to be squared, symmetric and semi-definite positive. Each of its terms
describes the covariance of the two random variables corresponding to its
position in the matrix. The normalized form of the covariance is the linear
correlation. One can express the following relation, between a covariance
matrix :math:`\mathbf{M}` and its corresponding correlation matrix
:math:`\mathbf{C}` (full matrix) and standard deviation matrix
:math:`\mathbf{\Sigma}` (diagonal matrix):

.. math:: \mathbf{M} = \mathbf{\Sigma} * \mathbf{C} * \mathbf{\Sigma}

Various covariance matrices are required to implement the data assimilation or
optimization procedures. The main ones are the background error covariance
matrix, noted as :math:`\mathbf{B}`, and the observation error covariance matrix,
noted as :math:`\mathbf{R}`.

In the graphical interface EFICAS of ADAO, there are 3 practical methods for
the user to provide a covariance matrix. The method is chosen by the
"*INPUT_TYPE*" keyword of each defined covariance matrix, as shown by the
following figure:

  .. eficas_covariance_matrix:
  .. image:: images/eficas_covariance_matrix.png
    :align: center
    :width: 100%
  .. centered::
    **Choosing covariance matrix representation**

In the textual interface (TUI) of ADAO (see the part :ref:`section_tui`), the
same information can be given with the right command "*setBackgroundError*",
"*setObservationError*" or "*setEvolutionError*" depending on the physical
quantity to define. The other arguments "*Matrix*", "*ScalarSparseMatrix*" and
"*DiagonalSparseMatrix*" of the command allow to define it as described in the
following sub-parts. These information can also be given as a script in an
external file (argument "*Script*").

First matrix form: using "*Matrix*" representation
++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Matrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError
.. index:: single: setBackgroundError
.. index:: single: setObservationError
.. index:: single: setEvolutionError

This first form is the default and more general one. The covariance matrix
:math:`\mathbf{M}` has to be fully specified. Even if the matrix is symmetric by
nature, the entire :math:`\mathbf{M}` matrix has to be given.

.. math:: \mathbf{M} =  \begin{pmatrix}
    m_{11} & m_{12} & \cdots   & m_{1n} \\
    m_{21} & m_{22} & \cdots   & m_{2n} \\
    \vdots & \vdots & \vdots   & \vdots \\
    m_{n1} & \cdots & m_{nn-1} & m_{nn}
    \end{pmatrix}

It can be either a Python Numpy array or a matrix, or a list of lists of values
(that is, a list of rows). For example, a simple diagonal unitary background
error covariance matrix :math:`\mathbf{B}` can be described in a Python script
file as::

    BackgroundError = [[1, 0 ... 0], [0, 1 ... 0] ... [0, 0 ... 1]]

or::

    BackgroundError = numpy.eye(...)

Second matrix form: using "*ScalarSparseMatrix*" representation
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScalarSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError
.. index:: single: setBackgroundError
.. index:: single: setObservationError
.. index:: single: setEvolutionError

On the opposite, this second form is a very simplified method to provide a
matrix. The covariance matrix :math:`\mathbf{M}` is supposed to be a positive
multiple of the identity matrix. This matrix can then be specified in a unique
way by the multiplier :math:`m`:

.. math:: \mathbf{M} =  m \times \begin{pmatrix}
    1       & 0      & \cdots   & 0      \\
    0       & 1      & \cdots   & 0      \\
    \vdots  & \vdots & \vdots   & \vdots \\
    0       & \cdots & 0        & 1
    \end{pmatrix}

The multiplier :math:`m` has to be a floating point or integer positive value
(if it is negative, which is impossible for a positive covariance matrix, it is
converted to positive value). For example, a simple diagonal unitary background
error covariance matrix :math:`\mathbf{B}` can be described in a python script
file as::

    BackgroundError = 1.

or, better, by a "*String*" directly in the graphical or textual ADAO case.

Third matrix form: using "*DiagonalSparseMatrix*" representation
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: DiagonalSparseMatrix
.. index:: single: BackgroundError
.. index:: single: EvolutionError
.. index:: single: ObservationError
.. index:: single: setBackgroundError
.. index:: single: setObservationError
.. index:: single: setEvolutionError

This third form is also a simplified method to provide a matrix, but a little
more powerful than the second one. The covariance matrix :math:`\mathbf{M}` is
already supposed to be diagonal, but the user has to specify all the positive
diagonal values. The matrix can then be specified only by a vector
:math:`\mathbf{V}` which will be set on a diagonal matrix:

.. math:: \mathbf{M} =  \begin{pmatrix}
    v_{1}  & 0      & \cdots   & 0      \\
    0      & v_{2}  & \cdots   & 0      \\
    \vdots & \vdots & \vdots   & \vdots \\
    0      & \cdots & 0        & v_{n}
    \end{pmatrix}

It can be either a Python Numpy array or a matrix, or a list or a list of list
of positive values (in all cases, if some are negative, which is impossible,
they are converted to positive values). For example, a simple diagonal unitary
background error covariance matrix :math:`\mathbf{B}` can be described in a
python script file as::

    BackgroundError = [1, 1 ... 1]

or::

    BackgroundError = numpy.ones(...)

As previously indicated, one can also define this matrix by a "*String*"
directly in the graphical or textual ADAO case.
