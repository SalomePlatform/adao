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

Exigences pour les fonctions d�crivant un "*observer*"
------------------------------------------------------

.. index:: single: Observer
.. index:: single: Observer Template

Certaines variables sp�ciales internes � l'optimisation, utilis�es au cours des
calculs, peuvent �tre surveill�es durant un calcul ADAO en YACS. Ces variables
peuvent �tre affich�es, trac�es, enregistr�es, etc. C'est r�alisable en
utilisant des "*observer*", qui sont des scripts, chacun associ� � une
variable, qui sont activ�s � chaque modification de la variable.

Il y a 3 m�thodes pratiques pour int�grer un "*observer*" dans un cas ADAO. La
m�thode est choisie � l'aide du mot-cl� "*NodeType*" de chaque entr�e de type
*observer*, comme montr� dans la figure qui suit :

  .. eficas_observer_nodetype:
  .. image:: images/eficas_observer_nodetype.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir le type d'entr�e**

L'"*observer*" peut �tre fourni sous la forme d'un script explicite (entr�e de
type "*String*"), d'un script contenu dans un fichier externe (entr�e de type
"*Script*"), ou en utilisant un mod�le (entr�e de type "*Template*") fourni par
d�faut dans ADAO lors de l'�dition dans l'�diteur graphique. Ces derniers sont
des scripts simples qui peuvent �tre adapt�s par l'utilisateur, soit dans
l'�tape d'�dition int�gr�e, soit dans l'�tape d'�dition avant l'ex�cution, pour
am�liorer l'adaptation du calcul ADAO dans le superviseur d'ex�cution de SALOME.

Forme g�n�rale d'un script permettant de d�finir un  *observer*
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour pouvoir utiliser cette capacit�, l'utilisateur doit disposer ou construire
des scripts utilisant en entr�e standard (i.e. disponible dans l'espace de
nommage) des variables ``var`` et ``info``. La variable ``var`` est � utiliser
comme un objet de type liste/tuple, contenant la variable d'int�r�t indic�e par
l'�tape de mise � jour.

A titre d'exemple, voici un script tr�s simple (similaire au mod�le
"*ValuePrinter*") utilisable pour afficher la valeur d'une variable surveill�e::

    print "    --->",info," Value =",var[-1]

Stock� comme un fichier Python, ce script peut �tre associ� � chaque variable
pr�sente dans le mot-cl� "*SELECTION*" de la commande "*Observers*":
"*Analysis*", "*CurrentState*", "*CostFunction*"... La valeur courante de la
variable sera affich�e � chaque �tape de l'algorithme d'optimisation ou
d'assimilation. Les "*observer*" peuvent inclure des capacit�s d'affichage
graphique, de stockage, d'affichage complexe, de traitement statistique, etc.

On donne ci-apr�s l'identifiant et le contenu de chaque mod�le disponible.

Inventaire des mod�les d'*observer* disponibles ("*Template*")
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ValueGnuPlotter (Observer)

Mod�le **ValueGnuPlotter** :
............................

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

.. index:: single: ValueMean (Observer)

Mod�le **ValueMean** :
......................

::

    import numpy
    print info, numpy.nanmean(var[-1])

.. index:: single: ValuePrinter (Observer)

Mod�le **ValuePrinter** :
.........................

Imprime sur la sortie standard la valeur courante de la variable.

::

    print info, var[-1]

.. index:: single: ValuePrinterAndGnuPlotter (Observer)

Mod�le **ValuePrinterAndGnuPlotter** :
......................................

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

.. index:: single: ValuePrinterAndSaver (Observer)

Mod�le **ValuePrinterAndSaver** :
.................................

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

.. index:: single: ValuePrinterSaverAndGnuPlotter (Observer)

Mod�le **ValuePrinterSaverAndGnuPlotter** :
...........................................

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

.. index:: single: ValueRMS (Observer)

Mod�le **ValueRMS** :
.....................

::

    import numpy
    v = numpy.matrix( numpy.ravel( var[-1] ) )
    print info, float( numpy.sqrt((1./v.size)*(v*v.T)) )

.. index:: single: ValueSaver (Observer)

Mod�le **ValueSaver** :
.......................

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

.. index:: single: ValueSerieGnuPlotter (Observer)

Mod�le **ValueSerieGnuPlotter** :
.................................

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

.. index:: single: ValueSeriePrinter (Observer)

Mod�le **ValueSeriePrinter** :
..............................

Imprime sur la sortie standard la s�rie des valeurs de la variable.

::

    print info, var[:]

.. index:: single: ValueSeriePrinterAndGnuPlotter (Observer)

Mod�le **ValueSeriePrinterAndGnuPlotter** :
...........................................

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

.. index:: single: ValueSeriePrinterAndSaver (Observer)

Mod�le **ValueSeriePrinterAndSaver** :
......................................

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

.. index:: single: ValueSeriePrinterSaverAndGnuPlotter (Observer)

Mod�le **ValueSeriePrinterSaverAndGnuPlotter** :
................................................

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

.. index:: single: ValueSerieSaver (Observer)

Mod�le **ValueSerieSaver** :
............................

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

.. index:: single: ValueStandardError (Observer)

Mod�le **ValueStandardError** :
...............................

::

    import numpy
    print info, numpy.nanstd(var[-1])

.. index:: single: ValueVariance (Observer)

Mod�le **ValueVariance** :
..........................

::

    import numpy
    print info, numpy.nanvar(var[-1])
