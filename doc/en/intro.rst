..
   Copyright (C) 2008-2025 EDF R&D

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

.. _section_intro:

================================================================================
Introduction to ADAO
================================================================================

The aim of the ADAO module is **to help using data assimilation or optimization
methodology, in conjunction with other modules or simulation codes, in Python**
[Python]_ **or SALOME context** [Salome]_. It provides a simple interface to
many robust and powerful data assimilation or optimization algorithms, with or
without reduction, as well as testing and verification aids. It allows to
integrate these tools in a Python or SALOME study.

Its main objective is to **provide the use of standard and robust data
assimilation or optimization methods, in a usual numerical simulation study
approach, in an efficient way, while remaining easy to setup, and by providing
a simplified approach to help the implementation**. For the end user, who has
previously collected information on his physical problem, the environment
allows him to have an approach centered on the simple declaration of this
information to build a valid ADAO case, to then evaluate it, and to get the
physical results he needs.

The module covers a wide variety of practical applications, in a robust way,
allowing for real world engineering applications, and also for performing quick
methodological experimentation. It is based on the use of other Python or
SALOME modules, in particular YACS and EFICAS if available, and on the use of
an underlying generic data assimilation library and tools. The computational or
simulation user modules must provide one or more specific calling methods in
order to be callable in the Python or SALOME framework. In the SALOME
environment, all native modules can be used through integration in Python or
YACS.
