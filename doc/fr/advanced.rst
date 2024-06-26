..
   Copyright (C) 2008-2024 EDF R&D

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

.. _section_advanced:

================================================================================
**[DocU]** Usages avancés du module ADAO et interopérabilité
================================================================================

Cette section présente des méthodes avancées d'usage du module ADAO, comment
obtenir plus d'information lors d'un calcul, ou comment l'utiliser sans
l'interface graphique (GUI). Cela nécessite de savoir comment trouver les
fichiers ou les commandes incluses dans l'installation complète de SALOME. Tous
les noms à remplacer par l'utilisateur sont indiqués par la syntaxe ``<...>``.

.. _section_advanced_convert_JDC:

Convertir et exécuter un fichier de commandes ADAO (JDC) par l'intermédiaire d'un script Shell
----------------------------------------------------------------------------------------------

Il est possible de convertir et exécuter une fichier de commandes ADAO (JDC, ou
paire de fichiers ".comm/.py", qui se trouvent dans le répertoire ``<Répertoire
du fichier JDC ADAO>``) automatiquement en utilisant un script de commandes
Shell "type" contenant toutes les étapes requises. Si la commande principale de
lancement de SALOME, nommée ``salome``, n'est pas couramment accessible dans un
terminal standard, l'utilisateur doit savoir où se trouvent les principaux
fichiers de lancement de SALOME, et en particulier ce fichier ``salome``. Le
répertoire dans lequel ce fichier réside est symboliquement nommé ``<Répertoire
principal d'installation de SALOME>`` et doit être remplacé par le bon dans le
modèle "type" de fichier Shell.

Lorsqu'un fichier de commande ADAO est construit par l'interface d'édition
graphique d'ADAO et est enregistré, s'il est nommé par exemple
"EtudeAdao1.comm", alors un fichier compagnon nommé "EtudeAdao1.py" est
automatiquement créé dans le même répertoire. Il est nommé ``<Fichier Python
ADAO>`` dans le modèle "type", et il est converti vers YACS comme un ``<Schéma
xml YACS ADAO>`` sous la forme d'un fichier en ".xml" nommé "EtudeAdao1.xml".
Ensuite, ce dernier peut être exécuté en mode console en utilisant l'ordre
standard du mode console de YACS (voir la documentation YACS pour de plus amples
informations).

Dans tous les exemples de fichiers de commandes Shell de lancement, on choisit
de démarrer et arrêter le serveur d'application SALOME dans le même script. Ce
n'est pas indispensable, mais c'est utile pour éviter des sessions SALOME en
attente.

L'exemple le plus simple consiste uniquement à lancer l'exécution d'un schéma
YACS donné, qui a préalablement été généré par l'utilisateur en interface
graphique. Dans ce cas, en ayant pris soin de remplacer les textes contenus
entre les symboles ``<...>``, il suffit d'enregistrer le script de commandes
Shell suivant :
::

    #!/bin/bash
    USERDIR="<Répertoire du fichier JDC ADAO>"
    SALOMEDIR="<Répertoire principal d'installation de SALOME>"
    $SALOMEDIR/salome start -k -t
    $SALOMEDIR/salome shell -- "driver $USERDIR/<Schéma xml YACS ADAO>"
    $SALOMEDIR/salome shell killSalome.py

Il faut ensuite le rendre exécutable pour l'exécuter.

