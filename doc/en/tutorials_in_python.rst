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

.. _section_tutorials_in_python:

================================================================================
**[DocU]** Tutorials on using the ADAO module in Python
================================================================================

This section presents some examples on using the ADAO module in SALOME. The
first one shows how to build a simple data assimilation case defining
explicitly all the required input data through the textual user
interface (TUI). The second one shows, on the same case, how to define input
data using external sources through scripts.

The mathematical notations used afterward are explained in the section
:ref:`section_theory`.

Building an estimation case with explicit data definition
---------------------------------------------------------

