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

.. _section_notations:

Notations and common conventions
================================

In all this documentation, we use standard notations of linear algebra, data
assimilation (as described in [Ide97]_) and optimization.

For algebraic formulations, vectors are written horizontally or vertically
without making a difference. Matrices are written either normally, or with a
condensed notation, consisting in the use of a space to separate the values,
and a "``;``" to separate the rows of the matrix, in a continuous line.

Files can be indicated by an absolute or relative path. For some old or shared
file systems, the full name with the path must not contain more than 256
characters. In the case of Python files, it is advisable not to use dots in the
name apart for the extension, to prevent difficulties in using it that are
complicated to diagnose.

File type and naming conventions rely heavily on the extensions of the files
themselves. Some of them are briefly specified here, without being exhaustive:

- extension ``.py``   : data or commands text file of Python source type
- extension ``.comm`` : commands text file of EFICAS type
- extension ``.xml``  : data text file of XML type or commands (for YACS, not exclusive)
- extension ``.txt``  : data text file with space separator
- extension ``.dat``  : data text file with space separator
- extension ``.csv``  : data text file with comma or semicolon separator
- extension ``.tsv``  : data text file with tab separator
- extension ``.npy``  : data binary file of type Numpy mono-variable
- extension ``.npz``  : data binary file of type Numpy multi-variables
- extension ``.sdf``  : data binary file of type Scientific Data Format

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Asch16]_
- [Bouttier99]_
- [Ide97]_
- [WikipediaMO]_
