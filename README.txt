=====================================================
ADAO: A module for Data Assimilation and Optimization
=====================================================

About
-----

**The ADAO module provides data assimilation and optimization**
features in Python or SALOME context (see
http://www.salome-platform.org/). Briefly stated, Data Assimilation is
a methodological framework to compute the optimal estimate of the
inaccessible true value of a system state, eventually over time. It
uses information coming from experimental measurements or observations,
and from numerical *a priori* models, including information about their
errors. Parts of the framework are also known under the names of
*parameter estimation*, *inverse problems*, *Bayesian estimation*,
*optimal interpolation*, etc. More details can be found in the full
ADAO documentation (see http://www.salome-platform.org/).

Only the use of ADAO text programming interface (API/TUI) is introduced
here. This interface gives ability to create a calculation object in a
similar way than the case building obtained through the graphical
interface (GUI). When one wants to elaborate "by hand" the TUI
calculation case, it is recommended to extensively use all the ADAO
module documentation, and to go back if necessary to the graphical
interface (GUI), to get all the elements allowing to correctly set the
commands.

A simple setup example of an ADAO TUI calculation case
------------------------------------------------------

To introduce the TUI interface, lets begin by a simple but complete
example of ADAO calculation case. All the data are explicitly defined
inside the script in order to make the reading easier. The whole set of
commands is the following one::

    from numpy import array, matrix
    from adao import adaoBuilder
    case = adaoBuilder.New()
    case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
    case.set( 'Background',          Vector=[0, 1, 2] )
    case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
    case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
    case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
    case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
    case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
    case.execute()

The result of running these commands in SALOME (either as a SALOME
"*shell*" command, in the Python command window of the interface, or by
the script execution entry of the menu) is the following::

    Analysis [ 0.25000264  0.79999797  0.94999939]

More advanced examples of ADAO TUI calculation case
---------------------------------------------------

Real cases involves observations loaded from files, operators
explicitly defined as generic functions including physical simulators,
time dependant information in order to deal with forecast analysis in
addition to calibration or re-analysis. More details can be found in
the full ADAO documentation (see http://www.salome-platform.org/).

License and requirements
------------------------

The license for this module is the GNU Lesser General Public License
(Lesser GPL), as stated here and in the source files::

    <ADAO, a module for Data Assimilation and Optimization>

    Copyright (C) 2008-2020 EDF R&D

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

    See http://www.salome-platform.org/

In addition, we require that all publication or presentation describing
work using this software, or all commercial or not products using it,
quote at least one of the references given below:

    * *ADAO, a module for Data Assimilation and Optimization*,
      http://www.salome-platform.org/

    * *ADAO, un module pour l'Assimilation de Données et l'Aide à
      l'Optimisation*, http://www.salome-platform.org/

    * *SALOME The Open Source Integration Platform for Numerical Simulation*,
      http://www.salome-platform.org/

The documentation of the module is also covered by the license and the
requirement of quoting.
