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

.. index:: single: TabuSearch
.. _section_ref_algorithm_TabuSearch:

Algorithme de calcul "*TabuSearch*"
-----------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme réalise une estimation de l'état d'un système par minimisation
sans gradient d'une fonctionnelle d'écart :math:`J`, en utilisant une méthode
de recherche avec liste Tabou. C'est une méthode qui n'utilise pas les dérivées
de la fonctionnelle d'écart. Elle entre, par exemple, dans la même catégorie
que
l':ref:`section_ref_algorithm_DerivativeFreeOptimization`,
l':ref:`section_ref_algorithm_ParticleSwarmOptimization` ou
l':ref:`section_ref_algorithm_DifferentialEvolution`.

C'est une méthode d'optimisation mono-objectif permettant la recherche du
minimum global d'une fonctionnelle d'erreur :math:`J` quelconque de type
:math:`L^1`, :math:`L^2` ou :math:`L^{\infty}`, avec ou sans pondérations. La
fonctionnelle d'erreur par défaut est celle de moindres carrés pondérés
augmentés, classiquement utilisée en assimilation de données.

Elle fonctionne par exploration aléatoire itérative du voisinage du point
courant, pour en choisir l'état qui minimise la fonctionnelle d'écart. Pour
éviter de revenir dans un point déjà exploré, le mécanisme de mémoire de
l'algorithme permet d'interdire (d'où le nom de *tabou*) le retour dans les
derniers états explorés. Les positions déjà explorées sont conservées dans une
liste de longueur finie.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropNonLocalOptimization.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. include:: snippets/FeaturePropConvergenceOnNumbers.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. include:: snippets/BoundsWithNone.rst

.. include:: snippets/LengthOfTabuList.rst

.. include:: snippets/MaximumNumberOfIterations_50.rst

.. include:: snippets/NoiseAddingProbability.rst

.. include:: snippets/NoiseDistribution.rst

.. include:: snippets/NoiseHalfRange.rst

.. include:: snippets/NumberOfElementaryPerturbations.rst

.. include:: snippets/QualityCriterion.rst

.. include:: snippets/SetSeed.rst

.. include:: snippets/StandardDeviation.rst

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
  "CurrentIterationNumber",
  "CurrentState",
  "Innovation",
  "OMA",
  "OMB",
  "SimulatedObservationAtBackground",
  "SimulatedObservationAtCurrentState",
  "SimulatedObservationAtOptimum",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

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

.. include:: snippets/CurrentIterationNumber.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/OMA.rst

.. include:: snippets/OMB.rst

.. include:: snippets/SimulatedObservationAtBackground.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtOptimum.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_TabuSearch_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_DerivativeFreeOptimization`
- :ref:`section_ref_algorithm_DifferentialEvolution`
- :ref:`section_ref_algorithm_ParticleSwarmOptimization`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Glover89]_
- [Glover90]_
- [WikipediaTS]_
