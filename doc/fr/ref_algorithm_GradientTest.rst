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

.. index:: single: GradientTest
.. _section_ref_algorithm_GradientTest:

Algorithme de vérification "*GradientTest*"
-------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de vérifier la qualité du gradient de l'opérateur, en
calculant un résidu dont les propriétés théoriques sont connues. Plusieurs
formules de résidu sont disponibles. Le test est applicable à un opérateur
quelconque, d'évolution comme d'observation.

Pour toutes les formules, avec :math:`\mathbf{x}` le point courant de
vérification, on prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha_0*\mathbf{dx}_0` avec :math:`\alpha_0` un paramètre
utilisateur de mise à l'échelle, par défaut à 1. :math:`F` est l'opérateur ou
le code de calcul (qui est ici acquis par la commande d'opérateur d'observation
"*ObservationOperator*").

Résidu "Taylor"
***************

On observe le résidu issu du développement de Taylor de la fonction :math:`F`,
normalisé par la valeur au point nominal :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{|| F(\mathbf{x}) ||}

Si le résidu décroît et que la décroissance se fait en :math:`\alpha^2` selon
:math:`\alpha`, cela signifie que le gradient est bien calculé jusqu'à la
précision d'arrêt de la décroissance quadratique, et que :math:`F` n'est pas
linéaire.

Si le résidu décroît et que la décroissance se fait en :math:`\alpha` selon
:math:`\alpha`, jusqu'à un certain seuil après lequel le résidu est faible et
constant, cela signifie que :math:`F` est linéaire et que le résidu décroît à
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

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/AmplitudeOfInitialDirection.rst

.. include:: snippets/AmplitudeOfTangentPerturbation.rst

.. include:: snippets/EpsilonMinimumExponent.rst

.. include:: snippets/InitialDirection.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/ResiduFormula_GradientTest.rst

.. include:: snippets/SetSeed.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *Liste de noms*. Cette liste indique les noms des variables supplémentaires,
  qui peuvent être disponibles au cours du déroulement ou à la fin de
  l'algorithme, si elles sont initialement demandées par l'utilisateur. Leur
  disponibilité implique, potentiellement, des calculs ou du stockage coûteux.
  La valeur par défaut est donc une liste vide, aucune de ces variables n'étant
  calculée et stockée par défaut (sauf les variables inconditionnelles). Les
  noms possibles pour les variables supplémentaires sont dans la liste suivante
  (la description détaillée de chaque variable nommée est donnée dans la suite
  de cette documentation par algorithme spécifique, dans la sous-partie
  "*Informations et variables disponibles à la fin de l'algorithme*") : [
  "CurrentState",
  "Residu",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Residu.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/Residu.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_GradientTest_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LinearityTest`
- :ref:`section_ref_algorithm_TangentTest`
- :ref:`section_ref_algorithm_AdjointTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`
