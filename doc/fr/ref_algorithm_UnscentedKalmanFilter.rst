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

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Bounds
.. index:: single: ConstrainedBy
.. index:: single: EstimationOf
.. index:: single: Alpha
.. index:: single: Beta
.. index:: single: Kappa
.. index:: single: Reconditioner
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

  Bounds
    Cette clé permet de définir des bornes supérieure et inférieure pour chaque
    variable d'état optimisée. Les bornes doivent être données par une liste de
    liste de paires de bornes inférieure/supérieure pour chaque variable, avec
    une valeur extrême chaque fois qu'il n'y a pas de borne (``None`` n'est pas
    une valeur autorisée lorsqu'il n'y a pas de borne).

    Exemple : ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,1.e99],[-1.e99,1.e99]]}``

  EstimationOf
    Cette clé permet de choisir le type d'estimation à réaliser. Cela peut être
    soit une estimation de l'état, avec la valeur "State", ou une estimation de
    paramètres, avec la valeur "Parameters". Le choix par défaut est "State".

    Exemple : ``{"EstimationOf":"Parameters"}``

  Alpha, Beta, Kappa, Reconditioner
    Ces clés sont des paramètres de mise à l'échelle interne. "Alpha" requiert
    une valeur comprise entre 1.e-4 et 1. "Beta" a une valeur optimale de 2 pour
    une distribution *a priori* gaussienne. "Kappa" requiert une valeur entière,
    dont la bonne valeur par défaut est obtenue en la mettant à 0.
    "Reconditioner" requiert une valeur comprise entre 1.e-3 et 10, son défaut
    étant 1.

    Exemple : ``{"Alpha":1,"Beta":2,"Kappa":0,"Reconditioner":1}``

  StoreInternalVariables
    Cette clé booléenne permet de stocker les variables internes par défaut,
    principalement l'état courant lors d'un processus itératif. Attention, cela
    peut être un choix numériquement coûteux dans certains cas de calculs. La
    valeur par défaut est "False".

    Exemple : ``{"StoreInternalVariables":True}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["APosterioriCovariance", "BMA",
    "Innovation"].

    Exemple : ``{"StoreSupplementaryCalculations":["BMA","Innovation"]}``

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_KalmanFilter`
  - :ref:`section_ref_algorithm_ExtendedKalmanFilter`

Références bibliographiques :
  - [WikipediaUKF]_
