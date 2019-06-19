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

.. _section_ref_entry_types:

List of possible input types
----------------------------

Each variable to be entered for the use of ADAO can be represented by means of
particular "pseudo-types", which help to logically fill it in and validate it
computationaly. These pseudo-types explicitly represent mathematical forms
(:ref:`section_ref_entry_types_math`) or simple computer forms
(:ref:`section_ref_entry_types_info`), which are detailed here.
:ref:`section_notations` are also used, together with
:ref:`section_ref_entry_types_names`.

.. _section_ref_entry_types_math:

Pseudo-types of mathematical representation of data
+++++++++++++++++++++++++++++++++++++++++++++++++++

The inputs are described according to the simplest possible logic, in
mathematical representation, for algorithms or calculation tools.

.. include:: snippets/EntryTypeVector.rst

.. include:: snippets/EntryTypeVectorSerie.rst

.. include:: snippets/EntryTypeMatrix.rst

.. include:: snippets/EntryTypeFunction.rst

.. include:: snippets/EntryTypeDict.rst

The variables to which these pseudo-types apply can themselves be given using
the following computer descriptions.

.. _section_ref_entry_types_info:

Pseudo-types of digital data description
++++++++++++++++++++++++++++++++++++++++

Three pseudo-types, purely computer-based, are used to specify the way in which
input variables are provided.

.. include:: snippets/EntryTypeScript.rst

.. include:: snippets/EntryTypeString.rst

.. include:: snippets/EntryTypeDataFile.rst

.. _section_ref_entry_types_names:

Information on the names required for file entries
++++++++++++++++++++++++++++++++++++++++++++++++++

When a command or keyword can be entered using a script file identified by the
pseudo-type "*Script*", this script must contain a variable or method that has
the same name than the variable to be completed. In other words, when importing
such a script into a Python command or Python node, it must create a variable
of the correct name in the current namespace of the node. For example, a Python
script making available the draft variable, named "*Background*", must have the
following form::

    ...
    ...
    Background =...
    ...
    ...

Its import thus makes it possible to create the variable "*Background*" in the
current namespace. The dots"..." symbolize any code around this particular line
beginning.

Similarly, when a particular vector can be filled in using a data file
designated by the pseudo-type "*DataFile*", the information in the file
"*DataFile*" must be named after the vector to be loaded.
