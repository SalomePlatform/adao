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

.. _section_ref_operator_requirements:

Conditions requises pour les fonctions décrivant un opérateur
-------------------------------------------------------------

.. index:: single: setObservationOperator
.. index:: single: setEvolutionModel
.. index:: single: setControlModel

La disponibilité des opérateurs d'observation et parfois d'évolution sont
nécessaires pour mettre en oeuvre les procédures d'assimilation de données ou
d'optimisation. Comme l'opérateur d'évolution est considéré dans sa forme
incrémentale, qui représente la transition entre deux états successifs, il est
alors formellement similaire à l'opérateur d'observation et la manière de les
décrire est unique.

Ces opérateurs comprennent la **simulation physique par des calculs
numériques**. Mais ils comprennent aussi **le filtrage, la projection ou la
restriction** des grandeurs simulées, qui sont nécessaires pour comparer la
simulation à l'observation.

Schématiquement, un opérateur :math:`O` a pour objet de restituer une
simulation ou une solution pour des paramètres d'entrée spécifiés. Une partie
des paramètres d'entrée peut être modifiée au cours de la procédure
d'optimisation. Ainsi, la représentation mathématique d'un tel processus est
une fonction. Il a été brièvement décrit dans la section :ref:`section_theory`.
Il est généralisé ici par la relation:

.. math:: \mathbf{y} = O( \mathbf{x} )

entre les pseudo-observations en sortie :math:`\mathbf{y}` et les paramètres
d'entrée :math:`\mathbf{x}` en utilisant l'opérateur :math:`O` d'observation ou
d'évolution. La même représentation fonctionnelle peut être utilisée
pour le modèle linéaire tangent :math:`\mathbf{O}` de :math:`O` et son adjoint
:math:`\mathbf{O}^*` qui sont aussi requis par certains algorithmes
d'assimilation de données ou d'optimisation.

En entrée et en sortie de ces opérateurs, les variables :math:`\mathbf{x}` et
:math:`\mathbf{y}`, ou leurs incréments, sont mathématiquement des vecteurs, et
ils peuvent donc être donnés par l'utilisateur comme des vecteurs non-orientés
(de type liste ou vecteur Numpy) ou orientés (de type matrice Numpy).

Ainsi, **pour décrire de manière complète un opérateur, l'utilisateur n'a qu'à
fournir une fonction qui réalise complètement et uniquement l'opération
fonctionnelle**.

Cette fonction est généralement donnée comme une **fonction ou un script
Python**, qui peuvent en particulier être exécutée comme une fonction Python
indépendante ou dans un noeud YACS. Cette fonction ou ce script peuvent, sans
différences, lancer des codes externes ou utiliser des appels et des méthodes
internes Python ou SALOME. Si l'algorithme nécessite les 3 aspects de
l'opérateur (forme directe, forme tangente et forme adjointe), l'utilisateur
doit donner les 3 fonctions ou les approximer grâce à ADAO.

Il existe pour l'utilisateur 3 méthodes effectives de fournir une représentation
fonctionnelle de l'opérateur, qui diffèrent selon le type d'argument choisi:

- :ref:`section_ref_operator_one`
- :ref:`section_ref_operator_funcs`
- :ref:`section_ref_operator_switch`

Dans le cas de l'interface textuelle d'ADAO (TUI), seules les deux premières
sont nécessaires car la troisième est incluse dans la seconde. Dans le cas de
l'interface graphique EFICAS d'ADAO, ces méthodes sont choisies dans le champ
"*FROM*" de chaque opérateur ayant une valeur "*Function*" comme
"*INPUT_TYPE*", comme le montre la figure suivante :

  .. eficas_operator_function:
  .. image:: images/eficas_operator_function.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir graphiquement une représentation fonctionnelle de l'opérateur**

En interface textuelle d'ADAO (TUI), dans le cas précis illustré ci-dessus, on
réalise la même démarche en écrivant :
::

    ...
    case.set( 'ObservationOperator',
        OneFunction = True,
        Script = 'scripts_for_JDC.py'
        )
    ...

.. _section_ref_operator_one:

