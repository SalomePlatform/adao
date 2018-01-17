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

.. index:: single: DerivativeFreeOptimization
.. _section_ref_algorithm_DerivativeFreeOptimization:

Algorithme de calcul "*DerivativeFreeOptimization*"
----------------------------------------------------

.. warning::

  dans sa présente version, cet algorithme est expérimental, et reste donc
  susceptible de changements dans les prochaines versions.

Description
+++++++++++

Cet algorithme réalise une estimation d'état d'un système par minimisation d'une
fonctionnelle d'écart :math:`J` sans gradient. C'est une méthode qui n'utilise
pas les dérivées de la fonctionnelle d'écart. Elle entre, par exemple, dans la
même catégorie que l':ref:`section_ref_algorithm_ParticleSwarmOptimization`.

C'est une méthode d'optimisation permettant la recherche du minimum global d'une
fonctionnelle d'erreur :math:`J` quelconque de type :math:`L^1`, :math:`L^2` ou
:math:`L^{\infty}`, avec ou sans pondérations. La fonctionnelle d'erreur par
défaut est celle de moindres carrés pondérés augmentés, classiquement utilisée
en assimilation de données.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Minimizer
.. index:: single: MaximumNumberOfSteps
.. index:: single: MaximumNumberOfFunctionEvaluations
.. index:: single: StateVariationTolerance
.. index:: single: CostDecrementTolerance
.. index:: single: QualityCriterion
.. index:: single: StoreSupplementaryCalculations

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

  Minimizer
    Cette clé permet de changer le minimiseur pour l'optimiseur. Le choix par
    défaut est "BOBYQA", et les choix possibles sont
    "BOBYQA" (minimisation avec ou sans contraintes par approximation quadratique [Powell09]_),
    "COBYLA" (minimisation avec ou sans contraintes par approximation linéaire [Powell94]_ [Powell98]_).
    "NEWUOA" (minimisation avec ou sans contraintes par approximation quadratique itérative [Powell04]_),
    "POWELL" (minimisation sans contraintes de type directions conjuguées [Powell64]_),
    "SIMPLEX" (minimisation avec ou sans contraintes de type simplexe ou Nelder-Mead, voir [Nelder65]_),
    "SUBPLEX" (minimisation avec ou sans contraintes de type simplexe sur une suite de sous-espaces [Rowan90]_).
    Remarque : la méthode "POWELL" effectue une optimisation par boucles
    imbriquées interne/externe, conduisant ainsi à un contrôle relaché du
    nombre d'évaluations de la fonctionnelle à optimiser. Si un contrôle précis
    du nombre d'évaluations de cette fonctionnelle est requis, il faut choisir
    un autre minimiseur.

    Exemple : ``{"Minimizer":"BOBYQA"}``

  Bounds
    Cette clé permet de définir des bornes supérieure et inférieure pour chaque
    variable d'état optimisée. Les bornes doivent être données par une liste de
    liste de paires de bornes inférieure/supérieure pour chaque variable, avec
    une valeur ``None`` chaque fois qu'il n'y a pas de borne. Les bornes peuvent
    toujours être spécifiées, mais seuls les optimiseurs sous contraintes les
    prennent en compte.

    Exemple : ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``

  MaximumNumberOfSteps
    Cette clé indique le nombre maximum d'itérations possibles en optimisation
    itérative. Le défaut est 15000, qui est une limite arbitraire. Il est ainsi
    fortement recommandé d'adapter ce paramètre aux besoins pour des problèmes
    réels. Pour certains optimiseurs, le nombre de pas effectif d'arrêt peut
    être légèrement différent de la limite à cause d'exigences de contrôle
    interne de l'algorithme.

    Exemple : ``{"MaximumNumberOfSteps":50}``

  MaximumNumberOfFunctionEvaluations
    Cette clé indique le nombre maximum d'évaluations possibles de la
    fonctionnelle à optimiser. Le défaut est de 15000, qui est une limite
    arbitraire. Il est ainsi recommandé d'adapter ce paramètre aux besoins pour
    des problèmes réels. Pour certains optimiseurs, le nombre effectif
    d'évaluations à l'arrêt peut être légèrement différent de la limite à cause
    d'exigences de déroulement interne de l'algorithme.

    Exemple : ``{"MaximumNumberOfFunctionEvaluations":50}``

  StateVariationTolerance
    Cette clé indique la variation relative maximale de l'état lors pour l'arrêt
    par convergence sur l'état. Le défaut est de 1.e-4, et il est recommandé
    de l'adapter aux besoins pour des problèmes réels.

    Exemple : ``{"StateVariationTolerance":1.e-4}``

  CostDecrementTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la fonction coût décroît moins que cette
    tolérance au dernier pas. Le défaut est de 1.e-7, et il est recommandé
    de l'adapter aux besoins pour des problèmes réels.

    Exemple : ``{"CostDecrementTolerance":1.e-7}``

  QualityCriterion
    Cette clé indique le critère de qualité, qui est minimisé pour trouver
    l'estimation optimale de l'état. Le défaut est le critère usuel de
    l'assimilation de données nommé "DA", qui est le critère de moindres carrés
    pondérés augmentés. Les critères possibles sont dans la liste suivante, dans
    laquelle les noms équivalents sont indiqués par un signe "=" :
    ["AugmentedWeightedLeastSquares"="AWLS"="DA", "WeightedLeastSquares"="WLS",
    "LeastSquares"="LS"="L2", "AbsoluteValue"="L1",  "MaximumError"="ME"].

    Exemple : ``{"QualityCriterion":"DA"}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["BMA", "CostFunctionJ",
    "CostFunctionJb", "CostFunctionJo", "CostFunctionJAtCurrentOptimum",
    "CostFunctionJbAtCurrentOptimum", "CostFunctionJoAtCurrentOptimum",
    "CurrentOptimum", "CurrentState", "IndexOfOptimum",
    "InnovationAtCurrentState", "OMA", "OMB",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentOptimum",
    "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"].

    Exemple : ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

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

  CurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'état courant utilisé
    au cours du déroulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

