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

.. index:: single: SamplingTest
.. _section_ref_algorithm_SamplingTest:

Algorithme de v�rification "*SamplingTest*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet d'�tablir les valeurs, li�es � un �tat :math:`\mathbf{x}`,
d'une fonctionnelle d'erreur :math:`J` quelconque de type :math:`L^1`,
:math:`L^2` ou :math:`L^{\infty}`, avec ou sans pond�rations, et de l'op�rateur
d'observation, pour un �chantillon d'�tats donn� a priori. La fonctionnelle
d'erreur par d�faut est celle de moindres carr�s pond�r�s augment�s,
classiquement utilis�e en assimilation de donn�es.

C'est un algorithme utile pour tester la sensibilit�, de la fonctionnelle
:math:`J` en particulier, aux variations de l'�tat :math:`\mathbf{x}`. Lorsque
un �tat n'est pas observable, une value *"NaN"* est retourn�e.

L'�chantillon des �tats :math:`\mathbf{x}` peut �tre fourni explicitement ou
sous la forme d'hypercubes.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: CheckingPoint
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: SampleAsnUplet
.. index:: single: SampleAsExplicitHyperCube
.. index:: single: SampleAsMinMaxStepHyperCube
.. index:: single: QualityCriterion
.. index:: single: SetDebug
.. index:: single: StoreSupplementaryCalculations

Les commandes requises g�n�rales, disponibles dans l'interface en �dition, sont
les suivantes:

  CheckingPoint
    *Commande obligatoire*. Elle d�finit le vecteur utilis� comme l'�tat autour
    duquel r�aliser le test requis, not� :math:`\mathbf{x}` et similaire �
    l'�bauche :math:`\mathbf{x}^b`. Sa valeur est d�finie comme un objet de type
    "*Vector*".

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
    *Commande obligatoire*. Elle indique l'op�rateur d'observation, not�e
    pr�c�demment :math:`H`, qui transforme les param�tres d'entr�e
    :math:`\mathbf{x}` en r�sultats :math:`\mathbf{y}` qui sont � comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est d�finie comme un objet de
    type "*Function*". Diff�rentes formes fonctionnelles peuvent �tre
    utilis�es, comme d�crit dans la section
    :ref:`section_ref_operator_requirements`. Si un contr�le :math:`U` est
    inclus dans le mod�le d'observation, l'op�rateur doit �tre appliqu� � une
    paire :math:`(X,U)`.

Les commandes optionnelles g�n�rales, disponibles dans l'interface en �dition,
sont indiqu�es dans la :ref:`section_ref_checking_keywords`. En particulier, la
commande optionnelle "*AlgorithmParameters*" permet d'indiquer les options
particuli�res, d�crites ci-apr�s, de l'algorithme. On se reportera � la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  SampleAsnUplet
    Cette cl� d�crit les points de calcul sous la forme d'une liste de n-uplets,
    chaque n-uplet �tant un �tat.

    Exemple : ``{"SampleAsnUplet":[[0,1,2,3],[4,3,2,1],[-2,3,-4,5]]}`` pour 3 points dans un espace d'�tat de dimension 4

  SampleAsExplicitHyperCube
    Cette cl� d�crit les points de calcul sous la forme d'un hyper-cube, dont on
    donne la liste des �chantillonages de chaque variable comme une liste. C'est
    donc une liste de listes, chacune �tant de taille potentiellement
    diff�rente.

    Exemple : ``{"SampleAsExplicitHyperCube":[[0.,0.25,0.5,0.75,1.],[-2,2,1]]}`` pour un espace d'�tat � 2 dimensions

  SampleAsMinMaxStepHyperCube
    Cette cl� d�crit les points de calcul sous la forme d'un hyper-cube dont on
    donne la liste des �chantillonages de chaque variable par un triplet
    *[min,max,step]*. C'est donc une liste de la m�me taille que celle de
    l'�tat. Les bornes sont incluses.

    Exemple : ``{"SampleAsMinMaxStepHyperCube":[[0.,1.,0.25],[-1,3,1]]}`` pour un espace d'�tat � 2 dimensions

  QualityCriterion
    Cette cl� indique le crit�re de qualit�, qui est utilis� pour trouver
    l'estimation de l'�tat. Le d�faut est le crit�re usuel de l'assimilation de
    donn�es nomm� "DA", qui est le crit�re de moindres carr�s pond�r�s
    augment�s. Les crit�res possibles sont dans la liste suivante, dans laquelle
    les noms �quivalents sont indiqu�s par un signe "=" :
    ["AugmentedWeightedLeastSquares"="AWLS"="DA", "WeightedLeastSquares"="WLS",
    "LeastSquares"="LS"="L2", "AbsoluteValue"="L1",  "MaximumError"="ME"].

    Exemple : ``{"QualityCriterion":"DA"}``

  SetDebug
    Cette cl� requiert l'activation, ou pas, du mode de d�bogage durant
    l'�valuation de la fonction. La valeur par d�faut est "True", les choix sont
    "True" ou "False".

    Exemple : ``{"SetDebug":False}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage co�teux. La valeur par d�faut est une liste vide,
    aucune de ces variables n'�tant calcul�e et stock�e par d�faut. Les noms
    possibles sont dans la liste suivante : ["CostFunctionJ", "CurrentState",
    "Innovation", "ObservedState"].

    Exemple : ``{"StoreSupplementaryCalculations":["CostFunctionJ", "ObservedState"]}``

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`
