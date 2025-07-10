..
   Copyright (C) 2008-2025 EDF R&D

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

.. _section_ref_observers_requirements:

Conditions requises pour les fonctions décrivant un "*observer*"
----------------------------------------------------------------

.. index:: single: Observer
.. index:: single: setObserver
.. index:: single: Observer Template

Certaines variables spéciales, internes à l'optimisation et utilisées au cours
des calculs, peuvent être surveillées durant un calcul ADAO. Ces variables
peuvent être affichées, tracées, enregistrées, etc. par l'utilisateur. C'est
réalisable en utilisant des "*observer*", parfois aussi appelés des "callback",
sur une variable. Ce sont des fonctions Python spéciales, qui sont chacune
associées à une variable donnée, comme décrit conceptuellement dans la figure
suivante :

  .. ref_observer_simple:
  .. image:: images/ref_observer_simple.png
    :align: center
    :width: 75%
  .. centered::
    **Définition conceptuelle d'une fonction "observer"**

Ces fonctions "*observer*" sont décrites dans les sous-sections suivantes.

Enregistrer et activer une fonction "*observer*"
++++++++++++++++++++++++++++++++++++++++++++++++

Dans l'interface graphique EFICAS d'ADAO, il y a 3 méthodes pratiques pour
intégrer une fonction "*observer*" dans un cas ADAO. La méthode est choisie à
l'aide du mot-clé "*NodeType*" de chaque entrée de type "*observer*", comme
montré dans la figure qui suit :

  .. eficas_observer_nodetype:
  .. image:: images/eficas_observer_nodetype.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir son type d'entrée pour une fonction "observer"**

Une fonction "*observer*" peut être fourni sous la forme d'un script explicite
(entrée de type "*String*"), d'un script contenu dans un fichier externe
(entrée de type "*Script*"), ou en utilisant un modèle (entrée de type
"*Template*"). Les modèles sont fournis par défaut dans ADAO, lors de l'usage
de l'éditeur graphique EFICAS d'ADAO ou de l'interface TUI, et sont détaillés
dans la partie :ref:`section_ref_observers_templates` qui suit. Ces derniers
sont des scripts simples qui peuvent être adaptés par l'utilisateur, soit dans
l'étape d'édition intégrée du cas avec EFICAS d'ADAO, soit dans l'étape
d'édition du schéma avant l'exécution, pour améliorer la performance du calcul
ADAO dans le superviseur d'exécution de SALOME.

Dans l'interface textuelle (TUI) d'ADAO (voir la partie :ref:`section_tui`),
les mêmes informations peuvent être données à l'aide de la commande
"*setObserver*" appliquée pour une variable donnée indiquée en utilisant
l'argument "*Variable*". Les autres arguments de cette commande permettent de
définir un "*observer*" soit comme un modèle (argument "*Template*") désignant
l'un des scripts détaillés dans la partie
:ref:`section_ref_observers_templates`, soit comme un script explicite
(argument "*String*"), soit comme un script contenu dans un fichier externe
(argument "*Script*").

Forme générale d'un script permettant de définir une fonction "*observer*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Une fonction "*observer*" est un script Python spécial, associé à une variable
donnée, et qui est automatiquement activée à chaque modification de la variable
lors du calcul. Chaque fonction (soigneusement établie) qui s'applique à la
variable sélectionnée peut être utilisée. De nombreuses fonctions "*observer*"
sont disponibles par défaut.

Pour pouvoir utiliser directement cette capacité "*observer*", l'utilisateur
doit utiliser ou construire un script utilisant en entrée standard (i.e.
disponible dans l'espace de nommage) les variables ``var`` et ``info``. La
variable ``var`` est à utiliser comme un objet de type liste/tuple, contenant
l'historique de la variable d'intérêt, indicé par les pas d'itérations et/ou de
temps. Seul le corps de la fonction "*observer*" doit être spécifié par
l'utilisateur, pas l'appel Python ``def`` de fonction lui-même.

A titre d'exemple, voici un script très simple (similaire au modèle
"*ValuePrinter*"), utilisable pour afficher la valeur d'une variable
surveillée :
::

    print("    --->",info," Value =",var[-1])

