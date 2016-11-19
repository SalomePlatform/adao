..
   Copyright (C) 2008-2016 EDF R&D

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

.. index:: single: SamplingTest
.. _section_ref_algorithm_SamplingTest:

Algorithme de vérification "*SamplingTest*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet d'établir les valeurs, liées à un état :math:`\mathbf{x}`,
d'une fonctionnelle d'erreur :math:`J` quelconque de type :math:`L^1`,
:math:`L^2` ou :math:`L^{\infty}`, avec ou sans pondérations, et de l'opérateur
d'observation, pour un échantillon d'états donné a priori. La fonctionnelle
d'erreur par défaut est celle de moindres carrés pondérés augmentés,
classiquement utilisée en assimilation de données.

Il est utile pour tester la sensibilité, de la fonctionnelle :math:`J`, en
particulier, aux variations de l'état :math:`\mathbf{x}`. Lorsque un état n'est
pas observable, une valeur *"NaN"* est retournée.

L'échantillon des états :math:`\mathbf{x}` peut être fourni explicitement ou
sous la forme d'hyper-cubes, explicites ou échantillonnés selon des lois
courantes. Attention à la taille de l'hyper-cube (et donc au nombre de calculs)
qu'il est possible d'atteindre, elle peut rapidement devenir importante.

Pour apparaître pour l'utilisateur, les résultats de l'échantillonnage doivent
être demandés explicitement. On utilise pour cela, sur la variable désirée, la
sauvegarde finale à l'aide du mot-clé "*UserPostAnalysis*" ou le traitement en
cours de calcul à l'aide des "*observer*" adaptés.

Pour effectuer un échantillonnage distribué ou plus complexe, voir d'autres
modules disponibles dans SALOME : PARAMETRIC ou OPENTURNS.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: CheckingPoint
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: SampleAsnUplet
.. index:: single: SampleAsExplicitHyperCube
.. index:: single: SampleAsMinMaxStepHyperCube
.. index:: single: SampleAsIndependantRandomVariables
.. index:: single: QualityCriterion
.. index:: single: SetDebug
.. index:: single: SetSeed
.. index:: single: StoreSupplementaryCalculations

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  CheckingPoint
    *Commande obligatoire*. Elle définit le vecteur utilisé comme l'état autour
    duquel réaliser le test requis, noté :math:`\mathbf{x}` et similaire à
    l'ébauche :math:`\mathbf{x}^b`. Sa valeur est définie comme un objet de type
    "*Vector*".

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
    *Commande obligatoire*. Elle indique l'opérateur d'observation, notée
    précédemment :math:`H`, qui transforme les paramètres d'entrée
    :math:`\mathbf{x}` en résultats :math:`\mathbf{y}` qui sont à comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est définie comme un objet de
    type "*Function*". Différentes formes fonctionnelles peuvent être
    utilisées, comme décrit dans la section
    :ref:`section_ref_operator_requirements`. Si un contrôle :math:`U` est
    inclus dans le modèle d'observation, l'opérateur doit être appliqué à une
    paire :math:`(X,U)`.

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_checking_keywords`. De plus, les
paramètres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  SampleAsnUplet
    Cette clé décrit les points de calcul sous la forme d'une liste de n-uplets,
    chaque n-uplet étant un état.

    Exemple : ``{"SampleAsnUplet":[[0,1,2,3],[4,3,2,1],[-2,3,-4,5]]}`` pour 3 points dans un espace d'état de dimension 4

  SampleAsExplicitHyperCube
    Cette clé décrit les points de calcul sous la forme d'un hyper-cube, dont on
    donne la liste des échantillonnages explicites de chaque variable comme une
    liste. C'est donc une liste de listes, chacune étant de taille
    potentiellement différente.

    Exemple : ``{"SampleAsExplicitHyperCube":[[0.,0.25,0.5,0.75,1.], [-2,2,1]]}`` pour un espace d'état de dimension 2

  SampleAsMinMaxStepHyperCube
    Cette clé décrit les points de calcul sous la forme d'un hyper-cube, dont on
    donne la liste des échantillonnages implicites de chaque variable par un
    triplet *[min,max,step]*. C'est donc une liste de la même taille que celle
    de l'état. Les bornes sont incluses.

    Exemple : ``{"SampleAsMinMaxStepHyperCube":[[0.,1.,0.25],[-1,3,1]]}`` pour un espace d'état de dimension 2

  SampleAsIndependantRandomVariables
    Cette clé décrit les points de calcul sous la forme d'un hyper-cube, dont
    les points sur chaque axe proviennent de l'échantillonnage aléatoire
    indépendant de la variable d'axe, selon la spécification de la
    distribution, de ses paramètres et du nombre de points de l'échantillon,
    sous la forme d'une liste ``['distribution', [parametres], nombre]`` pour
    chaque axe. Les distributions possibles sont 'normal' de paramètres
    (mean,std), 'lognormal' de paramètres (mean,sigma), 'uniform' de paramètres
    (low,high), ou 'weibull' de paramètre (shape). C'est donc une liste de la
    même taille que celle de l'état.

    Exemple : ``{"SampleAsIndependantRandomVariables":[ ['normal',[0.,1.],3], ['uniform',[-2,2],4]]`` pour un espace d'état de dimension 2

  QualityCriterion
    Cette clé indique le critère de qualité, qui est utilisé pour trouver
    l'estimation de l'état. Le défaut est le critère usuel de l'assimilation de
    données nommé "DA", qui est le critère de moindres carrés pondérés
    augmentés. Les critères possibles sont dans la liste suivante, dans laquelle
    les noms équivalents sont indiqués par un signe "=" :
    ["AugmentedWeightedLeastSquares"="AWLS"="DA", "WeightedLeastSquares"="WLS",
    "LeastSquares"="LS"="L2", "AbsoluteValue"="L1", "MaximumError"="ME"].

    Exemple : ``{"QualityCriterion":"DA"}``

  SetDebug
    Cette clé requiert l'activation, ou pas, du mode de débogage durant
    l'évaluation de la fonction. La valeur par défaut est "True", les choix sont
    "True" ou "False".

    Exemple : ``{"SetDebug":False}``

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

    Exemple : ``{"SetSeed":1000}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["CostFunctionJ", "CostFunctionJb",
    "CostFunctionJo", "CurrentState", "InnovationAtCurrentState",
    "SimulatedObservationAtCurrentState"].

    Exemple : ``{"StoreSupplementaryCalculations":["CostFunctionJ", "SimulatedObservationAtCurrentState"]}``

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

  CurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'état courant utilisé
    au cours du déroulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  InnovationAtCurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'innovation à l'état
    courant.

    Exemple : ``ds = ADD.get("InnovationAtCurrentState")[-1]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'état courant, c'est-à-dire dans l'espace des observations.

    Exemple : ``hxs = ADD.get("SimulatedObservationAtCurrentState")[-1]``

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`

Références vers d'autres modules SALOME :
  - PARAMETRIC, voir le *Guide utilisateur du module PARAMETRIC* dans le menu principal *Aide* de l'environnement SALOME
  - OPENTURNS, voir le *Guide utilisateur du module OPENTURNS* dans le menu principal *Aide* de l'environnement SALOME
