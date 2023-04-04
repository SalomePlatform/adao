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

.. _section_reference:

================================================================================
**[DocR]** Description de référence des commandes et mots-clés ADAO
================================================================================

Les sections suivantes présentent la description de référence des commandes et
mots-clés ADAO disponibles à travers l'interface textuelle (TUI), graphique
(GUI) ou à travers des scripts. Les deux premières sections communes présentent
les :ref:`section_reference_entry` et les
:ref:`section_reference_special_entry`. Ensuite, on décrit successivement les
:ref:`section_reference_assimilation` et les :ref:`section_reference_checking`.

Chaque commande ou mot-clé à définir par la TUI ou la GUI a des propriétés
particulières. La première propriété est d'être *requise*, *optionnelle* ou
simplement utile, décrivant un type d'entrée. La seconde propriété est d'être
une variable "ouverte" avec un type fixé mais avec n'importe quelle valeur
autorisée par le type, ou une variable "fermée", limitée à des valeurs
spécifiées. L'éditeur graphique GUI intégré disposant de capacités intrinsèques
de validation, les propriétés des commandes ou mots-clés données à l'aide de
l'interface graphique sont automatiquement correctes.

.. _section_reference_entry:

================================================================================
**[DocR]** Entrées et sorties générales
================================================================================

Cette section décrit de manière générale les différentes options de types
d'entrées et de variables de sortie. Les notations mathématiques utilisées sont
expliquées dans la section :ref:`section_theory`.

.. toctree::
   :maxdepth: 1

   ref_entry_types
   ref_options_AlgorithmParameters
   ref_output_variables

.. _section_reference_special_entry:

==========================================================================================
**[DocR]** Entrées spéciales : mesures, fonctions, matrices, "*observer*", post-traitement
==========================================================================================

Cette section décrit les entrées spéciales, comme les formes fonctionnelles ou
matricielles, et les conditions requises pour les utiliser. Les notions et
notations mathématiques relatives à ces entrées sont expliquées dans la section
:ref:`section_theory`.

.. toctree::
   :maxdepth: 1

   ref_observations_requirements
   ref_operator_requirements
   ref_covariance_requirements
   ref_observers_requirements
   ref_userpostanalysis_requirements

.. _section_reference_assimilation:

================================================================================
**[DocR]** Cas d'assimilation de données ou d'optimisation
================================================================================

Cette section décrit les choix algorithmiques pour utiliser des méthodes
d'assimilation de données, des méthodes d'optimisation ou des méthodes avec
réduction, disponibles dans ADAO, en détaillant leurs caractéristiques et leurs
options.

Des exemples sur l'usage de ces commandes sont disponibles dans la section des
:ref:`section_tutorials_in_salome`, dans la section des
:ref:`section_tutorials_in_python`, dans la section des
:ref:`section_docu_examples`, et dans les fichiers d'exemple installés avec
ADAO. Les notions et notations mathématiques utilisées sont expliquées dans la
section générale donnant :ref:`section_theory`.

.. toctree::
   :maxdepth: 1

   ref_algorithm_3DVAR
   ref_algorithm_4DVAR
   ref_algorithm_Blue
   ref_algorithm_DerivativeFreeOptimization
   ref_algorithm_DifferentialEvolution
   ref_algorithm_EnsembleBlue
   ref_algorithm_EnsembleKalmanFilter
   ref_algorithm_ExtendedBlue
   ref_algorithm_ExtendedKalmanFilter
   ref_algorithm_KalmanFilter
   ref_algorithm_LinearLeastSquares
   ref_algorithm_NonLinearLeastSquares
   ref_algorithm_ParticleSwarmOptimization
   ref_algorithm_QuantileRegression
   ref_algorithm_TabuSearch
   ref_algorithm_UnscentedKalmanFilter
   ref_assimilation_keywords

.. _section_reference_checking:

================================================================================
**[DocR]** Cas de vérification
================================================================================

Cette section décrit les algorithmes de vérification disponibles dans ADAO,
détaillant leurs caractéristiques d'utilisation et leurs options.

Des exemples sur l'usage de ces commandes sont disponibles dans la section des
:ref:`section_tutorials_in_salome`, dans la section des
:ref:`section_tutorials_in_python`, dans la section des
:ref:`section_docu_examples`, et dans les fichiers d'exemple installés avec
ADAO. Les notions et notations mathématiques utilisées sont expliquées dans la
section générale donnant :ref:`section_theory`.

.. toctree::
   :maxdepth: 1

   ref_algorithm_AdjointTest
   ref_algorithm_ControledFunctionTest
   ref_algorithm_FunctionTest
   ref_algorithm_GradientTest
   ref_algorithm_InputValuesTest
   ref_algorithm_LinearityTest
   ref_algorithm_LocalSensitivityTest
   ref_algorithm_ObservationSimulationComparisonTest
   ref_algorithm_ObserverTest
   ref_algorithm_ParallelFunctionTest
   ref_algorithm_SamplingTest
   ref_algorithm_TangentTest
   ref_checking_keywords

.. _section_reference_task:

================================================================================
**[DocR]** Cas orientés tâches ou études dédiées
================================================================================

Cette section décrit les algorithmes de tâches facilitant une étude dédiée
disponibles dans ADAO, détaillant leurs caractéristiques d'utilisation et leurs
options.

Ces tâches utilisent des algorithmes provenant de méthodes d'assimilation de
données, de méthodes d'optimisation ou de méthodes avec réduction. On renvoie à
la section générale donnant :ref:`section_theory` et à celle des
:ref:`section_reference_assimilation` pour les détails algorithmiques
sous-jacents.

.. toctree::
   :maxdepth: 1

   ref_algorithm_EnsembleOfSimulationGenerationTask
   ref_algorithm_MeasurementsOptimalPositioningTask
   ref_task_keywords
