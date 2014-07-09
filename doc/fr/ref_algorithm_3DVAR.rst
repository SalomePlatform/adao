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

.. index:: single: 3DVAR
.. _section_ref_algorithm_3DVAR:

Algorithme de calcul "*3DVAR*"
------------------------------

Description
+++++++++++

Cet algorithme r�alise une estimation d'�tat par minimisation variationnelle de
la fonctionnelle :math:`J` d'�cart classique en assimilation de donn�es
statique:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

qui est usuellement d�sign�e comme la fonctionnelle "*3D-VAR*" (voir par exemple
[Talagrand97]_).

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Minimizer
.. index:: single: Bounds
.. index:: single: MaximumNumberOfSteps
.. index:: single: CostDecrementTolerance
.. index:: single: ProjectedGradientTolerance
.. index:: single: GradientNormTolerance
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

  Minimizer
    Cette cl� permet de changer le minimiseur pour l'optimiseur. Le choix par
    d�faut est "LBFGSB", et les choix possibles sont "LBFGSB" (minimisation non
    lin�aire sous contraintes, voir [Byrd95]_, [Morales11]_ et [Zhu97]_), "TNC"
    (minimisation non lin�aire sous contraintes), "CG" (minimisation non
    lin�aire sans contraintes), "BFGS" (minimisation non lin�aire sans
    contraintes), "NCG" (minimisation de type gradient conjugu� de Newton). Il
    est fortement conseill� de conserver la valeur par d�faut.

  Bounds
    Cette cl� permet de d�finir des bornes sup�rieure et inf�rieure pour
    chaque variable d'�tat optimis�e. Les bornes doivent �tre donn�es par une
    liste de liste de paires de bornes inf�rieure/sup�rieure pour chaque
    variable, avec une valeur ``None`` chaque fois qu'il n'y a pas de borne. Les
    bornes peuvent toujours �tre sp�cifi�es, mais seuls les optimiseurs sous
    contraintes les prennent en compte.

  MaximumNumberOfSteps
    Cette cl� indique le nombre maximum d'it�rations possibles en optimisation
    it�rative. Le d�faut est 15000, qui est tr�s similaire � une absence de
    limite sur les it�rations. Il est ainsi recommand� d'adapter ce param�tre
    aux besoins pour des probl�mes r�els. Pour certains optimiseurs, le nombre
    de pas effectif d'arr�t peut �tre l�g�rement diff�rent de la limite � cause
    d'exigences de contr�le interne de l'algorithme.

  CostDecrementTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la fonction co�t d�cro�t moins que cette
    tol�rance au dernier pas. Le d�faut est de 1.e-7, et il est recommand�
    de l'adapter aux besoins pour des probl�mes r�els.

  ProjectedGradientTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque toutes les composantes du gradient projet�
    sont en-dessous de cette limite. C'est utilis� uniquement par les
    optimiseurs sous contraintes. Le d�faut est -1, qui d�signe le d�faut
    interne de chaque optimiseur (usuellement 1.e-5), et il n'est pas recommand�
    de le changer.

  GradientNormTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la norme du gradient est en dessous de cette
    limite. C'est utilis� uniquement par les optimiseurs sans contraintes. Le
    d�faut est 1.e-5 et il n'est pas recommand� de le changer.

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs co�teux. La valeur par d�faut est une liste vide, aucune de ces
    variables n'�tant calcul�e et stock�e par d�faut. Les noms possibles sont
    dans la liste suivante : ["APosterioriCovariance", "BMA", "OMA", "OMB",
    "Innovation", "SigmaObs2", "MahalanobisConsistency"].

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_Blue`
  - :ref:`section_ref_algorithm_ExtendedBlue`
  - :ref:`section_ref_algorithm_LinearityTest`

R�f�rences bibliographiques :
  - [Byrd95]_
  - [Morales11]_
  - [Talagrand97]_
