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

Exigences pour les fonctions d�crivant un op�rateur
---------------------------------------------------

Les op�rateurs d'observation et d'�volution sont n�cessaires pour mettre en
oeuvre les proc�dures d'assimilation de donn�es ou d'optimisation. Ils
comprennent la simulation physique par des calculs num�riques, mais aussi le
filtrage et de restriction pour comparer la simulation � l'observation.
L'op�rateur d'�volution est ici consid�r� dans sa forme incr�mentale, qui
repr�sente la transition entre deux �tats successifs, et il est alors similaire
� l'op�rateur d'observation.

Sch�matiquement, un op�rateur doit donner une solution �tant donn� les
param�tres d'entr�e. Une partie des param�tres d'entr�e peut �tre modifi�e au
cours de la proc�dure d'optimisation. Ainsi, la repr�sentation math�matique d'un
tel processus est une fonction. Il a �t� bri�vement d�crit dans la section
:ref:`section_theory` et il est g�n�ralis�e ici par la relation:

.. math:: \mathbf{y} = O( \mathbf{x} )

entre les pseudo-observations :math:`\mathbf{y}` et les param�tres
:math:`\mathbf{x}` en utilisant l'op�rateur d'observation ou d'�volution
:math:`O`. La m�me repr�sentation fonctionnelle peut �tre utilis�e pour le
mod�le lin�aire tangent :math:`\mathbf{O}` de :math:`O` et son adjoint
:math:`\mathbf{O}^*`, qui sont aussi requis par certains algorithmes
d'assimilation de donn�es ou d'optimisation.

En entr�e et en sortie de ces op�rateurs, les variables :math:`\mathbf{x}` et
:math:`\mathbf{y}` ou leurs incr�ments sont math�matiquement des vecteurs, et
ils sont donc pass�s comme des vecteurs non-orient�s (de type liste ou vecteur
Numpy) ou orient�s (de type matrice Numpy).

Ensuite, **pour d�crire compl�tement un op�rateur, l'utilisateur n'a qu'�
fournir une fonction qui r�alise uniquement l'op�ration fonctionnelle de mani�re
compl�te**.

Cette fonction est g�n�ralement donn�e comme un script qui peut �tre ex�cut�
dans un noeud YACS. Ce script peut aussi, sans diff�rences, lancer des codes
externes ou utiliser des appels et des m�thodes internes SALOME. Si l'algorithme
n�cessite les 3 aspects de l'op�rateur (forme directe, forme tangente et forme
adjointe), l'utilisateur doit donner les 3 fonctions ou les approximer.

Il existe 3 m�thodes effectives pour l'utilisateur de fournir une repr�sentation
fonctionnelle de l'op�rateur. Ces m�thodes sont choisies dans le champ "*FROM*"
de chaque op�rateur ayant une valeur "*Function*" comme "*INPUT_TYPE*", comme le
montre la figure suivante:

  .. eficas_operator_function:
  .. image:: images/eficas_operator_function.png
    :align: center
    :width: 100%
  .. centered::
    **Choisir une repr�sentation fonctionnelle de l'op�rateur**

Premi�re forme fonctionnelle : utiliser "*ScriptWithOneFunction*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithOneFunction
.. index:: single: DirectOperator
.. index:: single: DifferentialIncrement
.. index:: single: CenteredFiniteDifference

La premi�re consiste � ne fournir qu'une seule fonction potentiellement non
lin�aire, et d'approximer les op�rateurs tangent et adjoint. Ceci est fait en
utilisant le mot-cl� "*ScriptWithOneFunction*" pour la description de
l'op�rateur choisi dans l'interface graphique ADAO. L'utilisateur doit fournir
la fonction dans un script, avec un nom obligatoire "*DirectOperator*". Par
exemple, le script peut suivre le mod�le suivant::

    def DirectOperator( X ):
        """ Op�rateur direct de simulation non-lin�aire """
        ...
        ...
        ...
        return Y=O(X)

Dans ce cas, l'utilisateur doit aussi fournir une valeur pour l'incr�ment
diff�rentiel (ou conserver la valeur par d�faut), en utilisant dans l'interface
graphique (GUI) le mot-cl� "*DifferentialIncrement*", qui a une valeur par
d�faut de 1%. Ce coefficient est utilis� dans l'approximation diff�rences finies
pour construire les op�rateurs tangent et adjoint. L'ordre de l'approximation
diff�rences finies peut aussi �tre choisi � travers l'interface, en utilisant le
mot-cl� "*CenteredFiniteDifference*", avec 0 pour un sch�ma non centr� du
premier ordre (qui est la valeur par d�faut), et avec 1 pour un sch�ma centr� du
second ordre (qui co�te num�riquement deux fois plus cher que le premier ordre).
Si n�cessaire et si possible, on peut :ref:`subsection_ref_parallel_df`.

Cette premi�re forme de d�finition de l'op�rateur permet ais�ment de tester la
forme fonctionnelle avant son usage dans un cas ADAO, r�duisant notablement la
complexit� de l'impl�mentation de l'op�rateur. On peut ainsi utiliser
l'algorithme ADAO de v�rification "*FunctionTest*" (voir la section sur
l':ref:`section_ref_algorithm_FunctionTest`) pour ce test.

**Avertissement important :** le nom "*DirectOperator*" est obligatoire, et le
type de l'argument ``X`` peut �tre une liste, un vecteur ou une matrice Numpy.
La fonction utilisateur doit accepter et traiter tous ces cas.

