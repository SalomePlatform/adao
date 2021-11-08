..
   Copyright (C) 2008-2021 EDF R&D

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

Cet algorithme permet d'établir les valeurs, liées à un état :math:`\mathbf{x}`,
d'une fonctionnelle d'erreur :math:`J` quelconque de type :math:`L^1`,
:math:`L^2` ou :math:`L^{\infty}`, avec ou sans pondérations, et de l'opérateur
d'observation, pour un échantillon d'états donné a priori. La fonctionnelle
d'erreur par défaut est celle de moindres carrés pondérés augmentés,
classiquement utilisée en assimilation de données.

Il est utile pour tester la sensibilité, de la fonctionnelle :math:`J`, en
particulier, aux variations de l'état :math:`\mathbf{x}`. Lorsque un état n'est
pas observable, une valeur *"NaN"* est retournée.

L'échantillon des états :math:`\mathbf{x}` peut être fourni explicitement ou
sous la forme d'hyper-cubes, explicites ou échantillonnés selon des lois
courantes. Attention à la taille de l'hyper-cube (et donc au nombre de calculs)
qu'il est possible d'atteindre, elle peut rapidement devenir importante.

Pour apparaître pour l'utilisateur, les résultats de l'échantillonnage doivent
être demandés explicitement. On utilise pour cela, sur la variable désirée, la
sauvegarde finale à l'aide du mot-clé "*UserPostAnalysis*" ou le traitement en
cours de calcul à l'aide des "*observer*" adaptés.

Pour effectuer un échantillonnage distribué ou plus complexe, voir le module
OPENTURNS disponible dans SALOME.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/BackgroundError.rst

.. include:: snippets/Observation.rst

.. include:: snippets/ObservationError.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/QualityCriterion.rst

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
  "CostFunctionJ",
  "CostFunctionJb",
  "CostFunctionJo",
  "CurrentState",
  "InnovationAtCurrentState",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

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

.. include:: snippets/InnovationAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo08.rst

- OPENTURNS, voir le *Guide utilisateur du module OPENTURNS* dans le menu principal *Aide* de l'environnement SALOME
