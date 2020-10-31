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

.. index:: single: ParticleSwarmOptimization
.. _section_ref_algorithm_ParticleSwarmOptimization:

Algorithme de calcul "*ParticleSwarmOptimization*"
--------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme réalise une estimation de l'état d'un système par minimisation
d'une fonctionnelle d'écart :math:`J` en utilisant une méthode évolutionnaire
d'essaim particulaire. C'est une méthode qui n'utilise pas les dérivées de la
fonctionnelle d'écart. Elle entre dans la même catégorie que
l':ref:`section_ref_algorithm_DerivativeFreeOptimization`,
l':ref:`section_ref_algorithm_DifferentialEvolution` ou
l':ref:`section_ref_algorithm_TabuSearch`.

C'est une méthode d'optimisation permettant la recherche du minimum global d'une
fonctionnelle d'erreur :math:`J` quelconque de type :math:`L^1`, :math:`L^2` ou
:math:`L^{\infty}`, avec ou sans pondérations. La fonctionnelle d'erreur par
défaut est celle de moindres carrés pondérés augmentés, classiquement utilisée
en assimilation de données.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. index:: single: NumberOfInsects
.. index:: single: SwarmVelocity
.. index:: single: GroupRecallRate
.. index:: single: QualityCriterion
.. index:: single: BoxBounds

.. include:: snippets/MaximumNumberOfSteps_50.rst

.. include:: snippets/MaximumNumberOfFunctionEvaluations.rst

.. include:: snippets/QualityCriterion.rst

NumberOfInsects
  Cette clé indique le nombre d'insectes ou de particules dans l'essaim. La
  valeur par défaut est 100, qui est une valeur par défaut usuelle pour cet
  algorithme.

  Exemple :
  ``{"NumberOfInsects":100}``

SwarmVelocity
  Cette clé indique la part de la vitesse d'insecte qui est imposée par
  l'essaim. C'est une valeur réelle positive. Le défaut est de 1.

  Exemple :
  ``{"SwarmVelocity":1.}``

GroupRecallRate
  Cette clé indique le taux de rappel vers le meilleur insecte de l'essaim.
  C'est une valeur réelle comprise entre 0 et 1. Le défaut est de 0.5.

  Exemple :
  ``{"GroupRecallRate":0.5}``

BoxBounds
  Cette clé permet de définir des bornes supérieure et inférieure pour chaque
  incrément de  variable d'état optimisée (et non pas chaque variable d'état
  elle-même). Les bornes doivent être données par une liste de liste de paires
  de bornes inférieure/supérieure pour chaque incrément de variable, avec une
  valeur extrême chaque fois qu'il n'y a pas de borne (``None`` n'est pas une
  valeur autorisée lorsqu'il n'y a pas de borne). Cette clé est requise et il
  n'y a pas de valeurs par défaut.

  Exemple :
  ``{"BoxBounds":[[-0.5,0.5], [0.01,2.], [0.,1.e99], [-1.e99,1.e99]]}``

.. include:: snippets/SetSeed.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  Cette liste indique les noms des variables supplémentaires qui peuvent être
  disponibles à la fin de l'algorithme, si elles sont initialement demandées par
  l'utilisateur. Cela implique potentiellement des calculs ou du stockage
  coûteux. La valeur par défaut est une liste vide, aucune de ces variables
  n'étant calculée et stockée par défaut sauf les variables inconditionnelles.
  Les noms possibles sont dans la liste suivante : [
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
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

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
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_DerivativeFreeOptimization`
- :ref:`section_ref_algorithm_DifferentialEvolution`
- :ref:`section_ref_algorithm_TabuSearch`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [WikipediaPSO]_