Stockées comme un fichier Python ou une chaîne de caractères explicite, cette
ou ces lignes de script peuvent être associées à chaque variable présente dans
le mot-clé "*SELECTION*" de la commande "*Observers*" du cas ADAO :
"*Analysis*", "*CurrentState*", "*CostFunction*"... La valeur courante de la
variable sera par exemple affichée à chaque étape de l'algorithme
d'optimisation ou d'assimilation. Les "*observer*" peuvent inclure des
capacités d'affichage graphique, de stockage, de traitement complexe, d'analyse
statistique, etc. Si une variable, à laquelle est lié un "*observer*", n'est
pas requise dans le calcul et par l'utilisateur, l'exécution de cet
"*observer*" n'est tout simplement jamais activée.

.. warning::

    Si les modèles disponibles par défaut ne sont pas utilisés, il revient à
    l'utilisateur de faire des scripts de fonctions soigneusement établis ou
    des programmes externes qui ne se plantent pas avant d'être enregistrés
    comme une fonction "*observer*". Le débogage peut sinon être vraiment
    difficile !

Certains "*observer*" permettent de créer des fichiers ou des figures
successives, qui sont numérotées de manière unique et, le cas échéant,
enregistrées par défaut dans un répertoire temporaire standard ``/tmp`` ou
obtenu par le module Python ``tempfile``. Dans le cas où ces informations sont
à modifier (comme par exemple lorsque le répertoire temporaire est un dossier
virtuel ou local non pérenne, ou lorsque l'on désire une numérotation en
fonction de l'itération comme dans certains exemples), l'utilisateur est invité
à s'inspirer d'un modèle lui convenant pour le modifier en spécifiant
différemment ces informations communes. Ensuite, la fonction modifiée peut être
utilisée dans une entrée de type "*String*" ou de type "*Script*".

.. note::

    Une partie des "*observer*" permet de créer des figures en utilisant le
    module Python intégré Gnuplot.py [Gnuplot.py]_, ici mis à jour pour
    supporter Python 3. Ce module est une interface de contrôle et de
    transmission d'arguments au remarquable utilitaire classique de tracé
    graphique Gnuplot [Gnuplot]_. Disponible pour la grande majorité des
    environnements, ce dernier est indépendant et doit être correctement
    préinstallé.

On donne ci-après l'identifiant et le contenu de tous les modèles "*observer*"
disponibles.

.. _section_ref_observers_templates:

Inventaire des modèles de fonctions "*observer*" disponibles ("*Template*")
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ValuePrinter (Observer)

Modèle **ValuePrinter**
.......................

Imprime sur la sortie standard la valeur courante de la variable.

::

    print(str(info)+" "+str(var[-1]))

.. index:: single: ValueAndIndexPrinter (Observer)

Modèle **ValueAndIndexPrinter**
...............................

Imprime sur la sortie standard la valeur courante de la variable, en ajoutant son index.

::

    print(str(info)+(" index %i:"%(len(var)-1))+" "+str(var[-1]))

.. index:: single: ValueSeriePrinter (Observer)

Modèle **ValueSeriePrinter**
............................

Imprime sur la sortie standard la série des valeurs de la variable.

::

    print(str(info)+" "+str(var[:]))

.. index:: single: ValueSaver (Observer)

Modèle **ValueSaver**
.....................

Enregistre la valeur courante de la variable dans un fichier situé dans le répertoire temporaire du système nommé 'value...txt' selon le nom de la variable et l'étape d'enregistrement.

::

    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    v=numpy.array(var[-1], ndmin=1)
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)

.. index:: single: ValueSerieSaver (Observer)

Modèle **ValueSerieSaver**
..........................

Enregistre la série des valeurs de la variable dans un fichier situé dans le répertoire temporaire du système nommé 'value...txt' selon le nom de la variable et l'étape.

::

    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    v=numpy.array(var[:], ndmin=1)
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)

.. index:: single: ValuePrinterAndSaver (Observer)

Modèle **ValuePrinterAndSaver**
...............................

Imprime sur la sortie standard et, en même temps enregistre dans un fichier situé dans le répertoire temporaire du système, la valeur courante de la variable.

::

    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    v=numpy.array(var[-1], ndmin=1)
    print(str(info)+" "+str(v))
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)

.. index:: single: ValueIndexPrinterAndSaver (Observer)

Modèle **ValueIndexPrinterAndSaver**
....................................

Imprime sur la sortie standard et, en même temps enregistre dans un fichier situé dans le répertoire temporaire du système, la valeur courante de la variable, en ajoutant son index.

