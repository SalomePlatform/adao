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

.. _ref_observers_requirements:

Requirements for functions describing an "*observer*"
-----------------------------------------------------

.. index:: single: Observer
.. index:: single: Observer Template

Some special variables, internal to the optimization process, used inside
calculation, can be monitored during an ADAO calculation. These variables can be
printed, plotted, saved, etc. It can be done using some "*observer*", sometimes
also called "callback". They are Python scripts, each one associated to a given
variable. They are activated for each variable modification.

There are 3 practical methods to provide an "*observer*" in an ADAO case. The
method is chosen with the "*NodeType*" keyword of each "*observer*" entry type, as
shown in the following figure:

  .. eficas_observer_nodetype:
  .. image:: images/eficas_observer_nodetype.png
    :align: center
    :width: 100%
  .. centered::
    **Choosing for an "*observer*" its entry type**

The "*observer*" can be given as a explicit script (entry of type "*String*"),
as a script in an external file (entry of type "*Script*"), or by using a
template or pattern (entry of type"*Template*") available by default in ADAO
when using the graphical editor. These templates are simple scripts that can be
tuned by the user, either in the integrated edtition stage of the case, or in
the edition stage of the schema before execution, to improve the ADAO case
performance in the SALOME execution supervisor.

General form of a script to define an *observer*
++++++++++++++++++++++++++++++++++++++++++++++++

To use this capability, the user must have or build scripts that have on
standard input (that is, in the naming space) the variables ``var`` and
``info``. The variable ``var`` is to be used as an object of list/tuple type,
that contains the variable of interest indexed by the updating step.

As an example, here is a very simple script (similar to the model
"*ValuePrinter*"), that can be used to print the value of the monitored
variable::

    print "    --->",info," Value =",var[-1]

Stored as a Python file or as an explicit string, these script lines can be
associated to each variable found in the keyword "*SELECTION*" of the
"*Observers*" command of the ADAO case: "*Analysis*", "*CurrentState*",
"*CostFunction*"... The current value of the variable will be printed at each
step of the optimization or data assimilation algorithm. The "*observer*" can
include graphical output, storage capacities, complex treatment, statistical
analysis, etc.

Hereinafter we give the identifier and the contents of each model available.

Inventory of available *observer* models ("*Template*")
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ValuePrinter (Observer)

Template **ValuePrinter** :
...........................

Print on standard output the current value of the variable.

::

    print info, var[-1]

.. index:: single: ValueSeriePrinter (Observer)

Template **ValueSeriePrinter** :
................................

Print on standard output the value serie of the variable.

::

    print info, var[:]

.. index:: single: ValueSaver (Observer)

Template **ValueSaver** :
.........................

Save the current value of the variable in a file of the '/tmp' directory named 'value...txt' from the variable name and the saving step.

::

    import numpy, re
    v=numpy.array(var[-1], ndmin=1)
    global istep
    try:
        istep += 1
    except:
        istep = 0
    f='/tmp/value_%s_%05i.txt'%(info,istep)
    f=re.sub('\s','_',f)
    print 'Value saved in "%s"'%f
    numpy.savetxt(f,v)

.. index:: single: ValueSerieSaver (Observer)

Template **ValueSerieSaver** :
..............................

Save the value serie of the variable in a file of the '/tmp' directory named 'value...txt' from the variable name and the saving step.

::

    import numpy, re
    v=numpy.array(var[:],  ndmin=1)
    global istep
    try:
        istep += 1
    except:
        istep = 0
    f='/tmp/value_%s_%05i.txt'%(info,istep)
    f=re.sub('\s','_',f)
    print 'Value saved in "%s"'%f
    numpy.savetxt(f,v)

.. index:: single: ValuePrinterAndSaver (Observer)

Template **ValuePrinterAndSaver** :
...................................

Print on standard output and, in the same time, save in a file the current value of the variable.

::

    import numpy, re
    v=numpy.array(var[-1], ndmin=1)
    print info,v
    global istep
    try:
        istep += 1
    except:
        istep = 0
    f='/tmp/value_%s_%05i.txt'%(info,istep)
    f=re.sub('\s','_',f)
    print 'Value saved in "%s"'%f
    numpy.savetxt(f,v)

.. index:: single: ValueSeriePrinterAndSaver (Observer)