Un exemple un peu plus complet consiste à lancer l'exécution d'un schéma YACS
indiqué par l'utilisateur, en ayant préalablement vérifié sa disponibilité. Pour
cela, en remplaçant le texte ``<Répertoire principal d'installation de
SALOME>``, il suffit d'enregistrer le script de commandes Shell suivant :
::

    #!/bin/bash
    if (test $# != 1)
    then
      echo -e "\nUsage: $0 <Schéma xml YACS ADAO>\n"
      exit
    else
      USERFILE="$1"
    fi
    if (test ! -e $USERFILE)
    then
      echo -e "\nErreur : le fichier XML nommé $USERFILE n'existe pas.\n"
      exit
    else
      SALOMEDIR="<Répertoire principal d'installation de SALOME>"
      $SALOMEDIR/salome start -k -t
      $SALOMEDIR/salome shell -- "driver $USERFILE"
      $SALOMEDIR/salome shell killSalome.py
    fi

Un autre exemple de script consiste à ajouter la conversion du fichier de
commandes ADAO (JDC, ou paire de fichiers ".comm/.py") en un schéma YACS associé
(fichier ".xml"). A la fin du script, on choisit aussi de supprimer le fichier
de ``<Schéma xml YACS ADAO>`` car c'est un fichier généré. Pour cela, en ayant
bien pris soin de remplacer le texte ``<Répertoire principal d'installation de
SALOME>``, il suffit d'enregistrer le script de commandes Shell suivant :
::

    #!/bin/bash
    if (test $# != 1)
    then
      echo -e "\nUsage: $0 <Cas .comm/.py ADAO>\n"
      exit
    else
      D=`dirname $1`
      F=`basename -s .comm $1`
      F=`basename -s .py $F`
      USERFILE="$D/$F"
    fi
    if (test ! -e $USERFILE.py)
    then
      echo -e "\nErreur : le fichier PY nommé $USERFILE.py n'existe pas.\n"
      exit
    else
      SALOMEDIR="<Répertoire principal d'installation de SALOME>"
      $SALOMEDIR/salome start -k -t
      $SALOMEDIR/salome shell -- "python $SALOMEDIR/bin/AdaoYacsSchemaCreator.py $USERFILE.py $USERFILE.xml"
      $SALOMEDIR/salome shell -- "driver $USERFILE.xml"
      $SALOMEDIR/salome shell killSalome.py
      rm -f $USERFILE.xml
    fi

Dans tous les cas, les sorties standard et d'erreur se font dans le terminal de
lancement.

.. _section_advanced_YACS_tui:

Exécuter un schéma de calcul ADAO dans YACS en utilisant le mode "texte" (TUI YACS)
-----------------------------------------------------------------------------------

Cette section décrit comment exécuter en mode TUI (Text User Interface) YACS un
schéma de calcul YACS, obtenu dans l'interface graphique par la fonction
"*Exporter vers YACS*" d'ADAO. Cela utilise le mode texte standard de YACS, qui
est rapidement rappelé ici (voir la documentation YACS pour de plus amples
informations) à travers un exemple simple. Comme décrit dans la documentation,
un schéma XML peut être chargé en python. On donne ici une séquence complète de
commandes pour tester la validité du schéma avant de l'exécuter, ajoutant des
lignes supplémentaires initiales pour charger de manière explicite le catalogue
de types pour éviter d'obscures difficultés :
::

    #-*- coding: utf-8 -*-
    import pilot
    import SALOMERuntime
    import loader
    SALOMERuntime.RuntimeSALOME_setRuntime()

    r = pilot.getRuntime()
    xmlLoader = loader.YACSLoader()
    xmlLoader.registerProcCataLoader()
    try:
        catalogAd = r.loadCatalog("proc", "<Schéma xml YACS ADAO>")
        r.addCatalog(catalogAd)
    except:
        pass

    try:
        p = xmlLoader.load("<Schéma xml YACS ADAO>")
    except IOError,ex:
        print("IO exception:",ex)

    logger = p.getLogger("parser")
    if not logger.isEmpty():
        print("The imported file has errors :")
        print(logger.getStr())

    if not p.isValid():
        print("Le schéma n'est pas valide et ne peut pas être exécuté")
        print(p.getErrorReport())

    info=pilot.LinkInfo(pilot.LinkInfo.ALL_DONT_STOP)
    p.checkConsistency(info)
    if info.areWarningsOrErrors():
        print("Le schéma n'est pas cohérent et ne peut pas être exécuté")
        print(info.getGlobalRepr())

    e = pilot.ExecutorSwig()
    e.RunW(p)
    if p.getEffectiveState() != pilot.DONE:
        print(p.getErrorReport())

Cette démarche permet par exemple d'éditer le schéma YACS XML en mode texte TUI,
ou de rassembler les résultats pour un usage ultérieur.

.. _section_advanced_R:

Exécuter un calcul ADAO en environnement R en utilisant l'interface TUI ADAO
----------------------------------------------------------------------------

.. index:: single: R
.. index:: single: rPython
.. index:: single: reticulate

Pour étendre les possibilités d'analyse et de traitement, il est possible
d'utiliser les calculs ADAO dans l'environnement **R** (voir [R]_ pour plus de
détails). Ce dernier est disponible dans SALOME en lançant l'interpréteur R
dans le shell "``salome shell``". Il faut de plus disposer, en R, du package
"*rPython*" (ou du package "*reticulate*", plus récent), qui peut si nécessaire
être installé par l'utilisateur à l'aide de la commande R suivante :
::

    #-*- coding: utf-8 -*-
    #
    # IMPORTANT : à exécuter dans l'interpréteur R
    # --------------------------------------------
    install.packages("rPython")

On se reportera à la documentation [GilBellosta15]_ pour de plus amples
renseignements sur ce package.

Les calculs ADAO définis en interface textuelle (API/TUI, voir la
:ref:`section_tui`) peuvent alors être interprétés depuis l'environnement R, en
utilisant des données et des informations depuis R. La démarche est illustrée
sur :ref:`subsection_tui_example`, proposé dans la description de l'interface
API/TUI. Dans l'interpréteur R, on peut exécuter les commandes suivantes,
directement issues de l'exemple simple :
::

    #-*- coding: utf-8 -*-
    #
    # IMPORTANT : à exécuter dans l'interpréteur R
    # --------------------------------------------
    library(rPython)
    python.exec("
        from numpy import array
        from adao import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=[0, 1, 2] )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
        case.set( 'Observer',            Variable='Analysis', Template='ValuePrinter' )
        case.execute()
    ")

dont le résultat est :
::

    Analysis [ 0.25000264  0.79999797  0.94999939]

Dans la rédaction des calculs ADAO exécutés depuis R, il convient d'être très
attentif au bon usage des guillemets simples et doubles, qui ne doivent pas
collisionner entre les deux langages.

Les données peuvent venir l'environnement R et doivent être rangées dans des
variables correctement assignées, pour être utilisées ensuite en Python pour
ADAO. On se reportera à la documentation [GilBellosta15]_ pour la mise en
oeuvre. On peut transformer l'exemple ci-dessus pour utiliser des données
provenant de R pour alimenter les trois variables d'ébauche, d'observation et
d'opérateur d'observation. On récupère à la fin l'état optimal dans une variable
R aussi. Les autres lignes sont identiques. L'exemple devient ainsi :
::

    #-*- coding: utf-8 -*-
    #
    # IMPORTANT : à exécuter dans l'interpréteur R
    # --------------------------------------------
    #
    # Variables R
    # -----------
    xb <- 0:2
    yo <- c(0.5, 1.5, 2.5)
    h <- '1 0 0;0 2 0;0 0 3'
    #
    # Code Python
    # -----------
    library(rPython)
    python.assign( "xb",  xb )
    python.assign( "yo",  yo )
    python.assign( "h",  h )
    python.exec("
        from numpy import array
        from adao import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=xb )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array(yo) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix=str(h) )
        case.set( 'Observer',            Variable='Analysis', Template='ValuePrinter' )
        case.execute()
        xa = list(case.get('Analysis')[-1])
    ")
    #
    # Variables R
    # -----------
    xa <- python.get("xa")

On remarquera les conversions explicite de type ``str`` et ``list`` pour
s'assurer que les données sont bien transmises en type standards connus du
package "*rPython*". De plus, ce sont les données qui peuvent être transférées
entre les deux langages, et pas des fonctions ou méthodes. Il convient donc
d'élaborer en Python de manière générique les fonctions d'exécution requises par
ADAO, et de leur transmettre ensuite de manière correcte les données disponibles
en R.

Les cas plus complets, proposés dans les :ref:`subsection_tui_advanced`, peuvent
être exécutés de la même manière, et ils donnent le même résultat que dans
l'interface API/TUI en Python standard.

.. _section_advanced_eficas_gui:

Utiliser l'interface graphique EFICAS d'ADAO comme une commande TUI d'ADAO
--------------------------------------------------------------------------

Pour faciliter l'édition rapide avec EFICAS d'ADAO d'un fichier de commandes
ADAO (JDC, ou paire de fichiers ".comm/.py", qui se trouvent ensemble dans un
répertoire d'étude de l'utilisateur), on peut lancer l'interface graphique
directement depuis l'interpréteur Python. Pour cela, dans un interpréteur
Python obtenu depuis le "SALOME shell", on utilise les commandes suivantes :
::

    from adao import adaoBuilder
    adaoBuilder.Gui()

Pour mémoire, le moyen le plus simple d'obtenir un interpréteur Python inclu
dans une session "SALOME shell" est de lancer la commande suivante dans un
terminal : ::

    $SALOMEDIR/salome shell -- python

avec ``SALOMEDIR`` le ``<Répertoire principal d'installation de SALOME>``.

Si nécessaire, des messages explicites permettent d'identifier les variables
d'environnement requises qui seraient absentes. **Cette commande ne doit
néanmoins pas être lancée dans la console Python de SALOME** (car dans ce cas
il suffit d'activer le module puisque l'on est déjà dans l'interface
graphique...) ou dans une installation Python indépendante, mais elle peut
l'être dans une session "SALOME shell" obtenue depuis le menu
"Outils/Extensions" de SALOME.

.. _section_advanced_execution_mode:

Changer le mode par défaut d'exécution de noeuds dans YACS
----------------------------------------------------------

.. index:: single: YACS
.. index:: single: ExecuteInContainer

Diverses raisons peuvent conduire à vouloir modifier le mode par défaut
d'exécution de noeuds dans YACS (voir [#]_ pour le bon usage de ces
possibilités). Cela peut être pour des raisons de performances, ou par exemple
pour des raisons de conflits de ressources.

