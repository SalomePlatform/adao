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

.. index:: single: EnsembleOfSimulationGenerationTask
.. index:: single: Génération d'ensemble de simulations
.. index:: single: Ensemble de simulations
.. index:: single: Ensemble de snapshots
.. index:: single: Simulations (Ensemble)
.. index:: single: Snapshots (Ensemble)
.. _section_ref_algorithm_EnsembleOfSimulationGenerationTask:

Algorithme de tâche "*EnsembleOfSimulationGenerationTask*"
----------------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. warning::

  Cet algorithme n'est utilisable qu'en interface textuelle (TUI) et pas en
  interface graphique (GUI).

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de générer un ensemble de résultats physiques, de type
simulation ou observation, à l'aide de l'opérateur :math:`H` pour un plan
d'expérience de l'espace des états :math:`\mathbf{x}` paramétriques. Le
résultat de cet algorithme est une collection homogène de vecteurs simulés
:math:`\mathbf{y}` (disponible à l'aide de la variable stockable
"*EnsembleOfSimulations*") correspondants directement à la collection homogène
choisie de vecteurs d'états :math:`\mathbf{x}` (disponible à l'aide de la
variable stockable "*EnsembleOfStates*").

L'échantillonnage des états :math:`\mathbf{x}` peut être fourni explicitement
ou sous la forme d'hyper-cubes, explicites ou échantillonnés selon des
distributions courantes. Les calculs sont optimisés selon les ressources
informatiques disponibles et les options demandées par l'utilisateur. Attention
à la taille de l'hyper-cube (et donc au nombre de calculs) qu'il est possible
d'atteindre, elle peut rapidement devenir importante.

Pour apparaître pour l'utilisateur tout en réduisant les difficultés de
stockage, les résultats de l'échantillonnage ou des simulations doivent être
demandés **explicitement** à l'aide de la variable requise.

Les résultats obtenus avec cet algorithme peuvent être utilisés pour alimenter
un :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`. De manière
complémentaire, et si le but est d'évaluer l'erreur calcul-mesure, un
:ref:`section_ref_algorithm_SamplingTest` utilise les mêmes commandes
d'échantillonnage pour établir un ensemble de valeurs de fonctionnelle d'erreur
:math:`J` à partir d'observations :math:`\mathbf{y}^o`.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Task.rst

.. include:: snippets/SampleAsExplicitHyperCube.rst

.. include:: snippets/SampleAsIndependantRandomVariables.rst

.. include:: snippets/SampleAsMinMaxStepHyperCube.rst

.. include:: snippets/SampleAsnUplet.rst

.. include:: snippets/SetDebug.rst

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
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_EnsembleOfSimulationGenerationTask_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_ParallelFunctionTest`
- :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`