Les sorties conditionnelles de l'algorithme sont les suivantes:

  CostFunctionJAtCurrentOptimum
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J`. A chaque pas, la valeur correspond à l'état optimal trouvé depuis
    le début.

    Exemple : ``JACO = ADD.get("CostFunctionJAtCurrentOptimum")[:]``

  CostFunctionJbAtCurrentOptimum
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J^b`, c'est-à-dire de la partie écart à l'ébauche. A chaque pas, la
    valeur correspond à l'état optimal trouvé depuis le début.

    Exemple : ``JbACO = ADD.get("CostFunctionJbAtCurrentOptimum")[:]``

  CostFunctionJoAtCurrentOptimum
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J^o`, c'est-à-dire de la partie écart à l'observation. A chaque pas,
    la valeur correspond à l'état optimal trouvé depuis le début.

    Exemple : ``JoACO = ADD.get("CostFunctionJoAtCurrentOptimum")[:]``

  CurrentOptimum
    *Liste de vecteurs*. Chaque élément est le vecteur d'état optimal au pas de
    temps courant au cours du déroulement de l'algorithme d'optimisation. Ce
    n'est pas nécessairement le dernier état.

    Exemple : ``Xo = ADD.get("CurrentOptimum")[:]``

  IndexOfOptimum
    *Liste d'entiers*. Chaque élément est l'index d'itération de l'optimum
    obtenu au cours du déroulement de l'algorithme d'optimisation. Ce n'est pas
    nécessairement le numéro de la dernière itération.

    Exemple : ``i = ADD.get("IndexOfOptimum")[-1]``

  InnovationAtCurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'innovation à l'état
    courant.

    Exemple : ``ds = ADD.get("InnovationAtCurrentState")[-1]``

  OMA
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'observation et l'état optimal dans l'espace des observations.

    Exemple : ``oma = ADD.get("OMA")[-1]``

  OMB
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'observation et l'état d'ébauche dans l'espace des observations.

    Exemple : ``omb = ADD.get("OMB")[-1]``

  SimulatedObservationAtBackground
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'ébauche :math:`\mathbf{x}^b`.

    Exemple : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtCurrentOptimum
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'état optimal au pas de temps courant au cours du déroulement de
    l'algorithme d'optimisation, c'est-à-dire dans l'espace des observations.

    Exemple : ``hxo = ADD.get("SimulatedObservationAtCurrentOptimum")[-1]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur observé à l'état courant,
    c'est-à-dire dans l'espace des observations.

    Exemple : ``Ys = ADD.get("SimulatedObservationAtCurrentState")[-1]``

  SimulatedObservationAtOptimum
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'analyse ou de l'état optimal :math:`\mathbf{x}^a`.

    Exemple : ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_ParticleSwarmOptimization`

Références bibliographiques :
  - [Johnson08]_
  - [Nelder65]_
  - [Powell64]_
  - [Powell94]_
  - [Powell98]_
  - [Powell04]_
  - [Powell07]_
  - [Powell09]_
  - [Rowan90]_
