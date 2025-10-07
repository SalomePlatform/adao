..
   Copyright (C) 2008-2025 EDF R&D

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

.. index:: single: SimulatedAnnealing
.. _section_ref_algorithm_SimulatedAnnealing:

Algorithme de calcul "*SimulatedAnnealing*"
-------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme réalise une estimation de l'état d'un système par minimisation
sans gradient d'une fonctionnelle d'écart :math:`J`, en utilisant la
méta-heuristique de recherche de recuit simulé. Elle est basée sur une
réduction de l'erreur :math:`J` tant que c'est possible, en autorisant une
remontée temporaire de cette erreur pour éviter de rester bloqué dans un
minimum local. La remontée de l'erreur est pilotée par une loi statistique de
température, d'où l'analogie avec le recuit des métaux qui donne son nom à la
méthode. La méthode ne requiert pas d'information particulière sur la
fonctionnelle et ne nécessite pas les dérivées (sauf dans sa version hybride de
type "DualAnnealing").

Elle entre dans la même catégorie que les
:ref:`section_ref_algorithm_DerivativeFreeOptimization`,
:ref:`section_ref_algorithm_DifferentialEvolution`,
:ref:`section_ref_algorithm_ParticleSwarmOptimization`,
:ref:`section_ref_algorithm_TabuSearch`.

C'est une méthode d'optimisation mono-objectif, permettant la recherche du
minimum global d'une fonctionnelle d'erreur :math:`J` quelconque de type
:math:`L^1`, :math:`L^2` ou :math:`L^{\infty}`, avec ou sans pondérations,
comme décrit dans la section pour :ref:`section_theory_optimization`. Comme
c'est une méta-heuristique, hormis dans des cas particuliers, l'atteinte d'un
résultat optimal global ou local n'est pas garantie (sauf dans sa version
hybride de type "DualAnnealing"). La fonctionnelle d'erreur par défaut est
celle de moindres carrés pondérés augmentés, classiquement utilisée en
assimilation de données.

Il existe diverses variantes de cet algorithme. On propose ici les formulations
stables et robustes suivantes :

.. index::
    pair: Variant ; GeneralizedSimulatedAnnealing
    pair: Variant ; DualAnnealing

- "GeneralizedSimulatedAnnealing" (Generalized Simulated Annealing ou GSA, voir
  [Tsallis96]_), algorithme classique combinant les approches classiques et
  rapides de recuit simulé. Il est performant, robuste et définit une référence
  pour les méthodes de recuit simulé.
- "DualAnnealing" (Dual Annealing, voir [Xiang97]_), algorithme combinant le
  GSA précédent à une stratégie de recherche locale, appliquée aux états
  acceptables du point de vue du recuit simulé, ce qui améliore la rapidité et
  la précision du GSA. Cette amélioration nécessite les opérateurs tangent et
  adjoint.

Voici quelques suggestions pratiques pour une utilisation efficace de ces
algorithmes :

- La variante recommandée de cet algorithme est le "DualAnnealing" car il est à
  la fois robuste et sa convergence est très performante, surtout en grande
  dimension pour un tel algorithme. Néanmoins, comme elle nécessite les
  opérateurs tangent et adjoint, il n'est pas toujours judicieux d'utiliser
  cette caractéristique d'accélération.
- Dans le cas où la fonction d'écart ou l'opérateur d'observation ne sont pas
  dérivables, l'algorithme "GeneralizedSimulatedAnnealing" convient et réalise
  la même optimisation de recuit simulé que la variante accélérée.
- Le contrôle de la convergence le plus aisé se fait en laissant les paramètres
  par défaut, en laissant le recuit simulé se stabiliser. Néanmoins, comme la
  convergence stochastique peut être longue, on peut aussi restreindre les
  calculs par la limitation du nombre d'évaluations de la fonction de
  simulation. Cela ne limite la convergence théorique, mais permet néanmoins de
  restreindre notablement le nombre de calculs.

Ces conseils sont à utiliser comme des indications expérimentales, et non comme
des prescriptions, car ils sont à apprécier ou à adapter selon la physique de
chaque problème que l'on traite.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropGlobalOptimization.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. include:: snippets/FeaturePropParallelFree.rst

.. include:: snippets/FeaturePropConvergenceOnBoth.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/EvolutionError.rst

.. include:: snippets/EvolutionModel.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. include:: snippets/BoundsWithNone.rst

.. include:: snippets/EstimationOf_Parameters.rst

.. include:: snippets/MaximumNumberOfIterations.rst

.. include:: snippets/MaximumNumberOfFunctionEvaluations.rst

.. include:: snippets/Minimizer_xDVAR.rst

.. include:: snippets/QualityCriterion.rst

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
  "Analysis",
  "BMA",
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CostFunctionJAtCurrentOptimum",
  "CostFunctionJbAtCurrentOptimum",
  "CostFunctionJoAtCurrentOptimum",
  "CurrentIterationNumber",
  "CurrentOptimum",
  "CurrentState",
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  "IndexOfOptimum",
  "Innovation",
  "InnovationAtCurrentState",
  "OMA",
  "OMB",
  "SimulatedObservationAtBackground",
  "SimulatedObservationAtCurrentOptimum",
  "SimulatedObservationAtCurrentState",
  "SimulatedObservationAtOptimum",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. include:: snippets/Variant_SA.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/BMA.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CostFunctionJAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

.. include:: snippets/CurrentIterationNumber.rst

.. include:: snippets/CurrentOptimum.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. include:: snippets/IndexOfOptimum.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/OMA.rst

.. include:: snippets/OMB.rst

.. include:: snippets/SimulatedObservationAtBackground.rst

.. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtOptimum.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_SimulatedAnnealing_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_DerivativeFreeOptimization`
- :ref:`section_ref_algorithm_DifferentialEvolution`
- :ref:`section_ref_algorithm_ParticleSwarmOptimization`
- :ref:`section_ref_algorithm_TabuSearch`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Kirkpatrick83]_
- [Tsallis96]_
- [WikipediaSA]_
- [Xiang97]_
