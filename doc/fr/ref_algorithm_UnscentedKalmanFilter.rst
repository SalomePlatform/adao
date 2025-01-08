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

.. index:: single: UnscentedKalmanFilter
.. _section_ref_algorithm_UnscentedKalmanFilter:

Algorithme de calcul "*UnscentedKalmanFilter*"
----------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme réalise une estimation de l'état d'un système dynamique par un
filtre de Kalman utilisant une transformation "unscented" et un échantillonnage
par points "sigma", permettant d'éviter de devoir calculer les opérateurs tangent
ou adjoint pour les opérateurs d'observation ou d'évolution, comme dans les
filtres de Kalman simple ou étendu.

Il s'applique aux cas d'opérateurs d'observation et d'évolution incrémentale
(processus) non-linéaires et présente d'excellentes qualités de robustesse et
de performances. Il peut être rapproché de
l':ref:`section_ref_algorithm_EnsembleKalmanFilter`, dont les qualités sont
similaires pour les systèmes non-linéaires.

On remarque qu'il n'y a pas d'analyse effectuée au pas de temps initial
(numéroté 0 dans l'indexage temporel) car il n'y a pas de prévision à cet
instant (l'ébauche est stockée comme pseudo-analyse au pas initial). Si les
observations sont fournies en série par l'utilisateur, la première n'est donc
pas utilisée. Pour une bonne compréhension de la gestion du temps, on se
reportera au :ref:`schema_d_AD_temporel` et aux explications décrites dans la
section pour :ref:`section_theory_dynamic`.

Dans le cas d'opérateurs linéaires ou "faiblement" non-linéaire, on peut
aisément utiliser l':ref:`section_ref_algorithm_ExtendedKalmanFilter` ou même
l':ref:`section_ref_algorithm_KalmanFilter`, qui sont souvent largement moins
coûteux en évaluation sur de petits systèmes. On peut vérifier la linéarité des
opérateurs à l'aide de l':ref:`section_ref_algorithm_LinearityTest`.

Il existe diverses variantes de cet algorithme. On propose ici les formulations
stables et robustes suivantes :

.. index::
    pair: Variant ; UKF
    pair: Variant ; S3F
    pair: Variant ; CUKF
    pair: Variant ; CS3F
    pair: Variant ; 2UKF

- "UKF" (Unscented Kalman Filter, voir [Julier95]_, [Julier00]_, [Wan00]_),
  algorithme canonique d'origine et de référence, très robuste et performant,
- "CUKF", aussi nommée "2UKF" (Constrained Unscented Kalman Filter, voir
  [Julier07]_), version avec contraintes d'inégalités ou de bornes de
  l'algorithme "UKF",
- "S3F" (Scaled Spherical Simplex Filter, voir [Papakonstantinou22]_),
  algorithme amélioré, réduisant le nombre de (sigma) points d'échantillonnage
  pour avoir la même qualité que la variante "UKF" canonique,
- "CS3F" (Constrained Scaled Spherical Simplex Filter), version avec
  contraintes d'inégalités ou de bornes de l'algorithme "S3F".

Voici quelques suggestions pratiques pour une utilisation efficace de ces
algorithmes :

- La variante recommandée de cet algorithme est le "S3F", même si l'algorithme
  canonique "UKF" reste par défaut le plus robuste.
- Lorsqu'il n'y a aucune borne de définie, les versions avec prise en compte
  des contraintes des algorithmes ("CUKF" et "CS3F") sont identiques aux
  versions sans contraintes ("UKF" et "S3F"). Ce n'est pas le cas s'il a des
  contraintes définies, mêmes si les bornes choisies sont très larges.
- Une différence essentielle entre les algorithmes est le nombre de "sigma"
  points d'échantillonnage utilisés en fonction de la dimension :math:`n` de
  l'espace des états. L'algorithme canonique "UKF" en utilise :math:`2n+1`,
  l'algorithme "S3F" en utilise :math:`n+2`. Cela signifie qu'il faut de
  l'ordre de deux fois plus d'évaluations de la fonction à simuler pour l'une
  que l'autre.
- Les évaluations de la fonction à simuler sont algorithmiquement indépendantes
  à chaque étape du filtrage (évolution ou observation) et peuvent donc être
  parallélisées ou distribuées dans le cas où la fonction à simuler le
  supporte.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropLocalOptimization.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. include:: snippets/FeaturePropParallelAlgorithm.rst

.. include:: snippets/FeaturePropConvergenceOnStatic.rst

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

.. include:: snippets/ConstrainedBy.rst

.. include:: snippets/EstimationOf_State.rst

.. include:: snippets/AlphaBeta.rst

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
  "APosterioriCorrelations",
  "APosterioriCovariance",
  "APosterioriStandardDeviations",
  "APosterioriVariances",
  "BMA",
  "CostFunctionJ",
  "CostFunctionJAtCurrentOptimum",
  "CostFunctionJb",
  "CostFunctionJbAtCurrentOptimum",
  "CostFunctionJo",
  "CostFunctionJoAtCurrentOptimum",
  "CurrentOptimum",
  "CurrentState",
  "ForecastCovariance",
  "ForecastState",
  "IndexOfOptimum",
  "InnovationAtCurrentAnalysis",
  "InnovationAtCurrentState",
  "SimulatedObservationAtCurrentAnalysis",
  "SimulatedObservationAtCurrentOptimum",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. include:: snippets/Variant_UKF.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/APosterioriCorrelations.rst

.. include:: snippets/APosterioriCovariance.rst

.. include:: snippets/APosterioriStandardDeviations.rst

.. include:: snippets/APosterioriVariances.rst

.. include:: snippets/BMA.rst

.. include:: snippets/CostFunctionJ.rst

.. include:: snippets/CostFunctionJAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

.. include:: snippets/CurrentOptimum.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/ForecastCovariance.rst

.. include:: snippets/ForecastState.rst

.. include:: snippets/IndexOfOptimum.rst

.. include:: snippets/InnovationAtCurrentAnalysis.rst

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentAnalysis.rst

.. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_UnscentedKalmanFilter_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_KalmanFilter`
- :ref:`section_ref_algorithm_ExtendedKalmanFilter`
- :ref:`section_ref_algorithm_EnsembleKalmanFilter`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Julier95]_
- [Julier00]_
- [Julier07]_
- [Papakonstantinou22]_
- [Wan00]_
- [WikipediaUKF]_
