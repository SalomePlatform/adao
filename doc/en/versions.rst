..
   Copyright (C) 2008-2026 EDF R&D

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

.. _section_versions:

================================================================================
Versions of ADAO and external compatibility
================================================================================

.. _subsection_new_adao_version:
.. index::
    pair: Version ; ADAO
    pair: Version of ADAO ; Switching

Switching from a version of ADAO to a newer one
-----------------------------------------------

The ADAO module and its ".comm" case files are identified by versions, with
"Major", "Minor", "Revision" and optionally "Installation" characteristics. A
particular version is numbered as "Major.Minor.Revision", with strong link with
the numbering of the SALOME platform. The optional indication of a fourth
number indicates a difference in the installation method, not in the content of
the version.

Each version "Major.Minor.Revision" of the ADAO module can read ADAO case files
of the previous minor version "Major.Minor-1.*". In general, it can also read
ADAO case files of all the previous minor versions for one major branch, but it
is not guaranteed for all the commands or keywords. In general also, an ADAO
case file for one version can not be read by a previous minor or major version
of the ADAO module.

Switching from 9.x to 9.y with y > x
++++++++++++++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

However, there may be incompatibilities from user cases written directly in TUI
interface. It is advisable to review the syntax and arguments in the TUI
scripts at each version change. In particular, it is advisable to check that
the algorithm parameters are still adequate and active, knowing that it has
been explicitly chosen that there is no message when an optional parameter
becomes inactive or changes its name (for the example, we quote the parameter
"*MaximumNumberOfSteps*" as having changed its name to
"*MaximumNumberOfIterations*", for homogeneity with the variables that can be
displayed) to avoid a lock.

Switching from 8.5 to 9.2
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

However, there may be incompatibilities from user script files that would not
have a syntax compatible with Python 3. The most immediate error is the use of
printing "*print*" with "*command*" syntax instead of functional syntax
"*print(...)*". In this case, it is suggested to correct the syntax of user
files in environment 8 before switching to environment 9.

Switching from 8.x to 8.y with y > x
++++++++++++++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

To make future developments easier, it is strongly recommended to ensure that
your user scripts files use a Python 2 and a Python 3 compatible syntax. In
particular, it is recommended to use the functional syntax for "*print*" and not
the "*command*" syntax, for example::

    # Python 2 & 3
    x, unit = 1., "cm"
    print( "x = %s %s"%(str(x),str(unit)) )

or::

    # Python 2 & 3
    x, unit = 1., "cm"
    print( "x = {0} {1}".format(str(x),str(unit)) )

rather than::

    # Python 2 only
    x, unit = 1., "cm"
    print "x =", x, unit

Switching from 7.8 to 8.1
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

Switching from 7.x to 7.y with y > x
++++++++++++++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

Switching from 6.6 to 7.2
+++++++++++++++++++++++++

There is no known incompatibility for the ADAO case files. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

There is one incompatibility introduced for the post-processing or observer
script files. The old syntax to call a result object, such as the "*Analysis*"
one (in a script provided through the "*UserPostAnalysis*" keyword), was for
example::

    Analysis = ADD.get("Analysis").valueserie(-1)
    Analysis = ADD.get("Analysis").valueserie()

The new syntax is entirely similar to the (classical) one of a list or tuple
object::

    Analysis = ADD.get("Analysis")[-1]
    Analysis = ADD.get("Analysis")[:]

The post-processing scripts has to be modified.

Switching from 6.x to 6.y with y > x
++++++++++++++++++++++++++++++++++++

There is no known incompatibility for the ADAO case file. The upgrade procedure
is to read the old ADAO case file with the new SALOME/ADAO module, and save it
with a new name.

There is one incompatibility introduced for the operator script files, in the
naming of operators used to for the observation operator. The new mandatory
names are "*DirectOperator*", "*TangentOperator*" and "*AdjointOperator*", as
described in the last subsection of the chapter :ref:`section_reference`. The
operator script files has to be modified.

.. _subsection_version_compatibility:
.. index::
    pair: Version ; ADAO
    pair: Version ; SALOME
    pair: Version ; EFICAS
    pair: Version ; Python
    pair: Version ; Numpy
    pair: Version ; Scipy
    pair: Version ; MatplotLib
    pair: Version ; Gnuplot
    pair: Version ; NLopt

Versions of ADAO compatibility with support tools
-------------------------------------------------

The module benefits greatly from the **Python environment** [Python]_ and the
multiple features of this language, from the scientific calculation tools
included in **NumPy** [NumPy20]_, **SciPy** [SciPy20]_, **NLopt** [Johnson08]_
or in the tools that can be reached with them, and from the numerous
capabilities of **SALOME** [Salome]_ when used in combination.

.. include:: snippets/ModuleValidation.rst

.. include:: snippets/ModuleCompatibility.rst