Première forme fonctionnelle : un seul opérateur direct
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: OneFunction
.. index:: single: ScriptWithOneFunction
.. index:: single: DirectOperator
.. index:: single: DifferentialIncrement
.. index:: single: CenteredFiniteDifference

La première consiste à ne fournir qu'une seule fonction, potentiellement non
linéaire, et à approximer les opérateurs tangent et adjoint associés.

Ceci est fait dans ADAO en utilisant, dans l'interface graphique EFICAS d'ADAO,
le mot-clé "*ScriptWithOneFunction*" pour la description par un script. Dans
l'interface textuelle, c'est le mot-clé "*OneFunction*", éventuellement combiné
avec le mot-clé "*Script*" selon que c'est une fonction ou un script. Si c'est
par script externe, l'utilisateur doit fournir un fichier contenant une
fonction qui porte le nom obligatoire "*DirectOperator*". Par exemple, un
script externe peut suivre le modèle générique suivant::

    def DirectOperator( X ):
        """ Opérateur direct de simulation non-linéaire """
        ...
        ...
        ...
        # Résultat : Y = O(X)
        return "un vecteur similaire à Y"

Dans ce cas, l'utilisateur doit aussi fournir une valeur pour l'incrément
différentiel ou conserver la valeur par défaut. Cela se réalise en utilisant
dans l'interface graphique (GUI) ou textuelle (TUI) le mot-clé
"*DifferentialIncrement*" comme paramètre, qui a une valeur par défaut de 1%.
Ce coefficient est utilisé dans l'approximation différences finies pour
construire les opérateurs tangent et adjoint. L'ordre de l'approximation
différences finies peut aussi être choisi à travers l'interface, en utilisant
le mot-clé "*CenteredFiniteDifference*", avec ``False`` ou 0 pour un schéma non
centré du premier ordre (qui est la valeur par défaut), et avec ``True`` ou 1
pour un schéma centré du second ordre (et qui coûte numériquement deux fois
plus cher que le premier ordre). Si nécessaire et si possible, on peut
:ref:`subsection_ref_parallel_df`. Dans tous les cas, un mécanisme de cache
interne permet de limiter le nombre d'évaluations de l'opérateur au minimum
possible du point de vue de l'exécution séquentielle ou parallèle des
approximations numériques des opérateurs tangent et adjoint, pour éviter des
calculs redondants. On se reportera à la partie permettant de
:ref:`subsection_iterative_convergence_control` pour connaître l'interaction
avec les paramètres relatifs à la convergence.

Cette première forme de définition de l'opérateur permet aisément de tester la
forme fonctionnelle avant son usage dans un cas ADAO, réduisant notablement la
complexité de l'implémentation de l'opérateur. On peut ainsi utiliser
l'algorithme ADAO de vérification "*FunctionTest*" (voir la section sur
l':ref:`section_ref_algorithm_FunctionTest`) spécifiquement prévu pour ce test.

**Important :** le nom "*DirectOperator*" est obligatoire lorsque l'on utilise
un script Python indépendant. Le type de l'argument ``X`` en entrée peut être
une liste de valeurs réelles, un vecteur Numpy ou une matrice Numpy, et la
fonction utilisateur doit accepter et traiter tous ces cas. Le type de
l'argument ``Y`` en sortie doit aussi être équivalent à une liste de valeurs
réelles.

Des formes variées d'opérateurs sont disponibles dans les divers scripts inclus
dans les :ref:`section_docu_examples`.

.. _section_ref_operator_funcs:

Seconde forme fonctionnelle : trois opérateurs direct, tangent et adjoint
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ThreeFunctions
.. index:: single: ScriptWithFunctions
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

.. warning::

  En général, il est recommandé d'utiliser la première forme fonctionnelle
  plutôt que la seconde. Un petit accroissement de performances n'est pas une
  bonne raison pour utiliser l'implémentation détaillée de cette seconde forme
  fonctionnelle.

