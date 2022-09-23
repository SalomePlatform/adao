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

.. index:: single: ExtendedKalmanFilter
.. _section_ref_algorithm_ExtendedKalmanFilter:

Algorithme de calcul "*ExtendedKalmanFilter*"
---------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme réalise une estimation de l'état d'un système dynamique par un
filtre de Kalman étendu, utilisant un calcul non linéaire de l'observation
d'état et de l'évolution incrémentale (processus). Techniquement, l'estimation
de l'état est réalisée par les équations classiques du filtre de Kalman, en
utilisant à chaque pas la jacobienne obtenue par linéarisation de l'observation
et de l'évolution pour évaluer la covariance d'erreur d'état. Cet algorithme
est donc plus coûteux que le Filtre de Kalman linéaire, mais il est par nature
mieux adapté dès que les opérateurs sont non linéaires, étant par principe
universellement recommandé dans ce cas.

Conceptuellement, on peut représenter le schéma temporel d'action des
opérateurs d'évolution et d'observation dans cet algorithme de la manière
suivante, avec **x** l'état, **P** la covariance d'erreur d'état, *t* le temps
itératif discret :

  .. _schema_temporel_KF:
  .. image:: images/schema_temporel_KF.png
    :align: center
    :width: 100%
  .. centered::
    **Schéma temporel des étapes en assimilation de données par filtre de Kalman étendu**

Dans ce schéma, l'analyse **(x,P)** est obtenue à travers la "*correction*" par
l'observation de la "*prévision*" de l'état précédent. On remarque qu'il n'y a
pas d'analyse effectuée au pas de temps initial (numéroté 0 dans l'indexage
temporel) car il n'y a pas de prévision à cet instant (l'ébauche est stockée
comme pseudo-analyse au pas initial). Si les observations sont fournies en
série par l'utilisateur, la première n'est donc pas utilisée.

Ce filtre peut aussi être utilisé pour estimer (conjointement ou uniquement)
des paramètres et non pas l'état, auquel cas ni le temps ni l'évolution n'ont
plus de signification. Les pas d'itération sont alors liés à l'insertion d'une
nouvelle observation dans l'estimation récursive. On consultera la section
:ref:`section_theory_dynamique` pour les concepts de mise en oeuvre.

Dans le cas d'opérateurs plus fortement non-linéaires, on peut utiliser un
:ref:`section_ref_algorithm_EnsembleKalmanFilter` ou un
:ref:`section_ref_algorithm_UnscentedKalmanFilter`, qui sont largement plus
adaptés aux comportements non-linéaires même si parfois plus coûteux. On peut
vérifier la linéarité des opérateurs à l'aide d'un
:ref:`section_ref_algorithm_LinearityTest`.

.. index::
    pair: Variant ; EKF
    pair: Variant ; CEKF

Le filtre de Kalman étendu peut tenir compte de bornes sur les états (la
variante est nommée "CEKF", elle est recommandée et elle est utilisée par
défaut), ou être conduit sans aucune contrainte (cette variante est nommée
"EKF", et elle n'est pas recommandée).

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

.. include:: snippets/Variant_EKF.rst

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
.. _section_ref_algorithm_ExtendedKalmanFilter_examples:
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_KalmanFilter`
- :ref:`section_ref_algorithm_EnsembleKalmanFilter`
- :ref:`section_ref_algorithm_UnscentedKalmanFilter`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [WikipediaEKF]_
