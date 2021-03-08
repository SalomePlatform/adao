..
   Copyright (C) 2008-2021 EDF R&D

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
   :alt: ADAO logo

**The ADAO module provides data assimilation and optimization** features in
Python [Python]_ or SALOME context [Salome]_.

Briefly stated, Data Assimilation is a methodological framework to compute the
optimal estimate of the inaccessible true value of a system state, eventually
over time. It uses information coming from experimental measurements or
observations, and from numerical *a priori* models, including information about
their errors. Parts of the framework are also known under the names of
*parameter estimation*, *inverse problems*, *Bayesian estimation*, *optimal
interpolation*, *field reconstruction*, etc. The ADAO module currently offers
more than 100 different algorithmic methods and allows the study of about 350
distinct applied problems. More details can be found in the section
:ref:`section_theory`.

The documentation for this module is divided into several major categories,
related to the theoretical documentation (indicated in the section title by
**[DocT]**), to the user documentation (indicated in the section title by
**[DocU]**), and to the reference documentation (indicated in the section title
by **[DocR]**).

The first part is the :ref:`section_intro`. The second part introduces
:ref:`section_theory`, and their concepts, and the next part describes the
:ref:`section_methodology`. For a standard user, the next parts describe
examples on ADAO usage as :ref:`section_tutorials_in_salome` or
:ref:`section_tutorials_in_python`, then indicates the :ref:`section_advanced`,
with how to obtain additional information or how to use non-GUI command
execution scripting. Users interested in quick use of the module can stop
before reading the rest, but a valuable use of the module requires to read and
come back regularly to these parts. The following parts describe
:ref:`section_gui_in_salome` and :ref:`section_tui`. The last main part gives a
detailed :ref:`section_reference`, with three essential main sub-parts
describing the details of commands and options of the algorithms. A
:ref:`section_glossary`, some :ref:`section_notations`, a
:ref:`section_bibliography` and an extensive index are included in
the document. And, to comply with the module requirements, be sure to read the
part :ref:`section_license`.

.. toctree::
   :caption: Table of contents
   :name: mastertoc
   :maxdepth: 2
   :numbered: 2

   intro
   theory
   methodology
   tutorials_in_salome
   tutorials_in_python
   advanced
   gui_in_salome
   tui
   reference
   license
   bibliography
   notations
   glossary
   genindex

* :ref:`search`
