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

.. index:: single: 4DVAR
.. _section_ref_algorithm_4DVAR:

Algorithme de calcul "*4DVAR*"
------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme réalise une estimation de l'état d'un système dynamique, par une
méthode de minimisation variationnelle de la fonctionnelle :math:`J` d'écart
classique en assimilation de données :

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\sum_{t\in T}(\mathbf{y^o}(t)-H(\mathbf{x},t))^T.\mathbf{R}^{-1}.(\mathbf{y^o}(t)-H(\mathbf{x},t))

qui est usuellement désignée comme la fonctionnelle "*4D-VAR*" (voir par exemple
[Talagrand97]_). Il est bien adapté aux cas d'opérateurs d'observation et
d'évolution non-linéaires, son domaine d'application est comparable aux
algorithmes de filtrage de Kalman et en particulier
l':ref:`section_ref_algorithm_ExtendedKalmanFilter` ou
l':ref:`section_ref_algorithm_UnscentedKalmanFilter`.

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

.. include:: snippets/CostDecrementTolerance.rst

.. include:: snippets/EstimationOf.rst

.. include:: snippets/GradientNormTolerance.rst

.. include:: snippets/MaximumNumberOfSteps.rst

.. include:: snippets/Minimizer_xDVAR.rst

.. include:: snippets/ProjectedGradientTolerance.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *Liste de noms*. Cette liste indique les noms des variables supplémentaires
  qui peuvent être disponibles au cours du déroulement ou à la fin de
  l'algorithme, si elles sont initialement demandées par l'utilisateur. Cela
  implique potentiellement des calculs ou du stockage coûteux. La valeur par
  défaut est une liste vide, aucune de ces variables n'étant calculée et
  stockée par défaut sauf les variables inconditionnelles. Les noms possibles
  sont dans la liste suivante : [
  "Analysis",
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
  "IndexOfOptimum",
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

.. include:: snippets/CostFunctionJAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJb.rst

.. include:: snippets/CostFunctionJbAtCurrentOptimum.rst

.. include:: snippets/CostFunctionJo.rst

.. include:: snippets/CostFunctionJoAtCurrentOptimum.rst

.. include:: snippets/CurrentIterationNumber.rst

.. include:: snippets/CurrentOptimum.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/IndexOfOptimum.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_3DVAR`
- :ref:`section_ref_algorithm_KalmanFilter`
- :ref:`section_ref_algorithm_ExtendedKalmanFilter`
- :ref:`section_ref_algorithm_EnsembleKalmanFilter`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Byrd95]_
- [Morales11]_
- [Talagrand97]_
- [Zhu97]_
