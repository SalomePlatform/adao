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

.. index:: single: Blue
.. _section_ref_algorithm_Blue:

Algorithme de calcul "*Blue*"
-----------------------------

Description
+++++++++++

Cet algorithme réalise une estimation de type BLUE (Best Linear Unbiased
Estimator) de l'état d'un système. De manière précise, c'est un estimateur
d'Aitken.

Cet algorithme est toujours le plus rapide de l'ensemble des algorithmes
d'assimilation d'ADAO. Il est théoriquement réservé aux cas d'opérateurs
d'observation linéaires, même s'il fonctionne parfois dans les cas "faiblement"
non-linéaires. On peut vérifier la linéarité de l'opérateur d'observation à
l'aide de l':ref:`section_ref_algorithm_LinearityTest`.

En cas de non-linéarité, même peu marquée, on lui préférera aisément
l':ref:`section_ref_algorithm_ExtendedBlue` ou
l':ref:`section_ref_algorithm_3DVAR`.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: StoreSupplementaryCalculations
.. index:: single: Quantiles
.. index:: single: SetSeed
.. index:: single: NumberOfSamplesForQuantiles
.. index:: single: SimulationForQuantiles

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  Background
    *Commande obligatoire*. Elle définit le vecteur d'ébauche ou
    d'initialisation, noté précédemment :math:`\mathbf{x}^b`. Sa valeur est
    définie comme un objet de type "*Vector*" ou de type "*VectorSerie*".

  BackgroundError
    *Commande obligatoire*. Elle définit la matrice de covariance des erreurs
    d'ébauche, notée précédemment :math:`\mathbf{B}`. Sa valeur est définie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  Observation
    *Commande obligatoire*. Elle définit le vecteur d'observation utilisé en
    assimilation de données ou en optimisation, et noté précédemment
    :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de type "*Vector*"
    ou de type "*VectorSerie*".

  ObservationError
    *Commande obligatoire*. Elle définit la matrice de covariance des erreurs
    d'ébauche, notée précédemment :math:`\mathbf{R}`. Sa valeur est définie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  ObservationOperator
    *Commande obligatoire*. Elle indique l'opérateur d'observation, noté
    précédemment :math:`H`, qui transforme les paramètres d'entrée
    :math:`\mathbf{x}` en résultats :math:`\mathbf{y}` qui sont à comparer aux
    observations :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de
    type "*Function*" ou de type "*Matrix*". Dans le cas du type "*Function*",
    différentes formes fonctionnelles peuvent être utilisées, comme décrit dans
    la section :ref:`section_ref_operator_requirements`. Si un contrôle
    :math:`U` est inclus dans le modèle d'observation, l'opérateur doit être
    appliqué à une paire :math:`(X,U)`.

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_assimilation_keywords`. De plus, les
paramètres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["APosterioriCorrelations",
    "APosterioriCovariance", "APosterioriStandardDeviations",
    "APosterioriVariances", "BMA", "OMA", "OMB", "CurrentState",
    "CostFunctionJ", "CostFunctionJb", "CostFunctionJo", "Innovation",
    "SigmaBck2", "SigmaObs2", "MahalanobisConsistency", "SimulationQuantiles",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum"].

    Exemple : ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

  Quantiles
    Cette liste indique les valeurs de quantile, entre 0 et 1, à estimer par
    simulation autour de l'état optimal. L'échantillonnage utilise des tirages
    aléatoires gaussiens multivariés, dirigés par la matrice de covariance a
    posteriori. Cette option n'est utile que si le calcul supplémentaire
    "SimulationQuantiles" a été choisi. La valeur par défaut est une liste vide.

    Exemple : ``{"Quantiles":[0.1,0.9]}``

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

    Exemple : ``{"SetSeed":1000}``

  NumberOfSamplesForQuantiles
    Cette clé indique le nombre de simulations effectuées pour estimer les
    quantiles. Cette option n'est utile que si le calcul supplémentaire
    "SimulationQuantiles" a été choisi. Le défaut est 100, ce qui suffit souvent
    pour une estimation correcte de quantiles courants à 5%, 10%, 90% ou 95%.

    Exemple : ``{"NumberOfSamplesForQuantiles":100}``

  SimulationForQuantiles
    Cette clé indique le type de simulation, linéaire (avec l'opérateur
    d'observation tangent appliqué sur des incréments de perturbations autour de
    l'état optimal) ou non-linéaire (avec l'opérateur d'observation standard
    appliqué aux états perturbés), que l'on veut faire pour chaque perturbation.
    Cela change essentiellement le temps de chaque simulation élémentaire,
    usuellement plus long en non-linéaire qu'en linéaire. Cette option n'est
    utile que si le calcul supplémentaire "SimulationQuantiles" a été choisi. La
    valeur par défaut est "Linear", et les choix possibles sont "Linear" et
    "NonLinear".

    Exemple : ``{"SimulationForQuantiles":"Linear"}``

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

  Analysis
    *Liste de vecteurs*. Chaque élément est un état optimal :math:`\mathbf{x}*`
    en optimisation ou une analyse :math:`\mathbf{x}^a` en assimilation de
    données.

    Exemple : ``Xa = ADD.get("Analysis")[-1]``

Les sorties conditionnelles de l'algorithme sont les suivantes:

  APosterioriCorrelations
    *Liste de matrices*. Chaque élément est une matrice de corrélation des
    erreurs *a posteriori* de l'état optimal.

    Exemple : ``C = ADD.get("APosterioriCorrelations")[-1]``

  APosterioriCovariance
    *Liste de matrices*. Chaque élément est une matrice :math:`\mathbf{A}*` de
    covariances des erreurs *a posteriori* de l'état optimal.

    Exemple : ``A = ADD.get("APosterioriCovariance")[-1]``

  APosterioriStandardDeviations
    *Liste de matrices*. Chaque élément est une matrice d'écart-types des
    erreurs *a posteriori* de l'état optimal.

    Exemple : ``E = ADD.get("APosterioriStandardDeviations")[-1]``

  APosterioriVariances
    *Liste de matrices*. Chaque élément est une matrice de variances des erreurs
    *a posteriori* de l'état optimal.

    Exemple : ``V = ADD.get("APosterioriVariances")[-1]``

  BMA
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'ébauche et l'état optimal.

    Exemple : ``bma = ADD.get("BMA")[-1]``

  CostFunctionJ
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J`.

    Exemple : ``J = ADD.get("CostFunctionJ")[:]``

  CostFunctionJb
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J^b`, c'est-à-dire de la partie écart à l'ébauche.

    Exemple : ``Jb = ADD.get("CostFunctionJb")[:]``

  CostFunctionJo
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J^o`, c'est-à-dire de la partie écart à l'observation.

    Exemple : ``Jo = ADD.get("CostFunctionJo")[:]``

  Innovation
    *Liste de vecteurs*. Chaque élément est un vecteur d'innovation, qui est
    en statique l'écart de l'optimum à l'ébauche, et en dynamique l'incrément
    d'évolution.

    Exemple : ``d = ADD.get("Innovation")[-1]``

  MahalanobisConsistency
    *Liste de valeurs*. Chaque élément est une valeur de l'indicateur de
    qualité de Mahalanobis.

    Exemple : ``m = ADD.get("MahalanobisConsistency")[-1]``

  OMA
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'observation et l'état optimal dans l'espace des observations.

    Exemple : ``oma = ADD.get("OMA")[-1]``

  OMB
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'observation et l'état d'ébauche dans l'espace des observations.

    Exemple : ``omb = ADD.get("OMB")[-1]``

  SigmaBck2
    *Liste de valeurs*. Chaque élément est une valeur de l'indicateur de
    qualité :math:`(\sigma^b)^2` de la partie ébauche.

    Exemple : ``sb2 = ADD.get("SigmaBck")[-1]``

  SigmaObs2
    *Liste de valeurs*. Chaque élément est une valeur de l'indicateur de
    qualité :math:`(\sigma^o)^2` de la partie observation.

    Exemple : ``so2 = ADD.get("SigmaObs")[-1]``

  SimulatedObservationAtBackground
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'ébauche :math:`\mathbf{x}^b`.

    Exemple : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtOptimum
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'analyse ou de l'état optimal :math:`\mathbf{x}^a`.

    Exemple : ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``

  SimulationQuantiles
    *Liste de vecteurs*. Chaque élément est un vecteur correspondant à l'état
    observé qui réalise le quantile demandé, dans le même ordre que les
    quantiles requis par l'utilisateur.

    Exemple : ``sQuantiles = ADD.get("SimulationQuantiles")[:]``

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_ExtendedBlue`
  - :ref:`section_ref_algorithm_3DVAR`
  - :ref:`section_ref_algorithm_LinearityTest`

Références bibliographiques :
  - [Bouttier99]_