On peut vouloir utiliser ce changement de mode d'exécution pour étendre l'usage
des ressources de calcul locales ou pour déporter les calculs d'un noeud qui le
nécessite. C'est en particulier le cas d'un noeud qui devrait utiliser une
ressource de simulation disponible sur un cluster par exemple.

Par ailleurs, les divers calculs qui sont menés (opérateurs fournis par
l'utilisateur, fonctions de restitution des résultats, etc.) peuvent aussi
présenter des conflits s'ils sont exécutés dans un processus unique, et en
particulier dans le processus principal de SALOME. C'est le fonctionnement par
défaut de YACS pour des raisons de performances et de simplicité. Il est
néanmoins recommandé de changer ce fonctionnement lorsque l'on rencontre des
instabilités d'exécution ou des messages d'erreur au niveau de l'interface
graphique.

Dans tous les cas, dans le schéma YACS en édition, il suffit de changer le mode
d'exécution du ou des noeuds qui le nécessitent. Il faut les exécuter dans un
nouveau conteneur créé pour l'occasion (il ne suffit pas d'utiliser le
conteneur par défaut, il faut explicitement en créer un nouveau) et dont les
caractéristiques sont adaptées à l'usage visé. La démarche est donc la suivante
:

#. Créer un nouveau conteneur YACS, par utilisation du menu contextuel des "*Containers*" dans la vue arborescente du schéma YACS (usuellement à gauche),
#. Adapter les caractéristiques du conteneur, en sélectionnant par exemple une propriété de "*type*" valant "*multi*" pour une exécution véritablement parallèle, ou en choisissant une ressource distante de calcul définie par la propriété de "*Resource*", ou en utilisant les paramètres avancés,
#. Sélectionner graphiquement dans la vue centrale le noeud dont on veut changer le mode d'exécution,
#. Dans le panneau à droite des entrées du noeud, déplier les choix d'exécution (nommés "*Execution Mode"*), cocher la case "*Container*" à la place du défaut "*YACS*", et choisir le conteneur nouvellement créé (il porte usuellement le nom "*container0*"),
#. Enregistrer le schéma YACS modifié.