Template **ValueSeriePrinterAndSaver** :
........................................

Print on standard output and, in the same time, save in a file the value serie of the variable.

::

    import numpy, re
    v=numpy.array(var[:],  ndmin=1)
    print info,v
    global istep
    try:
        istep += 1
    except:
        istep = 0
    f='/tmp/value_%s_%05i.txt'%(info,istep)
    f=re.sub('\s','_',f)
    print 'Value saved in "%s"'%f
    numpy.savetxt(f,v)

.. index:: single: ValueGnuPlotter (Observer)

Template **ValueGnuPlotter** :
..............................

Graphically plot with Gnuplot the current value of the variable.

::

    import numpy, Gnuplot
    v=numpy.array(var[-1], ndmin=1)
    global ifig, gp
    try:
        ifig += 1
        gp('set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp('set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSerieGnuPlotter (Observer)

Template **ValueSerieGnuPlotter** :
...................................

Graphically plot with Gnuplot the value serie of the variable.

::

    import numpy, Gnuplot
    v=numpy.array(var[:],  ndmin=1)
    global ifig, gp
    try:
        ifig += 1
        gp('set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp('set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValuePrinterAndGnuPlotter (Observer)

Template **ValuePrinterAndGnuPlotter** :
........................................

Print on standard output and, in the same time, graphically plot with Gnuplot the current value of the variable.

::

    print info, var[-1]
    import numpy, Gnuplot
    v=numpy.array(var[-1], ndmin=1)
    global ifig,gp
    try:
        ifig += 1
        gp('set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp('set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSeriePrinterAndGnuPlotter (Observer)

Template **ValueSeriePrinterAndGnuPlotter** :
.............................................

Print on standard output and, in the same time, graphically plot with Gnuplot the value serie of the variable.

::

    print info, var[:] 
    import numpy, Gnuplot
    v=numpy.array(var[:],  ndmin=1)
    global ifig,gp
    try:
        ifig += 1
        gp('set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp('set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValuePrinterSaverAndGnuPlotter (Observer)

Template **ValuePrinterSaverAndGnuPlotter** :
.............................................

Print on standard output and, in the same, time save in a file and graphically plot the current value of the variable.

::

    print info, var[-1]
    import numpy, re
    v=numpy.array(var[-1], ndmin=1)
    global istep
    try:
        istep += 1
    except:
        istep = 0
    f='/tmp/value_%s_%05i.txt'%(info,istep)
    f=re.sub('\s','_',f)
    print 'Value saved in "%s"'%f
    numpy.savetxt(f,v)
    import Gnuplot
    global ifig,gp
    try:
        ifig += 1
        gp('set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp('set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSeriePrinterSaverAndGnuPlotter (Observer)

Template **ValueSeriePrinterSaverAndGnuPlotter** :
..................................................

Print on standard output and, in the same, time save in a file and graphically plot the value serie of the variable.

::

    print info, var[:] 
    import numpy, re
    v=numpy.array(var[:],  ndmin=1)
    global istep
    try:
        istep += 1
    except:
        istep = 0
    f='/tmp/value_%s_%05i.txt'%(info,istep)
    f=re.sub('\s','_',f)
    print 'Value saved in "%s"'%f
    numpy.savetxt(f,v)
    import Gnuplot
    global ifig,gp
    try:
        ifig += 1
        gp('set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp('set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueMean (Observer)

Template **ValueMean** :
........................

Print on standard output the mean of the current value of the variable.

::

    import numpy
    print info, numpy.nanmean(var[-1])

.. index:: single: ValueStandardError (Observer)

Template **ValueStandardError** :
.................................

Print on standard output the standard error of the current value of the variable.

::

    import numpy
    print info, numpy.nanstd(var[-1])

.. index:: single: ValueVariance (Observer)

Template **ValueVariance** :
............................

Print on standard output the variance of the current value of the variable.

::

    import numpy
    print info, numpy.nanvar(var[-1])

.. index:: single: ValueRMS (Observer)

Template **ValueRMS** :
.......................

Print on standard output the root mean square (RMS), or quadratic mean, of the current value of the variable.

::

    import numpy
    v = numpy.matrix( numpy.ravel( var[-1] ) )
    print info, float( numpy.sqrt((1./v.size)*(v*v.T)) )