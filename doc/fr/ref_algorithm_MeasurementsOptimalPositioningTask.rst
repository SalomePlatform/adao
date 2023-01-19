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
.. index:: single: Ensemble de simulations
.. index:: single: Ensemble de snapshots
.. index:: single: Simulations (Ensemble)
.. index:: single: Snapshots (Ensemble)
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
une analyse EIM (Empirical Interpolation Method). Ces positions sont
déterminées de manière itérative, à partir d'un ensemble de vecteurs d'état
pré-existants (usuellement appelés "*snapshots*" en méthodologie de bases
réduites) ou obtenus par une simulation directe au cours de l'algorithme.
Chacun de ces vecteurs d'état est habituellement (mais pas obligatoirement) le
résultat :math:`\mathbf{y}` d'une simulation :math:`H` pour un jeu de
paramètres donné :math:`\mathbf{x}`.

Il y a deux manières d'utiliser cet algorithme:

#. Dans son usage le plus simple, si l'ensemble des vecteurs d'état est
   pré-existant, il suffit de le fournir par l'option "*EnsembleOfSnapshots*"
   d'algorithme.
#. Si l'ensemble des vecteurs d'état doit être obtenu par des simulations au
   cours de l'algorithme, alors on doit fournir l'opérateur de simulation
   :math:`H` et le plan d'expérience de l'espace des états :math:`\mathbf{x}`
   paramétriques.

L'échantillon des états :math:`\mathbf{x}` peut être fourni explicitement ou
sous la forme d'hyper-cubes, explicites ou échantillonnés selon des lois
courantes. Attention à la taille de l'hyper-cube (et donc au nombre de calculs)
qu'il est possible d'atteindre, elle peut rapidement devenir importante.

Il est possible d'exclure a priori des positions potentielles pour les points
de mesures optimaux, en utilisant le variant "*lcEIM*" d'analyse pour une
recherche de positionnement contraint.

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
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  "OptimalPoints",
  "ReducedBasis",
  "Residus",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. include:: snippets/Variant_MOP.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/OptimalPoints.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/EnsembleOfSimulations.rst

.. include:: snippets/EnsembleOfStates.rst

.. include:: snippets/OptimalPoints.rst

.. include:: snippets/ReducedBasis.rst

.. include:: snippets/Residus.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_MeasurementsOptimalPositioningTask_examples:
.. include:: snippets/Header2Algo07.rst

- [Barrault04]_
- [Gong18]_
- [Quarteroni16]_
