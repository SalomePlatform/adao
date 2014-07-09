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

.. _section_home:

================================================================================
ADAO documentation
================================================================================

.. image:: images/ADAO_logo.png
   :align: center
   :width: 20%

The ADAO module provides **data assimilation and optimization** features in
SALOME context. It is based on usage of other SALOME modules, namely YACS and
EFICAS, and on usage of a generic underlying data assimilation library.

Briefly stated, Data Assimilation is a methodological framework to compute the
optimal estimate of the inaccessible true value of a system state over time. It
uses information coming from experimental measurements or observations, and from
numerical *a priori* models, including information about their errors. Parts of
the framework are also known under the names of *parameter estimation*, *inverse
problems*, *Bayesian estimation*, *optimal interpolation*, etc. More details can
be found in the section :ref:`section_theory`.

The documentation of this module is divided in parts. The first one is an
:ref:`section_intro`. The second part introduces :ref:`section_theory`, and
their concepts. The third part describes :ref:`section_using`. The fourth part
gives examples on ADAO usage as :ref:`section_examples`. The fifth part gives a
detailed :ref:`section_reference`. Users interested in quick use of the module
can stop reading before this fifth part, but a valuable use of the module
requires to read and come back regularly to the third and fifth ones. The last
part focuses on :ref:`section_advanced`, how to get more information, or how to
use it by scripting, without the graphical user interface (GUI). And, to respect
the module requirements, be sure to read the part :ref:`section_license`.

In all this documentation, we use standard notations of linear algebra, data
assimilation (as described in [Ide97]_) and optimization. In particular, vectors
are written horizontally or vertically without making difference. Matrices are
written either normally, or with a condensed notation, consisting in the use of
a space to separate values and a "``;``" to separate the rows, in a continuous
line.

Table of contents
-----------------

.. toctree::
   :maxdepth: 2

   intro
   theory
   using
   examples
   advanced
   reference
   license
   glossary
   bibliography

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`

.. * :ref:`section_glossary`
