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

.. index:: single: InterpolationByReducedModelTask
.. index:: single: Interpolation de mesures
.. index:: single: Reconstruction de champ
.. index:: single: Snapshots (Ensemble)
.. index:: single: Reduced Order Model
.. index:: single: ROM
.. _section_ref_algorithm_InterpolationByReducedModelTask:

Algorithme de tâche "*InterpolationByReducedModelTask*"
-------------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo99.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de réaliser une interpolation très efficace de mesures
physiques à l'aide d'une représentation réduite du modèle pour cette physique.
On obtient en sortie, pour chaque jeu de mesures fournies aux positions
requises, un champ complet :math:`\mathbf{y}` par interpolation. Dit autrement,
c'est une reconstruction de champ physique à l'aide de mesures et d'un modèle
numérique réduit.

Pour interpoler ces mesures, on utilise une méthode de type Empirical
Interpolation Method (EIM [Barrault04]_), qui utilise un modèle réduit de type
Reduced Order Model (ROM) provenant d'une décomposition EIM or DEIM, avec ou
sans contraintes de positionnement de mesures.

Pour utiliser cet algorithme, il faut disposer des mesures optimalement
positionnées et de la base réduite associée pour la représentation du modèle.
C'est réalisable selon le schéma suivant, par une analyse préalable à l'aide
d'un :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`, qui
fournit positions et base. Une fois la base construite et les positions
déterminées, il peut être réalisé autant d'interpolations que l'on a de jeu de
mesures aux positions requises, sans devoir refaire l'analyse préalable.

  .. _irm_determination:
  .. image:: images/irm_determination.png
    :align: center
    :width: 95%
  .. centered::
    **Schéma général d'utilisation de l'algorithme**

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/Observation.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Task.rst

.. include:: snippets/ObservationsAlreadyRestrictedOnOptimalLocations.rst

.. include:: snippets/OptimalLocations.rst

.. include:: snippets/ReducedBasis.rst

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
  "ReducedCoordinates",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Analysis.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/Analysis.rst

.. include:: snippets/ReducedCoordinates.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_InterpolationByReducedModelTask_examples:

.. include:: snippets/Header2Algo09.rst

.. --------- ..
.. include:: scripts/simple_InterpolationByReducedModelTask1.rst

.. literalinclude:: scripts/simple_InterpolationByReducedModelTask1.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_InterpolationByReducedModelTask1.res
    :language: none

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Barrault04]_
- [Quarteroni16]_
