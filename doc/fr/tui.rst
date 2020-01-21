..
   Copyright (C) 2008-2020 EDF R&D

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

.. index:: single: TUI
.. index:: single: API/TUI
.. index:: single: adaoBuilder
.. _section_tui:

================================================================================
**[DocR]** Interface textuelle pour l'utilisateur (TUI/API)
================================================================================

Cette section présente des méthodes avancées d'usage du module ADAO à l'aide de
son interface de programmation textuelle (API/TUI). Cette interface permet de
créer un objet de calcul de manière similaire à la construction d'un cas par
l'interface graphique (GUI). Dans le cas où l'on désire réaliser à la main le
cas de calcul TUI, on recommande de bien s'appuyer sur l'ensemble de la
documentation du module ADAO, et de se reporter si nécessaire à l'interface
graphique (GUI), pour disposer de l'ensemble des éléments permettant de
renseigner correctement les commandes. Les notions générales et termes utilisés
ici sont définis dans :ref:`section_theory`.

.. _subsection_tui_creating:

Création de cas de calcul TUI ADAO et exemples
----------------------------------------------

.. _subsection_tui_example:

Un exemple simple de création d'un cas de calcul TUI ADAO
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour introduire l'interface TUI, on commence par un exemple simple mais complet
de cas de calcul ADAO. Toutes les données sont explicitement définies dans le
corps du script pour faciliter la lecture. L'ensemble des commandes est le
suivant::

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

Le résultat de l'exécution de ces commandes dans SALOME (que ce soit par la
commande "*shell*" de SALOME, dans la console Python de l'interface, ou par le
menu d'exécution d'un script) est le suivant::

    Analysis [ 0.25000264  0.79999797  0.94999939]

Création détaillée d'un cas de calcul TUI ADAO
++++++++++++++++++++++++++++++++++++++++++++++

On décrit ici plus en détail les différentes étapes de création d'un cas de
calcul TUI ADAO. Les commandes elles-mêmes sont détaillées juste après dans
l':ref:`subsection_tui_commands`.

La création et l'initialisation d'une étude se font par les commandes suivantes,
le nom ``case`` de l'objet du cas de calcul TUI ADAO étant quelconque, au choix
de l'utilisateur::

    from numpy import array, matrix
    from adao import adaoBuilder
    case = adaoBuilder.New()

Il est recommandé d'importer par principe le module ``numpy`` ou ses
constructeurs particuliers comme celui d'``array``, pour faciliter ensuite son
usage dans les commandes elle-mêmes.

Ensuite, le cas doit être construit par une préparation et un enregistrement des
données définissant l'étude. L'ordre de ces commande n'a pas d'importance, il
suffit que les concepts requis par l'algorithme utilisé soient présentes. On se
reportera à :ref:`section_reference` et à ses sous-parties pour avoir le détail
des commandes par algorithme. Ici, on définit successivement l'algorithme
d'assimilation de données ou d'optimisation choisi et ses paramètres, puis
l'ébauche :math:`\mathbf{x}^b` (nommée ``Background``) et sa covariance
d'erreurs :math:`\mathbf{B}` (nommée ``BackgroundError``), et enfin
l'observation :math:`\mathbf{y}^o` (nommée ``Observation``) et sa covariance
d'erreurs :math:`\mathbf{R}` (nommée ``ObservationError``)::

    case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
    #
    case.set( 'Background',          Vector=[0, 1, 2] )
    case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
    #
    case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
    case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )

On remarque que l'on peut donner, en entrée des quantités vectorielles ou
matricielles, des objets de type ``str``, ``list`` ou ``tuple`` de Python, ou de
type ``array`` ou ``matrix`` de Numpy. Dans ces deux derniers cas, il faut
simplement importer le module Numpy avant.

On doit ensuite définir les opérateurs :math:`H` d'observation et éventuellement
:math:`M` d'évolution. Dans tous les cas, linéaire ou non-linéaire, on peut les
définir comme des fonctions. Dans le cas simple d'un opérateur linéaire, on peut
aussi le définir à l'aide de la matrice qui correspond à l'opérateur linéaire.
Dans le cas présent le plus simple d'opérateur linéaire, on utilise la syntaxe
suivante pour un opérateur de :math:`\mathbf{R}^3` sur lui-même::

    case.set( 'ObservationOperator', Matrix = "1 0 0;0 2 0;0 0 3")

