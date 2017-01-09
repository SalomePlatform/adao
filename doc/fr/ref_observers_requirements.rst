..
   Copyright (C) 2008-2017 EDF R&D

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

Certaines variables sp�ciales, internes � l'optimisation, utilis�es au cours des
calculs, peuvent �tre surveill�es durant un calcul ADAO. Ces variables peuvent
�tre affich�es, trac�es, enregistr�es, etc. C'est r�alisable en utilisant des
"*observer*", parfois aussi appel�s des "callback". Ce sont des scripts Python,
qui sont chacun associ�s � une variable donn�e. Ils sont activ�s � chaque
modification de la variable.

Il y a 3 m�thodes pratiques pour int�grer un "*observer*" dans un cas ADAO. La
m�thode est choisie � l'aide du mot-cl� "*NodeType*" de chaque entr�e de type
"*observer*", comme montr� dans la figure qui suit :

  .. eficas_observer_nodetype:
  .. image:: images/eficas_observer_nodetype.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir pour un "*observer*" son type d'entr�e**

L'"*observer*" peut �tre fourni sous la forme d'un script explicite (entr�e de
type "*String*"), d'un script contenu dans un fichier externe (entr�e de type
"*Script*"), ou en utilisant un mod�le (entr�e de type "*Template*") fourni par
d�faut dans ADAO lors de l'usage de l'�diteur graphique. Ces derniers sont des
scripts simples qui peuvent �tre adapt�s par l'utilisateur, soit dans l'�tape
d'�dition int�gr�e du cas, soit dans l'�tape d'�dition du sch�ma avant
l'ex�cution, pour am�liorer la performance du calcul ADAO dans le superviseur
d'ex�cution de SALOME.

Forme g�n�rale d'un script permettant de d�finir un *observer*
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour pouvoir utiliser cette capacit�, l'utilisateur doit disposer ou construire
des scripts utilisant en entr�e standard (i.e. disponible dans l'espace de
nommage) les variables ``var`` et ``info``. La variable ``var`` est � utiliser
comme un objet de type liste/tuple, contenant la variable d'int�r�t indic�e par
l'�tape de mise � jour.

A titre d'exemple, voici un script tr�s simple (similaire au mod�le
"*ValuePrinter*"), utilisable pour afficher la valeur d'une variable
surveill�e::

    print "    --->",info," Value =",var[-1]

Stock�es comme un fichier Python ou une cha�ne de caract�res explicite, ces
lignes de script peuvent �tre associ�es � chaque variable pr�sente dans le
mot-cl� "*SELECTION*" de la commande "*Observers*" du cas ADAO : "*Analysis*",
"*CurrentState*", "*CostFunction*"... La valeur courante de la variable sera
affich�e � chaque �tape de l'algorithme d'optimisation ou d'assimilation. Les
"*observer*" peuvent inclure des capacit�s d'affichage graphique, de stockage,
de traitement complexe, d'analyse statistique, etc.

On donne ci-apr�s l'identifiant et le contenu de chaque mod�le disponible.

Inventaire des mod�les d'*observer* disponibles ("*Template*")
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ValuePrinter (Observer)

Mod�le **ValuePrinter** :
.........................

Imprime sur la sortie standard la valeur courante de la variable.

::

    print info, var[-1]

.. index:: single: ValueAndIndexPrinter (Observer)

Mod�le **ValueAndIndexPrinter** :
.................................

Imprime sur la sortie standard la valeur courante de la variable, en ajoutant son index.

::

    print str(info)+" index %i:"%(len(var)-1), var[-1]

.. index:: single: ValueSeriePrinter (Observer)

Mod�le **ValueSeriePrinter** :
..............................

Imprime sur la sortie standard la s�rie des valeurs de la variable.

::

    print info, var[:]

.. index:: single: ValueSaver (Observer)

Mod�le **ValueSaver** :
.......................

Enregistre la valeur courante de la variable dans un fichier du r�pertoire '/tmp' nomm� 'value...txt' selon le nom de la variable et l'�tape d'enregistrement.

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

Mod�le **ValueSerieSaver** :
............................

Enregistre la s�rie des valeurs de la variable dans un fichier du r�pertoire '/tmp' nomm� 'value...txt' selon le nom de la variable et l'�tape.

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

Mod�le **ValuePrinterAndSaver** :
.................................

Imprime sur la sortie standard et, en m�me temps enregistre dans un fichier, la valeur courante de la variable.

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

