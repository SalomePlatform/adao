..
   Copyright (C) 2008-2014 EDF R&D

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

.. index:: single: LinearityTest
.. _section_ref_algorithm_LinearityTest:

Algorithme de vérification "*LinearityTest*"
--------------------------------------------

Description
+++++++++++

Cet algorithme permet de vérifier la qualité de linéarité de l'opérateur, en
calculant un résidu dont les propriétés théoriques sont connues. Plusieurs
formules de résidu sont utilisables.

Dans tous les cas, on prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.

Résidu "CenteredDL"
*******************

On observe le résidu suivant, provenant de la différence centrée des valeurs de
:math:`F` au point nominal et aux points perturbés, normalisée par la valeur au
point nominal :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) + F(\mathbf{x}-\alpha*\mathbf{dx}) - 2*F(\mathbf{x}) ||}{|| F(\mathbf{x}) ||}

S'il reste constamment très faible par rapport à 1, l'hypothèse de linéarité
de :math:`F` est vérifiée.

Si le résidu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
faible qu'à partir d'un certain ordre d'incrément, l'hypothèse de linéarité
de :math:`F` n'est pas vérifiée.

Si le résidu décroit et que la décroissance se fait en :math:`\alpha^2` selon
:math:`\alpha`, cela signifie que le gradient est bien calculé jusqu'au niveau
d'arrêt de la décroissance quadratique.

Résidu "Taylor"
***************

On observe le résidu issu du développement de Taylor de la fonction :math:`F`,
normalisée par la valeur au point nominal :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{|| F(\mathbf{x}) ||}

S'il reste constamment trés faible par rapport à 1, l'hypothèse de linéarité
de :math:`F` est vérifiée.

Si le résidu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
faible qu'à partir d'un certain ordre d'incrément, l'hypothèse de linéarité
de :math:`F` n'est pas vérifiée.

Si le résidu décroit et que la décroissance se fait en :math:`\alpha^2` selon
:math:`\alpha`, cela signifie que le gradient est bien calculé jusqu'au niveau
d'arrêt de la décroissance quadratique.

Résidu "NominalTaylor"
**********************

On observe le résidu obtenu à partir de deux approximations d'ordre 1 de
:math:`F(\mathbf{x})`, normalisées par la valeur au point nominal :

.. math:: R(\alpha) = \max(|| F(\mathbf{x}+\alpha*\mathbf{dx}) - \alpha * F(\mathbf{dx}) || / || F(\mathbf{x}) ||,|| F(\mathbf{x}-\alpha*\mathbf{dx}) + \alpha * F(\mathbf{dx}) || / || F(\mathbf{x}) ||)

S'il reste constamment égal à 1 à moins de 2 ou 3 pourcents prés (c'est-à-dire
que :math:`|R-1|` reste égal à 2 ou 3 pourcents), c'est que l'hypothèse de
linéarité de :math:`F` est vérifiée.

S'il est égal à 1 sur une partie seulement du domaine de variation de
l'incrément :math:`\alpha`, c'est sur sous-domaine que l'hypothèse de linéarité
de :math:`F` est vérifiée.

Résidu "NominalTaylorRMS"
*************************

On observe le résidu obtenu à partir de deux approximations d'ordre 1 de
:math:`F(\mathbf{x})`, normalisées par la valeur au point nominal, dont on
calcule l'écart quadratique (RMS) avec la valeur au point nominal :

.. math:: R(\alpha) = \max(RMS( F(\mathbf{x}), F(\mathbf{x}+\alpha*\mathbf{dx}) - \alpha * F(\mathbf{dx}) ) / || F(\mathbf{x}) ||,RMS( F(\mathbf{x}), F(\mathbf{x}-\alpha*\mathbf{dx}) + \alpha * F(\mathbf{dx}) ) / || F(\mathbf{x}) ||)

S'il reste constamment égal à 0 à moins de 1 ou 2 pourcents prés, c'est
que l'hypothèse de linéarité de F est vérifiée.

S'il est égal à 0 sur une partie seulement du domaine de variation de
l'incrément :math:`\alpha`, c'est sur cette partie que l'hypothèse de linéarité
de F est vérifiée.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: AmplitudeOfInitialDirection
.. index:: single: EpsilonMinimumExponent
.. index:: single: InitialDirection
.. index:: single: ResiduFormula
.. index:: single: SetSeed

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
sont indiquées dans la :ref:`section_ref_checking_keywords`. En particulier, la
commande optionnelle "*AlgorithmParameters*" permet d'indiquer les options
particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
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
    Le choix par défaut est "CenteredDL", et les choix possibles sont
    "CenteredDL" (résidu de la différence entre la fonction au point nominal et
    ses valeurs avec des incréments positif et négatif, qui doit rester très
    faible), "Taylor" (résidu du développement de Taylor de l'opérateur
    normalisé par sa valeur nominal, qui doit rester très faible),
    "NominalTaylor" (résidu de l'approximation à l'ordre 1 de l'opérateur,
    normalisé au point nominal, qui doit rester proche de 1), et
    "NominalTaylorRMS" (résidu de l'approximation à l'ordre 1 de l'opérateur,
    normalisé par l'écart quadratique moyen (RMS) au point nominal, qui doit
    rester proche de 0).

    Exemple : ``{"ResiduFormula":"CenteredDL"}``

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

    Exemple : ``{"SetSeed":1000}``

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`