Dans le cas beaucoup plus courant d'un opérateur non-linéaire de
:math:`\mathbf{R}^n` dans  :math:`\mathbf{R}^p`, il doit être préalablement
disponible sous la forme d'une fonction Python, connue dans l'espace de nommage
courant, qui prend en entrée un vecteur ``numpy`` (ou une liste ordonnée) de
taille :math:`n` et qui restitue en sortie un vecteur ``numpy`` de taille
:math:`p`. Lorsque seul l'opérateur non-linéaire est défini par l'argument
"*OneFunction*", son adjoint est directement établi de manière numérique et il
est paramétrable par l'argument "*Parameters*". L'exemple suivant montre une
fonction ``simulation`` (qui réalise ici le même opérateur linéaire que
ci-dessus) et l'enregistre dans le cas ADAO::

    import numpy
    def simulation(x):
        "Fonction de simulation H pour effectuer Y=H(X)"
        __x = numpy.matrix(numpy.ravel(numpy.matrix(x))).T
        __H = numpy.matrix("1 0 0;0 2 0;0 0 3")
        return __H * __x
    #
    case.set( 'ObservationOperator',
        OneFunction = simulation,
        Parameters  = {"DifferentialIncrement":0.01},
        )

Pour connaître les résultats intermédiaire ou finaux du calcul du cas, on peut
ajouter des "*observer*", qui permettent d'associer l'exécution d'un script à
une variable intermédiaire ou finale du calcul. On se reportera à la description
de la manière d':ref:`section_advanced_observer`, et à la :ref:`section_reference`
pour savoir quelles sont les quantités observables. Cette association
d'"*observer*" avec une quantité existante se fait de manière similaire à la
définition des données du calcul::

    case.set( 'Observer', Variable="Analysis", Template="ValuePrinter" )

Enfin, lorsque toutes les informations requises sont disponibles dans le cas
``case`` de calcul ADAO, on peut en demander l'exécution de manière très
simple dans l'environnement de l'interpréteur Python::

    case.execute()

Au final, on obtient le script très compact proposé précédemment dans
:ref:`subsection_tui_example`.

Fournir des données ou informations de calcul plus complexes
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Une telle interface s'écrivant en Python, il est possible d'utiliser toute la
puissance du langage pour entrer des données plus complexes qu'une déclaration
explicite.

L'enregistrement des données d'entrées supporte différents types de variables,
mais surtout, ces entrées peuvent recevoir des variables courantes disponibles
dans l'espace de nommage du script. Il est donc aisé d'utiliser des variables
calculées préalablement ou obtenues par l'import de scripts "utilisateur". Si
par exemple les observations sont disponibles sous la forme d'une liste dans un
fichier Python externe nommé ``observations.py`` sous le nom ``table``, il
suffit de réaliser les opérations suivantes pour enregistrer les observations
dans le cas de calcul TUI ADAO::

    from observations import table
    case.set( 'Observation', Vector=table )

La première ligne importe la variable ``table`` depuis le fichier externe, et la
seconde enregistre directement cette table comme la donnée "*Observation*".

La simplicité de cet enregistrement montre bien la facilité d'obtenir les
données de calcul depuis des sources externes, fichiers ou flux informatiques
atteignables en Python. Comme d'habitude, il est recommandé à l'utilisateur de
vérifier ses données avant de les enregistrer dans le cas de calcul TUI ADAO
pour éviter les erreurs compliquées à corriger.

Obtenir et utiliser les résultats de calcul de manière plus riche
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

De la même manière, il est possible d'obtenir et traiter les résultats de calcul
de manière plus riche, pour enchaîner sur des post-traitements après le calcul
en TUI.

Les variables de résultats de calcul, ou les variables internes issues de
l'optimisation ou de l'assimilation de données, sont disponibles à travers la
méthode ``get`` du cas de calcul TUI ADAO, qui renvoie un objet de type liste de
la variable demandée. On se reportera aux :ref:`section_ref_output_variables`
pour une description détaillée sur ce sujet.

A titre d'exemple, on donne quelques lignes de script qui permettent d'obtenir
le nombre d'itérations de l'optimisation et la valeur optimale ainsi que sa
taille::

    print("")
    print("    Nombre d'iterations : %i"%len(case.get("CostFunctionJ")))
    Xa = case.get("Analysis")
    print("    Analyse optimale    : %s"%(Xa[-1],))
    print("    Taille de l'analyse : %i"%len(Xa[-1]))
    print("")

Ces lignes peuvent être très simplement additionnées à l'exemple initial de cas
de calcul TUI ADAO proposé dans :ref:`subsection_tui_example`.