On peut répéter cette démarche pour chaque noeud qui le nécessite, en
réutilisant le même nouveau conteneur pour tous les noeuds, ou en créant un
nouveau conteneur pour chaque noeud.

Une manière plus générale pour imposer une exécution globale dans un conteneur
séparé est d'utiliser une variable nommée "*ExecuteInContainer*". Cette
variable est disponible pour les cas ADAO via l'interface graphique (GUI) ou
l'interface scriptée (elle est par exemple présente par défaut dans la
:ref:`section_ref_assimilation_keywords`).

.. warning::

  Ce changement de mode d'exécution est extrêmement puissant et souple. Il est
  donc recommandé à l'utilisateur à la fois de l'utiliser, et en même temps
  d'être attentif à l'interaction des différents choix qu'il effectue, pour
  éviter par exemple une dégradation involontaire des performances, ou des
  conflits informatiques compliqués à diagnostiquer.

.. _section_advanced_observer:

Obtenir des informations sur des variables spéciales au cours d'un calcul ADAO
------------------------------------------------------------------------------

.. index:: single: Observer
.. index:: single: Observer Template

Certaines variables spéciales internes à l'optimisation, utilisées au cours des
calculs, peuvent être surveillées durant un calcul ADAO. Ces variables peuvent
être affichées, tracées, enregistrées, etc. C'est réalisable en utilisant des
"*observer*", qui sont des commandes rassemblées sous forme de scripts, chacun
associé à une variable.

