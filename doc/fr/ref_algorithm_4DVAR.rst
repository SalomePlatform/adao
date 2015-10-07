..
   Copyright (C) 2008-2015 EDF R&D

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

.. index:: single: 4DVAR
.. _section_ref_algorithm_4DVAR:

Algorithme de calcul "*4DVAR*"
------------------------------

.. warning::

  dans sa présente version, cet algorithme est expérimental, et reste donc
  susceptible de changements dans les prochaines versions.

Description
+++++++++++

Cet algorithme réalise une estimation de l'état d'un système dynamique, par une
méthode de minimisation variationnelle de la fonctionnelle :math:`J` d'écart
classique en assimilation de données :

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\sum_{t\in T}(\mathbf{y^o}(t)-H(\mathbf{x},t))^T.\mathbf{R}^{-1}.(\mathbf{y^o}(t)-H(\mathbf{x},t))

qui est usuellement désignée comme la fonctionnelle "*4D-VAR*" (voir par exemple
[Talagrand97]_). Il est bien adapté aux cas d'opérateurs d'observation et
d'évolution non-linéaires, son domaine d'application est comparable aux
algorithmes de filtrage de Kalman et en particulier
l':ref:`section_ref_algorithm_ExtendedKalmanFilter` ou
l':ref:`section_ref_algorithm_UnscentedKalmanFilter`.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Bounds
.. index:: single: ConstrainedBy
.. index:: single: EstimationOf
.. index:: single: MaximumNumberOfSteps
.. index:: single: CostDecrementTolerance
.. index:: single: ProjectedGradientTolerance
.. index:: single: GradientNormTolerance
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
    défaut est "LBFGSB", et les choix possibles sont "LBFGSB" (minimisation non
    linéaire sous contraintes, voir [Byrd95]_, [Morales11]_ et [Zhu97]_), "TNC"
    (minimisation non linéaire sous contraintes), "CG" (minimisation non
    linéaire sans contraintes), "BFGS" (minimisation non linéaire sans
    contraintes), "NCG" (minimisation de type gradient conjugué de Newton). Il
    est fortement conseillé de conserver la valeur par défaut.

    Exemple : ``{"Minimizer":"LBFGSB"}``

  Bounds
    Cette clé permet de définir des bornes supérieure et inférieure pour chaque
    variable d'état optimisée. Les bornes doivent être données par une liste de
    liste de paires de bornes inférieure/supérieure pour chaque variable, avec
    une valeur ``None`` chaque fois qu'il n'y a pas de borne. Les bornes peuvent
    toujours être spécifiées, mais seuls les optimiseurs sous contraintes les
    prennent en compte.

    Exemple : ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``

  ConstrainedBy
    Cette clé permet d'indiquer la méthode de prise en compte des contraintes de
    bornes. La seule disponible est "EstimateProjection", qui projete
    l'estimation de l'état courant sur les contraintes de bornes.

    Exemple : ``{"ConstrainedBy":"EstimateProjection"}``

  MaximumNumberOfSteps
    Cette clé indique le nombre maximum d'itérations possibles en optimisation
    itérative. Le défaut est 15000, qui est très similaire à une absence de
    limite sur les itérations. Il est ainsi recommandé d'adapter ce paramètre
    aux besoins pour des problèmes réels. Pour certains optimiseurs, le nombre
    de pas effectif d'arrêt peut être légèrement différent de la limite à cause
    d'exigences de contrôle interne de l'algorithme.

    Exemple : ``{"MaximumNumberOfSteps":100}``

  CostDecrementTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la fonction coût décroît moins que cette
    tolérance au dernier pas. Le défaut est de 1.e-7, et il est recommandé
    de l'adapter aux besoins pour des problèmes réels.

    Exemple : ``{"CostDecrementTolerance":1.e-7}``

  EstimationOf
    Cette clé permet de choisir le type d'estimation à réaliser. Cela peut être
    soit une estimation de l'état, avec la valeur "State", ou une estimation de
    paramètres, avec la valeur "Parameters". Le choix par défaut est "State".

    Exemple : ``{"EstimationOf":"Parameters"}``

  ProjectedGradientTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque toutes les composantes du gradient projeté
    sont en-dessous de cette limite. C'est utilisé uniquement par les
    optimiseurs sous contraintes. Le défaut est -1, qui désigne le défaut
    interne de chaque optimiseur (usuellement 1.e-5), et il n'est pas recommandé
    de le changer.

    Exemple : ``{"ProjectedGradientTolerance":-1}``

  GradientNormTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la norme du gradient est en dessous de cette
    limite. C'est utilisé uniquement par les optimiseurs sans contraintes. Le
    défaut est 1.e-5 et il n'est pas recommandé de le changer.

    Exemple : ``{"GradientNormTolerance":1.e-5}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["BMA", "CostFunctionJ",
    "CostFunctionJAtCurrentOptimum", "CurrentOptimum", "CurrentState",
    "IndexOfOptimum"].

    Exemple : ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

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

Les sorties conditionnelles de l'algorithme sont les suivantes:

  BMA
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'ébauche et l'état optimal.

    Exemple : ``bma = ADD.get("BMA")[-1]``

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

  CurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'état courant utilisé
    au cours du déroulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  IndexOfOptimum
    *Liste d'entiers*. Chaque élément est l'index d'itération de l'optimum
    obtenu au cours du déroulement de l'algorithme d'optimisation. Ce n'est pas
    nécessairement le numéro de la dernière itération.

    Exemple : ``i = ADD.get("IndexOfOptimum")[-1]``

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_3DVAR`
  - :ref:`section_ref_algorithm_KalmanFilter`
  - :ref:`section_ref_algorithm_ExtendedKalmanFilter`

Références bibliographiques :
  - [Byrd95]_
  - [Morales11]_
  - [Talagrand97]_
  - [Zhu97]_
