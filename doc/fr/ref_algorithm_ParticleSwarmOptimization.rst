..
   Copyright (C) 2008-2014 EDF R&D

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

.. index:: single: ParticleSwarmOptimization
.. _section_ref_algorithm_ParticleSwarmOptimization:

Algorithme de calcul "*ParticleSwarmOptimization*"
--------------------------------------------------

Description
+++++++++++

Cet algorithme réalise une estimation de l'état d'un système dynamique par un
essaim particulaire.

C'est une méthode d'optimisation permettant la recherche du minimum global d'une
fonctionnelle quelconque de type :math:`L^1`, :math:`L^2` ou :math:`L^{\infty}`,
avec ou sans pondérations.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: MaximumNumberOfSteps
.. index:: single: NumberOfInsects
.. index:: single: SwarmVelocity
.. index:: single: GroupRecallRate
.. index:: single: QualityCriterion
.. index:: single: BoxBounds
.. index:: single: SetSeed
.. index:: single: StoreInternalVariables
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
sont indiquées dans la :ref:`section_ref_assimilation_keywords`. En particulier,
la commande optionnelle "*AlgorithmParameters*" permet d'indiquer les options
particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  MaximumNumberOfSteps
    Cette clé indique le nombre maximum d'itérations possibles en optimisation
    itérative. Le défaut est 50, qui est une limite arbitraire. Il est ainsi
    recommandé d'adapter ce paramètre aux besoins pour des problèmes réels.

  NumberOfInsects
    Cette clé indique le nombre d'insectes ou de particules dans l'essaim. La
    valeur par défaut est 100, qui est une valeur par défaut usuelle pour cet
    algorithme.

  SwarmVelocity
    Cette clé indique la part de la vitesse d'insecte qui est imposée par
    l'essaim. C'est une valeur réelle positive. Le défaut est de 1.

  GroupRecallRate
    Cette clé indique le taux de rappel vers le meilleur insecte de l'essaim.
    C'est une valeur réelle comprise entre 0 et 1. Le défaut est de 0.5.

  QualityCriterion
    Cette clé indique le critère de qualité, qui est minimisé pour trouver
    l'estimation optimale de l'état. Le défaut est le critère usuel de
    l'assimilation de données nommé "DA", qui est le critère de moindres carrés
    pondérés augmentés. Les critères possibles sont dans la liste suivante, dans
    laquelle les noms équivalents sont indiqués par un signe "=" :
    ["AugmentedWeightedLeastSquares"="AWLS"="DA", "WeightedLeastSquares"="WLS",
    "LeastSquares"="LS"="L2", "AbsoluteValue"="L1",  "MaximumError"="ME"]

  BoxBounds
    Cette clé permet de définir des bornes supérieure et inférieure pour chaque
    incrément de  variable d'état optimisée (et non pas chaque variable d'état
    elle-même). Les bornes doivent être données par une liste de liste de paires
    de bornes inférieure/supérieure pour chaque incrément de variable, avec une
    valeur extrême chaque fois qu'il n'y a pas de borne (``None`` n'est pas une
    valeur autorisée lorsqu'il n'y a pas de borne). Cette clé est requise et il
    n'y a pas de valeurs par défaut.

  SetSeed
    Cette clé permet de donner un nombre entier pour fixer la graine du
    générateur aléatoire utilisé pour générer l'ensemble. Un valeur pratique est
    par exemple 1000. Par défaut, la graine est laissée non initialisée, et elle
    utilise ainsi l'initialisation par défaut de l'ordinateur.

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs coûteux. La valeur par défaut est une liste vide, aucune de ces
    variables n'étant calculée et stockée par défaut. Les noms possibles sont
    dans la liste suivante : ["BMA", "OMA", "OMB", "Innovation"].

Voir aussi
++++++++++

Références bibliographiques :
  - [WikipediaPSO]_
