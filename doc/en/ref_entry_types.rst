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

.. _section_ref_entry_types:

List of possible input types
----------------------------

.. index:: single: Dict
.. index:: single: Function
.. index:: single: Matrix
.. index:: single: ScalarSparseMatrix
.. index:: single: DiagonalSparseMatrix
.. index:: single: String
.. index:: single: Script
.. index:: single: Vector

Each ADAO variable has a pseudo-type to help filling it and validation. The
different pseudo-types are:

.. index:: single: Dict

**Dict**
    This indicates a variable that has to be filled by a Python dictionary
    ``{"key":"value...}``, usually given either as a string or as a script file.

.. index:: single: Function

**Function**
    This indicates a variable that has to be filled by a Python function,
    usually given as a script file or a component method.

.. index:: single: Matrix

**Matrix**
    This indicates a variable that has to be filled by a matrix, usually given
    either as a string or as a script file.

.. index:: single: ScalarSparseMatrix

**ScalarSparseMatrix**
    This indicates a variable that has to be filled by a unique number (which
    will be used to multiply an identity matrix), usually given either as a
    string or as a script file.

.. index:: single: DiagonalSparseMatrix

**DiagonalSparseMatrix**
    This indicates a variable that has to be filled by a vector (which will be
    used to replace the diagonal of an identity matrix), usually given either as
    a string or as a script file.

.. index:: single: Script

**Script**
    This indicates a script given as an external file. It can be described by a
    full absolute path name or only by the file name without path. If the file
    is given only by a file name without path, and if a study directory is also
    indicated, the file is searched in the given directory.

.. index:: single: String

**String**
    This indicates a string giving a literal representation of a matrix, a
    vector or a vector series, such as "1 2 ; 3 4" or "[[1,2],[3,4]]" for a
    square 2x2 matrix.

.. index:: single: Vector

**Vector**
    This indicates a variable that has to be filled by a vector, usually given
    either as a string or as a script file.

.. index:: single: VectorSerie

**VectorSerie**
    This indicates a variable that has to be filled by a list of
    vectors, usually given either as a string or as a script file.

When a command or keyword can be filled by a script file name, the script has to
contain a variable or a method that has the same name as the one to be filled.
In other words, when importing the script in a YACS Python node, it must create
a variable of the good name in the current name space of the node.