..
   Copyright (C) 2008-2021 EDF R&D

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

.. _section_tutorials_in_python:

================================================================================
**[DocU]** Tutoriaux sur l'utilisation du module ADAO dans Python
================================================================================

Cette section présente quelques exemples d'utilisation du module ADAO en
Python. Le premier montre comment construire un cas simple d'assimilation de
données définissant explicitement toutes les données d'entrée requises à
travers l'interface utilisateur textuelle (TUI). Le second montre, sur le même
cas, comment définir les données d'entrée à partir de sources externes à
travers des scripts. On présente ici toujours des scripts Python car ils sont
directement insérables dans les définitions de script de l'interface Python,
mais les fichiers externes peuvent utiliser d'autres langages.

Ces exemples sont intentionnellement décrits de manière semblables aux
:ref:`section_tutorials_in_salome` car ils sont similaires à ceux que l'on peut
traiter dans l'interface graphique SALOME. Les notations mathématiques
utilisées ci-dessous sont expliquées dans la section :ref:`section_theory`.

.. _section_tutorials_in_python_explicit:

Construire un cas d'estimation avec une définition explicite des données
------------------------------------------------------------------------

Cet exemple très simple est un cas de démonstration, et il décrit comment
mettre au point un environnement d'estimation par BLUE de manière à obtenir un
*état estimé par méthode de moindres carrés pondérés* d'un système à partir
d'une observation de l'état et d'une connaissance *a priori* (ou ébauche) de
cet état. En d'autres termes, on cherche l'intermédiaire pondéré entre les
vecteurs d'observation et d'ébauche. Toutes les valeurs numériques de cet
exemple sont arbitraires.

Conditions d'expérience
+++++++++++++++++++++++

On choisit d'opérer dans un espace d'observation à 3 dimensions. La 3D est
choisie de manière à restreindre la taille des objets numériques à entrer
explicitement par l'utilisateur, mais le problème n'est pas dépendant de la
dimension et peut être posé en dimension 10, 100, 1000... L'observation
:math:`\mathbf{y}^o` vaut 1 dans chaque direction, donc :
::

    Yo = [1 1 1]

L'ébauche :math:`\mathbf{x}^b` de l'état , qui représente une connaissance *a
priori* ou une régularisation mathématique, est choisie comme valant 0 dans
chaque cas, ce qui donne donc :
::

    Xb = [0 0 0]

La mise en oeuvre de l'assimilation de données requiert des informations sur
les covariances d'erreur :math:`\mathbf{R}` et :math:`\mathbf{B}`,
respectivement pour les variables d'erreur d'observation et d'ébauche. On
choisit ici des erreurs décorrélées (c'est-à-dire des matrices diagonales) et
d'avoir la même variance de 1 pour toutes les variables (c'est-à-dire des
matrices identité). On pose donc :
::

    B = R = Id = [1 0 0 ; 0 1 0 ; 0 0 1]

Enfin, on a besoin d'un opérateur d'observation :math:`\mathbf{H}` pour
convertir l'état d'ébauche dans l'espace des observations. Ici, comme les
dimensions d'espace sont les mêmes et que l'on postule un opérateur linéaire de
sélection, on peut choisir l'identité comme opérateur d'observation :
::

    H = Id = [1 0 0 ; 0 1 0 ; 0 0 1]

Avec de tels choix, l'estimateur "Best Linear Unbiased Estimator" (BLUE) sera le
vecteur moyen entre :math:`\mathbf{y}^o` et :math:`\mathbf{x}^b`, nommé
*analysis*, noté :math:`\mathbf{x}^a`, et valant :
::

    Xa = [0.5 0.5 0.5]

Pour étendre cet exemple, on peut modifier les variances représentées par
:math:`\mathbf{B}` ou :math:`\mathbf{R}` indépendamment, et l'analyse
:math:`\mathbf{x}^a` se déplacera vers :math:`\mathbf{y}^o` ou vers
:math:`\mathbf{x}^b`, en proportion inverse des variances dans
:math:`\mathbf{B}` et :math:`\mathbf{R}`. Comme autre extension, on peut aussi
dire qu'il est équivalent de rechercher l'analyse à l'aide d'un algorithme de
BLUE ou d'un algorithme de 3DVAR.