Seconde forme fonctionnelle : utiliser "*ScriptWithFunctions*"
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithFunctions
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**En g�n�ral, il est recommand� d'utiliser la premi�re forme fonctionnelle
plut�t que la seconde. Un petit accroissement de performances n'est pas une
bonne raison pour utiliser l'impl�mentation d�taill�e de cette seconde forme
fonctionnelle.**

La seconde consiste � fournir directement les trois op�rateurs li�s :math:`O`,
:math:`\mathbf{O}` et :math:`\mathbf{O}^*`. C'est effectu� en utilisant le
mot-cl� "*ScriptWithFunctions*" pour la description de l'op�rateur choisi dans
l'interface graphique (GUI) d'ADAO. L'utilisateur doit fournir trois fonctions
dans un script, avec trois noms obligatoires "*DirectOperator*",
"*TangentOperator*" et "*AdjointOperator*". Par exemple, le script peut suivre
le squelette suivant::

    def DirectOperator( X ):
        """ Op�rateur direct de simulation non-lin�aire """
        ...
        ...
        ...
        return quelque chose comme Y

    def TangentOperator( (X, dX) ):
        """ Op�rateur lin�aire tangent, autour de X, appliqu� � dX """
        ...
        ...
        ...
        return quelque chose comme Y

    def AdjointOperator( (X, Y) ):
        """ Op�rateur adjoint, autour de X, appliqu� � Y """
        ...
        ...
        ...
        return quelque chose comme X

Un nouvelle fois, cette seconde d�finition d'op�rateur permet ais�ment de tester
les formes fonctionnelles avant de les utiliser dans le cas ADAO, r�duisant la
complexit� de l'impl�mentation de l'op�rateur.

Pour certains algorithmes, il faut que les fonctions tangente et adjointe puisse
renvoyer les matrices �quivalentes � l'op�rateur lin�aire. Dans ce cas, lorsque,
respectivement, les arguments ``dX`` ou ``Y`` valent ``None``, l'utilisateur
doit renvoyer la matrice associ�e.

**Avertissement important :** les noms "*DirectOperator*", "*TangentOperator*"
et "*AdjointOperator*" sont obligatoires, et le type des arguments ``X``,
``Y``, ``dX`` peut �tre une liste, un vecteur ou une matrice Numpy.
La fonction utilisateur doit accepter et traiter tous ces cas.

Troisi�me forme fonctionnelle : utiliser "*ScriptWithSwitch*"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: ScriptWithSwitch
.. index:: single: DirectOperator
.. index:: single: TangentOperator
.. index:: single: AdjointOperator

**Il est recommand� de ne pas utiliser cette troisi�me forme fonctionnelle sans
une solide raison num�rique ou physique. Un accroissement de performances n'est
pas une bonne raison pour utiliser la complexit� de cette troisi�me forme
fonctionnelle. Seule une impossibilit� � utiliser les premi�re ou seconde formes
justifie l'usage de la troisi�me.**

La troisi�me forme donne de plus grandes possibilit�s de contr�le de l'ex�cution
des trois fonctions repr�sentant l'op�rateur, permettant un usage et un contr�le
avanc�s sur chaque ex�cution du code de simulation. C'est r�alisable en
utilisant le mot-cl� "*ScriptWithSwitch*" pour la description de l'op�rateur �
travers l'interface graphique (GUI) d'ADAO. L'utilisateur doit fournir un script
unique aiguillant, selon un contr�le, l'ex�cution des formes directe, tangente
et adjointe du code de simulation. L'utilisateur peut alors, par exemple,
utiliser des approximations pour les codes tangent et adjoint, ou introduire une
plus grande complexit� du traitement des arguments des fonctions. Mais cette
d�marche sera plus difficile � impl�menter et � d�boguer.

Toutefois, si vous souhaitez utiliser cette troisi�me forme, on recommande de se
baser sur le mod�le suivant pour le script d'aiguillage. Il n�cessite un fichier
script ou un code externe nomm� ici "*Physical_simulation_functions.py*",
contenant trois fonctions nomm�es "*DirectOperator*", "*TangentOperator*" et
"*AdjointOperator*" comme pr�c�demment. Voici le squelette d'aiguillage::

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

Toutes les modifications envisageables peuvent �tre faites � partir de cette
hypoth�se de squelette.

Cas sp�cial d'un op�rateur d'�volution avec contr�le
++++++++++++++++++++++++++++++++++++++++++++++++++++

Dans certains cas, l'op�rateur d'�volution ou d'observation doit �tre contr�l�
par un contr�le d'entr�e externe, qui est donn� *a priori*. Dans ce cas, la
forme g�n�rique du mod�le incr�mental est l�g�rement modifi� comme suit:

.. math:: \mathbf{y} = O( \mathbf{x}, \mathbf{u})

o� :math:`\mathbf{u}` est le contr�le sur l'incr�ment d'�tat. En effet,
l'op�rateur direct doit �tre appliqu� � une paire de variables :math:`(X,U)`.
Sch�matiquement, l'op�rateur doit �tre construit comme suit::

    def DirectOperator( (X, U) ):
        """ Op�rateur direct de simulation non-lin�aire """
        ...
        ...
        ...
        return quelque chose comme X(n+1) (�volution) ou Y(n+1) (observation)

Les op�rateurs tangent et adjoint ont la m�me signature que pr�c�demment, en
notant que les d�riv�es doivent �tre faites seulement partiellement par rapport
� :math:`\mathbf{x}`. Dans un tel cas de contr�le explicite, seule la deuxi�me
forme fonctionnelle (en utilisant "*ScriptWithFunctions*") et la troisi�me forme
fonctionnelle (en utilisant "*ScriptWithSwitch*") peuvent �tre utilis�es.
