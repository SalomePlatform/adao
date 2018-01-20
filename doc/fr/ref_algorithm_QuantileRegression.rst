..
   Copyright (C) 2008-2018 EDF R&D

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

.. index:: single: QuantileRegression
.. _section_ref_algorithm_QuantileRegression:

Algorithme de calcul "*QuantileRegression*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet d'estimer les quantiles conditionnels de la distribution
des paramètres d'état, exprimés à l'aide d'un modèle des variables observées. Ce
sont donc les quantiles sur les variables observées qui vont permettre de
déterminer les paramètres de modèles satisfaisant aux conditions de quantiles.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  .. include:: snippets/Background.rst

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationOperator.rst

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_assimilation_keywords`. De plus, les
paramètres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  .. include:: snippets/Quantile.rst

  .. include:: snippets/MaximumNumberOfSteps.rst

  .. include:: snippets/CostDecrementTolerance_6.rst

  .. include:: snippets/BoundsWithNone.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["BMA", "CostFunctionJ",
    "CostFunctionJb", "CostFunctionJo", "CurrentState", "OMA", "OMB",
    "Innovation", "SimulatedObservationAtBackground",
    "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"].

    Exemple :
    ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

*Astuce pour cet algorithme :*

    Comme les commandes *"BackgroundError"* et *"ObservationError"* sont
    requises pour TOUS les algorithmes de calcul dans l'interface graphique,
    vous devez fournir une valeur, malgré le fait que ces commandes ne sont pas
    requises pour cet algorithme, et ne seront pas utilisées. La manière la
    plus simple est de donner "1" comme un STRING pour les deux.

Informations et variables disponibles à la fin de l'algorithme
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En sortie, après exécution de l'algorithme, on dispose d'informations et de
variables issues du calcul. La description des
:ref:`section_ref_output_variables` indique la manière de les obtenir par la
méthode nommée ``get`` de la variable "*ADD*" du post-processing. Les variables
d'entrée, mises à disposition de l'utilisateur en sortie pour faciliter
l'écriture des procédures de post-processing, sont décrites dans
l':ref:`subsection_r_o_v_Inventaire`.

Les sorties non conditionnelles de l'algorithme sont les suivantes:

  .. include:: snippets/Analysis.rst

  .. include:: snippets/CostFunctionJ.rst

  .. include:: snippets/CostFunctionJb.rst

  .. include:: snippets/CostFunctionJo.rst

Les sorties conditionnelles de l'algorithme sont les suivantes:

  .. include:: snippets/BMA.rst

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/Innovation.rst

  .. include:: snippets/OMA.rst

  .. include:: snippets/OMB.rst

  .. include:: snippets/SimulatedObservationAtBackground.rst

  .. include:: snippets/SimulatedObservationAtCurrentState.rst

  .. include:: snippets/SimulatedObservationAtOptimum.rst

Voir aussi
++++++++++

Références bibliographiques :
  - [Buchinsky98]_
  - [Cade03]_
  - [Koenker00]_
  - [Koenker01]_
  - [WikipediaQR]_