Utiliser l'interface textuelle (TUI) pour construire le cas ADAO
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

On va renseigner les variables pour construire le cas ADAO en utilisant les
conditions d'expérience décrites ci-dessus. L'ensemble des informations
techniques données au-dessus sont à insérer directement dans la définition du
cas ADAO, en utilisant au choix une liste, un vecteur ou une chaîne de
caractères pour chaque variable. On s'appuie sur la documentation de référence
:ref:`section_tui`. On constitue ainsi un cas ADAO, qui peut être enregistré en
fichier Python standard.

L'entête du fichier doit comporter les déclarations habituelles du cas :
::

    from adao import adaoBuilder
    case = adaoBuilder.New()
    case.set( 'AlgorithmParameters', Algorithm='Blue' )

La définition des observations et des covariances d'erreurs sont les suivantes :
::

    case.set( 'Observation',         Vector=[1, 1, 1] )
    case.set( 'ObservationError',    Matrix="1 0 0 ; 0 1 0 ; 0 0 1" )

De la même manière, l'information *a priori* est définie avec ses covariances
d'erreur par :
::

    case.set( 'Background',          Vector=[0, 0, 0] )
    case.set( 'BackgroundError',     Matrix="1 0 0 ; 0 1 0 ; 0 0 1" )

L'opérateur d'observation, très simple et ici linéaire, peut être défini par:
::

    case.set( 'ObservationOperator', Matrix="1 0 0 ; 0 1 0 ; 0 0 1" )

Pour obtenir un affichage automatique de l'état optimal analysé, on peut
ajouter une commande d'"*observer*", ou ajouter après l'exécution des commandes de
traitement des résultats de l'assimilation de données. On peut se contenter
dans ce cas très simple d'ajouter :
::

    case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )

La démarche d'exécution est extrêmement simple et consiste à effectuer à la
ligne de commande, ou dans le fichier enregistrant le cas, la commande
suivante :
::

    case.execute()

Le résultat de l'exécution de ces commandes (que ce soit en console Python, par
la commande "*shell*" de SALOME, dans la console Python de l'interface, ou par
le menu d'exécution d'un script) est le suivant :
::

    Analysis [0.5 0.5 0.5]

comme montré ci-après :
::

    adao@python$ python
    Python 3.6.5 (default, Feb 01 2019, 12:12:12)
    [GCC] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
    >>> from adao import adaoBuilder
    >>> case = adaoBuilder.New()
    >>> case.set( 'AlgorithmParameters', Algorithm='Blue' )
    >>> case.set( 'Observation',         Vector=[1, 1, 1] )
    >>> case.set( 'ObservationError',    Matrix="1 0 0 ; 0 1 0 ; 0 0 1" )
    >>> case.set( 'Background',          Vector=[0, 0, 0] )
    >>> case.set( 'BackgroundError',     Matrix="1 0 0 ; 0 1 0 ; 0 0 1" )
    >>> case.set( 'ObservationOperator', Matrix="1 0 0 ; 0 1 0 ; 0 0 1" )
    >>> case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
    >>> case.execute()
    Analysis [0.5 0.5 0.5]
    0
    >>>

Pour étendre cet exemple, on peut remarquer que le même problème résolu par un
algorithme de 3DVAR donne le même résultat. Cet algorithme peut être choisi
lors de l'étape de construction du cas ADAO en changeant simplement l'argument
"*Algorithm*" en entête. Le reste du cas ADAO en 3DVAR est alors entièrement
similaire au cas algorithmique du BLUE.

.. _section_tutorials_in_python_script:

Construire un cas d'estimation avec une définition de données externes par scripts
----------------------------------------------------------------------------------

Il est utile d'acquérir une partie ou la totalité des données du cas ADAO
depuis une définition externe, en utilisant des scripts Python pour donner
accès à ces données. À titre d'exemple, on construit ici un cas ADAO présentant
le même dispositif expérimental que dans l'exemple ci-dessus
:ref:`section_tutorials_in_python_explicit`, mais en utilisant des données
issues d'un unique fichier script Python externe.