La seconde consiste à fournir directement les trois opérateurs liés :math:`O`,
:math:`\mathbf{O}` et :math:`\mathbf{O}^*`. C'est effectué en utilisant le
mot-clé "*ScriptWithFunctions*" pour la description de l'opérateur choisi dans
l'interface graphique EFICAS d'ADAO. Dans l'interface textuelle, c'est le
mot-clé "*ThreeFunctions*", éventuellement combiné avec le mot-clé "*Script*"
selon que c'est une fonction ou un script. L'utilisateur doit fournir dans un
script trois fonctions, avec les trois noms obligatoires "*DirectOperator*",
"*TangentOperator*" et "*AdjointOperator*". Par exemple, le script externe peut
suivre le squelette suivant::

    def DirectOperator( X ):
        """ Opérateur direct de simulation non-linéaire """
        ...
        ...
        ...
        return "un vecteur similaire à Y"

    def TangentOperator( paire = (X, dX) ):
        """ Opérateur linéaire tangent, autour de X, appliqué à dX """
        X, dX = paire
        ...
        ...
        ...
        return "un vecteur similaire à Y"

    def AdjointOperator( paire = (X, Y) ):
        """ Opérateur adjoint, autour de X, appliqué à Y """
        X, Y = paire
        ...
        ...
        ...
        return "un vecteur similaire à X"

Une nouvelle fois, cette seconde définition d'opérateur permet aisément de
tester les formes fonctionnelles avant de les utiliser dans le cas ADAO,
réduisant la complexité de l'implémentation de l'opérateur.

Pour certains algorithmes (en particulier les filtres non ensemblistes), il
faut que les fonctions tangente et adjointe puissent renvoyer les matrices
équivalentes à l'opérateur linéaire. Dans ce cas, lorsque, respectivement, les
arguments ``dX`` ou ``Y`` valent ``None``, le script de l'utilisateur doit
renvoyer la matrice associée. Les squelettes des fonctions "*TangentOperator*"
et "*AdjointOperator*" deviennent alors les suivants::

    def TangentOperator( paire = (X, dX) ):
        """ Opérateur linéaire tangent, autour de X, appliqué à dX """
        X, dX = paire
        ...
        ...
        ...
        if dX is None or len(dX) == 0:
            return "la matrice de l'opérateur linéaire tangent"
        else:
            return "un vecteur similaire à Y"

    def AdjointOperator( paire = (X, Y) ):
        """ Opérateur adjoint, autour de X, appliqué à Y """
        X, Y = paire
        ...
        ...
        ...
        if Y is None or len(Y) == 0:
            return "la matrice de l'opérateur linéaire adjoint"
        else:
            return "un vecteur similaire à X"

**Important :** les noms "*DirectOperator*", "*TangentOperator*" et
"*AdjointOperator*" sont obligatoires lorsque l'on utilise un script Python
indépendant. Le type des arguments en entrée ou en sortie ``X``, ``Y``, ``dX``
peut être une liste de valeur réelles, un vecteur Numpy ou une matrice Numpy.
La fonction utilisateur doit accepter et traiter tous ces cas.

.. _section_ref_operator_switch:

Troisième forme fonctionnelle : trois opérateurs avec un branchement
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithSwitch
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

.. warning::

  Il est recommandé de ne pas utiliser cette troisième forme fonctionnelle sans
  une solide raison numérique ou physique. Un accroissement de performances
  n'est pas une bonne raison pour utiliser la complexité de cette troisième
  forme fonctionnelle. Seule une impossibilité à utiliser les première ou
  seconde formes justifie l'usage de la troisième.

La troisième forme donne de plus grandes possibilités de contrôle de
l'exécution des trois fonctions représentant l'opérateur, permettant un usage
et un contrôle avancés sur chaque exécution du code de simulation. C'est
réalisable en utilisant le mot-clé "*ScriptWithSwitch*" pour la description de
l'opérateur à travers l'interface graphique EFICAS d'ADAO. Dans l'interface
textuelle, il suffit d'utiliser le mot-clé "*ThreeFunctions*" précédent pour
définir aussi ce cas, en indiquant les fonctions adéquates. L'utilisateur doit
fournir un script unique aiguillant, selon un contrôle, l'exécution des formes
directe, tangente et adjointe du code de simulation. L'utilisateur peut alors,
par exemple, utiliser des approximations pour les codes tangent et adjoint, ou
introduire une plus grande complexité du traitement des arguments des
fonctions. Mais cette démarche sera plus difficile à implémenter et à déboguer.