Des modèles ("templates") sont disponibles lors de l'édition le cas ADAO dans
l'éditeur graphique. Ces scripts simples peuvent être adaptés par l'utilisateur,
soit dans l'étape d'édition intégrée, ou dans l'étape d'édition avant
l'exécution, pour améliorer l'adaptation du calcul ADAO dans le superviseur
d'exécution de SALOME.

Pour mettre en oeuvre ces "*observer*" de manière efficace, on se reportera aux
:ref:`section_ref_observers_requirements`.

.. _section_advanced_logging:

Obtenir plus d'information lors du déroulement d'un calcul
----------------------------------------------------------

.. index:: single: Logging
.. index:: single: Debug
.. index:: single: setDebug

Lors du déroulement d'un calcul, des données et messages utiles sont
disponibles. Il y a deux manières d'obtenir ces informations.

La première, et la manière préférentielle, est d'utiliser la variable interne
"*Debug*" disponible dans chaque cas ADAO. Elle est atteignable dans
l'interface graphique d'édition (GUI) du module comme dans l'interface
textuelle (TUI). La mettre à "*1*" permet d'envoyer des messages dans la
fenêtre de sortie de l'exécution dans YACS ("*YACS Container Log*").

La seconde consiste à utiliser le module Python natif "*logging*" (voir la
documentation Python http://docs.python.org/library/logging.html pour de plus
amples informations sur ce module). Dans l'ensemble du schéma YACS,
principalement à travers les entrées sous forme de scripts, l'utilisateur peut
fixer le niveau de logging en accord avec les besoins d'informations détaillées.
Les différents niveaux de logging sont : "*DEBUG*", "*INFO*", "*WARNING*",
"*ERROR*", "*CRITICAL*". Toutes les informations associées à un niveau sont
affichées à tous les niveaux au-dessus de celui-ci (inclus). La méthode la plus
facile consiste à changer le niveau de surveillance en utilisant les lignes
Python suivantes :
::

    import logging
    logging.getLogger().setLevel(logging.DEBUG)

Le niveau par défaut standard de surveillance par logging est "*WARNING*", le
niveau par défaut dans le module ADAO est "*INFO*".

