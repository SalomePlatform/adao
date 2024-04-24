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

.. index:: single: Blue
.. _section_ref_algorithm_Blue:

Algorithme de calcul "*Blue*"
-----------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme réalise une estimation de type BLUE (Best Linear Unbiased
Estimator) de l'état d'un système. C'est une estimation linéaire, sans biais et
optimale. De manière technique, c'est ici un estimateur d'Aitken. Il réalise la
meilleure estimation linéaire de l'état à l'aide de l'état d'ébauche initial et
des observations. Il est théoriquement réservé aux cas d'opérateurs
d'observation linéaires, même s'il fonctionne parfois dans les cas "faiblement"
non-linéaires. On peut vérifier la linéarité de l'opérateur d'observation à
l'aide d'un :ref:`section_ref_algorithm_LinearityTest`. Cet algorithme est
toujours le plus rapide de l'ensemble des algorithmes d'assimilation d'ADAO.

Cet algorithme d'optimisation mono-objectif est naturellement écrit pour une
estimation unique, sans notion dynamique ou itérative (il n'y a donc pas besoin
dans ce cas d'opérateur d'évolution incrémentale, ni de covariance d'erreurs
d'évolution). Dans ADAO, il peut aussi être utilisé sur une succession
d'observations, plaçant alors l'estimation dans un cadre récursif en partie
similaire à un :ref:`section_ref_algorithm_KalmanFilter`. Une estimation
standard est effectuée à chaque pas d'observation sur l'état prévu par le
modèle d'évolution incrémentale, sachant que la covariance d'erreur d'état
reste la covariance d'ébauche initialement fournie par l'utilisateur. Pour être
explicite, contrairement aux filtres de type Kalman, la covariance d'erreurs
sur les états n'est pas remise à jour.

En cas de non-linéarité, même peu marquée, on lui préférera aisément un
:ref:`section_ref_algorithm_ExtendedBlue` ou un
:ref:`section_ref_algorithm_3DVAR`.

.. index:: single: Optimal Interpolation
.. index:: single: OI

Remarque complémentaire : une simplification algébrique du BLUE conduit à la
méthode d'interpolation dite optimale nommée "*Optimal Interpolation*" ou
"*OI*". C'est une méthode très simple et peu coûteuse, spécialement adaptée aux
problèmes de très (très) grande taille, mais dont l'inconvénient est de fournir
un résultat d'analyse globalement sous-optimal et bruité, voire incohérent. Le
moyen d'éviter ces désavantages est d'adapter très précisément les éléments de
la méthode à chaque modèle physique, la rendant non robuste. Pour ces raisons,
cette méthode n'est donc pas proposée.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropLocalOptimization.rst

.. include:: snippets/FeaturePropDerivativeNeeded.rst

.. include:: snippets/FeaturePropParallelDerivativesOnly.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Background.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03AdOp.rst

.. include:: snippets/EstimationOf_Parameters.rst

.. include:: snippets/NumberOfSamplesForQuantiles.rst

.. include:: snippets/Quantiles.rst

.. include:: snippets/SetSeed.rst

.. include:: snippets/SimulationForQuantiles.rst

.. include:: snippets/StateBoundsForQuantilesWithNone.rst

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
  "CurrentStepNumber",
  "ForecastState",
  "Innovation",
  "InnovationAtCurrentAnalysis",
  "MahalanobisConsistency",
  "OMA",
  "OMB",
  "SampledStateForQuantiles",
  "SigmaBck2",
  "SigmaObs2",
  "SimulatedObservationAtBackground",
  "SimulatedObservationAtCurrentOptimum",
  "SimulatedObservationAtCurrentState",
  "SimulatedObservationAtOptimum",
  "SimulationQuantiles",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

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

.. include:: snippets/CurrentStepNumber.rst

.. include:: snippets/ForecastState.rst

.. include:: snippets/Innovation.rst

.. include:: snippets/InnovationAtCurrentAnalysis.rst

.. include:: snippets/MahalanobisConsistency.rst

.. include:: snippets/OMA.rst

.. include:: snippets/OMB.rst

.. include:: snippets/SampledStateForQuantiles.rst

.. include:: snippets/SigmaBck2.rst

.. include:: snippets/SigmaObs2.rst

.. include:: snippets/SimulatedObservationAtBackground.rst

.. include:: snippets/SimulatedObservationAtCurrentOptimum.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtOptimum.rst

.. include:: snippets/SimulationQuantiles.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_Blue_examples:

.. include:: snippets/Header2Algo09.rst

.. include:: scripts/simple_Blue.rst

.. literalinclude:: scripts/simple_Blue.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_Blue.res
    :language: none

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_ExtendedBlue`
- :ref:`section_ref_algorithm_3DVAR`
- :ref:`section_ref_algorithm_LinearityTest`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Bouttier99]_
