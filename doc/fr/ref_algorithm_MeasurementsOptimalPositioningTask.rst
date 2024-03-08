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

.. index:: single: MeasurementsOptimalPositioningTask
.. index:: single: Positionnement optimal de mesures
.. index:: single: Positions de mesures
.. index:: single: Mesures (Positionnement optimal)
.. index:: single: Ensemble de simulations
.. index:: single: Ensemble de snapshots
.. index:: single: Simulations (Ensemble)
.. index:: single: Snapshots (Ensemble)
.. index:: single: Reduced Order Model
.. index:: single: ROM
.. _section_ref_algorithm_MeasurementsOptimalPositioningTask:

Algorithme de tâche "*MeasurementsOptimalPositioningTask*"
----------------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo00.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet d'établir la position optimale de mesures d'un champ
physique :math:`\mathbf{y}`, pour en assurer l'interpolation la meilleure
possible. Ces positions optimales de mesure sont déterminées de manière
itérative, à partir d'un ensemble de vecteurs d'état :math:`\mathbf{y}`
pré-existants (usuellement appelés "*snapshots*" en méthodologie de bases
réduites) ou obtenus par une simulation de ce(s) champ(s) physiqu(e) d'intérêt
au cours de l'algorithme. Chacun de ces vecteurs d'état est habituellement
(mais pas obligatoirement) le résultat :math:`\mathbf{y}` d'une simulation à
l'aide de l'opérateur :math:`H` restituant le (ou les) champ(s) complet(s) pour
un jeu de paramètres donné :math:`\mathbf{x}`, ou d'une observation explicite
du (ou des) champ(s) complet(s) :math:`\mathbf{y}`.

Pour établir la position optimale de mesures, on utilise une méthode de type
Empirical Interpolation Method (EIM [Barrault04]_) ou Discrete Empirical
Interpolation Method (DEIM [Chaturantabut10]_), qui établit un modèle réduit de
type Reduced Order Model (ROM), avec contraintes (variante "*lcEIM*" ou
"*lcDEIM*") ou sans contraintes (variante "*EIM*" ou "*DEIM*") de
positionnement. Pour la performance, il est recommandé d'utiliser la variante
"*lcEIM*" ou "*EIM*" lorsque la dimension de l'espace des champs complets est
grande.

Il y a deux manières d'utiliser cet algorithme:

#. Dans son usage le plus simple, si l'ensemble des vecteurs d'état physique
   :math:`\mathbf{y}` est pré-existant, il suffit de le fournir sous la forme
   d'une collection ordonnée par l'option "*EnsembleOfSnapshots*" de
   l'algorithme. C'est par exemple ce que l'on obtient par défaut si l'ensemble
   des états a été généré par un
   :ref:`section_ref_algorithm_EnsembleOfSimulationGenerationTask`.
#. Si l'ensemble des vecteurs d'état physique :math:`\mathbf{y}` doit être
   obtenu par des simulations explicites au cours de l'algorithme, alors on
   doit fournir à la fois l'opérateur de simulation du champ complet, ici
   identifié à l'opérateur d'observation :math:`H` du champ complet, et le plan
   d'expérience de l'espace des états :math:`\mathbf{x}` paramétriques.

Dans le cas où l'on fournit le plan d'expérience, l'échantillonnage des états
:math:`\mathbf{x}` peut être fourni comme pour un
:ref:`section_ref_algorithm_EnsembleOfSimulationGenerationTask`, explicitement
ou sous la forme d'hypercubes, explicites ou échantillonnés selon des
distributions courantes, ou à l'aide d'un échantillonnage par hypercube latin
(LHS) ou par séquence de Sobol. Les calculs sont optimisés selon les ressources
informatiques disponibles et les options demandées par l'utilisateur. On pourra
se reporter aux :ref:`section_ref_sampling_requirements` pour une illustration
de l'échantillonnage. Attention à la taille de l'hypercube (et donc au nombre
de calculs) qu'il est possible d'atteindre, elle peut rapidement devenir
importante. La mémoire requise est ensuite le produit de la taille d'un état
individuel :math:`\mathbf{y}` par la taille de l'hypercube.

  .. _mop_determination:
  .. image:: images/mop_determination.png
    :align: center
    :width: 95%
  .. centered::
    **Schéma général d'utilisation de l'algorithme**

Il est possible d'exclure a priori des positions potentielles pour le
positionnement des mesures, en utilisant le variant "*lcEIM*" ou "*lcDEIM*"
d'analyse pour une recherche de positionnement contraint.

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

.. include:: snippets/NameOfLocations.rst

.. include:: snippets/ReduceMemoryUse.rst

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
  "EnsembleOfSimulations",
  "EnsembleOfStates",
  "ExcludedPoints",
  "OptimalPoints",
  "ReducedBasis",
  "Residus",
  "SingularValues",
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

.. include:: snippets/ExcludedPoints.rst

.. include:: snippets/OptimalPoints.rst

.. include:: snippets/ReducedBasis.rst

.. include:: snippets/Residus.rst

.. include:: snippets/SingularValues.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_MeasurementsOptimalPositioningTask_examples:

.. include:: snippets/Header2Algo09.rst

.. --------- ..
.. include:: scripts/simple_MeasurementsOptimalPositioningTask1.rst

.. literalinclude:: scripts/simple_MeasurementsOptimalPositioningTask1.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_MeasurementsOptimalPositioningTask1.res
    :language: none

.. --------- ..
.. include:: scripts/simple_MeasurementsOptimalPositioningTask2.rst

.. literalinclude:: scripts/simple_MeasurementsOptimalPositioningTask2.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_MeasurementsOptimalPositioningTask2.res
    :language: none

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_ParallelFunctionTest`
- :ref:`section_ref_algorithm_EnsembleOfSimulationGenerationTask`

.. ------------------------------------ ..
.. include:: snippets/Header2Algo07.rst

- [Barrault04]_
- [Chaturantabut10]_
- [Gong18]_
- [Quarteroni16]_
