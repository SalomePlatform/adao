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

.. _section_ref_operator_requirements:

Exigences pour les fonctions décrivant un opérateur
---------------------------------------------------

Les opérateurs d'observation et d'évolution sont nécessaires pour mettre en
oeuvre les procédures d'assimilation de données ou d'optimisation. Ils
comprennent la simulation physique par des calculs numériques, mais aussi le
filtrage et de restriction pour comparer la simulation à l'observation.
L'opérateur d'évolution est ici considéré dans sa forme incrémentale, qui
représente la transition entre deux états successifs, et il est alors similaire
à l'opérateur d'observation.

Schématiquement, un opérateur doit donner une solution étant donné les
paramètres d'entrée. Une partie des paramètres d'entrée peut être modifiée au
cours de la procédure d'optimisation. Ainsi, la représentation mathématique d'un
tel processus est une fonction. Il a été brièvement décrit dans la section
:ref:`section_theory` et il est généralisée ici par la relation:

.. math:: \mathbf{y} = O( \mathbf{x} )

entre les pseudo-observations :math:`\mathbf{y}` et les paramètres
:math:`\mathbf{x}` en utilisant l'opérateur d'observation ou d'évolution
:math:`O`. La même représentation fonctionnelle peut être utilisée pour le
modèle linéaire tangent :math:`\mathbf{O}` de :math:`O` et son adjoint
:math:`\mathbf{O}^*`, qui sont aussi requis par certains algorithmes
d'assimilation de données ou d'optimisation.

En entrée et en sortie de ces opérateurs, les variables :math:`\mathbf{x}` et
:math:`\mathbf{y}` ou leurs incréments sont mathématiquement des vecteurs, et
ils sont donc passés comme des vecteurs non-orientés (de type liste ou vecteur
Numpy) ou orientés (de type matrice Numpy).

Ensuite, **pour décrire complètement un opérateur, l'utilisateur n'a qu'à
fournir une fonction qui réalise uniquement l'opération fonctionnelle de manière
complète**.

Cette fonction est généralement donnée comme un script qui peut être exécuté
dans un noeud YACS. Ce script peut aussi, sans différences, lancer des codes
externes ou utiliser des appels et des méthodes internes SALOME. Si l'algorithme
nécessite les 3 aspects de l'opérateur (forme directe, forme tangente et forme
adjointe), l'utilisateur doit donner les 3 fonctions ou les approximer.

Il existe 3 méthodes effectives pour l'utilisateur de fournir une représentation
fonctionnelle de l'opérateur. Ces méthodes sont choisies dans le champ "*FROM*"
de chaque opérateur ayant une valeur "*Function*" comme "*INPUT_TYPE*", comme le
montre la figure suivante:

  .. eficas_operator_function:
  .. image:: images/eficas_operator_function.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir une représentation fonctionnelle de l'opérateur**

Première forme fonctionnelle : utiliser "*ScriptWithOneFunction*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithOneFunction
.. index:: single: DirectOperator
.. index:: single: DifferentialIncrement
.. index:: single: CenteredFiniteDifference

La première consiste à ne fournir qu'une seule fonction potentiellement non
linéaire, et d'approximer les opérateurs tangent et adjoint. Ceci est fait en
utilisant le mot-clé "*ScriptWithOneFunction*" pour la description de
l'opérateur choisi dans l'interface graphique ADAO. L'utilisateur doit fournir
la fonction dans un script, avec un nom obligatoire "*DirectOperator*". Par
exemple, le script peut suivre le modèle suivant::

    def DirectOperator( X ):
        """ Opérateur direct de simulation non-linéaire """
        ...
        ...
        ...
        return Y=O(X)

Dans ce cas, l'utilisateur doit aussi fournir une valeur pour l'incrément
différentiel (ou conserver la valeur par défaut), en utilisant dans l'interface
graphique (GUI) le mot-clé "*DifferentialIncrement*", qui a une valeur par
défaut de 1%. Ce coefficient est utilisé dans l'approximation différences finies
pour construire les opérateurs tangent et adjoint. L'ordre de l'approximation
différences finies peut aussi être choisi à travers l'interface, en utilisant le
mot-clé "*CenteredFiniteDifference*", avec 0 pour un schéma non centré du
premier ordre (qui est la valeur par défaut), et avec 1 pour un schéma centré du
second ordre (qui coûte numériquement deux fois plus cher que le premier ordre).
Si nécessaire et si possible, on peut :ref:`subsection_ref_parallel_df`.

Cette première forme de définition de l'opérateur permet aisément de tester la
forme fonctionnelle avant son usage dans un cas ADAO, réduisant notablement la
complexité de l'implémentation de l'opérateur. On peut ainsi utiliser
l'algorithme ADAO de vérification "*FunctionTest*" (voir la section sur
l':ref:`section_ref_algorithm_FunctionTest`) pour ce test.

**Avertissement important :** le nom "*DirectOperator*" est obligatoire, et le
type de l'argument ``X`` peut être une liste, un vecteur ou une matrice Numpy.
La fonction utilisateur doit accepter et traiter tous ces cas.

