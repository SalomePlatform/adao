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

.. index:: single: SamplingTest
.. _section_ref_algorithm_SamplingTest:

Algorithme de vérification "*SamplingTest*"
-------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet d'établir la collection des valeurs d'une fonctionnelle
d'erreur :math:`J` quelconque de type :math:`L^1`, :math:`L^2` ou
:math:`L^{\infty}`, avec ou sans pondérations, comme décrit dans la section
pour :ref:`section_theory_optimization`. Chaque calcul de :math:`J` est conduit
à l'aide de l'opérateur d'observation :math:`\mathcal{H}` et des observations
:math:`\mathbf{y}^o` pour un état :math:`\mathbf{x}`. Les états
:math:`\mathbf{x}` proviennent d'un échantillon d'états défini *a priori*. La
fonctionnelle d'erreur par défaut est celle de moindres carrés pondérés
augmentés, classiquement utilisée en assimilation de données.

Ce test est utile pour analyser explicitement la sensibilité de la
fonctionnelle :math:`J` aux variations de l'état :math:`\mathbf{x}`.

L'échantillonnage des états :math:`\mathbf{x}` peut être fourni explicitement
ou sous la forme d'hypercubes, explicites ou échantillonnés selon des
distributions courantes, ou à l'aide d'un échantillonnage par hypercube latin
(LHS) ou par séquence de Sobol. Les calculs sont optimisés selon les ressources
informatiques disponibles et les options demandées par l'utilisateur. On pourra
se reporter aux :ref:`section_ref_sampling_requirements` pour une illustration
de l'échantillonnage. Attention à la taille de l'hypercube (et donc au nombre
de calculs) qu'il est possible d'atteindre, elle peut rapidement devenir
importante. Lorsqu'un état n'est pas observable, une valeur "*NaN*" est
retournée.

Il est aussi possible de fournir un ensemble de simulations :math:`\mathbf{y}`
déjà établies par ailleurs (donc sans besoin explicite d'un opérateur
:math:`\mathcal{H}`), qui sont implicitement associées à un ensemble
d'échantillons d'états :math:`\mathbf{x}`. Dans ce cas où l'ensemble de
simulations est fourni, il est impératif de fournir aussi l'ensemble des états
:math:`\mathbf{x}` par un échantillonnage explicite, dont l'ordre des états
correspond à l'ordre des simulations :math:`\mathbf{y}`.

Pour accéder aux informations calculées, les résultats de l'échantillonnage ou
des simulations doivent être demandés **explicitement** pour éviter les
difficultés de stockage (en l'absence de résultats demandés, rien n'est
disponible). On utilise pour cela, sur la variable désirée, la sauvegarde
finale à l'aide du mot-clé "*UserPostAnalysis*" ou le traitement en cours de
calcul à l'aide des "*observer*" adaptés.

Remarque : dans les cas où l'échantillonnage est généré, il peut être utile
d'obtenir explicitement la collection des états :math:`\mathbf{x}` selon la
définition *a priori* sans nécessairement effectuer de long calculs pour la
fonctionnelle :math:`J`. Pour cela, il suffit d'utiliser cet algorithme avec
des calculs simplifiés. Par exemple, on peut définir un opérateur d'observation
matriciel égal à l'identité (matrice carrée de la taille d'un état), une
ébauche et une observation égales, valant 1 (vecteurs de la taille de l'état).
Ensuite, on établit le cas ADAO avec cet algorithme pour récupérer l'ensemble
des états échantillonnés à l'aide de la variable habituelle de
"*CurrentState*".

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. include:: snippets/FeaturePropParallelAlgorithm.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/EnsembleOfSnapshots.rst

.. include:: snippets/QualityCriterion.rst

.. include:: snippets/SampleAsExplicitHyperCube.rst

.. include:: snippets/SampleAsIndependantRandomVariables.rst

.. include:: snippets/SampleAsMinMaxLatinHyperCube.rst

.. include:: snippets/SampleAsMinMaxSobolSequence.rst

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
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CurrentState",
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  "Innovation",
  "InnovationAtCurrentState",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_SamplingTest_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo08.rst

- OPENTURNS, voir le *Guide utilisateur du module OPENTURNS* dans le menu principal *Aide* de l'environnement SALOME
