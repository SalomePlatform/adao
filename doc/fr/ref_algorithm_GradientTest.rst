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

.. index:: single: GradientTest
.. _section_ref_algorithm_GradientTest:

Algorithme de vérification "*GradientTest*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet de vérifier la qualité du gradient de l'opérateur, en
calculant un résidu dont les propriétés théoriques sont connues. Plusieurs
formules de résidu sont disponibles.

Dans tous les cas, on prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.

Résidu "Taylor"
***************

On observe le résidu issu du développement de Taylor de la fonction :math:`F`,
normalisé par la valeur au point nominal :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{|| F(\mathbf{x}) ||}

Si le résidu décroit et que la décroissance se fait en :math:`\alpha^2` selon
:math:`\alpha`, cela signifie que le gradient est bien calculé jusqu'à la
précision d'arrêt de la décroissance quadratique, et que :math:`F` n'est pas
linéaire.

Si le résidu décroit et que la décroissance se fait en :math:`\alpha` selon
:math:`\alpha`, jusqu'à un certain seuil après lequel le résidu est faible et
constant, cela signifie que :math:`F` est linéaire et que le résidu décroit à
partir de l'erreur faite dans le calcul du terme :math:`\nabla_xF`.

Résidu "TaylorOnNorm"
*********************

On observe le résidu issu du développement de Taylor de la fonction :math:`F`,
rapporté au paramètre :math:`\alpha` au carré :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{\alpha^2}

C'est un résidu essentiellement similaire au critère classique de Taylor décrit
précédemment, mais son comportement peut différer selon les propriétés
numériques des calculs de ses différents termes.

Si le résidu est constant jusqu'à un certain seuil et croissant ensuite, cela
signifie que le gradient est bien calculé jusqu'à cette précision d'arrêt, et
que :math:`F` n'est pas linéaire.

Si le résidu est systématiquement croissant en partant d'une valeur faible par
rapport à :math:`||F(\mathbf{x})||`, cela signifie que :math:`F` est
(quasi-)linéaire et que le calcul du gradient est correct jusqu'au moment où le
résidu est de l'ordre de grandeur de :math:`||F(\mathbf{x})||`.

Résidu "Norm"
*************

On observe le résidu, qui est basé sur une approximation du gradient :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) ||}{\alpha}

qui doit rester constant jusqu'à ce que l'on atteigne la précision du calcul.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
.. index:: single: ResiduFormula
.. index:: single: SetSeed
.. index:: single: StoreSupplementaryCalculations

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  CheckingPoint
    *Commande obligatoire*. Elle définit le vecteur utilisé comme l'état autour
    duquel réaliser le test requis, noté :math:`\mathbf{x}` et similaire à
    l'ébauche :math:`\mathbf{x}^b`. Sa valeur est définie comme un objet de type
    "*Vector*".

  ObservationOperator
    *Commande obligatoire*. Elle indique l'opérateur d'observation, notée
    précédemment :math:`H`, qui transforme les paramètres d'entrée
    :math:`\mathbf{x}` en résultats :math:`\mathbf{y}` qui sont à comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est définie comme un objet de
    type "*Function*". Différentes formes fonctionnelles peuvent être
    utilisées, comme décrit dans la section
    :ref:`section_ref_operator_requirements`. Si un contrôle :math:`U` est
    inclus dans le modèle d'observation, l'opérateur doit être appliqué à une
    paire :math:`(X,U)`.

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_checking_keywords`. De plus, les
paramètres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  AmplitudeOfInitialDirection
    Cette clé indique la mise à l'échelle de la perturbation initiale construite
    comme un vecteur utilisé pour la dérivée directionnelle autour du point
    nominal de vérification. La valeur par défaut est de 1, ce qui signifie pas
    de mise à l'échelle.

    Exemple : ``{"AmplitudeOfInitialDirection":0.5}``

  EpsilonMinimumExponent
    Cette clé indique la valeur de l'exposant minimal du coefficient en
    puissance de 10 qui doit être utilisé pour faire décroître le multiplicateur
    de l'incrément. La valeur par défaut est de -8, et elle doit être entre 0 et
    -20. Par exemple, la valeur par défaut conduit à calculer le résidu de la
    formule avec un incrément fixe multiplié par 1.e0 jusqu'à 1.e-8.

    Exemple : ``{"EpsilonMinimumExponent":-12}``

  InitialDirection
    Cette clé indique la direction vectorielle utilisée pour la dérivée
    directionnelle autour du point nominal de vérification. Cela doit être un
    vecteur. Si elle n'est pas spécifiée, la direction par défaut est une
    perturbation par défaut autour de zéro de la même taille vectorielle que le
    point de vérification.

    Exemple : ``{"InitialDirection":[0.1,0.1,100.,3}``

  ResiduFormula
    Cette clé indique la formule de résidu qui doit être utilisée pour le test.
    Le choix par défaut est "Taylor", et les choix possibles sont "Taylor"
    (résidu du développement de Taylor normalisé de l'opérateur, qui doit
    décroître comme le carré de la perturbation), "TaylorOnNorm" (résidu du
    développement de Taylor rapporté à la perturbation de l'opérateur, qui doit
    rester constant) et "Norm" (résidu obtenu en prenant la norme du
    développement de Taylor à l'ordre 0, qui approxime le gradient, et qui doit
    rester constant).

    Exemple : ``{"ResiduFormula":"Taylor"}``

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

    Exemple : ``{"SetSeed":1000}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["CurrentState", "Residu",
    "SimulatedObservationAtCurrentState"].

    Exemple : ``{"StoreSupplementaryCalculations":["CurrentState"]}``

Informations et variables disponibles à la fin de l'algorithme
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En sortie, après exécution de l'algorithme, on dispose d'informations et de
variables issues du calcul. La description des
:ref:`section_ref_output_variables` indique la manière de les obtenir par la
méthode nommée ``get`` de la variable "*ADD*" du post-processing. Les variables
d'entrée, mises à disposition de l'utilisateur en sortie pour faciliter
l'écriture des procédures de post-processing, sont décrites dans
l':ref:`subsection_r_o_v_Inventaire`.

Les sorties non conditionnelles de l'algorithme sont les suivantes:

  Residu
    *Liste de valeurs*. Chaque élément est la valeur du résidu particulier
    vérifié lors d'un algorithme de vérification, selon l'ordre des tests
    effectués.

    Exemple : ``r = ADD.get("Residu")[:]``

Les sorties conditionnelles de l'algorithme sont les suivantes:

  CurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'état courant utilisé
    au cours du déroulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'état courant, c'est-à-dire dans l'espace des observations.

    Exemple : ``hxs = ADD.get("SimulatedObservationAtCurrentState")[-1]``

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`
  - :ref:`section_ref_algorithm_LinearityTest`
  - :ref:`section_ref_algorithm_TangentTest`
  - :ref:`section_ref_algorithm_AdjointTest`