::

    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    v=numpy.array(var[-1], ndmin=1)
    print(str(info)+(" index %i:"%(len(var)-1))+" "+str(v))
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)

.. index:: single: ValueSeriePrinterAndSaver (Observer)

Modèle **ValueSeriePrinterAndSaver**
....................................

Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système, la série des valeurs de la variable.

::

    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    v=numpy.array(var[:], ndmin=1)
    print(str(info)+" "+str(v))
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)

.. index:: single: ValueGnuPlotter (Observer)

Modèle **ValueGnuPlotter**
..........................

Affiche graphiquement avec Gnuplot la valeur courante de la variable (affichage persistant).

::

    import numpy, Gnuplot
    v=numpy.array(var[-1], ndmin=1)
    global igfig, gp
    try:
        igfig+=1
        gp('set title "%s (Figure %i)"'%(info,igfig))
    except:
        igfig=0
        gp=Gnuplot.Gnuplot(persist=1)
        gp('set title "%s (Figure %i)"'%(info,igfig))
        gp('set style data lines')
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSerieGnuPlotter (Observer)

Modèle **ValueSerieGnuPlotter**
...............................

Affiche graphiquement avec Gnuplot la série des valeurs de la variable (affichage persistant).

::

    import numpy, Gnuplot
    v=numpy.array(var[:], ndmin=1)
    global igfig, gp
    try:
        igfig+=1
        gp('set title "%s (Figure %i)"'%(info,igfig))
    except:
        igfig=0
        gp=Gnuplot.Gnuplot(persist=1)
        gp('set title "%s (Figure %i)"'%(info,igfig))
        gp('set style data lines')
        gp('set xlabel "Step"')
        gp('set ylabel "Variable"')
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValuePrinterAndGnuPlotter (Observer)

Modèle **ValuePrinterAndGnuPlotter**
....................................

Imprime sur la sortie standard et, en même temps, affiche graphiquement avec Gnuplot la valeur courante de la variable (affichage persistant).

::

    print(str(info)+' '+str(var[-1]))
    import numpy, Gnuplot
    v=numpy.array(var[-1], ndmin=1)
    global igfig, gp
    try:
        igfig+=1
        gp('set title "%s (Figure %i)"'%(info,igfig))
    except:
        igfig=0
        gp=Gnuplot.Gnuplot(persist=1)
        gp('set title "%s (Figure %i)"'%(info,igfig))
        gp('set style data lines')
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSeriePrinterAndGnuPlotter (Observer)

Modèle **ValueSeriePrinterAndGnuPlotter**
.........................................

Imprime sur la sortie standard et, en même temps, affiche graphiquement avec Gnuplot la série des valeurs de la variable (affichage persistant).

::

    print(str(info)+' '+str(var[:]))
    import numpy, Gnuplot
    v=numpy.array(var[:], ndmin=1)
    global igfig, gp
    try:
        igfig+=1
        gp('set title "%s (Figure %i)"'%(info,igfig))
    except:
        igfig=0
        gp=Gnuplot.Gnuplot(persist=1)
        gp('set title "%s (Figure %i)"'%(info,igfig))
        gp('set style data lines')
        gp('set xlabel "Step"')
        gp('set ylabel "Variable"')
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValuePrinterSaverAndGnuPlotter (Observer)

Modèle **ValuePrinterSaverAndGnuPlotter**
.........................................

Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système et affiche graphiquement avec Gnuplot la valeur courante de la variable (affichage persistant).

::

    print(str(info)+' '+str(var[-1]))
    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    v=numpy.array(var[-1], ndmin=1)
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)
    import Gnuplot
    global igfig, gp
    try:
        igfig+=1
        gp('set title "%s (Figure %i)"'%(info,igfig))
    except:
        igfig=0
        gp=Gnuplot.Gnuplot(persist=1)
        gp('set title "%s (Figure %i)"'%(info,igfig))
        gp('set style data lines')
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueSeriePrinterSaverAndGnuPlotter (Observer)

Modèle **ValueSeriePrinterSaverAndGnuPlotter**
..............................................

Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système et affiche graphiquement avec Gnuplot la série des valeurs de la variable (affichage persistant).