De même que pour l'entrée des données, la simplicité de récupération des
résultats permet d'envisager aisément des post-traitements enchaînés dans
SALOME, pour utiliser par exemple de la visualisation avec MatPlotLib ou PARAVIS
[PARAVIS]_, de l'adaptation de maillage avec HOMARD [HOMARD]_, ou pour d'autres
calculs.

.. _subsection_tui_commands:

Ensemble des commandes disponibles en interface textuelle TUI
-------------------------------------------------------------

Dans l'interface TUI du module ADAO, on suit les conventions et recommandations
courantes en Python pour la distinction entre ce qui est public, et ce qui est
privé ou réservé car relevant des détails d'implémentation. De manière pratique,
tout nom d'objet ou de fonction commençant par au moins un signe "_" est privé
au sens courant de programmation ("*private*"). Néanmoins, l'absence d'un tel
signe au début d'un nom ne le désigne pas comme public. De manière générale, en
Python, et contrairement à d'autres langages, on peut accéder aux objets ou aux
fonction privés. Cela peut parfois être utile, mais un tel usage dans vos codes
conduira à des plantages sans avertissement lors de futures versions. Il est
donc fortement recommandé de ne pas le faire.

Pour clarifier et faciliter l'utilisation du module pour du script, **cette
section définit donc l'interface de programmation (API) textuelle publique pour
l'utilisateur (TUI) de manière complète et limitative**. L'usage en script
d'objets ou fonctions ADAO autres que ceux qui sont définis ici est fortement
déconseillé, car cela conduira vraisemblablement à des plantages sans
avertissement lors de futures versions.

Syntaxes d'appel équivalentes pour les commandes TUI
++++++++++++++++++++++++++++++++++++++++++++++++++++

La définition des données lors de la création de cas de calcul TUI ADAO supporte
**deux syntaxes entièrement équivalentes**. On peut :

- soit utiliser la commande ``set`` et comme premier argument le concept
  ``XXXXX`` sur lequel appliquer la commande dont les arguments suivent,
- soit utiliser la commande ``setXXXXX`` contenant les arguments de la commande
  à appliquer.

Pour illustrer cette équivalence, on prend l'exemple des deux commandes
suivantes qui conduisent au même résultat::

    case.set( 'Background', Vector=[0, 1, 2] )

et::

    case.setBackground( Vector=[0, 1, 2] )

Le choix de l'une ou l'autre des syntaxes est librement laissé à l'utilisateur,
selon son contexte d'usage. Dans la suite, par souci de clarté, on définit les
commandes selon la seconde syntaxe.

Création d'un cas de calcul en interface textuelle TUI
++++++++++++++++++++++++++++++++++++++++++++++++++++++

La création et l'initialisation d'un cas de calcul en interface textuelle TUI se
font en important le module d'interface "*adaoBuilder*" et en invoquant sa
méthode "*New()*" comme illustré dans les quelques lignes suivantes (le nom
``case`` de l'objet étant quelconque, au choix de l'utilisateur)::

    from numpy import array, matrix
    from adao import adaoBuilder
    case = adaoBuilder.New()