.. index:: single: ValueIndexPrinterAndSaver (Observer)

Mod�le **ValueIndexPrinterAndSaver** :
......................................

Imprime sur la sortie standard et, en m�me temps enregistre dans un fichier, la valeur courante de la variable, en ajoutant son index.

::

    import numpy, re
    v=numpy.array(var[-1], ndmin=1)
    print str(info)+" index %i:"%(len(var)-1),v
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

Mod�le **ValueSeriePrinterAndSaver** :
......................................

Imprime sur la sortie standard et, en m�me temps, enregistre dans un fichier la s�rie des valeurs de la variable.

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

Mod�le **ValueGnuPlotter** :
............................

Affiche graphiquement avec Gnuplot la valeur courante de la variable.

::

    import numpy, Gnuplot
    v=numpy.array(var[-1], ndmin=1)
    global ifig, gp
    try:
        ifig += 1
        gp(' set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp(' set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSerieGnuPlotter (Observer)

Mod�le **ValueSerieGnuPlotter** :
.................................

Affiche graphiquement avec Gnuplot la s�rie des valeurs de la variable.

::

    import numpy, Gnuplot
    v=numpy.array(var[:],  ndmin=1)
    global ifig, gp
    try:
        ifig += 1
        gp(' set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp(' set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValuePrinterAndGnuPlotter (Observer)

Mod�le **ValuePrinterAndGnuPlotter** :
......................................

Imprime sur la sortie standard et, en m�me temps, affiche graphiquement avec Gnuplot la valeur courante de la variable.

::

    print info, var[-1]
    import numpy, Gnuplot
    v=numpy.array(var[-1], ndmin=1)
    global ifig,gp
    try:
        ifig += 1
        gp(' set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp(' set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSeriePrinterAndGnuPlotter (Observer)

Mod�le **ValueSeriePrinterAndGnuPlotter** :
...........................................

Imprime sur la sortie standard et, en m�me temps, affiche graphiquement avec Gnuplot la s�rie des valeurs de la variable.

::

    print info, var[:] 
    import numpy, Gnuplot
    v=numpy.array(var[:],  ndmin=1)
    global ifig,gp
    try:
        ifig += 1
        gp(' set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp(' set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValuePrinterSaverAndGnuPlotter (Observer)

Mod�le **ValuePrinterSaverAndGnuPlotter** :
...........................................

Imprime sur la sortie standard et, en m�me temps, enregistre dans un fichier et affiche graphiquement la valeur courante de la variable .

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
        gp(' set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp(' set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSeriePrinterSaverAndGnuPlotter (Observer)

Mod�le **ValueSeriePrinterSaverAndGnuPlotter** :
................................................

Imprime sur la sortie standard et, en m�me temps, enregistre dans un fichier et affiche graphiquement la s�rie des valeurs de la variable.

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
        gp(' set style data lines')
    except:
        ifig = 0
        gp = Gnuplot.Gnuplot(persist=1)
        gp(' set style data lines')
    gp('set title  "%s (Figure %i)"'%(info,ifig))
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueMean (Observer)

Mod�le **ValueMean** :
......................

Imprime sur la sortie standard la moyenne de la valeur courante de la variable.

::

    import numpy
    print info, numpy.nanmean(var[-1])

.. index:: single: ValueStandardError (Observer)

Mod�le **ValueStandardError** :
...............................

Imprime sur la sortie standard l'�cart-type de la valeur courante de la variable.

::

    import numpy
    print info, numpy.nanstd(var[-1])

.. index:: single: ValueVariance (Observer)

Mod�le **ValueVariance** :
..........................

Imprime sur la sortie standard la variance de la valeur courante de la variable.

::

    import numpy
    print info, numpy.nanvar(var[-1])

.. index:: single: ValueL2Norm (Observer)

Mod�le **ValueL2Norm** :
........................

Imprime sur la sortie standard la norme L2 de la valeur courante de la variable.

::

    import numpy
    v = numpy.matrix( numpy.ravel( var[-1] ) )
    print info, float( numpy.linalg.norm(v) )

.. index:: single: ValueRMS (Observer)

Mod�le **ValueRMS** :
.....................

Imprime sur la sortie standard la racine de la moyenne des carr�s (RMS), ou moyenne quadratique, de la valeur courante de la variable.

::

    import numpy
    v = numpy.matrix( numpy.ravel( var[-1] ) )
    print info, float( numpy.sqrt((1./v.size)*(v*v.T)) )
