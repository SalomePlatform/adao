..
   Copyright (C) 2008-2023 EDF R&D

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

.. index:: single: MeasurementsOptimalPositioningTask
.. index:: single: Positionnement optimal de mesures
.. index:: single: Positions de mesures
.. index:: single: Mesures (Positionnement optimal)
.. _section_ref_algorithm_MeasurementsOptimalPositioningTask:

Algorithme de tâche "*MeasurementsOptimalPositioningTask*"
----------------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. warning::

  Cet algorithme n'est utilisable qu'en interface textuelle (TUI) et pas en
  interface graphique (GUI).

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet d'établir la position de points de mesures optimaux par
une analyse EIM (Empirical Interpolation Method), de manière itérative à partir
d'un ensemble de vecteurs d'état (usuellement appelés "*snapshots*" en
méthodologie de bases réduites).

Chacun de ces vecteurs d'état est habituellement (mais pas obligatoirement) le
résultat :math:`\mathbf{y}` d'une simulation :math:`H` pour un jeu de
paramètres donné :math:`\mathbf{x}=\mu`. Dans son usage le plus simple, si
l'ensemble des vecteurs d'état est pré-existant, il suffit de le fournir par
les options d'algorithme.

Il est aussi possible d'exclure a priori des positions potentielles pour les
points de mesures optimaux, en utilisant l'analyse "*lcEIM*" pour une recherche
de positionnement contraint.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

*Aucune*

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Task.rst

.. include:: snippets/EnsembleOfSnapshots.rst

.. include:: snippets/ExcludeLocations.rst

.. include:: snippets/ErrorNorm.rst

.. include:: snippets/ErrorNormTolerance.rst

.. include:: snippets/MaximumNumberOfLocations.rst

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
  "EnsembleOfSnapshots",
  "OptimalPoints",
  "ReducedBasis",
  "Residus",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

.. include:: snippets/Variant_MOP.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/OptimalPoints.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/EnsembleOfSnapshots.rst

.. include:: snippets/OptimalPoints.rst

.. include:: snippets/ReducedBasis.rst

.. include:: snippets/Residus.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_MeasurementsOptimalPositioningTask_examples:
.. include:: snippets/Header2Algo07.rst

- [Barrault04]_
- [Gong18]_
- [Quarteroni16]_