Il est recommandé par principe de toujours importer le module ``numpy`` (ou ses
constructeurs particuliers, comme celui d'``array``) pour faciliter ensuite son
usage dans les commandes elles-mêmes.

Définir les données de calcul
+++++++++++++++++++++++++++++

Les commandes qui suivent permettent de définir les données d'un cas de calcul
TUI ADAO. Le pseudo-type des arguments est similaire et compatible avec ceux des
entrées en interface GUI, décrits dans la section des
:ref:`section_reference_entry` et en particulier par la
:ref:`section_ref_entry_types`. La vérification de l'adéquation des grandeurs se
fait soit lors de leur définition, soit lors de l'exécution.

Dans chaque commande, le mot-clé booléen "*Stored*" permet d'indiquer si l'on
veut éventuellement la stocker la grandeur définie, pour en disposer en cours de
calcul ou en sortie. Le choix par défaut est de ne pas stocker, et il est
recommandé de conserver cette valeur par défaut. En effet, pour un cas de calcul
TUI, on dispose déjà souvent des grandeurs données en entrées qui sont présentes
dans l'espace de nommage courant du cas.

Les commandes disponibles sont les suivantes :

.. index:: single: setBackground

**setBackground** (*Vector, VectorSerie, Script, DataFile, ColNames, ColMajor, Stored*)
    Cette commande permet de définir l'ébauche :math:`\mathbf{x}^b`. Selon les
    algorithmes, on peut la définir comme un vecteur simple par "*Vector*", ou
    comme une liste de vecteurs par "*VectorSerie*". Si on la définit par un
    script dans "*Script*", le vecteur est de type "*Vector*" (par défaut) ou
    "*VectorSerie*" selon que l'une de ces variables est placée à "*True*". Si
    on utilise un fichier de données par "*DataFile*" (en sélectionnant, en
    colonne par défaut ou en ligne selon "*ColMajor*", toutes les variables par
    défaut ou celles de la liste "*ColNames*"), le vecteur est de type
    "*Vector*".

.. index:: single: setBackgroundError

**setBackgroundError** (*Matrix, ScalarSparseMatrix, DiagonalSparseMatrix, Script, Stored*)
    Cette commande permet de définir la matrice :math:`\mathbf{B}` de
    covariance des erreurs d'ébauche. La matrice peut être définie de manière
    complète par le mot-clé "*Matrix*", ou de manière parcimonieuse, comme une
    matrice diagonale dont on donne la variance unique sur la diagonale par
    "*ScalarSparseMatrix*", ou comme une matrice diagonale dont on donne le
    vecteur des variances situé sur la diagonale par "*DiagonalSparseMatrix*".
    Si on la définit par un script dans "*Script*", la matrice est de type
    "*Matrix*" (par défaut), "*ScalarSparseMatrix*" ou "*DiagonalSparseMatrix*"
    selon que l'une de ces variables est placée à "*True*".

.. index:: single: setCheckingPoint

**setCheckingPoint** (*Vector, VectorSerie, Script, DataFile, ColNames, ColMajor, Stored*)
    Cette commande permet de définir un point courant :math:`\mathbf{x}`
    utilisé pour un algorithme de vérification. Selon les algorithmes, on peut
    le définir comme un vecteur simple par "*Vector*", ou comme une liste de
    vecteurs par "*VectorSerie*". Si on le définit par un script dans
    "*Script*", le vecteur est de type "*Vector*" (par défaut) ou
    "*VectorSerie*" selon que l'une de ces variables est placée à "*True*". Si
    on utilise un fichier de données par "*DataFile*" (en sélectionnant, en
    colonne par défaut ou en ligne selon "*ColMajor*", toutes les variables par
    défaut ou celles de la liste "*ColNames*"), le vecteur est de type
    "*Vector*".

.. index:: single: setControlModel

**setControlModel** (*Matrix, OneFunction, ThreeFunctions, Parameters, Script, ExtraArgs, Stored*)
    Cette commande permet de définir l'opérateur de contrôle :math:`O`, qui
    décrit un contrôle d'entrée linéaire externe de l'opérateur d'évolution ou
    d'observation. On se reportera :ref:`section_ref_operator_control`. Sa
    valeur est définie comme un objet de type fonction ou de type "*Matrix*".
    Dans le cas d'une fonction, différentes formes fonctionnelles peuvent être
    utilisées, comme décrit dans la section
    :ref:`section_ref_operator_requirements`, et entrées par les mots-clés
    "*OneFunction*" ou "*ThreeFunctions*". Dans le cas d'une définition par
    "*Script*", l'opérateur est de type "*Matrix*", "*OneFunction*" ou
    "*ThreeFunctions*" selon que l'une de ces variables est placée à "*True*".
    Les paramètres de contrôle de l'approximation numérique de l'opérateur
    adjoint, dans le cas "*OneFunction*", peuvent être renseignés par un
    dictionnaire à travers le mot-clé "*Parameters*". Les entrées potentielles
    de ce dictionnaire de paramètres sont "*DifferentialIncrement*",
    "*CenteredFiniteDifference*" (similaires à celles de l'interface graphique).

.. index:: single: setControlInput

**setControlInput** (*Vector, VectorSerie, Script, DataFile, ColNames, ColMajor, Stored*)
    Cette commande permet de définir le vecteur de contrôle :math:`\mathbf{u}`.
    Selon les algorithmes, on peut le définir comme un vecteur simple par
    "*Vector*", ou comme une liste de vecteurs par "*VectorSerie*". Si on le
    définit par un script dans "*Script*", le vecteur est de type "*Vector*"
    (par défaut) ou "*VectorSerie*" selon que l'une de ces variables est placée
    à "*True*". Si on utilise un fichier de données par "*DataFile*" (en
    sélectionnant, en colonne par défaut ou en ligne selon "*ColMajor*", toutes
    les variables par défaut ou celles de la liste "*ColNames*"), le vecteur
    est de type "*Vector*".

.. index:: single: setEvolutionError

**setEvolutionError** (*Matrix, ScalarSparseMatrix, DiagonalSparseMatrix, Script, Stored*)
    Cette commande permet de définir la matrice :math:`\mathbf{Q}` de
    covariance des erreurs d'évolution. La matrice peut être définie de manière
    complète par le mot-clé "*Matrix*", ou de manière parcimonieuse, comme une
    matrice diagonale dont on donne la variance unique sur la diagonale par
    "*ScalarSparseMatrix*", ou comme une matrice diagonale dont on donne le
    vecteur des variances situé sur la diagonale par "*DiagonalSparseMatrix*".
    Si on la définit par un script dans "*Script*", la matrice est de type
    "*Matrix*" (par défaut), "*ScalarSparseMatrix*" ou "*DiagonalSparseMatrix*"
    selon que l'une de ces variables est placée à "*True*".

.. index:: single: setEvolutionModel

**setEvolutionModel** (*Matrix, OneFunction, ThreeFunctions, Parameters, Script, ExtraArgs, Stored*)
    Cette commande permet de définir l'opérateur d'evolution :math:`M`, qui
    décrit un pas élémentaire d'évolution. Sa valeur est définie comme un objet
    de type fonction ou de type "*Matrix*". Dans le cas d'une fonction,
    différentes formes fonctionnelles peuvent être utilisées, comme décrit dans
    la section :ref:`section_ref_operator_requirements`, et entrées par les
    mots-clés "*OneFunction*" ou "*ThreeFunctions*". Dans le cas d'une
    définition par "*Script*", l'opérateur est de type "*Matrix*",
    "*OneFunction*" ou "*ThreeFunctions*" selon que l'une de ces variables est
    placée à "*True*". Les paramètres de contrôle de l'approximation numérique
    de l'opérateur adjoint, dans le cas "*OneFunction*", peuvent être renseignés
    par un dictionnaire dans "*Parameters*". Les entrées potentielles de ce
    dictionnaire de paramètres sont "*DifferentialIncrement*",
    "*CenteredFiniteDifference*", "*EnableMultiProcessing*",
    "*NumberOfProcesses*" (similaires à celles de l'interface graphique).

.. index:: single: setObservation

**setObservation** (*Vector, VectorSerie, Script, DataFile, ColNames, ColMajor, Stored*)
    Cette commande permet de définir le vecteur d'observation
    :math:`\mathbf{y}^o`. Selon les algorithmes, on peut le définir comme un
    vecteur simple par "*Vector*", ou comme une liste de vecteurs par
    "*VectorSerie*". Si on le définit par un script dans "*Script*", le vecteur
    est de type "*Vector*" (par défaut) ou "*VectorSerie*" selon que l'une de
    ces variables est placée à "*True*". Si on utilise un fichier de données
    par "*DataFile*" (en sélectionnant, en colonne par défaut ou en ligne selon
    "*ColMajor*", toutes les variables par défaut ou celles de la liste
    "*ColNames*"), le vecteur est de type "*Vector*".

.. index:: single: setObservationError

**setObservationError** (*Matrix, ScalarSparseMatrix, DiagonalSparseMatrix, Script, Stored*)
    Cette commande permet de définir la matrice :math:`\mathbf{R}` de
    covariance des erreurs d'observation. La matrice peut être définie de
    manière complète par le mot-clé "*Matrix*", ou de manière parcimonieuse,
    comme une matrice diagonale dont on donne la variance unique sur la
    diagonale par "*ScalarSparseMatrix*", ou comme une matrice diagonale dont on
    donne le vecteur des variances situé sur la diagonale par
    "*DiagonalSparseMatrix*". Si on la définit par un script dans "*Script*", la
    matrice est de type "*Matrix*" (par défaut), "*ScalarSparseMatrix*" ou
    "*DiagonalSparseMatrix*" selon que l'une de ces variables est placée à
    "*True*".

.. index:: single: setObservationOperator

**setObservationOperator** (*Matrix, OneFunction, ThreeFunctions, AppliedInXb, Parameters, Script, ExtraArgs, Stored*)
    Cette commande permet de définir l'opérateur d'observation :math:`H`, qui
    transforme les paramètres d'entrée :math:`\mathbf{x}` en résultats
    :math:`\mathbf{y}` qui sont à comparer aux observations
    :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de type fonction
    ou de type "*Matrix*". Dans le cas d'une fonction, différentes formes
    fonctionnelles peuvent être utilisées, comme décrit dans la section
    :ref:`section_ref_operator_requirements`, et entrées par les mots-clés
    "*OneFunction*" ou "*ThreeFunctions*". Dans le cas d'une définition par
    "*Script*", l'opérateur est de type "*Matrix*", "*OneFunction*" ou
    "*ThreeFunctions*" selon que l'une de ces variables est placée à "*True*".
    Dans le cas où l'opérateur :math:`H` évalué en :math:`\mathbf{x}^b` est
    disponible, il peut être donné en utilisant "*AppliedInXb*" et sera
    considéré comme un vecteur. Les paramètres de contrôle de l'approximation
    numérique de l'opérateur adjoint, dans le cas "*OneFunction*", peuvent être
    renseignés par un dictionnaire dans "*Parameters*". Les entrées potentielles
    de ce dictionnaire de paramètres sont "*DifferentialIncrement*",
    "*CenteredFiniteDifference*", "*EnableMultiProcessing*",
    "*NumberOfProcesses*" (similaires à celles de l'interface graphique).

.. index:: single: set

**set** (*Concept,...*)
    Cette commande permet de disposer d'une syntaxe équivalente pour toutes les
    commandes de ce paragraphe. Son premier argument est le nom du concept à
    définir (par exemple "*Background*" ou "*ObservationOperator*"), sur lequel
    s'applique ensuite les arguments qui suivent, qui sont les mêmes que dans
    les commandes individuelles précédentes. Lors de l'usage de cette commande,
    il est indispensable de nommer les arguments (par exemple "*Vector=...*").

Paramétrer le calcul, les sorties, etc.
+++++++++++++++++++++++++++++++++++++++

.. index:: single: setAlgorithmParameters

**setAlgorithmParameters** (*Algorithm, Parameters, Script*)
    Cette commande permet de choisir l'algorithme de calcul ou de vérification
    par l'argument "*Algorithm*" sous la forme d'un nom d'algorithme (on se
    reportera utilement aux listes des :ref:`section_reference_assimilation` et
    des :ref:`section_reference_checking`), et de définir les paramètres de
    calcul par l'argument "*Parameters*". Dans le cas d'une définition par
    "*Script*", le fichier indiqué doit contenir les deux variables
    "*Algorithm*" et "*Parameters*" (ou "*AlgorithmParameters*" de manière
    équivalente).

.. index:: single: setName

**setName** (*String*)
    Cette commande permet de donner un titre court au cas de calcul.

.. index:: single: setDirectory

**setDirectory** (*String*)
    Cette commande permet d'indiquer le répertoire courant d'exécution.

.. index:: single: setDebug

**setDebug** ()
    Cette commande permet d'activer le mode d'information détaillé lors de
    l'exécution.

.. index:: single: setNoDebug

**setNoDebug** ()
    Cette commande permet de désactiver le mode d'information détaillé lors de
    l'exécution.

.. index:: single: setObserver

**setObserver** (*Variable, Template, String, Script, Info*)
    Cette commande permet de définir un *observer* sur une variable courante ou
    finale du calcul. On se reportera à la description des
    :ref:`section_ref_observers_requirements` pour avoir leur liste et leur
    format, et à la :ref:`section_reference` pour savoir quelles sont les
    quantités observables. On définit comme un "*String*" le corps de
    l'*observer*, en utilisant une chaîne de caractères incluant si nécessaire
    des sauts de lignes. On recommande d'utiliser les patrons disponibles par
    l'argument "*Template*". Dans le cas d'une définition par "*Script*", le
    fichier indiqué doit contenir uniquement le corps de la fonction, comme
    décrit dans les :ref:`section_ref_observers_requirements`. La variable
    "*Info*" contient une chaîne de caractère d'information ou une chaine vide.

Effectuer le calcul
+++++++++++++++++++

.. index:: single: execute
.. index:: single: Executor
.. index:: single: SaveCaseInFile

**execute** (*Executor, SaveCaseInFile*)
    Cette commande lance le calcul complet dans l'environnement d'exécution
    choisi par le mot-clé *Executor*. Cet environnement peut être celui de
    l'interpréteur Python, sans interaction avec YACS (demandé par la valeur
    "*Python*"), ou celui de YACS (demandé par la valeur "*YACS*" [YACS]_). Si
    un fichier est indiqué dans le mot-clé *SaveCaseInFile*, il sera utilisé
    pour enregistrer la version associée du fichier de commande pour
    l'environnement d'exécution requis. Lors de l'exécution, les sorties
    courantes (standard et d'erreur) sont celles de l'environnement choisi. On
    dispose si nécessaire (ou si possible) du parallélisme interne des
    algorithmes dans ADAO, du parallélisme de YACS, et du parallélisme interne
    du ou des codes de simulation utilisés.

Obtenir séparément les résultats de calcul
++++++++++++++++++++++++++++++++++++++++++

.. index:: single: get

**get** (*Concept*)
    Cette commande permet d'extraire explicitement les variables disponibles en
    sortie du cas de calcul TUI ADAO pour les utiliser dans la suite du
    scripting, par exemple en visualisation. Elle a pour argument le nom d'un
    variable dans "*Concept*", et renvoie en retour la grandeur sous la forme
    d'une liste (même s'il n'y en a qu'un exemplaire) de cette variable de
    base. Pour connaître la liste des variables et les utiliser, on se
    reportera à l':ref:`subsection_r_o_v_Inventaire`, et plus généralement à la
    fois aux :ref:`section_ref_output_variables` et aux documentations
    individuelles des algorithmes.

Enregistrer, charger ou convertir les commandes de cas de calcul
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

L'enregistrement ou le chargement d'un cas de calcul concernent les quantités
et les actions qui lui sont liées par les commandes précédentes, à l'exclusion
d'opérations externes au cas (comme par exemple le post-processing qui peut
être développé après le cas de calcul). Les commandes enregistrées ou chargées
restent néanmoins parfaitement compatibles avec ces opérations en Python
externes au cas.

.. index:: single: load
.. index:: single: FileName
.. index:: single: Content
.. index:: single: Object
.. index:: single: Formater

**load** (*FileName, Content, Object, Formater*)
    Cette commande permet de lire ou charger un cas d'étude, à partir d'un
    fichier "*FileName*" ou d'un contenu en mémoire par "*Content*" ou
    "*Object*". Le mot-clé "*Formater*" peut désigner le format "*TUI*" pour
    les commandes du type interface de programmation textuelle (défaut), et le
    format "*COM*" pour les commandes du type COMM provenant de l'interface
    ADAO de type EFICAS.

.. index:: single: dump

**dump** (*FileName, Formater*)
    Cette commande permet d'enregistrer, dans un fichier "*FileName*", les
    commandes du cas d'étude en cours. Le mot-clé "*Formater*" peut désigner
    les formats "*TUI*" pour les commandes du type interface de programmation
    textuelle (défaut), et "*YACS*" pour les commandes du type YACS.

.. index:: single: convert
.. index:: single: FileNameFrom
.. index:: single: ContentFrom
.. index:: single: ObjectFrom
.. index:: single: FormaterFrom
.. index:: single: FileNameTo
.. index:: single: FormaterTo

**convert** (*FileNameFrom, ContentFrom, ObjectFrom, FormaterFrom, FileNameTo, FormaterTo*)
    Cette commande permet de convertir directement d'un format reconnu à un
    autre les commandes établissant le cas de calcul en cours. Certains
    formats ne sont disponibles qu'en entrée ou qu'en sortie.

.. _subsection_tui_advanced:

Exemples plus avancés de cas de calcul TUI ADAO
-----------------------------------------------

On propose ici des exemples plus complets de cas de calcul TUI ADAO, en donnant
l'objectif de l'exemple et un jeu de commandes qui permet de parvenir à cet
objectif.

Exploitation indépendante des résultats d'un cas de calcul
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

L'objectif est d'effectuer en TUI la mise en données d'un cas de calcul ADAO,
son exécution, puis la récupération des résultats pour ensuite enchaîner sur une
exploitation indépendante de ces résultats (cette dernière n'étant pas décrite
ici, puisque dépendante de l'utilisateur).

Les hypothèses du cas utilisateur sont les suivantes. On suppose :

#. que l'on veut recaler 3 paramètres ``alpha``, ``beta`` et ``gamma`` dans un domaine borné,
#. que l'on dispose d'observations nommées ``observations``,
#. que l'utilisateur dispose en Python d'une fonction de simulation physique appelée ``simulation``, préalablement (bien) testée, qui transforme les 3 paramètres en résultats similaires aux observations,
#. que l'exploitation indépendante, que l'utilisateur veut faire, est représentée ici par l'affichage simple de l'état initial, de l'état optimal, de la simulation en ce point, des états intermédiaires et du nombre d'itérations d'optimisation.

Pour effectuer de manière simple cet essai de cas de calcul TUI, on se donne par
exemple les entrées suivantes, parfaitement arbitraires, en construisant les
observations par simulation pour se placer dans un cas d'expériences jumelles::

    #
    # Construction artificielle d'un exemple de données utilisateur
    # -------------------------------------------------------------
    alpha = 5.
    beta = 7
    gamma = 9.0
    #
    alphamin, alphamax = 0., 10.
    betamin,  betamax  = 3, 13
    gammamin, gammamax = 1.5, 15.5
    #
    def simulation(x):
        "Fonction de simulation H pour effectuer Y=H(X)"
        import numpy
        __x = numpy.matrix(numpy.ravel(numpy.matrix(x))).T
        __H = numpy.matrix("1 0 0;0 2 0;0 0 3; 1 2 3")
        return __H * __x
    #
    # Observations obtenues par simulation
    # ------------------------------------
    observations = simulation((2, 3, 4))

Le jeu de commandes que l'on peut utiliser est le suivant::

    import numpy
    from adao import adaoBuilder
    #
    # Mise en forme des entrées
    # -------------------------
    Xb = (alpha, beta, gamma)
    Bounds = (
        (alphamin, alphamax),
        (betamin,  betamax ),
        (gammamin, gammamax))
    #
    # TUI ADAO
    # --------
    case = adaoBuilder.New()
    case.set(
        'AlgorithmParameters',
        Algorithm = '3DVAR',
        Parameters = {
            "Bounds":Bounds,
            "MaximumNumberOfSteps":100,
            "StoreSupplementaryCalculations":[
                "CostFunctionJ",
                "CurrentState",
                "SimulatedObservationAtOptimum",
                ],
            }
        )
    case.set( 'Background', Vector = numpy.array(Xb), Stored = True )
    case.set( 'Observation', Vector = numpy.array(observations) )
    case.set( 'BackgroundError', ScalarSparseMatrix = 1.0e10 )
    case.set( 'ObservationError', ScalarSparseMatrix = 1.0 )
    case.set(
        'ObservationOperator',
        OneFunction = simulation,
        Parameters  = {"DifferentialIncrement":0.0001},
        )
    case.set( 'Observer', Variable="CurrentState", Template="ValuePrinter" )
    case.execute()
    #
    # Exploitation indépendante
    # -------------------------
    Xbackground   = case.get("Background")
    Xoptimum      = case.get("Analysis")[-1]
    FX_at_optimum = case.get("SimulatedObservationAtOptimum")[-1]
    J_values      = case.get("CostFunctionJ")[:]
    print("")
    print("Nombre d'itérations internes...: %i"%len(J_values))
    print("Etat initial...................: %s"%(numpy.ravel(Xbackground),))
    print("Etat optimal...................: %s"%(numpy.ravel(Xoptimum),))
    print("Simulation à l'état optimal....: %s"%(numpy.ravel(FX_at_optimum),))
    print("")

L'exécution de jeu de commandes donne le résultat suivant::

    CurrentState [ 5.  7.  9.]
    CurrentState [ 0.   3.   1.5]
    CurrentState [ 1.40006418  3.86705307  3.7061137 ]
    CurrentState [ 1.42580231  3.68474804  3.81008738]
    CurrentState [ 1.60220353  3.0677108   4.06146069]
    CurrentState [ 1.72517855  3.03296953  4.04915706]
    CurrentState [ 2.00010755  3.          4.00055409]
    CurrentState [ 1.99995528  3.          3.99996367]
    CurrentState [ 2.00000007  3.          4.00000011]
    CurrentState [ 2.  3.  4.]

    Nombre d'itérations internes...: 10
    Etat initial...................: [ 5.  7.  9.]
    Etat optimal...................: [ 2.  3.  4.]
    Simulation à l'état optimal....: [  2.   6.  12.  20.]

Comme il se doit en expériences jumelles, avec une confiance majoritairement
placée dans les observations, on constate que l'on retrouve bien les paramètres
qui ont servi à construire artificiellement les observations.

.. Réconciliation de courbes à l'aide de MedCoupling
.. +++++++++++++++++++++++++++++++++++++++++++++++++

.. Utilisation de fonctions de surveillance de type "observer"
.. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Equivalences entre l'interface graphique (GUI) et l'interface textuelle (TUI)
.. -----------------------------------------------------------------------------

.. [HOMARD] Pour de plus amples informations sur HOMARD, voir le *module HOMARD* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [PARAVIS] Pour de plus amples informations sur PARAVIS, voir le *module PARAVIS* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.

.. [YACS] Pour de plus amples informations sur YACS, voir le *module YACS* et son aide intégrée disponible dans le menu principal *Aide* de l'environnement SALOME.