Il est aussi recommandé d'inclure de la surveillance par logging ou des
mécanismes de débogage dans le code de simulation physique de l'utilisateur, et
de les exploiter en conjonction avec les deux méthodes précédentes. Néanmoins,
il convient d'être prudent dans le stockage de "grosses" variables car cela
coûte du temps ou de la mémoire, quel que soit le niveau de surveillance choisi
(c'est-à-dire même si ces variables ne sont pas affichées).

.. _subsection_ref_parallel_df:

Accélérer les calculs de dérivées numériques en utilisant un mode parallèle
---------------------------------------------------------------------------

.. index:: single: EnableWiseParallelism
.. index:: single: NumberOfProcesses

Lors de la définition d'un opérateur, comme décrit dans le chapitre des
:ref:`section_ref_operator_requirements`, l'utilisateur peut choisir la forme
fonctionnelle "*ScriptWithOneFunction*". Cette forme conduit explicitement à
approximer les opérateurs tangent et adjoint (s'ils sont nécessaires) par un
calcul par différences finies. Cela requiert de nombreux appels à l'opérateur
direct (qui est la fonction définie par l'utilisateur), au moins autant de fois
que la dimension du vecteur d'état. Ce sont ces appels qui peuvent être
potentiellement exécutés en parallèle.

Sous certaines conditions (décrites juste après), il est possible d'accélérer
les calculs de dérivées numériques en utilisant un mode parallèle pour
l'approximation par différences finies. Lors de la définition d'un cas ADAO,
c'est effectué en ajoutant le mot-clé optionnel "*EnableWiseParallelism*", mis
à "*1*" ou à "*True*". Ce mot-clé est inclus à la commande
"*SCRIPTWITHONEFUNCTION*" dans la définition de l'opérateur par interface
graphique, ou aux "*Parameters*" accompagnant la commande "*OneFunction*" par
interface textuelle. Par défaut, ce mode parallèle est désactivé
("*EnableWiseParallelism=0*"). Le mode parallèle utilise uniquement des
ressources locales (à la fois multi-coeurs ou multi-processeurs) de
l'ordinateur sur lequel l'exécution est en train de se dérouler, demandant par
défaut autant de ressources que disponible. Si nécessaire, on peut réduire les
ressources disponibles en limitant le nombre possible de processus parallèles
grâce au mot-clé optionnel "*NumberOfProcesses*", que l'on met au nombre
maximal souhaité (ou à "*0*" pour le contrôle automatique, qui est la valeur
par défaut).

Les principales conditions pour réaliser ces calculs parallèles viennent de la
fonction définie par l'utilisateur, qui représente l'opérateur direct. Cette
fonction doit au moins être "thread safe" pour être exécutée dans un
environnement Python parallèle (notions au-delà du cadre de ce paragraphe). Il
n'est pas évident de donner des règles générales, donc il est recommandé, à
l'utilisateur qui active ce parallélisme interne, de vérifier soigneusement sa
fonction et les résultats obtenus.

D'un point de vue utilisateur, certaines conditions, qui doivent être réunies
pour mettre en place des calculs parallèles pour les approximations des
opérateurs tangent et adjoint, sont les suivantes :

#. La dimension du vecteur d'état est supérieure à 2 ou 3.
#. Le calcul unitaire de la fonction utilisateur directe "dure un certain temps", c'est-à-dire plus que quelques minutes.
#. La fonction utilisateur directe n'utilise pas déjà du parallélisme (ou l'exécution parallèle est désactivée dans le calcul de l'utilisateur).
#. La fonction utilisateur directe n'effectue pas d'accès en lecture/écriture à des ressources communes, principalement des données stockées, des fichiers de sortie ou des espaces mémoire.
#. Les "*observer*" ajoutés par l'utilisateur n'effectuent pas d'accès en lecture/écriture à des ressources communes, comme des fichiers ou des espaces mémoire.

Si ces conditions sont satisfaites, l'utilisateur peut choisir d'activer le
parallélisme interne pour le calcul des dérivées numériques. Malgré la
simplicité d'activation, obtenue en définissant une variable seulement,
l'utilisateur est fortement invité à vérifier les résultats de ses calculs. Il
faut au moins les effectuer une fois avec le parallélisme activé, et une autre
fois avec le parallélisme désactivé, pour comparer les résultats. Si cette mise
en oeuvre échoue à un moment ou à un autre, il faut savoir que ce schéma de
parallélisme fonctionne pour des codes complexes, comme *Code_Aster* dans
*SalomeMeca* [SalomeMeca]_ par exemple. Donc, si cela ne marche pas dans votre
cas, vérifiez bien votre fonction d'opérateur avant et pendant l'activation du
parallélisme...

.. warning::

  En cas de doute, il est recommandé de NE PAS ACTIVER ce parallélisme.

On rappelle aussi qu'il faut choisir dans YACS un container par défaut de type
"*multi*" pour le lancement du schéma, pour permettre une exécution
véritablement parallèle.

.. _subsection_iterative_convergence_control:

Contrôler la convergence pour des cas de calculs et algorithmes itératifs
-------------------------------------------------------------------------

.. index:: single: Convergence
.. index:: single: Convergence itérative

Il existe de nombreuses raisons de vouloir contrôler la convergence des cas de
calculs ou algorithmes disponibles dans ADAO. Par exemple, on peut vouloir de
la *reproductibilité* des solutions optimales, une *qualité* certifiée, une
*stabilité* des conditions de recherche optimale en études, une *économie du
temps de calcul* global, etc. De plus, on remarque que les méthodes utilisées
dans ADAO sont fréquemment itératives, renforçant l'intérêt de ce contrôle de
convergence.

Par défaut, **les cas de calculs ou algorithmes disponibles dans ADAO donnent
accès à de multiples moyens de contrôler leur convergence, spécialement adaptés
à chaque méthode**. Ces moyens de contrôle sont issus de la théorie classique
de l'optimisation et des capacités de chaque algorithme. Les valeurs par défaut
des contrôles sont choisies pour assurer une recherche optimale de qualité sur
des fonctions de simulation aux comportements "*standards*" (régularité,
qualité physique et numérique...), ce qui n'est pas forcément la propriété
principale des simulations réelles en raison de contraintes variées. Il est
donc tout à fait normal d'adapter les critères de convergence aux cas d'études
rencontrés, mais c'est une démarche d'expertise que d'établir la bonne
adaptation.

Il existe des manières assez génériques de contrôler la recherche optimale et
la convergence des algorithmes. On en indique ici les plus utiles, de manière
non exhaustive, et avec l'importante réserve qu'il y a fréquemment des
exceptions aux recommandations formulées. Pour aller plus loin, ces
informations génériques sont impérativement à compléter par les informations
spécifiques à chaque algorithme ou cas de calcul, indiquées dans la
documentation des différents :ref:`section_reference_assimilation`.

**Un premier moyen est de limiter le nombre d'itérations par défaut dans les
processus de recherches itératives**. Même si ce n'est pas la meilleure manière
théorique de contrôler l'algorithme, elle est très efficace dans un processus
d'étude réelle. Pour cela, le mot-clé "*MaximumNumberOfIterations*" existe dans
tous les cas de calculs qui le supportent, et sa valeur par défaut est
usuellement fixée à un équivalent de l'infini pour que ce ne soit pas le
critère d'arrêt. C'est le cas pour les calculs à base de méthodes
variationnelles comme les :ref:`section_ref_algorithm_3DVAR`,
:ref:`section_ref_algorithm_4DVAR` et
:ref:`section_ref_algorithm_NonLinearLeastSquares`, mais c'est aussi le cas
pour d'autres comme les :ref:`section_ref_algorithm_DerivativeFreeOptimization`
ou :ref:`section_ref_algorithm_QuantileRegression`. Dans la pratique, on
recommande une valeur comprise entre 10 et 30 pour rendre ce paramètre de
contrôle effectif et obtenir quand même une recherche optimale de bonne
qualité. Pour une recherche optimale de qualité suffisante, il convient de ne
pas fixer cette restriction trop strictement, c'est-à-dire qu'une limite à 30
itérations devrait être plus favorable qu'une limite à 10 itérations.

**Un second moyen de contrôle de la convergence est d'adapter la tolérance de
décroissance relative dans la minimisation de la fonctionnelle de coût
considérée**. Cette tolérance est contrôlée par le mot-clé
"*CostDecrementTolerance*" dans les algorithmes qui le supportent. La valeur
par défaut est plutôt stricte, elle est choisie pour un contrôle théorique de
convergence lorsque les simulations numériques sont d'une qualité numérique
importante. Dans la pratique, elle peut être adaptée sans hésitation pour
valoir entre :math:`10^{-5}` et :math:`10^{-2}`. Cette adaptation permet en
particulier de réduire ou d'éviter les difficultés de recherche optimale qui se
manifestent par de nombreuses itérations successives portant sur des états
presque identiques.

**Un troisième moyen d'améliorer la convergence est d'adapter le réglage par
défaut de l'approximation par différences finies, essentiellement pour
l'opérateur d'observation et une représentation en mono-opérateur**. Le
contrôle de cette propriété se fait à l'aide du mot-clé
"*DifferentialIncrement*" qui paramètre la définition à l'aide de la
:ref:`section_ref_operator_one`. Sa valeur par défaut est de :math:`10^{-2}`
(ou 1%), et il peut généralement être ajusté entre :math:`10^{-5}` et
:math:`10^{-3}` (même s'il est sage de vérifier soigneusement la pertinence de
sa valeur, il est aisé dans ADAO de modifier ce paramètre). Le critère de
convergence doit ensuite être ajusté de telle sorte qu'il ne surpasse pas
l'ordre de grandeur de cette approximation. En pratique, on peut se contenter
de fixer le critère "*CostDecrementTolerance*" à peu près à la même précision
(c'est-à-dire avec un ordre de grandeur de plus ou de moins) que le critère
"*DifferentialIncrement*". Ce moyen d'amélioration est aussi à compléter
d'analyses à l'aide des :ref:`section_ref_algorithm_LinearityTest` et
:ref:`section_ref_algorithm_GradientTest`.

Par expérience, il n'est *a priori* pas recommandé d'utiliser d'autres moyens
de contrôler la convergence, même s'il en existe. Ces ajustements de paramètres
sont simples à mettre en œuvre, et il est favorable de les essayer (en
expériences jumelles ou pas) car ils résolvent de nombreux problèmes rencontrés
en pratique.

.. [#] Pour de plus amples informations sur YACS, voir le *module YACS* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.