Toutefois, si vous souhaitez utiliser cette troisième forme, on recommande de
se baser sur le modèle suivant pour le script d'aiguillage. Il nécessite un
fichier script ou un code externe nommé ici
"*Physical_simulation_functions.py*", contenant trois fonctions nommées
"*DirectOperator*", "*TangentOperator*" et "*AdjointOperator*" comme
précédemment. Voici le squelette d'aiguillage:
::

    import Physical_simulation_functions
    import numpy, logging, codecs, pickle
    def loads( data ):
        return pickle.loads(codecs.decode(data.encode(), "base64"))
    #
    method = ""
    for param in computation["specificParameters"]:
        if param["name"] == "method":
            method = loads(param["value"])
    if method not in ["Direct", "Tangent", "Adjoint"]:
        raise ValueError("No valid computation method is given")
    logging.info("Found method is \'%s\'"%method)
    #
    logging.info("Loading operator functions")
    Function = Physical_simulation_functions.DirectOperator
    Tangent  = Physical_simulation_functions.TangentOperator
    Adjoint  = Physical_simulation_functions.AdjointOperator
    #
    logging.info("Executing the possible computations")
    data = []
    if method == "Direct":
        logging.info("Direct computation")
        Xcurrent = computation["inputValues"][0][0][0]
        data = Function(numpy.matrix( Xcurrent ).T)
    if method == "Tangent":
        logging.info("Tangent computation")
        Xcurrent  = computation["inputValues"][0][0][0]
        dXcurrent = computation["inputValues"][0][0][1]
        data = Tangent(numpy.matrix(Xcurrent).T, numpy.matrix(dXcurrent).T)
    if method == "Adjoint":
        logging.info("Adjoint computation")
        Xcurrent = computation["inputValues"][0][0][0]
        Ycurrent = computation["inputValues"][0][0][1]
        data = Adjoint((numpy.matrix(Xcurrent).T, numpy.matrix(Ycurrent).T))
    #
    logging.info("Formatting the output")
    it = numpy.ravel(data)
    outputValues = [[[[]]]]
    for val in it:
      outputValues[0][0][0].append(val)
    #
    result = {}
    result["outputValues"]        = outputValues
    result["specificOutputInfos"] = []
    result["returnCode"]          = 0
    result["errorMessage"]        = ""

Toutes les modifications envisageables peuvent être faites à partir de cette
hypothèse de squelette.

.. _section_ref_operator_control:

Cas spécial d'un opérateur d'évolution avec contrôle
++++++++++++++++++++++++++++++++++++++++++++++++++++

Dans certains cas, l'opérateur d'évolution ou d'observation doit être contrôlé
par un contrôle d'entrée externe, qui est donné *a priori*. Dans ce cas, la
forme générique du modèle incrémental :math:`O` est légèrement modifiée comme
suit :

.. math:: \mathbf{y} = O( \mathbf{x}, \mathbf{u})

où :math:`\mathbf{u}` est le contrôle sur l'incrément d'état. En effet,
l'opérateur direct doit être appliqué à une paire de variables :math:`(X,U)`.
Schématiquement, l'opérateur :math:`O` doit être construit comme une fonction
applicable sur une paire :math:`\mathbf{(X, U)}` comme suit :
::

    def DirectOperator( paire = (X, U) ):
        """ Opérateur direct de simulation non-linéaire """
        X, U = paire
        ...
        ...
        ...
        return quelque chose comme X(n+1) (évolution) ou Y(n+1) (observation)

Les opérateurs tangent et adjoint ont la même signature que précédemment, en
notant que les dérivées doivent être faites seulement partiellement par rapport
à :math:`\mathbf{x}`. Dans un tel cas de contrôle explicite, seule la deuxième
forme fonctionnelle (en utilisant "*ScriptWithFunctions*") et la troisième
forme fonctionnelle (en utilisant "*ScriptWithSwitch*") peuvent être utilisées.

.. _section_ref_operator_dimensionless:

Remarques complémentaires sur l'adimensionnement des opérateurs
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Adimensionnement
.. index:: single: Sans dimension

