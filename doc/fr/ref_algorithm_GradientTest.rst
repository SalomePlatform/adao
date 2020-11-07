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

.. index:: single: GradientTest
.. _section_ref_algorithm_GradientTest:

Algorithme de vérification "*GradientTest*"
-------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de vérifier la qualité du gradient de l'opérateur, en
calculant un résidu dont les propriétés théoriques sont connues. Plusieurs
formules de résidu sont disponibles.

Dans tous les cas, on prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha_0*\mathbf{dx}_0` avec :math:`\alpha_0` un paramètre
utilisateur de mise à l'échelle, par défaut à 1. :math:`F` est le code de
calcul.

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

.. include:: snippets/EpsilonMinimumExponent.rst

.. include:: snippets/InitialDirection.rst

.. include:: snippets/SetSeed.rst

ResiduFormula
  .. index:: single: ResiduFormula

  *Nom prédéfini*. Cette clé indique la formule de résidu qui doit être
  utilisée pour le test. Le choix par défaut est "Taylor", et les choix
  possibles sont "Taylor" (résidu du développement de Taylor normalisé de
  l'opérateur, qui doit décroître comme le carré de la perturbation),
  "TaylorOnNorm" (résidu du développement de Taylor rapporté à la perturbation
  de l'opérateur, qui doit rester constant) et "Norm" (résidu obtenu en prenant
  la norme du développement de Taylor à l'ordre 0, qui approxime le gradient,
  et qui doit rester constant).

  Exemple :
  ``{"ResiduFormula":"Taylor"}``

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *Liste de noms*. Cette liste indique les noms des variables supplémentaires
  qui peuvent être disponibles au cours du déroulement ou à la fin de
  l'algorithme, si elles sont initialement demandées par l'utilisateur. Cela
  implique potentiellement des calculs ou du stockage coûteux. La valeur par
  défaut est une liste vide, aucune de ces variables n'étant calculée et
  stockée par défaut sauf les variables inconditionnelles. Les noms possibles
  sont dans la liste suivante : [
  "CurrentState",
  "Residu",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Residu.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/Residu.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LinearityTest`
- :ref:`section_ref_algorithm_TangentTest`
- :ref:`section_ref_algorithm_AdjointTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`
