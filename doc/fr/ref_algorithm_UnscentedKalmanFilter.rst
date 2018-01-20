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

.. index:: single: UnscentedKalmanFilter
.. _section_ref_algorithm_UnscentedKalmanFilter:

Algorithme de calcul "*UnscentedKalmanFilter*"
----------------------------------------------

Description
+++++++++++

Cet algorithme réalise une estimation de l'état d'un système dynamique par un
filtre de Kalman "unscented", permettant d'éviter de devoir calculer les
opérateurs tangent ou adjoint pour les opérateurs d'observation ou d'évolution,
comme dans les filtres de Kalman simple ou étendu.

Il s'applique aux cas d'opérateurs d'observation et d'évolution incrémentale
(processus) non-linéaires et présente d'excellentes qualités de robustesse et
de performances. Il peut être comparé à
l':ref:`section_ref_algorithm_EnsembleKalmanFilter`, dont les qualités sont
similaires pour les systèmes non-linéaires.

Dans le cas d'opérateurs linéaires ou "faiblement" non-linéaire, on peut
aisément utiliser l':ref:`section_ref_algorithm_ExtendedKalmanFilter` ou même
l':ref:`section_ref_algorithm_KalmanFilter`, qui sont souvent largement moins
coûteux en évaluation sur de petits systèmes. On peut vérifier la linéarité des
opérateurs à l'aide de l':ref:`section_ref_algorithm_LinearityTest`.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  .. include:: snippets/Background.rst

  .. include:: snippets/BackgroundError.rst

  .. include:: snippets/EvolutionError.rst

  .. include:: snippets/EvolutionModel.rst

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationError.rst

  .. include:: snippets/ObservationOperator.rst

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_assimilation_keywords`. De plus, les
paramètres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  .. include:: snippets/BoundsWithExtremes.rst

  .. include:: snippets/ConstrainedBy.rst

  .. include:: snippets/EstimationOf.rst

  Alpha, Beta, Kappa, Reconditioner
    .. index:: single: Alpha
    .. index:: single: Beta
    .. index:: single: Kappa
    .. index:: single: Reconditioner

    Ces clés sont des paramètres de mise à l'échelle interne. "Alpha" requiert
    une valeur comprise entre 1.e-4 et 1. "Beta" a une valeur optimale de 2 pour
    une distribution *a priori* gaussienne. "Kappa" requiert une valeur entière,
    dont la bonne valeur par défaut est obtenue en la mettant à 0.
    "Reconditioner" requiert une valeur comprise entre 1.e-3 et 10, son défaut
    étant 1.

    Exemple :
    ``{"Alpha":1,"Beta":2,"Kappa":0,"Reconditioner":1}``

  StoreSupplementaryCalculations


    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["APosterioriCorrelations",
    "APosterioriCovariance", "APosterioriStandardDeviations",
    "APosterioriVariances", "BMA", "CostFunctionJ", "CostFunctionJb",
    "CostFunctionJo", "CurrentState", "Innovation"].

    Exemple :
    ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

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

Les sorties conditionnelles de l'algorithme sont les suivantes:

  .. include:: snippets/APosterioriCorrelations.rst

  .. include:: snippets/APosterioriCovariance.rst

  .. include:: snippets/APosterioriStandardDeviations.rst

  .. include:: snippets/APosterioriVariances.rst

  .. include:: snippets/BMA.rst

  .. include:: snippets/CostFunctionJ.rst

  .. include:: snippets/CostFunctionJb.rst

  .. include:: snippets/CostFunctionJo.rst

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/Innovation.rst

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_KalmanFilter`
  - :ref:`section_ref_algorithm_ExtendedKalmanFilter`
  - :ref:`section_ref_algorithm_EnsembleKalmanFilter`

Références bibliographiques :
  - [WikipediaUKF]_