Il est fréquent que les grandeurs physiques, en entrée ou en sortie des
opérateurs, présentent des différences notables d'ordre de grandeur ou de taux
de variation. Une manière d'éviter des difficultés numériques est d'utiliser,
ou d'établir, un adimensionnement des calculs menés dans les opérateurs
[WikipediaND]_. Par principe, dans la mesure où la simulation de la physique
devrait être la plus adimensionnée possible, il est en premier lieu recommandé
d'utiliser les capacités existantes d'adimensionnement du code de calcul.

Néanmoins, dans le cas courant où l'on ne peut en disposer, il est souvent
utile d'environner le calcul pour l'adimensionner en entrée ou en sortie. Une
manière simple de faire cela en entrée consiste à transformer les paramètres
:math:`\mathbf{x}` en argument d'une fonction comme "*DirectOperator*". On
utilise le plus souvent comme référence les valeurs par défaut
:math:`\mathbf{x}^b` (ébauche, ou valeur nominale). Pourvu que chaque
composante de :math:`\mathbf{x}^b` soit non nulle, on peut ensuite procéder par
correction multiplicative. Pour cela, on peut par exemple poser :

.. math:: \mathbf{x} = \mathbf{\alpha}\mathbf{x}^b

et optimiser ensuite le paramètre multiplicatif :math:`\mathbf{\alpha}`. Ce
paramètre a pour valeur par défaut (ou pour ébauche) un vecteur de 1. De
manière similaire, on peut procéder par correction additive si c'est plus
judicieux pour la physique sous-jacente. Ainsi, dans ce cas, on peut poser :

.. math:: \mathbf{x} =\mathbf{x}^b + \mathbf{\alpha}

et optimiser ensuite le paramètre additif :math:`\mathbf{\alpha}`. Cette fois,
ce paramètre a pour valeur d'ébauche un vecteur de 0.

Attention, l'application d'une démarche d'adimensionnement nécessite aussi la
modification des covariances d'erreurs associées dans la formulation globale du
problème d'optimisation.

Une telle démarche suffit rarement à éviter tous les problèmes numériques, mais
permet souvent d'améliorer beaucoup le conditionnement numérique de
l'optimisation.

.. index:: single: InputFunctionAsMulti

Gestion explicite de fonctions "multiples"
++++++++++++++++++++++++++++++++++++++++++

.. warning::

  Il est fortement recommandé de ne pas utiliser cette gestion explicite de
  fonctions "multiples" sans une très solide raison informatique pour le faire.
  Cette gestion est déjà effectuée par défaut dans ADAO pour l'amélioration des
  performances. Seul l'utilisateur très averti, cherchant à gérer des cas
  particulièrement difficiles, peut s'intéresser à cette extension. En dépit de
  sa simplicité, c'est au risque explicite de dégrader notablement les
  performances, ou d'avoir des erreurs d'exécution étranges.

Il est possible, lorsque l'on fournit des fonctions d'opérateurs, de les
définir comme des fonctions qui traitent non pas un seul argument, mais une
série d'arguments, pour restituer en sortie la série des valeurs
correspondantes. En pseudo-code, la fonction "multiple", ici nommée
``MultiFunctionO``, représentant l'opérateur classique :math:`O` nommé
"*DirectOperator*", effectue :
::

    def MultiFunctionO( Inputs ):
        """ Multiple ! """
        Outputs = []
        for X in Inputs:
            Y = DirectOperator( X )
            Outputs.append( Y )
        return Outputs

La longueur de la sortie (c'est-à-dire le nombre de valeurs calculées) est
égale à la longueur de l'entrée (c'est-à-dire le nombre d'états dont on veut
calculer la valeur par l'opérateur).

Cette possibilité n'est disponible que dans l'interface textuelle TUI d'ADAO.
Pour cela, lors de la définition d'une fonction d'opérateur, en même temps que
l'on définit de manière habituelle la fonction ou le script externe, il suffit
d'indiquer en plus en argument par un booléen supplémentaire
"*InputFunctionAsMulti*" que la définition est celle d'une fonction "multiple".
Par exemple, si c'est l'opérateur d'observation que l'on définit de cette
manière, il faut écrire (sachant que toutes les autres commandes optionnelles
restent inchangées) :
::

    case.set( 'ObservationOperator',
        OneFunction          = MultiFunctionO,
        ...
        InputFunctionAsMulti = True,
        )
