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

.. index:: single: LinearityTest
.. _section_ref_algorithm_LinearityTest:

Algorithme de vérification "*LinearityTest*"
--------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

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

Si le résidu décroît et que la décroissance se fait en :math:`\alpha^2` selon
:math:`\alpha`, cela signifie que le gradient est bien calculé jusqu'au niveau
d'arrêt de la décroissance quadratique.

Résidu "Taylor"
***************

On observe le résidu issu du développement de Taylor de la fonction :math:`F`,
normalisée par la valeur au point nominal :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) - \alpha * \nabla_xF(\mathbf{dx}) ||}{|| F(\mathbf{x}) ||}

S'il reste constamment très faible par rapport à 1, l'hypothèse de linéarité
de :math:`F` est vérifiée.

Si le résidu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
faible qu'à partir d'un certain ordre d'incrément, l'hypothèse de linéarité
de :math:`F` n'est pas vérifiée.

Si le résidu décroît et que la décroissance se fait en :math:`\alpha^2` selon
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

  Exemple :
  ``{"ResiduFormula":"CenteredDL"}``

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  Cette liste indique les noms des variables supplémentaires qui peuvent être
  disponibles à la fin de l'algorithme, si elles sont initialement demandées par
  l'utilisateur. Cela implique potentiellement des calculs ou du stockage
  coûteux. La valeur par défaut est une liste vide, aucune de ces variables
  n'étant calculée et stockée par défaut sauf les variables inconditionnelles.
  Les noms possibles sont dans la liste suivante : [
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
