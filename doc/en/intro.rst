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

.. _section_intro:

================================================================================
Introduction to ADAO
================================================================================

The aim of the ADAO module is **to help using data assimilation or optimization
methodology in conjunction with other modules or simulation codes in SALOME**.
The ADAO module provides interface to some standard algorithms of data
assimilation or optimization, and allows integration of their use in a SALOME
study. Calculation or simulation modules have to provide one or more specific
calling methods in order to be callable in the SALOME/ADAO framework, and all
the SALOME modules can be used through YACS integration of ADAO.

Its main objective is **to provide the use of various standard data 
assimilation or optimization methods, while remaining easy to use and providing 
a path to help the implementation**. For an end user, having already gathered 
his physical input information, it's a matter of "point\&click" to build an 
ADAO valid case and to evaluate it.

The module covers a wide variety of practical applications, in a robust way,
allowing real engineering applications but also quick experimental methodology
setup to be performed. Its methodological and numerical scalability gives way to
extend the application domain.
