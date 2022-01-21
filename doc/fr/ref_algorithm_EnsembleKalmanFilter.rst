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

.. index:: single: EnsembleKalmanFilter
.. _section_ref_algorithm_EnsembleKalmanFilter:

Algorithme de calcul "*EnsembleKalmanFilter*"
---------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme réalise une estimation de l'état d'un système dynamique par un
filtre de Kalman d'ensemble (EnKF), permettant d'éviter de devoir calculer les
opérateurs tangent ou adjoint pour les opérateurs d'observation ou d'évolution,
comme dans les filtres de Kalman simple ou étendu.

Il s'applique aux cas d'opérateurs d'observation et d'évolution incrémentale
(processus) non-linéaires et présente d'excellentes qualités de robustesse et
de performances. Il peut être rapproché de
l':ref:`section_ref_algorithm_UnscentedKalmanFilter` dont les qualités sont
similaires pour les systèmes non-linéaires.

On remarque qu'il n'y a pas d'analyse effectuée au pas de temps initial
(numéroté 0 dans l'indexage temporel) car il n'y a pas de prévision à cet
instant (l'ébauche est stockée comme pseudo-analyse au pas initial). Si les
observations sont fournies en série par l'utilisateur, la première n'est donc
pas utilisée.

Dans le cas d'opérateurs linéaires ou "faiblement" non-linéaire, on peut
aisément utiliser l':ref:`section_ref_algorithm_ExtendedKalmanFilter` ou même
l':ref:`section_ref_algorithm_KalmanFilter`, qui sont souvent largement moins
coûteux en évaluations sur de petits systèmes. On peut vérifier la linéarité
des opérateurs à l'aide de l':ref:`section_ref_algorithm_LinearityTest`.

Il existe de nombreuses variantes de cet algorithme. On propose ici des
formulations stables et robustes suivantes :

.. index::
    pair: Variant ; EnKF
    pair: Variant ; ETKF
    pair: Variant ; ETKF-N
    pair: Variant ; MLEF
    pair: Variant ; IEnKF

- "EnKF" (Ensemble Kalman Filter, voir [Evensen94]_), algorithme stochastique original, permettant de traiter de manière consistante un opérateur d'évolution non-linéaire,
- "ETKF" (Ensemble-Transform Kalman Filter), algorithme déterministe d'EnKF, permettant de traiter un opérateur d'évolution non-linéaire avec beaucoup moins de membres (on recommande d'utiliser un nombre de membres de l'ordre de 10 ou même parfois moins),
- "ETKF-N" (Ensemble-Transform Kalman Filter of finite size N), algorithme d'ETKF dit de "taille finie N", évitant de recourir à une inflation souvent nécessaire avec les autres algorithmes,
- "MLEF" (Maximum Likelihood Kalman Filter, voir [Zupanski05]_), algorithme déterministe d'EnKF, permettant en plus de traiter de manière consistante un opérateur d'observation non-linéaire),
- "IEnKF" (Iterative EnKF), algorithme déterministe d'EnKF, améliorant le traitement des non-linéarités des opérateurs,
- "EnKS" (Ensemble Kalman Smoother), algorithme de lissage avec un décalage fixe.

Sans pouvoir prétendre à l'universalité, on recommande d'utiliser l'"EnKF"
comme référence, et les autres algorithmes (dans l'ordre) comme des moyens pour
obtenir une assimilation de données plus économique et de qualité
éventuellement similaire.

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

.. include:: snippets/EstimationOf_State.rst

.. include:: snippets/InflationFactor.rst

.. include:: snippets/InflationType.rst

.. include:: snippets/NumberOfMembers.rst

.. include:: snippets/SetSeed.rst

.. include:: snippets/SmootherLagL.rst

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
  "CurrentIterationNumber",
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
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

.. include:: snippets/Variant_EnKF.rst

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

.. include:: snippets/CurrentIterationNumber.rst

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
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_KalmanFilter`
- :ref:`section_ref_algorithm_ExtendedKalmanFilter`
- :ref:`section_ref_algorithm_UnscentedKalmanFilter`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Evensen94]_
- [Burgers98]_
- [Bishop01]_
- [Evensen03]_
- [Zupanski05]_
- [WikipediaEnKF]_