::

    print(str(info)+' '+str(var[:]))
    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    v=numpy.array(var[:], ndmin=1)
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)
    import Gnuplot
    global igfig, gp
    try:
        igfig+=1
        gp('set title "%s (Figure %i)"'%(info,igfig))
    except:
        igfig=0
        gp=Gnuplot.Gnuplot(persist=1)
        gp('set title "%s (Figure %i)"'%(info,igfig))
        gp('set style data lines')
        gp('set xlabel "Step"')
        gp('set ylabel "Variable"')
    gp.plot( Gnuplot.Data( v, with_='lines lw 2' ) )

.. index:: single: ValueMatPlotter (Observer)

Modèle **ValueMatPlotter**
..........................

Affiche graphiquement avec Matplolib la valeur courante de la variable (affichage non persistant).

::

    import numpy
    import matplotlib.pyplot as plt
    v=numpy.array(var[-1], ndmin=1)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    ax.plot(v)
    plt.show()

.. index:: single: ValueMatPlotterSaver (Observer)

Modèle **ValueMatPlotterSaver**
...............................

Affiche graphiquement avec Matplolib la valeur courante de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant).

::

    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    import matplotlib.pyplot as plt
    v=numpy.array(var[-1], ndmin=1)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    ax.plot(v)
    f=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))
    f=re.sub(r'\s','_',f)
    plt.savefig(f)
    plt.show()

.. index:: single: ValueSerieMatPlotter (Observer)

Modèle **ValueSerieMatPlotter**
...............................

Affiche graphiquement avec Matplolib la série des valeurs de la variable (affichage non persistant).

::

    import numpy
    import matplotlib.pyplot as plt
    v=numpy.array(var[:], ndmin=1)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
        ax.set_xlabel('Step')
        ax.set_ylabel('Variable')
    ax.plot(v)
    plt.show()

.. index:: single: ValueSerieMatPlotterSaver (Observer)

Modèle **ValueSerieMatPlotterSaver**
....................................

Affiche graphiquement avec Matplolib la série des valeurs de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant).

::

    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    import matplotlib.pyplot as plt
    v=numpy.array(var[:], ndmin=1)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
        ax.set_xlabel('Step')
        ax.set_ylabel('Variable')
    ax.plot(v)
    f=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))
    f=re.sub(r'\s','_',f)
    plt.savefig(f)
    plt.show()

.. index:: single: ValuePrinterAndMatPlotter (Observer)

Modèle **ValuePrinterAndMatPlotter**
....................................

Affiche graphiquement avec Matplolib la valeur courante de la variable (affichage non persistant).

::

    print(str(info)+' '+str(var[-1]))
    import numpy
    import matplotlib.pyplot as plt
    v=numpy.array(var[-1], ndmin=1)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    ax.plot(v)
    plt.show()

.. index:: single: ValuePrinterAndMatPlotterSaver (Observer)

Modèle **ValuePrinterAndMatPlotterSaver**
.........................................

Affiche graphiquement avec Matplolib la valeur courante de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant).

::

    print(str(info)+' '+str(var[-1]))
    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    import matplotlib.pyplot as plt
    v=numpy.array(var[-1], ndmin=1)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    ax.plot(v)
    f=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))
    f=re.sub(r'\s','_',f)
    plt.savefig(f)
    plt.show()

.. index:: single: ValueSeriePrinterAndMatPlotter (Observer)

Modèle **ValueSeriePrinterAndMatPlotter**
.........................................

Affiche graphiquement avec Matplolib la série des valeurs de la variable (affichage non persistant).

::

    print(str(info)+' '+str(var[:]))
    import numpy
    import matplotlib.pyplot as plt
    v=numpy.array(var[:], ndmin=1)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
        ax.set_xlabel('Step')
        ax.set_ylabel('Variable')
    ax.plot(v)
    plt.show()

.. index:: single: ValueSeriePrinterAndMatPlotterSaver (Observer)

Modèle **ValueSeriePrinterAndMatPlotterSaver**
..............................................

Affiche graphiquement avec Matplolib la série des valeurs de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant).

::

    print(str(info)+' '+str(var[:]))
    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    import matplotlib.pyplot as plt
    v=numpy.array(var[:], ndmin=1)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
        ax.set_xlabel('Step')
        ax.set_ylabel('Variable')
    ax.plot(v)
    f=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))
    f=re.sub(r'\s','_',f)
    plt.savefig(f)
    plt.show()

.. index:: single: ValuePrinterSaverAndMatPlotter (Observer)

Modèle **ValuePrinterSaverAndMatPlotter**
.........................................

Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système et affiche graphiquement avec Matplolib la valeur courante de la variable (affichage non persistant).

