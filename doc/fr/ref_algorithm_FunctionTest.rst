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

.. index:: single: FunctionTest
.. _section_ref_algorithm_FunctionTest:

Algorithme de vérification "*FunctionTest*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet de vérifier que l'opérateur d'observation fonctionne
correctement et que son appel se déroule de manière compatible avec son usage
dans les algorithmes d'ADAO. De manière pratique, il permet d'appeler une ou
plusieurs fois l'opérateur, en activant ou non le mode "debug" lors de
l'exécution.

Une statistique sur les vecteurs en entrée et en sortie de chaque exécution de
l'opérateur est indiquée, et une autre globale est fournie de manière
récapitulative à la fin de l'algorithme de vérification. La précision
d'affichage est contrôlable pour permettre l'automatisation des tests
d'opérateur.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: CheckingPoint
.. index:: single: ObservationOperator
.. index:: single: NumberOfPrintedDigits
.. index:: single: NumberOfRepetition
.. index:: single: SetDebug

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
paramètres de la commande "*AlgorithmParameters*" permettent d'indiquer les options
particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  NumberOfPrintedDigits
    Cette clé indique le nombre de décimales de précision pour les affichages de
    valeurs réelles. La valeur par défaut est 5, avec un minimum de 0.

    Exemple : ``{"NumberOfPrintedDigits":5}``

  NumberOfRepetition
    Cette clé indique le nombre de fois où répéter l'évaluation de la fonction.
    La valeur par défaut est 1.

    Exemple : ``{"NumberOfRepetition":3}``

  SetDebug
    Cette clé requiert l'activation, ou pas, du mode de débogage durant
    l'évaluation de la fonction. La valeur par défaut est "True", les choix sont
    "True" ou "False".

    Exemple : ``{"SetDebug":False}``

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_LinearityTest`
