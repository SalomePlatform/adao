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

Exigences pour les fonctions décrivant un "*observer*"
------------------------------------------------------

.. index:: single: Observer
.. index:: single: Observer Template

Certaines variables spéciales, internes à l'optimisation, utilisées au cours des
calculs, peuvent être surveillées durant un calcul ADAO. Ces variables peuvent
être affichées, tracées, enregistrées, etc. C'est réalisable en utilisant des
"*observer*", parfois aussi appelés des "callback". Ce sont des scripts Python,
qui sont chacun associés à une variable donnée. Ils sont activés à chaque
modification de la variable.

Il y a 3 méthodes pratiques pour intégrer un "*observer*" dans un cas ADAO. La
méthode est choisie à l'aide du mot-clé "*NodeType*" de chaque entrée de type
"*observer*", comme montré dans la figure qui suit :

  .. eficas_observer_nodetype:
  .. image:: images/eficas_observer_nodetype.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir pour un "*observer*" son type d'entrée**

L'"*observer*" peut être fourni sous la forme d'un script explicite (entrée de
type "*String*"), d'un script contenu dans un fichier externe (entrée de type
"*Script*"), ou en utilisant un modèle (entrée de type "*Template*") fourni par
défaut dans ADAO lors de l'usage de l'éditeur graphique. Ces derniers sont des
scripts simples qui peuvent être adaptés par l'utilisateur, soit dans l'étape
d'édition intégrée du cas, soit dans l'étape d'édition du schéma avant
l'exécution, pour améliorer la performance du calcul ADAO dans le superviseur
d'exécution de SALOME.

Forme générale d'un script permettant de définir un *observer*
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour pouvoir utiliser cette capacité, l'utilisateur doit disposer ou construire
des scripts utilisant en entrée standard (i.e. disponible dans l'espace de
nommage) les variables ``var`` et ``info``. La variable ``var`` est à utiliser
comme un objet de type liste/tuple, contenant la variable d'intérêt indicée par
l'étape de mise à jour.

A titre d'exemple, voici un script très simple (similaire au modèle
"*ValuePrinter*"), utilisable pour afficher la valeur d'une variable
surveillée::

    print "    --->",info," Value =",var[-1]

Stockées comme un fichier Python ou une chaîne de caractères explicite, ces
lignes de script peuvent être associées à chaque variable présente dans le
mot-clé "*SELECTION*" de la commande "*Observers*" du cas ADAO : "*Analysis*",
"*CurrentState*", "*CostFunction*"... La valeur courante de la variable sera
affichée à chaque étape de l'algorithme d'optimisation ou d'assimilation. Les
"*observer*" peuvent inclure des capacités d'affichage graphique, de stockage,
de traitement complexe, d'analyse statistique, etc.

On donne ci-après l'identifiant et le contenu de chaque modèle disponible.

Inventaire des modèles d'*observer* disponibles ("*Template*")
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ValuePrinter (Observer)

Modèle **ValuePrinter** :
.........................

Imprime sur la sortie standard la valeur courante de la variable.

::

    print info, var[-1]

.. index:: single: ValueAndIndexPrinter (Observer)

Modèle **ValueAndIndexPrinter** :
.................................

Imprime sur la sortie standard la valeur courante de la variable, en ajoutant son index.

::

    print str(info)+" index %i:"%(len(var)-1), var[-1]

.. index:: single: ValueSeriePrinter (Observer)

Modèle **ValueSeriePrinter** :
..............................

Imprime sur la sortie standard la série des valeurs de la variable.

::

    print info, var[:]

.. index:: single: ValueSaver (Observer)

Modèle **ValueSaver** :
.......................

Enregistre la valeur courante de la variable dans un fichier du répertoire '/tmp' nommé 'value...txt' selon le nom de la variable et l'étape d'enregistrement.

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

Modèle **ValueSerieSaver** :
............................

Enregistre la série des valeurs de la variable dans un fichier du répertoire '/tmp' nommé 'value...txt' selon le nom de la variable et l'étape.

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

Modèle **ValuePrinterAndSaver** :
.................................

Imprime sur la sortie standard et, en même temps enregistre dans un fichier, la valeur courante de la variable.

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

Modèle **ValueIndexPrinterAndSaver** :
......................................

Imprime sur la sortie standard et, en même temps enregistre dans un fichier, la valeur courante de la variable, en ajoutant son index.

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

Modèle **ValueSeriePrinterAndSaver** :
......................................

Imprime sur la sortie standard et, en même temps, enregistre dans un fichier la série des valeurs de la variable.

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

Modèle **ValueGnuPlotter** :
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

Modèle **ValueSerieGnuPlotter** :
.................................

Affiche graphiquement avec Gnuplot la série des valeurs de la variable.

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

Modèle **ValuePrinterAndGnuPlotter** :
......................................

Imprime sur la sortie standard et, en même temps, affiche graphiquement avec Gnuplot la valeur courante de la variable.

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

Modèle **ValueSeriePrinterAndGnuPlotter** :
...........................................

Imprime sur la sortie standard et, en même temps, affiche graphiquement avec Gnuplot la série des valeurs de la variable.

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

Modèle **ValuePrinterSaverAndGnuPlotter** :
...........................................

Imprime sur la sortie standard et, en même temps, enregistre dans un fichier et affiche graphiquement la valeur courante de la variable .

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

Modèle **ValueSeriePrinterSaverAndGnuPlotter** :
................................................

Imprime sur la sortie standard et, en même temps, enregistre dans un fichier et affiche graphiquement la série des valeurs de la variable.

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

Modèle **ValueMean** :
......................

Imprime sur la sortie standard la moyenne de la valeur courante de la variable.

::

    import numpy
    print info, numpy.nanmean(var[-1])

.. index:: single: ValueStandardError (Observer)

Modèle **ValueStandardError** :
...............................

Imprime sur la sortie standard l'écart-type de la valeur courante de la variable.

::

    import numpy
    print info, numpy.nanstd(var[-1])

.. index:: single: ValueVariance (Observer)

Modèle **ValueVariance** :
..........................

Imprime sur la sortie standard la variance de la valeur courante de la variable.

::

    import numpy
    print info, numpy.nanvar(var[-1])

.. index:: single: ValueL2Norm (Observer)

Modèle **ValueL2Norm** :
........................

Imprime sur la sortie standard la norme L2 de la valeur courante de la variable.

::

    import numpy
    v = numpy.matrix( numpy.ravel( var[-1] ) )
    print info, float( numpy.linalg.norm(v) )

.. index:: single: ValueRMS (Observer)

Modèle **ValueRMS** :
.....................

Imprime sur la sortie standard la racine de la moyenne des carrés (RMS), ou moyenne quadratique, de la valeur courante de la variable.

::

    import numpy
    v = numpy.matrix( numpy.ravel( var[-1] ) )
    print info, float( numpy.sqrt((1./v.size)*(v*v.T)) )
