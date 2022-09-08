..
   Copyright (C) 2008-2022 EDF R&D

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

.. index:: single: AdjointTest
.. _section_ref_algorithm_AdjointTest:

Algorithme de vérification "*AdjointTest*"
------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de vérifier la qualité de l'adjoint d'un opérateur
:math:`F`, en calculant un résidu dont les propriétés théoriques sont connues.
Le test est applicable à un opérateur quelconque, d'évolution comme
d'observation.

Pour toutes les formules, avec :math:`\mathbf{x}` le point courant de
vérification, on prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha_0*\mathbf{dx}_0` avec :math:`\alpha_0` un paramètre
utilisateur de mise à l'échelle, par défaut à 1. :math:`F` est l'opérateur ou
le code de calcul (qui est ici acquis par la commande d'opérateur d'observation
"*ObservationOperator*").

On observe le résidu suivant, qui est la différence de deux produits scalaires :

.. math:: R(\alpha) = | < TangentF_x(\mathbf{dx}) , \mathbf{y} > - < \mathbf{dx} , AdjointF_x(\mathbf{y}) > |

dans lequel la quantité optionnelle :math:`\mathbf{y}` doit être dans l'image
de :math:`F`. Si elle n'est pas donnée, on prend son évaluation par défaut
:math:`\mathbf{y} = F(\mathbf{x})`.

Ce résidu doit rester constamment égal à zéro à la précision du calcul.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/AmplitudeOfInitialDirection.rst

.. include:: snippets/EpsilonMinimumExponent.rst

.. include:: snippets/InitialDirection.rst

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
- :ref:`section_ref_algorithm_GradientTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`
