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

Cet algorithme r�alise une estimation de l'�tat d'un syst�me dynamique par un
filtre de Kalman "unscented", permettant d'�viter de devoir calculer les
op�rateurs tangent ou adjoint pour les op�rateurs d'observation ou d'�volution,
comme dans les filtres de Kalman simple ou �tendu.

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

Les commandes requises g�n�rales, disponibles dans l'interface en �dition, sont
les suivantes:

  Background
    *Commande obligatoire*. Elle d�finit le vecteur d'�bauche ou
    d'initialisation, not� pr�c�demment :math:`\mathbf{x}^b`. Sa valeur est
    d�finie comme un objet de type "*Vector*" ou de type "*VectorSerie*".

  BackgroundError
    *Commande obligatoire*. Elle d�finit la matrice de covariance des erreurs
    d'�bauche, not�e pr�c�demment :math:`\mathbf{B}`. Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  Observation
    *Commande obligatoire*. Elle d�finit le vecteur d'observation utilis� en
    assimilation de donn�es ou en optimisation, et not� pr�c�demment
    :math:`\mathbf{y}^o`. Sa valeur est d�finie comme un objet de type "*Vector*"
    ou de type "*VectorSerie*".

  ObservationError
    *Commande obligatoire*. Elle d�finit la matrice de covariance des erreurs
    d'�bauche, not�e pr�c�demment :math:`\mathbf{R}`. Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  ObservationOperator
    *Commande obligatoire*. Elle indique l'op�rateur d'observation, not�
    pr�c�demment :math:`H`, qui transforme les param�tres d'entr�e
    :math:`\mathbf{x}` en r�sultats :math:`\mathbf{y}` qui sont � comparer aux
    observations :math:`\mathbf{y}^o`. Sa valeur est d�finie comme un objet de
    type "*Function*" ou de type "*Matrix*". Dans le cas du type "*Function*",
    diff�rentes formes fonctionnelles peuvent �tre utilis�es, comme d�crit dans
    la section :ref:`section_ref_operator_requirements`. Si un contr�le
    :math:`U` est inclus dans le mod�le d'observation, l'op�rateur doit �tre
    appliqu� � une paire :math:`(X,U)`.

Les commandes optionnelles g�n�rales, disponibles dans l'interface en �dition,
sont indiqu�es dans la :ref:`section_ref_assimilation_keywords`. En particulier,
la commande optionnelle "*AlgorithmParameters*" permet d'indiquer les options
particuli�res, d�crites ci-apr�s, de l'algorithme. On se reportera � la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  Bounds
    Cette cl� permet de d�finir des bornes sup�rieure et inf�rieure pour chaque
    variable d'�tat optimis�e. Les bornes doivent �tre donn�es par une liste de
    liste de paires de bornes inf�rieure/sup�rieure pour chaque variable, avec
    une valeur extr�me chaque fois qu'il n'y a pas de borne (``None`` n'est pas
    une valeur autoris�e lorsqu'il n'y a pas de borne).

    Exemple : ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,1.e99],[-1.e99,1.e99]]}``

  EstimationOf
    Cette cl� permet de choisir le type d'estimation � r�aliser. Cela peut �tre
    soit une estimation de l'�tat, avec la valeur "State", ou une estimation de
    param�tres, avec la valeur "Parameters". Le choix par d�faut est "State".

    Exemple : ``{"EstimationOf":"Parameters"}``

  Alpha, Beta, Kappa, Reconditioner
    Ces cl�s sont des param�tres de mise � l'�chelle interne. "Alpha" requiert
    une valeur comprise entre 1.e-4 et 1. "Beta" a une valeur optimale de 2 pour
    une distribution *a priori* gaussienne. "Kappa" requiert une valeur enti�re,
    dont la bonne valeur par d�faut est obtenue en la mettant � 0.
    "Reconditioner" requiert une valeur comprise entre 1.e-3 et 10, son d�faut
    �tant 1.

    Exemple : ``{"Alpha":1,"Beta":2,"Kappa":0,"Reconditioner":1}``

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

    Exemple : ``{"StoreInternalVariables":True}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage co�teux. La valeur par d�faut est une liste vide,
    aucune de ces variables n'�tant calcul�e et stock�e par d�faut. Les noms
    possibles sont dans la liste suivante : ["APosterioriCovariance", "BMA",
    "Innovation"].

    Exemple : ``{"StoreSupplementaryCalculations":["BMA","Innovation"]}``

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_KalmanFilter`
  - :ref:`section_ref_algorithm_ExtendedKalmanFilter`

R�f�rences bibliographiques :
  - [WikipediaUKF]_
