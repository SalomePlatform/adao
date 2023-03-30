..
   Copyright (C) 2008-2023 EDF R&D

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

.. index:: single: ObservationSimulationComparisonTest
.. _section_ref_algorithm_ObservationSimulationComparisonTest:

Algorithme de vérification "*ObservationSimulationComparisonTest*"
------------------------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme de vérification permet d'analyser de manière simple la stabilité
de l'écart entre des mesures et le calcul d'un opérateur :math:`F`, lors de son
exécution. L'opérateur est quelconque, et il peut donc être celui d'observation
:math:`\mathcal{H}` comme celui d'évolution :math:`\mathcal{D}`, pourvu qu'il
soit fourni dans chaque cas selon les :ref:`section_ref_operator_requirements`.
L'opérateur :math:`F` est considéré comme dépendant d'une variable vectorielle
:math:`\mathbf{x}` et restituant une autre variable vectorielle
:math:`\mathbf{y}`.

L'algorithme vérifie que l'écart est stable, que l'opérateur fonctionne
correctement et que son appel se déroule de manière compatible avec son usage
dans les algorithmes d'ADAO. De manière pratique, il permet d'appeler une ou
plusieurs fois l'opérateur, en activant ou non le mode "debug" lors de
l'exécution. Il est très similaire dans son fonctionnement courant à un
:ref:`section_ref_algorithm_FunctionTest` mais il teste la stabilité de l'écart
mesures-calculs.

Une statistique sur les vecteurs :math:`\mathbf{x}` en entrée et
:math:`\mathbf{y}` en sortie, et potentiellement sur la fonctionnelle d'erreur
standard d'assimilation de données :math:`J`, est indiquée lors de chaque
exécution de l'opérateur, et une autre statistique globale est fournie de
manière récapitulative à la fin. La précision d'affichage est contrôlable pour
permettre l'automatisation des tests d'opérateur. Il peut être aussi utile de
vérifier préalablement les entrées elles-mêmes avec le test prévu
:ref:`section_ref_algorithm_InputValuesTest`.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/NumberOfRepetition.rst

.. include:: snippets/SetDebug.rst

.. include:: snippets/ShowElementarySummary.rst

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
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CurrentState",
  "Innovation",
  "InnovationAtCurrentState",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/NoUnconditionalOutput.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_ObservationSimulationComparisonTest_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