Seconde forme fonctionnelle : utiliser "*ScriptWithFunctions*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithFunctions
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**En général, il est recommandé d'utiliser la première forme fonctionnelle
plutôt que la seconde. Un petit accroissement de performances n'est pas une
bonne raison pour utiliser l'implémentation détaillée de cette seconde forme
fonctionnelle.**

La seconde consiste à fournir directement les trois opérateurs liés :math:`O`,
:math:`\mathbf{O}` et :math:`\mathbf{O}^*`. C'est effectué en utilisant le
mot-clé "*ScriptWithFunctions*" pour la description de l'opérateur choisi dans
l'interface graphique (GUI) d'ADAO. L'utilisateur doit fournir trois fonctions
dans un script, avec trois noms obligatoires "*DirectOperator*",
"*TangentOperator*" et "*AdjointOperator*". Par exemple, le script peut suivre
le squelette suivant::

    def DirectOperator( X ):
        """ Opérateur direct de simulation non-linéaire """
        ...
        ...
        ...
        return quelque chose comme Y

    def TangentOperator( (X, dX) ):
        """ Opérateur linéaire tangent, autour de X, appliqué à dX """
        ...
        ...
        ...
        return quelque chose comme Y

    def AdjointOperator( (X, Y) ):
        """ Opérateur adjoint, autour de X, appliqué à Y """
        ...
        ...
        ...
        return quelque chose comme X

Un nouvelle fois, cette seconde définition d'opérateur permet aisément de tester
les formes fonctionnelles avant de les utiliser dans le cas ADAO, réduisant la
complexité de l'implémentation de l'opérateur.

Pour certains algorithmes, il faut que les fonctions tangente et adjointe puisse
renvoyer les matrices équivalentes à l'opérateur linéaire. Dans ce cas, lorsque,
respectivement, les arguments ``dX`` ou ``Y`` valent ``None``, l'utilisateur
doit renvoyer la matrice associée.

**Avertissement important :** les noms "*DirectOperator*", "*TangentOperator*"
et "*AdjointOperator*" sont obligatoires, et le type des arguments ``X``,
``Y``, ``dX`` peut être une liste, un vecteur ou une matrice Numpy.
La fonction utilisateur doit accepter et traiter tous ces cas.

Troisième forme fonctionnelle : utiliser "*ScriptWithSwitch*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithSwitch
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**Il est recommandé de ne pas utiliser cette troisième forme fonctionnelle sans
une solide raison numérique ou physique. Un accroissement de performances n'est
pas une bonne raison pour utiliser la complexité de cette troisième forme
fonctionnelle. Seule une impossibilité à utiliser les première ou seconde formes
justifie l'usage de la troisième.**

La troisième forme donne de plus grandes possibilités de contrôle de l'exécution
des trois fonctions représentant l'opérateur, permettant un usage et un contrôle
avancés sur chaque exécution du code de simulation. C'est réalisable en
utilisant le mot-clé "*ScriptWithSwitch*" pour la description de l'opérateur à
travers l'interface graphique (GUI) d'ADAO. L'utilisateur doit fournir un script
unique aiguillant, selon un contrôle, l'exécution des formes directe, tangente
et adjointe du code de simulation. L'utilisateur peut alors, par exemple,
utiliser des approximations pour les codes tangent et adjoint, ou introduire une
plus grande complexité du traitement des arguments des fonctions. Mais cette
démarche sera plus difficile à implémenter et à déboguer.

Toutefois, si vous souhaitez utiliser cette troisième forme, on recommande de se
baser sur le modèle suivant pour le script d'aiguillage. Il nécessite un fichier
script ou un code externe nommé ici "*Physical_simulation_functions.py*",
contenant trois fonctions nommées "*DirectOperator*", "*TangentOperator*" et
"*AdjointOperator*" comme précédemment. Voici le squelette d'aiguillage::

    import Physical_simulation_functions
    import numpy, logging
    #
    method = ""
    for param in computation["specificParameters"]:
        if param["name"] == "method":
            method = param["value"]
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

Cas spécial d'un opérateur d'évolution avec contrôle
++++++++++++++++++++++++++++++++++++++++++++++++++++

Dans certains cas, l'opérateur d'évolution ou d'observation doit être contrôlé
par un contrôle d'entrée externe, qui est donné *a priori*. Dans ce cas, la
forme générique du modèle incrémental est légèrement modifié comme suit:

.. math:: \mathbf{y} = O( \mathbf{x}, \mathbf{u})

où :math:`\mathbf{u}` est le contrôle sur l'incrément d'état. En effet,
l'opérateur direct doit être appliqué à une paire de variables :math:`(X,U)`.
Schématiquement, l'opérateur doit être construit comme suit::

    def DirectOperator( (X, U) ):
        """ Opérateur direct de simulation non-linéaire """
        ...
        ...
        ...
        return quelque chose comme X(n+1) (évolution) ou Y(n+1) (observation)

Les opérateurs tangent et adjoint ont la même signature que précédemment, en
notant que les dérivées doivent être faites seulement partiellement par rapport
à :math:`\mathbf{x}`. Dans un tel cas de contrôle explicite, seule la deuxième
forme fonctionnelle (en utilisant "*ScriptWithFunctions*") et la troisième forme
fonctionnelle (en utilisant "*ScriptWithSwitch*") peuvent être utilisées.