En premier lieu, on écrit le fichier script suivant, utilisant des noms
conventionnels pour les variables requises. Ici toutes les variables sont
définies dans le même script, mais l'utilisateur peut choisir de séparer le
fichier en plusieurs autres, ou de mélanger une définition explicite des
données dans l'interface textuelle ADAO et une définition implicite dans des
fichiers externes. Le fichier script actuel ressemble à:
::

    import numpy
    #
    # Definition of the Background as a vector
    # ----------------------------------------
    Background = [0, 0, 0]
    #
    # Definition of the Observation as a vector
    # -----------------------------------------
    Observation = "1 1 1"
    #
    # Definition of the Background Error covariance as a matrix
    # ---------------------------------------------------------
    BackgroundError = numpy.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    #
    # Definition of the Observation Error covariance as a matrix
    # ----------------------------------------------------------
    ObservationError = numpy.matrix("1 0 0 ; 0 1 0 ; 0 0 1")
    #
    # Definition of the Observation Operator as a matrix
    # --------------------------------------------------
    ObservationOperator = numpy.identity(3)

Les noms des variables Python sont obligatoires, de manière à définir les
bonnes variables dans le cas ADAO, mais le script Python peut être plus
conséquent et définir des classes, des fonctions, des accès à des fichiers ou
des bases de données, etc. avec des noms différents. De plus, le fichier
ci-dessus présente différentes manières de définir des vecteurs ou des
matrices, utilisant des listes, des chaînes de caractères (comme dans Numpy ou
Octave), des types vecteur ou matrice de Numpy, et des fonctions spéciales de
Numpy. Toutes ces syntaxes sont valides.

Après avoir enregistré ce script dans un fichier (nommé ici "*script.py*" pour
l'exemple) à un endroit quelconque dans l'arborescence de l'utilisateur, on
utilise l'interface textuelle pour construire le cas ADAO. La procédure pour
compléter le cas est similaire à celle de l'exemple précédent à part le fait
que, au lieu de choisir l'option "*Vector*" ou "*Matrix*" pour construire
chaque variable, on choisit l'option "*Script*" en indiquant simultanément le
type "*Vector*" ou "*Matrix*" de la variable. Cela permet d'obtenir les
commandes suivantes (que ce soit en console Python, par la commande "*shell*"
de SALOME, dans la console Python de l'interface, ou par le menu d'exécution
d'un script) :
::

    adao@python$ python
    Python 3.6.5 (default, Feb 01 2019, 12:12:12)
    [GCC] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
    >>> from adao import adaoBuilder
    >>> case = adaoBuilder.New()
    >>> case.set( 'AlgorithmParameters', Algorithm='Blue' )
    >>> case.set( 'Observation',         Vector=True, Script="script.py" )
    >>> case.set( 'ObservationError',    Matrix=True, Script="script.py" )
    >>> case.set( 'Background',          Vector=True, Script="script.py" )
    >>> case.set( 'BackgroundError',     Matrix=True, Script="script.py" )
    >>> case.set( 'ObservationOperator', Matrix=True, Script="script.py" )
    >>> case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
    >>> case.execute()
    Analysis [0.5 0.5 0.5]
    0
    >>>

Les autres étapes et résultats sont exactement les mêmes que dans l'exemple
précédent :ref:`section_tutorials_in_python_explicit`.

Dans la pratique, cette démarche par scripts est la manière la plus facile pour
récupérer des informations depuis des calculs en ligne ou préalables, depuis des
fichiers statiques, depuis des bases de données ou des flux informatiques,
chacun pouvant être dans ou hors SALOME. Cela permet aussi de modifier aisément
des données d'entrée, par exemple à des fin de débogage ou pour des traitements
répétitifs, et c'est la méthode la plus polyvalente pour paramétrer les données
d'entrée. **Mais attention, la méthodologie par scripts n'est pas une procédure
"sûre", en ce sens que des données erronées ou des erreurs dans les calculs,
peuvent être directement introduites dans l'exécution du cas ADAO.
L'utilisateur doit vérifier avec attention le contenu de ses scripts.**