::

    print(str(info)+' '+str(var[-1]))
    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    import matplotlib.pyplot as plt
    v=numpy.array(var[-1], ndmin=1)
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    ax.plot(v)
    plt.show()

.. index:: single: ValuePrinterSaverAndMatPlotterSaver (Observer)

Modèle **ValuePrinterSaverAndMatPlotterSaver**
..............................................

Imprime sur la sortie standard et, en même temps, enregistre dans un fichier situé dans le répertoire temporaire du système et affiche graphiquement avec Matplolib la valeur courante de la variable (affichage non persistant et sauvegardé).

::

    print(str(info)+' '+str(var[-1]))
    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    import matplotlib.pyplot as plt
    v=numpy.array(var[-1], ndmin=1)
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    ax.plot(v)
    f=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))
    f=re.sub(r'\s','_',f)
    plt.savefig(f)
    plt.show()

.. index:: single: ValueSeriePrinterSaverAndMatPlotter (Observer)

Modèle **ValueSeriePrinterSaverAndMatPlotter**
..............................................

Affiche graphiquement avec Matplolib la série des valeurs de la variable (affichage non persistant).

::

    print(str(info)+' '+str(var[:]))
    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    import matplotlib.pyplot as plt
    v=numpy.array(var[:], ndmin=1)
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
        ax.set_xlabel('Step')
        ax.set_ylabel('Variable')
    ax.plot(v)
    plt.show()

.. index:: single: ValueSeriePrinterSaverAndMatPlotterSaver (Observer)

Modèle **ValueSeriePrinterSaverAndMatPlotterSaver**
...................................................

Affiche graphiquement avec Matplolib la série des valeurs de la variable, et enregistre la figure dans un fichier situé dans le répertoire temporaire du système (affichage persistant).

::

    print(str(info)+' '+str(var[:]))
    import os.path, numpy, re, tempfile
    tempdir=tempfile.gettempdir()
    import matplotlib.pyplot as plt
    v=numpy.array(var[:], ndmin=1)
    global istep
    try:
        istep+=1
    except:
        istep=0
    f=os.path.join(tempdir,'value_%s_%05i.txt'%(info,istep))
    f=re.sub(r'\s','_',f)
    print('Value saved in "%s"'%f)
    numpy.savetxt(f,v)
    global imfig, mp, ax
    plt.ion()
    try:
        imfig+=1
        mp.suptitle('%s (Figure %i)'%(info,imfig))
    except:
        imfig=0
        mp = plt.figure()
        ax = mp.add_subplot(1, 1, 1)
        mp.suptitle('%s (Figure %i)'%(info,imfig))
        ax.set_xlabel('Step')
        ax.set_ylabel('Variable')
    ax.plot(v)
    f=os.path.join(tempdir,'figure_%s_%05i.pdf'%(info,imfig))
    f=re.sub(r'\s','_',f)
    plt.savefig(f)
    plt.show()

.. index:: single: ValueMean (Observer)

Modèle **ValueMean**
....................

Imprime sur la sortie standard la moyenne de la valeur courante de la variable.

::

    import numpy
    print(str(info)+' '+str(numpy.nanmean(var[-1])))

.. index:: single: ValueStandardError (Observer)

Modèle **ValueStandardError**
.............................

Imprime sur la sortie standard l'écart-type de la valeur courante de la variable.

::

    import numpy
    print(str(info)+' '+str(numpy.nanstd(var[-1])))

.. index:: single: ValueVariance (Observer)

Modèle **ValueVariance**
........................

Imprime sur la sortie standard la variance de la valeur courante de la variable.

::

    import numpy
    print(str(info)+' '+str(numpy.nanvar(var[-1])))

.. index:: single: ValueL2Norm (Observer)

Modèle **ValueL2Norm**
......................

Imprime sur la sortie standard la norme L2 de la valeur courante de la variable.

::

    import numpy
    v = numpy.ravel( var[-1] )
    print(str(info)+' '+str(float( numpy.linalg.norm(v) )))

.. index:: single: ValueRMS (Observer)

Modèle **ValueRMS**
...................

Imprime sur la sortie standard la racine de la moyenne des carrés (RMS), ou moyenne quadratique, de la valeur courante de la variable.

::

    import numpy
    v = numpy.ravel( var[-1] )
    print(str(info)+' '+str(float( numpy.sqrt((1./v.size)*numpy.dot(v,v)) )))
